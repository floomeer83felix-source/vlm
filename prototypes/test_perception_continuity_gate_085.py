"""Synthetic temporary files only. These tests do not qualify real media."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from perception_continuity_gate_085 import (
    MetadataReader, StopAudit, audit, classify_continuity, inside,
)


class SafeContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'root'
        self.root.mkdir()

    def write(self, name, value):
        (self.root/name).write_text(json.dumps(value), encoding='utf-8')

    def evidence(self, **changes):
        base = dict(complete_original_recording_sealed=True,
                    time_basis='original_recording', recorded_duration=3,
                    intervals=[[0, 1], [1, 2], [2, 3]])
        base.update(changes)
        return base

    def test_inside_explicit_safe_file(self):
        self.write('parent.json', {'task': 'synthetic'})
        a = MetadataReader(self.root, ['parent.json'])
        self.assertEqual(a.meta('parent.json')['task'], 'synthetic')
        self.assertEqual(a.files, 1)
        a.meta('parent.json')
        self.assertEqual(a.files, 1)  # shared bytes, no reread

    def test_outside_rejected_before_stat(self):
        with self.assertRaisesRegex(StopAudit, 'OUTSIDE_APPROVED_ROOT'):
            inside(self.root, self.root.parent/'outside')

    def test_junction_or_symlink_resolution_guard(self):
        # A deterministic mocked resolution exercises the canonical-path check
        # even when Windows does not permit synthetic symlink creation.
        original = Path.resolve
        def resolve(path, strict=False):
            if path.name == 'parent.json':
                return self.root.parent/'outside.json'
            return original(path, strict=strict)
        with patch.object(Path, 'resolve', resolve):
            with self.assertRaisesRegex(StopAudit, 'OUTSIDE_APPROVED_ROOT'):
                inside(self.root, 'parent.json')

    def test_byte_budget_before_open(self):
        self.write('parent.json', {'x': 1})
        a = MetadataReader(self.root, ['parent.json'], max_bytes=0)
        with patch.object(Path, 'open', side_effect=AssertionError('must not open')):
            with self.assertRaisesRegex(StopAudit, 'BYTE_BUDGET'):
                a.read('parent.json')
        self.assertEqual(a.files, 0)

    def test_file_budget_before_second_open(self):
        self.write('parent.json', {})
        self.write('manifest-seal.json', {})
        a = MetadataReader(self.root, ['parent.json', 'manifest-seal.json'], max_files=1)
        a.read('parent.json')
        with self.assertRaisesRegex(StopAudit, 'FILE_BUDGET'):
            a.read('manifest-seal.json')

    def test_missing_registered_metadata(self):
        a = MetadataReader(self.root, ['parent.json'])
        with self.assertRaisesRegex(StopAudit, 'MISSING_REGISTERED_METADATA'):
            a.read('parent.json')

    def test_unknown_schema_not_peeked(self):
        self.write('unknown.json', {'answer': 'protected synthetic'})
        a = MetadataReader(self.root, ['unknown.json'])
        with patch.object(Path, 'open', side_effect=AssertionError('must not open')):
            with self.assertRaisesRegex(StopAudit, 'UNATTESTED_SCHEMA'):
                a.read('unknown.json')

    def test_known_GT_mixed_file_not_opened(self):
        self.write('media-plan.json', {'questions': ['synthetic'], 'GT': 1})
        a = MetadataReader(self.root, ['media-plan.json'])
        with patch.object(Path, 'open', side_effect=AssertionError('must not open')):
            with self.assertRaisesRegex(StopAudit, 'NOT_PERMITTED_MIXED_FILE'):
                a.read('media-plan.json')

    def test_media_stat_has_no_content_open(self):
        p = self.root/'dummy.mp4'
        p.write_bytes(b'synthetic, not a video')
        a = MetadataReader(self.root, [])
        with patch.object(Path, 'open', side_effect=AssertionError('media open forbidden')):
            self.assertEqual(a.media_stat(p, p.stat().st_size), 'SIZE_MATCH')
            self.assertEqual(a.media_stat(self.root.parent/'unread.mp4', 1),
                             'EXTERNAL_REF_UNVERIFIED')

    def test_missing_media_is_not_all_sources_no_media(self):
        a = MetadataReader(self.root, [])
        self.assertEqual(a.media_stat('absent.mp4', 1), 'MISSING_REGISTERED_MEDIA')

    def test_unknown_root_returns_safe_block(self):
        self.assertEqual(audit(self.root/'absent', [])['status'],
                         'BLOCKED_MISSING_REGISTERED_ROOT')

    def test_missing_optional_summary_does_not_force_other_root_search(self):
        self.write('parent.json', dict(task='VLM-TIMESTAMPED-TRIPLES-STREAM-081', sync_sha='be0d3ca'))
        records = [dict(group=i, path=str(self.root/(str(i)+'.mp4')),
                        bytes=579702543 if i == 0 else 1, crc=1,
                        media_directory=dict(uncompressed=579702543 if i == 0 else 1, crc=1),
                        source_generation='1685446268139925',
                        pipeline_code_sha256='bb0a1736f4fa4d48ace4a91182c96c1841529d52bfe8352d4075c0d69cf4edc3')
                   for i in range(32)]
        self.write('media-manifest.json', records)
        digest = hashlib.sha256((self.root/'media-manifest.json').read_bytes()).hexdigest()
        self.write('media-manifest-gate.json', dict(status='PASS', members=32, reused=5,
                                                  new=27, manifest_sha256=digest))
        result = audit(self.root, ['parent.json', 'manifest-seal.json',
                                  'media-manifest-gate.json', 'media-manifest.json'])
        self.assertEqual(result['status'], 'HOLD_INSUFFICIENT_TIMESTAMPS')
        self.assertEqual(result['files_read'], 3)
        self.assertEqual(result['denial_reason_counts']['MISSING_REGISTERED_METADATA'], 1)
        self.assertEqual(result['current_media_metadata_counts']['MISSING_REGISTERED_MEDIA'], 32)

    def test_natural_interval_candidate_is_only_metadata(self):
        self.assertEqual(classify_continuity(self.evidence()), 'METADATA_CANDIDATE_EXISTS')

    def test_gap_without_predeclared_tolerance(self):
        self.assertEqual(classify_continuity(self.evidence(
            intervals=[[0, .5], [1, 1.5], [2, 3]])), 'CONTIGUITY_UNCONFIRMED')

    def test_gap_exceeds_sealed_tolerance(self):
        self.assertEqual(classify_continuity(self.evidence(
            intervals=[[0, .5], [1, 1.5], [2, 3]], sealed_gap_tolerance=.1)),
            'CONTIGUITY_UNCONFIRMED')

    def test_cut_only_not_original(self):
        self.assertEqual(classify_continuity(self.evidence(media_kind='cut_only')),
                         'ONLY_CUT_OR_REASSEMBLED_EVIDENCE')

    def test_timestamp_missing_or_postprocessing_clock(self):
        for basis in (None, 'synthetic_runtime'):
            self.assertEqual(classify_continuity(self.evidence(time_basis=basis)),
                             'INSUFFICIENT_TIMESTAMPS')

    def test_invalid_order_or_zero_duration(self):
        for intervals in ([[0, 1.5], [1, 2], [2, 3]], [[0, 0], [1, 2], [2, 3]]):
            self.assertEqual(classify_continuity(self.evidence(intervals=intervals)),
                             'INVALID_INTERVALS')


if __name__ == '__main__':
    unittest.main(verbosity=2)
