"""027-only repair witnesses. All fixture QA/options/gold are invented.

No old suite imports or historical experiments. Caller supplies the fresh root
and the single shared persistent027 ledger; at most two launches,24 workers.
"""
from dataclasses import replace
import hashlib
import io
import json
import os
from pathlib import Path
import time
import unittest
from unittest.mock import patch

from temporal_evidence_adapter_025 import ContractError, TASK
from temporal_pilot_prepare_026 import (
    InputBudget, difference_mask, identity, read_manifest, same_file,
)
from temporal_pilot_coordinator_027 import Journal, command, safe_error
from temporal_pilot_supervisor_026 import FixtureWorkerBudget, Supervisor


ROOT = TAG = LOG = None


def configure(root, launch, journal):
    global ROOT, TAG, LOG
    ROOT, TAG, LOG = Path(root), str(launch), journal


def leaf(name, data=b"fictional data"):
    path = ROOT / ("v" + TAG + "-" + name)
    with open(path, "xb") as target:
        target.write(data)
    return path


def supervisor(name, keys=("a",), digest=None):
    return Supervisor(ROOT, "v" + TAG + "-" + name, keys,
                      FixtureWorkerBudget(ROOT, 24, LOG), cohort_digest=digest)


def invented_binding(name):
    data = json.dumps({"fictional": {"benchmark_dataset": [
        {"correct_answer_label": "A", "unrelated": "invented canary"}]}}).encode()
    path = leaf(name, data)
    return dict(path=str(path), size=len(data), digest=hashlib.sha256(data).hexdigest())


def scorer_command(payload):
    return command(ROOT, "--fixture-score", "--payload", json.dumps(payload))


class IdentityRepair(unittest.TestCase):
    def test_real_runtime_fixture_field_mask_and_stability(self):
        path = leaf("stable")
        before = path.stat()
        with open(path, "rb") as handle:
            opened = os.fstat(handle.fileno())
            self.assertTrue(same_file(before, opened))
            self.assertEqual(identity(opened), identity(os.fstat(handle.fileno())))
            mask = difference_mask(before, opened)
        LOG.event("FIXTURE_IDENTITY", difference=list(mask), same_file=True)
        self.assertEqual(identity(before), identity(path.stat()))
        budget = InputBudget()
        budget.register("stable", path, 1024)
        with budget.text("stable") as stream:
            self.assertEqual(stream.read(), "fictional data")
        self.assertTrue(budget.receipts[-1].complete)

    def test_cross_api_times_are_separate_but_positive_identity_required(self):
        path = leaf("api-difference")
        original = os.fstat
        class Difference:
            def __init__(self, info):
                for name in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns"):
                    setattr(self, name, getattr(info, name))
                self.st_ctime_ns += 100
        budget = InputBudget()
        budget.register("fixture", path, 1024)
        with patch("os.fstat", side_effect=lambda fd: Difference(original(fd))):
            with budget.text("fixture") as stream:
                stream.read()
        self.assertEqual(budget.diagnostics[-1]["cross_api_difference"], ("ctime_ns",))
        self.assertTrue(budget.receipts[-1].complete)
        zero = Difference(path.stat())
        zero.st_ino = 0
        self.assertFalse(same_file(zero, zero))

    def test_different_file_and_path_replacement_rejected(self):
        path, other = leaf("identity-a"), leaf("identity-b")
        self.assertFalse(same_file(path.stat(), other.stat()))
        budget = InputBudget()
        budget.register("fixture", path, 1024)
        # Simulate path replacement by a different physical path-stat record.
        from temporal_pilot_prepare_026 import checked_path
        def observed(p, directory=False):
            return (Path(p), other.stat()) if Path(p) == path else checked_path(p, directory)
        with patch("temporal_pilot_prepare_026.checked_path", side_effect=observed):
            with self.assertRaises(ContractError):
                with budget.text("fixture") as stream:
                    stream.read()
        self.assertEqual(budget.receipts[-1].byte_count, 0)
        self.assertFalse(budget.receipts[-1].complete)

    def test_growth_and_truncation_refuse_publication(self):
        for suffix, content in (("grow", b"a" * 30), ("truncate", b"b")):
            path = leaf(suffix)
            budget = InputBudget()
            budget.register(suffix, path, 1024)
            with self.assertRaises(ContractError):
                with budget.text(suffix) as stream:
                    stream.read()
                    with open(path, "wb") as target:
                        target.write(content)
            self.assertFalse(budget.receipts[-1].complete)

    def test_half_read_is_incomplete_not_a_snapshot(self):
        # Larger than TextIO's buffer, so reading one char is a genuine half read.
        path = leaf("half", b"z" * 65536)
        budget = InputBudget()
        budget.register("half", path, 65536)
        with self.assertRaises(ContractError):
            with budget.text("half") as stream:
                stream.read(1)
        self.assertFalse(budget.receipts[-1].complete)
        self.assertLess(budget.receipts[-1].byte_count, 65536)


