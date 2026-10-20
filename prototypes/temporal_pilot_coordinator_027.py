"""027 auditable CPU coordinator. No real paths, model or network defaults.

CLI config is explicit JSON on stdin, not an authorization by itself. --private
requires the current user's exact027 scope and an exclusive new output root.
Tests precede research reads. Journals fail closed; pending reservations retire
the input, even after a crash. OS ACL gold denial is NOT provided by this code.
"""
import ast
import builtins
from contextlib import contextmanager
from dataclasses import asdict
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import textwrap
import time
import unittest

# -I -S -B: only this explicit public directory is added, never site-packages.
PUBLIC = Path(__file__).absolute().parent
sys.path.insert(0, str(PUBLIC))
from temporal_evidence_adapter_025 import ContractError, Projection, build_plan, project_nongold
from temporal_pilot_prepare_026 import (
    InputBudget, MIB, canonical_digest, checked_path, choose_cohort,
    flatten_strings, historical_projection, index_annotation, read_manifest,
)


class Journal:
    """OS-locked append/fsync ledger, shared across phases and fresh processes.

    Every record has a sequence and hash chain. Truncation/corruption aborts;
    no replacement, refund, renamed aliases or reset on restart is permitted.
    Reads of this self-owned ledger are not research-input reopens.
    """
    def __init__(self, root):
        self.root, _ = checked_path(root, directory=True)
        self.path = self.root / "027-ledger.jsonl"
        self.lock = self.root / "027-ledger.lock"
        try:
            with open(self.lock, "xb") as target:
                target.write(b"0")
                target.flush()
                os.fsync(target.fileno())
        except FileExistsError:
            pass
        try:
            with open(self.path, "xb"):
                pass
        except FileExistsError:
            pass

    @contextmanager
    def transaction(self):
        checked_path(self.lock)
        checked_path(self.path)
        with open(self.lock, "r+b", buffering=0) as lock:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            try:
                if self.path.stat().st_size > 4 * MIB:
                    raise ContractError("LEDGER_SIZE_HOLD")
                rows, previous = [], ""
                with open(self.path, "rb") as source:
                    for line in source:
                        if not line.endswith(b"\n"):
                            raise ContractError("LEDGER_TRUNCATED_HOLD")
                        row = json.loads(line)
                        digest = row.pop("digest")
                        if (row.get("seq") != len(rows) or row.get("previous") != previous
                                or digest != canonical_digest(row)):
                            raise ContractError("LEDGER_CHAIN_HOLD")
                        row["digest"] = digest
                        rows.append(row)
                        previous = digest
                yield rows
            finally:
                lock.seek(0)
                if os.name == "nt":
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(lock, fcntl.LOCK_UN)

    def append(self, rows, event, **values):
        row = dict(seq=len(rows), previous=rows[-1]["digest"] if rows else "",
                   event=event, **values)
        row["digest"] = canonical_digest(row)
        data = (json.dumps(row, ensure_ascii=True, allow_nan=False) + "\n").encode()
        if self.path.stat().st_size + len(data) > 4 * MIB:
            raise ContractError("LEDGER_SIZE_HOLD")
        with open(self.path, "ab", buffering=0) as target:
            target.write(data)
            os.fsync(target.fileno())
        rows.append(row)

    def event(self, event, **values):
        with self.transaction() as rows:
            self.append(rows, event, **values)

    def snapshot(self):
        with self.transaction() as rows:
            return list(rows)

    def reserve_input(self, alias, path, role, info, cap, maximum):
        token = os.path.normcase(str(path))
        physical = [info.st_dev, info.st_ino]
        with self.transaction() as rows:
            prior = [r for r in rows if r["event"] == "INPUT_RESERVED"
                     and (r["path"] == token or r["physical"] == physical)]
            if any(r["alias"] != alias or r["role"] == role for r in prior):
                raise ContractError("INPUT_ALIAS_OR_ROLE_REUSE")
            completed = {(r["path"], r["role"]): r for r in rows
                         if r["event"] == "INPUT_FINISHED"}
            if any(not completed.get((r["path"], r["role"]), {}).get("complete") for r in prior):
                raise ContractError("INPUT_FAILED_OR_PENDING_NO_RETRY")
            used = sum(r["reserved"] for r in rows if r["event"] == "INPUT_RESERVED")
            if (len(prior) >= maximum or info.st_size > cap or info.st_size < 0
                    or used + info.st_size > 48 * MIB):
                raise ContractError("DURABLE_INPUT_LIMIT")
            self.append(rows, "INPUT_RESERVED", alias=alias, path=token, role=role,
                        physical=physical, reserved=info.st_size)

    def finish_input(self, alias, path, role, actual, complete, reason):
        self.event("INPUT_FINISHED", alias=alias, path=os.path.normcase(str(path)),
                   role=role, actual=actual, complete=complete, reason=reason)

    def reserve_runtime(self, kind, seconds, limit, count_limit):
        with self.transaction() as rows:
            prior = [r for r in rows if r["event"] == "RUNTIME_RESERVED" and r["kind"] == kind]
            all_cpu = sum(r["seconds"] for r in rows if r["event"] == "RUNTIME_RESERVED")
            if (len(prior) >= count_limit or sum(r["seconds"] for r in prior) + seconds > limit
                    or all_cpu + seconds > 600):
                raise ContractError("DURABLE_RUNTIME_LIMIT")
            self.append(rows, "RUNTIME_RESERVED", kind=kind, seconds=seconds)
            return len(prior)


