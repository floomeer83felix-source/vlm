"""030 fixed development pilot. No default private paths or import-time work.

Windows sharing/Job gates are OS gates, not a hostile-code sandbox. Every child
waits for a parent handshake before dependency imports or research work.
"""
import argparse
import ctypes
from ctypes import wintypes as W
from dataclasses import asdict
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import uuid

from temporal_evidence_adapter_025 import ContractError
from temporal_pilot_prepare_026 import checked_path

MIB = 1024 ** 2
GIB = 1024 ** 3


def require(condition, reason):
    if not condition:
        raise ContractError(reason)


def packed(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(packed(value)).hexdigest()


class Journal:
    """OS-locked, append/fsync hash chain; a consumed attempt never refunds."""
    def __init__(self, root, create=False):
        self.root = Path(root)
        if create:
            require(self.root.name == 'integration_030', 'ROOT_NAME')
            checked_path(self.root.parent, directory=True)
            self.root.mkdir()  # Existing root is terminal, never resume/relabel.
        checked_path(self.root, directory=True)
        self.lock = open(self.root / '030.lock', 'a+b')
        import msvcrt
        self.lock.seek(0)
        if self.lock.read(1) == b'':
            self.lock.write(b'0'); self.lock.flush(); os.fsync(self.lock.fileno())
        self.lock.seek(0)
        msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
        self.path = self.root / '030-ledger.jsonl'
        self.rows = []
        self.byte_length = 0
        if self.path.exists():
            raw = self.path.read_bytes()
            self.byte_length = len(raw)
            require(len(raw) <= 8 * MIB and raw.endswith(b'\n'), 'LEDGER_TRUNCATED')
            for line in raw.splitlines():
                row = json.loads(line)
                sig = row.pop('hash')
                require(row['seq'] == len(self.rows) and row['prev'] == (self.rows[-1]['hash'] if self.rows else '0' * 64)
                        and sig == digest(row), 'LEDGER_CHAIN')
                self.rows.append(dict(row, hash=sig))
        if create:
            self.add('RUN', run_id=uuid.uuid4().hex, epoch=time.time(), parent_cap=7200)
        require(self.rows and self.rows[0]['event'] == 'RUN', 'RUN_REQUIRED')
        self.check_time()

    def close(self):
        self.lock.close()

    def check_time(self):
        if self.rows:
            require(0 <= time.time() - self.rows[0]['epoch'] < 7200, 'PARENT_DEADLINE')

    def add(self, event, **fields):
        self.check_time()
        row = dict(seq=len(self.rows), prev=self.rows[-1]['hash'] if self.rows else '0' * 64,
                   event=event, **fields)
        row['hash'] = digest(row)
        raw = packed(row) + b'\n'
        require(self.byte_length + len(raw) <= 8 * MIB, 'LEDGER_BYTES')
        with open(self.path, 'ab') as target:
            target.write(raw); target.flush(); os.fsync(target.fileno())
        self.rows.append(row)
        self.byte_length += len(raw)

    def events(self, event):
        return [r for r in self.rows if r['event'] == event]

    def once(self, event, key, **fields):
        require(not any(r.get('key') == key for r in self.events(event)), 'CONSUMED_NO_RETRY')
        self.add(event, key=key, **fields)

    def reserve_time(self, stage, seconds, key):
        caps = dict(cpu=600, media=1200, acquisition=3600, gpu=900)
        require(stage in caps and seconds > 0 and
                sum(r['seconds'] for r in self.events('WINDOW') if r['stage'] == stage) + seconds <= caps[stage], 'STAGE_TIME')
        self.once('WINDOW', key, stage=stage, seconds=seconds)

    def reserve_output(self, name, size, category='metadata'):
        require(Path(name).name == name and name not in ('030.lock', '030-ledger.jsonl') and size >= 0, 'OUTPUT_NAME')
        used = self.events('OUTPUT')
        limits = dict(metadata=32 * MIB - 9 * MIB, media=16 * GIB, frames=4 * GIB)
        require(category in limits and len(used) + 3 <= 384 and
                sum(r['size'] for r in used) + size + 9 * MIB <= 24 * GIB and
                sum(r['size'] for r in used if r['category'] == category) + size <= limits[category], 'OUTPUT_CAP')
        require(not (self.root / name).exists(), 'OUTPUT_EXISTS')
        self.once('OUTPUT', name, size=size, category=category)

    def write(self, name, value):
        raw = packed(value)
        self.reserve_output(name, len(raw))
        with open(self.root / name, 'xb') as target:
            target.write(raw); target.flush(); os.fsync(target.fileno())

    def input(self, alias, path, category='handoff'):
        path, before = checked_path(path)
        caps = dict(handoff=12, source=7, config=4, gold=1)
        cap = 4 * MIB if category == 'gold' else MIB
        used = self.events('INPUT')
        require(category in caps and sum(r['category'] == category for r in used) < caps[category]
                and 0 < before.st_size <= cap and
                sum(r['size'] for r in used) + before.st_size <= 32 * MIB, 'INPUT_CAP')
        ident = [before.st_dev, before.st_ino]
        require(before.st_ino > 0 and not any(r['identity'] == ident or r['path'].casefold() == str(path).casefold() for r in used), 'INPUT_ALIAS')
        self.once('INPUT', alias, path=str(path), identity=ident, size=before.st_size, category=category)
        with open(path, 'rb') as source:
            opened = os.fstat(source.fileno())
            require(os.path.samestat(before, opened), 'INPUT_IDENTITY')
            raw = source.read(cap + 1)
            after_fd = os.fstat(source.fileno())
        after = path.stat()
        # Compare each API to itself: Windows path/fd ctime may differ.
        stable = lambda a, b: (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
        require(stable(before, after) and stable(opened, after_fd) and len(raw) == before.st_size, 'INPUT_CHANGED_OR_PARTIAL')
        self.add('INPUT_COMPLETE', alias=alias, size=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        return raw


def load(root, name):
    return json.loads((Path(root) / name).read_bytes())


class ExclusiveRead:
    def __init__(self, path):
        require(os.name == 'nt', 'WINDOWS_REQUIRED')
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, W.LPVOID, W.DWORD, W.DWORD, W.HANDLE]
        self.api.CreateFileW.restype = W.HANDLE
        self.api.CloseHandle.argtypes = [W.HANDLE]
        self.handle = self.api.CreateFileW(str(path), 0x80000000, 0, None, 3, 0x80, None)
        require(self.handle != ctypes.c_void_p(-1).value, 'EXCLUSIVE_HANDLE_FAILED')
        flags = W.DWORD()
        require(self.api.GetHandleInformation(W.HANDLE(self.handle), ctypes.byref(flags)) and not flags.value & 1, 'HANDLE_INHERITANCE')

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle); self.handle = None


class _Basic(ctypes.Structure):
    _fields_ = [('per_process_time', ctypes.c_int64), ('per_job_time', ctypes.c_int64),
                ('flags', W.DWORD), ('min_ws', ctypes.c_size_t), ('max_ws', ctypes.c_size_t),
                ('active_limit', W.DWORD), ('affinity', ctypes.c_size_t), ('priority', W.DWORD), ('scheduling', W.DWORD)]


class _IO(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint64) for n in ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]


