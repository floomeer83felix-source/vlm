"""Independent stdlib synthetic assertions; no media, answers or runtime models."""

import copy
import itertools
import random
import unittest

from ordered_evidence_selector_023 import (
    BUDGET, CANDIDATES, TAU, global_top12, oep12, unordered12,
)


def toy():
    return dict(ids=list(range(48)), pts=[i * 2.5 for i in range(48)],
                s_a=[0.0] * 48, s_b=[0.0] * 48,
                s_q=[i / 64.0 for i in range(48)], decomposable=True)


class OrderedEvidenceTests(unittest.TestCase):
    def assert_hold(self, data, reason):
        for selector in (oep12, unordered12, global_top12):
            with self.subTest(selector=selector.__name__):
                result = selector(**data)
                self.assertEqual(result.status, "HOLD")
                self.assertEqual(result.reason, reason)
                self.assertEqual(result.indices, ())
                self.assertEqual(result.ids, ())
                self.assertEqual(result.anchors, ())
                self.assertIsNone(result.ab)
                self.assertIsNone(result.ba)

    def test_01_fixed_unique_chronological_budget(self):
        data = toy()
        data['s_a'][3], data['s_b'][22] = 0.9, 0.8
        for selector in (oep12, unordered12, global_top12):
            result = selector(**data)
            self.assertEqual(result.status, "OK")
            self.assertEqual(len(result.ids), BUDGET)
            self.assertEqual(len(set(result.ids)), 12)
            self.assertEqual(result.indices, tuple(sorted(result.indices)))
            self.assertTrue(all(a < b for a, b in zip(result.pts, result.pts[1:])))
            self.assertEqual(result.ids, tuple(data['ids'][i] for i in result.indices))

    def test_02_ab_only_never_invents_ba(self):
        data = toy()
        data['s_a'][2], data['s_b'][30] = 1.0, 0.875
        result = oep12(**data)
        self.assertEqual((result.ab.first, result.ab.second), (2, 30))
        self.assertEqual(result.ab.score_sum, 1.875)
        self.assertEqual((result.ab_status, result.ba_status), ('SUPPORTED', 'UNSUPPORTED'))
        self.assertIsNone(result.ba)

    def test_03_ba_only_never_invents_ab(self):
        data = toy()
        data['s_b'][2], data['s_a'][30] = 1.0, 0.875
        result = oep12(**data)
        self.assertEqual((result.ba.first, result.ba.second), (2, 30))
        self.assertEqual((result.ab_status, result.ba_status), ('UNSUPPORTED', 'SUPPORTED'))
        self.assertIsNone(result.ab)

    def test_04_both_directions_retain_four_distinct_anchors(self):
        data = toy()
        data['s_a'][2], data['s_b'][20] = 1.0, 1.0
        data['s_b'][5], data['s_a'][10] = 0.875, 0.875
        result = oep12(**data)
        self.assertEqual((result.ab.first, result.ab.second), (2, 20))
        self.assertEqual((result.ba.first, result.ba.second), (5, 10))
        self.assertEqual(result.anchors, (2, 5, 10, 20))
        self.assertTrue(set(result.anchors).issubset(result.indices))

    def test_05_pair_score_ties_use_lexicographic_indices(self):
        data = toy()
        data['s_a'][1] = data['s_a'][3] = 0.75
        data['s_b'][5] = data['s_b'][7] = 1.0
        self.assertEqual((oep12(**data).ab.first, oep12(**data).ab.second), (1, 5))

    def test_06_global_ties_use_pts_not_numeric_id(self):
        data = toy()
        data['ids'].reverse()
        data['s_q'] = [0.5] * 48
        result = global_top12(**data)
        self.assertEqual(result.indices, tuple(range(12)))
        self.assertEqual(result.ids, tuple(range(47, 35, -1)))
        self.assertEqual(oep12(**data).indices, result.indices)

    def test_07_no_events_exact_global_fallback_not_uniform(self):
        data = toy()
        data['s_q'] = [((i * 17) % 48) / 64 for i in range(48)]
        expected = tuple(sorted(i for i in range(48) if (i * 17) % 48 >= 36))
        result = oep12(**data)
        self.assertEqual(result.policy, 'GLOBAL_TOP12')
        self.assertEqual(result.reason, 'NO_SUPPORTED_DIRECTION')
        self.assertEqual(result.indices, expected)
        self.assertEqual(result.indices, global_top12(**data).indices)
        self.assertEqual(result.anchors, ())

    def test_08_no_decomposition_ignores_apparent_direction(self):
        data = toy()
        data['s_a'][1], data['s_b'][9] = 1.0, 1.0
        data['decomposable'] = False
        for selector in (oep12, unordered12):
            result = selector(**data)
            self.assertEqual(result.indices, tuple(range(36, 48)))
            self.assertEqual(result.reason, 'NOT_DECOMPOSABLE')
            self.assertEqual(result.ab_status, 'NOT_EVALUATED')
            self.assertIsNone(result.ab)

    def test_09_single_event_crowding_exposes_baseline_omission(self):
        data = toy()
        for i in range(12):
            data['s_a'][i], data['s_q'][i] = 1.0, 1.0
        data['s_b'][30] = 1.0
        baseline, ordered = global_top12(**data), oep12(**data)
        self.assertNotIn(30, baseline.indices, 'Top12 should miss low-sQ event B')
        self.assertIn(30, ordered.indices, 'OEP must retain the supported B anchor')
        self.assertEqual(ordered.anchors, (0, 30))
        self.assertEqual(ordered.indices, tuple(range(11)) + (30,))

    def test_10_temporal_reversal_swaps_direction_status(self):
        data = toy()
        data['s_a'][3], data['s_b'][35] = 0.9, 0.9
        before = oep12(**data)
        # Permute evidence across a newly valid increasing timeline, not repair
        # an invalid descending timestamp list.
        data['s_a'].reverse()
        data['s_b'].reverse()
        after = oep12(**data)
        self.assertEqual((before.ab_status, before.ba_status), ('SUPPORTED', 'UNSUPPORTED'))
        self.assertEqual((after.ab_status, after.ba_status), ('UNSUPPORTED', 'SUPPORTED'))
        self.assertEqual((after.ba.first, after.ba.second), (12, 44))

    def test_11_previous_symmetric_head_cannot_encode_direction(self):
        a, b = (1, -2, 3), (4, 5, -6)
        def representation(x, y):
            return tuple(abs(i - j) for i, j in zip(x, y)) + tuple(i * j for i, j in zip(x, y))
        self.assertNotEqual(a + b, b + a, 'An ordered representation can differ')
        self.assertEqual(representation(a, b), (3, 7, 9, 4, -10, -18))
        self.assertEqual(representation(a, b), representation(b, a),
                         'Any deterministic head of identical inputs has identical outputs')

    def test_12_duplicate_ids_hold(self):
        data = toy()
        data['ids'][1] = data['ids'][0]
        self.assert_hold(data, 'DUPLICATE_ID')

    def test_13_repeated_pts_hold_without_reordering(self):
        data = toy()
        data['pts'][7] = data['pts'][6]
        self.assert_hold(data, 'PTS_MUST_BE_STRICTLY_INCREASING')

    def test_14_descending_pts_hold(self):
        data = toy()
        data['pts'].reverse()
        self.assert_hold(data, 'PTS_MUST_BE_STRICTLY_INCREASING')

    def test_15_nonfinite_and_non_numeric_pts_hold(self):
        for bad in (float('nan'), float('inf'), -float('inf'), 10 ** 1000, True):
            with self.subTest(value_kind=type(bad).__name__):
                data = toy()
                data['pts'][2] = bad
                self.assert_hold(data, 'FINITE_PTS_REQUIRED')

    def test_16_illegal_scores_hold_in_every_channel(self):
        for field in ('s_a', 's_b', 's_q'):
            for bad in (float('nan'), float('inf'), -0.01, 1.01, '0.9', True):
                with self.subTest(field=field, kind=type(bad).__name__):
                    data = toy()
                    data[field][4] = bad
                    self.assert_hold(data, field.upper() + '_FINITE_UNIT_SCORES_REQUIRED')

    def test_17_wrong_lengths_and_insufficient_candidates_hold(self):
        for field in ('ids', 'pts', 's_a', 's_b', 's_q'):
            for length in (0, 11, 47, 49):
                with self.subTest(field=field, length=length):
                    data = toy()
                    data[field] = list(range(length))
                    self.assert_hold(data, field.upper() + '_LENGTH_MUST_BE_48')

    def test_18_threshold_is_inclusive_and_not_a_soft_hint(self):
        data = toy()
        data['s_a'][2] = data['s_b'][8] = TAU
        self.assertEqual(oep12(**data).anchors, (2, 8))
        data['s_b'][8] = TAU - 1e-12
        result = oep12(**data)
        self.assertEqual(result.ab_status, 'UNSUPPORTED')
        self.assertEqual(result.indices, tuple(range(36, 48)))

    def test_19_one_frame_supporting_both_is_not_an_ordered_pair(self):
        data = toy()
        data['s_a'][4] = data['s_b'][4] = 1.0
        ordered, unordered = oep12(**data), unordered12(**data)
        self.assertEqual((ordered.ab_status, ordered.ba_status), ('UNSUPPORTED', 'UNSUPPORTED'))
        self.assertEqual(ordered.indices, tuple(range(36, 48)))
        self.assertEqual(unordered.anchors, (4,))
        self.assertNotEqual(ordered.indices, unordered.indices,
                            'Unordered event maxima can collapse onto a single frame')

    def test_20_shared_direction_anchor_is_deduplicated(self):
        data = toy()
        data['s_a'][2] = data['s_a'][10] = 1.0
        data['s_b'][5] = 1.0
        result = oep12(**data)
        self.assertEqual(result.anchors, (2, 5, 10))
        self.assertEqual(result.indices.count(5), 1)
        self.assertEqual(len(result.indices), 12)

    def test_21_unordered_has_no_direction_constraint(self):
        data = toy()
        data['s_b'][2], data['s_a'][10] = 1.0, 1.0
        data['s_a'][1], data['s_b'][15] = 0.75, 0.75
        unordered, ordered = unordered12(**data), oep12(**data)
        self.assertEqual(unordered.anchors, (2, 10))
        self.assertEqual((unordered.ab_status, unordered.ba_status), ('NOT_EVALUATED', 'NOT_EVALUATED'))
        self.assertIsNone(unordered.ab)
        # AB sums tie at (1,2) and (10,15); lexicographic choice is (1,2).
        self.assertEqual(ordered.anchors, (1, 2, 10))
        self.assertNotEqual(ordered.indices, unordered.indices)

    def test_22_repeated_instances_cannot_certify_event_identity(self):
        data = toy()
        data['s_a'][2] = data['s_a'][40] = 0.9
        data['s_b'][20] = 0.9
        result = oep12(**data)
        # Same scores can denote one recurring action or unrelated lookalikes.
        # No instance-identity evidence is an input: both worlds are identical.
        other_world = copy.deepcopy(data)
        self.assertEqual(result, oep12(**other_world))
        self.assertEqual((result.ab_status, result.ba_status), ('SUPPORTED', 'SUPPORTED'))
        self.assertEqual(result.anchors, (2, 20, 40))
        self.assertEqual(result.reason, 'SCORE_QUALIFIED_CANDIDATES_ONLY')
        self.assertFalse(hasattr(result, 'relation_truth'))

    def test_23_pair_optima_match_independent_exhaustive_oracle(self):
        rng = random.Random(23)
        for _ in range(16):
            data = toy()
            data['s_a'] = [rng.choice((0.0, 0.5, 0.75, 0.875, 1.0)) for _ in range(48)]
            data['s_b'] = [rng.choice((0.0, 0.5, 0.75, 0.875, 1.0)) for _ in range(48)]
            result = oep12(**data)
            for first, second, observed in ((data['s_a'], data['s_b'], result.ab),
                                            (data['s_b'], data['s_a'], result.ba)):
                feasible = [(i, j) for i, j in itertools.combinations(range(48), 2)
                            if first[i] >= 0.70 and second[j] >= 0.70]
                if not feasible:
                    self.assertIsNone(observed)
                else:
                    expected = min(feasible, key=lambda pair: (-(first[pair[0]] + second[pair[1]]), pair))
                    self.assertEqual((observed.first, observed.second), expected)

    def test_24_pure_deterministic_and_input_preserving(self):
        data = toy()
        data['s_a'][2], data['s_b'][18] = 1.0, 0.9
        original = copy.deepcopy(data)
        for selector in (oep12, unordered12, global_top12):
            first = selector(**data)
            for _ in range(5):
                self.assertEqual(selector(**data), first)
            self.assertEqual(data, original)

    def test_25_invalid_flag_types_and_non_numeric_ids_hold(self):
        data = toy()
        data['decomposable'] = 1
        self.assert_hold(data, 'DECOMPOSABLE_BOOL_REQUIRED')
        for bad in ('toy-id', -1, True, 1.0):
            data = toy()
            data['ids'][0] = bad
            self.assert_hold(data, 'SYNTHETIC_NONNEGATIVE_INTEGER_IDS_REQUIRED')

    def test_26_invalid_data_never_bypasses_validation_via_fallback(self):
        data = toy()
        data['decomposable'] = False
        data['s_q'][0] = float('nan')
        self.assert_hold(data, 'S_Q_FINITE_UNIT_SCORES_REQUIRED')

    def test_27_unordered_ties_and_lone_event_are_explicit(self):
        data = toy()
        data['s_a'][3] = data['s_a'][9] = 0.9
        result = unordered12(**data)
        self.assertEqual(result.anchors, (3,))
        self.assertEqual(result.ab_status, 'NOT_EVALUATED')
        self.assertEqual(unordered12(**toy()).indices, tuple(range(36, 48)))

    def test_28_nonuniform_pts_use_order_not_assumed_index_clock(self):
        data = toy()
        data['pts'] = [float(i * i) + 0.125 for i in range(48)]
        data['s_a'][0], data['s_b'][47] = 0.875, 0.875
        result = oep12(**data)
        self.assertEqual(result.anchors, (0, 47))
        self.assertEqual(result.pts[0], 0.125)
        self.assertEqual(result.pts[-1], 2209.125)

    def test_29_anchor_priority_can_evict_a_high_question_score(self):
        data = toy()
        data['s_a'][0], data['s_b'][1] = 1.0, 1.0
        result = oep12(**data)
        self.assertEqual(result.indices, (0, 1) + tuple(range(38, 48)))
        self.assertIn(36, global_top12(**data).indices)
        self.assertNotIn(36, result.indices, 'Anchor retention sacrifices Top12 relevance; no QA guarantee')

    def test_30_iterators_and_strings_are_rejected_without_consumption(self):
        data = toy()
        data['s_a'] = iter(data['s_a'])
        self.assert_hold(data, 'S_A_LIST_OR_TUPLE_REQUIRED')
        data = toy()
        data['pts'] = '0' * CANDIDATES
        self.assert_hold(data, 'PTS_LIST_OR_TUPLE_REQUIRED')

    def test_31_finite_increasing_negative_relative_origin_is_valid(self):
        data = toy()
        data['s_a'][2], data['s_b'][30] = 0.9, 0.9
        before = oep12(**data)
        data['pts'] = [time - 50.0 for time in data['pts']]
        after = oep12(**data)
        self.assertEqual(after.status, 'OK')
        self.assertEqual(after.indices, before.indices)
        self.assertEqual(after.ab, before.ab)
        self.assertEqual(after.pts, tuple(time - 50.0 for time in before.pts))


if __name__ == '__main__':
    unittest.main(verbosity=2)
