"""Synthetic CPU temporal-pair harness; no media, model, file or network adapter.

Importing this module does not import torch or train. Callers must explicitly
select synthetic_cpu_only and supply generated anonymous numeric data. PTS are
used to construct targets, never supplied to the visual head. This proxy is not
an event-order task or evidence of video-QA performance.
"""
from __future__ import annotations

import importlib
import math
import random
import time
from dataclasses import dataclass

MODE = "synthetic_cpu_only"
MAX_SAMPLES = 16
MAX_DIM = 32
MAX_UPDATES = 12
MAX_BYTES = 256 * 1024**2


class Hold(ValueError):
    """Fail closed; the caller must stop, never retry an optimizer update."""


def require(condition, code):
    if not condition:
        raise Hold(code)


def require_mode(mode):
    require(mode == MODE, "EXPLICIT_SYNTHETIC_CPU_MODE_REQUIRED")


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_pts(values):
    require(type(values) in (list, tuple) and 2 <= len(values) <= MAX_SAMPLES,
            "PTS_COUNT_OR_TYPE")
    require(all(number(v) and v >= 0 for v in values), "MISSING_OR_NONFINITE_PTS")
    require(all(b > a for a, b in zip(values, values[1:])), "PTS_NOT_INCREASING")
    return tuple(values)


def validate_window(window):
    require(type(window) in (list, tuple) and len(window) == 2 and
            all(number(x) and x >= 0 for x in window) and window[0] < window[1],
            "INVALID_HALF_OPEN_WINDOW")
    return tuple(window)


def assert_isolation(train_group, train_window, validation_group,
                     validation_window, heldout_groups):
    """Training-internal validation is distinct from external held-out sources.

    True is an explicit evidence assertion supplied by the synthetic caller;
    missing/unknown physical-source evidence holds. This cannot certify a real
    capture or infer independence from different anonymous IDs.
    """
    tw, vw = validate_window(train_window), validate_window(validation_window)
    require(type(heldout_groups) is dict and heldout_groups, "HELDOUT_EVIDENCE_MISSING")
    for group in (train_group, validation_group, *heldout_groups):
        require(type(group) is str and group.startswith("SYNTH_") and
                group.replace("_", "").isalnum(), "SYNTHETIC_GROUP_REQUIRED")
    require(all(v is True for v in heldout_groups.values()),
            "PHYSICAL_INDEPENDENCE_UNKNOWN_HOLD")
    require(train_group not in heldout_groups and validation_group not in heldout_groups,
            "TRAIN_HELDOUT_SOURCE_LEAK")
    require(train_group == validation_group, "VALIDATION_MUST_BE_TRAIN_SOURCE")
    require(tw[1] <= vw[0] or vw[1] <= tw[0], "TRAIN_VALIDATION_WINDOW_LEAK")


@dataclass(frozen=True)
class Pair:
    left: int
    right: int
    target: int