class _Extended(ctypes.Structure):
    _fields_ = [('basic', _Basic), ('io', _IO), ('process_memory', ctypes.c_size_t),
                ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t), ('peak_job', ctypes.c_size_t)]


class _Accounting(ctypes.Structure):
    _fields_ = [('user', ctypes.c_int64), ('kernel', ctypes.c_int64), ('period_user', ctypes.c_int64),
                ('period_kernel', ctypes.c_int64), ('faults', W.DWORD), ('total', W.DWORD), ('active', W.DWORD), ('terminated', W.DWORD)]


class Job:
    def __init__(self, memory=24 * GIB):
        require(os.name == 'nt', 'WINDOWS_REQUIRED')
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [W.LPVOID, W.LPCWSTR]; self.api.CreateJobObjectW.restype = W.HANDLE
        for name, args in (('SetInformationJobObject', [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD]),
                           ('QueryInformationJobObject', [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD, W.LPVOID]),
                           ('AssignProcessToJobObject', [W.HANDLE, W.HANDLE]),
                           ('TerminateJobObject', [W.HANDLE, W.UINT]), ('CloseHandle', [W.HANDLE])):
            getattr(self.api, name).argtypes = args
        self.handle = self.api.CreateJobObjectW(None, None)
        require(bool(self.handle), 'JOB_CREATE')
        limits = _Extended()
        limits.basic.flags = 0x2000 | 0x100 | 0x200  # kill-on-close, process and Job memory.
        limits.process_memory = limits.job_memory = memory
        require(self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)), 'JOB_MEMORY_LIMIT')

    def assign(self, child):
        require(self.api.AssignProcessToJobObject(self.handle, W.HANDLE(int(child._handle))), 'JOB_ASSIGN')

    def active(self):
        record = _Accounting()
        require(self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(record), ctypes.sizeof(record), None), 'JOB_ACCOUNTING')
        return record.active

    def peak(self):
        record = _Extended()
        require(self.api.QueryInformationJobObject(self.handle, 9, ctypes.byref(record), ctypes.sizeof(record), None), 'JOB_PEAK')
        return record.peak_job

    def kill(self):
        self.api.TerminateJobObject(self.handle, 99)

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle); self.handle = None


