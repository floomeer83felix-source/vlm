"""048 single authorized local-media CPU boundary. No model/inference/network.

Only caller-supplied exact paths; no discovery. Source and input identities,
clocks, native text and hashes are PRIVATE receipts, never public evidence.
"""
import bisect
import ctypes as C
from ctypes import wintypes as W
from fractions import Fraction as Q
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import time
from types import MappingProxyType

API_SHA = 'efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9'
ARMS = ('B0', 'P', 'N')
STAGES = dict(sha_pre=60, scan=600, select=600, processor=300, sha_post=60)


def need(ok, code):
    if not ok:
        raise ValueError(code)


def pack(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(x):
    return hashlib.sha256(pack(x)).hexdigest()


def read(p):
    return json.loads(Path(p).read_bytes())


def write(p, x, replace=False):
    p = Path(p); b = pack(x)
    need(len(b) <= 16*1024**2, 'RECEIPT_SIZE')
    target = p.with_suffix(p.suffix+'.writing') if replace else p
    with target.open('xb') as h:
        h.write(b); h.flush(); os.fsync(h.fileno())
    if replace:
        os.replace(target, p)


def fingerprint_file_stat(path):
    s = Path(path).lstat()
    need(stat.S_ISREG(s.st_mode) and not getattr(s, 'st_file_attributes', 0) & 1024 and not stat.S_ISLNK(s.st_mode), 'MEDIA_TYPE')
    return dict(size=s.st_size, mtime_ns=s.st_mtime_ns, ino=s.st_ino, dev=s.st_dev)


def initial_stat_agrees(current, initial):
    # Windows st_dev representation differs between the installed Python runtimes.
    # Preserve inode/size/mtime initially; ALL fields remain strict within worker.
    return all(current[k] == initial[k] for k in ('size', 'mtime_ns', 'ino'))


def choose(points):
    need(len(points) >= 48 and all(a < b for a, b in zip(points, points[1:])), 'PTS_ORDER_OR_COUNT')
    first = points[0]; normalized = tuple(p-first for p in points)
    span = normalized[-1]
    indices = tuple(round(Q(j*(len(points)-1), 47)) for j in range(48))
    targets = tuple(Q(j)*span/48 for j in range(48))
    ni = tuple(bisect.bisect_right(normalized, target)-1 for target in targets)
    need(all(0 <= i < len(points)-1 and normalized[i] <= u < normalized[i+1] for i, u in zip(ni, targets)), 'N_HOLD_INTERVAL')
    return normalized, indices, ni, targets


class RequestMap:
    __slots__ = ('points', 'indices', 'rate', 'F', 'T', '_locked')
    def __setattr__(self, k, v):
        if getattr(self, '_locked', False):
            raise AttributeError('IMMUTABLE_REQUEST_MAP')
        object.__setattr__(self, k, v)

    def __init__(self, points, indices, rate):
        self.points = MappingProxyType(dict(enumerate(points)))
        self.indices = tuple(indices); self.rate = Q(rate)
        self.F = len(points); self.T = points[-1]
        need(len(self.indices) == 48 and all(type(i) is int and 0 <= i < self.F for i in self.indices), 'MAP_INDICES')
        need(self.rate > 0 and math.isfinite(float(self.rate)), 'MAP_RATE')
        need(points[0] == 0 and all(a < b for a, b in zip(points, points[1:])), 'MAP_POINTS')
        self._locked = True

    def resolve(self, indices, fps, merge_size):
        if hasattr(indices, 'tolist'):
            indices = indices.tolist()
        need(isinstance(indices, (list, tuple)) and all(type(i) is int for i in indices) and tuple(indices) == self.indices, 'CALLBACK_INDICES')
        need(type(merge_size) is int and merge_size == 2, 'CALLBACK_MERGE')
        need(type(fps) is not bool and float(fps) == float(self.rate), 'CALLBACK_FPS')
        return tuple((self.points[indices[j]]+self.points[indices[j+1]])/2 for j in range(0, 48, 2))


def scoped(base, mapping):
    class Scoped(type(base)):
        def __call__(self, **kw):
            need(not self._used, 'REQUEST_REUSED'); self._used = True
            need(set(kw) == {'text', 'videos', 'video_metadata', 'do_sample_frames', 'do_resize', 'return_tensors'}, 'REQUEST_KEYS')
            need(kw['do_sample_frames'] is False and kw['do_resize'] is False and kw['return_tensors'] == 'pt', 'REQUEST_CONFIG')
            need(len(kw['videos']) == len(kw['video_metadata']) == len(kw['text']) == 1 and tuple(kw['videos'][0].shape) == (48, 192, 288, 3), 'REQUEST_SHAPE')
            m = kw['video_metadata'][0]
            need(m.total_num_frames == mapping.F and m.duration == float(mapping.T) and m.width == 288 and m.height == 192, 'REQUEST_METADATA')
            mapping.resolve(m.frames_indices, m.fps, self.video_processor.merge_size)
            self._active = True
            try:
                return super().__call__(**kw)
            finally:
                self._active = False

        def _calculate_timestamps(self, indices, video_fps, merge_size=2):
            need(self._active, 'CALLBACK_OUTSIDE_REQUEST')
            raw = mapping.resolve(indices, video_fps, merge_size)
            self._raw_trace.append([str(v) for v in raw])
            return [float(v) for v in raw]
    instance = Scoped(image_processor=base.image_processor, tokenizer=base.tokenizer,
                      video_processor=base.video_processor, chat_template=base.chat_template)
    instance._used = False; instance._active = False; instance._raw_trace = []
    return instance


def letterbox_size(w, h):
    need(type(w) is int and type(h) is int and 0 < w <= 4096 and 0 < h <= 2160, 'FRAME_DIMENSION')
    scale = min(Q(288, w), Q(192, h))
    nw, nh = max(1, round(w*scale)), max(1, round(h*scale))
    return nw, nh, (288-nw)//2, (192-nh)//2


def policy(root, cfg, state):
    root = Path(root).absolute(); media = Path(cfg['media']).absolute()
    runtime = [Path(cfg['site']).absolute(), Path(sys.base_prefix).absolute()]
    model = Path(cfg['model']).absolute()
    exact = {Path(__file__).absolute(), Path(__file__).with_name('test_existing_media_input_048.py').absolute()}
    def within(p, bases):
        return any(p == b or b in p.parents for b in bases)
    def audit(event, args):
        if event.startswith('socket.') or event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.startfile'):
            raise PermissionError('NETWORK_OR_CHILD_DENIED')
        if event in ('os.listdir', 'os.scandir'):
            p = Path(os.path.abspath(args[0] or '.'))
            need(within(p, [root, model]+runtime), 'ENUMERATION_DENIED')
        if event == 'open' and not isinstance(args[0], int):
            if os.path.normcase(os.fsdecode(args[0])) == os.path.normcase(os.devnull):
                return
            p = Path(os.path.abspath(args[0])); mode, flags = args[1], args[2]
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and bool(flags & (os.O_CREAT | os.O_WRONLY | os.O_RDWR | os.O_TRUNC)))
            if writing:
                need(within(p, [root]), 'WRITE_SCOPE')
            elif p == media:
                need(state.get('media_open') is True, 'UNMETERED_MEDIA_OPEN')
            else:
                need(p.suffix.lower() not in ('.safetensors', '.bin', '.pt', '.pth', '.gguf', '.onnx', '.mp4', '.webm', '.wav'), 'WEIGHTS_OR_OTHER_MEDIA_DENIED')
                need(p in exact or within(p, [root, model]+runtime), 'READ_SCOPE')
    sys.addaudithook(audit)


