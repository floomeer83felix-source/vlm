"""TOY ONLY, NOT FOR REAL DATA OR MODEL USE; fictitious frames, no file I/O."""
import unittest
from dataclasses import replace
from fractions import Fraction as F
from toy_g1_contract import (Frame, Source, ContractError, timeline, inside,
                             source_groups, pair_contract, validate_reference_intervals)


class ToyTests(unittest.TestCase):
    def reject(self, code, fn, *args, **kwargs):
        with self.assertRaises(ContractError) as caught:
            fn(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def scenario(self):
        a = [Frame(i, i, F(1), rgb="toy-rgb-"+str(i)) for i in range(12)]
        b = [f if i < 3 else replace(f, index=i+20, pts=F(i)*2)
             for i, f in enumerate(a)]
        b = [replace(f, pts=int(f.pts)) for f in b]
        refs = [(F(i), F(i)+F(1, 4), "closed") for i in range(3)]
        return a, b, [f.key for f in a[:3]], refs

    def pair(self, a=None, b=None, anchors=None, refs=None, **kw):
        x, y, default_anchors, default_refs = self.scenario()
        return pair_contract(x if a is None else a, y if b is None else b,
                             default_anchors if anchors is None else anchors,
                             default_refs if refs is None else refs,
                             F(0), F(0), F(1), F(1, 10), **kw)

    def test_vfr_and_explicit_nonzero_origin(self):
        fs = [Frame(i, p, F(1, 10)) for i, p in enumerate([10, 13, 21])]
        self.assertEqual(timeline(fs, F(1), F(20), F(2)), [F(20), F(103, 5), F(111, 5)])

    def test_unknown_clock_and_version(self):
        self.reject("RATIONAL_TIME_REQUIRED", timeline, [Frame(0, 0, F(1))], None, 0, 1)
        self.reject("MEDIA_VERSION_UNKNOWN", timeline, [Frame(0, 0, F(1), version="")], 0, 0, 1)

    def test_nonmonotonic_duplicate_and_missing_pts(self):
        self.reject("NONMONOTONIC_PTS", timeline, [Frame(0, 2, F(1)), Frame(1, 1, F(1))], 0, 0, 1)
        self.reject("NONMONOTONIC_PTS", timeline, [Frame(0, 1, F(1)), Frame(1, 1, F(1))], 0, 0, 1)
        self.reject("DUPLICATE_SOURCE_FRAME", timeline, [Frame(0, 0, F(1)), Frame(0, 1, F(1))], 0, 0, 1)
        self.reject("FRAME_PTS_REQUIRED", timeline, [Frame(0, None, F(1))], 0, 0, 1)

    def test_interval_edges_and_patch_mean_is_not_coverage(self):
        self.assertTrue(inside(F(1), (0, 1, "closed")))
        self.assertFalse(inside(F(1), (0, 1, "half-open")))
        interval = (F(9, 10), F(11, 10), "closed")
        self.assertFalse(any(inside(t, interval) for t in [F(0), F(2)]))
        self.assertTrue(inside(F(1), interval))  # Display mean would create a false hit.

    def test_typed_alias_parent_and_transitive_protection(self):
        ss = [Source("toy-a", ("toy-P", "episode", "1"), "toy-byte-a"),
              Source("toy-b", ("toy-P", "episode", "1"), "toy-byte-b"),
              Source("toy-c", ("toy-P", "episode", "2"), verified_parent="toy-b"),
              Source("toy-d", ("toy-Q", "episode", "3"), protected=True)]
        self.assertEqual(source_groups(ss, [("toy-c", "toy-d")])[0]["status"], "BLOCKED")
        self.assertEqual(len(source_groups([ss[0], replace(ss[1], typed_id=("toy-Q", "episode", "1"))])), 2)
        self.assertEqual(len(source_groups([ss[0], replace(ss[1], typed_id=("toy-Q", "episode", "1"), content_alias="toy-byte-a")])), 1)

    def test_missing_source_evidence_is_unknown(self):
        self.assertTrue(all(g["status"] == "UNKNOWN" for g in source_groups([
            Source("toy-x", content_alias="toy-X"), Source("toy-y", content_alias="toy-Y"),
            Source("toy-z", ("toy-P", "episode", "3"), coverage_known=False)])))

    def test_pair_unknown_fairness_even_with_equal_toy_tokens(self):
        out = self.pair(toy_token_counts=(100, 100))
        self.assertEqual(out["fairness"], "UNKNOWN")
        self.assertIn("TOKEN_BUDGET_UNKNOWN", out["warnings"])
        self.assertIn("TEMPORAL_MATCH_UNVERIFIED", out["warnings"])

    def test_twelve_unique_frames_and_anchor_identity(self):
        a, b, _, _ = self.scenario()
        self.reject("TWELVE_FRAMES_REQUIRED", self.pair, a[:-1], b)
        self.reject("DUPLICATE_SOURCE_FRAME", self.pair, a[:11]+[a[10]], b)
        self.reject("ANCHOR_IDENTITY_MISMATCH", self.pair, a, [replace(b[0], rgb="toy-changed")]+b[1:])
        self.reject("MEDIA_VERSION_MISMATCH", self.pair, a, [replace(f, version="toy-v2") for f in b])

    def test_background_guard_and_preprocess(self):
        a, b, _, _ = self.scenario()
        bad = a[:3]+[replace(a[3], pts=22, time_base=F(1, 10))]+a[4:]
        self.reject("BACKGROUND_IN_GUARD", self.pair, bad, b)
        self.reject("PREPROCESS_MISMATCH", self.pair, a,
                    b[:3]+[replace(f, size=(32, 32)) for f in b[3:]])

    def test_temporal_bins_and_token_mismatch(self):
        self.reject("TEMPORAL_MATCH_MISMATCH", self.pair, time_bins=(0, 12, 30))
        self.reject("TOKEN_BUDGET_MISMATCH", self.pair, toy_token_counts=(100, 101))
        self.assertEqual(self.pair(time_bins=(0, 30))["warnings"],
                         ["TOKEN_BUDGET_UNKNOWN", "TEMPORAL_FINE_MATCH_UNVERIFIED"])

    def test_at_least_three_intervals_is_enforced_by_pair(self):
        _, _, _, refs = self.scenario()
        for invalid in ([], refs[:1], refs[:2]):
            self.reject("AT_LEAST_THREE_REFERENCE_INTERVALS", self.pair, refs=invalid)

    def test_reference_overlap_unordered_and_duplicate(self):
        _, _, _, refs = self.scenario()
        self.reject("REFERENCE_INTERVALS_OVERLAP", self.pair,
                    refs=[(0, F(3, 2), "closed")]+refs[1:])
        self.reject("REFERENCE_INTERVALS_UNORDERED", self.pair, refs=[refs[1], refs[0], refs[2]])
        self.reject("REFERENCE_INTERVALS_OVERLAP", self.pair, refs=[refs[0], refs[0], refs[2]])

    def test_invalid_reference_endpoints_and_shape(self):
        _, _, _, refs = self.scenario()
        for endpoint in (None, True, float("nan"), "not-a-time"):
            self.reject("INVALID_REFERENCE_ENDPOINT", self.pair,
                        refs=[(endpoint, 1, "closed")]+refs[1:])
        for item in ((0, 0, "closed"), (1, 0, "closed"), (0, 1, "unknown"), (0,)):
            self.reject("INVALID_REFERENCE_INTERVAL", self.pair, refs=[item]+refs[1:])

    def test_touching_intervals_respect_endpoint_semantics(self):
        closed = [(i, i+1, "closed") for i in range(3)]
        self.reject("REFERENCE_INTERVALS_OVERLAP", validate_reference_intervals, closed)
        half_open = [(i, i+1, "half-open") for i in range(3)]
        self.assertEqual(len(validate_reference_intervals(half_open)), 3)

    def test_missing_interval_coverage_and_extra_outside_anchor(self):
        a, _, _, refs = self.scenario()
        self.reject("REFERENCE_UNCOVERED", self.pair, refs=refs[:2]+[(10, F(41, 4), "closed")])
        self.reject("ANCHOR_OUTSIDE_REFERENCE", self.pair, b=a,
                    anchors=[f.key for f in a[:4]])

    def test_equal_coarse_bins_do_not_certify_fine_time(self):
        out = self.pair(time_bins=(0, 30), toy_token_counts=(100, 100))
        self.assertEqual(out["structural"], "PASS_TOY_ONLY")
        self.assertIn("TEMPORAL_FINE_MATCH_UNVERIFIED", out["warnings"])
        self.assertEqual(out["fairness"], "UNKNOWN")

    def test_matched_toy_clocks_still_have_unknown_real_tokens(self):
        a, _, _, _ = self.scenario()
        out = self.pair(b=a, time_bins=(0, 30), toy_token_counts=(100, 100))
        self.assertEqual(out["warnings"], ["TOKEN_BUDGET_UNKNOWN"])
        self.assertEqual(out["fairness"], "UNKNOWN")
        self.assertEqual(out["real_G1"], "HOLD")

    def test_unknown_evidence_cannot_override_protected_component(self):
        known = Source("toy-known", ("toy-P", "episode", "1"))
        unknown = Source("toy-unknown", coverage_known=False)
        heldout = Source("toy-heldout", protected=True, coverage_known=False)
        self.assertEqual(source_groups([known, unknown], [(known.name, unknown.name)])[0]["status"],
                         "UNKNOWN")
        group = source_groups([known, unknown, heldout],
                              [(known.name, unknown.name), (unknown.name, heldout.name)])[0]
        self.assertEqual(group["status"], "BLOCKED")
        self.assertEqual(group["real_event_independence"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
