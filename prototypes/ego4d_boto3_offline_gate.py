"""SYNTHETIC_ONLY: stdlib mapping and GET-budget simulation, never an SDK client.

python -B prototypes/ego4d_boto3_offline_gate.py --synthetic
python -B prototypes/ego4d_boto3_offline_gate.py --synthetic --self-test
Only internally owned tempfile ledgers are supported; no input file flags.
Live access, credentials, real release bridges and transport: NOT AUTHORIZED.
"""
import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit

GIB = 1024 ** 3
MEDIA_LIMIT, TOTAL_LIMIT, META_LIMIT = 4 * GIB, 8 * GIB, 32 * 1024 ** 2
VERSION = "SYNTH_EGO_GATE_V1"
RELEASES = ("v1", "v2", "v2_1")


class GateError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise GateError(message)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, allow_nan=False).encode()).hexdigest()


def synthetic_id(value):
    return type(value) is str and re.fullmatch(r"SYNTH_[A-Z0-9_]+", value) is not None


def manifest_key(release, dataset):
    need(release in RELEASES, "UNKNOWN_RELEASE")
    need(dataset == "full_scale", "EXPLICIT_FULL_SCALE_REQUIRED")
    return f"public/{release}/{dataset}/manifest.csv"


def check_uri(uri, release, uid, buckets):
    need(type(uri) is str and not any(c in uri for c in ("\\", "%", "?", "#", "@")),
         "BAD_URI")
    parts = urlsplit(uri)
    need(parts.scheme == "s3" and parts.netloc in buckets and
         synthetic_id(parts.netloc) and not parts.query and not parts.fragment,
         "UNTRUSTED_SYNTHETIC_SOURCE")
    need(parts.path == f"/public/{release}/full_scale/{uid}.mp4", "KEY_IDENTITY_MISMATCH")
    return uri


def join_manifest(text, requested, release, dataset, buckets=("SYNTH_BUCKET",),
                  SYNTH_BRIDGE_CONFIRMED=False):
    """Stricter fictional policy, not a parser claiming to validate real releases."""
    manifest_key(release, dataset)
    need(SYNTH_BRIDGE_CONFIRMED is True, "RELEASE_BRIDGE_UNKNOWN")
    need(type(text) is str and 1 <= len(requested) <= 2 and
         len(set(requested)) == len(requested) and all(synthetic_id(x) for x in requested),
         "BAD_SYNTHETIC_UID_SET")
    reader = csv.DictReader(io.StringIO(text))
    names = reader.fieldnames or []
    need(len(names) == len(set(names)) and "video_uid" in names, "VIDEO_UID_REQUIRED")
    found = {}
    for row in reader:
        need(None not in row and all(v is not None for v in row.values()), "BAD_CSV_ROW")
        uid = row["video_uid"]
        need(synthetic_id(uid), "SYNTHETIC_UID_REQUIRED")
        need(not row.get("file_uid"), "FILE_UID_NOT_VIDEO_UID")
        uris = [row[k] for k in ("canonical_s3_location", "s3_path") if row.get(k)]
        need(uris and len(set(uris)) == 1, "MISSING_OR_CONFLICTING_SOURCE")
        check_uri(uris[0], release, uid, buckets)
        need(uid not in found, "DUPLICATE_UID_AMBIGUOUS")
        found[uid] = uris[0]
    need(all(uid in found for uid in requested), "UID_NOT_FOUND")
    return tuple((uid, found[uid]) for uid in requested)


