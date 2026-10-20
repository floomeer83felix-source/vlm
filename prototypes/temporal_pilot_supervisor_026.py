"""026 stdlib process/journal integration. No live-model default command.

Only injected fictional workers are exercised by this task. A real worker must
later receive a gold-free projection, never the mixed annotation or an opener.
Python process ownership is real; OS ACL/gold access denial is NOT implemented.
Persistent locks are deliberately never deleted, and uncertain work cannot retry.
"""

from dataclasses import dataclass, field
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time

from temporal_evidence_adapter_025 import ContractError
from temporal_pilot_prepare_026 import checked_path


_NAME = re.compile(r"[A-Za-z0-9_-]{1,80}\Z")


def _name(value):
    if type(value) is not str or not _NAME.fullmatch(value):
        raise ContractError("SAFE_OPAQUE_NAME_REQUIRED")
    return value


def _write_exclusive(path, text):
    with open(path, "xb") as target:
        target.write(text.encode("utf-8"))
        target.flush()
        os.fsync(target.fileno())


class FixtureWorkerBudget:
    """Persistent sixteen-slot fixture cap, shared by both allowed test runs.

    Exact known slot names only, no directory inventory. Used slots never
    refund, even if spawning fails. Not an authorization for real workers.
    """
    def __init__(self, root, limit=16, runtime=None):
        self.root, _ = checked_path(root, directory=True)
        if limit not in (16, 24):
            raise ContractError("FIXTURE_SLOT_LIMIT")
        self.limit, self.runtime = limit, runtime

    def reserve(self):
        if self.runtime is not None:
            self.runtime.reserve_runtime("fixture", 5, 120, 24)
        for number in range(self.limit):
            path = self.root / ("fixture_worker_slot_%02d.used" % number)
            try:
                _write_exclusive(path, "RESERVED_NO_REFUND\n")
                return number
            except FileExistsError:
                continue
        raise ContractError("FIXTURE_WORKER_LIMIT")

    def used(self):
        return sum((self.root / ("fixture_worker_slot_%02d.used" % n)).exists()
                   for n in range(self.limit))


@dataclass(frozen=True)
class Terminal:
    key: str = field(repr=False)
    state: str
    exit_code: object
    elapsed: float
    timed_out: bool


class _HashRaw(io.RawIOBase):
    def __init__(self, source):
        super().__init__()
        self.source, self.sha = source, hashlib.sha256()
        self.count, self.eof = 0, False

    def readable(self):
        return True

    def readinto(self, buffer):
        # Fixed 64MiB ceiling; reject excess before any result is published.
        size = min(len(buffer), 64 * 1024 * 1024 - self.count + 1)
        if size <= 0:
            raise ContractError("SCORING_INPUT_LIMIT")
        chunk = self.source.read(size)
        if type(chunk) is not bytes or len(chunk) > size:
            raise ContractError("BINARY_SCORING_STREAM_REQUIRED")
        self.sha.update(chunk)
        self.count += len(chunk)
        if self.count > 64 * 1024 * 1024:
            raise ContractError("SCORING_INPUT_LIMIT")
        self.eof = not chunk
        buffer[:len(chunk)] = chunk
        return len(chunk)


