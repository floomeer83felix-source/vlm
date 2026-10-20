"""029 metadata-only primitives. No default private entries or live network.

Schema keys/expressions/digests and exact object identities are PRIVATE outputs.
No tuple interpretation without both producer semantics and artifact binding.
"""
import ast
import csv
from dataclasses import dataclass
import hashlib
import io
import json
import re
from urllib.parse import urlsplit, unquote

from temporal_evidence_adapter_025 import (
    ContractError, _Projector, SKIP_NONFINITE_028, container_binding,
)
from temporal_pilot_prepare_026 import GROUP_FIELDS


PROTECTED = frozenset(("question", "questions", "options", "event_a", "event_b",
                       "gold", "correct_answer_label", "canary", "prediction",
                       "predictions", "relevant_timestamps", "benchmark_dataset"))
IDENTITY = frozenset(GROUP_FIELDS) | frozenset(("source_group", "participant",
    "producer_sha256", "writer_sha256", "script_sha256", "producer_version",
    "artifact_sha256", "media_path", "video_path", "canonical_s3_location"))


class SchemaProjector(_Projector):
    """Scalar-free complete traversal. Dynamic keys remain private."""
    def __init__(self, stream):
        self.nodes = []
        super().__init__(stream, lambda p: False, profile=SKIP_NONFINITE_028)
    def _value(self, path, depth):
        self._space()
        char = self._peek()
        kind = ("object" if char == "{" else "array" if char == "[" else
                "string" if char == '"' else "scalar")
        self.nodes.append(dict(path=list(path), kind=kind))
        return super()._value(path, depth)


def observe_schema(stream):
    parser = SchemaProjector(stream)
    parser.read()
    return dict(nodes=parser.nodes, diagnostic=parser.diagnostic)


def project_handoff(stream, role):
    """Exact028 wrappers only; no QA/options/events, even in nongold artifacts."""
    def allow(p):
        if not p or any(type(x) is str and x in PROTECTED for x in p):
            return False
        if p[0] == "binding":
            return len(p) == 2 and type(p[1]) is int
        if role == "keys":
            return len(p) == 3 and p[0] == "keys" and p[-1] in ("source", "index")
        if role == "cohort":
            return (len(p) == 4 and p[0] == "cohort" and p[2] == "key" and p[3] in ("source", "index")
                    or len(p) == 4 and p[0] == "cohort" and p[2] == "metadata" and p[3] in IDENTITY
                    or len(p) == 4 and p[0] == "cohort" and p[2] == "limits" and type(p[3]) is int)
        if role == "receipts":
            return (len(p) == 3 and p[0] == "receipts" and p[2] in ("alias", "digest", "complete", "byte_count")
                    or len(p) == 4 and p[0] == "receipts" and p[2] in ("before", "after") and type(p[3]) is int)
        if role == "plan":
            return (len(p) == 5 and p[:2] == ("plan", "calls") and p[3] == "key"
                    and p[4] in ("source", "index")
                    or len(p) == 4 and p[:2] == ("plan", "calls") and p[3] == "arm")
        return False
    return _Projector(stream, allow, profile=SKIP_NONFINITE_028).read()


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return dotted(node.value) + "." + node.attr
    if isinstance(node, ast.Call):
        return dotted(node.func) + "()"
    return "EXPRESSION"


def _source_field(node):
    return (node.slice.value if isinstance(node, ast.Subscript)
            and isinstance(node.slice, ast.Constant)
            and node.slice.value in ("video_source", "origin_video_id") else None)


def inspect_producer(text):
    """Targeted AST descriptions; never eval/import a private source.

    A semantic tuple is only evidence when directly constructed in an output
    dict/assignment. Mere reads of prior['source_group'] do not prove schema.
    """
    tree = ast.parse(text)
    semantics, writers, references, output_proofs = [], [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "source_group":
                    if isinstance(value, (ast.Tuple, ast.List)):
                        fields = [_source_field(x) for x in value.elts]
                        if fields == ["video_source", "origin_video_id"]:
                            semantics.append(dict(line=node.lineno, field="source_group",
                                                  items=fields, evidence="DIRECT_CONSTRUCTION"))
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
                                               and t.id == "source_group" for t in node.targets):
            if isinstance(node.value, (ast.Tuple, ast.List)):
                fields = [_source_field(x) for x in node.value.elts]
                if fields == ["video_source", "origin_video_id"]:
                    semantics.append(dict(line=node.lineno, field="source_group",
                                          items=fields, evidence="DIRECT_CONSTRUCTION"))
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name.split(".")[-1] in ("record", "write_text", "write_bytes", "dump", "persist"):
                filenames = [a.value for a in node.args if isinstance(a, ast.Constant)
                             and isinstance(a.value, str) and a.value.endswith(".json")]
                writers.append(dict(line=node.lineno, function=name, filenames=filenames))
                if name.split(".")[-1] == "record" and len(node.args) >= 2 and filenames:
                    payload = node.args[1]
                    if isinstance(payload, ast.Dict):
                        fields = {k.value: v for k, v in zip(payload.keys, payload.values)
                                  if isinstance(k, ast.Constant) and type(k.value) is str}
                        group = fields.get("source_group")
                        fingerprint = fields.get("producer_sha256")
                        expected = ast.parse("hashlib.sha256(Path(__file__).read_bytes()).hexdigest()", mode="eval").body
                        if (isinstance(group, (ast.Tuple, ast.List))
                                and [_source_field(x) for x in group.elts] == ["video_source", "origin_video_id"]
                                and fingerprint is not None
                                and ast.dump(fingerprint) == ast.dump(expected)):
                            output_proofs.append(dict(filename=filenames[0],
                                items=["video_source", "origin_video_id"], binding_field="producer_sha256",
                                evidence="DIRECT_OUTPUT_SELF_SOURCE_DIGEST"))
            # Exact paths only: no directory probing and no filename guessing.
            if name.split(".")[-1] in ("Path", "open"):
                for arg in node.args[:1]:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        value = arg.value
                        if re.match(r"^[A-Za-z]:[\\/]", value) and value.lower().endswith((".json", ".csv")):
                            references.append(dict(line=node.lineno, path=value,
                                                   status="LITERAL_REFERENCE_ONLY_NOT_AUTHORITY"))
    return dict(source_group_semantics=semantics, writers=writers,
                exact_references=references, output_proofs=output_proofs)