@dataclass(frozen=True)
class Request:
    uid: str
    uri: str
    kind: str
    length: int
    etag: str = "SYNTH_ETAG"
    version_id: str = "SYNTH_OBJECT_VERSION"

    def validate(self, release):
        need(synthetic_id(self.uid) and synthetic_id(self.etag) and
             synthetic_id(self.version_id), "SYNTHETIC_IDENTITY_REQUIRED")
        need(self.kind in ("media", "metadata"), "BAD_REQUEST_KIND")
        need(type(self.length) is int and self.length > 0, "UNKNOWN_LENGTH")
        limit = MEDIA_LIMIT if self.kind == "media" else META_LIMIT
        need(self.length <= limit, "OBJECT_LENGTH_LIMIT")
        if self.kind == "media":
            check_uri(self.uri, release, self.uid, ("SYNTH_BUCKET",))
        else:
            need(self.uri == f"s3://SYNTH_BUCKET/{manifest_key(release, 'full_scale')}",
                 "BAD_METADATA_SOURCE")


@dataclass(frozen=True)
class Response:
    chunks: tuple[int, ...]
    content_length: int
    status: int = 200
    etag: str = "SYNTH_ETAG"
    version_id: str = "SYNTH_OBJECT_VERSION"
    encoding: str = "identity"
    redirected: bool = False
    retry: bool = False


def live_access(*args, **kwargs):
    raise GateError("LIVE_ACCESS_NOT_AUTHORIZED")


def owned_root(root):
    root = Path(root)
    need(root.name == "run" and root.parent.name.startswith("vlm-ego-synth-") and
         root.parent.parent.resolve() == Path(tempfile.gettempdir()).resolve() and
         not root.is_symlink() and not root.parent.is_symlink(), "OWNED_TEMP_REQUIRED")
    need((root.parent / "owner").read_text() == VERSION and root.is_dir() and
         not any(p.is_symlink() for p in root.iterdir()), "UNSAFE_ROOT")


class Lock:
    def __init__(self, root):
        self.root, self.f = root, None

    def __enter__(self):
        owned_root(self.root)
        self.f = (self.root / "lock").open("a+b")
        if self.f.seek(0, 2) == 0:
            self.f.write(b"0"); self.f.flush()
        self.f.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.f.close()
            raise GateError("LOCK_CONFLICT") from None
        return self

    def __exit__(self, *args):
        try:
            self.f.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.f.fileno(), fcntl.LOCK_UN)
        finally:
            self.f.close()


class Workspace:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vlm-ego-synth-")
        parent = Path(self.temp.name)
        (parent / "owner").write_text(VERSION)
        self.root = parent / "run"; self.root.mkdir()
        return self.root

    def __exit__(self, *args):
        with Lock(self.root):
            pass
        self.temp.cleanup()


def atomic(path, obj):
    need(not path.exists(), "IMMUTABLE_SNAPSHOT_EXISTS")
    pending = path.with_suffix(".pending")
    with pending.open("x", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, allow_nan=False)
        f.flush(); os.fsync(f.fileno())
    os.replace(pending, path)


