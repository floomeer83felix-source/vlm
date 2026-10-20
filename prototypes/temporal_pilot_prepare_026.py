"""026 preparation primitives. No real default paths, data or live backend.

Callers supply exact authorized entries and own one cumulative InputBudget.
Protected values use the unchanged 025 lexical projector. Snapshot digests and
identifiers are private handoff data, not suitable for public receipts.
"""

from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import stat

from temporal_evidence_adapter_025 import (
    ContractError, QuestionKey, TASK, _Projector, build_plan, decompose,
    project_nongold,
    STRICT_025,
)


MIB = 1024 * 1024
GROUP_FIELDS = (
    "video_uid", "uid", "video_source", "origin_video_id", "fb_participant_id",
    "release_1", "canonical_is_validated", "canonical_mp4_duration_sec",
    "duration_in_seconds", "canonical_version", "canonical_mp4_version", "version",
    "canonical_mp4_size_bytes", "canonical_video_size_bytes", "canonical_size_bytes",
    "file_size_bytes", "parent_video_uid", "source_video_uid", "parent_uid", "source_uid",
)
_UID_LISTS = frozenset(("excluded_video_uids", "used_video_uids", "previous_video_uids",
                        "excluded_uids", "old_video_uids", "historical_uids"))
_PRIVATE_BRANCHES = ("question", "answer", "gold", "prediction", "canary",
                     "timestamp", "mcq_test")


def identity(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def same_file(left, right):
    """Positive physical identity, not equal sizes or zero/default identities."""
    return left.st_ino > 0 and right.st_ino > 0 and os.path.samestat(left, right)


def difference_mask(left, right):
    return tuple(name for name, a, b in zip(
        ("dev", "ino", "size", "mtime_ns", "ctime_ns"), identity(left), identity(right))
                 if a != b)


def checked_path(path, directory=False):
    """Metadata only, exact ancestor chain; no listing or candidate search."""
    path = Path(path).absolute()
    for item in tuple(reversed(path.parents)) + (path,):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ContractError("REPARSE_OR_LINK_PATH")
    info = path.stat()
    if not (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)):
        raise ContractError("UNEXPECTED_PATH_KIND")
    return path, info


@dataclass(frozen=True)
class ReadReceipt:
    alias: str
    byte_count: int
    digest: str = field(repr=False)
    before: tuple = field(repr=False)
    after: tuple = field(repr=False)
    complete: bool


class _BudgetRaw(io.RawIOBase):
    def __init__(self, file, size, owner):
        super().__init__()
        self.file, self.size, self.owner = file, size, owner
        self.count, self.sha = 0, hashlib.sha256()

    def readable(self):
        return True

    def readinto(self, buffer):
        size = min(len(buffer), self.size - self.count)
        if size <= 0:
            return 0
        # The whole statted size has already been conservatively reserved.
        data = self.file.read(size)
        self.count += len(data)
        self.owner.actual += len(data)
        self.sha.update(data)
        buffer[:len(data)] = data
        return len(data)


class InputBudget:
    """One ledger for all input opens; failed reservations never refund.

    Registration is a caller responsibility, not a grant of filesystem access.
    No implicit entry discovery, recursion, retry or scope enlargement occurs.
    """

    def __init__(self, total_limit=48 * MIB, *, durable=None):
        if type(total_limit) is not int or not 0 < total_limit <= 48 * MIB:
            raise ContractError("INVALID_INPUT_LIMIT")
        self.limit, self.reserved, self.actual = total_limit, 0, 0
        self.entries, self.opens, self.receipts = {}, {}, []
        self.durable, self.diagnostics = durable, []

    def register(self, alias, path, cap, max_opens=1):
        if alias in self.entries or type(cap) is not int or not 0 < cap <= 8 * MIB:
            raise ContractError("INVALID_INPUT_REGISTRATION")
        if type(max_opens) is not int or not 1 <= max_opens <= 3:
            raise ContractError("INVALID_OPEN_LIMIT")
        path = Path(path).absolute()
        if any(entry[0] == path for entry in self.entries.values()):
            raise ContractError("DUPLICATE_INPUT_PATH")
        self.entries[alias] = (path, cap, max_opens)
        self.opens[alias] = 0

    @contextmanager
    def text(self, alias, role="content"):
        if alias not in self.entries:
            raise ContractError("UNREGISTERED_INPUT")
        path, cap, maximum = self.entries[alias]
        if self.opens[alias] >= maximum:
            raise ContractError("INPUT_OPEN_LIMIT")
        self.opens[alias] += 1
        path, before = checked_path(path)
        if before.st_size > cap or self.reserved + before.st_size > self.limit:
            raise ContractError("INPUT_BYTE_LIMIT")
        if self.durable is not None:
            self.durable.reserve_input(alias, path, role, before, cap, maximum)
        self.reserved += before.st_size
        raw_file = raw = stream = None
        complete, reason = False, "INPUT_OPEN_OR_PROJECTION_FAILED"
        try:
            raw_file = open(path, "rb", buffering=0)
            opened = os.fstat(raw_file.fileno())
            self.diagnostics.append({"alias": alias, "role": role,
                                     "cross_api_difference": difference_mask(before, opened),
                                     "same_file": same_file(before, opened)})
            if not same_file(before, opened) or before.st_size != opened.st_size:
                raise ContractError("INPUT_IDENTITY_CHANGED_AT_OPEN")
            raw = _BudgetRaw(raw_file, before.st_size, self)
            stream = io.TextIOWrapper(io.BufferedReader(raw), encoding="utf-8-sig", newline="")
            yield stream
            _, after_path = checked_path(path)
            after_fd = os.fstat(raw_file.fileno())
            complete = (same_file(after_path, after_fd)
                        and identity(before) == identity(after_path)
                        and identity(opened) == identity(after_fd)
                        and raw.count == before.st_size)
            reason = "COMPLETE" if complete else "INPUT_CHANGED_OR_INCOMPLETE"
            if not complete:
                raise ContractError(reason)
        finally:
            try:
                count = raw.count if raw is not None else 0
                self.receipts.append(ReadReceipt(alias, count, raw.sha.hexdigest() if raw else "",
                                                 identity(before), (), complete))
                if self.durable is not None:
                    self.durable.finish_input(alias, path, role, count, complete, reason)
            finally:
                if stream is not None:
                    stream.close()
                if raw_file is not None:
                    raw_file.close()


