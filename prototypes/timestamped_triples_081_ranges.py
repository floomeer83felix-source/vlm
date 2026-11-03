"""Bounded, streaming Range transfer for the unfinished 081 media acquisition.

The transport adapter only opens the fixed versioned object. It receives an
absolute response deadline and an on_connected callback; no HTTP is done here
at import time. Body data is appended/fsynced before progress is committed.
EOF/timeout retries continue from the durable prefix of the same 4 MiB chunk.
Identity, local-write and quota failures are never treated as transport retries.
"""
from pathlib import Path
import hashlib
import http.client
import os
import time

CHUNK_BYTES = 4 * 1024 * 1024
READ_BYTES = 256 * 1024
PRIOR_REQUESTS = 21
PRIOR_RANGE_CHARGE = 134757960
MAX_REQUESTS = 232
MAX_RANGE_CHARGE = 805306368
MAX_BODY_RETRIES = 16
MAX_METADATA_RETRIES = 8
OBJECT_BYTES = 28404087974
GENERATION = "1685446268139925"
ETAG = '"-CJXz5tD4nP8CEAE="'


class TransferLimitError(RuntimeError):
    pass


class ResponseIdentityError(RuntimeError):
    pass


class LocalStateError(RuntimeError):
    pass


class RangeIncompleteError(RuntimeError):
    pass


def _require(condition, reason, kind=TransferLimitError):
    if not condition:
        raise kind(reason)


class RangeBudget:
    def __init__(self, commit, *, deadline, clock=time.monotonic):
        self.commit, self.deadline, self.clock = commit, deadline, clock
        self.requests, self.range_charge = PRIOR_REQUESTS, PRIOR_RANGE_CHARGE
        self.body_retries, self.metadata_retries, self.application_bytes = 0, 0, 0

    def record(self, event, **fields):
        try:
            self.commit(event, fields)
        except Exception as exc:
            raise LocalStateError("DURABLE_LEDGER_FAILURE") from exc

    def reserve(self, start, length, kind, retry=False):
        maximum = CHUNK_BYTES if kind == "body" else 131070
        _require(kind in ("body", "metadata") and isinstance(start, int)
                 and isinstance(length, int) and 0 < length <= maximum
                 and 0 <= start < start + length <= OBJECT_BYTES, "RANGE_BOUNDS")
        _require(self.clock() < self.deadline - 1, "NETWORK_GLOBAL_DEADLINE")
        _require(self.requests < MAX_REQUESTS
                 and self.range_charge + length <= MAX_RANGE_CHARGE, "REQUEST_OR_BYTE_CAP")
        if retry:
            if kind == "body":
                _require(self.body_retries < MAX_BODY_RETRIES, "BODY_RETRY_CAP")
                self.body_retries += 1
            else:
                _require(self.metadata_retries < MAX_METADATA_RETRIES, "METADATA_RETRY_CAP")
                self.metadata_retries += 1
        self.requests += 1
        self.range_charge += length
        now = self.clock()
        request = dict(request=self.requests, start=start, length=length, kind=kind,
                       retry=bool(retry), deadline=min(self.deadline, now + (90 if kind == "body" else 30)),
                       range_charge=self.range_charge)
        self.record("REQUEST_RESERVED", **request)
        return request

    def snapshot(self):
        return dict(requests=self.requests, range_charge=self.range_charge,
                    body_retries=self.body_retries, metadata_retries=self.metadata_retries,
                    application_bytes=self.application_bytes)