class Ledger:
    def __init__(self, root, requests, release="v2_1", resume=False, run_id="SYNTH_RUN"):
        self.root, self.requests = Path(root), tuple(requests)
        manifest_key(release, "full_scale")
        need(synthetic_id(run_id), "BAD_RUN_ID")
        need(0 < len(requests) <= 3 and len({r.uid for r in requests}) == len(requests)
             and len({r.uri for r in requests}) == len(requests), "DUPLICATE_OBJECT")
        for r in requests:
            need(type(r) is Request, "BAD_REQUEST")
            r.validate(release)
        need(sum(r.kind == "media" for r in requests) <= 2, "TWO_MEDIA_LIMIT")
        need(sum(r.length for r in requests) <= TOTAL_LIMIT, "TOTAL_BUDGET")
        need(sum(r.length for r in requests if r.kind == "metadata") <= META_LIMIT,
             "METADATA_BUDGET")
        self.contract = {"run_id": run_id, "release": release, "code_version": VERSION,
                         "source_hash": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         "requests": [asdict(r) for r in requests],
                         "limits": [MEDIA_LIMIT, TOTAL_LIMIT, META_LIMIT, 2]}
        with Lock(self.root):
            if resume:
                self._load()
            else:
                need(not list(self.root.glob("snapshot_*.json")) and
                     not list(self.root.glob("*.pending")), "LEDGER_ALREADY_EXISTS")
                self._save({"contract": self.contract, "records": {}})

    def _save(self, state):
        need(not list(self.root.glob("*.pending")), "PENDING_WRITE_STOP")
        snapshots = sorted(self.root.glob("snapshot_*.json"))
        previous = sha(json.loads(snapshots[-1].read_text())) if snapshots else None
        envelope = {"state": state, "checksum": sha(state), "previous": previous}
        try:
            atomic(self.root / f"snapshot_{len(snapshots):06d}.json", envelope)
        except OSError:
            raise GateError("PERSISTENCE_STOP_NO_RETRY") from None

    def latest_path(self):
        return sorted(self.root.glob("snapshot_*.json"))[-1]

    def _load(self):
        try:
            need(not list(self.root.glob("*.pending")), "PENDING_WRITE_STOP")
            snapshots = sorted(self.root.glob("snapshot_*.json"))
            need(bool(snapshots), "NO_SNAPSHOT")
            previous = None
            for index, path in enumerate(snapshots):
                need(path.name == f"snapshot_{index:06d}.json", "SNAPSHOT_SEQUENCE_GAP")
                envelope = json.loads(path.read_text())
                need(envelope["previous"] == previous and
                     envelope["checksum"] == sha(envelope["state"]), "LEDGER_CHECKSUM")
                previous = sha(envelope)
            state = envelope["state"]
            need(envelope["checksum"] == sha(state), "LEDGER_CHECKSUM")
            need(state["contract"] == self.contract, "CONTRACT_CHANGED")
            allowed = {r.uid: r for r in self.requests}
            need(set(state["records"]) <= set(allowed), "UNKNOWN_LEDGER_UID")
            for uid, rec in state["records"].items():
                need(rec["reserved"] == allowed[uid].length and
                     type(rec["actually_read"]) is int and 0 <= rec["actually_read"] <= rec["reserved"]
                     and rec["status"] in ("STARTED", "COMPLETE", "FAILED"), "BAD_LEDGER_RECORD")
            need(sum(r["reserved"] for r in state["records"].values()) <= TOTAL_LIMIT,
                 "LEDGER_OVER_BUDGET")
            return state
        except (OSError, KeyError, TypeError, json.JSONDecodeError):
            raise GateError("LEDGER_UNREADABLE") from None

    def transfer(self, uid, response, crash_after_start=False, interrupt_after=None):
        """Integers represent offered chunk sizes; no bytes/network are allocated.

        Full upper bound is durable before invoking any simulated response read.
        Offered overlong chunks are rejected BEFORE acceptance (not a claim about
        counting already-received live HTTP buffers). No refunds or retries.
        """
        with Lock(self.root):
            state = self._load()
            request = next((r for r in self.requests if r.uid == uid), None)
            need(request is not None, "UNPLANNED_OBJECT")
            need(uid not in state["records"], "NO_REPEAT_OR_RETRY")
            record = {"status": "STARTED", "reserved": request.length, "actually_read": 0}
            state["records"][uid] = record
            self._save(state)
            if crash_after_start:
                raise SystemExit("SYNTH_CRASH")
            try:
                need(type(response) is Response, "BAD_RESPONSE")
                need(not response.retry and not response.redirected, "RETRY_OR_REDIRECT")
                need(response.status == 200 or 400 <= response.status <= 599,
                     "UNEXPECTED_RANGE_OR_STATUS")
                need(response.encoding == "identity" and type(response.content_length) is int
                     and 0 <= response.content_length <= request.length, "UNKNOWN_RESPONSE_BOUND")
                if response.status == 200:
                    need(response.content_length == request.length and response.etag == request.etag
                         and response.version_id == request.version_id, "HEAD_GET_IDENTITY_CHANGED")
                for i, chunk in enumerate(response.chunks):
                    need(type(chunk) is int and chunk > 0, "BAD_CHUNK")
                    need(record["actually_read"] + chunk <= response.content_length,
                         "CHUNK_EXCEEDS_READ_BOUND")
                    record["actually_read"] += chunk
                    self._save(state)
                    if interrupt_after is not None and i + 1 == interrupt_after:
                        raise SystemExit("SYNTH_READ_INTERRUPT")
                need(record["actually_read"] == response.content_length, "SHORT_READ")
                need(response.status == 200, "HTTP_ERROR_BODY_CHARGED")
                record["status"] = "COMPLETE"
            except Exception as exc:
                if isinstance(exc, GateError) and str(exc) in (
                        "PERSISTENCE_STOP_NO_RETRY", "PENDING_WRITE_STOP"):
                    raise
                record["status"] = "FAILED"
                record["failure"] = str(exc) if isinstance(exc, GateError) else "SYNTH_EXCEPTION"
                self._save(state)
                raise GateError(record["failure"]) from None
            self._save(state)

    def summary(self):
        with Lock(self.root):
            records = self._load()["records"]
        return {"scope": "SYNTHETIC_ONLY", "reserved": sum(r["reserved"] for r in records.values()),
                "actually_read": sum(r["actually_read"] for r in records.values()),
                "started_unfinished": sum(r["status"] == "STARTED" for r in records.values()),
                "completed": sum(r["status"] == "COMPLETE" for r in records.values()),
                "failed": sum(r["status"] == "FAILED" for r in records.values()),
                "not_started": len(self.requests) - len(records),
                "hard_limits": {"single_media": MEDIA_LIMIT, "all_get_body": TOTAL_LIMIT,
                                "metadata": META_LIMIT, "different_media": 2},
                "live_access": "LIVE_ACCESS_NOT_AUTHORIZED",
                "real_bridge": "REAL_BRIDGE_NOT_VERIFIED",
                "real_transfer": "REAL_TRANSFER_ENFORCEMENT_NOT_VERIFIED",
                "real_aws_requests": 0, "real_videos": 0, "gpu_calls": 0}


