"""Synthetic-only CPU tests; never read dataset files, IDs, or private paths."""
import unittest
import zipfile
import stat
from charades_metadata_audit import (
    AuditError, MIB, safe_members, csv_rows, summarize, public_summary)


def row(key="toy-video", subject="toy-person", actions="c000 0 1", length="10"):
    return {"id": key, "subject": subject, "actions": actions, "length": length}


def count(result, name):
    return result["train"]["counts"].get(name, 0)


def members(extra=()):
    return [zipfile.ZipInfo(n) for n in (
        "bundle/Charades_v1_train.csv", "bundle/Charades_v1_test.csv",
        "bundle/Charades_v1_classes.txt")] + list(extra)


class MetadataTests(unittest.TestCase):
    def test_p1_positive_gaps_fixed_sensitivity(self):
        s = summarize([row(actions="c000 0 1;c000 2 3;c000 5 6")], [], {"c000"})
        for key in ("p1_gap_gt0_groups", "p1_gap_gt05_groups", "p1_gap_gt1_groups", "p1_videos"):
            self.assertEqual(count(s, key), 1)
        self.assertEqual(count(s, "same_class_distinct_pairs"), 3)

    def test_touch_and_duplicate_not_p1(self):
        s = summarize([row(actions="c000 0 1;c000 1 2;c000 1 2")], [], {"c000"})
        self.assertEqual(count(s, "p1_gap_gt0_groups"), 0)
        self.assertEqual(count(s, "same_class_touch_pairs"), 1)
        self.assertEqual(count(s, "exact_duplicate_intervals"), 1)
        self.assertEqual(count(s, "valid_action_tokens"), 3)
        self.assertEqual(count(s, "unique_valid_intervals"), 2)

    def test_mixed_same_class_overlap_and_gap_is_marked(self):
        s = summarize([row(actions="c000 0 2;c000 1 3;c000 5 6")], [], {"c000"})
        self.assertEqual(count(s, "p1_qualified_with_ambiguity_groups"), 1)
        self.assertEqual(count(s, "same_class_overlap_pairs"), 1)

    def test_p2_overlap_containment_and_touch(self):
        s = summarize([row(actions="c000 0 4;c001 1 2;c002 4 5")], [], {"c000", "c001", "c002"})
        self.assertEqual(count(s, "different_class_pair_denominator"), 3)
        self.assertEqual(count(s, "p2_overlap_pairs"), 1)
        self.assertEqual(count(s, "p2_strong_overlap_pairs"), 1)
        self.assertEqual(count(s, "different_class_containment_pairs"), 1)
        self.assertEqual(count(s, "different_class_touch_pairs"), 1)

    def test_invalid_intervals_keep_full_denominator(self):
        actions = "c000 -1 1;c000 3 3;c000 9 11;c000 NaN 3;c999 1 2;bad"
        s = summarize([row(actions=actions)], [], {"c000"})
        self.assertEqual(count(s, "rows"), 1)
        self.assertEqual(count(s, "action_tokens"), 6)
        self.assertEqual(count(s, "invalid_action_tokens"), 6)
        for key in ("negative_start", "start_not_before_end", "end_exceeds_length",
                    "nonfinite_or_invalid_time", "unknown_class", "action_parse_error"):
            self.assertEqual(count(s, key), 1)

    def test_duplicate_id_blocks_both_rows_qualification(self):
        r = row(actions="c000 0 1;c000 3 4")
        s = summarize([r, dict(r)], [], {"c000"})
        self.assertEqual(count(s, "duplicate_id_extra_rows"), 1)
        self.assertEqual(count(s, "qualification_identity_or_shape_blocked_rows"), 2)
        self.assertEqual(count(s, "p1_videos"), 0)

    def test_subject_intersection_and_missing_not_independence(self):
        s = summarize([row()], [row(key="toy-other"), row(key="toy-third", subject="")], {"c000"})
        self.assertEqual(s["cross_split_subject_count"], 1)
        self.assertEqual(s["union_subject_count"], 1)
        self.assertEqual(s["test"]["counts"]["empty_subject"], 1)

    def test_empty_denominator_no_made_up_average(self):
        s = summarize([], [], {"c000"})
        self.assertIsNone(s["train"]["duration"]["mean_seconds_rounded"])
        self.assertEqual(s["cross_split_subject_count"], 0)
        self.assertEqual(s["train"]["counts"]["unique_video_ids"], 0)

    def test_headers_named_and_extra_description_not_exported(self):
        header, rows = csv_rows('id,subject,actions,length,descriptions\ntoy-v,toy-s,c000 0 1,10,"toy phrase, not real"\n')
        s = summarize(rows, [], {"c000"})
        self.assertNotIn("descriptions", repr(s))
        self.assertNotIn("toy-v", repr(s))
        self.assertIn("actions", header)
        with self.assertRaisesRegex(AuditError, "CSV_REQUIRED_HEADER"):
            csv_rows("id,subject\n")

    def test_suppression_small_positive_counts(self):
        self.assertEqual(public_summary({"x": 2, "y": 0, "z": 10}),
                         {"x": "WITHHELD_LT10", "y": 0, "z": 10})

    def test_zip_paths_collision_and_devices_rejected(self):
        for name in ("../bad.txt", "/bad.txt", "C:/bad.txt", "a\\b.txt", "CON.txt", "a/./b.txt", "bad|name.txt", "bad\x00name"):
            with self.subTest(name=name), self.assertRaises(AuditError):
                safe_members(members([zipfile.ZipInfo(name)]))
        with self.assertRaisesRegex(AuditError, "ZIP_CASE_COLLISION"):
            safe_members(members([zipfile.ZipInfo("bundle/CHARADES_V1_TRAIN.CSV")]))
        with self.assertRaisesRegex(AuditError, "ZIP_FILE_PARENT_COLLISION"):
            safe_members(members([zipfile.ZipInfo("parent"), zipfile.ZipInfo("parent/child")]))

    def test_zip_limits_special_and_nested_rejected(self):
        oversized = zipfile.ZipInfo("huge.csv"); oversized.file_size = 17*MIB
        total = members([zipfile.ZipInfo("x"+str(i)) for i in range(198)])
        symlink = zipfile.ZipInfo("link"); symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        encrypted = zipfile.ZipInfo("secret"); encrypted.flag_bits = 1
        for extras in ([oversized], [symlink], [encrypted], [zipfile.ZipInfo("inner.zip")]):
            with self.assertRaises(AuditError): safe_members(members(extras))
        with self.assertRaisesRegex(AuditError, "ZIP_TOTAL_LIMIT"): safe_members(total)

    def test_zip_unknown_script_not_extracted_and_required_enforced(self):
        selected = safe_members(members([zipfile.ZipInfo("bundle/not-run.m")]))
        self.assertEqual(len(selected), 3)
        self.assertNotIn("not-run.m", selected)
        with self.assertRaisesRegex(AuditError, "ZIP_REQUIRED_MISSING"):
            safe_members([zipfile.ZipInfo("README.txt")])


if __name__ == "__main__":
    unittest.main()