def safe_error(phase, alias, error):
    reason = str(error) if isinstance(error, ContractError) else "UNEXPECTED_EXCEPTION"
    if not re.fullmatch(r"[A-Z0-9_]{1,100}", reason):
        reason = "CONTRACT_HOLD"
    return dict(phase=phase, alias=alias, reason=reason,
                exception_kind=type(error).__name__, errno=getattr(error, "errno", None))


def output(root, name, value):
    """Fixed self-owned leaf, exclusive; reserve conservative storage globally.

    128 reservations and 32MiB include ledger/locks/fixtures. Only coordinator
    helpers write real artifacts. Suite uses a checked fixed output inventory.
    """
    if Path(name).name != name:
        raise ContractError("SIMPLE_OUTPUT_NAME_REQUIRED")
    data = json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False).encode()
    with open(Path(root) / name, "xb") as target:
        target.write(data)
        target.flush()
        os.fsync(target.fileno())


def enforce_output_limits(root, journal):
    """All writes are flat, named, pre-reserved, and capped per file.

    ≤128 leaves: ledger≤4MiB and every other leaf≤128KiB imply <20MiB,
    conservatively below32MiB including failed/partially written outputs.
    The fixed ledger/OS-lock leaves consume two initial file reservations.
    """
    import builtins
    original = builtins.open
    local = threading.local()
    class Limited:
        def __init__(self, file, cap):
            self.file, self.cap = file, cap
        def __getattr__(self, name):
            return getattr(self.file, name)
        def write(self, data):
            size = len(data.encode("utf-8")) if isinstance(data, str) else len(data)
            if self.file.tell() + size > self.cap:
                raise ContractError("OUTPUT_BYTE_LIMIT")
            return self.file.write(data)
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return self.file.__exit__(*args)
    def bounded(file, mode="r", *args, **kwargs):
        writing = any(c in mode for c in "wax+")
        if not writing or isinstance(file, int):
            return original(file, mode, *args, **kwargs)
        path = Path(file).absolute()
        if path.parent != Path(root):
            raise ContractError("FLAT_OUTPUT_SCOPE_REQUIRED")
        if path not in (journal.path, journal.lock) and not getattr(local, "active", False):
            local.active = True
            try:
                with journal.transaction() as rows:
                    reserved = {r["name"] for r in rows if r["event"] == "OUTPUT_RESERVED"}
                    if path.name not in reserved:
                        if len(reserved) + 2 >= 128:
                            raise ContractError("OUTPUT_FILE_LIMIT")
                        journal.append(rows, "OUTPUT_RESERVED", name=path.name)
            finally:
                local.active = False
        target = original(file, mode, *args, **kwargs)
        return Limited(target, 4 * MIB if path == journal.path else 128 * 1024)
    builtins.open = bounded


