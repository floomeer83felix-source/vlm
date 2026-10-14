"""Minimal real-video temporal order head. Engineering smoke, not a VLM benchmark.

Runs locally with existing PyAV, OpenCV, NumPy and PyTorch; no networking,
no private labels and no checkpoint output. Keep real clips and logs private.
"""
import argparse
import json
import math
import pathlib
import sys
import time


def emit(status, **fields):
    print(json.dumps({"status": status, **fields}, sort_keys=True), flush=True)


def extract_real_frames(video, max_frames=96):
    import av
    import cv2
    import numpy as np

    features = []
    times = []
    seen = 0
    with av.open(str(video), mode="r") as reader:
        streams = reader.streams.video
        if len(streams) != 1:
            raise ValueError("video_stream_count")
        stream = streams[0]
        for frame in reader.decode(stream):
            seen += 1
            if seen > 480:
                break
            if seen % 2 != 0:
                continue
            if frame.pts is None or frame.time_base is None:
                raise ValueError("frame_pts_missing")
            ts = float(frame.pts * frame.time_base)
            if not math.isfinite(ts) or ts < 0 or (times and ts <= times[-1]):
                raise ValueError("nonmonotonic_pts")
            rgb = frame.to_ndarray(format="rgb24")
            if rgb.ndim != 3 or rgb.shape[2] != 3:
                raise ValueError("not_rgb")
            small = cv2.resize(rgb, (8, 8), interpolation=cv2.INTER_AREA)
            features.append(small.astype(np.float32).reshape(-1) / 255.0)
            times.append(ts)
            if len(features) >= max_frames:
                break

    if len(features) < 32 or times[-1] - times[0] < 1.0:
        raise ValueError("insufficient_real_frames_or_pts")
    data = np.stack(features, axis=0)
    if not np.isfinite(data).all():
        raise ValueError("features_nonfinite")
    if float(data.std(axis=0).mean()) < 0.00005:
        raise ValueError("nearly_identical_frames")
    return data, times


def pair_batch(features, count, rng):
    import torch

    n = int(features.shape[0])
    if n < 8:
        raise ValueError("short_segment")
    first = torch.randint(0, n - 1, (count,), generator=rng)
    gaps = torch.randint(1, min(8, n), (count,), generator=rng)
    second = torch.clamp(first + gaps, max=n - 1)
    reverse = torch.randint(0, 2, (count,), generator=rng).bool()
    left = torch.where(reverse[:, None], features[second], features[first])
    right = torch.where(reverse[:, None], features[first], features[second])
    return torch.cat([left, right], dim=1), (~reverse).to(torch.float32).unsqueeze(1)


def run(video, steps, gpu_minutes):
    import numpy as np
    import torch
    from torch import nn

    if not video.is_file() or video.stat().st_size <= 0 or video.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("video_size_or_missing")
    data, times = extract_real_frames(video)
    split = max(24, int(len(data) * 0.75))
    train = torch.from_numpy(data[:split].copy())
    valid = torch.from_numpy(data[split:].copy())
    if valid.shape[0] < 8:
        raise ValueError("validation_block_short")
    if not torch.cuda.is_available():
        raise RuntimeError("cuda_unavailable")
    if torch.cuda.get_device_name(0).lower().find("3090") < 0:
        raise RuntimeError("not_rtx3090")

    torch.manual_seed(19)
    torch.cuda.reset_peak_memory_stats(0)
    start = time.monotonic()
    model = nn.Sequential(
        nn.Linear(int(train.shape[1]) * 2, 64),
        nn.ReLU(),
        nn.Linear(64, 1),
    ).to("cuda:0")
    parameter_count = sum(p.numel() for p in model.parameters())
    if parameter_count > 100_000:
        raise RuntimeError("head_too_large")
    initial = [p.detach().clone() for p in model.parameters()]
    opt = torch.optim.AdamW(model.parameters(), lr=0.002)
    criterion = nn.BCEWithLogitsLoss()
    trng = torch.Generator().manual_seed(2026)
    vrng = torch.Generator().manual_seed(3037)
    vx, vy = pair_batch(valid, 96, vrng)
    vx, vy = vx.to("cuda:0"), vy.to("cuda:0")
    losses = []
    updates = 0
    for _ in range(min(int(steps), 100)):
        torch.cuda.synchronize()
        if time.monotonic() - start >= float(gpu_minutes) * 60.0:
            break
        x, y = pair_batch(train, 16, trng)
        x, y = x.to("cuda:0"), y.to("cuda:0")
        opt.zero_grad(set_to_none=True)
        loss = criterion(model(x), y)
        if not bool(torch.isfinite(loss).item()):
            raise RuntimeError("nonfinite_loss")
        loss.backward()
        opt.step()
        updates += 1
        losses.append(float(loss.detach().item()))
        if torch.cuda.max_memory_allocated(0) > 512 * 1024 * 1024:
            raise RuntimeError("gpu_allocator_over_512mb")
    torch.cuda.synchronize()
    elapsed = time.monotonic() - start
    change = sum((p.detach() - x).abs().sum().item()
                 for p, x in zip(model.parameters(), initial))
    with torch.no_grad():
        val_prob = torch.sigmoid(model(vx))
        val_accuracy = float(((val_prob >= 0.5) == (vy >= 0.5)).float().mean().item())
    if updates < 1 or not math.isfinite(change) or change <= 0:
        raise RuntimeError("no_real_weight_update")

    emit("REAL_CC0_VIDEO_GPU_TECH_SMOKE",
         decoded_real_frames=len(data), decoded_span_seconds=round(times[-1] - times[0], 3),
         train_frames=int(train.shape[0]), validation_frames=int(valid.shape[0]),
         trainable_parameters=parameter_count, gpu_optimizer_updates=updates,
         first_train_loss=round(losses[0], 6), last_train_loss=round(losses[-1], 6),
         parameter_l1_change=round(change, 6),
         same_clip_temporal_holdout_accuracy=round(val_accuracy, 4),
         gpu_stage_seconds=round(elapsed, 3),
         torch_peak_allocated_mib=round(torch.cuda.max_memory_allocated(0) / (2**20), 2),
         scientific_benchmark=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bounded real CC0 clip CUDA training smoke")
    parser.add_argument("--video", required=True, type=pathlib.Path)
    parser.add_argument("--steps", default=80, type=int)
    parser.add_argument("--gpu-minutes", default=10, type=float)
    args = parser.parse_args()
    try:
        if not (1 <= args.steps <= 100 and 0 < args.gpu_minutes <= 20):
            raise ValueError("unsafe_budget")
        run(args.video, args.steps, args.gpu_minutes)
    except Exception as exc:
        emit("HOLD", reason=type(exc).__name__)
        sys.exit(2)