def fixture():
    uids = ("SYNTH_VIDEO_01", "SYNTH_VIDEO_02")
    text = "video_uid,canonical_s3_location\n" + "".join(
        f"{u},s3://SYNTH_BUCKET/public/v2_1/full_scale/{u}.mp4\n" for u in uids)
    return uids, text


def dry_run():
    uids, text = fixture()
    mapped = join_manifest(text, uids, "v2_1", "full_scale", SYNTH_BRIDGE_CONFIRMED=True)
    requests = tuple(Request(uid, uri, "media", 9) for uid, uri in mapped)
    with Workspace() as root:
        ledger = Ledger(root, requests)
        ledger.transfer(uids[0], Response((2, 3, 4), 9))
        ledger.transfer(uids[1], Response((3, 6), 9))
        resumed = Ledger(root, requests, resume=True)
        try:
            resumed.transfer(uids[0], Response((9,), 9))
        except GateError as exc:
            need(str(exc) == "NO_REPEAT_OR_RETRY", "RESUME_REJECTION_FAILED")
        else:
            raise GateError("DUPLICATE_WAS_ALLOWED")
        return resumed.summary()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--synthetic", action="store_true", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        import unittest
        result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromName(
            "prototypes.test_ego4d_boto3_offline_gate"))
        print(json.dumps({"scope": "SYNTHETIC_ONLY", "tests": result.testsRun,
                          "passed": result.wasSuccessful(), "real_aws_requests": 0,
                          "live_access": "LIVE_ACCESS_NOT_AUTHORIZED"}))
        return 0 if result.wasSuccessful() and result.testsRun >= 18 else 1
    print(json.dumps(dry_run(), sort_keys=True))
    return 0


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    raise SystemExit(main())
