"""Metadata-only stdlib audit. No network, media, models, code execution, or ID output."""
import argparse
import csv
import hashlib
import io
import json
import os
import pathlib
import re
import stat
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from itertools import combinations

MIB = 1024 * 1024
ALLOWED = frozenset((
    "Charades_v1_train.csv", "Charades_v1_test.csv", "Charades_v1_classes.txt",
    "Charades_v1_objectclasses.txt", "Charades_v1_verbclasses.txt",
    "Charades_v1_mapping.txt", "README.txt", "license.txt"))
REQUIRED = frozenset(("id", "subject", "actions", "length"))
DEVICES = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$", re.I)


class AuditError(ValueError):
    """Only fixed error codes; do not put source paths or records in exceptions."""


def check_ancestors(path):
    path = pathlib.Path(path).absolute()
    for part in (path,) + tuple(path.parents):
        if part.exists() or part.is_symlink():
            s = part.lstat()
            if part.is_symlink() or getattr(s, "st_file_attributes", 0) & 0x400:
                raise AuditError("STORAGE_REPARSE")
    if path.resolve() != path:
        raise AuditError("STORAGE_REALPATH_MISMATCH")


def safe_members(infos):
    if len(infos) > 200 or sum(i.file_size for i in infos) > 64 * MIB:
        raise AuditError("ZIP_TOTAL_LIMIT")
    seen, selected, path_kinds = set(), {}, {}
    for item in infos:
        name = item.orig_filename
        if name != item.filename or not name or name.startswith(("/", "\\")) or "\\" in name or ":" in name:
            raise AuditError("ZIP_PATH_INVALID")
        parts = name.rstrip("/").split("/")
        if len(parts) > 4 or any(p in ("", ".", "..") or p[-1:] in (" ", ".")
                                or DEVICES.match(p.split(".")[0])
                                or any(ord(ch)<32 or ch in '<>"|?*' for ch in p) for p in parts):
            raise AuditError("ZIP_COMPONENT_INVALID")
        key = "/".join(parts).casefold()
        if key in seen:
            raise AuditError("ZIP_CASE_COLLISION")
        seen.add(key)
        path_kinds[key] = item.is_dir()
        mode = (item.external_attr >> 16) & 0xFFFF
        kind = stat.S_IFMT(mode)
        if item.flag_bits & 1 or kind not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise AuditError("ZIP_ENCRYPTED_OR_SPECIAL")
        if item.file_size < 0 or item.compress_size < 0 or item.file_size > 16 * MIB:
            raise AuditError("ZIP_MEMBER_LIMIT")
        if item.is_dir() and item.file_size != 0:
            raise AuditError("ZIP_DIRECTORY_DATA")
        if parts[-1].lower().endswith((".zip", ".7z", ".rar", ".tar", ".gz")):
            raise AuditError("ZIP_NESTED_ARCHIVE")
        if not item.is_dir() and parts[-1] in ALLOWED:
            if parts[-1] in selected:
                raise AuditError("ZIP_WHITELIST_DUPLICATE")
            selected[parts[-1]] = item
    for key in path_kinds:
        parts = key.split('/')
        if any(path_kinds.get('/'.join(parts[:i])) is False for i in range(1,len(parts))):
            raise AuditError("ZIP_FILE_PARENT_COLLISION")
    if not {"Charades_v1_train.csv", "Charades_v1_test.csv", "Charades_v1_classes.txt"} <= set(selected):
        raise AuditError("ZIP_REQUIRED_MISSING")
    return selected


def inspect_archive(archive):
    archive = pathlib.Path(archive)
    if not 0 < archive.stat().st_size <= 8 * MIB:
        raise AuditError("ARCHIVE_SIZE_LIMIT")
    check_ancestors(archive)
    try:
        with archive.open("rb") as f:
            if f.read(4) != b"PK\x03\x04":
                raise AuditError("ZIP_SIGNATURE")
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            selected = safe_members(infos)
            if z.testzip() is not None:
                raise AuditError("ZIP_CRC_FAILURE")
            return {
                "member_count": len(infos), "declared_uncompressed_bytes": sum(i.file_size for i in infos),
                "whitelist_count": len(selected), "unextracted_member_count": len(infos)-len(selected),
                "selected_names": sorted(selected), "crc": "PASS"}
    except (zipfile.BadZipFile, NotImplementedError, RuntimeError, EOFError):
        raise AuditError("ZIP_INTEGRITY_FAILURE") from None


