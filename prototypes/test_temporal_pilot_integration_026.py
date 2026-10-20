"""New026 integration checks only. Every question/option/gold/worker is invented.

An explicit caller-configured new private026 output root is mandatory. There
is no default temp directory, real input reference, discovery or model command.
Worker reservations are durable across both allowed verification launches.
"""

import hashlib
import io
import json
import os
from pathlib import Path
import sys
import unittest
from dataclasses import replace

from temporal_evidence_adapter_025 import ContractError, QuestionKey, TASK, project_nongold
from temporal_pilot_prepare_026 import (
    InputBudget, MIB, ReadReceipt, binding_matches, canonical_digest,
    choose_cohort, index_annotation,
)
from temporal_pilot_supervisor_026 import FixtureWorkerBudget, Supervisor


_ROOT = None
_TAG = None
_WORKER_ELAPSED = []


def configure(root, verification_tag):
    global _ROOT, _TAG
    _ROOT, _TAG = Path(root), verification_tag


def worker_command(payload):
    # Workers can touch only026 fixture output/new public source or stdlib.
    # The tiny payload is public/invented, never a real nongold/gold source.
    module_root = Path(__file__).parent
    bootstrap = """
import sys, os
from pathlib import Path
scope = Path(sys.argv[1]).absolute()
public = Path(sys.argv[2]).absolute()
lib = (Path(sys.base_prefix)/'Lib').absolute()
def audit(event,args):
    if event.startswith(('socket.','ctypes.','subprocess.')) or event in ('os.system','os.remove','os.rename','os.rmdir','os.putenv','os.chdir'):
        raise RuntimeError('FIXTURE_SIDE_EFFECT_DENIED')
    if event == 'open':
        path = Path(os.fsdecode(args[0])).absolute()
        mode, flags = args[1:]
        write = (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if write and scope not in path.parents:
            raise RuntimeError('FIXTURE_WRITE_SCOPE')
        if not write and scope not in path.parents and public not in path.parents and lib not in path.parents:
            raise RuntimeError('FIXTURE_READ_SCOPE')
        if 'site-packages' in path.parts:
            raise RuntimeError('FIXTURE_THIRD_PARTY')
    if event in ('os.listdir','os.scandir'):
        path = Path(os.fsdecode(args[0])).absolute()
        if path != public and path != lib and lib not in path.parents:
            raise RuntimeError('FIXTURE_NO_SCAN')
sys.addaudithook(audit)
"""
    return [sys.executable, "-I", "-S", "-B", "-c", bootstrap + payload,
            str(_ROOT), str(module_root)]


class PreparationIntegration(unittest.TestCase):
    def test_cohort_uses_nongold_original_order_and_known_group_exclusions(self):
        names = ("toy-old", "toy-same-origin", "toy-same-person", "toy-first",
                 "toy-first-sibling", "toy-second")
        pairs = (("o-old", "p-old"), ("o-old", "p-2"), ("o-3", "p-old"),
                 ("o-4", "p-4"), ("o-5", "p-4"), ("o-6", "p-6"))
        data, manifest = {}, {}
        for name, (origin, person) in zip(names, pairs):
            row = {"video_uid": name, "task": TASK,
                   "question": "How long after folding a toy map did the robot open a paper box?",
                   "correct_answer_label": "FICTIONAL_NOT_ALLOWED_IN_SCREEN",
                   **{"answer_" + str(i): "fictional choice" for i in range(1, 6)}}
            data[name] = {"benchmark_dataset": [row]}
            manifest[name] = {"video_source": "toy-collection", "origin_video_id": origin,
                              "fb_participant_id": person, "release_1": "true"}
        index = index_annotation(io.StringIO(json.dumps(data)))
        projection = project_nongold(io.StringIO(json.dumps(data)), index.batch)
        selected, counts, excluded = choose_cohort(projection, manifest, {names[0]})
        self.assertEqual(tuple(row["key"].source for row in selected), (names[3], names[5]))
        self.assertEqual(counts["supported_questions"], 6)
        self.assertEqual(counts["excluded_OLD_UID"], 1)
        self.assertEqual(counts["excluded_OLD_ORIGIN"], 1)
        self.assertEqual(counts["excluded_OLD_PARTICIPANT"], 1)
        self.assertEqual(counts["excluded_COHORT_PARTICIPANT"], 1)
        self.assertEqual(counts["executable_candidates"], 0)
        self.assertTrue(all("OLD_SOURCE_MAPPING_INCOMPLETE" in row["limits"] for row in selected))
        frozen = canonical_digest([row["key"].index for row in selected])
        # Options become visible only after screen admission; no replacement.
        batch = tuple(row["key"] for row in selected)
        inf = project_nongold(io.StringIO(json.dumps(data)), batch, "inference")
        self.assertEqual(sum(len(q.options) for q in inf.questions), 10)
        self.assertEqual(frozen, canonical_digest([q.key.index for q in inf.questions]))

    def test_real_fixture_stream_binding_and_nonrefundable_open_limit(self):
        if _ROOT is None:
            self.fail("EXPLICIT_026_FIXTURE_ROOT_REQUIRED")
        path = _ROOT / ("fixture_input_" + _TAG + ".json")
        raw = b'{"fixture_only":"nongold input"}'
        with open(path, "xb") as target:
            target.write(raw)
            target.flush()
            os.fsync(target.fileno())
        budget = InputBudget()
        budget.register("fixture", path, MIB, 1)
        with budget.text("fixture") as source:
            self.assertEqual(source.read(), raw.decode())
        receipt = budget.receipts[0]
        self.assertTrue(receipt.complete)
        self.assertEqual(receipt.digest, hashlib.sha256(raw).hexdigest())
        self.assertTrue(binding_matches(receipt, receipt))
        with self.assertRaises(ContractError):
            with budget.text("fixture"):
                self.fail("OPEN_LIMIT_MUST_PRECEDE_READ")
        with self.assertRaises(ContractError):
            budget.register("other_alias", path, MIB)
        self.assertEqual(budget.reserved, len(raw))
        self.assertEqual(budget.actual, len(raw))
        self.assertEqual(budget.opens["fixture"], 1)

    def test_binding_rejects_changed_bytes_alias_identity_or_partial_read(self):
        receipt = ReadReceipt("toy", 3, "a" * 64, (1, 2, 3, 4, 5), (1, 2, 3, 4, 5), True)
        for altered in (replace(receipt, alias="other"), replace(receipt, digest="b" * 64),
                        replace(receipt, byte_count=4), replace(receipt, complete=False),
                        replace(receipt, before=(1, 9, 3, 4, 5))):
            self.assertFalse(binding_matches(receipt, altered))


