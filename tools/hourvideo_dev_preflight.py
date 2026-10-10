#!/usr/bin/env python3
"""Offline HourVideo annotation-only pilot preflight (stdlib; no network, video, or GPU).

This tool NEVER grants permission to use a dataset or start a model experiment.
It validates only metadata from an explicitly supplied, locally obtained JSON.
The original annotation file must never be edited, especially its canary.
Public output is aggregates only. A private selection requires an explicit
output path outside a Git working tree and MUST NOT be published.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


LETTERS = frozenset("ABCDE")


def _hash_order(value: str, salt: str) -> str:
    return hashlib.sha256((salt + "\x00" + value).encode("utf-8")).hexdigest()


def _valid_qa(item: Any) -> bool:
    if not isinstance(item, dict):
        return False
    qid = item.get("qid")
    label = item.get("correct_answer_label")
    mcq = item.get("mcq_test")
    question = item.get("question")
    if not isinstance(qid, str) or not qid.strip():
        return False
    if not isinstance(label, str) or label.strip().upper() not in LETTERS:
        return False
    if not isinstance(question, str) or not question.strip():
        return False
    if not isinstance(mcq, str) or not mcq.strip():
        return False
    return True


def analyze(
    obj: Any, *,
    min_videos: int = 12,
    per_video: int = 2,
    min_seconds: float = 1200.0,
    min_long_videos: int = 4,
    long_seconds: float = 1800.0,
    seed: str = "longvideo-pilot-v1"
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return sanitized aggregate statistics and a PRIVATE identifier selection.

    This intentionally does NOT establish media existence, legality, source
    mapping, clip authenticity, independence, or actual scoring validity.
    """
    if not isinstance(obj, dict):
        raise ValueError("Expected a JSON object keyed by video UID")
    if min_videos < 1 or per_video < 1 or min_long_videos < 0:
        raise ValueError("Invalid requested counts")
    if min_long_videos > min_videos:
        raise ValueError("30-minute requirement exceeds video count")

    counts: Counter[str] = Counter()
    candidates: list[tuple[str, float, list[str]]] = []
    distinct_qids: set[str] = set()
    video_rows = 0
    for uid, block in obj.items():
        # Ignore non-video top-level metadata, including any preserved canary.
        if not isinstance(uid, str) or not isinstance(block, dict):
            continue
        if "benchmark_dataset" not in block:
            continue
        video_rows += 1
        meta = block.get("video_metadata")
        qa = block.get("benchmark_dataset")
        if not isinstance(meta, dict) or not isinstance(qa, list):
            counts["bad_metadata_or_question_list"] += 1
            continue
        duration = meta.get("duration_in_seconds")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)):
            counts["missing_or_invalid_duration"] += 1
            continue
        seconds = float(duration)
        if not math.isfinite(seconds) or seconds <= 0:
            counts["missing_or_invalid_duration"] += 1
            continue
        if seconds < min_seconds:
            counts["under_20_min"] += 1
            continue

        local_ids: set[str] = set()
        valid_ids: list[str] = []
        for question in qa:
            if not _valid_qa(question):
                counts["invalid_or_unanswered_questions"] += 1
                continue
            qid = question["qid"].strip()
            if qid in local_ids:
                counts["duplicate_qid_within_video"] += 1
                continue
            local_ids.add(qid)
            if qid in distinct_qids:
                counts["duplicate_qid_across_videos"] += 1
                continue
            distinct_qids.add(qid)
            valid_ids.append(qid)
        if len(valid_ids) < per_video:
            counts["insufficient_scored_questions"] += 1
            continue
        candidates.append((uid, seconds, valid_ids))
    counts["total_video_records"] = video_rows
    candidates.sort(key=lambda row: _hash_order(row[0], seed))

    over_30 = [r for r in candidates if r[1] >= long_seconds]
    if len(candidates) >= min_videos and len(over_30) >= min_long_videos:
        chosen = over_30[:min_long_videos]
        chosen_ids = {uid for uid, _, _ in chosen}
        chosen += [r for r in candidates if r[0] not in chosen_ids][: min_videos - len(chosen)]
    else:
        chosen = []
    private_selection: list[dict[str, Any]] = [
        {"video_uid": uid, "qid": sorted(qids, key=lambda q: _hash_order(q, seed))[:per_video]}
        for uid, _, qids in chosen
    ]
    public = {
        "status": "ANNOTATION_ONLY_CANDIDATE" if len(chosen) == min_videos else "ANNOTATION_PREFLIGHT_BLOCKED",
        "not_video_or_license_approval": True,
        "not_gpu_approval": True,
        "requires_separate_media_license_version_and_lock_checks": True,
        "video_records_seen": video_rows,
        "videos_at_least_20min_with_2_valid_scored_questions": len(candidates),
        "of_those_at_least_30min": len(over_30),
        "required_unique_videos": min_videos,
        "required_questions_per_video": per_video,
        "required_at_least_30min": min_long_videos,
        "private_selected_video_count": len(chosen),
        "private_selected_question_count": sum(len(x["qid"]) for x in private_selection),
        "rejections": {k: v for k, v in sorted(counts.items()) if k != "total_video_records"},
        "warnings": [
            "Only explicit local annotation JSON was read; no video, media header, network, model or GPU used.",
            "The official 2025 annotated dev release must be verified by the user; older dev_v1.0.json has no answers.",
            "Labels are not passed into question-aware retrieval; never train on HourVideo benchmark answers.",
            "Duration values are claims from metadata, not verified file or packet-PTS measurements.",
            "If schema differs, do NOT silently infer or fill answer labels; revise with reviewed official format.",
        ],
    }
    return public, private_selection


