"""Generated fixtures only. Run this file with --supervise (120s / 256MiB).

The supervisor imports no torch, starts one owned child, installs an OS private
commit limit before releasing its stdin gate, and kills only that child on a
timeout. No fixture, embedding, checkpoint or model output is written to disk.
"""
from __future__ import annotations

import ctypes
import dataclasses
import importlib.util
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import time
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prototypes import vlm_train_head_019 as h

REPORT = {"torch_status": "NOT_RUN", "trials": [], "actual_optimizer_updates": 0}
MEMORY_PROBE = lambda: 0
BUDGET = None
STDLIB_ONLY = False


def fixture():
    """Exactly16 fictional visual rows,8 dimensions; no timestamp coordinates.

    Cluster centers/noise are seeded visual surrogates, not PTS or index columns.
    Local repetition intentionally exposes the visual-similarity confound.
    """
    rng = random.Random(23)
    centers = [[rng.gauss(0, 1) for _ in range(8)] for _ in range(8)]
    rows = [[centers[i // 2][j] + rng.gauss(0, .02) for j in range(8)]
            for i in range(16)]
    return ({"source_group": "SYNTH_TRAIN", "window": (0., 8.),
             "pts": tuple(float(i) for i in range(8)), "embeddings": rows[:8]},
            {"source_group": "SYNTH_TRAIN", "window": (20., 28.),
             "pts": tuple(float(20 + i) for i in range(8)), "embeddings": rows[8:]})


TRAIN, VALIDATION = fixture()
HELDOUT = {"SYNTH_EXTERNAL": True}


def budget(**overrides):
    values = dict(max_updates=12, deadline=time.monotonic() + 90,
                  supervised=True, memory_probe=MEMORY_PROBE)
    values.update(overrides)
    return h.UpdateBudget(**values)


class StructureTests(unittest.TestCase):
    def test_import_does_not_load_torch(self):
        self.assertNotIn("torch", sys.modules)

    def test_explicit_mode_before_any_asset_or_training(self):
        b = budget()
        with self.assertRaisesRegex(h.Hold, "EXPLICIT_SYNTHETIC"):
            h.run_trial(TRAIN, VALIDATION, HELDOUT, b)
        self.assertTrue(b.stopped)
        with self.assertRaisesRegex(h.Hold, "TERMINAL_STOP"):
            b.check()

    def test_pts_missing_nonfinite_and_nonmonotone(self):
        for pts in ((), (0,), (0, None), (0, float("nan")), (0, float("inf")),
                    (0, 0), (1, 0), (-1, 0), (False, 1)):
            with self.subTest(pts=repr(pts)), self.assertRaises(h.Hold):
                h.validate_pts(pts)

    def test_time_boundary_and_extreme_pts(self):
        self.assertEqual(h.validate_pts((0., math.nextafter(0., 1.))),
                         (0., math.nextafter(0., 1.)))
        self.assertEqual(h.validate_pts((1e100, 2e100)), (1e100, 2e100))
        h.assert_isolation("SYNTH_TRAIN", (0, 8), "SYNTH_TRAIN", (8, 16), HELDOUT)
        with self.assertRaisesRegex(h.Hold, "PTS_OUTSIDE_WINDOW"):
            h.balanced_pairs((0., 1., 4., 8.), (0., 8.))

    def test_pairs_balanced_deterministic_exact_thresholds(self):
        pairs = h.balanced_pairs(TRAIN["pts"], TRAIN["window"])
        self.assertEqual(pairs, h.balanced_pairs(TRAIN["pts"], TRAIN["window"]))
        self.assertEqual((len(pairs), sum(x.target for x in pairs)), (8, 4))
        for p in pairs:
            gap = TRAIN["pts"][p.right] - TRAIN["pts"][p.left]
            self.assertTrue(gap <= 1 if p.target else gap >= 4)
        self.assertTrue(any(TRAIN["pts"][p.right] - TRAIN["pts"][p.left] == 1
                            for p in pairs if p.target))
        self.assertTrue(any(TRAIN["pts"][p.right] - TRAIN["pts"][p.left] == 4
                            for p in pairs if not p.target))

    def test_empty_classes_thresholds_and_pair_cap(self):
        for pts in ((0., .1, .2), (0., 5., 10.)):
            with self.assertRaisesRegex(h.Hold, "EMPTY_PAIR_CLASS"):
                h.balanced_pairs(pts, (0., 20.))
        for kwargs in ({"near": 0}, {"far": 1}, {"max_pairs": 17},
                       {"near": float("nan")}):
            with self.assertRaises(h.Hold):
                h.balanced_pairs(TRAIN["pts"], TRAIN["window"], **kwargs)

    def test_source_and_time_leaks(self):
        with self.assertRaisesRegex(h.Hold, "SOURCE_LEAK"):
            h.assert_isolation("SYNTH_TRAIN", (0, 8), "SYNTH_TRAIN", (20, 28),
                               {"SYNTH_TRAIN": True})
        with self.assertRaisesRegex(h.Hold, "WINDOW_LEAK"):
            h.assert_isolation("SYNTH_TRAIN", (0, 8), "SYNTH_TRAIN", (7, 16), HELDOUT)
        with self.assertRaisesRegex(h.Hold, "VALIDATION_MUST_BE_TRAIN_SOURCE"):
            h.assert_isolation("SYNTH_TRAIN", (0, 8), "SYNTH_OTHER", (20, 28), HELDOUT)

    def test_unknown_physical_evidence_holds(self):
        for evidence in ({}, {"SYNTH_EXTERNAL": None}, {"SYNTH_EXTERNAL": False}):
            with self.assertRaises(h.Hold):
                h.assert_isolation("SYNTH_TRAIN", (0, 8), "SYNTH_TRAIN", (20, 28), evidence)

    def test_qa_gold_paths_and_unknown_fields_rejected(self):
        for key in ("qa", "gold", "question", "answer", "correct_answer_label",
                    "timestamps_as_features", "uid", "path"):
            with self.subTest(key=key), self.assertRaisesRegex(h.Hold, "FORBIDDEN_INPUT_FIELD"):
                h.validate_payload(dict(TRAIN, **{key: "SYNTHETIC_POISON"}))

    def test_feature_size_and_finiteness(self):
        for rows in ([[1.] * 33] * 8, [[float("nan")]] * 8,
                     [[1.]] * 7, [[]] * 8):
            with self.assertRaises(h.Hold):
                h.validate_payload(dict(TRAIN, embeddings=rows))
        with self.assertRaises(h.Hold):
            h.validate_pts(list(range(17)))

    def test_shuffle_keeps_counts_changes_only_labels(self):
        p = h.balanced_pairs(TRAIN["pts"], TRAIN["window"])
        labels = h.shuffled_targets(p, 19)
        self.assertEqual(labels, h.shuffled_targets(p, 19))
        self.assertEqual(sorted(labels), sorted(x.target for x in p))
        self.assertNotEqual(labels, tuple(x.target for x in p))

    def test_global_reservations_cannot_reset_per_control(self):
        b = budget(max_updates=1)
        b.reserve()
        with self.assertRaisesRegex(h.Hold, "TOTAL_UPDATE_CAP"):
            b.reserve()
        self.assertEqual(b.reserved, 1)

    def test_limits_fail_closed(self):
        for options in ({"max_updates": 13}, {"supervised": False},
                        {"deadline": time.monotonic() - 1},
                        {"memory_limit_bytes": h.MAX_BYTES + 1},
                        {"memory_probe": lambda: h.MAX_BYTES + 1}):
            with self.subTest(options=list(options)), self.assertRaises(h.Hold):
                budget(**options).check()

    def test_head_mode_and_shape_reject_before_torch_import(self):
        with self.assertRaisesRegex(h.Hold, "EXPLICIT_SYNTHETIC"):
            h.make_head(8)
        for width, hidden in ((0, 8), (33, 8), (8, 129)):
            with self.assertRaisesRegex(h.Hold, "HEAD_SHAPE_HOLD"):
                h.make_head(width, hidden=hidden, mode=h.MODE)


class TorchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.torch = None
        if STDLIB_ONLY:
            REPORT["torch_status"] = "NOT_ATTEMPTED_STDLIB_ONLY"
            return
        if importlib.util.find_spec("torch") is None:
            REPORT["torch_status"] = "UNAVAILABLE_SKIP"
            return
        try:
            import torch
        except (ImportError, OSError, MemoryError) as exc:
            # Do not retry, install, increase limits or mislabel a loader failure
            # as successful training. Remaining dynamic checks are explicit skips.
            REPORT["torch_status"] = "IMPORT_RESOURCE_OR_RUNTIME_HOLD"
            REPORT["torch_import_exception"] = type(exc).__name__
            REPORT["torch_import_winerror"] = getattr(exc, "winerror", None)
            return
        cls.torch = torch
        torch.set_num_threads(1)
        REPORT["torch_status"] = "CPU_AVAILABLE"
        REPORT["torch_version"] = torch.__version__

    def setUp(self):
        if self.torch is None:
            self.skipTest(REPORT["torch_status"])

    def test_a_visual_forward_no_time_or_metadata_and_backbone_no_gradient(self):
        torch = self.torch
        head = h.make_head(8, mode=h.MODE)
        x = torch.tensor(TRAIN["embeddings"], device="cpu", dtype=torch.float32,
                         requires_grad=True)
        frozen = torch.nn.Linear(8, 8, device="cpu", dtype=torch.float32)
        frozen.requires_grad_(False)
        visual = frozen(x)
        logits = head(visual[:4], visual[4:])
        self.assertEqual(logits.shape, (4,))
        logits.sum().backward()
        self.assertIsNone(x.grad)
        self.assertTrue(all(p.grad is None and not p.requires_grad for p in frozen.parameters()))
        self.assertTrue(all(p.grad is not None for p in head.parameters()))
        self.assertLessEqual(sum(p.numel() for p in head.parameters()), 1_000_000)
        self.assertEqual(sum(isinstance(m, torch.nn.Linear) for m in head.modules()), 2)
        with self.assertRaises(h.Hold):
            head({"pts": (0, 1)}, visual[:4])
        with self.assertRaises(TypeError):
            head(visual[:4], visual[4:], gold="SYNTHETIC_POISON")

    def test_b_nonfinite_gradient_stops_before_optimizer(self):
        torch = self.torch
        head = h.make_head(8, mode=h.MODE)
        next(head.parameters()).register_hook(lambda grad: grad * float("nan"))
        b = budget()
        before = [p.detach().clone() for p in head.parameters()]
        with mock.patch.object(h, "make_head", return_value=head):
            with self.assertRaisesRegex(h.Hold, "GRADIENT_STOP"):
                h.run_trial(TRAIN, VALIDATION, HELDOUT, b, mode=h.MODE, updates=1)
        self.assertEqual((b.reserved, b.completed), (0, 0))
        self.assertTrue(b.stopped)
        self.assertTrue(all(torch.equal(a, v) for a, v in zip(before, head.parameters())))

    def test_c_nonfinite_loss_stops_before_optimizer(self):
        torch = self.torch
        head = h.make_head(8, mode=h.MODE)
        head.register_forward_hook(lambda module, args, output: output * float("nan"))
        b = budget()
        with mock.patch.object(h, "make_head", return_value=head):
            with self.assertRaisesRegex(h.Hold, "NONFINITE"):
                h.run_trial(TRAIN, VALIDATION, HELDOUT, b, mode=h.MODE, updates=1)
        self.assertEqual(b.reserved, 0)
        self.assertTrue(b.stopped)

    def test_d_unexpected_exception_is_terminal(self):
        b = budget()
        with mock.patch.object(h, "make_head", side_effect=MemoryError("SYNTHETIC_FAILURE")):
            with self.assertRaises(MemoryError):
                h.run_trial(TRAIN, VALIDATION, HELDOUT, b, mode=h.MODE, updates=1)
        self.assertTrue(b.stopped)
        self.assertEqual((b.reserved, b.completed), (0, 0))
        with self.assertRaisesRegex(h.Hold, "TERMINAL_STOP"):
            b.check()

    def test_z_real_updates_controls_and_seed_reproducibility(self):
        global BUDGET
        BUDGET = budget()
        for control, count in (("random", 0), ("trained", 4),
                               ("trained", 4), ("shuffled", 4)):
            result = h.run_trial(TRAIN, VALIDATION, HELDOUT, BUDGET,
                                 mode=h.MODE, control=control, updates=count)
            REPORT["trials"].append(result)
            REPORT["actual_optimizer_updates"] = BUDGET.completed
        random_head, trained, replay, shuffled = REPORT["trials"]
        self.assertEqual(trained, replay)
        self.assertEqual(random_head["parameter_l1_change"], 0)
        self.assertGreater(trained["parameter_l1_change"], 0)
        self.assertGreater(shuffled["parameter_l1_change"], 0)
        self.assertEqual((BUDGET.reserved, BUDGET.completed), (12, 12))
        with self.assertRaisesRegex(h.Hold, "TOTAL_UPDATE_CAP"):
            h.run_trial(TRAIN, VALIDATION, HELDOUT, BUDGET, mode=h.MODE, updates=1)
        self.assertTrue(BUDGET.stopped)
        self.assertEqual(BUDGET.completed, 12)


def windows_job():
    """Create an owned256MiB private-commit job; no other process is assigned."""
    from ctypes import wintypes as w

    class Basic(ctypes.Structure):
        _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                    ("flags", w.DWORD), ("min_working", ctypes.c_size_t),
                    ("max_working", ctypes.c_size_t), ("active", w.DWORD),
                    ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD)]

    class IO(ctypes.Structure):
        _fields_ = [(name, ctypes.c_ulonglong) for name in
                    ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]

    class Limits(ctypes.Structure):
        _fields_ = [("basic", Basic), ("io", IO), ("process_memory", ctypes.c_size_t),
                    ("job_memory", ctypes.c_size_t), ("peak_process", ctypes.c_size_t),
                    ("peak_job", ctypes.c_size_t)]

    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
    k.CreateJobObjectW.restype = w.HANDLE
    k.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
    k.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
    k.QueryInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                            w.DWORD, ctypes.c_void_p]
    k.CloseHandle.argtypes = [w.HANDLE]
    handle = k.CreateJobObjectW(None, None)
    if not handle:
        raise RuntimeError("JOB_CREATE_FAILED")
    limits = Limits()
    limits.basic.flags = 0x100 | 0x2000  # PROCESS_MEMORY | KILL_ON_JOB_CLOSE
    limits.process_memory = h.MAX_BYTES
    if not k.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
        k.CloseHandle(handle)
        raise RuntimeError("JOB_MEMORY_LIMIT_FAILED")
    return k, handle, Limits


