"""029-only offline witnesses; invented identities, source and transport.

No actual SDK imports/network, private reads, subprocesses or old suite imports.
"""
from contextlib import contextmanager
import io
import json
from types import SimpleNamespace
import unittest

from temporal_evidence_adapter_025 import ContractError
from source_provenance_029 import (
    observe_schema, inspect_producer, bound_group_rule, project_proven_identity,
    independent_group_join, candidate_qualification, SendGate, install_head_transport,
    canonical_object, safe_network_error, project_handoff,
)


def configure(journal):
    pass


class MemoryJournal:
    def __init__(self):
        self.rows = []
    @contextmanager
    def transaction(self):
        yield self.rows
    def append(self, rows, event, **values):
        rows.append(dict(event=event, **values))


WRITER = '''
record("invented.json", {"source_group": (meta["video_source"], meta["origin_video_id"]),
       "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
'''


class ProvenanceWitnesses(unittest.TestCase):
    def test_schema_complete_zero_scalar_decode_even_secret_values(self):
        result = observe_schema(io.StringIO('{"source_group":["invented","private-origin"],"gold":NaN}'))
        self.assertTrue(result["diagnostic"]["complete"])
        self.assertEqual(result["diagnostic"]["decoded_values"], 0)
        self.assertNotIn("private-origin", json.dumps(result))
        self.assertIn({"path": ["source_group"], "kind": "array"}, result["nodes"])

    def test_unproven_tuple_refused_without_any_source_read(self):
        class NoRead:
            def read(self, *args):
                self.fail("must not open")
        with self.assertRaises(ContractError):
            project_proven_identity(NoRead(), None)

    def test_direct_writer_and_artifact_fingerprint_jointly_required(self):
        proof = inspect_producer(WRITER)
        self.assertEqual(len(proof["output_proofs"]), 1)
        rule = bound_group_rule(proof, producer_digest="invented-digest",
                                binding_digest="invented-digest", output_name="invented.json")
        self.assertIsNotNone(rule)
        value = project_proven_identity(io.StringIO('{"source_group":["v","o"],"gold":"SECRET"}'), rule)
        self.assertEqual(value["source_group"], {0: "v", 1: "o"})
        self.assertNotIn("SECRET", json.dumps(value))

    def test_digest_mismatch_filename_similarity_or_reader_not_binding(self):
        proof = inspect_producer(WRITER)
        self.assertIsNone(bound_group_rule(proof, producer_digest="a", binding_digest="b", output_name="invented.json"))
        self.assertIsNone(bound_group_rule(proof, producer_digest="a", binding_digest="a", output_name="other.json"))
        reader = inspect_producer('x = prior["source_group"]\nrecord("invented.json", x)')
        self.assertIsNone(bound_group_rule(reader, producer_digest="a", binding_digest="a", output_name="invented.json"))

    def test_unrelated_group_literal_and_write_call_do_not_make_output_proof(self):
        proof = inspect_producer('x={"source_group":(m["video_source"],m["origin_video_id"])}\nrecord("invented.json", result)')
        self.assertEqual(len(proof["source_group_semantics"]), 1)
        self.assertEqual(proof["output_proofs"], [])
        self.assertIsNone(bound_group_rule(proof, producer_digest="a", binding_digest="a", output_name="invented.json"))

    def test_independent_group_join_retains_multiple_canonical_aliases(self):
        csv = 'video_uid,video_source,origin_video_id,fb_participant_id\nold-a,s,g,p\nold-b,s,g,p\nnew,s,n,q\n'
        joined = independent_group_join(io.StringIO(csv), ["new"], (), [("s", "g")])
        self.assertEqual(set(joined["rows"]), {"old-a", "old-b", "new"})
        self.assertEqual(set(joined["group_matches"][0]["uids"]), {"old-a", "old-b"})
        self.assertFalse(joined["group_matches"][0]["unique"])

    def test_group_overlap_is_exclusion_without_exact_old_uid(self):
        candidates = ["a", "b", "c", "d"]
        rows = {u: {"video_source": "s", "origin_video_id": "g" if u == "a" else u,
                    "fb_participant_id": u} for u in candidates}
        result = candidate_qualification(candidates, rows, set(), {("s", "g")}, set(), ledger_complete=True)
        self.assertEqual(result[0]["source_status"], "OVERLAP")
        self.assertEqual(result[1]["source_status"], "PASS")

    def test_participant_unknown_never_becomes_pass_and_candidates_not_replaced(self):
        candidates = ["a", "b", "c", "d"]
        rows = {u: {"video_source": "s", "origin_video_id": u, "fb_participant_id": u} for u in candidates}
        rows["c"]["fb_participant_id"] = ""
        result = candidate_qualification(candidates, rows, {"a"}, set(), set(), ledger_complete=False)
        self.assertEqual([r["alias"] for r in result], ["P1", "P2", "P3", "P4"])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["source_status"], "OVERLAP")
        self.assertEqual(result[2]["source_status"], "UNKNOWN")
        self.assertIn("PARTICIPANT_UNKNOWN", result[2]["reasons"])
        self.assertEqual(candidates, ["a", "b", "c", "d"])

    def test_handoff_projection_skips_question_options_and_event_values(self):
        text = '{"binding":["x","y"],"cohort":[{"key":{"source":"a","index":1},"question":"SECRET_Q","event_a":"SECRET_E","metadata":{"video_source":"s"}}]}'
        result = project_handoff(io.StringIO(text), "cohort")
        self.assertNotIn("SECRET_", json.dumps(result))
        self.assertEqual(result["cohort"][0]["key"]["source"], "a")


