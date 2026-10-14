"""Long-video exploratory A/B: uniform vs motion-prioritized real-frame sampling.

Single public-domain film, same-clip late-block test. NOT VLM question answering,
Qwen tuning, HourVideo, or cross-video generalization. No network.
"""
import argparse
import json
import math
from pathlib import Path
import sys
import time


def decode_long(path):
    import av
    import cv2
    import numpy as np

    samples = []
    stamps = []
    next_s = 0.0
    frames_seen = 0
    with av.open(str(path), mode="r") as container:
        if len(container.streams.video) != 1:
            raise ValueError("invalid_stream_count")
        stream = container.streams.video[0]
        for frame in container.decode(stream):
            frames_seen += 1
            if frames_seen > 100000:
                raise ValueError("too_many_frames")
            if frame.pts is None or frame.time_base is None:
                raise ValueError("unverified_pts")
            ts = float(frame.pts * frame.time_base)
            if not math.isfinite(ts) or ts < 0:
                raise ValueError("invalid_pts")
            if ts < next_s:
                continue
            if stamps and ts <= stamps[-1]:
                raise ValueError("nonmonotonic_sample_pts")
            rgb = frame.to_ndarray(format="rgb24")
            thumb = cv2.resize(rgb, (8, 8), interpolation=cv2.INTER_AREA)
            samples.append(thumb.reshape(-1).astype(np.float32) / 255.0)
            stamps.append(ts)
            next_s = ts + 3.0
            if len(stamps) > 560:
                raise ValueError("unexpected_video_duration_or_frame_rate")
    if len(stamps) < 350 or stamps[-1] - stamps[0] < 20 * 60:
        raise ValueError("verified_20min_span_not_met")
    if not np.isfinite(np.stack(samples)).all():
        raise ValueError("features_nonfinite")
    return np.stack(samples), np.asarray(stamps)


def select_train_candidates(data, stamps):
    import numpy as np

    threshold = stamps[0] + 0.70 * (stamps[-1] - stamps[0])
    train_mask = stamps < threshold - 9.0
    test_mask = stamps >= threshold + 9.0
    train = data[train_mask]
    test = data[test_mask]
    train_t = stamps[train_mask]
    test_t = stamps[test_mask]
    if len(train) < 210 or len(test) < 70:
        raise ValueError("train_test_frame_quantity")
    n = 128
    uniform_idx = np.linspace(0, len(train) - 1, n).astype(np.int64)
    motion = np.empty(len(train), dtype=np.float64)
    motion[0] = 0
    motion[1:] = np.mean(np.abs(np.diff(train, axis=0)), axis=1)
    top = np.argsort(-motion, kind="stable")[:n]
    motion_idx = np.sort(top)
    validation_idx = np.linspace(0, len(test) - 1, 70).astype(np.int64)
    return (train[uniform_idx], train[motion_idx], test[validation_idx],
            train_t[uniform_idx], train_t[motion_idx], test_t[validation_idx])


def sample_pairs(seq, num, g):
    import torch

    length = len(seq)
    start = torch.randint(0, length - 10, (num,), generator=g)
    gap = torch.randint(1, 11, (num,), generator=g)
    end = start + gap
    flipped = torch.randint(0, 2, (num,), generator=g).bool()
    left = torch.where(flipped[:, None], seq[end], seq[start])
    right = torch.where(flipped[:, None], seq[start], seq[end])
    return torch.cat((left, right), 1), (~flipped).float().unsqueeze(1)


