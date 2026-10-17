"""One independent020 CPU attempt; do not execute019's suite or supervisor.

Run with --execute-once. The public020 receipt is exclusively reserved before
preflight, so a failed attempt cannot be silently replayed. No checkpoint or
fixture is persisted. The120s runtime deadline starts before resource preflight;
source authoring/Git collaboration are outside this runtime measurement.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes as w
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
LIMIT = 2 * 1024**3
SECONDS = 120
RECEIPT = ROOT / "docs/codex-artifacts/VLM-TRAIN-CPU-RUNTIME-020/cpu-runtime-verification-receipt.md"


def need(value, code):
    if not value:
        raise RuntimeError(code)


class Basic(ctypes.Structure):
    _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                ("flags", w.DWORD), ("min_ws", ctypes.c_size_t), ("max_ws", ctypes.c_size_t),
                ("active", w.DWORD), ("affinity", ctypes.c_size_t),
                ("priority", w.DWORD), ("scheduling", w.DWORD)]


class IO(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in
                ("reads", "writes", "others", "read_bytes", "write_bytes", "other_bytes")]


class Limits(ctypes.Structure):
    _fields_ = [("basic", Basic), ("io", IO), ("process_memory", ctypes.c_size_t),
                ("job_memory", ctypes.c_size_t), ("peak_process", ctypes.c_size_t),
                ("peak_job", ctypes.c_size_t)]


def system_resources():
    class Performance(ctypes.Structure):
        _fields_ = [("cb", w.DWORD)] + [(n, ctypes.c_size_t) for n in
            ("commit", "commit_limit", "commit_peak", "physical", "available",
             "cache", "kernel", "kernel_paged", "kernel_nonpaged", "page_size")] + [
            (n, w.DWORD) for n in ("handles", "processes", "threads")]
    ps = ctypes.WinDLL("psapi", use_last_error=True)
    ps.GetPerformanceInfo.argtypes = [ctypes.c_void_p, w.DWORD]
    p = Performance()
    p.cb = ctypes.sizeof(p)
    need(ps.GetPerformanceInfo(ctypes.byref(p), p.cb), "SYSTEM_MEMORY_TELEMETRY_UNKNOWN")
    need(p.page_size > 0 and p.commit_limit > p.commit and p.physical >= p.available > 0,
         "SYSTEM_MEMORY_TELEMETRY_INVALID")
    free_commit = int((p.commit_limit - p.commit) * p.page_size)
    free_physical = int(p.available * p.page_size)
    #2GiB potential child demand plus1GiB conservative host reserve.
    need(min(free_commit, free_physical) >= LIMIT + 1024**3, "SYSTEM_MEMORY_HEADROOM_HOLD")
    return {"available_commit_bytes": free_commit, "available_physical_bytes": free_physical,
            "minimum_each_bytes": LIMIT + 1024**3, "status": "PASS"}


def kernel():
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, w.LPCWSTR]
    k.CreateJobObjectW.restype = w.HANDLE
    k.SetInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD]
    k.QueryInformationJobObject.argtypes = [w.HANDLE, ctypes.c_int, ctypes.c_void_p,
                                           w.DWORD, ctypes.c_void_p]
    k.AssignProcessToJobObject.argtypes = [w.HANDLE, w.HANDLE]
    k.CreateMutexW.argtypes = [ctypes.c_void_p, w.BOOL, w.LPCWSTR]
    k.CreateMutexW.restype = w.HANDLE
    k.ReleaseMutex.argtypes = [w.HANDLE]
    k.CloseHandle.argtypes = [w.HANDLE]
    return k


def child():
    token = json.loads(sys.stdin.readline())
    need(token.get("mode") == "020_CPU_JOB_VERIFIED" and token.get("memory_limit") == LIMIT,
         "PREIMPORT_JOB_GATE_MISSING")
    deadline = float(token["deadline_monotonic"])
    need(0 < deadline - time.monotonic() <= SECONDS, "PARENT_DEADLINE_HOLD")
    from prototypes import vlm_train_head_019 as h
    from prototypes import test_vlm_train_head_019 as frozen
    # Importing these definitions/fixtures does not run019 or load Torch.
    need("torch" not in sys.modules, "UNEXPECTED_PREEXISTING_TORCH")
    result = {"status": "CPU_RUNTIME_020_HOLD", "torch_import_attempts": 0,
              "torch_import": "NOT_ATTEMPTED",
              "checks": {}, "trials": [], "step_attempts": 0, "actual_updates": 0,
              "fixture_rows": 16, "dimension": 8, "fixture_seed": 23, "head_seed": 19}
    start = time.monotonic()
    allowed = [ROOT.resolve(), Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve(),
               Path(os.environ["WINDIR"]).resolve()]

    def audit(event, args):
        if event in ("socket.connect", "socket.getaddrinfo", "subprocess.Popen"):
            raise RuntimeError("CHILD_NETWORK_OR_SUBPROCESS_FORBIDDEN")
        if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(args[0])).resolve()
            need(any(p.is_relative_to(base) for base in allowed), "PRIVATE_FILE_OPEN_FORBIDDEN")
            need(p.suffix.lower() not in (".mp4", ".webm", ".mkv", ".safetensors", ".pt", ".pth"),
                 "MEDIA_OR_WEIGHT_OPEN_FORBIDDEN")
    sys.addaudithook(audit)

    def emit():
        print("020_RESULT " + json.dumps(result), flush=True)

    try:
        result["torch_import_attempts"] = 1
        result["torch_import"] = "HOLD"
        import torch  # Sole uncached Torch/DLL import in this020 execution.
        torch.set_num_threads(1)
        result.update(torch_import="PASS", torch_version=torch.__version__)

        def no_accelerator(*args, **kwargs):
            raise RuntimeError("GPU_INITIALIZATION_FORBIDDEN")
        torch.cuda._lazy_init = no_accelerator  # Child-local guard, no CUDA call.
        from torch.utils._python_dispatch import TorchDispatchMode

        class CPUOnly(TorchDispatchMode):
            def __torch_dispatch__(self, func, types, args=(), kwargs=None):
                kwargs = kwargs or {}
                def inspect(x):
                    if isinstance(x, torch.Tensor):
                        need(x.device.type == "cpu", "NON_CPU_TENSOR_FORBIDDEN")
                    elif isinstance(x, torch.device):
                        need(x.type == "cpu", "NON_CPU_DEVICE_FORBIDDEN")
                    elif isinstance(x, (list, tuple)):
                        for y in x: inspect(y)
                    elif isinstance(x, dict):
                        for y in x.values(): inspect(y)
                inspect(args); inspect(kwargs)
                if kwargs.get("device") is not None:
                    need(torch.device(kwargs["device"]).type == "cpu", "NON_CPU_FACTORY_FORBIDDEN")
                out = func(*args, **kwargs)
                inspect(out)
                return out

        class Budget020(h.UpdateBudget):
            """New020 adapter: old019 MAX_BYTES and check method remain unchanged."""
            def check(self):
                h.require(not self.stopped, "TERMINAL_STOP")
                h.require(self.supervised is True, "HARD_SUPERVISOR_REQUIRED")
                h.require(type(self.max_updates) is int and 0 <= self.max_updates <= 12,
                          "UPDATE_LIMIT_HOLD")
                h.require(0 < self.deadline - time.monotonic() <= 120, "CPU_DEADLINE_HOLD")
                h.require(self.memory_limit_bytes == LIMIT, "020_MEMORY_CONTRACT_HOLD")
                h.require(callable(self.memory_probe) and 0 <= self.memory_probe() <= LIMIT,
                          "MEMORY_CAP")
                h.require(0 <= self.completed <= self.reserved <= self.max_updates,
                          "UPDATE_LEDGER_HOLD")

        def budget():
            return Budget020(deadline=deadline, supervised=True, memory_limit_bytes=LIMIT,
                             memory_probe=frozen.private_memory_bytes)

        original_step = torch.optim.AdamW.step
        def counted_step(optimizer, *args, **kwargs):
            need(time.monotonic() < deadline and result["step_attempts"] < 12, "GLOBAL_STEP_CAP")
            need(all(p.device.type == "cpu" for g in optimizer.param_groups for p in g["params"]),
                 "NON_CPU_OPTIMIZER")
            result["step_attempts"] += 1
            emit()  # Durable parent-captured reservation, no tensor values.
            value = original_step(optimizer, *args, **kwargs)
            result["actual_updates"] += 1
            emit()
            return value

        def trial(b, **kwargs):
            return h.run_trial(frozen.TRAIN, frozen.VALIDATION, frozen.HELDOUT, b,
                               mode=h.MODE, **kwargs)

        with CPUOnly(), mock.patch.object(torch.optim.AdamW, "step", counted_step):
            #1: real visual-only forward and upstream gradient isolation.
            head = h.make_head(8, mode=h.MODE)
            x = torch.tensor(frozen.TRAIN["embeddings"], dtype=torch.float32,
                             device="cpu", requires_grad=True)
            backbone = torch.nn.Linear(8, 8, device="cpu", dtype=torch.float32)
            backbone.requires_grad_(False)
            visual = backbone(x)
            logits = head(visual[:4], visual[4:])
            need(logits.shape == (4,) and bool(torch.isfinite(logits).all()), "VISUAL_FORWARD_HOLD")
            logits.sum().backward()
            need(x.grad is None and all(p.grad is None for p in backbone.parameters()) and
                 all(p.grad is not None for p in head.parameters()), "BACKBONE_GRADIENT_LEAK")
            need(sum(isinstance(m, torch.nn.Linear) for m in head.modules()) == 2,
                 "HEAD_LAYER_HOLD")
            result["head_parameters"] = sum(p.numel() for p in head.parameters())
            need(result["head_parameters"] <= 1_000_000, "HEAD_PARAMETER_HOLD")
            try: head({"pts": (0, 1)}, visual[:4])
            except h.Hold: pass
            else: raise RuntimeError("HEAD_ACCEPTED_METADATA")
            try: head(visual[:4], visual[4:], gold="SYNTHETIC_POISON")
            except TypeError: pass
            else: raise RuntimeError("HEAD_ACCEPTED_GOLD_FIELD")
            result["checks"]["visual_forward_and_backbone_isolation"] = "PASS"

            #2: intentionally poisoned gradient, zero optimizer reservations.
            bad = h.make_head(8, mode=h.MODE)
            next(bad.parameters()).register_hook(lambda g: g * float("nan"))
            b = budget(); before = [p.detach().clone() for p in bad.parameters()]
            with mock.patch.object(h, "make_head", return_value=bad):
                try: trial(b, updates=1)
                except h.Hold as exc: need("GRADIENT_STOP" in str(exc), "WRONG_GRADIENT_STOP")
                else: raise RuntimeError("NAN_GRADIENT_ACCEPTED")
            need(b.stopped and b.reserved == b.completed == 0 and
                 all(torch.equal(a, v) for a, v in zip(before, bad.parameters())), "BAD_GRADIENT_LEDGER")
            result["checks"]["nonfinite_gradient_terminal_stop"] = "PASS"

            #3: intentionally nonfinite loss must stop before AdamW.step.
            bad = h.make_head(8, mode=h.MODE)
            bad.register_forward_hook(lambda m, args, out: out * float("nan"))
            b = budget()
            with mock.patch.object(h, "make_head", return_value=bad):
                try: trial(b, updates=1)
                except h.Hold as exc: need("NONFINITE" in str(exc), "WRONG_LOSS_STOP")
                else: raise RuntimeError("NAN_LOSS_ACCEPTED")
            need(b.stopped and b.reserved == b.completed == 0, "BAD_LOSS_LEDGER")
            result["checks"]["nonfinite_loss_terminal_stop"] = "PASS"

            #4: injected exception is an expected negative test, not a retry.
            b = budget()
            with mock.patch.object(h, "make_head", side_effect=MemoryError("SYNTHETIC_FAULT")):
                try: trial(b, updates=1)
                except MemoryError: pass
                else: raise RuntimeError("EXCEPTION_NOT_PROPAGATED")
            need(b.stopped and b.reserved == b.completed == 0, "EXCEPTION_NOT_TERMINAL")
            result["checks"]["unexpected_exception_terminal_stop"] = "PASS"

            #5: single shared12-update ledger for all actual optimization.
            shared = budget()
            for control, steps in (("random", 0), ("trained", 4), ("trained", 4), ("shuffled", 4)):
                result["trials"].append(trial(shared, control=control, updates=steps))
                emit()
            random_head, trained, replay, shuffled = result["trials"]
            need(trained == replay, "FIXED_SEED_REPLAY_MISMATCH")
            need(random_head["parameter_l1_change"] == 0 and
                 min(trained["parameter_l1_change"], shuffled["parameter_l1_change"]) > 0,
                 "REAL_PARAMETER_CHANGE_HOLD")
            need(shared.completed == shared.reserved == result["actual_updates"] ==
                 result["step_attempts"] == 12, "GLOBAL_UPDATE_RECONCILIATION_HOLD")
            try: trial(shared, updates=1)
            except h.Hold as exc: need("TOTAL_UPDATE_CAP" in str(exc), "WRONG_UPDATE_CAP")
            else: raise RuntimeError("THIRTEENTH_UPDATE_ACCEPTED")
            need(result["actual_updates"] == 12 and shared.stopped, "POST_CAP_UPDATE_HOLD")
            result["checks"]["real_updates_controls_and_seed_replay"] = "PASS"
        need(time.monotonic() < deadline, "PARENT_DEADLINE_HOLD")
        result["status"] = "CPU_RUNTIME_020_SYNTHETIC_DYNAMIC_PASS"
    except BaseException as exc:
        result.update(error_type=type(exc).__name__, winerror=getattr(exc, "winerror", None))
        # Constant/typed errors only; never expose a runtime pathname or traceback.
        result["reason"] = str(exc) if type(exc) in (RuntimeError, h.Hold) else "RUNTIME_IMPORT_OR_DYNAMIC_HOLD"
    finally:
        result["child_wall_seconds"] = time.monotonic() - start
        emit()
    return 0 if result["status"] == "CPU_RUNTIME_020_SYNTHETIC_DYNAMIC_PASS" else 2


def execute_once():
    started = time.monotonic()
    deadline = started + SECONDS
    # Exclusive reservation survives a crash and forbids a second runtime attempt.
    with RECEIPT.open("x", encoding="utf-8") as f:
        f.write("#020 runtime execution reserved\n\nDo not replay. Verification pending.\n")
    outcome = {"status": "CPU_RUNTIME_020_HOLD", "torch_import_attempts": 0,
               "torch_import": "NOT_ATTEMPTED",
               "actual_updates": 0, "memory_limit_bytes": LIMIT, "parent_limit_seconds": SECONDS}
    p = job = mutex = k = None
    mutex_owned = False
    sources = [ROOT / "prototypes" / n for n in
               ("vlm_train_head_019.py", "test_vlm_train_head_019.py")]
    hashes = [hashlib.sha256(x.read_bytes()).hexdigest() for x in sources]
    try:
        need(os.name == "nt", "WINDOWS_SUPERVISION_UNAVAILABLE")
        outcome["system_preflight"] = system_resources()
        k = kernel()
        ctypes.set_last_error(0)
        mutex = k.CreateMutexW(None, True, "Local\\VLM-TRAIN-CPU-RUNTIME-020")
        need(mutex and ctypes.get_last_error() != 183, "CPU_RUNTIME_MUTEX_CONFLICT")
        mutex_owned = True
        job = k.CreateJobObjectW(None, None)
        need(job, "JOB_CREATE_FAILED")
        limits = Limits()
        limits.basic.flags = 0x100 | 0x200 | 0x2000
        limits.process_memory = limits.job_memory = LIMIT
        need(k.SetInformationJobObject(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)),
             "JOB_LIMIT_SETUP_FAILED")
        check = Limits()
        need(k.QueryInformationJobObject(job, 9, ctypes.byref(check), ctypes.sizeof(check), None) and
             check.process_memory == check.job_memory == LIMIT and
             check.basic.flags & limits.basic.flags == limits.basic.flags, "JOB_LIMIT_VERIFY_FAILED")
        need(time.monotonic() < deadline, "PREFLIGHT_DEADLINE_HOLD")
        env = os.environ.copy()
        env.update(CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8",
                   HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", OMP_NUM_THREADS="1")
        p = subprocess.Popen([sys.executable, "-B", str(Path(__file__).resolve()), "--020-child"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            encoding="utf-8", errors="replace", env=env, creationflags=subprocess.CREATE_NO_WINDOW)
        need(k.AssignProcessToJobObject(job, int(p._handle)), "OWN_CHILD_JOB_ASSIGN_FAILED")
        token = {"mode": "020_CPU_JOB_VERIFIED", "memory_limit": LIMIT,
                 "deadline_monotonic": deadline}
        remaining = deadline - time.monotonic()
        need(remaining > 0, "PREIMPORT_DEADLINE_HOLD")
        try:
            out, err = p.communicate(json.dumps(token) + "\n", timeout=remaining)
        except subprocess.TimeoutExpired:
            p.kill(); out, err = p.communicate()
            outcome["reason"] = "OWN_CHILD_120S_DEADLINE_STOP"
        reports = [json.loads(x[len("020_RESULT "):]) for x in out.splitlines()
                   if x.startswith("020_RESULT ")]
        if reports:
            outcome.update(reports[-1])
        if p.returncode != 0:
            outcome["status"] = "CPU_RUNTIME_020_HOLD"
        outcome["child_exit"] = p.returncode
        outcome["unstructured_stderr_present"] = bool(err.strip())
        peak = Limits()
        need(k.QueryInformationJobObject(job, 9, ctypes.byref(peak), ctypes.sizeof(peak), None),
             "JOB_PEAK_TELEMETRY_UNKNOWN")
        outcome["peak_private_commit_bytes"] = int(peak.peak_process)
        need(peak.peak_process <= LIMIT, "JOB_MEMORY_CAP_VIOLATION")
        need(time.monotonic() <= deadline, "PARENT_120S_CAP")
    except BaseException as exc:
        outcome.update(status="CPU_RUNTIME_020_HOLD", error_type=type(exc).__name__)
        outcome["reason"] = str(exc) if type(exc) is RuntimeError else "SUPERVISION_HOLD"
    finally:
        if p is not None and p.poll() is None:
            p.kill(); p.wait()
        if k is not None:
            if job: k.CloseHandle(job)
            if mutex:
                if mutex_owned: k.ReleaseMutex(mutex)
                k.CloseHandle(mutex)
        outcome["parent_wall_seconds"] = time.monotonic() - started
        outcome["frozen019_source_bytes_unchanged"] = hashes == [
            hashlib.sha256(x.read_bytes()).hexdigest() for x in sources]
        text = "# VLM-TRAIN-CPU-RUNTIME-020 — one supervised CPU attempt\n\n"
        text += "2026-10-17 (Asia/Shanghai). Anonymous measured runtime result:\n\n```json\n"
        text += json.dumps(outcome, indent=2) + "\n```\n\n"
        text += ("A new020 2GiB adapter was used;019 source/constants/suite/supervisor were not changed or rerun. "
                 "The120s runtime timer includes resource preflight, job setup, the sole child and cleanup; "
                 "code authoring and Git collaboration are outside this measurement. "
                 "Expected injected faults are negative checks, not retries. No checkpoint or feature is saved.\n\n"
                 "This is synthetic CPU evidence only. Real training data/rights, physical-source independence, "
                 "real CPU preflight, external QA benefit and GPU admission remain UNKNOWN/HOLD. "
                 "No GPU, real media/QA, private assets, research downloads, installation or environment repair. "
                 "CLOCK_ZERO_ASSUMED_NOT_CERTIFIED; NOVELTY=RETAIN0; Charades FINAL_MEDIA_STOP. "
                 "One anonymous020 result append and ordinary main push, then STOP.\n")
        RECEIPT.write_text(text, encoding="utf-8")
        print(json.dumps(outcome), flush=True)
    return 0 if outcome["status"] == "CPU_RUNTIME_020_SYNTHETIC_DYNAMIC_PASS" else 2


if __name__ == "__main__":
    if sys.argv[1:] == ["--execute-once"]:
        raise SystemExit(execute_once())
    if sys.argv[1:] == ["--020-child"]:
        raise SystemExit(child())
    raise SystemExit("Use --execute-once; no implicit execution or replay.")
