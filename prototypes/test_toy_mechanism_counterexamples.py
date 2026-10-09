"""TOY_ONLY: exhaustive fictitious slots and graphs; no model/media/label access."""
import unittest
from itertools import product
from toy_mechanism_counterexamples import (
    TRUE, FALSE, UNKNOWN, ToyError, never, consistent_worlds, certify_never,
    naive_never, audit_small_worlds, retract, cache_baseline,
    observe, answer_set, separates_answers)


class MechanismTests(unittest.TestCase):
    def test_two_worlds_same_view_opposite_never(self):
        view = (0, None, 0)
        worlds = consistent_worlds(view)
        self.assertIn((0, 0, 0), worlds)
        self.assertIn((0, 1, 0), worlds)
        self.assertEqual({never(w) for w in worlds}, {True, False})
        self.assertEqual(certify_never(view), UNKNOWN)

    def test_seen_event_refutes_and_full_perfect_zero_certifies(self):
        for n in range(2, 5):
            self.assertEqual(certify_never((1,)+(None,)*(n-1)), FALSE)
            self.assertEqual(certify_never((0,)*n), TRUE)

    def test_all_incomplete_no_event_views_are_unknown(self):
        for n in range(2, 5):
            for view in product((None, 0), repeat=n):
                if None in view:
                    self.assertEqual(certify_never(view), UNKNOWN)

    def test_exhaustive_perfect_observation_soundness(self):
        counts = audit_small_worlds()
        self.assertEqual(counts["views"], 117)
        self.assertEqual(counts["world_view_pairs"], 336)
        self.assertEqual((counts[TRUE], counts[FALSE], counts[UNKNOWN]), (3, 89, 25))
        self.assertEqual(counts["monitor_false_true"], 0)
        self.assertEqual(counts["monitor_false_false"], 0)

    def test_naive_unknown_to_false_gives_false_certificates(self):
        self.assertTrue(naive_never((0, None)))
        self.assertFalse(never((0, 1)))
        self.assertEqual(audit_small_worlds()["naive_false_true"], 89)

    def test_always_unknown_is_zero_useful_coverage(self):
        outputs = [UNKNOWN for view in product((None, 0, 1), repeat=3)]
        self.assertEqual(sum(x != UNKNOWN for x in outputs), 0)
        self.assertEqual(audit_small_worlds()["always_unknown_determinate"], 0)

    def test_sensor_errors_break_oracle_assumptions(self):
        self.assertEqual(certify_never((0, 0)), TRUE)  # Hypothetical missed event.
        self.assertFalse(never((0, 1)))  # Actual toy world is outside that trusted view.
        self.assertEqual(certify_never((1, 0)), FALSE)  # Hypothetical false positive.
        self.assertTrue(never((0, 0)))

    def test_retraction_locality_matches_classical_cache(self):
        deps = {"toy-a": {"toy-e0"}, "toy-b": {"toy-e1"},
                "toy-c": {"toy-a", "toy-e2"}, "toy-d": {"toy-e3"}}
        self.assertEqual(retract(deps, {"toy-e0"}), {"toy-a", "toy-c"})
        for mask in product((0, 1), repeat=4):
            invalid = {"toy-e"+str(i) for i, bit in enumerate(mask) if bit}
            self.assertEqual(retract(deps, invalid), cache_baseline(deps, invalid))

    def test_shared_source_invalidates_all_dependents(self):
        deps = {"toy-e0": {"toy-source"}, "toy-e1": {"toy-source"},
                "toy-a": {"toy-e0"}, "toy-b": {"toy-e1"}, "toy-c": {"toy-unrelated"}}
        self.assertEqual(retract(deps, {"toy-source"}), {"toy-e0", "toy-e1", "toy-a", "toy-b"})

    def test_answer_partition_distinguishing_vs_topic_only(self):
        worlds = consistent_worlds((0, None, 0))
        self.assertEqual(answer_set(worlds), {"NEVER", "SOME"})
        self.assertFalse(separates_answers(worlds, 0))
        self.assertTrue(separates_answers(worlds, 1))
        self.assertEqual(answer_set(observe(worlds, 1, 0)), {"NEVER"})
        self.assertEqual(answer_set(observe(worlds, 1, 1)), {"SOME"})

    def test_unknown_or_legal_blind_observations_cannot_resolve(self):
        worlds = consistent_worlds((0, None, 0))
        self.assertEqual(observe(worlds, 1, None), worlds)
        self.assertTrue(all(not separates_answers(worlds, i) for i in (0, 2)))
        self.assertEqual(answer_set(worlds), {"NEVER", "SOME"})

    def test_invalid_observation_rejected_not_repaired(self):
        for bad in ((), (0,), (0, True), (0, 2), (0, 0.5)):
            with self.assertRaises(ToyError):
                consistent_worlds(bad)
        with self.assertRaisesRegex(ToyError, "NO_CONSISTENT_WORLD"):
            answer_set(())


if __name__ == "__main__":
    unittest.main()