def run_child(command, seconds, *, job_memory=24 * GIB, payload='', environment=None):
    """Child MUST read one stdin line before work. Job assignment precedes it."""
    job = Job(job_memory)
    child = None
    buffers = [bytearray(), bytearray()]
    overflow = threading.Event()
    threads = []
    start = time.monotonic()
    try:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 env=environment, creationflags=0x08000000, close_fds=True)
        job.assign(child)
        def capture(stream, buffer):
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                if len(buffer) + len(chunk) > 65536:
                    overflow.set()
                buffer.extend(chunk[:max(0, 65536 - len(buffer))])
        for stream, buffer in zip((child.stdout, child.stderr), buffers):
            thread = threading.Thread(target=capture, args=(stream, buffer), daemon=True)
            thread.start(); threads.append(thread)
        child.stdin.write((payload + '\n').encode()); child.stdin.flush(); child.stdin.close()
        while child.poll() is None:
            if time.monotonic() - start >= seconds or overflow.is_set():
                job.kill(); break
            time.sleep(.02)
        child.wait(timeout=3)
        # Includes descendants. Never search for or kill a peer process.
        if job.active():
            job.kill()
        deadline = time.monotonic() + 3
        while job.active() and time.monotonic() < deadline:
            time.sleep(.01)
        require(job.active() == 0, 'JOB_STILL_ACTIVE')
        for thread in threads:
            thread.join(1)
        require(not any(t.is_alive() for t in threads), 'PIPE_NOT_CLOSED')
        return dict(pid=child.pid, exit_code=child.returncode, job_active=0, peak_commit=job.peak(),
                    seconds=time.monotonic() - start, overflow=overflow.is_set(),
                    stdout=bytes(buffers[0]).decode(errors='replace'), stderr=bytes(buffers[1]).decode(errors='replace'))
    finally:
        if child is not None and child.poll() is None:
            job.kill(); child.kill(); child.wait(timeout=3)
        if child is not None:
            for stream in (child.stdin, child.stdout, child.stderr):
                if stream is not None and not stream.closed:
                    stream.close()
        job.close()


def python_command(interpreter, module, *arguments, site=None):
    # Explicit source insertion is needed because -I ignores PYTHONPATH.
    code = 'import sys;sys.path.insert(0,sys.argv.pop(1));'
    if site:
        code += 'sys.path.insert(0,sys.argv.pop(1));'
    code += 'import runpy;runpy.run_module(sys.argv.pop(1),run_name="__main__",alter_sys=True)'
    return [str(interpreter), '-I', '-S', '-B', '-c', code, str(Path(__file__).parent)] + ([str(site)] if site else []) + [module] + list(arguments)


def initialize(root, entries, annotation):
    journal = Journal(root, create=True)
    try:
        journal.reserve_time('cpu', 120, 'initialize')
        # Exact entries supplied by trusted local handoff, not discovered.
        for alias, record in entries.items():
            raw = journal.input(alias, record['path'], record['category'])
            if record['category'] == 'source':
                journal.reserve_output(alias + '.py', len(raw))
                with open(journal.root / (alias + '.py'), 'xb') as target:
                    target.write(raw); target.flush(); os.fsync(target.fileno())
            else:
                journal.write(alias + '.json', json.loads(raw))
        _, stat = checked_path(annotation)
        journal.write('annotation-reference.json', dict(path=str(annotation), identity=[stat.st_dev, stat.st_ino],
                                                        size=stat.st_size, mtime_ns=stat.st_mtime_ns))
        journal.add('INITIALIZED', handoffs=len(entries), annotation_body=0)
    finally:
        journal.close()


def probe(path):
    # This process never calls read(), even on an unexpected successful open.
    sys.stdin.readline()
    try:
        source = open(path, 'rb'); source.close()
    except OSError as error:
        print(json.dumps(dict(denied=getattr(error, 'winerror', None) == 32, winerror=getattr(error, 'winerror', None), body=0)))
        return
    print(json.dumps(dict(denied=False, body=0)))


def restored_plan(root):
    from temporal_evidence_adapter_025 import Projection, SourceRecord, QuestionRecord, QuestionKey, build_plan
    raw = load(root, 'nongold.json')['projection']
    projection = Projection(raw['view'], tuple(SourceRecord(s['source'], tuple(tuple(v) for v in s['metadata'])) for s in raw['sources']),
                            tuple(QuestionRecord(QuestionKey(**q['key']), q['task'], q['question'], tuple(q['options'])) for q in raw['questions']))
    return build_plan(projection)