def bound_group_rule(producer, *, producer_digest, binding_digest, output_name):
    """No adjacency/filename/similar-duration fallback for writer binding."""
    if not binding_digest or producer_digest != binding_digest:
        return None
    if not producer["source_group_semantics"]:
        return None
    if not any(output_name == proof["filename"] for proof in producer["output_proofs"]):
        return None
    return dict(field="source_group", items=("video_source", "origin_video_id"),
                producer_digest=producer_digest, output_name=output_name)


def project_proven_identity(stream, rule):
    if not rule or rule.get("items") != ("video_source", "origin_video_id"):
        raise ContractError("UNPROVEN_SOURCE_GROUP_SCHEMA")
    def allow(p):
        if any(type(x) is str and x in PROTECTED for x in p):
            return False
        return (p == ("producer_sha256",)
                or len(p) == 2 and p[0] == "source_group" and p[1] in (0, 1))
    return _Projector(stream, allow, profile=SKIP_NONFINITE_028).read()


def independent_group_join(stream, candidate_uids, old_uids=(), old_groups=()):
    rows = csv.DictReader(stream)
    headers = tuple(rows.fieldnames or ())
    if len(set(headers)) != len(headers) or "video_uid" not in headers:
        raise ContractError("OFFICIAL_MANIFEST_SCHEMA_HOLD")
    requested = set(candidate_uids) | set(old_uids)
    groups = set(tuple(g) for g in old_groups)
    retained, group_matches, duplicates, count = {}, {}, set(), 0
    allowed = set(GROUP_FIELDS) | {"canonical_s3_location", "s3_path"}
    for row in rows:
        count += 1
        if None in row or any(value is None for value in row.values()):
            raise ContractError("OFFICIAL_MANIFEST_ROW_HOLD")
        uid = row["video_uid"]
        group = (row.get("video_source", ""), row.get("origin_video_id", ""))
        if uid in requested or group in groups:
            if uid in retained:
                duplicates.add(uid)
            retained[uid] = {k: v for k, v in row.items() if k in allowed}
            if group in groups:
                group_matches.setdefault(group, []).append(uid)
    return dict(rows=retained, group_matches=[dict(group=g, uids=v, unique=len(v) == 1)
                                             for g, v in group_matches.items()],
                summary=dict(row_count=count, headers=headers, requested_uids=len(requested),
                             matched_uids=len(requested & retained.keys()),
                             missing_uids=len(requested - retained.keys()),
                             duplicate_uids=len(duplicates), requested_groups=len(groups),
                             matched_groups=len(group_matches)), duplicates=sorted(duplicates))


def candidate_qualification(candidates, official_rows, old_uids, old_groups,
                            old_participants, *, ledger_complete=False):
    if len(candidates) != 4:
        raise ContractError("EXACT_FROZEN_FOUR_REQUIRED")
    result = []
    for index, uid in enumerate(candidates):
        row = official_rows.get(uid, {})
        group = (row.get("video_source", ""), row.get("origin_video_id", ""))
        person = row.get("fb_participant_id")
        reasons = []
        if uid in old_uids:
            reasons.append("OLD_UID_OVERLAP")
        if group in old_groups:
            reasons.append("OLD_ORIGIN_OVERLAP")
        if person and person in old_participants:
            reasons.append("OLD_PARTICIPANT_OVERLAP")
        if any(row.get(k) in old_uids for k in ("parent_video_uid", "source_video_uid", "parent_uid")):
            reasons.append("KNOWN_DERIVATIVE_OVERLAP")
        overlaps = bool(reasons)
        if not person:
            reasons.append("PARTICIPANT_UNKNOWN")
        if not row:
            reasons.append("OFFICIAL_JOIN_UNKNOWN")
        if not ledger_complete:
            reasons.append("OLD_LEDGER_INCOMPLETE")
        result.append(dict(alias="P%d" % (index + 1),
                           source_status="OVERLAP" if overlaps else "UNKNOWN" if reasons else "PASS",
                           reasons=reasons, current_rights="UNKNOWN",
                           physical_independence="UNKNOWN"))
    return result


