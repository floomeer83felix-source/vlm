"""SYNTHETIC_ONLY stdlib A/B harness; no real adapters, data input or GPU.

Run: python -B prototypes/hourvideo_synthetic_ab_runner.py --synthetic
Test: python -B prototypes/hourvideo_synthetic_ab_runner.py --synthetic --self-test
Only internally created temporary workspaces are used. No external input flags
or output root are supported. Synthetic snapshots are deleted by their owner
after locks are released. Real model/scorer/media integration: NOT_INTEGRATED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from dataclasses import asdict, dataclass

LETTERS = "ABCDE"
VERSION = "SYNTH_AB_V1"


class HarnessError(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise HarnessError(code)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, allow_nan=False,
                                    separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Policy:
    seed: int = 17
    frames: int = 12
    candidates: int = 48
    max_attempts: int = 48
    simulated_budget_seconds: float = 7200.0
    version: str = VERSION

    def validate(self):
        require(type(self.seed) is int, "BAD_SEED")
        require(self.version == VERSION, "UNKNOWN_VERSION")
        require(type(self.frames) is int and self.frames == 12, "BAD_FRAME_LIMIT")
        require(type(self.candidates) is int and 12 <= self.candidates <= 48,
                "BAD_CANDIDATE_LIMIT")
        require(type(self.max_attempts) is int and 0 <= self.max_attempts <= 48,
                "BAD_ATTEMPT_LIMIT")
        require(type(self.simulated_budget_seconds) in (int, float) and
                math.isfinite(self.simulated_budget_seconds) and
                0 <= self.simulated_budget_seconds <= 7200, "BAD_SIMULATED_BUDGET")


@dataclass(frozen=True)
class Question:
    video: str
    qid: str
    duration: float
    text: str
    options: tuple[str, ...]


def synthetic_data(policy):
    policy.validate()
    questions, scoring_key = [], {}
    for i in range(12):
        for j in range(2):
            qid = f"SYNTH_Q_{i:02d}_{j}"
            questions.append(Question(f"SYNTH_VIDEO_{i:02d}", qid,
                                      1900.0 if i < 4 else 1400.0,
                                      f"SYNTH query about fictional phase {i}/{j}?",
                                      tuple(f"SYNTH option {k}" for k in LETTERS)))
            scoring_key[qid] = LETTERS[int(digest([policy.seed, qid]), 16) % 5]
    return tuple(questions), scoring_key


def validate_plan(questions, scoring_key):
    require(len(questions) == 24, "FIXED_24_QUESTIONS_REQUIRED")
    seen, groups = set(), {}
    for q in questions:
        require(type(q) is Question and q.qid.startswith("SYNTH_") and
                q.video.startswith("SYNTH_") and q.text.startswith("SYNTH "),
                "SYNTHETIC_NAMESPACE_REQUIRED")
        require(q.qid not in seen, "DUPLICATE_QUESTION")
        seen.add(q.qid)
        require(type(q.duration) in (int, float) and math.isfinite(q.duration)
                and q.duration >= 1200, "BAD_DURATION")
        require(len(q.options) == 5 and len(set(q.options)) == 5 and
                all(x.startswith("SYNTH ") for x in q.options), "BAD_OPTIONS")
        groups.setdefault(q.video, []).append(q)
        require(type(scoring_key.get(q.qid)) is str and
                scoring_key[q.qid] in LETTERS and
                len(scoring_key[q.qid]) == 1, "BAD_SCORING_LABEL")
    require(set(scoring_key) == seen, "SCORING_KEYS_DIFFER")
    require(len(groups) == 12 and all(len(rows) == 2 for rows in groups.values()),
            "FIXED_12_BY_2_REQUIRED")
    require(all(len({q.duration for q in rows}) == 1 for rows in groups.values()),
            "INCONSISTENT_VIDEO_DURATION")
    require(sum(rows[0].duration >= 1800 for rows in groups.values()) >= 4,
            "FOUR_LONG_VIDEOS_REQUIRED")


def uniform(duration, count):
    require(type(duration) in (int, float) and math.isfinite(duration) and
            duration > 0, "BAD_DURATION")
    require(type(count) is int and 1 <= count <= 48, "BAD_POINT_COUNT")
    # Bin centres avoid duration's exclusive right endpoint.
    return tuple(duration * (i + 0.5) / count for i in range(count))


@dataclass(frozen=True)
class SelectorInput:
    question: str
    duration: float
    positions: tuple[float, ...]
    policy: Policy


class SyntheticScorer:
    """Only query, candidate position and frozen policy enter the fake score."""
    def score(self, view, position):
        return int(digest([view.question, position, view.policy.seed]), 16)


def select_b(view, scorer):
    view.policy.validate()
    require(type(scorer) is SyntheticScorer, "REAL_SCORER_NOT_INTEGRATED")
    require(view.question.startswith("SYNTH "), "SYNTHETIC_QUERY_REQUIRED")
    require(type(view.duration) in (int, float) and math.isfinite(view.duration)
            and view.duration > 0, "BAD_DURATION")
    points = tuple(sorted(set(view.positions)))
    require(view.policy.frames <= len(points) <= view.policy.candidates,
            "BAD_CANDIDATE_COUNT")
    require(all(type(t) in (int, float) and math.isfinite(t) and
                0 <= t < view.duration for t in points), "BAD_CANDIDATE_TIME")
    ranked = sorted(points, key=lambda t: (-scorer.score(view, t), t))
    return tuple(sorted(ranked[:view.policy.frames]))


@dataclass(frozen=True)
class Prompt:
    question: str
    options: tuple[str, ...]
    frames: tuple[float, ...]
    arm: str
    seed: int


class SyntheticVLM:
    def generate(self, prompt):
        require(type(prompt) is Prompt and len(prompt.frames) == 12,
                "BAD_SYNTHETIC_PROMPT")
        return LETTERS[int(digest(asdict(prompt)), 16) % 5]


def real_adapter(*args, **kwargs):
    raise HarnessError("REAL_ADAPTER_NOT_INTEGRATED")


def atomic_json(path, obj):
    """Replace a snapshot only after fsync; uncommitted temp files are ignored."""
    temp = path.with_name(path.name + ".pending")
    with temp.open("x", encoding="utf-8") as f:
        json.dump(obj, f, sort_keys=True, allow_nan=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


class RunLock:
    """Nonblocking OS byte/flock lock; persistent file, never delete others' lock."""
    def __init__(self, root):
        self.root, self.handle = root, None

    def __enter__(self):
        check_root(self.root)
        self.handle = (self.root / "run.lock").open("a+b")
        if self.handle.seek(0, 2) == 0:
            self.handle.write(b"0")
            self.handle.flush()
        self.handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.handle.close()
            self.handle = None
            raise HarnessError("LOCK_CONFLICT") from None
        return self

    def __exit__(self, *args):
        try:
            self.handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        finally:
            self.handle.close()
            self.handle = None


