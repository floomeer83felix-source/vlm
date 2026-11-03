"""Append-only, durable progress for the 080 download worker/supervisor.

One writer owns a new journal. Readers keep the last complete validated record
when a write is incomplete. Neither side renames, replaces, truncates or deletes
the journal. Windows readers explicitly share read/write/delete access.
No network, model, subprocess or import-time filesystem operations.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import time

MAX_LINE_BYTES = 16384
MAX_JOURNAL_BYTES = 16 * 1024 * 1024
ZERO_HASH = "0" * 64
PHASES = {"BOOT", "CONNECT", "HEADERS", "BODY", "IDLE", "DONE", "FAILED"}


class JournalIntegrityError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise JournalIntegrityError("DUPLICATE_JSON_KEY")
        value[key] = item
    return value


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _state_valid(state):
    if state.get("phase") not in PHASES:
        raise JournalIntegrityError("INVALID_PHASE")
    for key in ("deadline", "response_deadline"):
        if not _finite(state.get(key)):
            raise JournalIntegrityError("INVALID_" + key.upper())


def _shared_read(path):
    if os.name != "nt":
        return open(path, "rb", buffering=0)
    import ctypes as C
    from ctypes import wintypes as W
    import msvcrt
    api = C.WinDLL("kernel32", use_last_error=True)
    api.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, W.LPVOID,
                               W.DWORD, W.DWORD, W.HANDLE]
    api.CreateFileW.restype = W.HANDLE
    api.CloseHandle.argtypes = [W.HANDLE]
    api.CloseHandle.restype = W.BOOL
    handle = api.CreateFileW(str(path), 0x80000000, 1 | 2 | 4, None, 3, 0x80, None)
    if handle == C.c_void_p(-1).value:
        raise C.WinError(C.get_last_error())
    try:
        fd = msvcrt.open_osfhandle(int(handle), os.O_RDONLY | os.O_BINARY)
    except BaseException:
        api.CloseHandle(handle)
        raise
    return os.fdopen(fd, "rb", buffering=0)


class ProgressWriter:
    def __init__(self, path, job_id):
        if not isinstance(job_id, str) or not job_id:
            raise ValueError("JOB_ID_REQUIRED")
        self.path, self.job_id = Path(path), job_id
        self.stream = open(self.path, "xb", buffering=0)
        self.sequence, self.previous, self.bytes_written = 0, ZERO_HASH, 0
        self.closed = False
        self.failed = False

    def append(self, **state):
        if self.closed or self.failed:
            raise ValueError("WRITER_CLOSED_OR_FAILED")
        if set(state) & {"job_id", "sequence", "previous", "digest", "epoch", "monotonic"}:
            raise ValueError("RESERVED_PROTOCOL_FIELD")
        _state_valid(state)
        record = dict(state, job_id=self.job_id, sequence=self.sequence,
                      previous=self.previous, epoch=time.time(), monotonic=time.monotonic())
        digest = hashlib.sha256(canonical(record)).hexdigest()
        record["digest"] = digest
        line = canonical(record) + b"\n"
        if len(line) > MAX_LINE_BYTES or self.bytes_written + len(line) > MAX_JOURNAL_BYTES:
            raise ValueError("JOURNAL_BYTE_LIMIT")
        try:
            view = memoryview(line)
            while view:
                written = self.stream.write(view)
                if not written:
                    raise OSError("ZERO_LENGTH_JOURNAL_WRITE")
                self.bytes_written += written
                view = view[written:]
            os.fsync(self.stream.fileno())
        except BaseException:
            self.failed = True
            raise
        self.sequence += 1
        self.previous = digest
        return record

    def close(self):
        if not self.closed:
            self.stream.close()
            self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class ProgressReader:
    def __init__(self, path, job_id):
        self.path, self.job_id = Path(path), job_id
        self.stream, self.pending, self.latest = None, b"", None
        self.sequence, self.previous, self.bytes_read = 0, ZERO_HASH, 0

    def poll(self):
        if self.stream is None:
            try:
                self.stream = _shared_read(self.path)
            except FileNotFoundError:
                return self.latest
        block = self.stream.read(65536)
        self.bytes_read += len(block)
        if self.bytes_read > MAX_JOURNAL_BYTES:
            raise JournalIntegrityError("JOURNAL_BYTE_LIMIT")
        self.pending += block
        while b"\n" in self.pending:
            line, self.pending = self.pending.split(b"\n", 1)
            if len(line) + 1 > MAX_LINE_BYTES:
                raise JournalIntegrityError("LINE_BYTE_LIMIT")
            try:
                record = json.loads(line, object_pairs_hook=_unique_object)
            except (ValueError, UnicodeError) as exc:
                raise JournalIntegrityError("INVALID_COMPLETE_RECORD") from exc
            if not isinstance(record, dict):
                raise JournalIntegrityError("RECORD_NOT_OBJECT")
            digest = record.get("digest")
            payload = {k: v for k, v in record.items() if k != "digest"}
            if (record.get("job_id") != self.job_id
                    or type(record.get("sequence")) is not int
                    or record["sequence"] != self.sequence
                    or record.get("previous") != self.previous
                    or digest != hashlib.sha256(canonical(payload)).hexdigest()):
                raise JournalIntegrityError("IDENTITY_SEQUENCE_OR_HASH_MISMATCH")
            _state_valid(record)
            if not _finite(record.get("epoch")) or not _finite(record.get("monotonic")):
                raise JournalIntegrityError("INVALID_RECORD_CLOCK")
            self.latest = record
            self.previous = digest
            self.sequence += 1
        if len(self.pending) >= MAX_LINE_BYTES:
            raise JournalIntegrityError("UNTERMINATED_LINE_BYTE_LIMIT")
        return self.latest

    def close(self):
        if self.stream is not None:
            self.stream.close()
            self.stream = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def effective_deadline(state, *, global_deadline, bootstrap_deadline):
    """Missing/partial state cannot refresh the worker's time allowance."""
    if not _finite(global_deadline) or not _finite(bootstrap_deadline):
        raise ValueError("INVALID_SUPERVISOR_DEADLINE")
    if state is None:
        return min(global_deadline, bootstrap_deadline)
    _state_valid(state)
    return min(global_deadline, state["deadline"], state["response_deadline"])