def extract_whitelist(archive, root):
    root = pathlib.Path(root)
    check_ancestors(root)
    inspect_archive(archive)
    destination = root / "extracted"
    destination.mkdir(exist_ok=True)
    check_ancestors(destination)
    if any(destination.iterdir()):
        raise AuditError("EXTRACTED_ALREADY_NONEMPTY")
    with zipfile.ZipFile(archive) as z:
        selected = safe_members(z.infolist())
        for name, item in selected.items():
            target = destination / name  # Fixed basename whitelist; no extractall.
            check_ancestors(target)
            with z.open(item) as source, target.open("xb") as output:
                written = 0
                while True:
                    chunk = source.read(65536)
                    if not chunk:
                        break
                    written += len(chunk)
                    if written > item.file_size or written > 16 * MIB:
                        raise AuditError("EXTRACTION_SIZE_LIMIT")
                    output.write(chunk)
                if written != item.file_size:
                    raise AuditError("EXTRACTION_TRUNCATED")


def finite_number(text):
    try:
        value = Decimal(str(text).strip())
        return value if value.is_finite() else None
    except (InvalidOperation, ValueError):
        return None


def csv_rows(text):
    reader = csv.DictReader(io.StringIO(text, newline=""))
    header = reader.fieldnames
    if not header or len(header) != len(set(header)) or not REQUIRED <= set(header):
        raise AuditError("CSV_REQUIRED_HEADER")
    try:
        return header, list(reader)
    except csv.Error:
        raise AuditError("CSV_PARSE_FAILURE") from None