@dataclass(frozen=True)
class AnnotationIndex:
    sources: tuple = field(repr=False)
    batch: tuple = field(repr=False)
    question_field_names: tuple
    metadata_field_names: tuple


def index_annotation(stream, *, profile=STRICT_025, diagnostic=None):
    sources, rows, question_fields, metadata_fields = [], {}, set(), set()

    def keys(path, key):
        if not path:
            sources.append(key)
            rows[key] = set()
        if len(path) == 3 and path[1] == "benchmark_dataset" and type(path[2]) is int:
            rows[path[0]].add(path[2])
            question_fields.add(key)
        if len(path) == 2 and path[1] == "video_metadata":
            metadata_fields.add(key)

    _Projector(stream, lambda path: False, keys, profile=profile, diagnostic=diagnostic).read()
    batch = tuple(QuestionKey(source, index) for source in sources
                  for index in sorted(rows[source]))
    return AnnotationIndex(tuple(sources), batch, tuple(sorted(question_fields)),
                           tuple(sorted(metadata_fields)))


def historical_projection(stream, *, profile=STRICT_025, diagnostic=None):
    """Approved identity/group fields only, never old questions or outputs."""
    def allow(path):
        names = tuple(p.lower() for p in path if type(p) is str)
        if any(any(token in name for token in _PRIVATE_BRANCHES) for name in names):
            return False
        return bool(path) and (path[-1] in GROUP_FIELDS
                               or any(name in _UID_LISTS for name in names)
                               or ("source_group" in names and type(path[-1]) is int))

    return _Projector(stream, allow, profile=profile, diagnostic=diagnostic).read()


def old_uid_fields(projected):
    """Field-aware identity extraction; never flatten strings or intersect dev.

    Source-group array slots are kept as group evidence, not guessed UID slots.
    This deliberately returns UNKNOWN for identities absent from known fields.
    """
    uids = set()
    singular = frozenset(("video_uid", "uid", "source_uid", "parent_video_uid",
                          "source_video_uid", "parent_uid"))
    def walk(value, uid_list=False):
        if type(value) is dict:
            for key, child in value.items():
                if key in singular and type(child) is str and child.strip():
                    uids.add(child)
                elif type(key) is str and key.lower() in _UID_LISTS:
                    walk(child, True)
                elif type(child) in (dict, list, tuple):
                    walk(child, uid_list)
                elif uid_list and type(child) is str and child.strip():
                    uids.add(child)
        elif type(value) in (tuple, list):
            for child in value:
                if uid_list and type(child) is str and child.strip():
                    uids.add(child)
                elif type(child) in (dict, tuple, list):
                    walk(child, uid_list)
    walk(projected)
    return frozenset(uids)


def independent_join_requests(index, old_projections):
    old = frozenset(uid for record in old_projections for uid in old_uid_fields(record))
    return old, old | (frozenset(index.sources) if index is not None else frozenset())


def read_manifest(stream, wanted_uids):
    """Retain approved columns/needed rows; other CSV cells are discarded.

    CSV syntax requires traversing complete rows. No URL/path columns persist.
    Unlike mixed annotation JSON, this list contains no protected QA values.
    """
    rows = csv.DictReader(stream)
    headers = tuple(rows.fieldnames or ())
    candidates = tuple(name for name in ("video_uid", "uid") if name in headers)
    if len(candidates) != 1 or len(set(headers)) != len(headers):
        raise ContractError("MANIFEST_UID_SCHEMA_HOLD")
    uid_column = candidates[0]
    retained, duplicates, count = {}, set(), 0
    columns = tuple(name for name in headers if name in GROUP_FIELDS)
    for row in rows:
        count += 1
        if None in row or any(value is None for value in row.values()):
            raise ContractError("MANIFEST_ROW_SCHEMA_HOLD")
        uid = row.get(uid_column)
        if uid in wanted_uids:
            if uid in retained:
                duplicates.add(uid)
            retained[uid] = {name: row.get(name, "") for name in columns}
    return retained, {"rows": count, "matched": len(retained),
                      "uid_column": uid_column,
                      "duplicate_needed_uids": len(duplicates),
                      "retained_columns": columns, "headers": headers}, duplicates


