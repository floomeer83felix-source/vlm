"""TOY_ONLY fictitious binary outcomes; no files, media, models or labels."""
import unittest
from fractions import Fraction as F
from toy_route2_pairing import Outcome, PairingError, estimate


class PairedTests(unittest.TestCase):
    def plan(self, count=1):
        return [("toy-g"+str(i), "toy-q"+str(i)) for i in range(count)]

    def rows(self, planned, scores):
        return [Outcome(g, q, arm, score) for (g, q), (t, s) in zip(planned, scores)
                for arm, score in (("S_t", t), ("S_q", s))]

    def reject(self, code, planned, rows):
        with self.assertRaisesRegex(PairingError, "^"+code+"$"):
            estimate(planned, rows)

    def test_paired_four_cells_and_full_denominator(self):
        p = self.plan(4)
        r = estimate(p, self.rows(p, [(0, 1), (1, 0), (0, 0), (1, 1)]))
        self.assertEqual((r["gains"], r["harms"], r["stable_wrong"], r["stable_correct"]),
                         (1, 1, 1, 1))
        self.assertEqual((r["group_n"], r["pair_n"], r["delta"]), (4, 4, 0))

    def test_algebra_one_question_per_source_group(self):
        p = self.plan(3)
        r = estimate(p, self.rows(p, [(0, 1), (0, 1), (1, 0)]))
        self.assertEqual(r["delta"], F(r["gains"]-r["harms"], r["group_n"]))
        self.assertEqual(r["delta"], r["group_gain_rate"]-r["group_harm_rate"])

    def test_duplicate_group_question_arm_is_rejected(self):
        p = self.plan()
        rows = self.rows(p, [(0, 1)])
        self.reject("DUPLICATE_GROUP_QUESTION_ARM", p, rows+[rows[0]])

    def test_duplicate_plan_is_rejected(self):
        p = self.plan()
        self.reject("DUPLICATE_PLANNED_PAIR", p+p, [])

    def test_missing_arm_is_not_silent_zero_or_drop(self):
        p = self.plan()
        self.reject("MISSING_ARM", p, self.rows(p, [(0, 1)])[:1])

    def test_invalid_scores_fail(self):
        p = self.plan()
        for bad in (-1, 2, None, True, 0.5):
            self.reject("INVALID_BINARY_SCORE", p,
                        [Outcome(*p[0], "S_t", 0), Outcome(*p[0], "S_q", bad)])

    def test_empty_denominator_forced_failure(self):
        self.reject("EMPTY_DENOMINATOR", [], [])

    def test_failures_remain_and_can_be_harms(self):
        p = self.plan(4)
        rows = [Outcome(g, q, a, 1 if a == "S_t" else 0,
                        "ok" if a == "S_t" else status)
                for (g, q), status in zip(p, ("failed", "invalid", "not_started", "construction_failed"))
                for a in ("S_t", "S_q")]
        r = estimate(p, rows)
        self.assertEqual((r["harms"], r["pair_n"], r["delta"]), (4, 4, -1))
        self.reject("FAILURE_MUST_SCORE_ZERO", self.plan(),
                    [Outcome("toy-g0", "toy-q0", "S_t", 1),
                     Outcome("toy-g0", "toy-q0", "S_q", 1, "failed")])

    def test_group_not_question_weighting(self):
        p = [("toy-A", "toy-1"), ("toy-A", "toy-2"), ("toy-B", "toy-3")]
        r = estimate(p, self.rows(p, [(0, 1), (0, 1), (1, 0)]))
        self.assertEqual((r["group_n"], r["pair_n"]), (2, 3))
        self.assertEqual(r["delta"], 0)
        self.assertEqual(r["question_delta"], F(1, 3))

    def test_one_question_cannot_be_relabelled_across_groups(self):
        self.reject("QUESTION_CROSSES_GROUPS",
                    [("toy-A", "toy-q"), ("toy-B", "toy-q")], [])

    def test_unplanned_pair_and_unknown_arm_fail(self):
        p = self.plan()
        self.reject("UNPLANNED_PAIR", p, [Outcome("toy-other", "toy-q0", "S_q", 0)])
        self.reject("UNKNOWN_ARM", p, [Outcome(*p[0], "other", 0)])


if __name__ == "__main__":
    unittest.main()