class ReadBudget:
    def __init__(self, root, cap):
        self.root = Path(root); self.cap = cap; self.reserved = 0; self.returned = 0
        self.by_phase = {}; self.persist()

    def persist(self):
        write(self.root/'read-budget.json', dict(cap=self.cap, reserved=self.reserved, returned=self.returned, phases=self.by_phase), replace=True)

    def reserve(self, phase, n):
        need(type(n) is int and n >= 0 and self.reserved+n <= self.cap, 'MEDIA_READ_CAP')
        self.reserved += n
        d = self.by_phase.setdefault(phase, dict(reserved=0, returned=0, reads=0, seeks=0))
        d['reserved'] += n; d['reads'] += 1; self.persist()

    def account(self, phase, n):
        self.returned += n; self.by_phase[phase]['returned'] += n; self.persist()


class Meter:
    def __init__(self, path, budget, phase, state):
        self.path = Path(path); self.budget = budget; self.phase = phase
        state['media_open'] = True
        try:
            self.file = self.path.open('rb')
        finally:
            state['media_open'] = False

    def read(self, n=-1):
        if n < 0:
            n = max(0, self.path.stat().st_size-self.file.tell())
        self.budget.reserve(self.phase, n)
        b = self.file.read(n); self.budget.account(self.phase, len(b))
        return b

    def seek(self, offset, whence=0):
        self.budget.by_phase.setdefault(self.phase, dict(reserved=0, returned=0, reads=0, seeks=0))['seeks'] += 1
        self.budget.persist()
        return self.file.seek(offset, whence)

    def tell(self):
        return self.file.tell()

    def readable(self):
        return True

    def seekable(self):
        return True

    def close(self):
        self.file.close()


