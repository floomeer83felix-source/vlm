"""Stdlib logical tests only: success supplies no real-data learnability result."""
import itertools
import math
from fractions import Fraction
import random
import unittest
from factorial_interaction_084 import (
    FIXTURE_ABS_TOL, Question, Unit, additive_scorer, fixture_truth, fixtures,
    four_logits, interaction, multiplicative_scorer, reverse_units, role_code,
    shortcut_scorer, swap_roles,
)


class FactorialInteractionTests(unittest.TestCase):
    def setUp(self):
        self.videos, self.q = fixtures()

    def close(self, left, right):
        self.assertLessEqual(abs(left - right), FIXTURE_ABS_TOL)

    def test_double_involutions(self):
        for v in self.videos:
            self.assertEqual(reverse_units(reverse_units(v)), v)
        self.assertEqual(swap_roles(swap_roles(self.q)), self.q)

    def test_actions_commute_on_pair(self):
        v, q = self.videos[0], self.q
        self.assertEqual((reverse_units(v), swap_roles(q)),
                         (reverse_units(v), swap_roles(q)))
        # Explicitly compose independent pair actions, without the operator.
        r = lambda x: (reverse_units(x[0]), x[1])
        tau = lambda x: (x[0], swap_roles(x[1]))
        self.assertEqual(r(tau((v, q))), tau(r((v, q))))

    def test_additive_cancellation_all_four_corners(self):
        for v, q in itertools.product(self.videos, (self.q, swap_roles(self.q))):
            self.close(interaction(additive_scorer, v, q), 0.0)

    def test_product_four_times_known_interaction(self):
        for v, q in itertools.product(self.videos, (self.q, swap_roles(self.q))):
            self.close(interaction(multiplicative_scorer, v, q),
                       4.0 * multiplicative_scorer(v, q))

    def test_role_and_video_oddness_for_general_tables(self):
        # Arbitrary corner values: signs follow from the operator, not an
        # assumed semantic property of any scorer.
        rng = random.Random(8401)
        v = self.videos[0]
        for _ in range(128):
            values = [rng.uniform(-100.0, 100.0) for _ in range(4)]
            table = {(vv, qq): value for (vv, qq), value in zip(
                itertools.product((v, reverse_units(v)),
                                  (self.q, swap_roles(self.q))), values)}
            scorer = lambda vv, qq: table[vv, qq]
            result = interaction(scorer, v, self.q)
            self.close(interaction(scorer, v, swap_roles(self.q)), -result)
            self.close(interaction(scorer, reverse_units(v), self.q), -result)
            self.close(interaction(scorer, reverse_units(v), swap_roles(self.q)), result)
            # Independent exact rational arithmetic on the float input values.
            exact = sum((sign * Fraction.from_float(value) for sign, value
                         in zip((1, -1, -1, 1), values)), Fraction(0))
            self.close(result, float(exact))

    def test_projection_normalization_not_new_math(self):
        # I is four times the odd/odd projection: I(I(f)) = 4 I(f).
        v = self.videos[0]
        projected = lambda vv, qq: interaction(multiplicative_scorer, vv, qq)
        self.close(interaction(projected, v, self.q),
                   4.0 * interaction(multiplicative_scorer, v, self.q))

    def test_scorer_cost_is_four_scalar_evaluations(self):
        calls = []
        def scorer(v, q):
            calls.append((v, q))
            return additive_scorer(v, q)
        interaction(scorer, self.videos[0], self.q)
        self.assertEqual(len(calls), 4)
        self.assertEqual(len(set(calls)), 4)

    def test_static_shortcut_satisfies_same_oddness(self):
        for v in self.videos:
            value = interaction(shortcut_scorer, v, self.q)
            self.close(value, 8.0)
            self.close(interaction(shortcut_scorer, reverse_units(v), self.q), -value)
            self.close(interaction(shortcut_scorer, v, swap_roles(self.q)), -value)

    def test_decoupled_semantics_defeats_shortcut(self):
        # Two complete synthetic orbits: 4/4 shortcut success on a correlated
        # orbit, 0/4 on the decoupled orbit, despite identical absolute I.
        correct = []
        for v in self.videos:
            orbit = itertools.product((v, reverse_units(v)),
                                      (self.q, swap_roles(self.q)))
            correct.append(sum((interaction(shortcut_scorer, vv, qq) > 0.0)
                               == fixture_truth(vv, qq) for vv, qq in orbit))
        self.assertEqual(correct, [4, 0])
        self.assertNotEqual(fixture_truth(self.videos[0], self.q),
                            fixture_truth(self.videos[1], self.q))

    def test_reversal_invariant_global_identity_cancels(self):
        def static_global(v, q):
            return sum(unit.badge for unit in v) * role_code(q)
        self.close(interaction(static_global, self.videos[0], self.q), 0.0)

    def test_repeatability(self):
        for scorer in (additive_scorer, multiplicative_scorer, shortcut_scorer):
            self.assertEqual([four_logits(scorer, self.videos[0], self.q) for _ in range(8)],
                             [four_logits(scorer, self.videos[0], self.q)] * 8)

    def test_nonfinite_logit_rejected(self):
        for invalid in (float('nan'), float('inf'), -float('inf')):
            with self.assertRaises(ValueError):
                interaction(lambda v, q: invalid, self.videos[0], self.q)

    def test_boolean_decision_rejected(self):
        with self.assertRaises(TypeError):
            interaction(lambda v, q: True, self.videos[0], self.q)

    def test_degenerate_role_swap_rejected(self):
        with self.assertRaises(ValueError):
            Question('A', 'A')


if __name__ == '__main__':
    unittest.main(verbosity=2)