def runner_map(text):
    tree = ast.parse(text)
    functions, literals = [], {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in ("inputs", "worker", "guard", "record", "persist", "need", "deny", "phase"):
                defined = {arg.arg for arg in node.args.args}
                defined.update(n.id for n in ast.walk(node) if isinstance(n, ast.Name)
                               and isinstance(n.ctx, (ast.Store, ast.Param)))
                loaded = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)
                          and isinstance(n.ctx, ast.Load)}
                functions.append(dict(name=node.name, args=[a.arg for a in node.args.args],
                                      external_names=sorted(loaded - defined),
                                      source=ast.get_source_segment(text, node)))
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [x.id for x in targets if isinstance(x, ast.Name)]
            if any(n.lower() in ("excluded_uids", "old_uids", "previous_video_uids",
                                 "used_video_uids", "excluded_video_uids") for n in names):
                try:
                    value = ast.literal_eval(node.value)
                    if type(value) in (list, tuple, set) and all(type(x) is str for x in value):
                        literals[names[0]] = list(value)
                except (ValueError, TypeError):
                    pass
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            if any(part in name.lower() for part in
                   ("processor", "generate", "decode", "frame", "chat_template", "pretrained")):
                calls.append(dict(function=name, args=[ast.unparse(a) for a in node.args],
                                  keywords={k.arg or "**": ast.unparse(k.value) for k in node.keywords}))
    return dict(functions=functions, calls=calls, exclusion_literals=literals)


