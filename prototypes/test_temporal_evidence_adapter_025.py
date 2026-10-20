"""All text/IDs/options/gold/numbers here are invented 025 fixtures.

No historical module, real file, model, network or subprocess is used.
Run only under the task's externally supervised CPU test budget.
"""

from contextlib import contextmanager
from dataclasses import FrozenInstanceError, replace
import copy
import io
import json
import sys
import unittest

import temporal_evidence_adapter_025 as adapter
from temporal_evidence_adapter_025 import (
    ARMS, TASK, Call, ContractError, QuestionKey, ProjectionError, build_plan,
    decompose, project_nongold, select_four,
)
from temporal_evidence_scorer_025 import (
    ChildExitReceipt, FrozenLedger, OneShotScorer, TerminalAttempt,
)


QUESTION = "How long after opening a paper gate did the toy robot lift a cube?"
SECRET = "FICTIONAL_OPAQUE_SENTINEL_025"
KEY = QuestionKey("invented-source-one", 0)
BATCH = (KEY,)


def fixture():
    row = {"video_uid": KEY.source, "task": TASK, "question": QUESTION,
           "correct_answer_label": SECRET,
           "relevant_timestamps": {"hidden": [SECRET, -2.5e12]},
           "mcq_test": {"canary": [SECRET]}}
    row.update({"answer_" + str(i): "fictional option " + str(i) for i in range(1, 6)})
    unrelated = {"video_uid": SECRET, "question": SECRET, "task": SECRET,
                 "answer_1": SECRET, "correct_answer_label": SECRET}
    metadata = {"video_source": "invented-collection", "origin_video_id": "invented-origin",
                "fb_participant_id": "invented-person", "duration_in_seconds": 1200.0,
                "release_1": True, "canonical_is_validated": True,
                "unknown_private_field": SECRET}
    return {KEY.source: {"video_metadata": metadata, "benchmark_dataset": [row, unrelated]},
            "invented-unrelated-source": {"benchmark_dataset": [unrelated], "canary": SECRET}}


def stream(data):
    return io.StringIO(json.dumps(data, ensure_ascii=True))


@contextmanager
def record_decodes():
    observed = []
    previous = adapter._Projector._decode_value

    def spy(self, token, path):
        observed.append((path, token))
        return previous(self, token, path)

    adapter._Projector._decode_value = spy
    try:
        yield observed
    finally:
        adapter._Projector._decode_value = previous


def scores():
    return tuple(float(i) for i in range(48)), (0.0,) * 48, (0.0,) * 48, (0.0,) * 48


def make_plan(data=None, batch=BATCH):
    return build_plan(project_nongold(stream(fixture() if data is None else data), batch))


def completed(plan, predictions=None):
    predictions = {} if predictions is None else predictions
    return FrozenLedger(tuple(TerminalAttempt(call, "RETURNED", predictions.get(call, "A"))
                              for call in plan.calls), True)


def exited():
    return ChildExitReceipt(("invented-child",), ("invented-child",), True)


class Opener:
    def __init__(self, data=None, raw=None):
        self.data, self.raw, self.count = data, raw, 0
        self.last_stream = None

    def __call__(self):
        self.count += 1
        self.last_stream = io.StringIO(self.raw) if self.raw is not None else stream(self.data)
        return self.last_stream


