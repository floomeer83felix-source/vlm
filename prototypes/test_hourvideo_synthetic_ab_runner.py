"""Pure fictional CPU tests; no benchmark files, network or real adapters."""
import dataclasses
import json
import subprocess
import sys
import unittest
from pathlib import Path
from prototypes import hourvideo_synthetic_ab_runner as h


class InvalidStub(h.SyntheticVLM):
    def generate(self, prompt):
        return "NOT_A_LABEL"


class FailedStub(h.SyntheticVLM):
    def generate(self, prompt):
        raise RuntimeError("SYNTH failure")


class HarnessTests(unittest.TestCase):
    def test_01_fixed_plan(self):
        q, key = h.synthetic_data(h.Policy())
        h.validate_plan(q, key)
        self.assertEqual((len(q), len(key), len({x.video for x in q})), (24, 24, 12))
        self.assertEqual(len({x.video for x in q if x.duration >= 1800}), 4)

    def test_02_uniform_points(self):
        pts = h.uniform(1200, 12)
        self.assertEqual(len(set(pts)), 12)
        self.assertEqual(pts, tuple(sorted(pts)))
        self.assertTrue(all(0 <= t < 1200 for t in pts))

    def test_03_query_changes_scores(self):
        policy = h.Policy()
        pts = h.uniform(1400, 48)
        v = h.SelectorInput("SYNTH query one", 1400, pts, policy)
        other = dataclasses.replace(v, question="SYNTH query two")
        s = h.SyntheticScorer()
        self.assertNotEqual([s.score(v, t) for t in pts], [s.score(other, t) for t in pts])
        self.assertNotEqual(h.select_b(v, s), h.select_b(other, s))
        chosen = h.select_b(v, s)
        self.assertEqual(len(set(chosen)), 12)
        self.assertEqual(chosen, tuple(sorted(chosen)))

    def test_04_selector_has_no_answers_or_options(self):
        self.assertEqual(set(h.SelectorInput.__dataclass_fields__),
                         {"question", "duration", "positions", "policy"})
        self.assertNotIn("label", h.Prompt.__dataclass_fields__)
        with self.assertRaises(TypeError):
            h.SelectorInput("SYNTH q", 1200, (), h.Policy(), label="A")

    def test_05_label_change_cannot_change_selection_or_generation(self):
        q, key = h.synthetic_data(h.Policy())
        v = h.SelectorInput(q[0].text, q[0].duration, h.uniform(q[0].duration, 48), h.Policy())
        first = h.select_b(v, h.SyntheticScorer())
        prompt = h.Prompt(q[0].text, q[0].options, first, "B", 17)
        response = h.SyntheticVLM().generate(prompt)
        key[q[0].qid] = "E" if key[q[0].qid] != "E" else "A"
        self.assertEqual(first, h.select_b(v, h.SyntheticScorer()))
        self.assertEqual(response, h.SyntheticVLM().generate(prompt))

    def test_06_complete_fixed_denominator(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            report = r.run()
            self.assertEqual(report["attempts_reserved"], 48)
            self.assertEqual(sum(report["paired_matrix"].values()), 24)
            for arm in report["arms"].values():
                self.assertEqual(sum(v for k, v in arm.items() if k != "planned"), 24)
            self.assertEqual(report["candidate_score_ops"], 24 * 48)
            self.assertEqual(len(report["video_clusters"]), 12)
            self.assertEqual(report["duration_strata"]["at_least30min"]["video_count"], 4)
            self.assertEqual(report["real_model_calls"], 0)

    def test_07_all_pair_cells(self):
        qs, key = h.synthetic_data(h.Policy())
        records = {}
        patterns = [(True, True), (False, False), (False, True), (True, False)]
        for i, q in enumerate(qs):
            for arm, correct in zip(("A", "B"), patterns[i % 4]):
                wrong = next(c for c in h.LETTERS if c != key[q.qid])
                records[q.qid + ":" + arm] = dict(status="TERMINAL", outcome="ok",
                                                   response=key[q.qid] if correct else wrong)
        report = h.evaluate(qs, key, records)
        self.assertEqual(list(report["paired_matrix"].values()), [6, 6, 6, 6, 0])
        records[qs[0].qid + ":A"] = dict(status="TERMINAL", outcome="invalid")
        report = h.evaluate(qs, key, records)
        self.assertEqual(report["paired_matrix"]["invalid_pairs"], 1)

    def test_08_invalid_failure_full_denominator(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            qid = r.questions[0].qid
            r.attempt(qid, "A", InvalidStub())
            r.attempt(qid, "B", FailedStub())
            report = r.summary()
            self.assertEqual(report["arms"]["A"]["invalid"], 1)
            self.assertEqual(report["arms"]["B"]["failed"], 1)
            self.assertEqual(report["arms"]["A"]["not_started"], 23)
            self.assertEqual(report["paired_matrix"]["invalid_pairs"], 24)

    def test_09_clean_resume_equivalence(self):
        with h.Workspace() as root1, h.Workspace() as root2:
            complete = h.Runner(root1).run()
            h.Runner(root2).run(stop_after=13)
            resumed = h.Runner(root2, resume=True).run()
            self.assertEqual(complete, resumed)

    def test_10_started_interrupt_not_retried(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            qid = r.questions[0].qid
            with self.assertRaises(SystemExit):
                r.attempt(qid, "A", crash_after_start=True)
            resumed = h.Runner(root, resume=True)
            report = resumed.run()
            self.assertEqual(report["attempts_reserved"], 48)
            self.assertEqual(report["arms"]["A"]["unfinished"], 1)
            self.assertEqual(report["paired_matrix"]["invalid_pairs"], 1)
            with self.assertRaisesRegex(h.HarnessError, "NO_RETRY"):
                resumed.attempt(qid, "A")

    def test_11_process_exit_after_durable_start(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            code = "\n".join([
                "import os, sys", "from pathlib import Path",
                "from prototypes import hourvideo_synthetic_ab_runner as h",
                "class ExitStub(h.SyntheticVLM):",
                " def generate(self, prompt): os._exit(23)",
                "r=h.Runner(Path(sys.argv[1]),resume=True)",
                "r.attempt(r.questions[0].qid,'A',ExitStub())"])
            result = subprocess.run([sys.executable, "-B", "-c", code, str(root)],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 23)
            report = h.Runner(root, resume=True).run()
            self.assertEqual(report["arms"]["A"]["unfinished"], 1)
            self.assertEqual(report["attempts_reserved"], 48)

    def test_12_budget_stop_no_refund(self):
        with h.Workspace() as root:
            r = h.Runner(root, h.Policy(max_attempts=2))
            r.attempt(r.questions[0].qid, "A", FailedStub())
            report = r.run()
            self.assertEqual(report["attempts_reserved"], 2)
            self.assertEqual(report["arms"]["A"]["failed"], 1)
            self.assertEqual(sum(x["not_started"] for x in report["arms"].values()), 46)
            with self.assertRaisesRegex(h.HarnessError, "BUDGET_STOP"):
                r.attempt(r.questions[1].qid, "A")

    def test_13_simulated_deadline(self):
        with h.Workspace() as root:
            r = h.Runner(root, h.Policy(simulated_budget_seconds=1))
            report = r.run()
            self.assertEqual(report["attempts_reserved"], 1)
            self.assertEqual(report["reserved_simulated_seconds"], 1)

    def test_14_config_seed_resume_conflict(self):
        with h.Workspace() as root:
            h.Runner(root)
            with self.assertRaisesRegex(h.HarnessError, "MANIFEST_CONFLICT"):
                h.Runner(root, h.Policy(seed=99), resume=True)

    def test_15_config_policy_resume_conflict(self):
        with h.Workspace() as root:
            h.Runner(root)
            with self.assertRaisesRegex(h.HarnessError, "MANIFEST_CONFLICT"):
                h.Runner(root, h.Policy(candidates=24), resume=True)

    def test_16_manifest_label_binding_changed(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            path = root / "manifest.json"
            doc = json.loads(path.read_text())
            doc["scoring_key_hash"] = "SYNTH_CHANGED"
            path.write_text(json.dumps(doc))
            with self.assertRaisesRegex(h.HarnessError, "MANIFEST_CONFLICT"):
                h.Runner(root, resume=True)

    def test_17_ledger_corruption(self):
        with h.Workspace() as root:
            h.Runner(root)
            path = root / "state.json"
            doc = json.loads(path.read_text())
            doc["state"]["reserved_simulated_seconds"] = 100
            path.write_text(json.dumps(doc))
            with self.assertRaisesRegex(h.HarnessError, "LEDGER_INTEGRITY"):
                h.Runner(root, resume=True)

    def test_18_terminal_cannot_be_overwritten(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            qid = r.questions[0].qid
            r.attempt(qid, "A")
            before = (root / "state.json").read_bytes()
            with self.assertRaisesRegex(h.HarnessError, "NO_RETRY"):
                r.attempt(qid, "A", InvalidStub())
            self.assertEqual(before, (root / "state.json").read_bytes())

    def test_19_lock_conflict_same_process(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            with h.RunLock(root):
                with self.assertRaisesRegex(h.HarnessError, "LOCK_CONFLICT"):
                    r.run()
            self.assertTrue((root / "run.lock").exists())

    def test_20_lock_conflict_other_process(self):
        with h.Workspace() as root:
            h.Runner(root)
            code = "\n".join(["import sys", "from pathlib import Path",
                                "from prototypes import hourvideo_synthetic_ab_runner as h",
                                "try: h.Runner(Path(sys.argv[1]),resume=True)",
                                "except h.HarnessError as e:",
                                " sys.exit(7 if str(e)=='LOCK_CONFLICT' else 8)"])
            with h.RunLock(root):
                result = subprocess.run([sys.executable, "-B", "-c", code, str(root)],
                                        capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 7)

    def test_21_real_flags_fail_closed(self):
        for flag in ("--real", "--annotations", "--video", "--output-root"):
            result = subprocess.run([sys.executable, "-B", "prototypes/hourvideo_synthetic_ab_runner.py",
                                     "--synthetic", flag, "SYNTH_FAKE"],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 2)

    def test_22_real_adapter_fail_closed(self):
        with self.assertRaisesRegex(h.HarnessError, "NOT_INTEGRATED"):
            h.real_adapter()
        with h.Workspace() as root:
            r = h.Runner(root)
            with self.assertRaisesRegex(h.HarnessError, "NOT_INTEGRATED"):
                r.attempt(r.questions[0].qid, "A", object())
            self.assertEqual(r.summary()["attempts_reserved"], 0)

    def test_23_invalid_duration(self):
        for duration in (0, -1, float("nan"), float("inf"), True, "1200"):
            with self.assertRaises(h.HarnessError):
                h.uniform(duration, 12)

    def test_24_duplicate_questions(self):
        qs, key = h.synthetic_data(h.Policy())
        with self.assertRaisesRegex(h.HarnessError, "DUPLICATE_QUESTION"):
            h.validate_plan((qs[0],) + qs[:-1], key)

    def test_25_invalid_labels(self):
        qs, key = h.synthetic_data(h.Policy())
        for label in (None, "", "AA", "Z", True):
            altered = dict(key, **{qs[0].qid: label})
            with self.assertRaises(h.HarnessError):
                h.validate_plan(qs, altered)

    def test_26_candidate_deduplication_and_bounds(self):
        p = h.Policy()
        points = h.uniform(1400, 48)
        v = h.SelectorInput("SYNTH query", 1400, points + points[:4], p)
        self.assertEqual(len(h.select_b(v, h.SyntheticScorer())), 12)
        for bad in (-1, 1400, float("inf")):
            with self.assertRaises(h.HarnessError):
                h.select_b(dataclasses.replace(v, positions=points[:-1] + (bad,)), h.SyntheticScorer())

    def test_27_policy_hard_limits(self):
        for kwargs in ({"max_attempts": 49}, {"frames": 13}, {"candidates": 49},
                       {"simulated_budget_seconds": 7201}, {"version": "SYNTH_OTHER"}):
            with self.assertRaises(h.HarnessError):
                h.Policy(**kwargs).validate()

    def test_28_new_run_refuses_existing(self):
        with h.Workspace() as root:
            h.Runner(root)
            with self.assertRaisesRegex(h.HarnessError, "RUN_ALREADY_EXISTS"):
                h.Runner(root)

    def test_29_schedule_is_balanced_and_fixed(self):
        with h.Workspace() as root:
            r = h.Runner(root)
            self.assertEqual(r.order[:2], [(r.questions[0].qid, "A"), (r.questions[0].qid, "B")])
            self.assertEqual(r.order[4:6], [(r.questions[2].qid, "B"), (r.questions[2].qid, "A")])
            self.assertEqual(len(set(r.order)), 48)

    def test_30_foreign_root_rejected_before_io(self):
        with self.assertRaisesRegex(h.HarnessError, "OWNED_TEMP_ROOT_REQUIRED"):
            h.Runner(Path("SYNTH_NONEXISTENT"))

    def test_31_implementation_pin_required(self):
        with h.Workspace() as root:
            h.Runner(root)
            path = root / "manifest.json"
            doc = json.loads(path.read_text())
            self.assertEqual(len(doc["implementation_sha256"]), 64)
            doc["implementation_sha256"] = "SYNTH_OTHER_CODE"
            path.write_text(json.dumps(doc))
            with self.assertRaisesRegex(h.HarnessError, "MANIFEST_CONFLICT"):
                h.Runner(root, resume=True)


if __name__ == "__main__":
    unittest.main()