def train_arm(train, validation, seed, steps, time_deadline):
    import torch
    from torch import nn

    torch.manual_seed(seed)
    model = nn.Sequential(nn.Linear(384, 64), nn.ReLU(), nn.Linear(64, 1)).to("cuda:0")
    if sum(p.numel() for p in model.parameters()) > 100000:
        raise ValueError("model_too_large")
    frozen_initial = [p.detach().clone() for p in model.parameters()]
    opt = torch.optim.AdamW(model.parameters(), lr=0.002)
    criterion = nn.BCEWithLogitsLoss()
    tr = torch.from_numpy(train.copy())
    va = torch.from_numpy(validation.copy())
    rng = torch.Generator().manual_seed(2026)
    vrng = torch.Generator().manual_seed(2126)
    vx, vy = sample_pairs(va, 160, vrng)
    vx, vy = vx.to("cuda:0"), vy.to("cuda:0")
    loss_first = None
    loss_last = None
    count = 0
    for _ in range(steps):
        torch.cuda.synchronize()
        if time.monotonic() >= time_deadline:
            break
        xx, yy = sample_pairs(tr, 16, rng)
        xx, yy = xx.to("cuda:0"), yy.to("cuda:0")
        opt.zero_grad(set_to_none=True)
        loss = criterion(model(xx), yy)
        if not torch.isfinite(loss).item():
            raise RuntimeError("loss_nonfinite")
        loss.backward()
        if not all(torch.isfinite(p.grad).all().item() for p in model.parameters()):
            raise RuntimeError("gradient_nonfinite")
        opt.step()
        count += 1
        if loss_first is None:
            loss_first = float(loss.item())
        loss_last = float(loss.item())
        if torch.cuda.max_memory_allocated(0) > 512 * 1024 * 1024:
            raise MemoryError("torch_allocator_limit")
    torch.cuda.synchronize()
    with torch.no_grad():
        logits = model(vx)
        accuracy = float(((logits >= 0) == (vy >= 0.5)).float().mean().item())
    update_l1 = sum((p.detach() - x).abs().sum().item()
                    for p, x in zip(model.parameters(), frozen_initial))
    if count < 1 or not math.isfinite(update_l1) or update_l1 <= 0:
        raise RuntimeError("optimizer_updates_not_valid")
    return {"steps": count, "loss_first": round(loss_first, 6),
            "loss_last": round(loss_last, 6),
            "same_film_late_accuracy": round(accuracy, 4),
            "parameter_l1_change": round(update_l1, 3)}


def run(path, steps, max_gpu_minutes):
    import torch

    if not path.is_file() or path.stat().st_size <= 0 or path.stat().st_size > 96 * 1024 * 1024:
        raise ValueError("input_size_invalid")
    data, stamps = decode_long(path)
    a, b, val, at, bt, vt = select_train_candidates(data, stamps)
    if not torch.cuda.is_available() or "3090" not in torch.cuda.get_device_name(0):
        raise RuntimeError("RTX3090_CUDA_not_available")
    torch.cuda.reset_peak_memory_stats(0)
    gpu_start = time.monotonic()
    gpu_deadline = gpu_start + 60 * max_gpu_minutes
    outputs = {}
    for name, train in (("uniform_128", a), ("motion_128", b)):
        if time.monotonic() >= gpu_deadline:
            raise TimeoutError("no_time_for_paired_arm")
        outputs[name] = train_arm(train, val, 19, steps, gpu_deadline)
        if outputs[name]["steps"] < steps:
            raise TimeoutError("paired_arm_budget_incomplete")
    torch.cuda.synchronize()
    print(json.dumps({
        "status": "LONG_PUBLIC_VIDEO_TEMPORAL_AB_EXPLORATORY",
        "single_video_scientific_benchmark": False,
        "original_duration_span_s": round(float(stamps[-1] - stamps[0]), 3),
        "sampled_real_frames": len(stamps),
        "train_time_span_s_uniform": round(float(at[-1] - at[0]), 3),
        "train_time_span_s_motion": round(float(bt[-1] - bt[0]), 3),
        "validation_time_span_s": round(float(vt[-1] - vt[0]), 3),
        "train_samples_each": 128, "validation_samples": 70,
        "uniform": outputs["uniform_128"], "motion": outputs["motion_128"],
        "gpu_stage_seconds": round(time.monotonic() - gpu_start, 3),
        "torch_peak_allocated_mib": round(torch.cuda.max_memory_allocated(0) / 2**20, 3),
        "not_HourVideo_or_Qwen": True,
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--steps-per-arm", type=int, default=100)
    parser.add_argument("--gpu-minutes", type=float, default=12)
    args = parser.parse_args()
    try:
        if args.steps_per_arm < 1 or args.steps_per_arm > 100 or not 0 < args.gpu_minutes <= 12:
            raise ValueError("budget_invalid")
        run(args.video, args.steps_per_arm, args.gpu_minutes)
    except Exception as ex:
        print(json.dumps({"status": "HOLD", "reason": type(ex).__name__}), flush=True)
        sys.exit(2)