def private_memory_bytes():
    from ctypes import wintypes as w

    class Counters(ctypes.Structure):
        _fields_ = [("cb", w.DWORD), ("faults", w.DWORD)] + [
            (name, ctypes.c_size_t) for name in ("peak_ws", "ws", "peak_paged", "paged",
                                                "peak_nonpaged", "nonpaged", "pagefile",
                                                "peak_pagefile", "private")]
    k = ctypes.WinDLL("kernel32")
    k.GetCurrentProcess.restype = w.HANDLE
    ps = ctypes.WinDLL("psapi")
    ps.GetProcessMemoryInfo.argtypes = [w.HANDLE, ctypes.c_void_p, w.DWORD]
    counter = Counters()
    counter.cb = ctypes.sizeof(counter)
    if not ps.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(counter), counter.cb):
        raise RuntimeError("MEMORY_TELEMETRY_FAILED")
    return int(counter.private)


def child():
    global MEMORY_PROBE, STDLIB_ONLY
    token = sys.stdin.readline().strip()
    if token not in ("SUPERVISED_SYNTHETIC_CPU_ONLY", "SUPERVISED_STDLIB_ONLY"):
        raise RuntimeError("SUPERVISOR_GATE_REQUIRED")
    STDLIB_ONLY = token == "SUPERVISED_STDLIB_ONLY"
    MEMORY_PROBE = private_memory_bytes
    start, cpu_start = time.perf_counter(), time.process_time()
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(StructureTests),
                                unittest.defaultTestLoader.loadTestsFromTestCase(TorchTests)])
    result = unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
    REPORT.update(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  skips=len(result.skipped), wall_seconds=time.perf_counter() - start,
                  cpu_seconds=time.process_time() - cpu_start, private_commit_bytes=MEMORY_PROBE(),
                  frame_rows=16, feature_dimension=8, fixed_seed=19, fixture_seed=23)
    if BUDGET is not None:
        REPORT["actual_optimizer_updates"] = BUDGET.completed
        REPORT["reserved_updates"] = BUDGET.reserved
    REPORT["status"] = ("TRAIN_HARNESS_SYNTHETIC_CPU_PASS" if result.wasSuccessful()
                         and REPORT["actual_optimizer_updates"] == 12 else
                         "SYNTHETIC_CPU_HARNESS_PARTIAL/HOLD")
    print("ANONYMOUS_RESULT " + json.dumps(REPORT), flush=True)
    if not result.wasSuccessful():
        return 1
    return 0 if STDLIB_ONLY or REPORT["status"] == "TRAIN_HARNESS_SYNTHETIC_CPU_PASS" else 2