class ProjectionTests(unittest.TestCase):
    def test_nested_metadata_and_exact_screen_values(self):
        with record_decodes() as decoded:
            result = project_nongold(stream(fixture()), BATCH)
        self.assertEqual(len(result.questions), 1)
        self.assertEqual(result.questions[0].key, KEY)
        self.assertEqual(result.questions[0].question, QUESTION)
        self.assertEqual(result.questions[0].options, ())
        self.assertEqual(dict(result.sources[0].metadata)["duration_in_seconds"], 1200.0)
        self.assertTrue(dict(result.sources[0].metadata)["release_1"])
        self.assertTrue(decoded)
        self.assertFalse(any(SECRET in token for _, token in decoded))
        self.assertFalse(any(path[-1] in adapter.OPTIONS + ("correct_answer_label",)
                             for path, _ in decoded))
        self.assertTrue(all(path[0] == KEY.source for path, _ in decoded))

    def test_inference_options_only_and_no_gold(self):
        data = fixture()
        for name in adapter.OPTIONS:
            data[KEY.source]["benchmark_dataset"][0][name] = SECRET + name
        with record_decodes() as decoded:
            inference = project_nongold(stream(data), BATCH, "inference")
        self.assertEqual(len(inference.questions[0].options), 5)
        self.assertEqual(sum(path[-1] in adapter.OPTIONS for path, _ in decoded), 5)
        self.assertFalse(any(path[-1] == "correct_answer_label" for path, _ in decoded))
        screen_plan = make_plan(data)
        self.assertEqual(screen_plan, build_plan(inference))
        self.assertNotIn(SECRET, repr(screen_plan))
        self.assertNotIn(SECRET, screen_plan.questions[0].decomposition.event_a)

    def test_protected_mutation_invariance_through_selection(self):
        original, changed = fixture(), fixture()
        row = changed[KEY.source]["benchmark_dataset"][0]
        row["correct_answer_label"] = {"nested": [SECRET, True, None, 1234]}
        row["relevant_timestamps"] = [SECRET, {"nested": "\\\"{}雪"}]
        row["mcq_test"] = [None, {"canary": SECRET}]
        row.update({name: SECRET for name in adapter.OPTIONS})
        changed["invented-unrelated-source"] = {"hidden": [SECRET]}
        first = project_nongold(stream(original), BATCH)
        with record_decodes() as decoded:
            second = project_nongold(stream(changed), BATCH)
        self.assertEqual(first, second)
        self.assertEqual(build_plan(first), build_plan(second))
        self.assertFalse(any(SECRET in token for _, token in decoded))
        first_events = first.questions[0]
        second_events = second.questions[0]
        self.assertEqual(decompose(first_events.task, first_events.question),
                         decompose(second_events.task, second_events.question))
        # A fake encoder accepts question/event text only, never the fixture row.
        def selected(record):
            parts = decompose(record.task, record.question)

            def fake_encode(text):
                seed = sum(ord(char) for char in text)
                return tuple(((seed + 7 * i) % 101 - 50) / 50 for i in range(48))

            return select_four(scores()[0], fake_encode(record.question),
                               fake_encode(parts.event_a), fake_encode(parts.event_b))

        self.assertEqual(selected(first_events), selected(second_events))

    def test_one_character_chunks_and_skipped_huge_number(self):
        class TinyStream(io.StringIO):
            def read(self, count):
                return super().read(min(1, count))

        data = fixture()
        data[KEY.source]["benchmark_dataset"][0]["question"] = QUESTION.replace("paper", "雪 paper")
        raw = json.dumps(data).replace('"' + SECRET + '"', '1' * 6000)
        with record_decodes() as decoded:
            result = project_nongold(TinyStream(raw), BATCH)
        self.assertIn("雪", result.questions[0].question)
        self.assertTrue(all(len(token) < 6000 for _, token in decoded))

    def test_skip_large_escaped_values_without_scalar_decode(self):
        data = fixture()
        data[KEY.source]["benchmark_dataset"][0]["mcq_test"] = {
            "nested": [SECRET + '\\"{}[]\n雪' * 10000, 1e200, None, False]}
        with record_decodes() as decoded:
            result = project_nongold(stream(data), BATCH)
        self.assertEqual(result.questions[0].question, QUESTION)
        self.assertFalse(any(SECRET in token for _, token in decoded))

    def test_escaped_duplicate_keys_even_in_discarded_object(self):
        raw = '{"discarded":{"secret":1,"secr\\u0065t":2}}'
        with self.assertRaisesRegex(ProjectionError, "DUPLICATE_JSON_KEY"):
            project_nongold(io.StringIO(raw), BATCH)

    def test_malformed_skipped_json_and_safe_errors(self):
        cases = [
            '{"discarded":"' + SECRET,
            '{"discarded":"' + SECRET + '\\q"}',
            '{"discarded":"' + SECRET + '\\u00XY"}',
            '{"discarded":01}', '{"discarded":1.}', '{"discarded":1e+}',
            '{"discarded":NaN}', '{"discarded":[1,]}', '{"discarded":true false}',
            '{"discarded":"line\nbreak"}', '{}{}', '[]',
        ]
        for raw in cases:
            with self.subTest(case=cases.index(raw)):
                with self.assertRaises(ProjectionError) as context:
                    project_nongold(io.StringIO(raw), BATCH)
                self.assertNotIn(SECRET, str(context.exception))

    def test_size_depth_and_decoded_string_limits(self):
        with self.assertRaisesRegex(ProjectionError, "INPUT_SIZE_LIMIT"):
            project_nongold(stream(fixture()), BATCH, max_bytes=128)
        with self.assertRaisesRegex(ProjectionError, "DEPTH_LIMIT"):
            project_nongold(io.StringIO('{"x":' + '[' * 65 + '0' + ']' * 65 + '}'), BATCH)
        data = fixture()
        data[KEY.source]["benchmark_dataset"][0]["question"] = "雪" * 30
        with self.assertRaisesRegex(ProjectionError, "STRING_SIZE_LIMIT"):
            project_nongold(stream(data), BATCH, max_string_bytes=80)
        for limits in ({"max_bytes": adapter.MAX_BYTES + 1}, {"max_depth": True}):
            with self.assertRaisesRegex(ProjectionError, "INVALID_PARSER_LIMIT"):
                project_nongold(stream(fixture()), BATCH, **limits)

    def test_empty_missing_numeric_and_extra_options(self):
        for mode in ("missing", "empty", "numeric", "extra"):
            data = fixture()
            row = data[KEY.source]["benchmark_dataset"][0]
            if mode == "missing":
                del row["answer_3"]
            elif mode == "empty":
                row["answer_3"] = "  "
            elif mode == "numeric":
                row["answer_3"] = 3
            else:
                row["answer_6"] = SECRET
            project_nongold(stream(data), BATCH, "screen")
            with self.assertRaises(ProjectionError):
                project_nongold(stream(data), BATCH, "inference")

    def test_uid_type_membership_and_batch_rejection(self):
        data = fixture()
        data[KEY.source]["benchmark_dataset"][0]["video_uid"] = "invented-mismatch"
        with self.assertRaisesRegex(ProjectionError, "UID_MISMATCH"):
            project_nongold(stream(data), BATCH)
        for batch in ((), (KEY, KEY), (QuestionKey(KEY.source, True),), [KEY]):
            with self.assertRaises(ContractError):
                project_nongold(stream(fixture()), batch)
        data = fixture()
        data[KEY.source]["video_metadata"]["duration_in_seconds"] = True
        with self.assertRaisesRegex(ProjectionError, "METADATA_TYPE"):
            project_nongold(stream(data), BATCH)