def prepare(config, root, journal):
    """Independent phases retain success despite another phase's safe HOLD."""
    budget = InputBudget(durable=journal)
    errors, result, saved = [], {}, {}

    def phase(name, alias, fn):
        journal.event("PHASE_STARTED", phase=name, alias=alias)
        try:
            value = fn()
            saved[name] = value
            journal.event("PHASE_FINISHED", phase=name, status="PASS")
            return value
        except Exception as error:
            record = safe_error(name, alias, error)
            journal.event("PHASE_ERROR", **record)
            errors.append(record)
            return None

    def consume(alias, fn, role="content"):
        with budget.text(alias, role) as stream:
            return fn(stream)

    annotation = config["annotation"]
    budget.register("annotation", annotation, 4 * MIB, max_opens=3)
    index = phase("index", "annotation", lambda: consume("annotation", index_annotation, "index"))
    projection = None
    if index:
        result["schema"] = dict(sources=len(index.sources), questions=len(index.batch),
                                question_fields=index.question_field_names,
                                metadata_fields=index.metadata_field_names)
        projection = phase("screen", "annotation", lambda: consume(
            "annotation", lambda s: project_nongold(s, index.batch), "screen"))

    old_values, maps = [], []
    old = config.get("old", [])
    if len(old) > 8 or len(config.get("handoff", [])) > 8 or len(config.get("runners", [])) > 6:
        raise ContractError("ENTRY_CATEGORY_LIMIT")
    for number, path in enumerate(old):
        alias = "old_%d" % number
        budget.register(alias, path, MIB)
        value = phase(alias, alias, lambda a=alias: consume(a, historical_projection))
        if value is not None:
            old_values.append(value)
    for number, path in enumerate(config.get("handoff", [])):
        alias = "handoff_%d" % number
        budget.register(alias, path, MIB)
        value = phase(alias, alias, lambda a=alias: consume(a, historical_projection))
        if value is not None:
            old_values.append(value)
    for number, path in enumerate(config.get("runners", [])):
        alias = "runner_%d" % number
        budget.register(alias, path, MIB)
        value = phase(alias, alias, lambda a=alias: consume(a, lambda s: runner_map(s.read())))
        if value is not None:
            maps.append(value)
            old_values.append(value["exclusion_literals"])

    # Only explicit projected UID/group values may identify old sources.
    universe = set(index.sources) if index else set()
    old_uids = set(flatten_strings(old_values)) & universe
    result["old_mapping"] = dict(recovered_in_annotation=len(old_uids),
                                 old_records_completed=len(old_values) - len(maps),
                                 missing_categories=config.get("missing_old_categories", []),
                                 complete=False)
    manifest = None
    budget.register("manifest", config["manifest"], 8 * MIB)
    manifest_result = phase("manifest", "manifest", lambda: consume(
        "manifest", lambda s: read_manifest(s, universe | old_uids)))
    if manifest_result is not None:
        manifest, info, duplicates = manifest_result
        result["manifest"] = info
        if duplicates:
            manifest = None
            result["manifest_status"] = "DUPLICATE_UID_HOLD"
    if projection is not None:
        # Metadata is the known annotation join; official fields corroborate,
        # missing official rows remain UNKNOWN rather than erasing screen.
        source_rows = {s.source: dict(s.metadata) for s in projection.sources}
        for uid, row in (manifest or {}).items():
            merged = source_rows.setdefault(uid, {})
            for name, value in row.items():
                if value != "":
                    merged[name] = value
        selected, counts, excluded = choose_cohort(projection, source_rows, old_uids)
        result["screen_counts"] = counts
        result["exclusions"] = dict(known_old_sources=len(old_uids),
                                     excluded_questions=len(excluded),
                                     complete=False)
        # Persist keys BEFORE options. Failure never selects replacement.
        output(root, "frozen-keys.json", [asdict(row["key"]) for row in selected])
        output(root, "cohort-private.json", [dict(row, key=asdict(row["key"])) for row in selected])
        result["frozen_candidates"] = len(selected)
        if selected:
            batch = tuple(row["key"] for row in selected)
            inference = phase("inference", "annotation", lambda: consume(
                "annotation", lambda s: project_nongold(s, batch, "inference"), "inference"))
            if inference is not None:
                output(root, "nongold-input.json", asdict(inference))
                output(root, "plan-private.json", asdict(build_plan(inference)))
                result["option_questions"] = len(inference.questions)
                result["options_retained"] = sum(len(q.options) for q in inference.questions)
        costs = []
        for number, row in enumerate(selected):
            metadata = row["metadata"]
            costs.append(dict(alias="P%d" % (number + 1),
                              declared_bytes={k: v for k, v in metadata.items() if "size" in k},
                              version={k: v for k, v in metadata.items() if "version" in k or k == "release_1"},
                              exact_media_reference="UNKNOWN", current_rights="UNKNOWN"))
        result["candidate_costs"] = costs
    output(root, "backend-map-private.json", maps)
    # Static adapter takes a resolved nested helper, never mixed annotations.
    # Factory injection remains an explicit unresolved backend responsibility.
    bridge = ('"""Static only; no backend import or runnable model entry."""\n'
              'def prompt_inputs(frozen_input, resolved_inputs, index, frame_ids):\n'
              '    if len(frozen_input["questions"][index]["options"]) != 5:\n'
              '        raise ValueError("FIVE_OPTIONS_REQUIRED")\n'
              '    return resolved_inputs(index, frame_ids)\n')
    compile(bridge, "integration_worker_027.py", "exec")
    with open(Path(root) / "integration_worker_027.py", "xb") as target:
        target.write(bridge.encode())
    result.update(errors=errors, diagnostics=budget.diagnostics,
                  receipts=[asdict(r) for r in budget.receipts],
                  reserved_bytes=budget.reserved, actual_bytes=budget.actual,
                  input_opens=budget.opens, runners_mapped=len(maps),
                  executable_n=0, real_pilot_readiness="HOLD",
                  media_stats=0, gold_values=0, historical_026="PARTIAL_COUNTS_NOT_RECOVERABLE")
    output(root, "preparation-private.json", result)
    # Receipt contains aggregate counts/field NAMES only. No private values.
    safe = {k: v for k, v in result.items() if k not in ("receipts", "candidate_costs")}
    output(root, "sanitized-summary.json", safe)
    return safe


