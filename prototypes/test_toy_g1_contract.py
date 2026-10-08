"""TOY ONLY, NOT FOR REAL DATA OR MODEL USE; fictitious frames, no file I/O."""
import unittest
from dataclasses import replace
from fractions import Fraction as F
from toy_g1_contract import Frame, Source, ContractError, timeline, inside, source_groups, pair_contract


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

    def pair(self, a=None, b=None, **kw):
        x, y, anchors, refs = self.scenario()
        return pair_contract(x if a is None else a, y if b is None else b, anchors, refs,
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
        self.assertEqual(self.pair(time_bins=(0, 30))["warnings"], ["TOKEN_BUDGET_UNKNOWN"])


if __name__ == "__main__":
    unittest.main()