def summarize_split(rows, classes):
    counts = Counter()
    ids, subjects, seen_ids = set(), set(), Counter()
    duration_bins = Counter({k: 0 for k in ("lt30", "30to60", "60to300", "ge300", "invalid")})
    valid_lengths = []
    id_totals = Counter((r.get("id") or "").strip() for r in rows)
    for row in rows:
        counts["rows"] += 1
        vid, subject = tuple((row.get(k) or "").strip() for k in ("id", "subject"))
        if not vid:
            counts["empty_id"] += 1
        else:
            ids.add(vid); seen_ids[vid] += 1
        if not subject:
            counts["empty_subject"] += 1
        else:
            subjects.add(subject)
        if None in row or any(row.get(k) is None for k in REQUIRED):
            counts["row_shape_invalid"] += 1
        length = finite_number(row.get("length"))
        length_ok = length is not None and length > 0
        if not length_ok:
            counts["invalid_length"] += 1; duration_bins["invalid"] += 1
        else:
            valid_lengths.append(length)
            b = "lt30" if length < 30 else "30to60" if length < 60 else "60to300" if length < 300 else "ge300"
            duration_bins[b] += 1
        raw = (row.get("actions") or "").strip()
        if not raw:
            counts["empty_actions"] += 1
            continue
        tokens = raw.split(";")
        if len(tokens) > 1024:
            raise AuditError("ROW_ACTION_LIMIT")
        groups, unique, malformed = defaultdict(list), set(), False
        for token in tokens:
            counts["action_tokens"] += 1
            fields = token.split()
            if len(fields) != 3:
                counts["action_parse_error"] += 1; counts["invalid_action_tokens"] += 1; malformed = True
                continue
            label, a, b = fields; start, end = finite_number(a), finite_number(b)
            errors = []
            if label not in classes: errors.append("unknown_class")
            if start is None or end is None: errors.append("nonfinite_or_invalid_time")
            else:
                if start < 0: errors.append("negative_start")
                if start >= end: errors.append("start_not_before_end")
                if length_ok and end > length: errors.append("end_exceeds_length")
            if not length_ok: errors.append("action_length_unknown")
            if errors:
                counts.update(errors); counts["invalid_action_tokens"] += 1; malformed = True
                continue
            counts["valid_action_tokens"] += 1
            triple = (label, start, end)
            if triple in unique:
                counts["exact_duplicate_intervals"] += 1
                continue
            unique.add(triple); groups[label].append((start, end))
            counts["unique_valid_intervals"] += 1
        if malformed: counts["rows_with_invalid_actions"] += 1
        if not vid or id_totals[vid] > 1 or None in row or any(row.get(k) is None for k in REQUIRED):
            counts["qualification_identity_or_shape_blocked_rows"] += 1
            continue
        counts["valid_video_class_groups"] += len(groups)
        qualified_p1 = False
        for intervals in groups.values():
            if len(intervals) < 2: continue
            counts["same_class_multi_interval_groups"] += 1
            gaps, touch, overlap = [], False, False
            for (a, b), (c, d) in combinations(intervals, 2):
                gap = max(a, c) - min(b, d)
                if gap > 0: gaps.append(gap)
                elif gap == 0: touch = True; counts["same_class_touch_pairs"] += 1
                else: overlap = True; counts["same_class_overlap_pairs"] += 1
                counts["same_class_distinct_pairs"] += 1
            for threshold, key in ((Decimal(0), "p1_gap_gt0_groups"), (Decimal('0.5'), "p1_gap_gt05_groups"), (Decimal(1), "p1_gap_gt1_groups")):
                if any(g > threshold for g in gaps): counts[key] += 1
            if touch: counts["same_class_touch_groups"] += 1
            if overlap: counts["same_class_overlap_groups"] += 1
            if gaps and (touch or overlap): counts["p1_qualified_with_ambiguity_groups"] += 1
            if gaps: qualified_p1 = True
        if qualified_p1: counts["p1_videos"] += 1
        records = [(c, a, b) for c, intervals in groups.items() for a, b in intervals]
        overlap_video, strong_video = False, False
        class_pairs, strong_class_pairs = set(), set()
        for (c, a, b), (k, s, e) in combinations(records, 2):
            if c == k: continue
            counts["different_class_pair_denominator"] += 1
            intersection = min(b, e)-max(a, s)
            if intersection == 0: counts["different_class_touch_pairs"] += 1
            if intersection <= 0: continue
            counts["p2_overlap_pairs"] += 1; overlap_video = True
            class_pairs.add(tuple(sorted((c, k))))
            if (a <= s and e <= b) or (s <= a and b <= e): counts["different_class_containment_pairs"] += 1
            if intersection / min(b-a, e-s) >= Decimal('0.5'):
                counts["p2_strong_overlap_pairs"] += 1; strong_video = True
                strong_class_pairs.add(tuple(sorted((c, k))))
        counts["p2_video_classpair_groups"] += len(class_pairs)
        counts["p2_strong_video_classpair_groups"] += len(strong_class_pairs)
        counts["p2_videos"] += int(overlap_video); counts["p2_strong_videos"] += int(strong_video)
    counts["unique_video_ids"] = len(ids)
    counts["distinct_subjects"] = len(subjects)
    counts["duplicate_id_extra_rows"] = sum(n-1 for n in seen_ids.values() if n>1)
    lengths = sorted(valid_lengths)
    median = None if not lengths else (lengths[(len(lengths)-1)//2]+lengths[len(lengths)//2])/2
    rough = {"valid_length_rows": len(lengths), "mean_seconds_rounded": None if not lengths else round(float(sum(lengths)/len(lengths)),1),
             "median_seconds_rounded": None if median is None else round(float(median),1), "duration_bins": dict(duration_bins)}
    return {"counts": dict(counts), "duration": rough}, ids, subjects


def summarize(train_rows, test_rows, classes):
    train, tids, ts = summarize_split(train_rows, classes)
    test, vids, vs = summarize_split(test_rows, classes)
    return {"train": train, "test": test, "cross_split_subject_count": len(ts & vs),
            "union_subject_count": len(ts | vs), "cross_split_video_id_count": len(tids & vids),
            "class_count": len(classes), "qualification_note": "RECORD_LEVEL_ONLY_NO_ORDINAL_OR_MEDIA_CERTIFICATE"}


def public_summary(summary):
    """Suppress every positive count <10, not only identity-linked cells."""
    def clean(value, key=""):
        if isinstance(value, dict): return {k: clean(v, k) for k, v in value.items()}
        if isinstance(value, int) and not isinstance(value, bool) and 0 < value < 10:
            return "WITHHELD_LT10"
        return value
    return clean(summary)


def run(root):
    root = pathlib.Path(root).absolute()
    pinned = (pathlib.Path(os.environ["LOCALAPPDATA"])/"VLM-Research-Isolated"/"Charades-v1-Metadata").absolute()
    if os.path.normcase(str(root)) != os.path.normcase(str(pinned)):
        raise AuditError("STORAGE_NOT_PROTOCOL_ROOT")
    check_ancestors(root)
    archive = root / "incoming" / "Charades.zip"
    receipt = inspect_archive(archive)
    extract_whitelist(archive, root)
    data = root / "extracted"
    try:
        classes = {line.split()[0] for line in (data/"Charades_v1_classes.txt").read_text(encoding="utf-8-sig").splitlines() if line.strip()}
        if not classes or any(not re.fullmatch(r"c\d{3}", c) for c in classes): raise AuditError("CLASS_TABLE_INVALID")
        th, train = csv_rows((data/"Charades_v1_train.csv").read_text(encoding="utf-8-sig"))
        vh, test = csv_rows((data/"Charades_v1_test.csv").read_text(encoding="utf-8-sig"))
    except UnicodeError:
        raise AuditError("TEXT_ENCODING_NOT_UTF8") from None
    summary = summarize(train, test, classes)
    summary.update({"headers": {"train": th, "test": vh}, "encoding": "UTF8_SIG_DECODER", "zip_safety": receipt,
                    "archive_bytes": archive.stat().st_size, "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest()})
    audit = root / "local-audit"
    check_ancestors(audit)
    with (audit/"aggregate-summary.json").open("x", encoding="utf-8") as f: json.dump(summary, f, indent=2)
    print(json.dumps(public_summary(summary), ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None)
    args = parser.parse_args()
    try:
        root = args.root or str(pathlib.Path(os.environ["LOCALAPPDATA"])/"VLM-Research-Isolated"/"Charades-v1-Metadata")
        run(root)
    except (AuditError, OSError, KeyError, csv.Error):
        print("AUDIT_BLOCKED; inspect only the local task receipt. No paths or records printed.")
        raise SystemExit(1) from None