def events():
    k = C.WinDLL('kernel32', use_last_error=True)
    signatures = [('OpenEventW', [W.DWORD, W.BOOL, W.LPCWSTR], W.HANDLE),
                  ('SetEvent', [W.HANDLE], W.BOOL), ('WaitForSingleObject', [W.HANDLE, W.DWORD], W.DWORD),
                  ('CloseHandle', [W.HANDLE], W.BOOL)]
    for name, args, result in signatures:
        getattr(k, name).argtypes = args; getattr(k, name).restype = result
    return k


def phase_start(root, cfg, name):
    # Parent ACK establishes a parent-local stage deadline BEFORE this work begins.
    k = events(); prefix = cfg['event_prefix']
    start = k.OpenEventW(2, False, prefix+'-'+name)
    ack = k.OpenEventW(0x100000, False, prefix+'-'+name+'-ack')
    need(start and ack, 'STAGE_EVENT_OPEN')
    try:
        need(k.SetEvent(start), 'STAGE_EVENT_SET')
        need(k.WaitForSingleObject(ack, 10000) == 0, 'PARENT_STAGE_ACK')
    finally:
        k.CloseHandle(start); k.CloseHandle(ack)
    return time.monotonic()


def boundary(batch, torch, common):
    result = {k: v.to(dtype=torch.bfloat16) if torch.is_tensor(v) and k in ('pixel_values', 'pixel_values_videos') and v.is_floating_point() else v for k, v in batch.items()}
    parts = {}
    for k, v in result.items():
        if torch.is_tensor(v):
            need(v.device.type == 'cpu', 'NON_CPU_TENSOR')
            parts[k] = dict(shape=list(v.shape), dtype=str(v.dtype), device='cpu', sha256=hashlib.sha256(v.contiguous().view(torch.uint8).numpy().tobytes()).hexdigest())
        else:
            parts[k] = dict(value=v)
    return result, dict(fields=parts, full_hash=digest(dict(fields=parts, common=common)))


def equal(left, right, torch, keys=None):
    if keys is None:
        if set(left) != set(right):
            return False
        keys = list(left)
    for key in keys:
        if key not in left or key not in right:
            return False
        a, b = left[key], right[key]
        if torch.is_tensor(a):
            if not torch.is_tensor(b) or a.dtype != b.dtype or a.shape != b.shape or a.device != b.device or not torch.equal(a, b):
                return False
        elif a != b:
            return False
    return True