def audit_scope(root, entries):
    root = Path(root).absolute()
    allowed = {os.path.normcase(str(Path(p).absolute())) for p in entries}
    lib = Path(sys.base_prefix) / "Lib"
    def audit(event, args):
        if event.startswith(("socket.", "ctypes.")) or event in (
                "os.system", "os.remove", "os.rename", "os.rmdir", "os.putenv"):
            raise ContractError("SIDE_EFFECT_DENIED")
        if event == "import" and str(args[0]).split(".")[0] in (
                "torch", "transformers", "numpy", "PIL", "av", "cv2"):
            raise ContractError("MODEL_PACKAGE_DENIED")
        if event in ("os.listdir", "os.scandir"):
            p = Path(os.fsdecode(args[0])).absolute()
            if p != root and p != PUBLIC and lib != p and lib not in p.parents:
                raise ContractError("DIRECTORY_SCAN_DENIED")
        if event == "open":
            if isinstance(args[0], int):  # Popen owns PIPE descriptors only.
                return
            p = Path(os.fsdecode(args[0])).absolute()
            mode, flags = args[1:]
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (
                isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if writing and root not in p.parents:
                raise ContractError("OUTPUT_SCOPE_DENIED")
            if not writing and not (root in p.parents or PUBLIC in p.parents or lib in p.parents
                                     or os.path.normcase(str(p)) in allowed):
                raise ContractError("INPUT_SCOPE_DENIED")
            if "site-packages" in p.parts:
                raise ContractError("THIRD_PARTY_DENIED")
    sys.addaudithook(audit)


def review_handoff(root, journal):
    """Read only027's own exact outputs, never retired original inputs."""
    journal.reserve_runtime("handoff_review", 120, 120, 1)
    with open(Path(root) / "backend-map-private.json", encoding="utf-8") as stream:
        maps = json.load(stream)
    observations = []
    for number, mapping in enumerate(maps):
        functions = [{"name": fn["name"], "args": fn["args"],
                      "external_names": fn["external_names"]} for fn in mapping["functions"]]
        calls = [{"function": call["function"], "keywords": list(call["keywords"])}
                 for call in mapping["calls"]]
        observations.append(dict(alias="backend_%d" % number, functions=functions, calls=calls,
                                 closure_status="STATIC_ONLY_UNRESOLVED"))
    # No injected old closure is represented as safely bound to frozen nongold.
    stub = ('"""027 static handoff; backend closure not bound or authorized."""\n'
            'def make_backend(frozen_nongold, resolved_dependencies):\n'
            '    raise RuntimeError("BACKEND_BINDING_HOLD_NO_MODEL_ENTRY")\n')
    compile(stub, "backend_handoff_027.py", "exec")
    with open(Path(root) / "backend_handoff_027.py", "xb") as target:
        target.write(stub.encode())
    result = dict(backends=observations, earlier_callback_draft="RETIRED_NOT_EXECUTABLE_EVIDENCE",
                  backend_static_binding="PARTIAL_HOLD", real_screen="PARSER_HOLD_NOT_REOPENED",
                  recovered_013_014="UNKNOWN", candidate_n=None, executable_n=0,
                  missing=["COMPLETE_SCREEN", "OLD_UID_JOIN", "FROZEN_OPTIONS",
                           "EXACT_MEDIA_REFERENCE", "CURRENT_RIGHTS", "BACKEND_CLOSURE_BINDING",
                           "OS_GOLD_DENIAL", "ACTUAL_TOKEN_EQUALITY"])
    output(root, "handoff-review-private.json", result)
    rows = journal.snapshot()
    reservations = [r for r in rows if r["event"] == "INPUT_RESERVED"]
    finishes = [r for r in rows if r["event"] == "INPUT_FINISHED"]
    result["budget"] = dict(input_reservations=len(reservations),
                            reserved_bytes=sum(r["reserved"] for r in reservations),
                            actual_bytes_recorded=sum(r["actual"] for r in finishes),
                            completed_reads=sum(r["complete"] for r in finishes),
                            pending_reads=len(reservations) - len(finishes),
                            runtime_reserved_seconds=sum(r["seconds"] for r in rows
                                                         if r["event"] == "RUNTIME_RESERVED"),
                            worker_reservations=sum(r["event"] == "RUNTIME_RESERVED"
                                                    and r["kind"] == "fixture" for r in rows),
                            suites=sum(r["event"] == "RUNTIME_RESERVED"
                                       and r["kind"] == "suite" for r in rows))
    # Inventory only the new flat output directory, never research directories.
    inventory = list(Path(root).iterdir())
    if any(not p.is_file() for p in inventory) or len(inventory) + 1 > 128:
        raise ContractError("OWN_OUTPUT_INVENTORY_HOLD")
    result["output_inventory_before_final_summary"] = dict(
        files=len(inventory), bytes=sum(p.stat().st_size for p in inventory))
    output(root, "final-review-summary.json", result)
    return result


def static_backend_bridge(root, journal):
    """AST/compile only: bind original inputs closure to an explicit factory.

    Questions can originate only in caller's frozen nongold projection. The
    original helper body, prompt/processor parameters and token assertions are
    retained. No dependency is imported, loaded, resolved or invoked here.
    """
    journal.reserve_runtime("static_bridge", 60, 60, 1)
    # Conservative charge for bounded earlier/final source parsing and own-output
    # inspections outside supervised children; never a refund or fresh balance.
    journal.reserve_runtime("auxiliary_windows", 30, 30, 1)
    with open(Path(root) / "backend-map-private.json", encoding="utf-8") as stream:
        maps = json.load(stream)
    bindings = []
    for index, mapping in enumerate(maps):
        candidates = [f for f in mapping["functions"] if f["name"] == "inputs"]
        if len(candidates) != 1 or candidates[0]["args"] != ["i", "ids"]:
            raise ContractError("EXACT_INPUT_HELPER_REQUIRED")
        fn = candidates[0]
        tree = ast.parse(textwrap.dedent(fn["source"]))
        question_fields = {n.slice.value for n in ast.walk(tree)
                           if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                           and n.value.id == "q" and isinstance(n.slice, ast.Constant)}
        if question_fields != {"question", "options"}:
            raise ContractError("FROZEN_QUESTION_ADAPTATION_HOLD")
        deps = sorted(set(fn["external_names"]) - set(dir(builtins)) - {"questions"})
        params = ", ".join(deps)
        prefix = ('"""Static027 factory only; no imports or live entry."""\n'
                  'def make_inputs(frozen_nongold, *, ' + params + '):\n'
                  '    questions = []\n'
                  '    for row in frozen_nongold["questions"]:\n'
                  '        if len(row["options"]) != 5:\n'
                  '            raise ValueError("FIVE_FROZEN_OPTIONS_REQUIRED")\n'
                  '        questions.append({"question": row["question"], "options": tuple(row["options"])})\n')
        source = prefix + textwrap.indent(textwrap.dedent(fn["source"]), "    ") + '\n    return inputs\n'
        compile(source, "backend_factory_%d.py" % index, "exec")
        with open(Path(root) / ("backend_factory_%d.py" % index), "xb") as target:
            target.write(source.encode())
        bindings.append(dict(alias="backend_%d" % index, explicit_dependencies=deps,
                             original_signature=fn["args"], question_fields=sorted(question_fields),
                             body="ORIGINAL_UNEXECUTED", processor="qp", model_config="qc",
                             visual_inputs=["frames", "times", "fps", "duration", "prior"],
                             receipt="r", runtime="NOT_RUN"))
    journal.event("STATIC_BRIDGE_FINISHED", backend_count=len(bindings))
    rows = journal.snapshot()
    leaves = list(Path(root).iterdir())
    result = dict(bindings=bindings, status="STATIC_CLOSURE_MAP_COMPLETE_RUNTIME_HOLD",
                  runtime_reserved_seconds=sum(r["seconds"] for r in rows
                                               if r["event"] == "RUNTIME_RESERVED"),
                  own_files_before_summary=len(leaves),
                  own_bytes_before_summary=sum(p.stat().st_size for p in leaves))
    output(root, "static-bridge-summary.json", result)
    return result


def command(root, *args):
    return [sys.executable, "-I", "-S", "-B", str(Path(__file__).absolute()),
            "--root", str(root), *args]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--review", action="store_true")
    parser.add_argument("--static-bridge", action="store_true")
    parser.add_argument("--worker", choices=("ok", "sleep", "flood", "fail", "lock"))
    parser.add_argument("--fixture-score", action="store_true")
    parser.add_argument("--payload")
    args = parser.parse_args()
    root = Path(args.root).absolute()
    if args.create:
        if root.name != "integration_027":
            raise ContractError("FIXED_NEW_DIRECTORY_REQUIRED")
        checked_path(root.parent, directory=True)
        os.mkdir(root)
    checked_path(root, directory=True)
    config = json.load(sys.stdin) if args.private else {}
    entries = [config[k] for k in ("annotation", "manifest") if k in config]
    for key in ("old", "handoff", "runners"):
        entries.extend(config.get(key, []))
    audit_scope(root, entries)
    journal = Journal(root)
    enforce_output_limits(root, journal)
    if args.static_bridge:
        print(json.dumps(static_backend_bridge(root, journal)))
        return 0
    if args.review:
        print(json.dumps(review_handoff(root, journal)))
        return 0
    if args.worker:
        if args.worker == "sleep":
            time.sleep(2)
        elif args.worker == "flood":
            sys.stdout.write("x" * (128 * 1024))
        elif args.worker == "fail":
            return 3
        elif args.worker == "lock":
            from temporal_pilot_supervisor_026 import Supervisor, FixtureWorkerBudget
            Supervisor(root, "renamed", ("a",), FixtureWorkerBudget(root, 24),
                       cohort_digest=args.payload)
        return 0
    if args.fixture_score:
        from temporal_pilot_supervisor_026 import fixture_score_child
        fixture_score_child(json.loads(args.payload))
        return 0
    if args.verify:
        launch = journal.reserve_runtime("suite", 120, 240, 2)
        import test_temporal_pilot_repair_027 as tests
        tests.configure(root, launch, journal)
        before = time.monotonic()
        suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        summary = dict(launch=launch + 1, tests=result.testsRun, failures=len(result.failures),
                       errors=len(result.errors), skipped=len(result.skipped),
                       elapsed=time.monotonic() - before)
        journal.event("SUITE_FINISHED", **summary)
        output(root, "verification-%d.json" % (launch + 1), summary)
        print(json.dumps(summary))
        return 0 if result.wasSuccessful() else 1
    if args.private:
        # No automatic retry: failed or pending input reservations retire paths.
        journal.reserve_runtime("preparation", 120, 120, 1)
        try:
            summary = prepare(config, root, journal)
            print(json.dumps(summary, ensure_ascii=True))
            return 0
        except Exception as error:
            record = safe_error("coordinator", "none", error)
            journal.event("COORDINATOR_FAILED", **record)
            print(json.dumps(record))
            return 2
    raise ContractError("EXPLICIT_MODE_REQUIRED")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps(safe_error("entry", "none", error)))
        sys.exit(2)