def prepare(root):
    import ast
    import shutil
    journal = Journal(root)
    try:
        require_ready(journal)
        journal.once('PHASE', 'prepare')
        binding = ['SKIP_NONFINITE_028', 'PROJECTOR_028_V1']
        for name in ('keys', 'cohort', 'nongold', 'plan', 'receipts', 'official'):
            require(load(root, name + '.json')['binding'] == binding, 'PROFILE_BINDING')
        plan = restored_plan(root)
        require(len(plan.questions) == 4 and len(plan.calls) == 16 and packed(asdict(plan)) == packed(load(root, 'plan.json')['plan']), 'FROZEN_PLAN_CHANGED')
        # asdict retains tuples, JSON has lists: canonical bytes normalize both.
        keys = [asdict(q.key) for q in plan.questions]
        require(keys == load(root, 'keys.json')['keys'], 'FOUR_KEYS_CHANGED')
        cohort = load(root, 'cohort.json')['cohort']
        nongold = load(root, 'nongold.json')['projection']['questions']
        require([q['key'] for q in cohort] == keys and [q['key'] for q in nongold] == keys
                and all(len(q['options']) == 5 and all(type(v) is str and v.strip() for v in q['options']) for q in nongold), 'COHORT_OPTIONS')
        receipts = [r for r in load(root, 'receipts.json')['receipts'] if r['alias'] == 'annotation']
        require(len(receipts) == 3 and all(r['complete'] for r in receipts)
                and len({(r['byte_count'], r['digest'], tuple(r['before'])) for r in receipts}) == 1, '028_FULL_SNAPSHOT')
        reference = load(root, 'annotation-reference.json'); _, stat = checked_path(reference['path'])
        old = receipts[0]
        require([stat.st_dev, stat.st_ino] == old['before'][:2] == reference['identity']
                and stat.st_size == old['byte_count'] == reference['size']
                and stat.st_mtime_ns == old['before'][3] == reference['mtime_ns'], 'ANNOTATION_SNAPSHOT_STAT')
        journal.write('expected-snapshot.json', dict(binding=binding, size=old['byte_count'], sha256=old['digest']))
        targets = load(root, 'targets.json')['targets']; official = load(root, 'official.json')['joined']['rows']
        require([x['alias'] for x in targets] == ['P1', 'P2', 'P3', 'P4'], 'TARGET_ALIASES')
        sources = []
        for i, (question, item, target) in enumerate(zip(plan.questions, nongold, targets)):
            row = official[question.key.source]
            metadata = dict(plan.sources[i].metadata)
            require(row['video_uid'] == question.key.source and row['canonical_s3_location'] == target['uri']
                    and row['release_1'] in ('True', True, 'true') and row['canonical_is_validated'] in ('True', True, 'true'), 'OFFICIAL_FIXED_SOURCE')
            duration = float(row['canonical_mp4_duration_sec'])
            require(abs(duration - float(metadata['duration_in_seconds'])) <= .01
                    and item['question'] == cohort[i]['question'] == question.question
                    and question.decomposition.event_a == cohort[i]['event_a']
                    and question.decomposition.event_b == cohort[i]['event_b'], 'SOURCE_OR_EVENT_BINDING')
            sources.append(dict(alias=target['alias'], question=item['question'], options=item['options'],
                                event_a=cohort[i]['event_a'], event_b=cohort[i]['event_b'], declared_duration=duration))
        systems = []; model_roots = []
        for number in range(2):
            source = (Path(root) / ('runner_%d.py' % number)).read_text(encoding='utf-8')
            tree = ast.parse(source)
            system = [node.value.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == 'system' for t in node.targets)
                      and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)]
            require(len(system) == 1, 'ORIGINAL_SYSTEM_PROMPT')
            systems.append(system[0])
            constants = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and type(node.value) is str}
            roots = []
            for class_name in ('Qwen3VLForConditionalGeneration', 'SiglipModel'):
                calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                         and n.func.attr == 'from_pretrained' and isinstance(n.func.value, ast.Name) and n.func.value.id == class_name]
                require(len(calls) == 1 and isinstance(calls[0].args[0], ast.Constant), 'ORIGINAL_MODEL_REFERENCE')
                roots.append(calls[0].args[0].value)
            model_roots.append(roots)
        require(systems[0] == systems[1] and model_roots[0] == model_roots[1], 'BACKEND_CONFIG_CONFLICT')
        for number in range(2):
            factory = ast.parse((Path(root) / ('factory_%d.py' % number)).read_text(encoding='utf-8'))
            helper = [n for n in ast.walk(factory) if isinstance(n, ast.FunctionDef) and n.name == 'inputs']
            runner = ast.parse((Path(root) / ('runner_%d.py' % number)).read_text(encoding='utf-8'))
            original = [n for n in ast.walk(runner) if isinstance(n, ast.FunctionDef) and n.name == 'inputs']
            require(len(helper) == len(original) == 1 and ast.dump(helper[0]) == ast.dump(original[0]), 'EXACT_HELPER_AST')
        configs = []
        for name, model in zip(('qwen_config', 'siglip_config'), model_roots[0]):
            configs.append(json.loads(journal.input(name, Path(model) / 'config.json', 'config')))
        require(configs[0]['model_type'] == 'qwen3_vl' and configs[1]['model_type'] == 'siglip', 'MODEL_CONFIG')
        slots = [dict(slot=n, alias='P%d' % (n // 4 + 1), arm=call.arm) for n, call in enumerate(plan.calls)]
        journal.write('worker-input.json', dict(binding=binding, sources=sources, slots=slots, system=systems[0],
                      models=model_roots[0], qwen_config=configs[0], seed=19, max_new_tokens=64, factory='factory_1.py'))
        journal.add('FROZEN', n=4, options=20, slots=16, plan_hash=digest(asdict(plan)), worker_hash=digest(load(root, 'worker-input.json')))
        # Resolve the explicitly existing named conda runtime, no inventory/import.
        conda = Path(sys.executable).parent / 'Scripts' / 'conda.exe'
        require(conda.is_file(), 'EXISTING_CONDA_ENTRY_UNKNOWN')
        code = 'import sys,os,json;sys.stdin.readline();print(json.dumps(dict(python=sys.executable,path=os.environ.get("PATH",""))))'
        result = run_child([str(conda), 'run', '--no-capture-output', '-n', 'pytorch', 'python', '-I', '-S', '-B', '-c', code], 30)
        require(result['exit_code'] == 0 and not result['overflow'], 'EXISTING_RUNTIME_RESOLUTION')
        runtime = json.loads(result['stdout'].strip())
        runtime['site'] = str(Path(runtime['python']).parent / 'Lib' / 'site-packages')
        journal.write('runtime.json', runtime)
        journal.add('PREPARED', helper_ast_matches=2, original_annotation_body=0, resolution_pid=result['pid'])
    finally:
        journal.close()


def phase(root, name, stage, seconds, command, environment=None):
    journal = Journal(root)
    try:
        if name.startswith('suite-'):
            require(name in ('suite-1', 'suite-2') and not journal.events('RUN_STOPPED'), 'SUITE_CAP_OR_STOP')
        journal.reserve_time(stage, seconds, name)
    finally:
        journal.close()
    result = run_child(command, seconds, environment=environment)
    journal = Journal(root)
    try:
        journal.write(name + '-exit-private.json', result)
        journal.add('PHASE_EXIT', name=name, pid=result['pid'], code=result['exit_code'], job_active=result['job_active'], seconds=result['seconds'])
        if name.startswith('suite-'):
            import re
            match = re.search(r'Ran ([1-9][0-9]*) tests? in ', result['stderr'])
            passed = result['exit_code'] == 0 and not result['overflow'] and bool(match) and result['stderr'].strip().endswith('OK')
            journal.add('SUITE_RESULT', name=name, passed=passed, tests=int(match.group(1)) if match else 0)
    finally:
        journal.close()
    return result


def require_ready(journal):
    results = journal.events('SUITE_RESULT')
    require(not journal.events('RUN_STOPPED') and results and results[-1]['passed'] is True
            and 0 < results[-1]['tests'] and len(results) <= 2, 'NEW_SUITE_NOT_PASSED')


def score_allowed(rows):
    closes = [r for r in rows if r['event'] == 'QUEUE_CLOSED']
    exits = [r for r in rows if r['event'] == 'MODEL_EXIT']
    require(len(closes) == len(exits) == 1 and exits[0]['job_active'] == 0
            and exits[0]['pid'] == closes[0]['pid'] and closes[0]['model_exit_hash'] == exits[0]['hash']
            and len([r for r in rows if r['event'] == 'TERMINAL']) == 16
            and any(r['event'] == 'TERMINAL' and r['state'] in ('RETURNED', 'INVALID') for r in rows), 'GOLD_GATE_CLOSED')


class SnapshotRaw(io.RawIOBase):
    def __init__(self, file, expected):
        super().__init__(); self.file = file; self.expected = expected; self.count = 0
        self.sha = hashlib.sha256(); self.eof = False
    def readable(self):
        return True
    def readinto(self, buffer):
        require(self.count <= self.expected, 'SCORE_BYTE_CAP')
        chunk = self.file.read(min(len(buffer), self.expected - self.count + 1))
        self.count += len(chunk); require(self.count <= self.expected, 'SCORE_OVERSIZE')
        self.sha.update(chunk); self.eof = not chunk
        buffer[:len(chunk)] = chunk; return len(chunk)
    def close(self):
        if not self.closed:
            self.after = os.fstat(self.file.fileno()); self.file.close()
        super().close()


def score(root):
    from temporal_evidence_scorer_025 import OneShotScorer, FrozenLedger, TerminalAttempt, ChildExitReceipt
    journal = Journal(root)
    try:
        score_allowed(journal.rows)
        journal.once('SCORE_CONSUMED', 'original')
        snapshot = load(root, 'expected-snapshot.json'); reference = load(root, 'annotation-reference.json')
        plan = restored_plan(root); terminal = {int(r['key']): r for r in journal.events('TERMINAL')}
        ledger = FrozenLedger(tuple(TerminalAttempt(call, terminal[n]['state'], terminal[n].get('prediction')) for n, call in enumerate(plan.calls)), True)
        exit_row = journal.events('MODEL_EXIT')[0]
        receipt = ChildExitReceipt((str(exit_row['pid']),), (str(exit_row['pid']),), True)
        holders = []; diagnostic = {}
        def opener():
            path, before = checked_path(reference['path'])
            require([before.st_dev,before.st_ino] == reference['identity'] and before.st_size == snapshot['size']
                    and before.st_mtime_ns == reference['mtime_ns'] and before.st_size <= 4 * MIB, 'SCORE_FILE_CHANGED')
            require(not journal.events('INPUT') or not any(r['category'] == 'gold' for r in journal.events('INPUT')), 'GOLD_ALREADY_OPENED')
            used = journal.events('INPUT')
            require(sum(r['size'] for r in used) + before.st_size <= 32 * MIB, 'INPUT_CAP')
            journal.once('INPUT', 'gold', category='gold', path=str(path), identity=reference['identity'], size=before.st_size)
            file = open(path, 'rb'); opened = os.fstat(file.fileno())
            if not os.path.samestat(before, opened):
                file.close(); raise ContractError('SCORE_IDENTITY')
            raw = SnapshotRaw(file, before.st_size); holders.append((raw, before, opened, path))
            return io.TextIOWrapper(io.BufferedReader(raw), encoding='utf-8')
        report = OneShotScorer().score(opener, plan, ledger, receipt, profile=snapshot['binding'][0],
                                     expected_binding=tuple(snapshot['binding']), diagnostic=diagnostic)
        require(len(holders) == 1, 'SCORE_OPEN_FAILED')
        raw, before, opened, path = holders[0]; after = path.stat()
        stable = lambda a,b: (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns) == (b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns)
        require(diagnostic.get('complete') is True and raw.eof and raw.count == snapshot['size']
                and raw.sha.hexdigest() == snapshot['sha256'] and stable(before,after) and stable(opened,raw.after), 'FULL_SNAPSHOT_BINDING')
        journal.write('score-private.json', asdict(report))
        # Publish only after the complete stream/OS/snapshot gate.
        safe = asdict(report)
        for index, source in enumerate(safe['by_source']):
            source['source'] = 'P%d' % (index+1)
        journal.write('score-anonymous.json', safe)
        journal.add('SCORED', status=report.status, n=4, raw_bytes=raw.count, decoded_labels=4)
    except Exception as error:
        journal.write('score-hold.json', dict(status='UNKNOWN', reason=str(error) if isinstance(error,ContractError) else type(error).__name__))
    finally:
        journal.close()


def execute(root):
    import xml.etree.ElementTree as ET
    gate = Journal(root)
    try:
        require_ready(gate)
        require(gate.events('PREPARED') and not gate.events('MODEL_LAUNCH'), 'PREPARED_ONCE_REQUIRED')
    finally:
        gate.close()
    runtime = load(root, 'runtime.json'); own_python = sys.executable
    sdk_python = load(root, 'execution-config.json')['sdk_python']
    sdk_site = str(Path(sdk_python).parent.parent / 'Lib' / 'site-packages')
    reference = load(root, 'annotation-reference.json'); handle = None
    model_exit = None
    try:
        handle = ExclusiveRead(reference['path'])
        journal = Journal(root); journal.once('ORIGINAL_LOCK', 'annotation', body=0); journal.close()
        for n in range(2):
            probe_result = phase(root, 'refusal-%d' % n, 'cpu', 5,
                                 python_command(own_python,'development_pilot_030','probe',reference['path']))
            require(probe_result['exit_code'] == 0 and json.loads(probe_result['stdout'])['denied'] is True, 'ORIGINAL_REFUSAL_PROBE')
        metadata_result = phase(root,'metadata','cpu',60,
                                python_command(sdk_python,'development_media_030','metadata',str(root),site=sdk_site))
        # Per-source operations are independent; never substitute an object.
        for alias in ('P1','P2','P3','P4'):
            if (Path(root)/(alias+'-head.json')).exists() and load(root,alias+'-head.json').get('eligible'):
                phase(root,'get-'+alias,'acquisition',900,
                      python_command(sdk_python,'development_media_030','get',str(root),alias,site=sdk_site))
            if (Path(root)/(alias+'-media-binding.json')).exists():
                environment = dict(os.environ, PATH=runtime['path'])
                phase(root,'candidates-'+alias,'media',300,
                      python_command(runtime['python'],'development_media_030','candidates',str(root),alias,site=runtime['site']),environment)
        config = load(root,'worker-input.json')
        available = {a: (Path(root)/(a+'-candidates.json')).exists() for a in ('P1','P2','P3','P4')}
        journal = Journal(root)
        journal.write('queue.json',dict(slots=config['slots'],available=available,worker_hash=digest(config),run_id=journal.rows[0]['run_id']))
        for item in config['slots']:
            if not available[item['alias']]:
                journal.once('TERMINAL',str(item['slot']),alias=item['alias'],arm=item['arm'],state='NOT_RUN',reason='MEDIA_NOT_QUALIFIED')
        journal.close()
        require(any(available.values()), 'NO_EXECUTABLE_MEDIA_GPU_GOLD_ZERO')
        # Exactly one actual nvidia-smi query, parses graphics vs compute processes.
        code = 'import sys,subprocess;sys.stdin.readline();p=subprocess.run(["nvidia-smi","-q","-x","-i","0"],capture_output=True,timeout=8);sys.stdout.buffer.write(p.stdout[:65536]);sys.exit(p.returncode)'
        telemetry = phase(root,'gpu-resource','cpu',10,[own_python,'-I','-S','-B','-c',code])
        require(telemetry['exit_code']==0 and not telemetry['overflow'],'GPU_TELEMETRY')
        gpu = ET.fromstring(telemetry['stdout']).find('gpu'); require(gpu is not None,'GPU_TELEMETRY_SCHEMA')
        memory = gpu.findtext('fb_memory_usage/free',''); free = int(memory.split()[0])
        processes = [p.findtext('type','') for p in gpu.findall('processes/process_info')]
        require('3090' in gpu.findtext('product_name','') and free >= 20*1024 and all('C' not in p for p in processes),'GPU_BUSY_OR_FREE_MEMORY')
        journal=Journal(root); journal.write('gpu-resource-summary.json',dict(free_MiB=free,process_types=processes,query_count=1));journal.close()
        # No credential values/profile overrides are passed to the model child.
        environment = {k:v for k,v in os.environ.items() if not k.upper().startswith(('AWS_','AZURE_','GOOGLE_','HF_TOKEN'))}
        environment.update(PATH=runtime['path'],HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',
                           TEMP=str(root),TMP=str(root),TOKENIZERS_PARALLELISM='false',PYTHONDONTWRITEBYTECODE='1')
        journal=Journal(root);journal.once('MODEL_LAUNCH','gpu',queue_hash=digest(load(root,'queue.json')));journal.close()
        model_exit = phase(root,'gpu-worker','gpu',900,
                           python_command(runtime['python'],'development_worker_030',str(root),site=runtime['site']),environment)
    except Exception as error:
        journal=Journal(root)
        journal.write('execution-hold.json',dict(reason=str(error) if isinstance(error,ContractError) else type(error).__name__))
        journal.close()
    finally:
        journal=Journal(root)
        config=load(root,'worker-input.json')
        ended={r['key'] for r in journal.events('TERMINAL')}; started={r['key'] for r in journal.events('STARTED')}
        for item in config['slots']:
            key=str(item['slot'])
            if key not in ended:
                journal.once('TERMINAL',key,alias=item['alias'],arm=item['arm'],state='FAILED' if key in started else 'NOT_RUN',reason='WORKER_STOPPED')
        if model_exit:
            journal.add('MODEL_EXIT',pid=model_exit['pid'],job_active=model_exit['job_active'],code=model_exit['exit_code'])
            journal.add('QUEUE_CLOSED',pid=model_exit['pid'],model_exit_hash=journal.events('MODEL_EXIT')[0]['hash'],terminal_hash=digest(journal.events('TERMINAL')))
        else:
            journal.add('NO_MODEL_QUEUE_CLOSED',slots=16)
        can_score=bool(model_exit and any(r['state'] in ('RETURNED','INVALID') for r in journal.events('TERMINAL')))
        journal.close()
        if handle is not None:
            handle.close()
        if can_score:
            phase(root,'score','cpu',120,python_command(own_python,'development_pilot_030','score',str(root)))


def finish_stopped(root):
    """Close this failed030 without original input, credentials, media or model IO."""
    import ast
    journal = Journal(root)
    try:
        journal.reserve_time('cpu', 60, 'finalize-stopped')
        # Recover the already persisted two suite exits, not another execution.
        for number in (1,2):
            name='suite-%d' % number
            result=load(root,name+'-exit-private.json')
            if not any(r['name']==name for r in journal.events('SUITE_RESULT')):
                journal.add('SUITE_RESULT',name=name,passed=False,tests=0 if number==1 else 18,
                            failures=0 if number==1 else 2,exit_code=result['exit_code'])
        require(len(journal.events('SUITE'))==2 and not any(r['passed'] for r in journal.events('SUITE_RESULT')), 'STOP_REASON_BINDING')
        journal.once('RUN_STOPPED','030',reason='SECOND_SUITE_FAILED_NO_THIRD_ATTEMPT')
        cached=dict(status='HOLD')
        try:
            plan=restored_plan(root)
            require(len(plan.questions)==4 and len(plan.calls)==16
                    and packed(asdict(plan))==packed(load(root,'plan.json')['plan']), 'CACHED_PLAN_BINDING')
            require([asdict(q.key) for q in plan.questions]==load(root,'keys.json')['keys'],'CACHED_KEYS')
            binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1']
            for name in ('keys','cohort','nongold','plan','receipts','official'):
                require(load(root,name+'.json')['binding']==binding,'CACHED_PROFILE')
            options=load(root,'nongold.json')['projection']['questions']
            require(len(options)==4 and all(len(q['options'])==5 and all(v.strip() for v in q['options']) for q in options),'CACHED_OPTIONS')
            receipt=[r for r in load(root,'receipts.json')['receipts'] if r['alias']=='annotation']
            require(len(receipt)==3 and all(r['complete'] for r in receipt)
                    and len({(r['byte_count'],r['digest'],tuple(r['before'])) for r in receipt})==1,'CACHED_FULL_RECEIPT')
            reference=load(root,'annotation-reference.json')
            require(reference['identity']==receipt[0]['before'][:2] and reference['size']==receipt[0]['byte_count']
                    and reference['mtime_ns']==receipt[0]['before'][3],'INITIAL_STAT_TO_028_BINDING')
            helper_matches=0
            for number in (0,1):
                factory=ast.parse((Path(root)/('factory_%d.py' % number)).read_text(encoding='utf-8'))
                source=ast.parse((Path(root)/('runner_%d.py' % number)).read_text(encoding='utf-8'))
                left=[n for n in ast.walk(factory) if isinstance(n,ast.FunctionDef) and n.name=='inputs']
                right=[n for n in ast.walk(source) if isinstance(n,ast.FunctionDef) and n.name=='inputs']
                require(len(left)==len(right)==1 and ast.dump(left[0])==ast.dump(right[0]),'CACHED_HELPER_AST')
                helper_matches+=1
            official=load(root,'official.json')['joined']['rows'];targets=load(root,'targets.json')['targets']
            require(len(targets)==4,'CACHED_TARGET_COUNT')
            for n,q in enumerate(plan.questions):
                row=official[q.key.source]
                require(row['video_uid']==q.key.source and row['canonical_s3_location']==targets[n]['uri']
                        and targets[n]['alias']=='P%d' % (n+1) and row['release_1']=='True'
                        and row['canonical_is_validated']=='True','CACHED_OFFICIAL_JOIN')
            cached=dict(status='PASS_CACHED_NONGOLD_ONLY',n=4,options=20,slots=16,helpers_ast_equal=helper_matches,
                        full028_receipts=3,profile=binding,source_overlap_allowed=True,prior_exposure_possible=True)
        except Exception as error:
            cached['reason']=str(error) if isinstance(error,ContractError) else type(error).__name__
        slots=[dict(slot=n,alias='P%d' % (n//4+1),arm='ABCD'[(n%4+n//4)%4],state='NOT_RUN',reason='SECOND_SUITE_FAILED') for n in range(16)]
        require(not journal.events('STARTED') and not journal.events('HTTPS') and not journal.events('MODEL_LAUNCH'),'NO_REAL_ACTIONS_FOR_STOP')
        for item in slots:
            journal.once('TERMINAL',str(item['slot']),alias=item['alias'],arm=item['arm'],state='NOT_RUN',reason=item['reason'])
        journal.write('stopped-queue.json',dict(n=4,slots=slots,queue_closed=True,model_launched=False,gold_opens=0))
        journal.add('NO_MODEL_QUEUE_CLOSED',slots=16,reason='SUITE_FAILURE',gold_allowed=False)
        journal.write('cached-handoff-verification.json',cached)
        inputs=journal.events('INPUT');windows=journal.events('WINDOW');exits=journal.events('PHASE_EXIT')
        summary=dict(status='IMPLEMENTATION_WITNESS_HOLD_REAL_QA_NOT_RUN',cached=cached,n=4,slots=16,
            suite_starts=2,first_suite_tests=0,second_suite_tests=18,second_suite_passed=16,second_suite_failures=2,
            fixture_children=len(journal.events('FIXTURE')),source_opens=len(inputs),source_bytes=sum(r['size'] for r in inputs),
            input_categories={k:sum(r['category']==k for r in inputs) for k in ('handoff','source','config','gold')},
            cpu_reserved_seconds=sum(r['seconds'] for r in windows if r['stage']=='cpu'),
            observed_suite_windows_seconds=sum(r['seconds'] for r in exits),parent_elapsed_seconds=time.time()-journal.rows[0]['epoch'],
            actual_https=0,head_bucket=0,head_object=0,get_object=0,media_bytes=0,original_annotation_body=0,gold_opens=0,
            model_launches=0,generate=0,gpu_seconds=0,nvidia_queries=0,training_updates=0)
        journal.write('final-summary.json',summary)
        print(json.dumps(summary))
    finally:
        journal.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['initialize', 'probe', 'prepare', 'execute', 'score', 'finalize-stopped'])
    parser.add_argument('root')
    args = parser.parse_args()
    if args.mode == 'probe':
        probe(args.root); return
    payload = sys.stdin.readline()
    if args.mode == 'initialize':
        config = json.loads(payload); initialize(args.root, config['entries'], config['annotation']); return
    if args.mode == 'prepare':
        prepare(args.root)
    elif args.mode == 'execute':
        execute(args.root)
    elif args.mode == 'score':
        score(args.root)
    elif args.mode == 'finalize-stopped':
        finish_stopped(args.root)


if __name__ == '__main__':
    main()