class ProcessIntegration(unittest.TestCase):
    def setUp(self):
        if _ROOT is None:
            self.fail("EXPLICIT_026_FIXTURE_ROOT_REQUIRED")
        self.root = _ROOT
        self.budget = FixtureWorkerBudget(self.root)
        self.run_id = _TAG + "_" + self._testMethodName

    def supervisor(self, keys=("toy/A",), **kwargs):
        return Supervisor(self.root, self.run_id, keys, self.budget, **kwargs)

    def test_complete_worker_exit_queue_and_one_shot_cpu_callback(self):
        sup = self.supervisor(("toy/A", "toy/B"))
        pid = sup.start("toy/A", worker_command("\nprint('FIXTURE_RETURN')\n"))
        result = sup.wait("toy/A")
        _WORKER_ELAPSED.append(result.elapsed)
        self.assertEqual(result.exit_code, 0)
        self.assertNotEqual(pid, os.getpid())
        sup.close_queue()
        self.assertEqual(tuple(sup.terminal[k].state for k in sup.keys), ("RETURNED", "NOT_RUN"))
        raw = b'{"invented_score":1}'
        opens = []

        def opener():
            opens.append(True)
            return io.BytesIO(raw)

        value = sup.score_once(opener, json.load, hashlib.sha256(raw).hexdigest(), len(raw))
        self.assertEqual(value, {"invented_score": 1})
        with self.assertRaises(ContractError):
            sup.score_once(opener, json.load, hashlib.sha256(raw).hexdigest(), len(raw))
        self.assertEqual(len(opens), 1)
        self.assertTrue(sup.lock.exists())

    def test_live_child_prevents_queue_close_and_zero_opener_calls(self):
        sup = self.supervisor()
        sup.start("toy/A", worker_command("\nimport time\ntime.sleep(0.25)\n"), timeout=2)
        opens = []
        with self.assertRaises(ContractError):
            sup.score_once(lambda: opens.append(True), lambda x: None, "0" * 64, 0)
        with self.assertRaises(ContractError):
            sup.close_queue()
        self.assertFalse(opens)
        self.assertFalse(sup.scoring_consumed)
        result = sup.wait("toy/A")
        _WORKER_ELAPSED.append(result.elapsed)
        self.assertEqual(result.state, "RETURNED")
        sup.close_queue()

    def test_owned_timeout_does_not_kill_healthy_owned_peer(self):
        sup = self.supervisor(("toy/slow", "toy/peer"))
        sup.start("toy/peer", worker_command("\nimport time\ntime.sleep(0.2)\n"), timeout=2)
        sup.start("toy/slow", worker_command("\nimport time\ntime.sleep(10)\n"), timeout=0.05)
        slow = sup.wait("toy/slow")
        peer = sup.wait("toy/peer")
        _WORKER_ELAPSED.extend((slow.elapsed, peer.elapsed))
        self.assertTrue(slow.timed_out)
        self.assertEqual(slow.state, "FAILED")
        self.assertFalse(peer.timed_out)
        self.assertEqual(peer.exit_code, 0)
        sup.close_queue()
        self.assertEqual(len(sup.terminal), 2)

    def test_persistent_lock_rejects_new_process_and_started_cannot_retry(self):
        sup = self.supervisor()
        payload = """
import types
for name in ('temporal_evidence_adapter_025','temporal_pilot_prepare_026','temporal_pilot_supervisor_026'):
    file = public/(name+'.py')
    module = types.ModuleType(name); module.__file__ = str(file); sys.modules[name] = module
    exec(compile(file.read_text(encoding='utf-8'),str(file),'exec'),module.__dict__)
try:
    sys.modules['temporal_pilot_supervisor_026'].Supervisor(scope, RUN_ID, ('toy/A',), None)
except FileExistsError:
    raise SystemExit(23)
raise SystemExit(99)
""".replace("RUN_ID", repr(self.run_id))
        sup.start("toy/A", worker_command(payload))
        with self.assertRaises(ContractError):
            sup.start("toy/A", worker_command("\nraise SystemExit(0)\n"))
        result = sup.wait("toy/A")
        _WORKER_ELAPSED.append(result.elapsed)
        self.assertEqual(result.exit_code, 23)
        sup.close_queue()
        with open(sup.journal, encoding="utf-8") as source:
            events = [json.loads(line)["event"] for line in source]
        self.assertLess(events.index("STARTED"), events.index("PID"))
        self.assertLess(events.index("PID"), events.index("TERMINAL"))
        self.assertTrue(sup.lock.exists())

    def test_spawn_failure_not_run_and_scoring_failure_consume_persistent_guard(self):
        def failed_spawn(*args, **kwargs):
            raise OSError("INVENTED_SPAWN_FAILURE")

        sup = self.supervisor(("toy/A", "toy/B"), spawn=failed_spawn)
        before = self.budget.used()
        with self.assertRaises(ContractError):
            sup.start("toy/A", worker_command("\nprint('never runs')\n"))
        self.assertEqual(self.budget.used(), before + 1)
        with self.assertRaises(ContractError):
            sup.start("toy/A", worker_command("\nprint('never retries')\n"))
        sup.close_queue()
        self.assertEqual(tuple(sup.terminal[k].state for k in sup.keys), ("FAILED", "NOT_RUN"))
        opens = []

        def bad_open():
            opens.append(True)
            raise RuntimeError("INVENTED_FAILURE")

        with self.assertRaises(ContractError):
            sup.score_once(bad_open, lambda x: None, "0" * 64, 0)
        with self.assertRaises(ContractError):
            sup.score_once(bad_open, lambda x: None, "0" * 64, 0)
        self.assertEqual(len(opens), 1)
        with open(sup.journal, encoding="utf-8") as source:
            events = [json.loads(line)["event"] for line in source]
        self.assertEqual(events.count("SCORING_CONSUMED"), 1)
        self.assertIn("SCORING_FAILED_NO_RETRY", events)

    def test_snapshot_mismatch_holds_before_publication_and_cannot_reopen(self):
        sup = self.supervisor()
        sup.close_queue()
        raw = b'{"fictional_gold":"C"}'
        opens = []

        def opener():
            opens.append(True)
            return io.BytesIO(raw)

        with self.assertRaises(ContractError):
            sup.score_once(opener, json.load, "0" * 64, len(raw))
        with self.assertRaises(ContractError):
            sup.score_once(opener, json.load, hashlib.sha256(raw).hexdigest(), len(raw))
        self.assertEqual(len(opens), 1)
        with open(sup.journal, encoding="utf-8") as source:
            self.assertNotIn('"SCORING_PUBLISHED"', source.read())

    def test_separate_cpu_scorer_process_only_after_generation_exit(self):
        sup = self.supervisor()
        sup.start("toy/A", worker_command("\nprint('FICTIONAL_GENERATION')\n"))
        result = sup.wait("toy/A")
        _WORKER_ELAPSED.append(result.elapsed)
        sup.close_queue()
        raw = sup.score_child_once(worker_command("\nimport json\nprint(json.dumps({'fixture_cpu_score':1}))\n"))
        self.assertEqual(json.loads(raw), {"fixture_cpu_score": 1})
        with self.assertRaises(ContractError):
            sup.score_child_once(worker_command("\nprint('must not run')\n"))
        with open(sup.journal, encoding="utf-8") as source:
            records = [json.loads(line) for line in source]
        events = [record["event"] for record in records]
        self.assertLess(events.index("QUEUE_CLOSED"), events.index("SCORING_CPU_PID"))
        self.assertEqual(next(r["exit_code"] for r in records if r["event"] == "SCORING_CPU_EXIT"), 0)


if __name__ == "__main__":
    raise SystemExit("CONFIGURE_AN_AUTHORIZED_026_FIXTURE_ROOT_BEFORE_LOADING_TESTS")