def supervise(*, stdlib_only=False):
    if os.name != "nt":
        print(json.dumps({"status": "SYNTHETIC_CPU_HARNESS_PARTIAL/HOLD",
                          "reason": "WINDOWS_HARD_MEMORY_SUPERVISOR_UNAVAILABLE"}))
        return 2
    started = time.perf_counter()
    k, job, limits_type = windows_job()
    p = None
    try:
        env = os.environ.copy()
        env.update(CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1",
                   HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", OMP_NUM_THREADS="1",
                   PYTHONIOENCODING="utf-8")
        p = subprocess.Popen([sys.executable, "-B", str(Path(__file__).resolve()), "--child"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, encoding="utf-8", errors="replace", env=env,
                             creationflags=subprocess.CREATE_NO_WINDOW)
        if not k.AssignProcessToJobObject(job, int(p._handle)):
            raise RuntimeError("JOB_ASSIGN_FAILED")
        try:
            token = "SUPERVISED_STDLIB_ONLY" if stdlib_only else "SUPERVISED_SYNTHETIC_CPU_ONLY"
            out, err = p.communicate(token + "\n",
                                     timeout=max(.1, 120 - (time.perf_counter() - started)))
        except subprocess.TimeoutExpired:
            p.kill()
            out, err = p.communicate()
            print(json.dumps({"status": "SYNTHETIC_CPU_HARNESS_PARTIAL/HOLD",
                              "reason": "OWN_CHILD_HARD_120S_STOP"}))
        info = limits_type()
        if not k.QueryInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info), None):
            raise RuntimeError("JOB_PEAK_QUERY_FAILED")
        print(err, file=sys.stderr, end="")
        print(out, end="")
        print("SUPERVISOR_RESULT " + json.dumps({"child_exit": p.returncode,
              "wall_seconds": time.perf_counter() - started,
              "hard_timeout_seconds": 120, "memory_limit_bytes": h.MAX_BYTES,
              "peak_private_commit_bytes": int(info.peak_process),
              "memory_scope": "entire_child_private_commit_including_torch_import",
              "only_owned_child_supervised": True}))
        return p.returncode
    finally:
        if p is not None and p.poll() is None:
            p.kill()
            p.wait()
        k.CloseHandle(job)


if __name__ == "__main__":
    if sys.argv[1:] == ["--supervise"]:
        raise SystemExit(supervise())
    if sys.argv[1:] == ["--supervise", "--stdlib-only"]:
        raise SystemExit(supervise(stdlib_only=True))
    if sys.argv[1:] == ["--child"]:
        raise SystemExit(child())
    raise SystemExit("Use --supervise; unsupervised training is forbidden.")