class GrammarAndPlanTests(unittest.TestCase):
    def test_supported_form_whitespace_comma_and_case(self):
        result = decompose(TASK, "  HOW long\nafter folding a paper wing, did the toy robot open a box? ")
        self.assertEqual(result.status, "OK")
        self.assertEqual(result.event_a, "folding a paper wing")
        self.assertEqual(result.event_b, "the toy robot open a box")
        self.assertEqual(result.reason, "QUESTION_GIVEN_A_BEFORE_B")

    def test_ambiguous_nested_missing_and_unsupported_forms(self):
        cases = [
            "How long after the lamp was lit did the robot move?",
            "How long after painting before lunch did the toy robot stop?",
            "How long after did the toy robot stop?",
            "How long after painting did?", "How many blocks did the toy robot lift?",
            "After opening the box, what happened before closing it?",
            QUESTION[:-1], "x" * 4097,
        ]
        for question in cases:
            self.assertEqual(decompose(TASK, question).status, "UNSUPPORTED")
        self.assertEqual(decompose("invented/other-task", QUESTION).status, "UNSUPPORTED")

    def test_source_and_original_index_order_rotation_and_immutability(self):
        data = fixture()
        row = data[KEY.source]["benchmark_dataset"][0]
        data[KEY.source]["benchmark_dataset"] = [copy.deepcopy(row) for _ in range(4)]
        batch = tuple(QuestionKey(KEY.source, i) for i in (3, 1, 0, 2))
        plan = make_plan(data, batch)
        self.assertEqual(tuple(q.key.index for q in plan.questions), (0, 1, 2, 3))
        self.assertEqual(plan.n_planned, 4)
        self.assertEqual(tuple(''.join(c.arm for c in plan.calls[i:i + 4])
                               for i in range(0, 16, 4)), ("ABCD", "BCDA", "CDAB", "DABC"))
        with self.assertRaises(FrozenInstanceError):
            plan.calls = ()
        second = "invented-source-two"
        data[second] = copy.deepcopy(data[KEY.source])
        for other in data[second]["benchmark_dataset"]:
            other["video_uid"] = second
        mixed = make_plan(data, (QuestionKey(second, 2), KEY))
        self.assertEqual(tuple(q.key.source for q in mixed.questions), (second, KEY.source))

    def test_unsupported_excluded_explicitly_not_fallback_denominator(self):
        data = fixture()
        row = copy.deepcopy(data[KEY.source]["benchmark_dataset"][0])
        row["question"] = "How many paper triangles are stacked?"
        data[KEY.source]["benchmark_dataset"].append(row)
        plan = make_plan(data, (KEY, QuestionKey(KEY.source, 2)))
        self.assertEqual(plan.n_planned, 1)
        self.assertEqual(len(plan.calls), 4)
        self.assertEqual(plan.exclusions, ((QuestionKey(KEY.source, 2), "NOT_TIME_GAP_FORM"),))

    def test_mutable_projection_components_cannot_be_frozen_into_plan(self):
        projection = project_nongold(stream(fixture()), BATCH)
        bad = replace(projection, sources=list(projection.sources))
        with self.assertRaises(ContractError):
            build_plan(bad)
        source = replace(projection.sources[0], metadata=(("origin_video_id", []),))
        with self.assertRaises(ContractError):
            build_plan(replace(projection, sources=(source,)))