class RangeClient:
    def __init__(self, open_response, budget, progress, *, sleep=time.sleep):
        self.open_response, self.budget, self.progress = open_response, budget, progress
        self.sleep = sleep

    def _progress(self, phase, request=None):
        now = self.budget.clock()
        outer = self.budget.deadline if request is None else request["deadline"]
        allowance = 15 if phase == "CONNECT" else 30
        deadline = min(outer, now + allowance) if phase in ("CONNECT", "HEADERS", "BODY") else outer
        try:
            self.progress(phase=phase, deadline=deadline, response_deadline=outer,
                          **self.budget.snapshot())
        except Exception as exc:
            raise LocalStateError("PROGRESS_WRITE_FAILURE") from exc

    def _identity(self, response, request):
        headers = {key.lower(): value for key, value in response.getheaders()}
        start, length = request["start"], request["length"]
        expected = f"bytes {start}-{start + length - 1}/{OBJECT_BYTES}"
        _require(response.status == 206 and headers.get("content-range") == expected
                 and headers.get("content-length") == str(length)
                 and headers.get("x-goog-generation") == GENERATION
                 and headers.get("etag") == ETAG
                 and headers.get("content-encoding", "identity") == "identity",
                 "HTTP_RANGE_OR_VERSION_MISMATCH", ResponseIdentityError)

    def _attempt(self, request, accept):
        """Return (complete, accepted_bytes, transport_reason), never hide local errors."""
        self._progress("CONNECT", request)
        response = None
        try:
            try:
                response = self.open_response(request, lambda: self._progress("HEADERS", request))
            except (OSError, http.client.HTTPException) as exc:
                return False, 0, type(exc).__name__
            self._identity(response, request)
            received = 0
            while received < request["length"]:
                if self.budget.clock() >= request["deadline"] - 1:
                    return False, received, "RESPONSE_DEADLINE"
                self._progress("BODY", request)
                partial_failure = None
                try:
                    data = response.read(min(READ_BYTES, request["length"] - received))
                except http.client.IncompleteRead as exc:
                    data, partial_failure = exc.partial, "IncompleteRead"
                except (OSError, http.client.HTTPException) as exc:
                    return False, received, type(exc).__name__
                _require(isinstance(data, bytes) and len(data) <= request["length"] - received,
                         "RESPONSE_OVERRUN_OR_INVALID_BYTES", ResponseIdentityError)
                if data:
                    self.budget.application_bytes += len(data)
                    # accept() failures are outside the transport catch and cannot cause another GET.
                    accept(data)
                    received += len(data)
                if partial_failure:
                    return received == request["length"], received, partial_failure
                if not data:
                    return False, received, "PREMATURE_EOF"
            return True, received, None
        finally:
            if response is not None:
                try:
                    response.close()
                except (OSError, http.client.HTTPException) as exc:
                    self.budget.record("RESPONSE_CLOSE_ERROR", request=request["request"],
                                       reason=type(exc).__name__)

    def _settle(self, request, complete, received, reason):
        self.budget.record("REQUEST_CLOSED" if complete else "REQUEST_INCOMPLETE",
                           request=request["request"], received=received,
                           requested=request["length"], reason=reason,
                           **self.budget.snapshot())
        self._progress("IDLE")

    def _pause(self):
        _require(self.budget.clock() + 2 < self.budget.deadline - 1, "NO_RETRY_TIME")
        self.sleep(2)

    def metadata(self, start, length):
        for attempt in range(2):
            buffer = bytearray()
            request = self.budget.reserve(start, length, "metadata", retry=attempt == 1)
            complete, got, reason = self._attempt(request, buffer.extend)
            self._settle(request, complete, got, reason)
            if complete:
                return bytes(buffer)
            if attempt == 0:
                self._pause()
        raise RangeIncompleteError("METADATA_INCOMPLETE_AFTER_ONE_RETRY")

    def member(self, object_start, size, path):
        _require(0 < size <= 80 * 1024 * 1024 and 0 <= object_start
                 and object_start + size <= OBJECT_BYTES, "MEMBER_BOUNDS")
        path = Path(path)
        prefix, digest = 0, hashlib.sha256()
        # New file only. Network disconnects resume inside this call, retaining durable bytes.
        with open(path, "xb", buffering=0) as output:
            while prefix < size:
                chunk_end = min(size, (prefix // CHUNK_BYTES + 1) * CHUNK_BYTES)
                for attempt in range(2):
                    request = self.budget.reserve(object_start + prefix, chunk_end - prefix,
                                                  "body", retry=attempt == 1)

                    def accept(data):
                        nonlocal prefix
                        self.budget.record("PAYLOAD_WRITE_RESERVED", prefix=prefix, length=len(data),
                                           data_sha256=hashlib.sha256(data).hexdigest())
                        try:
                            view = memoryview(data)
                            while view:
                                written = output.write(view)
                                if not written:
                                    raise OSError("ZERO_LENGTH_PAYLOAD_WRITE")
                                view = view[written:]
                            os.fsync(output.fileno())
                        except OSError as exc:
                            raise LocalStateError("PARTIAL_FILE_WRITE_FAILURE") from exc
                        digest.update(data)
                        prefix += len(data)
                        self.budget.record("PAYLOAD_COMMITTED", prefix=prefix,
                                           prefix_sha256=digest.hexdigest())

                    complete, got, reason = self._attempt(request, accept)
                    self._settle(request, complete, got, reason)
                    if complete:
                        _require(prefix == chunk_end, "CHUNK_PREFIX_MISMATCH")
                        break
                    if attempt == 0:
                        self._pause()
                else:
                    raise RangeIncompleteError("BODY_CHUNK_INCOMPLETE_AFTER_ONE_SUFFIX_RETRY")
        _require(path.stat().st_size == prefix == size, "COMPRESSED_FILE_SIZE")
        record = dict(path=str(path), compressed_bytes=size, compressed_sha256=digest.hexdigest(),
                      object_start=object_start, generation=GENERATION, etag=ETAG)
        self.budget.record("COMPRESSED_MEMBER_COMPLETE", **record)
        return record
