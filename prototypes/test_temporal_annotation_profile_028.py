"""028-only invented container/profile and independent-join witnesses.

No legacy suite import or subprocess workers. No real file references/data.
"""
import io
import json
import unittest

from temporal_evidence_adapter_025 import (
    _Projector, ContractError, ProjectionError, STRICT_025, SKIP_NONFINITE_028,
    container_binding, project_nongold, QuestionKey, TASK, build_plan,
)
from temporal_evidence_scorer_025 import (
    OneShotScorer, FrozenLedger, TerminalAttempt, ChildExitReceipt,
)
from temporal_pilot_prepare_026 import (
    historical_projection, old_uid_fields, independent_join_requests,
    index_annotation, read_manifest,
)


def configure(root, launch, journal):
    # No fixture files/workers needed; coordinator owns suite counters.
    pass


def parse(text, *, allow=None, profile=SKIP_NONFINITE_028, **kwargs):
    return _Projector(io.StringIO(text), allow or (lambda p: False),
                      profile=profile, **kwargs).read()


def annotation(extra="", question=None):
    row = dict(video_uid="fictional-source", task=TASK,
               question=question or "How long after folding paper did a robot open a box?",
               **{"answer_%d" % i: "invented choice %d" % i for i in range(1, 6)})
    text = json.dumps({"fictional-source": {"video_metadata": {
        "video_source": "invented", "origin_video_id": "invented-origin",
        "fb_participant_id": "invented-person", "release_1": True,
        "duration_in_seconds": 100.0}, "benchmark_dataset": [row]}})
    return text[:-1] + extra + "}"


def fixture_score(text, profile=SKIP_NONFINITE_028, expected=None, diagnostic=None):
    screen = project_nongold(io.StringIO(annotation()), (QuestionKey("fictional-source", 0),))
    plan = build_plan(screen)
    ledger = FrozenLedger(tuple(TerminalAttempt(c, "RETURNED", "A") for c in plan.calls), True)
    receipt = ChildExitReceipt(("invented-exited",), ("invented-exited",), True)
    report = OneShotScorer().score(lambda: io.StringIO(text), plan, ledger, receipt,
                                  profile=profile, expected_binding=expected or container_binding(profile),
                                  diagnostic=diagnostic)
    return report