class SelectorTests(unittest.TestCase):
    def test_reverse_pair_counterexample_equal_anchor_quota(self):
        pts, _, _, _ = scores()
        q = tuple(0.5 if i < 12 else 0.0 for i in range(48))
        a, b = [0.0] * 48, [0.0] * 48
        a[40], b[5] = 0.9, 0.8
        result = select_four(pts, q, a, b)
        c, d = result[2:]
        self.assertEqual(c.event_pair, (40, 5))
        self.assertEqual(d.event_pair, (40, 41))
        self.assertEqual(len(c.anchors), 2)
        self.assertEqual(len(d.anchors), 2)
        self.assertNotEqual(c.indices, d.indices)
        self.assertEqual(set(c.indices) - set(c.anchors), set(range(11)) - {5})
        self.assertEqual(set(d.indices) - set(d.anchors), set(range(10)))

    def test_ordered_maxima_identical_c_d_and_swapping_changes_problem(self):
        pts, q, _, _ = scores()
        a, b = [0.0] * 48, [0.0] * 48
        a[4], b[35] = 1.0, 1.0
        original = select_four(pts, q, a, b)
        swapped = select_four(pts, q, b, a)
        self.assertEqual(original[2].indices, original[3].indices)
        self.assertEqual(original[3].event_pair, (4, 35))
        self.assertNotEqual(original[3].event_pair, swapped[3].event_pair)
        self.assertNotEqual(original[3].indices, swapped[3].indices)

    def test_exact_ties_negative_scores_and_shared_maximum(self):
        pts, _, _, _ = scores()
        for value in (0.0, -0.9, 1.0):
            result = select_four(pts, (value,) * 48, (value,) * 48, (value,) * 48)
            self.assertEqual(result[1].indices, tuple(range(12)))
            for selection in result[2:]:
                self.assertEqual(selection.event_pair, (0, 1))
                self.assertEqual(selection.evidence_status, "EVIDENCE_PRESENCE_UNVERIFIED")
                self.assertEqual(selection.indices, tuple(range(12)))
        a = [0.0] * 48
        a[25] = 1.0
        result = select_four(pts, (0.0,) * 48, a, a)
        self.assertEqual(result[2].event_pair, (0, 25))
        self.assertEqual(result[3].event_pair, (0, 25))

    def test_frame_invariants_uniform_and_question_ties(self):
        result = select_four(*scores())
        self.assertEqual(result[0].indices, (0, 4, 9, 13, 17, 21, 26, 30, 34, 38, 43, 47))
        for selection in result:
            self.assertEqual(len(selection.indices), 12)
            self.assertEqual(len(set(selection.indices)), 12)
            self.assertEqual(selection.indices, tuple(sorted(selection.indices)))
            self.assertTrue(all(0 <= x < 48 for x in selection.indices))
        q = [-1.0] * 48
        q[20] = q[21] = 0.9
        chosen = select_four(scores()[0], q, scores()[2], scores()[3])[1]
        self.assertEqual(chosen.indices, tuple(range(10)) + (20, 21))

    def test_bad_pts_scores_types_lengths_hold_without_mutation(self):
        for mode in ("pts", "nan", "infinity", "range", "boolean", "length"):
            arrays = [list(v) for v in scores()]
            if mode == "pts":
                arrays[0][1] = arrays[0][0]
            elif mode == "nan":
                arrays[1][0] = float("nan")
            elif mode == "infinity":
                arrays[2][0] = float("inf")
            elif mode == "range":
                arrays[3][0] = 1.01
            elif mode == "boolean":
                arrays[1][0] = True
            else:
                arrays[1].pop()
            with self.assertRaises(ContractError):
                select_four(*arrays)
        arrays = [list(v) for v in scores()]
        original = copy.deepcopy(arrays)
        select_four(*arrays)
        self.assertEqual(arrays, original)


class ScorerTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.data[KEY.source]["benchmark_dataset"][0]["correct_answer_label"] = " a "
        self.plan = make_plan(self.data)
        self.ledger = completed(self.plan)

    def test_premature_incomplete_unfrozen_and_live_children_zero_open(self):
        opener = Opener(self.data)
        variants = [
            (replace(self.ledger, frozen=False), exited()),
            (replace(self.ledger, attempts=self.ledger.attempts[:-1]), exited()),
            (replace(self.ledger, attempts=(replace(self.ledger.attempts[0], state="RUNNING"),)
                     + self.ledger.attempts[1:]), exited()),
            (self.ledger, ChildExitReceipt(("invented-child",), (), True)),
            (self.ledger, replace(exited(), queue_closed=False)),
            (self.ledger, ChildExitReceipt(("invented-child",), ("other-child",), True)),
            (replace(self.ledger, attempts=(self.ledger.attempts[0],) * 4), exited()),
        ]
        scorer = OneShotScorer()
        for ledger, receipt in variants:
            with self.assertRaises(ContractError):
                scorer.score(opener, self.plan, ledger, receipt)
            self.assertEqual(opener.count, 0)
        report = scorer.score(opener, self.plan, self.ledger, exited())
        self.assertEqual(report.status, "PASS")
        self.assertEqual(opener.count, 1)

    def test_single_open_gold_only_current_batch_and_close(self):
        opener = Opener(self.data)
        scorer = OneShotScorer()
        with record_decodes() as decoded:
            report = scorer.score(opener, self.plan, self.ledger, exited())
        self.assertEqual([path for path, _ in decoded],
                         [(KEY.source, "benchmark_dataset", 0, "correct_answer_label")])
        self.assertFalse(any(SECRET in token for _, token in decoded))
        self.assertEqual(report.n_planned, 1)
        self.assertTrue(all(row.accuracy == 1.0 for row in report.arms))
        self.assertEqual(len(report.paired), 6)
        self.assertEqual(report.by_source[0].report.n_planned, 1)
        self.assertTrue(opener.last_stream.closed)
        with self.assertRaisesRegex(ContractError, "ALREADY_CONSUMED"):
            scorer.score(opener, self.plan, self.ledger, exited())
        self.assertEqual(opener.count, 1)

    def test_bad_missing_and_numeric_gold_unknown_without_denominator_drop(self):
        for label in (None, 1, "A or B", "", {"nested": SECRET}):
            data = copy.deepcopy(self.data)
            if label is None:
                del data[KEY.source]["benchmark_dataset"][0]["correct_answer_label"]
            else:
                data[KEY.source]["benchmark_dataset"][0]["correct_answer_label"] = label
            report = OneShotScorer().score(Opener(data), self.plan, self.ledger, exited())
            self.assertEqual(report.status, "GOLD_SCHEMA_HOLD")
            self.assertEqual((report.n_planned, report.n_valid_gold, report.n_bad_gold), (1, 0, 1))
            self.assertTrue(all(row.accuracy is None for row in report.arms))
            self.assertIsNone(report.paired)

    def test_malformed_duplicate_and_failed_opener_no_retry_or_secret_error(self):
        for raw in ('{"x":"' + SECRET, '{"discarded":1,"discarded":2}'):
            opener = Opener(raw=raw)
            scorer = OneShotScorer()
            report = scorer.score(opener, self.plan, self.ledger, exited())
            self.assertEqual(report.status, "GOLD_SCHEMA_HOLD")
            self.assertNotIn(SECRET, repr(report))
            with self.assertRaises(ContractError):
                scorer.score(opener, self.plan, self.ledger, exited())
            self.assertEqual(opener.count, 1)
        calls = []

        def broken():
            calls.append(True)
            raise ProjectionError(SECRET)

        scorer = OneShotScorer()
        self.assertNotIn(SECRET, repr(scorer.score(broken, self.plan, self.ledger, exited())))
        with self.assertRaises(ContractError):
            scorer.score(broken, self.plan, self.ledger, exited())
        self.assertEqual(len(calls), 1)

    def test_prediction_parser_strict_and_not_run_kept(self):
        states = (("RETURNED", " a "), ("RETURNED", "Answer: A"),
                  ("INVALID", "A"), ("NOT_RUN", None))
        ledger = FrozenLedger(tuple(TerminalAttempt(call, *state)
                                    for call, state in zip(self.plan.calls, states)), True)
        report = OneShotScorer().score(Opener(self.data), self.plan, ledger, exited())
        self.assertEqual([row.correct_known for row in report.arms], [0, 0, 0, 0])
        self.assertEqual([row.invalid for row in report.arms], [1, 1, 1, 0])
        self.assertEqual(report.arms[3].not_run, 1)
        self.assertEqual(report.n_planned, 1)
        self.assertTrue(all(row.accuracy == 0.0 for row in report.arms))
        self.assertTrue(all(pair.both_wrong == 1 for pair in report.paired))

    def test_full_invented_chain_hand_computed_pairs_and_source_counts(self):
        data = fixture()
        row = data[KEY.source]["benchmark_dataset"][0]
        data[KEY.source]["benchmark_dataset"] = [copy.deepcopy(row) for _ in range(4)]
        for index, label in enumerate("ABCD"):
            data[KEY.source]["benchmark_dataset"][index]["correct_answer_label"] = label
        batch = tuple(QuestionKey(KEY.source, i) for i in range(4))
        with record_decodes() as nongold_decoded:
            inference = project_nongold(stream(data), batch, "inference")
            plan = build_plan(inference)
        self.assertFalse(any(path[-1] == "correct_answer_label" for path, _ in nongold_decoded))
        selections = tuple(select_four(*scores()) for _ in plan.questions)
        self.assertEqual(len(selections), 4)
        self.assertEqual(len(plan.calls), 16)  # Identical frames never deduplicate calls.
        responses = {"A": ("A", "A", "C", None), "B": ("A", "B", "bad", "D"),
                     "C": ("E", "B", "C", None), "D": ("A", None, "C", "D")}
        terminal = []
        for call in plan.calls:
            value = responses[call.arm][call.key.index]
            state = ("NOT_RUN" if call.arm == "A" and call.key.index == 3
                     else "FAILED" if call.arm == "C" and call.key.index == 3
                     else "INVALID" if value is None else "RETURNED")
            terminal.append(TerminalAttempt(call, state, value))
        report = OneShotScorer().score(Opener(data), plan, FrozenLedger(tuple(terminal), True), exited())
        self.assertEqual((report.n_planned, report.n_valid_gold, report.n_bad_gold), (4, 4, 0))
        self.assertEqual(tuple(row.correct_known for row in report.arms), (2, 3, 2, 3))
        expected = ((1, 1, 2, 0), (1, 1, 1, 1), (2, 0, 1, 1),
                    (1, 2, 1, 0), (2, 1, 1, 0), (1, 1, 2, 0))
        actual = tuple((p.both_correct, p.left_only, p.right_only, p.both_wrong) for p in report.paired)
        self.assertEqual(actual, expected)
        self.assertEqual(report.arms[0].not_run, 1)
        self.assertEqual(report.arms[1].invalid, 1)
        self.assertEqual(report.arms[2].failed, 1)
        self.assertEqual(report.arms[3].invalid, 1)
        self.assertEqual(report.by_source[0].report.arms, report.arms)

    def test_partial_bad_gold_preserves_known_counts_and_global_unknown(self):
        data = fixture()
        row = data[KEY.source]["benchmark_dataset"][0]
        row["correct_answer_label"] = "A"
        second = "invented-source-two"
        data[second] = copy.deepcopy(data[KEY.source])
        data[second]["benchmark_dataset"][0]["video_uid"] = second
        data[second]["benchmark_dataset"][0]["correct_answer_label"] = 1
        plan = make_plan(data, (KEY, QuestionKey(second, 0)))
        report = OneShotScorer().score(Opener(data), plan, completed(plan), exited())
        self.assertEqual((report.n_planned, report.n_valid_gold, report.n_bad_gold), (2, 1, 1))
        self.assertEqual(tuple(a.correct_known for a in report.arms), (1, 1, 1, 1))
        self.assertTrue(all(a.accuracy is None for a in report.arms))
        self.assertIsNone(report.paired)
        self.assertEqual(report.by_source[0].report.status, "PASS")
        self.assertEqual(report.by_source[1].report.status, "GOLD_SCHEMA_HOLD")

    def test_forged_queue_and_nonterminal_state_denied(self):
        opener = Opener(self.data)
        with self.assertRaises(ContractError):
            OneShotScorer().score(opener, replace(self.plan, calls=self.plan.calls[::-1]), self.ledger, exited())
        bad = replace(self.ledger, attempts=(replace(self.ledger.attempts[0], state="NOT_RUN", prediction="A"),)
                      + self.ledger.attempts[1:])
        with self.assertRaises(ContractError):
            OneShotScorer().score(opener, self.plan, bad, exited())
        self.assertEqual(opener.count, 0)

    def test_close_failure_is_hold_and_instance_stays_consumed(self):
        class BrokenClose(io.StringIO):
            def close(self):
                if not self.closed:
                    super().close()
                    raise RuntimeError(SECRET)

        scorer = OneShotScorer()
        report = scorer.score(lambda: BrokenClose(json.dumps(self.data)),
                              self.plan, self.ledger, exited())
        self.assertEqual(report.reason, "STREAM_CLOSE_FAILED")
        self.assertIsNone(report.paired)
        with self.assertRaises(ContractError):
            scorer.score(Opener(self.data), self.plan, self.ledger, exited())


class ScopeTests(unittest.TestCase):
    def test_no_model_or_third_party_modules_loaded(self):
        for name in ("torch", "numpy", "transformers", "av", "siglip", "qwen"):
            self.assertFalse(any(key == name or key.startswith(name + ".") for key in sys.modules))


if __name__ == "__main__":
    unittest.main()
