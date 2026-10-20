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
    def __init__(self, root):
        self.root, _ = checked_path(root, directory=True)

    def reserve(self):
        for number in range(16):
            path = self.root / ("fixture_worker_slot_%02d.used" % number)
            try:
                _write_exclusive(path, "RESERVED_NO_REFUND\n")
                return number
            except FileExistsError:
                continue
        raise ContractError("FIXTURE_WORKER_LIMIT")

    def used(self):
        return sum((self.root / ("fixture_worker_slot_%02d.used" % n)).exists()
                   for n in range(16))


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
    def __init__(self, root, run_id, planned_keys, budget, *, spawn=subprocess.Popen):
        self.root, _ = checked_path(root, directory=True)
        self.run_id = _name(run_id)
        if (type(planned_keys) is not tuple or not planned_keys
                or any(type(key) is not str or not key for key in planned_keys)
                or len(set(planned_keys)) != len(planned_keys)):
            raise ContractError("UNIQUE_PLANNED_KEYS_REQUIRED")
        self.keys, self.budget, self.spawn = planned_keys, budget, spawn
        self.children, self.started, self.terminal = {}, set(), {}
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
        self._record("PID", key=key, pid=child.pid)
        return child.pid

    def wait(self, key):
        if key not in self.children or key in self.terminal:
            raise ContractError("OWN_LIVE_CALL_REQUIRED")
        child, before, timeout = self.children[key]
        timed_out = False
        try:
            child.communicate(timeout=max(0.001, timeout - (time.monotonic() - before)))
        except subprocess.TimeoutExpired:
            # Only this stored child handle; no PID-name search or group kill.
            child.kill()
            child.communicate()
            timed_out = True
        row = Terminal(key, "RETURNED" if child.returncode == 0 and not timed_out else "FAILED",
                       child.returncode, time.monotonic() - before, timed_out)
        self.terminal[key] = row
        self._record("TERMINAL", key=key, state=row.state, exit_code=row.exit_code,
                     elapsed=row.elapsed, timed_out=timed_out)
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
            stdout, _ = child.communicate(timeout=timeout)
            if child.returncode != 0:
                raise ContractError("CPU_SCORER_FAILED")
        except Exception:
            if child is not None and child.poll() is None:
                child.kill()
                child.communicate()
            self._record("SCORING_FAILED_NO_RETRY", elapsed=time.monotonic() - before)
            raise ContractError("CPU_SCORER_FAILED_NO_RETRY") from None
        self._record("SCORING_CPU_EXIT", exit_code=child.returncode,
                     elapsed=time.monotonic() - before)
        return stdout