class Supervisor:
    """Own Popen objects, immutable planned keys, append-and-fsync journal.

    Acquiring an existing lock always fails. No restart recovery or retry is
    inferred from an incomplete journal, terminal error or empty output file.
    """
    def __init__(self, root, run_id, planned_keys, budget, *, spawn=subprocess.Popen,
                 cohort_digest=None):
        self.root, _ = checked_path(root, directory=True)
        self.run_id = _name(run_id)
        if cohort_digest is not None:
            if not re.fullmatch(r"[0-9a-f]{64}", cohort_digest):
                raise ContractError("FIXED_COHORT_CONFIG_DIGEST_REQUIRED")
            # Same cohort/config cannot acquire another identity under a new name.
            _write_exclusive(self.root / ("cohort_" + cohort_digest + ".lock"),
                             "COHORT_CONFIG_CONSUMED_NO_RETRY\n")
        if (type(planned_keys) is not tuple or not planned_keys
                or any(type(key) is not str or not key for key in planned_keys)
                or len(set(planned_keys)) != len(planned_keys)):
            raise ContractError("UNIQUE_PLANNED_KEYS_REQUIRED")
        self.keys, self.budget, self.spawn = planned_keys, budget, spawn
        self.children, self.started, self.terminal = {}, set(), {}
        self.captures = {}
        self.queue_closed, self.scoring_consumed = False, False
        self.lock = self.root / (self.run_id + ".lock")
        self.journal = self.root / (self.run_id + ".journal.jsonl")
        _write_exclusive(self.lock, "EXCLUSIVE_OWNER_NO_RETRY\n")
        _write_exclusive(self.journal, "")
        self._record("PLAN", keys=list(self.keys), owner_pid=os.getpid())

    def _record(self, event, **values):
        record = {"event": event, **values}
        with open(self.journal, "ab") as target:
            target.write((json.dumps(record, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8"))
            target.flush()
            os.fsync(target.fileno())

    def start(self, key, command, *, timeout=5):
        if self.queue_closed or key not in self.keys or key in self.started or key in self.terminal:
            raise ContractError("CALL_CANNOT_START_OR_RETRY")
        if (type(timeout) not in (int, float) or not 0 < timeout <= 5
                or type(command) not in (list, tuple) or not command
                or any(type(arg) is not str for arg in command)):
            raise ContractError("BOUNDED_FIXTURE_COMMAND_REQUIRED")
        slot = self.budget.reserve()
        self.started.add(key)
        self._record("STARTED", key=key, slot=slot, reserved_timeout=timeout)
        before = time.monotonic()
        try:
            child = self.spawn(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            row = Terminal(key, "FAILED", None, time.monotonic() - before, False)
            self.terminal[key] = row
            self._record("TERMINAL", key=key, state="FAILED", exit_code=None,
                         elapsed=row.elapsed, timed_out=False)
            raise ContractError("SPAWN_FAILED_NO_RETRY") from None
        self.children[key] = (child, before, timeout)
        self.captures[key] = _Capture(child)
        self.captures[key].watch(child, before + timeout)
        self._record("PID", key=key, pid=child.pid)
        return child.pid

    def wait(self, key):
        if key not in self.children or key in self.terminal:
            raise ContractError("OWN_LIVE_CALL_REQUIRED")
        child, before, timeout = self.children[key]
        timed_out = False
        capture = self.captures[key]
        capture.monitor.join(timeout=max(0.001, before + timeout + 0.95 - time.monotonic()))
        if capture.monitor.is_alive() or capture.error:
            raise ContractError("OWN_MONITOR_CLEANUP_HOLD")
        timed_out, overflow = capture.result
        row = Terminal(key, "RETURNED" if child.returncode == 0 and not timed_out and not overflow else "FAILED",
                       child.returncode, time.monotonic() - before, timed_out)
        self.terminal[key] = row
        self._record("TERMINAL", key=key, state=row.state, exit_code=row.exit_code,
                     elapsed=row.elapsed, timed_out=timed_out, output_overflow=overflow)
        return row

    def close_queue(self):
        if any(child.poll() is None for child, _, _ in self.children.values()):
            raise ContractError("CHILDREN_STILL_LIVE")
        if any(key not in self.terminal for key in self.started):
            raise ContractError("WAIT_RECORDS_REQUIRED")
        for key in self.keys:
            if key not in self.terminal:
                self.terminal[key] = Terminal(key, "NOT_RUN", None, 0.0, False)
                self._record("TERMINAL", key=key, state="NOT_RUN", exit_code=None,
                             elapsed=0.0, timed_out=False)
        self.queue_closed = True
        self._record("QUEUE_CLOSED", planned_n=len(self.keys))

    def score_once(self, opener, scorer, expected_digest, expected_size):
        """Fictional streams in026; digest is checked before returning a result.

        File identity/rights and actual gold-denying OS isolation must be
        independently verified by a future authorized wrapper. Byte binding
        alone is not an OS security boundary or a source provenance certificate.
        """
        if self.scoring_consumed:
            raise ContractError("SCORING_ALREADY_CONSUMED")
        if (not self.queue_closed or len(self.terminal) != len(self.keys)
                or any(child.poll() is None for child, _, _ in self.children.values())):
            raise ContractError("SCORING_BEFORE_REAL_CHILD_EXITS")
        self._record("SCORING_CONSUMED")
        self.scoring_consumed = True
        source = text = None
        try:
            source = opener()
            raw = _HashRaw(source)
            text = io.TextIOWrapper(io.BufferedReader(raw), encoding="utf-8-sig")
            result = scorer(text)
            if (not raw.eof or raw.count != expected_size
                    or raw.sha.hexdigest() != expected_digest):
                raise ContractError("SNAPSHOT_BINDING_HOLD")
            text.close()
            source.close()
        except Exception:
            self._record("SCORING_FAILED_NO_RETRY")
            raise ContractError("SCORING_OR_BINDING_HOLD_NO_RETRY") from None
        finally:
            for resource in (text, source):
                if resource is not None:
                    try:
                        resource.close()
                    except Exception:
                        pass
        self._record("SCORING_PUBLISHED")
        return result

    def score_child_once(self, command, *, timeout=5):
        """Separate CPU entry, after owned generation children have exited.

        Only an invented CPU scoring command is tested in026. The future
        trusted scorer must itself perform the bound one-pass read and withhold
        output on a mismatch; this method does not accept a boolean proof of it.
        No annotation/opener is ever sent to a generation child by this API.
        """
        if self.scoring_consumed:
            raise ContractError("SCORING_ALREADY_CONSUMED")
        if (not self.queue_closed or len(self.terminal) != len(self.keys)
                or any(child.poll() is None for child, _, _ in self.children.values())):
            raise ContractError("SCORING_BEFORE_REAL_CHILD_EXITS")
        if (type(timeout) not in (int, float) or not 0 < timeout <= 5
                or type(command) not in (list, tuple) or not command
                or any(type(arg) is not str for arg in command)):
            raise ContractError("BOUNDED_CPU_SCORER_COMMAND_REQUIRED")
        self._record("SCORING_CONSUMED")
        self.scoring_consumed = True
        slot = self.budget.reserve()
        before = time.monotonic()
        child = None
        try:
            child = self.spawn(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self._record("SCORING_CPU_PID", pid=child.pid, slot=slot)
            capture = _Capture(child)
            timed_out, overflow = _finish_owned(child, capture, before + timeout)
            stdout = bytes(capture.data[0])
            if child.returncode != 0 or timed_out or overflow:
                raise ContractError("CPU_SCORER_FAILED")
        except Exception:
            if child is not None and child.poll() is None:
                child.kill()
                child.wait(timeout=0.5)
            self._record("SCORING_FAILED_NO_RETRY", elapsed=time.monotonic() - before)
            raise ContractError("CPU_SCORER_FAILED_NO_RETRY") from None
        self._record("SCORING_CPU_EXIT", exit_code=child.returncode,
                     elapsed=time.monotonic() - before)
        return stdout

    def bound_fixture_score(self, command_factory, binding, *, mode="full"):
        """One independent CPU child does BOTH stream binding and batch scoring.

        Only invented inputs are supported. Binding is not a real gold grant.
        Parent publishes only after successful child exit and matching receipt.
        """
        payload = dict(binding, mode=mode)
        raw = self.score_child_once(command_factory(payload), timeout=4)
        try:
            result = json.loads(raw)
            if (result.get("digest") != binding["digest"] or result.get("size") != binding["size"]
                    or result.get("status") != "PASS" or result.get("scorer_pid") == os.getpid()):
                raise ValueError()
        except Exception:
            self._record("SCORING_BINDING_HOLD")
            raise ContractError("SCORING_CHILD_BINDING_HOLD_NO_RETRY") from None
        self._record("SCORING_PUBLISHED")
        return result


class _Capture:
    """Drain concurrently, retaining at most64KiB on each pipe."""
    def __init__(self, child):
        self.data, self.overflow, self.threads = [bytearray(), bytearray()], threading.Event(), []
        self.result, self.error = None, False
        def drain(pipe, index):
            try:
                while True:
                    chunk = pipe.read(4096)
                    if not chunk:
                        break
                    remaining = 65536 - len(self.data[index])
                    self.data[index].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        self.overflow.set()
            finally:
                pipe.close()
        for index, pipe in enumerate((child.stdout, child.stderr)):
            thread = threading.Thread(target=drain, args=(pipe, index), daemon=True)
            thread.start()
            self.threads.append(thread)

    def watch(self, child, deadline):
        def monitor():
            try:
                self.result = _finish_owned(child, self, deadline)
            except Exception:
                self.error = True
        self.monitor = threading.Thread(target=monitor, daemon=True)
        self.monitor.start()


def _finish_owned(child, capture, deadline):
    timed_out = False
    while child.poll() is None:
        if capture.overflow.is_set() or time.monotonic() >= deadline:
            timed_out = time.monotonic() >= deadline
            child.kill()  # Stored handle only; never job/process-name lookup.
            break
        time.sleep(min(0.01, max(0.001, deadline - time.monotonic())))
    child.wait(timeout=0.5)
    for thread in capture.threads:
        thread.join(timeout=0.2)
    if any(thread.is_alive() for thread in capture.threads):
        raise ContractError("OWN_PIPE_CLEANUP_HOLD")
    return timed_out, capture.overflow.is_set()


def fixture_score_child(payload):
    """Invented fixture only. One open, no score output until full raw binding."""
    from dataclasses import asdict
    from temporal_pilot_prepare_026 import InputBudget
    from temporal_evidence_adapter_025 import (
        QuestionKey, QuestionRecord, Projection, SourceRecord, TASK, build_plan,
    )
    from temporal_evidence_scorer_025 import (
        OneShotScorer, TerminalAttempt, FrozenLedger, ChildExitReceipt,
    )
    budget = InputBudget()
    budget.register("invented_scoring", payload["path"], 1024 * 1024)
    key = QuestionKey("fictional", 0)
    plan = build_plan(Projection("screen", (SourceRecord("fictional", ()),),
                                (QuestionRecord(key, TASK,
                                 "How long after folding paper did a robot open a box?"),)))
    ledger = FrozenLedger(tuple(TerminalAttempt(c, "RETURNED", "A") for c in plan.calls), True)
    class NonClosing:
        def __init__(self, stream):
            self.stream = stream
        def read(self, *args):
            return self.stream.read(*args)
        def close(self):
            pass
    with budget.text("invented_scoring") as stream:
        if payload["mode"] == "fail":
            raise ContractError("INVENTED_SCORER_FAILURE")
        if payload["mode"] == "half":
            stream.read(1)
            raise ContractError("INVENTED_HALF_READ_HOLD")
        report = OneShotScorer().score(lambda: NonClosing(stream), plan, ledger,
                                     ChildExitReceipt(("observed-exited",), ("observed-exited",), True))
    receipt = budget.receipts[-1]
    if (not receipt.complete or receipt.digest != payload["digest"]
            or receipt.byte_count != payload["size"] or report.status != "PASS"):
        raise ContractError("SCORING_SNAPSHOT_HOLD")
    print(json.dumps(dict(status="PASS", digest=receipt.digest, size=receipt.byte_count,
                          scorer_pid=os.getpid(), report=asdict(report))))