class NetworkWitnesses(unittest.TestCase):
    def test_exact_canonical_extensionless_object_is_not_rewritten(self):
        self.assertEqual(canonical_object("s3://invented-bucket/exact-opaque-key"),
                         ("invented-bucket", "exact-opaque-key"))
        with self.assertRaises(ContractError):
            canonical_object("s3://invented-bucket/prefix/")

    def test_five_slots_failure_no_refund_and_sdk_retry_region_resend_denied(self):
        log = MemoryJournal()
        slots = {"bucket": "https://example.invalid/b"}
        slots.update({"P%d" % i: "https://example.invalid/o%d" % i for i in range(1, 6)})
        gate = SendGate(log, slots)
        for name in ("bucket", "P1", "P2", "P3", "P4"):
            gate.reserve(name, "HEAD", slots[name])
        self.assertEqual(len(log.rows), 5)
        for name in ("P1", "P5"):
            with self.assertRaises(ContractError):
                gate.reserve(name, "HEAD", slots[name])
        self.assertEqual(len(log.rows), 5)

    def test_get_unknown_host_and_changed_key_denied_before_transport(self):
        log = MemoryJournal(); url = "https://example.invalid/object"
        gate = SendGate(log, {"P1": url})
        for method, target in (("GET", url), ("HEAD", "https://other.invalid/object"), ("HEAD", url + "?x=1")):
            with self.assertRaises(ContractError):
                gate.reserve("P1", method, target)
        self.assertEqual(log.rows, [])

    def test_same_object_alias_cannot_send_twice(self):
        log = MemoryJournal(); url = "https://example.invalid/same"
        gate = SendGate(log, {"P1": url, "P2": url})
        gate.reserve("P1", "HEAD", url)
        with self.assertRaises(ContractError):
            gate.reserve("P2", "HEAD", url)
        self.assertEqual(len(log.rows), 1)

    def test_sdk_transport_retry_or_preload_unknown_refused(self):
        client = SimpleNamespace()
        with self.assertRaisesRegex(ContractError, "SDK_LOW_LEVEL"):
            install_head_transport(client, None, {}, session_source='pool.urlopen(retries=True, preload_content=True)')

    def test_actual_send_requires_gate_and_never_consumes_response_body(self):
        calls, closed = [], []
        raw = SimpleNamespace(length_remaining=0, chunked=False, close=lambda: closed.append(1))
        response = SimpleNamespace(raw=raw, headers={}, status_code=200)
        events = SimpleNamespace(register_first=lambda name, fn, **kw: calls.append(fn))
        http = SimpleNamespace(send=lambda request: response)
        client = SimpleNamespace(meta=SimpleNamespace(events=events), _endpoint=SimpleNamespace(http_session=http))
        log = MemoryJournal(); url = "https://example.invalid/object"; context = {"slot": "P1"}
        install_head_transport(client, SendGate(log, {"P1": url}), context,
            session_source='pool.urlopen(retries=Retry(False), preload_content=False)')
        request = SimpleNamespace(method="HEAD", url=url)
        with self.assertRaises(ContractError):
            http.send(request)
        calls[0](request)
        self.assertEqual(http.send(request).raw.read(), b"")
        self.assertEqual(closed, [1])
        self.assertEqual(len(log.rows), 1)
        with self.assertRaises(ContractError):
            calls[0](request)  # hidden SDK/region retry cannot send again

    def test_unexpected_body_closed_without_read(self):
        closed = []; functions = []
        raw = SimpleNamespace(length_remaining=1, chunked=False, close=lambda: closed.append(True))
        response = SimpleNamespace(raw=raw, headers={}, status_code=400)
        http = SimpleNamespace(send=lambda request: response)
        client = SimpleNamespace(meta=SimpleNamespace(events=SimpleNamespace(
            register_first=lambda name, fn, **kwargs: functions.append(fn))), _endpoint=SimpleNamespace(http_session=http))
        url = "https://example.invalid/object"
        install_head_transport(client, SendGate(MemoryJournal(), {"P1": url}), {"slot": "P1"},
            session_source='pool.urlopen(retries=Retry(False), preload_content=False)')
        request = SimpleNamespace(method="HEAD", url=url); functions[0](request)
        with self.assertRaisesRegex(ContractError, "UNEXPECTED_HEAD_BODY"):
            http.send(request)
        self.assertEqual(closed, [True])

    def test_errors_never_echo_payload_and_canonical_uri_requires_exact_reference(self):
        self.assertNotIn("SECRET", json.dumps(safe_network_error(RuntimeError("SECRET"))))
        self.assertEqual(canonical_object("s3://invented-bucket/exact.mp4"), ("invented-bucket", "exact.mp4"))
        for value in ("https://invented.invalid/video.mp4", "s3://b/../x.mp4", "s3://b/x.mp4?other"):
            with self.assertRaises(ContractError):
                canonical_object(value)


if __name__ == "__main__":
    raise SystemExit("USE_029_COORDINATOR")