def check_root(root):
    root = Path(root)
    require(root.name == "run" and root.parent.name.startswith("vlm-synth-ab-")
            and root.parent.parent.resolve() == Path(tempfile.gettempdir()).resolve()
            and not root.is_symlink() and not root.parent.is_symlink(),
            "OWNED_TEMP_ROOT_REQUIRED")
    require((root.parent / "synthetic.owner").read_text() == VERSION,
            "SYNTHETIC_OWNER_REQUIRED")
    require(root.is_dir() and not any(p.is_symlink() for p in root.iterdir()),
            "UNSAFE_SYNTHETIC_ROOT")


class Workspace:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vlm-synth-ab-")
        self.parent = Path(self.temp.name)
        (self.parent / "synthetic.owner").write_text(VERSION)
        self.root = self.parent / "run"
        self.root.mkdir()
        return self.root

    def __exit__(self, *args):
        # Verify ownership and exclusive lock before cleaning only our own temp.
        with RunLock(self.root):
            pass
        self.temp.cleanup()


class Runner:
    def __init__(self, root, policy=Policy(), resume=False):
        self.root, self.policy = Path(root), policy
        self.questions, self.scoring_key = synthetic_data(policy)
        validate_plan(self.questions, self.scoring_key)
        self.order = [(q.qid, arm) for i, q in enumerate(self.questions)
                      for arm in (("A", "B") if (i // 2) % 2 == 0 else ("B", "A"))]
        self.contract = {"namespace": "SYNTHETIC_ONLY", "policy": asdict(policy),
                         "implementation_sha256": hashlib.sha256(
                             Path(__file__).read_bytes()).hexdigest(),
                         "questions": [asdict(q) for q in self.questions],
                         "scoring_key_hash": digest(self.scoring_key),
                         "order": self.order, "planned_pairs": 24, "planned_arms": 48}
        # JSON representation normalizes tuples for comparison.
        self.contract = json.loads(json.dumps(self.contract))
        with RunLock(self.root):
            if resume:
                require(self._read("manifest.json") == self.contract,
                        "MANIFEST_CONFLICT")
                self._load()
            else:
                require(not (self.root / "manifest.json").exists() and
                        not (self.root / "state.json").exists(), "RUN_ALREADY_EXISTS")
                atomic_json(self.root / "manifest.json", self.contract)
                self._save({"contract_hash": digest(self.contract), "records": {},
                            "reserved_simulated_seconds": 0.0})

    def _read(self, name):
        try:
            return json.loads((self.root / name).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            raise HarnessError("SYNTHETIC_SNAPSHOT_UNREADABLE") from None

    def _save(self, state):
        atomic_json(self.root / "state.json", {"state": state, "checksum": digest(state)})

    def _load(self):
        require(self._read("manifest.json") == self.contract, "MANIFEST_CONFLICT")
        envelope = self._read("state.json")
        state = envelope["state"]
        require(envelope["checksum"] == digest(state) and
                state["contract_hash"] == digest(self.contract), "LEDGER_INTEGRITY")
        require(len(state["records"]) <= self.policy.max_attempts, "LEDGER_OVER_BUDGET")
        planned = {qid + ":" + arm for qid, arm in self.order}
        require(set(state["records"]) <= planned, "UNPLANNED_LEDGER_KEY")
        for record in state["records"].values():
            require(record["status"] in ("STARTED", "TERMINAL"), "BAD_LEDGER_STATE")
            if record["status"] == "TERMINAL":
                require(record["outcome"] in ("ok", "failed", "invalid"), "BAD_OUTCOME")
        require(0 <= state["reserved_simulated_seconds"] <=
                self.policy.simulated_budget_seconds, "LEDGER_TIME_OVER_BUDGET")
        return state

    def attempt(self, qid, arm, stub=None, crash_after_start=False):
        require((qid, arm) in self.order, "UNPLANNED_ATTEMPT")
        require(stub is None or isinstance(stub, SyntheticVLM), "REAL_MODEL_NOT_INTEGRATED")
        with RunLock(self.root):
            state = self._load()
            key = qid + ":" + arm
            require(key not in state["records"], "ALREADY_STARTED_NO_RETRY")
            require(len(state["records"]) < self.policy.max_attempts, "ATTEMPT_BUDGET_STOP")
            cost = 1.0 + (self.policy.candidates * 0.01 if arm == "B" else 0.0)
            require(state["reserved_simulated_seconds"] + cost <=
                    self.policy.simulated_budget_seconds, "SIMULATED_TIME_BUDGET_STOP")
            state["reserved_simulated_seconds"] += cost
            state["records"][key] = {"status": "STARTED", "synthetic_cost": cost}
            self._save(state)  # Durable debit BEFORE selector/stub, failures do not refund.
            if crash_after_start:
                raise SystemExit("SYNTHETIC_CRASH_AFTER_START")
            q = next(q for q in self.questions if q.qid == qid)
            try:
                candidates = uniform(q.duration, self.policy.candidates) if arm == "B" else ()
                frames = (select_b(SelectorInput(q.text, q.duration, candidates, self.policy),
                                   SyntheticScorer()) if arm == "B" else
                          uniform(q.duration, self.policy.frames))
                response = (stub or SyntheticVLM()).generate(
                    Prompt(q.text, q.options, frames, arm, self.policy.seed))
                outcome = "ok" if type(response) is str and response in LETTERS and len(response) == 1 else "invalid"
            except Exception:
                response, outcome = None, "failed"
            state["records"][key].update(status="TERMINAL", outcome=outcome,
                                          response=response if outcome == "ok" else None,
                                          frame_count=12 if outcome == "ok" else 0,
                                          candidate_score_ops=len(candidates) if arm == "B" else 0)
            self._save(state)

    def run(self, stop_after=None):
        require(stop_after is None or type(stop_after) is int and stop_after >= 0,
                "BAD_STOP_COUNT")
        started = 0
        for qid, arm in self.order:
            with RunLock(self.root):
                already = qid + ":" + arm in self._load()["records"]
            if already:
                continue  # STARTED without TERMINAL remains unfinished, never replayed.
            if stop_after is not None and started >= stop_after:
                break
            try:
                self.attempt(qid, arm)
            except HarnessError as exc:
                if str(exc) in ("ATTEMPT_BUDGET_STOP", "SIMULATED_TIME_BUDGET_STOP"):
                    break
                raise
            started += 1
        return self.summary()

    def summary(self):
        with RunLock(self.root):
            state = self._load()
        report = evaluate(self.questions, self.scoring_key, state["records"])
        report.update(attempts_reserved=len(state["records"]),
                      reserved_simulated_seconds=state["reserved_simulated_seconds"],
                      candidate_score_ops=sum(r.get("candidate_score_ops", 0)
                                              for r in state["records"].values()),
                      real_gpu_seconds=0, real_model_calls=0)
        return report


def evaluate(questions, scoring_key, records):
    """Scoring is downstream of generation; full plan remains the denominator."""
    validate_plan(questions, scoring_key)
    arms = {a: dict(correct=0, wrong=0, invalid=0, failed=0, unfinished=0,
                    not_started=0, planned=24) for a in ("A", "B")}
    cells = dict(both_correct=0, both_wrong=0, B_corrects_A_wrong=0,
                 B_harms_A_correct=0, invalid_pairs=0)
    clusters, strata = [], {"20_to_under30min": [], "at_least30min": []}
    for video in sorted({q.video for q in questions}):
        outcomes = []
        for q in (q for q in questions if q.video == video):
            pair = []
            for arm in ("A", "B"):
                record = records.get(q.qid + ":" + arm)
                if record is None:
                    status = "not_started"
                elif record["status"] == "STARTED":
                    status = "unfinished"
                elif record["outcome"] != "ok":
                    status = record["outcome"]
                else:
                    status = "correct" if record["response"] == scoring_key[q.qid] else "wrong"
                arms[arm][status] += 1
                pair.append(status)
            if all(s in ("correct", "wrong") for s in pair):
                category = {("correct", "correct"): "both_correct",
                            ("wrong", "wrong"): "both_wrong",
                            ("wrong", "correct"): "B_corrects_A_wrong",
                            ("correct", "wrong"): "B_harms_A_correct"}[tuple(pair)]
            else:
                category = "invalid_pairs"
            cells[category] += 1
            outcomes.append(pair)
        cluster = {"planned_pairs": 2, "A_correct": sum(x[0] == "correct" for x in outcomes),
                   "B_correct": sum(x[1] == "correct" for x in outcomes)}
        clusters.append(cluster)
        duration = next(q.duration for q in questions if q.video == video)
        strata["at_least30min" if duration >= 1800 else "20_to_under30min"].append(cluster)
    return {"scope": "SYNTHETIC_ONLY", "planned_pairs": 24, "planned_arm_attempts": 48,
            "arms": arms, "paired_matrix": cells, "video_clusters": clusters,
            "duration_strata": {k: {"video_count": len(v),
                                   "planned_pairs": sum(x["planned_pairs"] for x in v),
                                   "A_correct": sum(x["A_correct"] for x in v),
                                   "B_correct": sum(x["B_correct"] for x in v)}
                                for k, v in strata.items()},
            "statistics_notice": "SYNTHETIC_ONLY; no real statistical inference"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--synthetic", action="store_true", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromName(
            "prototypes.test_hourvideo_synthetic_ab_runner")
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        print(json.dumps({"scope": "SYNTHETIC_ONLY", "tests_run": result.testsRun,
                          "self_test": "PASS" if result.wasSuccessful() else "FAIL"}))
        return 0 if result.wasSuccessful() and result.testsRun >= 12 else 1
    with Workspace() as root:
        report = Runner(root).run()
        print(json.dumps({k: report[k] for k in
                          ("scope", "planned_pairs", "planned_arm_attempts", "attempts_reserved",
                           "real_gpu_seconds", "real_model_calls")}))
    return 0


if __name__ == "__main__":
    # Direct-file invocation needs only this public checkout on the import path.
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    raise SystemExit(main())