class LexicalProfile(unittest.TestCase):
    def test_strict_default_rejects_all_three_nonfinite_tokens(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(ProjectionError):
                _Projector(io.StringIO('{"discard":' + token + '}'), lambda p: False).read()

    def test_compat_skips_exact_three_without_value_decode(self):
        diagnostic, decoded = {}, []
        result = parse('{"discard":[NaN,Infinity,-Infinity]}', diagnostic=diagnostic,
                       value_observer=decoded.append)
        self.assertEqual(result, {})
        self.assertEqual(decoded, [])
        self.assertEqual(diagnostic["decoded_values"], 0)
        self.assertEqual(diagnostic["skipped_nonfinite"],
                         {"NAN": 1, "POSITIVE_INFINITY": 1, "NEGATIVE_INFINITY": 1})
        self.assertTrue(diagnostic["complete"])

    def test_retained_nonfinite_refused_before_decoder(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            seen = []
            with self.assertRaisesRegex(ProjectionError, "ADMITTED_NONFINITE_HOLD"):
                parse('{"keep":' + token + '}', allow=lambda p: p == ("keep",),
                      value_observer=seen.append)
            self.assertEqual(seen, [])

    def test_literal_boundaries_and_other_extensions_remain_illegal(self):
        values = ("NaNxxx", "Infinity0", "-Infinity_", "+Infinity", "nan", "undefined",
                  "-NaN", "inf", "0x10", "01", "1e", ".5", "--1", "/* comment */0")
        for token in values:
            with self.subTest(category="invalid_syntax"):
                with self.assertRaises(ProjectionError):
                    parse('{"discard":' + token + '}')

    def test_strings_are_not_nonfinite_and_decode_only_if_admitted(self):
        diagnostic = {}
        result = parse('{"keep":"NaN Infinity -Infinity","discard":"NaN"}',
                       allow=lambda p: p == ("keep",), diagnostic=diagnostic)
        self.assertEqual(result["keep"], "NaN Infinity -Infinity")
        self.assertEqual(diagnostic["skipped_nonfinite"], {})

    def test_duplicate_escaped_keys_and_syntax_are_not_relaxed(self):
        bad = ('{"x":NaN,"x":Infinity}', '{"x":0,"\\u0078":1}',
               '{"x":NaN,}', '{"x":[Infinity,]}', '{"x":"\\q"}',
               '{"x":"unescaped\ncontrol"}', '{"x":NaN} {}')
        for text in bad:
            with self.assertRaises(ProjectionError):
                parse(text)

    def test_size_depth_string_limits_and_unknown_profile(self):
        cases = [('{"x":[[0]]}', dict(max_depth=2)),
                 ('{"x":"abcdef"}', dict(max_bytes=8)),
                 ('{"x":"abcdef"}', dict(max_string_bytes=3, allow=lambda p: True))]
        for text, limits in cases:
            with self.assertRaises(ProjectionError):
                parse(text, **limits)
        with self.assertRaises(ProjectionError):
            container_binding("UNREGISTERED")

    def test_chunk_edges_half_read_prefix_and_eof(self):
        class OneCharacter(io.StringIO):
            def read(self, count=-1):
                return super().read(min(1, count) if count >= 0 else 1)
        diagnostic = {}
        _Projector(OneCharacter('{"x":-Infinity}'), lambda p: False,
                   profile=SKIP_NONFINITE_028, diagnostic=diagnostic).read()
        self.assertTrue(diagnostic["complete"])
        for text in ('{"x":Na', '{"x":Infinity', '{"x":-Infinit', '{"x":[NaN'):
            diagnostic = {}
            with self.assertRaises(ProjectionError):
                parse(text, diagnostic=diagnostic)
            self.assertFalse(diagnostic["complete"])
        # Entire underlying buffer prefetched does not certify parsed EOF.
        diagnostic = {}
        with self.assertRaises(ProjectionError):
            parse('{"x":NaN} trailing', diagnostic=diagnostic)
        self.assertFalse(diagnostic["complete"])

    def test_diagnostic_is_content_free_and_positions_are_not_raw_bytes(self):
        text = '{"invented_secret_key":"\u4e2d","x":undefined}'
        diagnostic = {}
        with self.assertRaises(ProjectionError):
            parse(text, diagnostic=diagnostic)
        serialized = json.dumps(diagnostic)
        self.assertNotIn("invented_secret_key", serialized)
        self.assertNotIn("undefined", serialized)
        self.assertIn(diagnostic["character_category"], ("LETTER", "PUNCTUATION"))
        self.assertLess(diagnostic["character_position"], len(text.encode("utf-8")))
        self.assertFalse(diagnostic["complete"])


class ProjectionAndJoin(unittest.TestCase):
    def test_actual_projection_boundary_instrumented_for_screen_and_inference(self):
        text = annotation(',"protected":{"correct_answer_label":NaN,"canary":[Infinity,-Infinity]}')
        key = QuestionKey("fictional-source", 0)
        for view in ("screen", "inference"):
            seen, diagnostic = [], {}
            projection = project_nongold(io.StringIO(text), (key,), view,
                profile=SKIP_NONFINITE_028, diagnostic=diagnostic, value_observer=seen.append)
            self.assertTrue(diagnostic["complete"])
            self.assertFalse(any("protected" in p or "correct_answer_label" in p or "canary" in p for p in seen))
            option_paths = [p for p in seen if str(p[-1]).startswith("answer_")]
            self.assertEqual(len(option_paths), 0 if view == "screen" else 5)
            self.assertEqual(len(projection.questions[0].options), 0 if view == "screen" else 5)

    def test_index_keeps_no_scalar_values_and_reports_original_order(self):
        text = annotation(',"skip":NaN')
        diagnostic = {}
        index = index_annotation(io.StringIO(text), profile=SKIP_NONFINITE_028, diagnostic=diagnostic)
        self.assertEqual(index.sources, ("fictional-source", "skip"))
        self.assertEqual(len(index.batch), 1)
        self.assertEqual(diagnostic["decoded_values"], 0)
        self.assertEqual(diagnostic["skipped_nonfinite"], {"NAN": 1})

    def test_admitted_task_metadata_and_options_nonfinite_hold(self):
        key = QuestionKey("fictional-source", 0)
        base = annotation()
        replacements = ((json.dumps(TASK), "NaN"), ('100.0', 'Infinity'),
                        ('"invented choice 1"', '-Infinity'))
        for old, new in replacements:
            with self.assertRaisesRegex(ProjectionError, "ADMITTED_NONFINITE_HOLD"):
                project_nongold(io.StringIO(base.replace(old, new)), (key,), "inference",
                                profile=SKIP_NONFINITE_028)

    def test_old_uid_fields_exclude_arbitrary_strings_and_source_group_slots(self):
        raw = ('{"video_uid":"invented-old","origin_video_id":"not-a-uid",'
               '"source_group":["not-a-uid-2","not-a-uid-3"],'
               '"excluded_video_uids":["invented-parent"],'
               '"questions":[{"video_uid":"forbidden-old-qa-uid"}]}')
        projected = historical_projection(io.StringIO(raw))
        self.assertEqual(old_uid_fields(projected), {"invented-old", "invented-parent"})

    def test_index_failure_still_requests_and_joins_old_uid(self):
        with self.assertRaises(ProjectionError):
            index_annotation(io.StringIO('{"bad":undefined}'), profile=SKIP_NONFINITE_028)
        old = historical_projection(io.StringIO('{"uid":"invented-old"}'))
        old_uids, requested = independent_join_requests(None, [old])
        self.assertEqual(old_uids, {"invented-old"})
        self.assertEqual(requested, old_uids)
        rows, info, duplicates = read_manifest(io.StringIO(
            "video_uid,origin_video_id\ninvented-old,invented-origin\n"), requested)
        self.assertEqual(set(rows), set(old_uids))
        self.assertEqual(info["matched"], 1)
        self.assertFalse(duplicates)


class ScoringProfileBinding(unittest.TestCase):
    def test_compat_skips_out_of_batch_gold_and_scores_only_invented_batch(self):
        text = ('{"fictional-source":{"benchmark_dataset":[{"correct_answer_label":"A"}]},'
                '"out-of-batch":{"correct_answer_label":NaN}}')
        diagnostic = {}
        report = fixture_score(text, diagnostic=diagnostic)
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.n_planned, 1)
        self.assertEqual([a.correct_known for a in report.arms], [1, 1, 1, 1])
        self.assertEqual(diagnostic["decoded_values"], 1)
        self.assertEqual(diagnostic["skipped_nonfinite"], {"NAN": 1})

    def test_bad_invented_gold_preserves_full_n_and_unknown_accuracy(self):
        for token in ('NaN', 'Infinity', '-Infinity', '"invalid"'):
            text = '{"fictional-source":{"benchmark_dataset":[{"correct_answer_label":' + token + '}]}}'
            report = fixture_score(text)
            self.assertEqual(report.status, "GOLD_SCHEMA_HOLD")
            self.assertEqual(report.n_planned, 1)
            self.assertTrue(all(a.accuracy is None for a in report.arms))
            self.assertIsNone(report.paired)

    def test_mismatch_consumes_guard_and_opener_remains_zero(self):
        projection = project_nongold(io.StringIO(annotation()), (QuestionKey("fictional-source", 0),))
        plan = build_plan(projection)
        ledger = FrozenLedger(tuple(TerminalAttempt(c, "NOT_RUN") for c in plan.calls), True)
        receipt = ChildExitReceipt(("x",), ("x",), True)
        scorer, opened = OneShotScorer(), []
        with self.assertRaisesRegex(ContractError, "SCORING_CONTAINER_BINDING_HOLD"):
            scorer.score(lambda: opened.append(1), plan, ledger, receipt,
                         profile=SKIP_NONFINITE_028, expected_binding=container_binding(STRICT_025))
        with self.assertRaises(ContractError):
            scorer.score(lambda: opened.append(1), plan, ledger, receipt)
        self.assertEqual(opened, [])


if __name__ == "__main__":
    raise SystemExit("USE_FIXED_028_COORDINATOR")