class SendGate:
    """Durable actual-before-send cap. One failed/uncertain slot never refunds."""
    def __init__(self, journal, slots):
        self.journal, self.slots = journal, slots
    def reserve(self, slot, method, url):
        expected = self.slots.get(slot)
        if method != "HEAD" or expected is None or url != expected:
            raise ContractError("HEAD_REQUEST_NOT_WHITELISTED")
        parsed = urlsplit(url)
        if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.query
                or parsed.fragment or parsed.port not in (None, 443)):
            raise ContractError("HEAD_URL_NOT_CANONICAL")
        with self.journal.transaction() as rows:
            used = [r for r in rows if r["event"] == "HTTPS_RESERVED"]
            if any(r["slot"] == slot or r["url"] == url for r in used):
                raise ContractError("HEAD_SLOT_CONSUMED_NO_RESEND")
            if (len(used) >= 5 or slot == "bucket" and any(r["slot"] == "bucket" for r in used)
                    or slot != "bucket" and sum(r["slot"] != "bucket" for r in used) >= 4):
                raise ContractError("HTTPS_HARD_LIMIT")
            self.journal.append(rows, "HTTPS_RESERVED", slot=slot, url=url, method="HEAD")


def canonical_object(uri):
    parsed = urlsplit(uri)
    if parsed.scheme != "s3" or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
        raise ContractError("CANONICAL_S3_REFERENCE_HOLD")
    key = unquote(parsed.path.lstrip("/"))
    # S3 object keys are opaque. The official canonical URI is authoritative;
    # never invent/append a filename suffix or derive another key from a UID.
    if (not key or key.endswith("/") or any(p in (".", "..") for p in key.split("/"))
            or any(ord(c) < 32 for c in key)):
        raise ContractError("CANONICAL_KEY_HOLD")
    return parsed.netloc, key


def safe_network_error(error, status=None):
    return dict(status=status, exception_kind=type(error).__name__,
                reason="HEAD_FAILED_NO_RETRY")


def install_head_transport(client, gate, context, *, session_source):
    """Before-send + exact transport validation, zero response-body consumption.

    Fail closed if the installed SDK transport cannot be statically shown to
    disable urllib3 retries and preload. SDK region resends hit the same slot.
    Headers are bounded in retained size, NOT a certified wire-byte limit.
    """
    tree = ast.parse(session_source)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and dotted(n.func).endswith("urlopen")]
    proven = False
    for call in calls:
        keys = {k.arg: k.value for k in call.keywords}
        retry = keys.get("retries")
        if (isinstance(retry, ast.Call) and dotted(retry.func).endswith("Retry")
                and len(retry.args) == 1 and isinstance(retry.args[0], ast.Constant)
                and retry.args[0].value is False
                and isinstance(keys.get("preload_content"), ast.Constant)
                and keys["preload_content"].value is False):
            proven = True
    if not proven:
        raise ContractError("SDK_LOW_LEVEL_RETRY_OR_BODY_GATE_UNPROVEN")
    pending = []
    def before_send(request, **kwargs):
        method = request.method.decode("ascii") if isinstance(request.method, bytes) else request.method
        gate.reserve(context["slot"], method, request.url)
        pending.append((method, request.url))
    client.meta.events.register_first("before-send.s3", before_send, unique_id="029-head-only")
    original = client._endpoint.http_session.send
    class EmptyBody:
        def stream(self, *args, **kwargs):
            return iter(())
        def read(self, *args, **kwargs):
            return b""
        def close(self):
            pass
    def send(request):
        method = request.method.decode("ascii") if isinstance(request.method, bytes) else request.method
        if not pending or pending.pop(0) != (method, request.url):
            raise ContractError("SDK_SEND_WITHOUT_PERSISTENT_GATE")
        response = original(request)
        raw = response.raw
        try:
            size = sum(len(str(k).encode()) + len(str(v).encode()) for k, v in response.headers.items())
            if size > 65536:
                raise ContractError("HEAD_HEADER_RETENTION_LIMIT")
            context["observed_region"] = response.headers.get("x-amz-bucket-region")
            context["observed_status"] = response.status_code
            if getattr(raw, "length_remaining", None) != 0 or getattr(raw, "chunked", False):
                raise ContractError("UNEXPECTED_HEAD_BODY_HOLD")
        finally:
            raw.close()  # No read/drain. Never consume unexpected response data.
        response.raw = EmptyBody()
        return response
    client._endpoint.http_session.send = send