def _in_git_tree(p: Path) -> bool:
    # Disallow a private sample/UID selection anywhere in a Git checkout.
    return any((parent / ".git").exists() for parent in (p.parent, *p.parent.parents))


def _atomic_write_json(p: Path, data: Any) -> None:
    if not p.parent.is_dir():
        raise ValueError("Output parent directory must already exist")
    if p.exists():
        raise ValueError("Refusing to overwrite an existing file")
    with p.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _self_test() -> None:
    obj = {}
    for i in range(12):
        obj[f"FICTIONAL_VIDEO_{i}"] = {
            "video_metadata": {"duration_in_seconds": 1900 if i < 4 else 1400},
            "benchmark_dataset": [
                {
                    "qid": f"FICTIONAL_QUESTION_{i}_{j}",
                    "question": "Synthetic example?",
                    "mcq_test": "A. one\nB. two\nC. three\nD. four\nE. five",
                    "correct_answer_label": "A",
                } for j in range(2)
            ],
        }
    report, selected = analyze(obj)
    assert report["status"] == "ANNOTATION_ONLY_CANDIDATE"
    assert report["private_selected_question_count"] == 24
    assert len(selected) == 12
    del obj["FICTIONAL_VIDEO_11"]["benchmark_dataset"][1]["correct_answer_label"]
    report, selected = analyze(obj)
    assert report["status"] == "ANNOTATION_PREFLIGHT_BLOCKED"
    assert selected == []
    print("SELF_TEST_PASS: two synthetic cases; no real benchmark data accessed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Run tests using fully fictional metadata")
    parser.add_argument("--annotations", type=Path, help="Explicit private local annotated HourVideo JSON path")
    parser.add_argument("--private-selection", type=Path, help="Optional private output (never Git/publish)")
    parser.add_argument("--public-report", type=Path, help="Optional aggregate-only JSON output")
    ns = parser.parse_args()
    if ns.self_test:
        _self_test()
        return 0
    if ns.annotations is None:
        parser.error("Pass --annotations or --self-test")
    # Reject writing confidential IDs into a public Git tree *before reading*.
    if ns.private_selection is not None:
        if _in_git_tree(ns.private_selection.resolve()):
            parser.error("Private selection must be outside any Git checkout")
        if ns.private_selection.exists():
            parser.error("Private selection destination already exists")
    if ns.public_report is not None and ns.public_report.exists():
        parser.error("Report destination already exists")
    with ns.annotations.open("r", encoding="utf-8") as f:
        data = json.load(f)
    public, private = analyze(data)
    if ns.private_selection is not None and private:
        _atomic_write_json(ns.private_selection, private)
    if ns.public_report is not None:
        _atomic_write_json(ns.public_report, public)
    print(json.dumps(public, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if public["status"] == "ANNOTATION_ONLY_CANDIDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