def base_identity(base, versions):
    return digest(dict(versions=versions, image=base.image_processor.to_dict(), video=base.video_processor.to_dict(),
                       tokenizer=base.tokenizer.backend_tokenizer.to_str(), special_tokens=base.tokenizer.special_tokens_map,
                       template=base.chat_template))


def worker(root):
    root = Path(root); cfg = read(root/'config.json'); gate = {}
    policy(root, cfg, gate); budget = ReadBudget(root, cfg['media_read_cap'])
    costs = []; rows = {a: dict(arm=a, status='NOT_RUN') for a in ARMS}
    active_stage = 'bootstrap'; calls = 0; load_count = 0
    def stage(name):
        nonlocal active_stage
        active_stage = name
        return phase_start(root, cfg, name)
    def finish(name, start, **extra):
        elapsed = time.monotonic()-start
        need(elapsed < STAGES[name], 'LOCAL_STAGE_TIMEOUT')
        costs.append(dict(stage=name, start=start, end=time.monotonic(), wall=elapsed, clock_domain='WORKER_LOCAL', **extra))
        write(root/'costs.json', costs, replace=True)
    def hash_media(name):
        meter = Meter(cfg['media'], budget, name, gate); h = hashlib.sha256()
        try:
            while True:
                b = meter.read(1024**2)
                if not b:
                    break
                h.update(b)
        finally:
            meter.close()
        return h.hexdigest()
    def open_video(av, meter):
        c = av.open(meter, mode='r', buffer_size=32768, hwaccel=None)
        need(len(c.streams.video) == 1, 'ONE_VIDEO_STREAM')
        s = c.streams.video[0]; s.codec_context.thread_count = 4; s.codec_context.thread_type = 'SLICE'
        return c, s
    try:
        start = stage('sha_pre')
        before = fingerprint_file_stat(cfg['media'])
        need(initial_stat_agrees(before, cfg['before_stat']) and before['size'] == 103909467, 'PREFLIGHT_STAT_CHANGED')
        pre_sha = hash_media('sha_pre'); write(root/'before.json', dict(stat=before, sha256=pre_sha))
        finish('sha_pre', start)

        start = stage('scan')
        import av
        need(av.__version__ == '15.1.0', 'PYAV_VERSION')
        av.logging.set_level(av.logging.PANIC)
        meter = Meter(cfg['media'], budget, 'scan', gate); table = []; eof = False
        try:
            container, stream = open_video(av, meter)
            with container:
                need(stream.average_rate is not None, 'AVERAGE_RATE_MISSING')
                rate = Q(stream.average_rate); need(rate > 0 and math.isfinite(float(rate)), 'AVERAGE_RATE_INVALID')
                previous = None
                for frame in container.decode(video=0):
                    need(len(table) < 60000 and frame.pts is not None and frame.time_base is not None, 'FRAME_LIMIT_OR_PTS_MISSING')
                    tb = Q(frame.time_base); point = Q(frame.pts)*tb
                    need(tb > 0 and (previous is None or point > previous), 'DISPLAY_PTS_ORDER')
                    letterbox_size(frame.width, frame.height)
                    table.append([int(frame.pts), str(tb), frame.duration, frame.width, frame.height]); previous = point
                    del frame
                eof = True
        finally:
            meter.close()
        points = [Q(r[0])*Q(r[1]) for r in table]
        normalized, indices, ni, targets = choose(points)
        span = normalized[-1]; need(eof and 1200 <= span <= 1800, 'COVERAGE_GATE')
        write(root/'clock-table.json', dict(rows=table, average_rate=str(rate), eof=eof))
        plan = dict(F=len(table), rate=str(rate), origin=str(points[0]), T_cov=str(span),
                    indices=indices, n_indices=ni, n_targets=[str(x) for x in targets],
                    selected_t=[str(normalized[i]) for i in indices],
                    n_selected_t=[str(normalized[i]) for i in ni],
                    max_offset=str(max(abs(Q(i)/rate-normalized[i]) for i in indices)),
                    frame_dimensions=sorted({(r[3], r[4]) for r in table}),
                    clock_table_sha=digest(dict(rows=table, average_rate=str(rate), eof=eof)),
                    convention='ENGINEERING_HOLD_BETWEEN_DISPLAY_STARTS_NOT_MEDIA_ENDPOINT')
        write(root/'plan.json', plan)
        write(root/'plan-seal.json', dict(plan_sha=digest(plan), code_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
        finish('scan', start, frames=len(table), eof=True)

        start = stage('select')
        import numpy as np
        from PIL import Image
        need(np.__version__ == '1.26.4', 'NUMPY_VERSION')
        wanted = set(indices+ni); need(len(wanted) <= 96, 'BUFFER_COUNT')
        buffers = {}; meter = Meter(cfg['media'], budget, 'select', gate)
        convert_wall = 0.; letterbox_wall = 0.; decode_wall = 0.; count = 0
        try:
            container, stream = open_video(av, meter)
            with container:
                need(Q(stream.average_rate) == rate, 'SECOND_RATE_CHANGED')
                iterator = iter(container.decode(video=0))
                while True:
                    tick = time.monotonic()
                    try:
                        frame = next(iterator)
                    except StopIteration:
                        decode_wall += time.monotonic()-tick; break
                    decode_wall += time.monotonic()-tick
                    need(count < len(table), 'SECOND_EXTRA_FRAMES')
                    actual = [int(frame.pts) if frame.pts is not None else None, str(Q(frame.time_base)), frame.duration, frame.width, frame.height]
                    need(actual == table[count], 'SECOND_PASS_TIMING_CHANGED')
                    if count in wanted:
                        tick = time.monotonic(); pixels = frame.to_ndarray(format='rgb24'); convert_wall += time.monotonic()-tick
                        tick = time.monotonic(); image = Image.fromarray(pixels)
                        nw, nh, x, y = letterbox_size(frame.width, frame.height)
                        canvas = Image.new('RGB', (288, 192), (0, 0, 0))
                        canvas.paste(image.resize((nw, nh), Image.Resampling.BILINEAR), (x, y))
                        buffers[count] = np.array(canvas, dtype=np.uint8)
                        letterbox_wall += time.monotonic()-tick
                        del pixels, image, canvas
                    count += 1; del frame
        finally:
            meter.close()
        need(count == len(table) and set(buffers) == wanted, 'SECOND_PASS_INCOMPLETE')
        stack_start = time.monotonic()
        bframes = np.stack([buffers[i] for i in indices]); nframes = np.stack([buffers[i] for i in ni])
        bframes.setflags(write=False); nframes.setflags(write=False)
        rgb_hash = dict(B0=hashlib.sha256(bframes.tobytes()).hexdigest(), N=hashlib.sha256(nframes.tobytes()).hexdigest())
        mapping = RequestMap(normalized, indices, rate)
        write(root/'selection.json', dict(frames=count, eof=True, buffered=len(buffers), n_duplicate_count=48-len(set(ni)),
                                          differing_indices=sum(a != b for a, b in zip(indices, ni)),
                                          displacements=[b-a for a, b in zip(indices, ni)], rgb_hash=rgb_hash,
                                          decoder_next_inclusive=decode_wall, convert=convert_wall, letterbox=letterbox_wall,
                                          stack=time.monotonic()-stack_start))
        finish('select', start, shared_once=True)

        start = stage('processor')
        import torch
        import transformers
        from transformers import AutoProcessor
        from transformers.video_utils import VideoMetadata
        need(torch.__version__ == '2.5.1' and transformers.__version__ == '4.57.6', 'CPU_RUNTIME_VERSION')
        torch.set_num_threads(4); torch.set_num_interop_threads(1)
        need(not torch.cuda.is_initialized(), 'CUDA_INITIALIZED')
        source = Path(cfg['site'])/'transformers/models/qwen3_vl/processing_qwen3_vl.py'
        need(hashlib.sha256(source.read_bytes()).hexdigest() == API_SHA, 'PROCESSOR_SOURCE')
        load_count += 1
        base = AutoProcessor.from_pretrained(cfg['model'], local_files_only=True, trust_remote_code=False)
        need(type(base).__name__ == 'Qwen3VLProcessor', 'PROCESSOR_CLASS')
        versions = dict(torch=torch.__version__, transformers=transformers.__version__, numpy=np.__version__, av=av.__version__)
        common = base_identity(base, versions); original = type(base)._calculate_timestamps
        component_ids = (id(base), id(base.image_processor), id(base.video_processor), id(base.tokenizer))
        template = base.apply_chat_template([dict(role='system', content='You are a helpful assistant.'),
                    dict(role='user', content=[dict(type='video'), dict(type='text', text='Describe the video.')])],
                    tokenize=False, add_generation_prompt=True)
        states = {}; records = {}
        def prepare(arm, kind):
            nonlocal calls
            need(calls < 4, 'PROCESSOR_CALL_CAP'); calls += 1
            write(root/'calls.json', dict(calls=calls, load_count=load_count, next_arm=arm, kind=kind), replace=True)
            nf, fps, selected, array = (48, Q(48)/span, tuple(range(48)), nframes) if arm == 'N' else (len(table), rate, indices, bframes)
            metadata = VideoMetadata(total_num_frames=nf, fps=float(fps), duration=float(span), width=288, height=192, frames_indices=list(selected))
            processor = scoped(base, mapping) if arm == 'P' else base
            traces = []
            def profile(frame, event, arg):
                if frame.f_code.co_name != '_calculate_timestamps':
                    return
                if event == 'call':
                    loc = frame.f_locals; ix = loc['indices']
                    traces.append(dict(indices=ix.tolist() if hasattr(ix, 'tolist') else list(ix), fps=float(loc['video_fps']), merge=loc['merge_size']))
                elif event == 'return' and traces:
                    traces[-1]['returned'] = list(arg) if arg is not None else None
            tick = time.monotonic(); sys.setprofile(profile)
            try:
                batch = processor(text=[template], videos=[array], video_metadata=[metadata], do_sample_frames=False, do_resize=False, return_tensors='pt')
            finally:
                sys.setprofile(None)
            state, info = boundary(batch, torch, common)
            need(set(state) == {'input_ids', 'attention_mask', 'pixel_values_videos', 'video_grid_thw'}, 'UNQUALIFIED_EXTRA_FIELD')
            need(state['input_ids'].dtype == state['attention_mask'].dtype == torch.int64 and state['pixel_values_videos'].dtype == torch.bfloat16, 'BOUNDARY_DTYPES')
            need(state['video_grid_thw'].tolist() == [[24, 12, 18]], 'GRID_BOUNDARY')
            need(int(state['video_grid_thw'].prod())//4 == 1296, 'VISUAL_TOKENS')
            need(state['input_ids'].shape == state['attention_mask'].shape and bool(torch.all(state['attention_mask'] == 1)), 'ATTENTION_CONTRACT')
            need(len(traces) == 1 and traces[0]['indices'] == list(selected) and traces[0]['fps'] == float(fps) and traces[0]['merge'] == 2 and len(traces[0]['returned']) == 24, 'ACTUAL_CALLBACK')
            decoded = base.tokenizer.decode(state['input_ids'][0].tolist(), skip_special_tokens=False, clean_up_tokenization_spaces=False)
            timecodes = re.findall(r'<([0-9]+\.[0-9]) seconds>', decoded)
            need(len(timecodes) == 24 and timecodes == [f'{t:.1f}' for t in traces[0]['returned']], 'NATIVE_FORMAT')
            need(base.tokenizer.encode(decoded, add_special_tokens=False) == state['input_ids'][0].tolist(), 'TOKENIZER_ROUNDTRIP')
            stripped = re.sub(r'<[0-9]+\.[0-9] seconds>', '<TIME>', decoded)
            need(base_identity(base, versions) == common and type(base)._calculate_timestamps is original and
                 component_ids == (id(base), id(base.image_processor), id(base.video_processor), id(base.tokenizer)), 'BASE_MUTATED')
            need(not torch.cuda.is_initialized(), 'CUDA_INITIALIZED')
            info.update(arm=arm, kind=kind, callbacks=traces, timecodes=timecodes, stripped=stripped,
                        native_fps=float(fps), rational_fps=str(fps), declared_frames=nf, declared_indices=list(selected),
                        duration=str(span), grid=state['video_grid_thw'].tolist(), visual_tokens=1296,
                        roundtrip=True, base_unchanged=True, all_fields_compared=True, wall=time.monotonic()-tick,
                        raw_rational=[str(x) for x in mapping.resolve(selected, float(rate), 2)] if arm == 'P' else
                        [str((Q(selected[j])+Q(selected[j+1]))/(2*Q.from_float(float(fps)))) for j in range(0, 48, 2)])
            if arm == 'P':
                need(len(processor._raw_trace) == 1, 'SCOPED_CALLBACK_TRACE')
            return state, info
        probe_state, probe = prepare('B0', 'probe')
        write(root/'probe.json', probe); del probe_state
        write(root/'formal-seal.json', dict(code_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                            plan_sha=digest(plan), base_identity=common, prompt=template, order=list(ARMS)))
        for arm in ARMS:
            rows[arm] = dict(arm=arm, status='STARTED'); write(root/'rows.json', list(rows.values()), replace=True)
            state, info = prepare(arm, 'formal'); states[arm] = state
            if arm == 'P':
                need(equal(state, states['B0'], torch, ('pixel_values_videos', 'video_grid_thw')), 'VISUAL_NOT_EQUAL')
                need(info['stripped'] == records['B0']['stripped'], 'NON_TIME_TEXT_CHANGED')
            info['visual_equal_B0'] = equal(state, states['B0'], torch, ('pixel_values_videos', 'video_grid_thw'))
            info['full_equal'] = {other: equal(state, other_state, torch) for other, other_state in states.items()}
            info['status'] = 'PASS'; rows[arm] = info; records[arm] = info
            write(root/'rows.json', list(rows.values()), replace=True)
        need(hashlib.sha256(bframes.tobytes()).hexdigest() == rgb_hash['B0'] and hashlib.sha256(nframes.tobytes()).hexdigest() == rgb_hash['N'], 'RGB_MUTATED')
        write(root/'processor-complete.json', dict(calls=calls, load_count=load_count, cuda_initialized=torch.cuda.is_initialized(), base_unchanged=True, versions=versions))
        finish('processor', start, calls=calls, load_count=load_count)

        start = stage('sha_post')
        after = fingerprint_file_stat(cfg['media']); post_sha = hash_media('sha_post')
        after2 = fingerprint_file_stat(cfg['media'])
        stable = before == after == after2 and pre_sha == post_sha
        write(root/'after.json', dict(stat=after2, sha256=post_sha, stable=stable))
        need(stable, 'FINAL_MEDIA_CHANGED')
        finish('sha_post', start)
        write(root/'complete.json', dict(status='CPU_REAL_MEDIA_INPUT_PASS', stable=True, calls=calls, load_count=load_count))
    except Exception as exc:
        for arm in ARMS:
            if rows[arm]['status'] == 'STARTED':
                rows[arm] = dict(arm=arm, status='FAILED')
        # Private diagnostic only; publication selects the safe stage/error enum.
        write(root/'failure.json', dict(stage=active_stage, exception=type(exc).__name__, diagnostic=str(exc)[:1200], calls=calls, load_count=load_count))
        write(root/'rows.json', list(rows.values()), replace=True)


if __name__ == '__main__':
    need(len(sys.argv) == 3 and sys.argv[1] == 'worker', 'ROLE')
    worker(sys.argv[2])