class DurableRepair(unittest.TestCase):
    def test_restart_alias_and_same_role_cannot_refund(self):
        path = leaf("durable-input")
        budget = InputBudget(durable=LOG)
        budget.register("persistent", path, 1024, 3)
        with budget.text("persistent", "index") as stream:
            stream.read()
        recovered = InputBudget(durable=Journal(ROOT))
        recovered.register("renamed", path, 1024, 3)
        with self.assertRaises(ContractError):
            with recovered.text("renamed", "screen"):
                self.fail("alias bypass")
        recovered = InputBudget(durable=Journal(ROOT))
        recovered.register("persistent", path, 1024, 3)
        with self.assertRaises(ContractError):
            with recovered.text("persistent", "index"):
                self.fail("role bypass")

    def test_pending_reservation_retires_all_roles(self):
        path = leaf("pending")
        LOG.reserve_input("crashed", path, "index", path.stat(), 1024, 3)
        recovered = InputBudget(durable=Journal(ROOT))
        recovered.register("crashed", path, 1024, 3)
        with self.assertRaises(ContractError):
            with recovered.text("crashed", "screen"):
                self.fail("pending input bypass")

    def test_safe_error_retains_phase_kind_errno_without_payload(self):
        error = OSError(5, "FICTIONAL_PRIVATE_PAYLOAD")
        value = safe_error("manifest", "manifest", error)
        self.assertEqual(value["errno"], 5)
        self.assertEqual(value["exception_kind"], "OSError")
        self.assertNotIn("FICTIONAL_PRIVATE_PAYLOAD", json.dumps(value))
        self.assertEqual(value["phase"], "manifest")

    def test_manifest_explicit_uid_column_and_ambiguity(self):
        rows, info, duplicates = read_manifest(io.StringIO("uid,release_1\nx,true\n"), {"x"})
        self.assertEqual(info["uid_column"], "uid")
        self.assertEqual(rows["x"]["release_1"], "true")
        self.assertFalse(duplicates)
        for header in ("uid,video_uid\nx,x\n", "id,release_1\nx,true\n", "uid,uid\nx,x\n"):
            with self.assertRaises(ContractError):
                read_manifest(io.StringIO(header), {"x"})
        _, _, duplicate = read_manifest(io.StringIO("uid\nx\nx\n"), {"x"})
        self.assertEqual(duplicate, {"x"})


class ProcessScoringRepair(unittest.TestCase):
    def test_renamed_fixed_cohort_refused_in_another_process(self):
        digest = hashlib.sha256(("cohort" + TAG).encode()).hexdigest()
        supervisor("cohort-owner", digest=digest)
        peer = supervisor("cohort-peer")
        peer.start("a", command(ROOT, "--worker", "lock", "--payload", digest), timeout=4)
        self.assertEqual(peer.wait("a").state, "FAILED")
        with self.assertRaises(FileExistsError):
            supervisor("renamed-again", digest=digest)

    def test_live_child_zero_opener_and_deadline_without_wait(self):
        own = supervisor("deadline", ("slow", "peer"))
        own.start("slow", command(ROOT, "--worker", "sleep"), timeout=0.25)
        own.start("peer", command(ROOT, "--worker", "ok"), timeout=4)
        opened = []
        with self.assertRaises(ContractError):
            own.score_once(lambda: opened.append(1), lambda _: None, "x", 0)
        self.assertEqual(opened, [])
        time.sleep(0.4)
        self.assertIsNotNone(own.children["slow"][0].poll())
        self.assertEqual(own.wait("slow").state, "FAILED")
        self.assertEqual(own.wait("peer").state, "RETURNED")
        own.close_queue()

    def test_stdout_overflow_is_bounded_and_terminal_failed(self):
        own = supervisor("flood")
        own.start("a", command(ROOT, "--worker", "flood"), timeout=4)
        self.assertEqual(own.wait("a").state, "FAILED")
        self.assertLessEqual(len(own.captures["a"].data[0]), 65536)
        self.assertTrue(own.captures["a"].overflow.is_set())
        own.close_queue()

    def test_independent_child_binds_and_scores_before_publish(self):
        own = supervisor("score-pass")
        own.start("a", command(ROOT, "--worker", "ok"), timeout=4)
        self.assertEqual(own.wait("a").state, "RETURNED")
        own.close_queue()
        report = own.bound_fixture_score(scorer_command, invented_binding("score-pass.json"))
        self.assertNotEqual(report["scorer_pid"], os.getpid())
        self.assertEqual(report["report"]["n_planned"], 1)
        self.assertEqual([a["correct_known"] for a in report["report"]["arms"]], [1, 1, 1, 1])
        self.assertEqual(len(report["report"]["paired"]), 6)
        self.assertTrue(own.scoring_consumed)

    def test_bad_digest_half_read_failure_consumes_guard_no_publish(self):
        for mode in ("digest", "half", "fail"):
            own = supervisor("score-" + mode)
            own.close_queue()
            binding = invented_binding("score-" + mode + ".json")
            if mode == "digest":
                binding["digest"] = "0" * 64
            with self.assertRaises(ContractError):
                own.bound_fixture_score(scorer_command, binding, mode="full" if mode == "digest" else mode)
            self.assertTrue(own.scoring_consumed)
            with self.assertRaises(ContractError):
                own.bound_fixture_score(scorer_command, binding)
            records = own.journal.read_text()
            self.assertNotIn('"event": "SCORING_PUBLISHED"', records)
            self.assertIn('"event": "SCORING_CONSUMED"', records)


if __name__ == "__main__":
    raise SystemExit("USE_AUTHORIZED_027_COORDINATOR")