def balanced_pairs(pts, window, *, near=1.0, far=4.0, max_pairs=8):
    pts, window = validate_pts(pts), validate_window(window)
    require(number(near) and number(far) and 0 < near < far, "PAIR_THRESHOLD_HOLD")
    require(type(max_pairs) is int and 2 <= max_pairs <= 16 and max_pairs % 2 == 0,
            "PAIR_COUNT_HOLD")
    require(all(window[0] <= p < window[1] for p in pts), "PTS_OUTSIDE_WINDOW")
    positives, negatives = [], []
    for i, a in enumerate(pts):
        for j in range(i + 1, len(pts)):
            delta = pts[j] - a
            if delta <= near:
                positives.append((delta, i, j))
            elif delta >= far:
                negatives.append((delta, i, j))
    require(positives and negatives, "EMPTY_PAIR_CLASS")
    count = min(len(positives), len(negatives), max_pairs // 2)
    pos, neg = sorted(positives)[:count], sorted(negatives)[:count]
    # Stable alternating classes; indices remain outside the forward interface.
    return tuple(p for a, b in zip(pos, neg)
                 for p in (Pair(a[1], a[2], 1), Pair(b[1], b[2], 0)))


def shuffled_targets(pairs, seed):
    require(type(seed) is int and 0 <= seed <= 2**31 - 1, "SEED_HOLD")
    labels = [p.target for p in pairs]
    random.Random(seed).shuffle(labels)
    return tuple(labels)


def validate_payload(payload):
    # A whitelist also rejects unanticipated QA/gold/path/UID fields.
    require(type(payload) is dict and set(payload) ==
            {"source_group", "window", "pts", "embeddings"}, "FORBIDDEN_INPUT_FIELD")
    pts = validate_pts(payload["pts"])
    window = validate_window(payload["window"])
    require(all(window[0] <= t < window[1] for t in pts), "PTS_OUTSIDE_WINDOW")
    features = payload["embeddings"]
    if type(features) not in (list, tuple):
        torch = importlib.import_module("torch")
        require(isinstance(features, torch.Tensor) and features.device.type == "cpu",
                "CPU_NUMERIC_FEATURES_REQUIRED")
        features = features.detach().tolist()
    require(len(features) == len(pts) and all(type(x) in (list, tuple) for x in features),
            "FEATURE_ROW_COUNT")
    width = len(features[0])
    require(1 <= width <= MAX_DIM and all(len(x) == width for x in features),
            "FEATURE_DIMENSION_HOLD")
    require(all(number(v) for x in features for v in x), "NONFINITE_VISUAL_INPUT")
    return tuple(tuple(x) for x in features), pts, window


@dataclass
class UpdateBudget:
    """One shared suite ledger; reservations are consumed even on failure.

    The external supervisor enforces the OS memory/time limits. The same budget
    object is shared by all control/replay calls; it is not reset per trial.
    """
    max_updates: int = MAX_UPDATES
    deadline: float = 0.0
    memory_limit_bytes: int = MAX_BYTES
    reserved: int = 0
    completed: int = 0
    stopped: bool = False
    supervised: bool = False
    memory_probe: object = None

    def check(self):
        require(not self.stopped, "TERMINAL_STOP")
        require(self.supervised is True, "HARD_SUPERVISOR_REQUIRED")
        require(type(self.max_updates) is int and 0 <= self.max_updates <= MAX_UPDATES,
                "UPDATE_LIMIT_HOLD")
        require(number(self.deadline) and 0 < self.deadline - time.monotonic() <= 120,
                "CPU_DEADLINE_HOLD")
        require(type(self.memory_limit_bytes) is int and
                0 < self.memory_limit_bytes <= MAX_BYTES, "MEMORY_LIMIT_HOLD")
        require(callable(self.memory_probe), "MEMORY_SUPERVISOR_REQUIRED")
        used = self.memory_probe()
        require(type(used) is int and 0 <= used <= self.memory_limit_bytes, "MEMORY_CAP")
        require(0 <= self.completed <= self.reserved <= self.max_updates,
                "UPDATE_LEDGER_HOLD")

    def reserve(self):
        self.check()
        require(self.reserved < self.max_updates, "TOTAL_UPDATE_CAP")
        self.reserved += 1


def make_head(width, *, mode=None, seed=19, hidden=8):
    require_mode(mode)
    require(type(width) is int and 1 <= width <= MAX_DIM and
            type(hidden) is int and 1 <= hidden <= 128, "HEAD_SHAPE_HOLD")
    require(type(seed) is int and 0 <= seed <= 2**31 - 1, "SEED_HOLD")
    torch = importlib.import_module("torch")
    # Explicit CPU allocation and CPU-only RNG state; never choose an accelerator.
    rng = torch.random.get_rng_state()
    try:
        torch.random.default_generator.manual_seed(seed)
        layers = torch.nn.Sequential(
            torch.nn.Linear(2 * width, hidden, device="cpu", dtype=torch.float32),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden, 1, device="cpu", dtype=torch.float32))
    finally:
        torch.random.set_rng_state(rng)

    class VisualPairHead(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = layers

        def forward(self, left, right):
            require(isinstance(left, torch.Tensor) and isinstance(right, torch.Tensor),
                    "VISUAL_TENSORS_ONLY")
            require(left.device.type == right.device.type == "cpu" and
                    left.dtype == right.dtype == torch.float32, "CPU_FLOAT32_ONLY")
            require(left.ndim == right.ndim == 2 and left.shape == right.shape and
                    0 < left.shape[0] <= 16 and left.shape[1] == width,
                    "VISUAL_SHAPE_HOLD")
            require(bool(torch.isfinite(left).all()) and bool(torch.isfinite(right).all()),
                    "NONFINITE_FORWARD_INPUT")
            # Detaching prevents gradients reaching any caller-owned backbone.
            a, b = left.detach(), right.detach()
            return self.layers(torch.cat(((a - b).abs(), a * b), dim=1)).squeeze(1)

    head = VisualPairHead()
    require(sum(p.numel() for p in head.parameters()) <= 1_000_000, "HEAD_PARAM_CAP")
    return head


def run_trial(train, validation, heldout_groups, budget, *, mode=None,
              control="trained", updates=4, seed=19, learning_rate=0.01):
    """Run one bounded synthetic trial; return aggregates, never weights/features.

    The random control uses the identical initialization with zero updates.
    The shuffled control changes only training labels; validation labels retain
    their original PTS rule. No checkpoint selection or early stopping occurs.
    """
    require(isinstance(budget, UpdateBudget), "SHARED_BUDGET_REQUIRED")
    try:
        require_mode(mode)
        budget.check()
        require(control in ("trained", "random", "shuffled"), "CONTROL_HOLD")
        require(type(updates) is int and 0 <= updates <= MAX_UPDATES and
                (updates == 0 if control == "random" else updates > 0), "UPDATE_REQUEST_HOLD")
        require(updates <= budget.max_updates - budget.reserved, "TOTAL_UPDATE_CAP")
        require(number(learning_rate) and 0 < learning_rate <= 0.1, "LEARNING_RATE_HOLD")
        tx, tp, tw = validate_payload(train)
        vx, vp, vw = validate_payload(validation)
        require(len(tx) + len(vx) <= MAX_SAMPLES and len(tx[0]) == len(vx[0]),
                "TOTAL_SAMPLE_OR_DIMENSION_CAP")
        assert_isolation(train["source_group"], tw, validation["source_group"],
                         vw, heldout_groups)
        pairs, vpairs = balanced_pairs(tp, tw), balanced_pairs(vp, vw)
        labels = tuple(p.target for p in pairs)
        if control == "shuffled":
            labels = shuffled_targets(pairs, seed)
            require(labels != tuple(p.target for p in pairs), "SHUFFLE_UNCHANGED_HOLD")
        torch = importlib.import_module("torch")
        head = make_head(len(tx[0]), mode=mode, seed=seed)
        tensor = lambda x: torch.tensor(x, device="cpu", dtype=torch.float32)
        features, vf = tensor(tx), tensor(vx)
        left, right = features[[p.left for p in pairs]], features[[p.right for p in pairs]]
        vl, vr = vf[[p.left for p in vpairs]], vf[[p.right for p in vpairs]]
        target, vt = tensor(labels), tensor([p.target for p in vpairs])
        loss_fn = torch.nn.BCEWithLogitsLoss()
        before = [p.detach().clone() for p in head.parameters()]
        with torch.no_grad():
            initial_loss = float(loss_fn(head(left, right), target))
        require(math.isfinite(initial_loss), "NONFINITE_LOSS_STOP")
        optimizer = torch.optim.AdamW(head.parameters(), lr=learning_rate,
                                      weight_decay=0.01) if updates else None
        gradients_finite = True
        for _ in range(updates):
            budget.check()
            optimizer.zero_grad(set_to_none=True)
            loss = loss_fn(head(left, right), target)
            require(bool(torch.isfinite(loss)), "NONFINITE_LOSS_STOP")
            loss.backward()
            gradients_finite = all(p.grad is not None and bool(torch.isfinite(p.grad).all())
                                   for p in head.parameters())
            require(gradients_finite, "NONFINITE_OR_MISSING_GRADIENT_STOP")
            step_before = [p.detach().clone() for p in head.parameters()]
            budget.reserve()
            optimizer.step()
            budget.completed += 1
            require(all(bool(torch.isfinite(p).all()) for p in head.parameters()),
                    "NONFINITE_PARAMETER_STOP")
            require(any(not torch.equal(a, b) for a, b in
                        zip(step_before, head.parameters())), "NO_PARAMETER_UPDATE_STOP")
            budget.check()
        with torch.no_grad():
            final_loss = float(loss_fn(head(left, right), target))
            validation_loss = float(loss_fn(head(vl, vr), vt))
        require(all(math.isfinite(x) for x in (initial_loss, final_loss, validation_loss)),
                "NONFINITE_METRIC_STOP")
        change = sum(float((a - b).abs().sum()) for a, b in zip(before, head.parameters()))
        require(change > 0 if updates else change == 0, "PARAMETER_CHANGE_MISMATCH")
        return {"control": control, "updates": updates, "parameters": sum(p.numel() for p in head.parameters()),
                "initial_loss": initial_loss, "final_loss": final_loss,
                "validation_loss": validation_loss, "parameter_l1_change": change,
                "finite_gradients": gradients_finite, "train_pairs": len(pairs),
                "validation_pairs": len(vpairs), "balanced_classes": True,
                "device": "cpu", "seed": seed, "targets_changed": control == "shuffled"}
    except BaseException:
        budget.stopped = True
        raise
