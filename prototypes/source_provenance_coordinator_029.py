"""029 exact-input provenance/metadata coordinator; no private path defaults.

Modes: offline new suite; inspect authorized schemas/source AST; join/cache;
SDK-only HEAD with explicit per-round authorization. No model/media-body path.
"""
import ast
from dataclasses import asdict
import inspect
import json
import os
from pathlib import Path
import sys
import time
import unittest
from urllib.parse import quote

PUBLIC = Path(__file__).absolute().parent
sys.path.insert(0, str(PUBLIC))
from temporal_evidence_adapter_025 import ContractError, container_binding, SKIP_NONFINITE_028
from temporal_pilot_prepare_026 import InputBudget, MIB, checked_path
from temporal_pilot_coordinator_027 import Journal, enforce_output_limits, output, safe_error
from source_provenance_029 import (
    observe_schema, project_handoff, inspect_producer, independent_group_join,
    candidate_qualification, canonical_object, SendGate, install_head_transport,
    bound_group_rule, project_proven_identity,
)


def scope(root, entries, *, sdk=False, network=False):
    allowed = {os.path.normcase(str(Path(p).absolute())) for p in entries}
    library = Path(sys.base_prefix) / "Lib"
    sdk_library = Path(sys.executable).parent.parent / "Lib" / "site-packages"
    shared = {os.path.normcase(str(Path.home() / ".aws" / n)) for n in ("config", "credentials")}
    def audit(event, args):
        if event.startswith("socket.") and not network:
            raise ContractError("029_NETWORK_NOT_AUTHORIZED_IN_CPU_MODE")
        if event.startswith(("subprocess.", "ctypes.")) or event in (
                "os.system", "os.remove", "os.rename", "os.rmdir", "os.putenv"):
            raise ContractError("029_SIDE_EFFECT_DENIED")
        if event == "import" and str(args[0]).split(".")[0] in (
                "torch", "transformers", "numpy", "av", "cv2", "PIL"):
            raise ContractError("029_MODEL_IMPORT_DENIED")
        if event in ("os.listdir", "os.scandir"):
            p = Path(os.fsdecode(args[0])).absolute()
            if not (p in (root, PUBLIC, library) or library in p.parents
                    or sdk and (p == sdk_library or sdk_library in p.parents)):
                raise ContractError("029_DIRECTORY_SCAN_DENIED")
        if event == "open":
            if isinstance(args[0], int):
                return
            p = Path(os.fsdecode(args[0])).absolute()
            mode, flags = args[1:]
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (
                isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if writing and p.parent != root:
                raise ContractError("029_WRITE_SCOPE_DENIED")
            if not writing and not (p.parent == root or PUBLIC in p.parents or library in p.parents
                    or os.path.normcase(str(p)) in allowed
                    or sdk and (sdk_library in p.parents or os.path.normcase(str(p)) in shared)):
                raise ContractError("029_READ_SCOPE_DENIED")
    sys.addaudithook(audit)
    if sdk:
        sys.path.insert(0, str(sdk_library))


def phase(journal, errors, name, alias, fn):
    journal.event("029_PHASE_STARTED", phase=name, alias=alias)
    try:
        value = fn()
        journal.event("029_PHASE_FINISHED", phase=name, alias=alias)
        return value
    except Exception as error:
        record = safe_error(name, alias, error)
        errors.append(record)
        journal.event("029_PHASE_ERROR", **record)
        return None


def consume(budget, alias, role, fn):
    with budget.text(alias, role) as stream:
        return fn(stream)


def inspect_inputs(config, root, journal):
    journal.reserve_runtime("029_inspect", 90, 90, 1)
    journal.reserve_runtime("029_auxiliary", 30, 30, 1)
    if set(config) != {"handoff", "old", "sources"}:
        raise ContractError("029_CONFIG_SCHEMA_HOLD")
    if len(config["handoff"]) > 16 or len(config["old"]) > 8 or len(config["sources"]) > 6:
        raise ContractError("029_ROLE_COUNT_LIMIT")
    budget, errors = InputBudget(durable=journal), []
    handoffs, old, sources = {}, [], []
    for role, path in config["handoff"].items():
        if role not in ("keys", "cohort", "plan", "receipts"):
            raise ContractError("029_HANDOFF_ROLE_HOLD")
        alias = "handoff_" + role
        budget.register(alias, path, MIB)
        value = phase(journal, errors, "handoff", alias, lambda a=alias, r=role:
                      consume(budget, a, "content", lambda stream: project_handoff(stream, r)))
        if value is not None:
            handoffs[role] = value
    for index, entry in enumerate(config["old"]):
        alias = "old_%d" % index
        budget.register(alias, entry["path"], MIB, 2)
        value = phase(journal, errors, "scalar_free_schema", alias,
                      lambda a=alias: consume(budget, a, "schema", observe_schema))
        if value is not None:
            old.append(dict(alias=entry["alias"], file=entry["path"], schema=value,
                            receipt=asdict(budget.receipts[-1]),
                            writer_status="UNKNOWN_NOT_BOUND", projection_status="NOT_AUTHORIZED_WITHOUT_PROOF"))
    for index, entry in enumerate(config["sources"]):
        alias = "producer_%d" % index
        budget.register(alias, entry["path"], MIB)
        value = phase(journal, errors, "source_ast_only", alias,
                      lambda a=alias: consume(budget, a, "content", lambda stream: inspect_producer(stream.read())))
        if value is not None:
            sources.append(dict(alias=entry["alias"], file=entry["path"], proof=value,
                                receipt=asdict(budget.receipts[-1])))
    # Only scalar-free observed shape; positions never assign tuple semantics.
    group_shapes = []
    for item in old:
        paths = [n for n in item["schema"]["nodes"] if n["path"] and n["path"][-1] == "source_group"]
        group_shapes.append(dict(alias=item["alias"], source_group_nodes=len(paths),
                                 schema_scalar_decodes=item["schema"]["diagnostic"]["decoded_values"]))
    output(root, "inspection-private.json", dict(handoffs=handoffs, old=old, sources=sources,
           errors=errors, receipts=[asdict(r) for r in budget.receipts]))
    summary = dict(old_schemas_completed=len(old), sources_completed=len(sources),
                   handoffs_completed=len(handoffs), group_shapes=group_shapes,
                   direct_group_constructions=sum(len(s["proof"]["source_group_semantics"]) for s in sources),
                   explicit_output_calls=sum(len(s["proof"]["writers"]) for s in sources),
                   exact_metadata_references=sum(len(s["proof"]["exact_references"]) for s in sources),
                   errors=errors, reserved_bytes=budget.reserved, actual_bytes=budget.actual)
    output(root, "inspection-summary.json", summary)
    return summary


def join_inputs(config, root, journal):
    journal.reserve_runtime("029_join", 90, 90, 1)
    with open(root / "inspection-private.json", encoding="utf-8") as source:
        prior = json.load(source)
    keys = prior["handoffs"]["keys"]
    binding = tuple(keys["binding"][str(i)] for i in range(2))
    if binding != container_binding(SKIP_NONFINITE_028):
        raise ContractError("029_FROZEN_PROFILE_BINDING_HOLD")
    records = keys["keys"]
    if set(records) != {str(i) for i in range(4)}:
        raise ContractError("029_EXACT_FROZEN_FOUR_REQUIRED")
    candidates = [records[str(i)]["source"] for i in range(4)]
    # No writer/version linkage from mere AST presence/adjacency. Only a directly
    # proven output schema can receive its one second projection; require the
    # declared self-source digest AND unchanged schema-pass artifact bytes.
    ledger = [dict(alias=a, artifact_found=any(o["alias"] == a for o in prior["old"]),
                   writer_bound=False, uid="UNKNOWN", origin="UNKNOWN", participant="UNKNOWN",
                   known_derivatives="UNKNOWN") for a in ("013", "014", "R1", "R2", "R3", "R4", "R5", "R6")]
    budget, errors = InputBudget(durable=journal), []
    old_uids, old_groups, people = set(), set(), set()
    for index, artifact in enumerate(prior["old"]):
        possible = [s for s in prior["sources"] if any(
            p["filename"] == Path(artifact["file"]).name for p in s["proof"]["output_proofs"])]
        if len(possible) != 1:
            continue
        writer = possible[0]
        provisional = dict(items=("video_source", "origin_video_id"))
        alias = "old_%d" % index
        budget.register(alias, artifact["file"], MIB, 2)
        value = phase(journal, errors, "proven_identity_projection", alias,
            lambda a=alias: consume(budget, a, "identity",
                                  lambda stream: project_proven_identity(stream, provisional)))
        if value is None:
            continue
        rule = bound_group_rule(writer["proof"], producer_digest=writer["receipt"]["digest"],
            binding_digest=value.get("producer_sha256"), output_name=Path(artifact["file"]).name)
        receipt = budget.receipts[-1]
        if not rule or receipt.digest != artifact["receipt"]["digest"]:
            errors.append(dict(phase="writer_binding", alias=alias, reason="029_ARTIFACT_WRITER_BINDING_HOLD",
                               exception_kind="ContractError", errno=None))
            continue
        group = value.get("source_group", {})
        if set(group) != {0, 1} or any(type(v) is not str or not v for v in group.values()):
            continue
        old_groups.add((group[0], group[1]))
        for record in ledger:
            if record["alias"] == artifact["alias"]:
                record.update(writer_bound=True, origin="PROVEN_RECORDED_GROUP")
        output(root, alias + "-proven-identity.json", dict(value=value, rule=rule, receipt=asdict(receipt)))
    budget.register("official_manifest", config["manifest"], 8 * MIB)
    joined = phase(journal, errors, "independent_official_join", "official_manifest",
        lambda: consume(budget, "official_manifest", "content",
                        lambda stream: independent_group_join(stream, candidates, old_uids, old_groups)))
    if joined is None:
        output(root, "join-failed.json", dict(errors=errors))
        return dict(status="OFFICIAL_JOIN_HOLD", errors=errors)
    if joined["duplicates"]:
        raise ContractError("029_DUPLICATE_OFFICIAL_UID_HOLD")
    rows = joined["rows"]
    group_alias_uids = {uid for match in joined["group_matches"] for uid in match["uids"]}
    people = {rows[u].get("fb_participant_id") for u in group_alias_uids
              if rows[u].get("fb_participant_id")}
    qualification = candidate_qualification(candidates, rows, old_uids, old_groups, people,
                                             ledger_complete=False)
    targets, target_errors = [], []
    for index, uid in enumerate(candidates):
        row = rows.get(uid, {})
        uri = row.get("canonical_s3_location", "")
        try:
            if not uri or row.get("s3_path") and row["s3_path"] != uri:
                raise ContractError("029_EXACT_CANONICAL_URI_UNKNOWN_OR_CONFLICT")
            bucket, key = canonical_object(uri)
            targets.append(dict(alias="P%d" % (index + 1), bucket=bucket, key=key, uri=uri))
        except Exception as error:
            target_errors.append(safe_error("canonical_reference", "P%d" % (index + 1), error))
    output(root, "source-ledger-private.json", dict(ledger=ledger, scope="WRITER_BINDING_UNKNOWN"))
    output(root, "official-join-private.json", dict(binding=binding, joined=joined, qualification=qualification))
    output(root, "head-targets-private.json", dict(binding=binding, targets=targets))
    summary = dict(qualification=qualification, official=joined["summary"], old_ledger=ledger,
                   canonical_targets=len(targets), target_errors=target_errors,
                   media_stats=0, frozen_text_n=4, frozen_plan_slots=16, candidates_replaced=0,
                   real_pilot_readiness="HOLD", errors=errors)
    output(root, "join-summary.json", summary)
    return summary


def sdk_heads(root, journal):
    """Existing isolated SDK only; no credential/provider/network fallback."""
    journal.reserve_runtime("029_head", 120, 120, 1)
    import boto3
    import botocore.session
    from botocore.config import Config
    from botocore.credentials import SharedCredentialProvider, CredentialResolver, Credentials
    import ego4d.cli.universities as universities
    from botocore.httpsession import URLLib3Session
    import textwrap
    if any(os.environ.get(k) for k in ("AWS_SHARED_CREDENTIALS_FILE", "AWS_CONFIG_FILE")):
        raise ContractError("029_CREDENTIAL_PATH_OVERRIDE_HOLD")
    session = botocore.session.Session(profile="ego4d")
    config = session.full_config.get("profiles", {}).get("ego4d", {})
    forbidden = ("role_arn", "credential_source", "credential_process", "source_profile",
                 "web_identity_token_file", "sso_session", "sso_start_url")
    if any(config.get(k) for k in forbidden):
        raise ContractError("029_NONSTATIC_PROFILE_HOLD")
    provider = SharedCredentialProvider(session.get_config_variable("credentials_file"), profile_name="ego4d")
    session.register_component("credential_provider", CredentialResolver([provider]))
    credentials = session.get_credentials()
    if type(credentials) is not Credentials or credentials.method != "shared-credentials-file":
        raise ContractError("029_STATIC_SHARED_PROVIDER_HOLD")
    # The official installed SDK is the bucket/region authority, not a guessed
    # URI prefix or a profile region standing in for bucket-region evidence.
    dictionaries = {k: v for k, v in vars(universities).items() if type(v) is dict}
    bucket_map = dictionaries.get("UNIV_TO_BUCKET", {})
    region_map = dictionaries.get("UNIV_TO_REGION", {})
    output(root, "sdk-schema-private.json", dict(dictionary_names=sorted(dictionaries),
           dictionary_value_types={k: sorted({type(x).__name__ for x in v.values()}) for k, v in dictionaries.items()},
           provider="shared-credentials-file", profile="ego4d"))
    if not bucket_map or not all(type(x) is str for x in bucket_map.values()):
        raise ContractError("029_OFFICIAL_SDK_BUCKET_SCHEMA_HOLD")
    trusted_buckets = set(bucket_map.values())
    bucket_regions = {bucket: region_map[name] for name, bucket in bucket_map.items()
                      if type(region_map.get(name)) is str}
    with open(root / "canonical-targets-confirmed-private.json", encoding="utf-8") as source:
        targets = json.load(source)["targets"]
    if any(t["bucket"] not in trusted_buckets for t in targets):
        raise ContractError("029_CANONICAL_BUCKET_NOT_IN_OFFICIAL_SDK")
    allowed_regions = set(session.get_available_regions("s3", partition_name="aws"))
    transport_source = textwrap.dedent(inspect.getsource(URLLib3Session.send))
    contexts, result = {}, []
    def client_for(region, slots, discovery=False):
        if region not in allowed_regions:
            raise ContractError("029_TRUSTED_COMMERCIAL_REGION_HOLD")
        endpoint = "https://s3.amazonaws.com" if discovery else "https://s3." + region + ".amazonaws.com"
        client = session.create_client("s3", region_name=region, endpoint_url=endpoint,
            config=Config(signature_version="s3v4", connect_timeout=10, read_timeout=10,
                          retries={"total_max_attempts": 1, "mode": "standard"},
                          proxies={}, max_pool_connections=1, s3={"addressing_style": "path"}))
        if type(client._endpoint.http_session) is not URLLib3Session:
            raise ContractError("029_SDK_HTTP_TRANSPORT_NOT_PROVEN")
        context = {}
        install_head_transport(client, SendGate(journal, slots), context, session_source=transport_source)
        return client, context
    bucket_used, completed_objects = False, {}
    for target in targets:
        object_key = (target["bucket"], target["key"])
        if object_key in completed_objects:
            result.append(dict(completed_objects[object_key], alias=target["alias"], shared_object=True))
            continue
        region = bucket_regions.get(target["bucket"])
        if region not in allowed_regions and not bucket_used:
            bucket_used = True
            bucket_url = "https://s3.amazonaws.com/" + target["bucket"]
            probe, probe_context = client_for("us-east-1", {"bucket": bucket_url}, discovery=True)
            probe_context["slot"] = "bucket"
            try:
                probe.head_bucket(Bucket=target["bucket"])
            except Exception:
                pass  # No resend; only trusted first-response region evidence.
            finally:
                probe.close()
            observed = probe_context.get("observed_region")
            if observed in allowed_regions:
                bucket_regions[target["bucket"]] = observed
                region = observed
        if region not in allowed_regions:
            result.append(dict(alias=target["alias"], status="HOLD", reason="TRUSTED_REGION_UNKNOWN"))
            continue
        url = "https://s3." + region + ".amazonaws.com/" + target["bucket"] + "/" + quote(target["key"], safe="/~")
        client, context = client_for(region, {target["alias"]: url})
        context["slot"] = target["alias"]
        try:
            response = client.head_object(Bucket=target["bucket"], Key=target["key"])
            record = dict(alias=target["alias"], status=response["ResponseMetadata"]["HTTPStatusCode"],
                          ContentLength=response.get("ContentLength"), ETag=response.get("ETag"),
                          VersionId=response.get("VersionId"),
                          LastModified=str(response.get("LastModified", "")), region=region)
        except Exception as error:
            status = getattr(error, "response", {}).get("ResponseMetadata", {}).get("HTTPStatusCode")
            record = dict(alias=target["alias"], status=status, reason="HEAD_FAILED_NO_RETRY",
                          exception_kind=type(error).__name__)
        finally:
            client.close()
        result.append(record)
        completed_objects[object_key] = record
    output(root, "head-results-private.json", dict(results=result))
    sent = [r for r in journal.snapshot() if r["event"] == "HTTPS_RESERVED"]
    safe = dict(results=[{k: v for k, v in r.items() if k in ("alias", "status", "reason", "exception_kind")}
                        | ({"ceil_MiB": (r["ContentLength"] + MIB - 1) // MIB}
                           if type(r.get("ContentLength")) is int else {}) for r in result],
                https_attempts=len(sent), head_bucket=sum(r["slot"] == "bucket" for r in sent),
                head_object=sum(r["slot"] != "bucket" for r in sent), body_bytes_read=0)
    output(root, "head-summary.json", safe)
    return safe


def sdk_mapping_inspection(root, journal):
    """Offline installed official SDK AST, never execute a downloader."""
    import importlib.util
    journal.reserve_runtime("029_sdk_mapping", 60, 60, 1)
    budget, errors, modules = InputBudget(durable=journal), [], []
    for index, name in enumerate(("ego4d.cli.download", "ego4d.cli.cli", "ego4d.cli.universities")):
        try:
            spec = importlib.util.find_spec(name)
            if spec is None or spec.origin is None or not spec.origin.endswith(".py"):
                raise ContractError("029_OFFICIAL_SDK_MODULE_ENTRY_UNKNOWN")
            alias = "sdk_source_%d" % index
            budget.register(alias, spec.origin, MIB)
            with budget.text(alias) as stream:
                text = stream.read()
                tree = ast.parse(text)
                relevant = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and any(
                            isinstance(x, ast.Constant) and x.value in ("canonical_s3_location", "s3_path")
                            or isinstance(x, ast.Attribute) and x.attr in ("canonical_s3_location", "s3_path")
                            for x in ast.walk(node)):
                        relevant.append(dict(name=node.name, source=ast.get_source_segment(text, node)))
                imports = [dict(module=n.module, names=[a.name for a in n.names], level=n.level)
                           for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
            modules.append(dict(module=name, functions=relevant, imports=imports,
                                receipt=asdict(budget.receipts[-1])))
        except Exception as error:
            errors.append(safe_error("sdk_mapping_inspection", "sdk_%d" % index, error))
    output(root, "sdk-mapping-private.json", dict(modules=modules, errors=errors))
    summary = dict(modules=[dict(module=m["module"], matching_functions=[f["name"] for f in m["functions"]])
                            for m in modules], errors=errors, network_attempts=0,
                   reserved_bytes=budget.reserved, actual_bytes=budget.actual)
    output(root, "sdk-mapping-summary.json", summary)
    return summary


def confirm_saved_canonical_targets(root, journal):
    """Exact official URI reuse after removing an invented suffix assumption.

    No SDK key construction and no original input reopen. Frozen keys and official
    rows are read solely from029's complete, already-bound private projections.
    """
    journal.reserve_runtime("029_canonical_confirmation", 60, 60, 1)
    with open(root / "inspection-private.json", encoding="utf-8") as source:
        frozen = json.load(source)["handoffs"]["keys"]["keys"]
    with open(root / "official-join-private.json", encoding="utf-8") as source:
        joined = json.load(source)["joined"]
    if joined["duplicates"]:
        raise ContractError("029_DUPLICATE_OFFICIAL_UID_HOLD")
    rows = joined["rows"]
    targets, errors = [], []
    for index in range(4):
        uid = frozen[str(index)]["source"]
        try:
            row = rows[uid]
            uri = row["canonical_s3_location"]
            if row.get("s3_path") and row["s3_path"] != uri:
                raise ContractError("029_CANONICAL_REFERENCE_CONFLICT")
            bucket, key = canonical_object(uri)
            targets.append(dict(alias="P%d" % (index + 1), uri=uri, bucket=bucket, key=key))
        except Exception as error:
            errors.append(safe_error("canonical_confirmation", "P%d" % (index + 1), error))
    output(root, "canonical-targets-confirmed-private.json", dict(targets=targets,
           evidence="OFFICIAL_MANIFEST_CANONICAL_URI_UNCHANGED", errors=errors))
    return dict(confirmed_targets=len(targets), distinct_objects=len({(t["bucket"], t["key"]) for t in targets}),
                suffix_appended=False, original_inputs_reopened=0, errors=errors)


def finalize_metadata(root, journal):
    """Actual self-output integrity/accounting, charged to auxiliary envelope.

    No research-input reopen, new fixture suite, model or network action.
    """
    with open(root / "inspection-private.json", encoding="utf-8") as source:
        handoffs = json.load(source)["handoffs"]
    keys = handoffs["keys"]["keys"]
    cohort = handoffs["cohort"]["cohort"]
    calls = handoffs["plan"]["plan"]["calls"]
    bindings = [tuple(handoffs[role]["binding"][str(i)] for i in range(2))
                for role in ("keys", "cohort", "plan", "receipts")]
    if not all(b == container_binding(SKIP_NONFINITE_028) for b in bindings):
        raise ContractError("029_HANDOFF_PROFILE_BINDING_MISMATCH")
    if set(keys) != {str(i) for i in range(4)} or set(calls) != {str(i) for i in range(16)}:
        raise ContractError("029_FROZEN_REFERENCE_SHAPE_MISMATCH")
    for i in range(4):
        if keys[str(i)] != cohort[str(i)]["key"]:
            raise ContractError("029_COHORT_KEY_MISMATCH")
        rotation = "ABCD"[i:] + "ABCD"[:i]
        for j, arm in enumerate(rotation):
            if calls[str(i * 4 + j)] != dict(key=keys[str(i)], arm=arm):
                raise ContractError("029_FROZEN_CALL_REFERENCE_MISMATCH")
    with open(root / "head-summary.json", encoding="utf-8") as source:
        heads = json.load(source)
    rows = journal.snapshot()
    reads = [r for r in rows if r["event"] == "INPUT_RESERVED"]
    finished = [r for r in rows if r["event"] == "INPUT_FINISHED"]
    summary = dict(status="SOURCE_ROUTE_STOP_MISSING_PROVENANCE", frozen_text_n=4,
        frozen_plan_slots=16, fixed_reference_and_rotation="PASS", profile_binding="PASS",
        head_summary=heads, head_bucket_response_status="NOT_PERSISTED_UNKNOWN",
        input_reservations=len(reads), input_finishes=len(finished),
        completed_inputs=sum(r["complete"] for r in finished),
        reserved_bytes=sum(r["reserved"] for r in reads), actual_bytes=sum(r["actual"] for r in finished),
        runtime_reserved_seconds=sum(r["seconds"] for r in rows if r["event"] == "RUNTIME_RESERVED"),
        suites=sum(r["event"] == "RUNTIME_RESERVED" and r["kind"] == "029_suite" for r in rows),
        actual_https_send_reservations=sum(r["event"] == "HTTPS_RESERVED" for r in rows),
        original_annotation_opens=0, media_stats=0, real_gold_values=0,
        missing=["013_014_EXACT_NON_GOLD_ROSTER_AND_WRITER_VERSION",
                 "R1_R6_ALIAS_TO_UID_OR_ORIGIN_REGISTRY_WITH_ARTIFACT_WRITER_BINDING",
                 "P3_TRUSTED_PARTICIPANT_EVIDENCE", "P2_P4_TRUSTED_BUCKET_REGION",
                 "CURRENT_RESEARCH_RIGHTS_AND_EXACT_LOCAL_MEDIA_REFERENCE"])
    journal.event("029_FINALIZED", status=summary["status"])
    output(root, "final-summary.json", summary)
    files = list(root.iterdir())
    summary["own_output_files"] = len(files)
    summary["own_output_bytes"] = sum(p.stat().st_size for p in files)
    return summary


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--mode", choices=("verify", "inspect", "join", "sdk", "confirm", "head", "final"), required=True)
    parser.add_argument("--authorized-cpu", action="store_true")
    parser.add_argument("--authorized-head", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).absolute()
    if root.name != "integration_029":
        raise ContractError("029_FIXED_ROOT_REQUIRED")
    if args.mode != "verify" and not args.authorized_cpu:
        raise ContractError("029_EXPLICIT_CPU_SCOPE_REQUIRED")
    if args.mode == "head" and not args.authorized_head:
        raise ContractError("029_EXPLICIT_HEAD_SCOPE_REQUIRED")
    if args.create:
        checked_path(root.parent, directory=True)
        os.mkdir(root)
    checked_path(root, directory=True)
    config = json.load(sys.stdin) if args.mode in ("inspect", "join") else {}
    entries = [e["path"] for e in config.get("old", []) + config.get("sources", [])]
    entries.extend(config.get("handoff", {}).values())
    if "manifest" in config:
        entries.append(config["manifest"])
    scope(root, entries, sdk=args.mode in ("sdk", "head"), network=args.mode == "head")
    journal = Journal(root, "029")
    enforce_output_limits(root, journal)
    try:
        if args.mode == "verify":
            launch = journal.reserve_runtime("029_suite", 60, 120, 2)
            import test_source_provenance_029 as tests
            before = time.monotonic()
            tests.configure(journal)
            result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
            summary = dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                           skipped=len(result.skipped), elapsed=time.monotonic() - before)
            output(root, "verification-%d.json" % (launch + 1), summary)
            print(json.dumps(summary))
            return 0 if result.wasSuccessful() else 1
        summary = (inspect_inputs(config, root, journal) if args.mode == "inspect" else
                   join_inputs(config, root, journal) if args.mode == "join" else
                   confirm_saved_canonical_targets(root, journal) if args.mode == "confirm" else
                   finalize_metadata(root, journal) if args.mode == "final" else
                   sdk_mapping_inspection(root, journal) if args.mode == "sdk" else sdk_heads(root, journal))
        print(json.dumps(summary))
        return 0
    except Exception as error:
        record = safe_error(args.mode, "029", error)
        journal.event("029_COORDINATOR_ERROR", **record)
        print(json.dumps(record))
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps(safe_error("029_entry", "029", error)))
        sys.exit(2)