def flatten_strings(value):
    if type(value) is str:
        yield value
    elif type(value) is dict:
        for child in value.values():
            yield from flatten_strings(child)
    elif type(value) in (tuple, list):
        for child in value:
            yield from flatten_strings(child)


def _truth(value):
    return value is True or type(value) is str and value.strip().lower() == "true"


def _group(row):
    origin, collection = row.get("origin_video_id"), row.get("video_source")
    return (collection, origin) if collection and origin else None


def choose_cohort(projection, manifest, old_uids, *, complete_old_mapping=False):
    """No option/gold input; order and first-per-source admission are frozen."""
    old_uids = frozenset(old_uids)
    old_rows = tuple(manifest[uid] for uid in old_uids if uid in manifest)
    old_groups = {_group(row) for row in old_rows} - {None}
    old_people = {row.get("fb_participant_id") for row in old_rows} - {None, ""}
    counters, selected, exclusions = Counter(), [], []
    seen_sources, seen_groups, seen_people = set(), set(), set()
    for question in projection.questions:
        counters["total_questions"] += 1
        parts = decompose(question.task, question.question)
        if parts.status != "OK":
            counters["unsupported_" + parts.reason] += 1
            continue
        counters["supported_questions"] += 1
        uid = question.key.source
        row = manifest.get(uid, {})
        group, person = _group(row), row.get("fb_participant_id")
        reason = ("OLD_UID" if uid in old_uids else "OLD_ORIGIN" if group and group in old_groups
                  else "OLD_PARTICIPANT" if person and person in old_people
                  else "KNOWN_DERIVATIVE" if any(row.get(name) in old_uids for name in
                       ("parent_video_uid", "source_video_uid", "parent_uid")) else "")
        if not reason:
            reason = ("SOURCE_FIRST_QUESTION_ONLY" if uid in seen_sources
                      else "COHORT_ORIGIN" if group and group in seen_groups
                      else "COHORT_PARTICIPANT" if person and person in seen_people else "")
        if reason:
            counters["excluded_" + reason] += 1
            exclusions.append((question.key, reason))
            continue
        seen_sources.add(uid)
        if group:
            seen_groups.add(group)
        if person:
            seen_people.add(person)
        counters["post_known_group_sources"] += 1
        if len(selected) < 4:
            limits = []
            if not row:
                limits.append("MANIFEST_JOIN_UNKNOWN")
            if not group or not person:
                limits.append("GROUP_FIELDS_INCOMPLETE")
            if not _truth(row.get("release_1")):
                limits.append("RELEASE1_UNKNOWN_OR_FALSE")
            if not complete_old_mapping:
                limits.append("OLD_SOURCE_MAPPING_INCOMPLETE")
            limits.extend(("CURRENT_RIGHTS_UNKNOWN", "PHYSICAL_RECORDING_INDEPENDENCE_UNKNOWN"))
            selected.append({"key": question.key, "task": question.task,
                             "question": question.question, "event_a": parts.event_a,
                             "event_b": parts.event_b, "metadata": row, "limits": tuple(limits)})
    counters["frozen_text_candidates"] = len(selected)
    # This preparation interface does not authenticate current rights or media.
    counters["executable_candidates"] = 0
    return tuple(selected), dict(counters), tuple(exclusions)


def binding_matches(preparation, scoring):
    return (type(preparation) is ReadReceipt and type(scoring) is ReadReceipt
            and preparation.complete and scoring.complete
            and preparation.alias == scoring.alias
            and preparation.byte_count == scoring.byte_count
            and preparation.digest == scoring.digest
            and preparation.before[:2] == scoring.before[:2])


def canonical_digest(value):
    data = json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class PrivateOutput:
    """Exclusive new-directory output; never overwrites or deletes anything."""
    def __init__(self, authorized_root, name="integration_026"):
        root, _ = checked_path(authorized_root, directory=True)
        if name != "integration_026":
            raise ContractError("FIXED_OUTPUT_DIRECTORY_REQUIRED")
        self.path = root / name
        os.mkdir(self.path)  # An existing leaf is a HOLD, never a suffix retry.
        checked_path(self.path, directory=True)
        self.count, self.bytes = 0, 0

    def write(self, name, text):
        if (Path(name).name != name or not name or name in (".", "..")
                or type(text) is not str):
            raise ContractError("SIMPLE_OUTPUT_NAME_REQUIRED")
        data = text.encode("utf-8")
        if self.count >= 64 or self.bytes + len(data) > 32 * MIB:
            raise ContractError("PRIVATE_OUTPUT_LIMIT")
        checked_path(self.path, directory=True)
        self.count += 1
        self.bytes += len(data)
        with open(self.path / name, "xb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())

    def json(self, name, value):
        self.write(name, json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False))
