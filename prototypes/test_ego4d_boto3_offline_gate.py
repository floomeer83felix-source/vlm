"""CPU-only fictional objects and integer chunks; no real cloud/data inputs."""
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from prototypes import ego4d_boto3_offline_gate as g


def media(n=9, suffix="01"):
    uid = "SYNTH_VIDEO_" + suffix
    return g.Request(uid, f"s3://SYNTH_BUCKET/public/v2_1/full_scale/{uid}.mp4", "media", n)


class GateTests(unittest.TestCase):
    def mapping(self, text=None, **kw):
        uids, original = g.fixture()
        return g.join_manifest(original if text is None else text, uids, "v2_1", "full_scale",
                               SYNTH_BRIDGE_CONFIRMED=True, **kw)

    def test_01_exact_join(self):
        self.assertEqual(len(self.mapping()), 2)
        self.assertEqual(g.manifest_key("v2_1", "full_scale"),
                         "public/v2_1/full_scale/manifest.csv")

    def test_02_s3_path_alias(self):
        _, text = g.fixture()
        self.assertEqual(self.mapping(text.replace("canonical_s3_location", "s3_path")), self.mapping())

    def test_03_file_uid_is_not_video_uid(self):
        _, text = g.fixture()
        with self.assertRaises(g.GateError):
            self.mapping(text.replace("video_uid", "file_uid"))
        text = "video_uid,file_uid,s3_path\nSYNTH_VIDEO_01,SYNTH_FILE_01,s3://SYNTH_BUCKET/x\n"
        with self.assertRaisesRegex(g.GateError, "FILE_UID"):
            self.mapping(text)

    def test_04_explicit_dataset_and_release(self):
        for release, dataset in (("v1.0", "full_scale"), ("v2_1", "clips"),
                                 ("v2_1", "video_540ss"), ("v2_1", "")):
            with self.assertRaises(g.GateError):
                g.manifest_key(release, dataset)

    def test_05_bridge_default_refused(self):
        uids, text = g.fixture()
        with self.assertRaisesRegex(g.GateError, "RELEASE_BRIDGE_UNKNOWN"):
            g.join_manifest(text, uids, "v2_1", "full_scale")

    def test_06_same_uid_conflict(self):
        _, text = g.fixture()
        with self.assertRaisesRegex(g.GateError, "DUPLICATE_UID"):
            self.mapping(text + text.splitlines()[1] + "\n")

    def test_07_source_and_uri_rejection(self):
        _, text = g.fixture()
        for before, after in (("s3://", "https://"), ("SYNTH_BUCKET", "SYNTH_MIRROR"),
                              ("/public/", "/../public/"), ("full_scale/", "clips/"),
                              (".mp4", ".mp4?token=fictional"), ("/public/", "\\public/")):
            with self.subTest(after=after), self.assertRaises(g.GateError):
                self.mapping(text.replace(before, after))

    def test_08_missing_uid_and_field(self):
        _, text = g.fixture()
        for altered in (text.replace("SYNTH_VIDEO_02", "SYNTH_VIDEO_03"),
                        text.replace("canonical_s3_location", "unknown")):
            with self.assertRaises(g.GateError):
                self.mapping(altered)

    def test_09_two_media_limit(self):
        with g.Workspace() as root, self.assertRaisesRegex(g.GateError, "TWO_MEDIA_LIMIT"):
            g.Ledger(root, (media(suffix="01"), media(suffix="02"), media(suffix="03")))

    def test_10_four_gib_boundary(self):
        with g.Workspace() as root:
            g.Ledger(root, (media(g.MEDIA_LIMIT),))
        with g.Workspace() as root, self.assertRaisesRegex(g.GateError, "OBJECT_LENGTH_LIMIT"):
            g.Ledger(root, (media(g.MEDIA_LIMIT + 1),))

    def test_11_eight_gib_virtual_chunks(self):
        requests = (media(g.MEDIA_LIMIT), media(g.MEDIA_LIMIT, "02"))
        with g.Workspace() as root:
            ledger = g.Ledger(root, requests)
            for r in requests:
                ledger.transfer(r.uid, g.Response((g.MEDIA_LIMIT,), g.MEDIA_LIMIT))
            summary = ledger.summary()
            self.assertEqual((summary["reserved"], summary["actually_read"]),
                             (g.TOTAL_LIMIT, g.TOTAL_LIMIT))
            self.assertLess(ledger.latest_path().stat().st_size, 5000)

    def test_12_metadata_total_and_subcap(self):
        meta = g.Request("SYNTH_META", "s3://SYNTH_BUCKET/public/v2_1/full_scale/manifest.csv",
                         "metadata", g.META_LIMIT)
        with g.Workspace() as root:
            ledger = g.Ledger(root, (meta,))
            ledger.transfer(meta.uid, g.Response((g.META_LIMIT,), g.META_LIMIT))
            self.assertEqual(ledger.summary()["reserved"], g.META_LIMIT)
        with g.Workspace() as root, self.assertRaises(g.GateError):
            g.Ledger(root, (replace(meta, length=g.META_LIMIT + 1),))
        with g.Workspace() as root, self.assertRaisesRegex(g.GateError, "TOTAL_BUDGET"):
            g.Ledger(root, (media(g.MEDIA_LIMIT), media(g.MEDIA_LIMIT, "02"), meta))

    def test_13_unknown_lengths(self):
        for value in (None, True, "9", -1, 0, 9.0):
            with g.Workspace() as root, self.assertRaises(g.GateError):
                g.Ledger(root, (media(value),))

    def test_14_reserve_before_crash_no_refund(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with self.assertRaises(SystemExit):
                ledger.transfer(r.uid, g.Response((9,), 9), crash_after_start=True)
            resumed = g.Ledger(root, (r,), resume=True)
            self.assertEqual(resumed.summary()["reserved"], 9)
            self.assertEqual(resumed.summary()["started_unfinished"], 1)
            with self.assertRaisesRegex(g.GateError, "NO_REPEAT"):
                resumed.transfer(r.uid, g.Response((9,), 9))

    def test_15_partial_read_interrupt(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with self.assertRaises(SystemExit):
                ledger.transfer(r.uid, g.Response((3, 6), 9), interrupt_after=1)
            summary = g.Ledger(root, (r,), resume=True).summary()
            self.assertEqual((summary["reserved"], summary["actually_read"]), (9, 3))

    def test_16_resume_equivalence(self):
        requests = (media(), media(suffix="02"))
        with g.Workspace() as one, g.Workspace() as two:
            a = g.Ledger(one, requests); b = g.Ledger(two, requests)
            for r in requests:
                a.transfer(r.uid, g.Response((9,), 9))
            b.transfer(requests[0].uid, g.Response((9,), 9))
            b = g.Ledger(two, requests, resume=True)
            b.transfer(requests[1].uid, g.Response((9,), 9))
            self.assertEqual(a.summary(), b.summary())

    def test_17_new_run_cannot_reset(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with self.assertRaisesRegex(g.GateError, "LEDGER_ALREADY_EXISTS"):
                g.Ledger(root, (r,), run_id="SYNTH_NEW_RUN")
            with self.assertRaisesRegex(g.GateError, "CONTRACT_CHANGED"):
                g.Ledger(root, (r,), resume=True, run_id="SYNTH_NEW_RUN")

    def test_18_contract_and_corruption(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with self.assertRaisesRegex(g.GateError, "CONTRACT_CHANGED"):
                g.Ledger(root, (replace(r, length=10),), resume=True)
            p = ledger.latest_path(); data = json.loads(p.read_text())
            data["checksum"] = "SYNTH_BAD_CHECKSUM"; p.write_text(json.dumps(data))
            with self.assertRaisesRegex(g.GateError, "LEDGER_CHECKSUM"):
                g.Ledger(root, (r,), resume=True)

    def test_19_process_lock_conflict(self):
        with g.Workspace() as root:
            g.Ledger(root, (media(),))
            code = "\n".join(["import sys", "from pathlib import Path",
                                "from prototypes import ego4d_boto3_offline_gate as g",
                                "try:", " with g.Lock(Path(sys.argv[1])): pass",
                                "except g.GateError as e: sys.exit(7 if str(e)=='LOCK_CONFLICT' else 8)"])
            with g.Lock(root):
                child = subprocess.run([sys.executable, "-B", "-c", code, str(root)],
                                       capture_output=True, timeout=10)
            self.assertEqual(child.returncode, 7)
            self.assertTrue((root / "lock").exists())

    def response_error(self, response, message):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with self.assertRaisesRegex(g.GateError, message):
                ledger.transfer(r.uid, response)
            report = ledger.summary()
            self.assertEqual(report["reserved"], 9)
            self.assertEqual(report["failed"], 1)
            with self.assertRaisesRegex(g.GateError, "NO_REPEAT"):
                ledger.transfer(r.uid, g.Response((9,), 9))
            return report

    def test_20_overlong_chunk(self):
        summary = self.response_error(g.Response((3, 7), 9), "CHUNK_EXCEEDS")
        self.assertEqual(summary["actually_read"], 3)

    def test_21_short_read(self):
        self.assertEqual(self.response_error(g.Response((4,), 9), "SHORT_READ")["actually_read"], 4)

    def test_22_error_body_is_accounted(self):
        report = self.response_error(g.Response((2, 1), 3, status=503), "HTTP_ERROR_BODY_CHARGED")
        self.assertEqual(report["actually_read"], 3)

    def test_23_retry_redirect_and_range(self):
        for response in (g.Response((9,), 9, retry=True), g.Response((9,), 9, redirected=True)):
            self.response_error(response, "RETRY_OR_REDIRECT")
        self.response_error(g.Response((9,), 9, status=206), "UNEXPECTED_RANGE")

    def test_24_etag_version_encoding_changes(self):
        for changes in ({"etag": "SYNTH_CHANGED"}, {"version_id": "SYNTH_CHANGED"},
                        {"content_length": 8}):
            self.response_error(replace(g.Response((9,), 9), **changes), "HEAD_GET_IDENTITY")
        self.response_error(g.Response((9,), 9, encoding="gzip"), "UNKNOWN_RESPONSE_BOUND")

    def test_25_failed_then_other_with_same_budget(self):
        one, two = media(), media(suffix="02")
        with g.Workspace() as root:
            ledger = g.Ledger(root, (one, two))
            with self.assertRaises(g.GateError):
                ledger.transfer(one.uid, g.Response((2,), 9))
            g.Ledger(root, (one, two), resume=True).transfer(two.uid, g.Response((9,), 9))
            report = ledger.summary()
            self.assertEqual((report["reserved"], report["actually_read"]), (18, 11))

    def test_26_stream_exception_charges_partial(self):
        def broken():
            yield 2
            raise RuntimeError("SYNTH stream exception")
        report = self.response_error(g.Response(broken(), 9), "SYNTH_EXCEPTION")
        self.assertEqual(report["actually_read"], 2)

    def test_27_live_flags_rejected(self):
        for flag in ("--real", "--profile", "--manifest", "--video", "--s3", "--download"):
            child = subprocess.run([sys.executable, "-B", "prototypes/ego4d_boto3_offline_gate.py",
                                    "--synthetic", flag, "SYNTH_FAKE"], capture_output=True, timeout=10)
            self.assertEqual(child.returncode, 2)

    def test_28_live_adapter_blocked(self):
        with self.assertRaisesRegex(g.GateError, "LIVE_ACCESS_NOT_AUTHORIZED"):
            g.live_access()

    def test_29_end_to_end(self):
        result = g.dry_run()
        self.assertEqual((result["completed"], result["reserved"], result["actually_read"]), (2, 18, 18))
        self.assertEqual(result["real_bridge"], "REAL_BRIDGE_NOT_VERIFIED")
        self.assertEqual(result["real_aws_requests"], 0)

    def test_30_duplicate_object_and_foreign_root(self):
        with g.Workspace() as root, self.assertRaises(g.GateError):
            g.Ledger(root, (media(), media()))
        with self.assertRaisesRegex(g.GateError, "OWNED_TEMP_REQUIRED"):
            g.Ledger(Path("SYNTH_NONEXISTENT"), (media(),))

    def test_31_snapshot_chain_rejects_history_damage(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            ledger.transfer(r.uid, g.Response((9,), 9))
            old = root / "snapshot_000000.json"
            doc = json.loads(old.read_text()); doc["state"]["contract"]["run_id"] = "SYNTH_CHANGED"
            old.write_text(json.dumps(doc))
            with self.assertRaisesRegex(g.GateError, "LEDGER_CHECKSUM"):
                ledger.summary()

    def test_32_pending_write_failure_never_retried(self):
        r = media()
        with g.Workspace() as root:
            ledger = g.Ledger(root, (r,))
            with patch.object(g.os, "replace", side_effect=PermissionError("SYNTH denied")) as swap:
                with self.assertRaisesRegex(g.GateError, "PERSISTENCE_STOP_NO_RETRY"):
                    ledger.transfer(r.uid, g.Response((9,), 9))
                self.assertEqual(swap.call_count, 1)
            with self.assertRaisesRegex(g.GateError, "PENDING_WRITE_STOP"):
                g.Ledger(root, (r,), resume=True)


if __name__ == "__main__":
    unittest.main()
