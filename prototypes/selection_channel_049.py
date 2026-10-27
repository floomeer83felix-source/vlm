"""049 bounded development comparison. Roles use separate explicit inputs.

No downloads or installed-library patching. Gold is opened only by score(),
after the owned inference Job actually exits. Private content is not published.
"""
import ctypes as C
from ctypes import wintypes as W
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import time
import unicodedata
import ast
from fractions import Fraction

U = [0, 4, 9, 13, 17, 21, 26, 30, 34, 38, 43, 47]
CONDITIONS = ['G1', 'G2', 'G3', 'G4', 'GU', 'Q', 'UO', 'UR', 'SO', 'SR']
SYSTEM = 'You are a helpful assistant.'
USER = ('Answer the multiple-choice question using the video when available.\n'
        'Time labels, when present, are ordinal positions, not real elapsed seconds.\n'
        'Question: {question}\nOptions:\nA. {A}\nB. {B}\nC. {C}\nD. {D}\nE. {E}\n'
        'Return exactly one uppercase letter: A, B, C, D, or E.')
TEMPORAL = re.compile(r'\b(?:when|before|after|during|first|last|next|previous|earlier|later|begin|beginning|end|ending|start|starting|finish|finished|order|sequence|duration|timestamp|timecode|elapsed|seconds?|minutes?|hours?|milliseconds?|fps|speed|frequency|pace|how\s+long|how\s+much\s+time|how\s+fast|how\s+often|what\s+time|which\s+time)\b|\d\s*:\s*\d')
CHINESE = ('何时','什么时候','之前','之后','期间','首先','最后','接着','此前','随后','开始','结束','顺序','时序','时长','时间戳','秒','分钟','小时','多久','多快','频率')
EXTERNAL = re.compile(r'https?://|\.(?:png|jpg|jpeg|gif|svg)\b|\b(?:image above|picture above|shown image|reference image|auxiliary image)\b|参考图片|上图|下图')


def need(ok, code):
    if not ok:
        raise ValueError(code)


def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(Path(p).read_bytes())


def projected_json(raw, wanted, fields):
    """Lexically skip unretained values; decode only keys and requested fields.

    Existing nonfinite literals are accepted ONLY while skipping, consistent
    with the unchanged frozen file. No unselected gold value is decoded.
    """
    text=raw.decode('utf-8-sig'); n=len(text)
    def ws(p):
        while p<n and text[p] in ' \r\n\t':p+=1
        return p
    def string_end(p):
        need(text[p]=='"','JSON_STRING');p+=1
        while p<n:
            if text[p]=='\\':p+=2
            elif text[p]=='"':return p+1
            else:p+=1
        raise ValueError('JSON_STRING_EOF')
    def skip(p):
        p=ws(p);need(p<n,'JSON_EOF')
        if text[p]=='"':return string_end(p)
        if text[p]=='{':
            p=ws(p+1)
            if text[p]=='}':return p+1
            while True:
                p=ws(string_end(p));need(text[p]==':','JSON_COLON');p=ws(skip(p+1))
                if text[p]=='}':return p+1
                need(text[p]==',','JSON_COMMA');p=ws(p+1)
        if text[p]=='[':
            p=ws(p+1)
            if text[p]==']':return p+1
            while True:
                p=ws(skip(p))
                if text[p]==']':return p+1
                need(text[p]==',','JSON_COMMA');p=ws(p+1)
        end=p
        while end<n and text[end] not in ',]} \r\n\t':end+=1
        token=text[p:end]
        need(token in ('true','false','null','NaN','Infinity','-Infinity') or re.fullmatch(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?',token),'JSON_TOKEN')
        return end
    def members(p):
        p=ws(p);need(text[p]=='{','JSON_OBJECT');p=ws(p+1);seen=set()
        if text[p]=='}':return
        while True:
            end=string_end(p);key=json.loads(text[p:end]);need(key not in seen,'JSON_DUPLICATE_KEY');seen.add(key)
            p=ws(end);need(text[p]==':','JSON_COLON');start=ws(p+1);end=skip(start)
            yield key,start,end
            p=ws(end)
            if text[p]=='}':return
            need(text[p]==',','JSON_COMMA');p=ws(p+1)
    def elements(p):
        p=ws(p);need(text[p]=='[','JSON_ARRAY');p=ws(p+1)
        if text[p]==']':return
        i=0
        while True:
            end=skip(p);yield i,p,end;i+=1;p=ws(end)
            if text[p]==']':return
            need(text[p]==',','JSON_COMMA');p=ws(p+1)
    result={};decoded_gold=0
    for uid,start,end in members(0):
        if uid not in wanted:continue
        result[uid]={}
        for name,a,b in members(start):
            if name!='benchmark_dataset':continue
            for ordinal,c,d in elements(a):
                if ordinal not in wanted[uid]:continue
                values={}
                for key,v,w in members(c):
                    if key in fields:
                        value=json.loads(text[v:w],parse_constant=lambda _:(_ for _ in ()).throw(ValueError('RETAINED_NONFINITE')))
                        values[key]=value
                        if key=='correct_answer_label':decoded_gold+=1
                result[uid][ordinal]=values
    need(ws(skip(0))==n,'JSON_TRAILING')
    return result,decoded_gold


def write(p, x, replace=False):
    p = Path(p); b = packed(x); need(len(b) < 32*1024**2, 'RECEIPT_SIZE')
    target = p.with_name(p.name+'.writing') if replace else p
    with target.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    if replace:
        os.replace(target, p)


def event(root, data):
    with (Path(root)/'049-call-ledger.jsonl').open('ab') as f:
        f.write(packed(data)+b'\n'); f.flush(); os.fsync(f.fileno())


def qualify(q):
    if not (isinstance(q.get('question'), str) and q['question'].strip() and isinstance(q.get('options'), list)
            and len(q['options']) == 5 and all(isinstance(v, str) and v.strip() for v in q['options'])
            and type(q.get('ordinal')) is int):
        return 'FORMAT_OR_JOIN'
    text = unicodedata.normalize('NFKC', q['question']+'\n'+'\n'.join(q['options'])).casefold()
    if TEMPORAL.search(text) or any(x in text for x in CHINESE):
        return 'TIME_DEPENDENT'
    if EXTERNAL.search(text):
        return 'EXTERNAL_RESOURCE'
    # Conservative semantic uncertainty beyond the literal word list.
    if re.search(r'\b(?:subsequent|preceding|chronolog\w*|successive|consecutive|eventually|initially|final\s+step|at\s+the\s+moment|prerequisite\s+steps?|immediately\s+follows?)\b', text):
        return 'TIME_DEPENDENT_TASK_SEMANTICS'
    return 'ELIGIBLE_NONGOLD'


def top12(scores):
    need(len(scores) == 48 and all(math.isfinite(float(v)) for v in scores), 'SCORE_FINITE_48')
    return sorted(sorted(range(48), key=lambda i: (-float(scores[i]), i))[:12])


def cross_scores(images, texts, np):
    image = np.asarray(images, dtype=np.float32).astype(np.float64)
    text = np.asarray(texts, dtype=np.float32).astype(np.float64)
    need(image.ndim == 3 and image.shape[:2] == (4, 48) and text.ndim == 2 and image.shape[2] == text.shape[1], 'CROSS_SOURCE_SHAPE')
    need(np.isfinite(image).all() and np.isfinite(text).all(), 'NONFINITE_FEATURE')
    im_norm = np.linalg.norm(image, axis=-1, keepdims=True); tx_norm = np.linalg.norm(text, axis=-1, keepdims=True)
    need((im_norm > 0).all() and (tx_norm > 0).all(), 'ZERO_NORM_FEATURE')
    return np.einsum('qd,svd->qsv', text/tx_norm, image/im_norm)


def parent_remaining(cfg):
    return max(0., cfg['deadline_epoch']-time.time())


def fmt(q):
    return USER.format(question=q['question'], **dict(zip('ABCDE', q['options'])))


def template(processor, q, video=True):
    content = ([dict(type='video')] if video else [])+[dict(type='text', text=fmt(q))]
    return processor.apply_chat_template([dict(role='system', content=SYSTEM), dict(role='user', content=content)], tokenize=False, add_generation_prompt=True)


def cpu_boundary(batch, torch, common):
    state = {k: v.to(dtype=torch.bfloat16) if torch.is_tensor(v) and k in ('pixel_values_videos', 'pixel_values') and v.is_floating_point() else v for k, v in batch.items()}
    fields = {}
    for k, v in state.items():
        if torch.is_tensor(v):
            need(v.device.type == 'cpu', 'CPU_INPUT_REQUIRED')
            fields[k] = dict(shape=list(v.shape), dtype=str(v.dtype), sha256=sha(v.contiguous().view(torch.uint8).numpy().tobytes()))
        else:
            fields[k] = dict(value=v)
    return state, dict(fields=fields, identity=sha(packed(dict(fields=fields, common=common))))


def exact_equal(a, b, torch, keys=None):
    if keys is None:
        if set(a) != set(b):
            return False
        keys = a.keys()
    for k in keys:
        if k not in a or k not in b:
            return False
        x, y = a[k], b[k]
        if torch.is_tensor(x):
            if not torch.is_tensor(y) or x.dtype != y.dtype or x.shape != y.shape or not torch.equal(x, y):
                return False
        elif x != y:
            return False
    return True


def processor_input(processor, q, frames, positions, torch, common):
    from transformers.video_utils import VideoMetadata
    traces = []
    def profile(frame, ev, value):
        if frame.f_code.co_name != '_calculate_timestamps':
            return
        if ev == 'call':
            x = frame.f_locals; ix = x['indices']
            traces.append(dict(indices=ix.tolist() if hasattr(ix, 'tolist') else list(ix), fps=float(x['video_fps']), merge=x['merge_size']))
        elif ev == 'return' and traces:
            traces[-1]['times'] = list(value)
    video = frames is not None; text = template(processor, q, video)
    tick = time.monotonic()
    if video:
        metadata = VideoMetadata(total_num_frames=48, fps=1., duration=48., width=288, height=192, frames_indices=list(positions))
        sys.setprofile(profile)
        try:
            batch = processor(text=[text], videos=[frames], video_metadata=[metadata], do_sample_frames=False, do_resize=False, return_tensors='pt')
        finally:
            sys.setprofile(None)
    else:
        batch = processor(text=[text], return_tensors='pt')
    state, info = cpu_boundary(batch, torch, common)
    need(state['input_ids'].shape[1] <= 2048, 'INPUT_TOKEN_CAP')
    decoded = processor.tokenizer.decode(state['input_ids'][0].tolist(), skip_special_tokens=False, clean_up_tokenization_spaces=False)
    need(processor.tokenizer.encode(decoded, add_special_tokens=False) == state['input_ids'][0].tolist(), 'TOKEN_ROUNDTRIP')
    if video:
        need(state['video_grid_thw'].tolist() == [[6, 12, 18]] and int(state['video_grid_thw'].prod())//4 == 324, 'GRID_TOKEN_GATE')
        need(len(traces) == 1 and traces[0]['indices'] == list(positions) and traces[0]['fps'] == 1. and traces[0]['merge'] == 2, 'ACTUAL_COORDINATE_CALLBACK')
        expected = [(positions[j]+positions[j+1])/2 for j in range(0,12,2)]
        need(traces[0]['times'] == expected, 'ACTUAL_NATIVE_TIMES')
        need(re.findall(r'<([0-9]+\.[0-9]) seconds>', decoded) == [f'{v:.1f}' for v in expected], 'NATIVE_TIMECODE_TEXT')
    else:
        need(not any('pixel' in k or 'grid' in k for k in state), 'TEXT_ONLY_NO_VISUAL')
    info.update(callback=traces, stripped=re.sub(r'<[0-9]+\.[0-9] seconds>', '<TIME>', decoded), tokens=state['input_ids'].shape[1], wall=time.monotonic()-tick)
    return state, info


def runtime(root):
    cfg = read(Path(root)/'runtime-config.json')
    import numpy as np
    import torch
    import transformers
    from transformers import AutoProcessor
    need(torch.__version__ == '2.5.1' and transformers.__version__ == '4.57.6' and np.__version__ == '1.26.4', 'RUNTIME_VERSION')
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    p = AutoProcessor.from_pretrained(cfg['qwen'], local_files_only=True, trust_remote_code=False)
    index=read(Path(cfg['qwen'])/'model.safetensors.index.json')
    names=sorted(set(index['weight_map'].values()));weights=[]
    for name in names:
        need(Path(name).name==name,'WEIGHT_INDEX_PATH');st=(Path(cfg['qwen'])/name).stat()
        weights.append(dict(name=name,size=st.st_size,mtime_ns=st.st_mtime_ns))
    assets={name:sha((Path(cfg['qwen'])/name).read_bytes()) for name in ('config.json','generation_config.json','model.safetensors.index.json')}
    common = sha(packed(dict(processor_image=p.image_processor.to_dict(), processor_video=p.video_processor.to_dict(), tokenizer=p.tokenizer.backend_tokenizer.to_str(), chat=p.chat_template, versions=[torch.__version__, transformers.__version__, np.__version__], assets=assets,weight_stat_bindings=weights,generation=dict(greedy=True, max_new_tokens=64, seed=19, bf16=True, attention='sdpa', fresh=True,use_cache=True,num_beams=1))))
    return cfg, np, torch, p, common


def bootstrap(root):
    root = Path(root); cfg, np, torch, p, common = runtime(root)
    need(not torch.cuda.is_initialized(), 'CPU_BOOTSTRAP_CUDA')
    q = dict(question='What color is the plain surface?', options=['Gray','Red','Blue','Green','Yellow'])
    frame = np.full((12,192,288,3),128,dtype=np.uint8)
    results = []
    for positions in (U, list(range(12))):
        state, info = processor_input(p, q, frame, positions, torch, common); results.append(info)
    need(not torch.cuda.is_initialized(), 'CPU_BOOTSTRAP_CUDA')
    write(root/'bootstrap-result.json', dict(status='PASS', calls=2, cuda_initialized=False, results=results))


def prepare(root):
    root = Path(root); cfg = read(root/'coordinator-config.json')
    _, np, torch, processor, common = runtime(root)
    gray = np.full((12,192,288,3),128,dtype=np.uint8)
    audit = []; selected = []; all_questions = []; small_bytes = 0
    # Separate nongold projection: this process physically opens the mixed file,
    # but the lexical projector never decodes gold fields or unrelated rows.
    raw=Path(cfg['annotation']).read_bytes();small_bytes+=len(raw)
    need(len(raw)<=4*1024**2 and sha(raw)==cfg['annotation_sha256'],'ANNOTATION_SNAPSHOT')
    frozen_bytes={s['alias']:Path(s['nongold']).read_bytes() for s in cfg['sources']}
    wanted={s['uid']:{q['ordinal'] for q in json.loads(frozen_bytes[s['alias']])} for s in cfg['sources']}
    metadata,gold_decoded=projected_json(raw,wanted,{'question','options','task_type','question_type','category','image','images','image_path','question_image','question_images','auxiliary_images','image_url'})
    need(gold_decoded==0,'NONGOLD_GOLD_ISOLATION')
    write(root/'nongold-projection-receipt.json',dict(original_annotation_open_count=1,bytes=len(raw),gold_values_decoded=0,max_records_per_source=50,unselected_values_lexically_skipped=True))
    for src in cfg['sources']:
        b = frozen_bytes[src['alias']]; small_bytes += len(b)
        manifest = read(src['manifest']); need(sha(b) == manifest['question_sha'], 'NONGOLD_SNAPSHOT_MISMATCH')
        questions = json.loads(b); need(len(questions) <= 50, 'SOURCE_QUESTION_CAP')
        kept = []; exclusions = []
        for q in sorted(questions, key=lambda x: x['ordinal']):
            reason = qualify(q)
            original=metadata.get(src['uid'],{}).get(q['ordinal'],{})
            if original.get('question',q['question'])!=q['question'] or original.get('options',q['options'])!=q['options']:
                reason='SOURCE_QUESTION_JOIN'
            if any(original.get(k) for k in ('image','images','image_path','question_image','question_images','auxiliary_images','image_url')):
                reason='EXTERNAL_RESOURCE_FIELD'
            task=' '.join(str(original.get(k,'')) for k in ('task_type','question_type','category')).casefold()
            if any(x in task for x in ('temporal','ordering','duration','timestamp','timecode','chronolog')):
                reason='TIME_DEPENDENT_TASK_TYPE'
            if reason == 'ELIGIBLE_NONGOLD':
                # Actual CPU boundary length qualification, no labels or model answers.
                try:
                    _, info = processor_input(processor, q, gray, U, torch, common)
                except ValueError as e:
                    if str(e) == 'INPUT_TOKEN_CAP':
                        exclusions.append(dict(ordinal=q['ordinal'], reason='INPUT_TOKEN_CAP')); continue
                    raise
                kept.append(q)
            else:
                exclusions.append(dict(ordinal=q['ordinal'], reason=reason))
        media = Path(src['media']); st = media.stat()
        media_ok = st.st_size == manifest['video_size'] and st.st_mtime_ns == manifest['video_mtime_ns'] and st.st_size <= 16*1024**3
        audit.append(dict(source=src['alias'], original_count=len(questions), eligible=len(kept), exclusions=exclusions, media_qualified=media_ok))
        if len(selected) < 4 and media_ok and len(kept) >= 3:
            chosen = kept[:6]; selected.append(src)
            for q in chosen:
                all_questions.append(dict(source=src['alias'], ordinal=q['ordinal'], question=q['question'], options=q['options']))
    need(small_bytes <= 32*1024**2, 'SMALL_INPUT_CAP')
    write(root/'eligibility.json', dict(sources=audit, selected=[s['alias'] for s in selected], N=len(all_questions), nongold_bytes=small_bytes))
    need(len(selected) == 4 and 12 <= len(all_questions) <= 24, 'FOUR_SOURCE_GATE')
    need(sum(Path(s['media']).stat().st_size for s in selected) <= 32*1024**3, 'MEDIA_SIZE_TOTAL')
    queue = []
    for position in range(6):
        for src in selected:
            qs = [q for q in all_questions if q['source'] == src['alias']]
            if position < len(qs):
                q = dict(qs[position], id='Q'+str(len(queue)+1).zfill(2)); queue.append(q)
    write(root/'nongold-projected.json', queue)
    write(root/'source-selection.json', dict(aliases=[s['alias'] for s in selected], N=len(queue), n_s={s['alias']:sum(q['source']==s['alias'] for q in queue) for s in selected}))
    # UID/media mapping only for CPU extraction and the eventual isolated scorer.
    write(root/'selected-source-private.json', selected)
    write(root/'preparation-seal.json', dict(nongold_sha=sha((root/'nongold-projected.json').read_bytes()), source_selection_sha=sha((root/'source-selection.json').read_bytes()), code_sha=sha(Path(__file__).read_bytes()), no_gold_values=True))
    # Only specified legacy identity/config/status fields; never decode old predictions.
    old_ids=set();legacy_bytes=0;legacy_started=0;old_systems=[]
    for src in cfg['sources']:
        b=Path(src['old_attempt_index']).read_bytes();legacy_bytes+=len(b)
        need(legacy_bytes<=128*1024**2,'LEGACY_INDEX_CAP')
        for line in b.decode('utf-8').splitlines():
            for match in re.finditer(r'"(stage|identity|input_sha256|full_input_hash|full_input_sha256)"\s*:\s*("(?:[^"\\]|\\.)*")',line):
                field,value=match[1],json.loads(match[2])
                if field=='stage' and value in ('ATTEMPT','STARTED','GENERATE_INTENT'):legacy_started+=1
                elif field!='stage' and re.fullmatch('[a-f0-9]{64}',value):old_ids.add(value)
        tree=ast.parse((Path(src['legacy_root'])/'model_runner.py').read_text(encoding='utf-8-sig'))
        systems=[n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str) and any(isinstance(a,ast.Name) and a.id=='system' for a in n.targets)]
        need(systems and all(x!=SYSTEM for x in systems),'LEGACY_PROMPT_NONIDENTITY_NOT_PROVEN');old_systems.extend(systems)
    write(root/'legacy-identity-index.json',dict(identities=sorted(old_ids),bytes=legacy_bytes,started_records=legacy_started,legacy_system_template_differs=True,old_predictions_opened=0,source_count=6))


class Meter:
    def __init__(self, path, root, source):
        self.f = Path(path).open('rb'); self.root=Path(root); self.source=source
        self.state = read(self.root/'media-read-budget.json') if (self.root/'media-read-budget.json').exists() else dict(reserved=0,returned=0)
        self.reads=0; self.seeks=0
    def read(self, n=-1):
        need(n >= 0, 'UNBOUNDED_MEDIA_READ')
        need(self.state['reserved']+n <= 48*1024**3, 'MEDIA_READ_CAP')
        self.state['reserved'] += n; write(self.root/'media-read-budget.json',self.state,True)
        b=self.f.read(n); self.state['returned']+=len(b); self.reads+=1
        write(self.root/'media-read-budget.json',self.state,True); return b
    def seek(self, offset, whence=0):
        self.seeks+=1; return self.f.seek(offset,whence)
    def tell(self): return self.f.tell()
    def readable(self): return True
    def seekable(self): return True
    def close(self): self.f.close()


def cache(root, alias):
    root=Path(root); sources=read(root/'selected-source-private.json'); src=next(s for s in sources if s['alias']==alias)
    import av,numpy as np
    from PIL import Image
    need(av.__version__=='15.1.0' and np.__version__=='1.26.4','DECODER_VERSION')
    manifest=read(src['manifest']); prior=read(src['pts']); path=Path(src['media']); before=path.stat()
    need(before.st_size==manifest['video_size'] and before.st_mtime_ns==manifest['video_mtime_ns'],'MEDIA_SNAPSHOT')
    need(prior['status']=='CONTAINER_PACKET_PREFLIGHT_PASS' and prior['demux_eof'],'PTS_REFERENCE')
    frames=[];times=[];start=time.monotonic();decoded=0; meter=Meter(path,root,alias)
    try:
        with av.open(meter,mode='r',hwaccel=None,buffer_size=32768) as c:
            need(len(c.streams.video)==1,'VIDEO_STREAMS');s=c.streams.video[0];s.thread_count=4
            for target in np.linspace(prior['min_packet_pts_s'],prior['max_packet_pts_s']-.10,48):
                need(time.monotonic()-start<580,'CACHE_TIMEOUT')
                c.seek(int(target/float(s.time_base)),stream=s,backward=True,any_frame=False)
                found=False
                for f in c.decode(s):
                    decoded+=1;need(f.pts is not None and f.time_base is not None and 0<f.width<=4096 and 0<f.height<=2160,'FRAME_QUALIFICATION')
                    ts=float(f.pts*f.time_base)
                    if ts+1e-6<target:continue
                    need(math.isfinite(ts) and (not times or ts>times[-1]),'CANDIDATE_ORDER')
                    image=Image.fromarray(f.to_ndarray(format='rgb24')).resize((288,192),Image.Resampling.BICUBIC)
                    frames.append(np.array(image,dtype=np.uint8));times.append(ts);found=True;break
                need(found,'CANDIDATE_MISSING')
    finally:meter.close()
    after=path.stat();need((before.st_size,before.st_mtime_ns,before.st_ino,before.st_dev)==(after.st_size,after.st_mtime_ns,after.st_ino,after.st_dev),'MEDIA_CHANGED')
    a=np.stack(frames);need(a.shape==(48,192,288,3) and a.dtype==np.uint8 and times[-1]-times[0]>=1200,'CACHE_SHAPE_OR_COVERAGE')
    np.save(root/(alias+'-candidates.npy'),a,allow_pickle=False)
    write(root/(alias+'-cache-receipt.json'),dict(alias=alias,count=48,shape=list(a.shape),dtype=str(a.dtype),times=times,array_sha=sha(a.tobytes()),wall=time.monotonic()-start,decoded_frames=decoded,requested_seeks=48,interface_seeks=meter.seeks,pillow=Image.__version__,stat_unchanged=True))


def lock_gpu(root):
    import msvcrt
    cfg=read(Path(root)/'runtime-config.json'); handle=open(cfg['global_lock'],'r+b');handle.seek(0)
    msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
    k=C.WinDLL('kernel32',use_last_error=True);k.CreateMutexW.argtypes=[W.LPVOID,W.BOOL,W.LPCWSTR];k.CreateMutexW.restype=W.HANDLE
    k.CloseHandle.argtypes=[W.HANDLE];k.ReleaseMutex.argtypes=[W.HANDLE]
    h=k.CreateMutexW(None,True,cfg['legacy_mutex']);need(h and C.get_last_error()!=183,'GPU_MUTEX_CONFLICT')
    return handle,k,h


def telemetry():
    import subprocess
    p=subprocess.run(['nvidia-smi','--query-gpu=name,uuid,pci.bus_id,memory.free,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=8,check=True)
    rows=[x.strip().split(', ') for x in p.stdout.splitlines() if x.strip()]
    need(len(rows)==1 and len(rows[0])==5 and '3090' in rows[0][0],'GPU_DEVICE')
    need(float(rows[0][3])>=12288,'GPU_FREE_MEMORY')
    return dict(name=rows[0][0],uuid=rows[0][1],bus=rows[0][2],free_mib=float(rows[0][3]),util=float(rows[0][4]))


def infer(root):
    root=Path(root); cfg,np,torch,p,common=runtime(root)
    questions=read(root/'nongold-projected.json');selection=read(root/'source-selection.json');aliases=selection['aliases'];N=len(questions)
    arrays={a:np.load(root/(a+'-candidates.npy'),allow_pickle=False) for a in aliases}
    gray=np.full((12,192,288,3),128,dtype=np.uint8)
    file_lock,k,mutex=lock_gpu(root);gpu_start=None;generated=0;states={};logical=[];records={};image_count=text_count=0
    try:
        snap=telemetry();need(snap['uuid']==cfg['gpu_expected']['uuid'] and snap['bus'].lower().endswith(cfg['gpu_expected']['bus'].lower().split(':')[-2]+':'+cfg['gpu_expected']['bus'].split(':')[-1].lower()),'GPU_IDENTITY')
        write(root/'telemetry-first.json',snap)
        from transformers import SiglipModel,AutoProcessor,Qwen3VLForConditionalGeneration
        torch.manual_seed(19);torch.cuda.set_per_process_memory_fraction(18/24,0)
        gpu_start=time.monotonic();event(root,dict(stage='SIGLIP_LOAD_INTENT',relative=0,images=0,texts=0))
        sp=AutoProcessor.from_pretrained(cfg['siglip'],local_files_only=True,trust_remote_code=False)
        sm=SiglipModel.from_pretrained(cfg['siglip'],local_files_only=True,trust_remote_code=False,torch_dtype=torch.float32).to('cuda').eval()
        image_features=[];text_features=[]
        with torch.inference_mode():
            for offset in range(0,192,8):
                need(time.monotonic()-gpu_start<1740,'GPU_TIME')
                image_count+=8;event(root,dict(stage='IMAGE_ENCODE_INTENT',count=image_count,relative=time.monotonic()-gpu_start))
                images=[arrays[aliases[i//48]][i%48] for i in range(offset,offset+8)]
                feed=sp(images=images,return_tensors='pt');out=sm.get_image_features(**{a:b.to('cuda') for a,b in feed.items()})
                image_features.append(out.float().cpu().numpy());need(torch.cuda.max_memory_allocated()<=18*1024**3,'GPU_ALLOCATED_CAP')
            for offset in range(0,N,8):
                n=min(8,N-offset);text_count+=n;event(root,dict(stage='TEXT_ENCODE_INTENT',count=text_count,relative=time.monotonic()-gpu_start))
                feed=sp(text=[q['question'] for q in questions[offset:offset+n]],padding='max_length',truncation=True,return_tensors='pt')
                out=sm.get_text_features(**{a:b.to('cuda') for a,b in feed.items()});text_features.append(out.float().cpu().numpy())
        images=np.concatenate(image_features).reshape(4,48,-1);texts=np.concatenate(text_features)
        scores=cross_scores(images,texts,np);selectors=[[top12(scores[i,s]) for s in range(4)] for i in range(N)]
        sig_wall=time.monotonic()-gpu_start
        del sm,feed,out;gc.collect();torch.cuda.empty_cache()
        write(root/'selectors.json',dict(positions=selectors,image_count=image_count,text_count=text_count,question_only=True,cosine='CPU_FLOAT64_AFTER_FLOAT32',siglip_inclusive_wall=sig_wall))
        preparation_start=time.monotonic();members={};infos={}
        for qi,q in enumerate(questions):
            source_idx=aliases.index(q['source']);own=arrays[q['source']];top=selectors[qi][source_idx]
            for condition in CONDITIONS:
                if condition.startswith('G') and condition!='GU':frame=gray;positions=selectors[qi][int(condition[1])-1]
                elif condition=='GU':frame=gray;positions=U
                elif condition=='Q':frame=None;positions=None
                elif condition in ('UO','UR'):frame=own[U];positions=U
                else:frame=own[top];positions=top if condition=='SO' else U
                state,info=processor_input(p,q,frame,positions,torch,common)
                identity=info['identity'];states.setdefault(identity,state);infos[(qi,condition)]=info
                members[(qi,condition)]=identity
            need(members[qi,'UO']==members[qi,'UR'],'UNIFORM_INPUT_NOT_IDENTICAL')
            for family in (['G1','G2','G3','G4','GU'],['SO','SR']):
                left=states[members[qi,family[0]]];base_info=infos[qi,family[0]]
                for c in family[1:]:
                    need(exact_equal(left,states[members[qi,c]],torch,['pixel_values_videos','video_grid_thw']),'CONTROL_VISUAL_DIFFERENCE')
                    need(base_info['stripped']==infos[qi,c]['stripped'],'NON_COORDINATE_TEXT_DIFFERENCE')
            order=CONDITIONS[qi%10:]+CONDITIONS[:qi%10]
            for c in order:logical.append(dict(question=qi,source=q['source'],condition=c,identity=members[qi,c]))
        need(any(len({members[i,'G'+str(s)] for s in range(1,5)})>1 for i in range(N)),'NO_G_INTERVENTION')
        unique=list(dict.fromkeys(x['identity'] for x in logical));need(len(unique)<=9*N<=216,'PHYSICAL_CAP')
        legacy=read(root/'legacy-identity-index.json');blocked=set(unique)&set(legacy['identities'])
        frozen=dict(logical=logical,unique=unique,legacy_unavailable=sorted(blocked),common=common,info=[dict(question=i,condition=c,**info) for (i,c),info in infos.items()],code_sha=sha(Path(__file__).read_bytes()),nongold_sha=sha((root/'nongold-projected.json').read_bytes()),generation=dict(max_new_tokens=64,greedy=True,seed=19,fresh_context=True),preparation_wall=time.monotonic()-preparation_start)
        write(root/'input-queue-seal.json',frozen)
        snap=telemetry();need(snap['uuid']==cfg['gpu_expected']['uuid'],'GPU_IDENTITY');write(root/'telemetry-qwen.json',snap)
        need(time.monotonic()-gpu_start<1700,'GPU_REMAINING_BEFORE_QWEN')
        event(root,dict(stage='QWEN_LOAD_INTENT',relative=time.monotonic()-gpu_start))
        model=Qwen3VLForConditionalGeneration.from_pretrained(cfg['qwen'],torch_dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).to('cuda').eval()
        eos=model.generation_config.eos_token_id;eos=[eos] if isinstance(eos,int) else list(eos)
        timing=dict(step=0,prefill=0.,decode=0.,tick=0.)
        def before_forward(module,args):
            torch.cuda.synchronize();timing['tick']=time.monotonic()
        def after_forward(module,args,value):
            torch.cuda.synchronize();elapsed=time.monotonic()-timing['tick']
            timing['prefill' if timing['step']==0 else 'decode']+=elapsed;timing['step']+=1
        pre_hook=model.register_forward_pre_hook(before_forward);post_hook=model.register_forward_hook(after_forward)
        for identity in unique:
            if identity in blocked:continue
            need(time.monotonic()-gpu_start<1740,'GPU_TIME')
            generated+=1;event(root,dict(stage='GENERATE_INTENT',ordinal=generated,identity=identity,relative=time.monotonic()-gpu_start))
            batch={a:b.to('cuda') if torch.is_tensor(b) else b for a,b in states[identity].items()};tick=time.monotonic();timing.update(step=0,prefill=0.,decode=0.)
            with torch.inference_mode():result=model.generate(**batch,do_sample=False,max_new_tokens=64,use_cache=True,num_beams=1)
            new=result[0,batch['input_ids'].shape[1]:];tokens=new.tolist();text=p.tokenizer.decode(tokens,skip_special_tokens=True).strip()
            ended=bool(tokens) and tokens[-1] in eos;valid=ended and text in tuple('ABCDE')
            rec=dict(identity=identity,state='VALID' if valid else 'INVALID',prediction=text if valid else None,eos=ended,generated_tokens=len(tokens),wall=time.monotonic()-tick,prefill_first_forward_wall=timing['prefill'],decode_forward_wall=timing['decode'],forward_steps=timing['step'])
            records[identity]=rec;event(root,dict(stage='GENERATE_RETURNED',**rec))
            write(root/'predictions-current-private.json',records,True)
            need(torch.cuda.max_memory_allocated()<=18*1024**3,'GPU_ALLOCATED_CAP')
        peak=torch.cuda.max_memory_allocated();pre_hook.remove();post_hook.remove();del model,batch,result,new;gc.collect();torch.cuda.empty_cache()
        write(root/'inference-complete.json',dict(status='ALL_NEW_GENERATIONS_RETURNED',generate_attempts=generated,returns=len(records),logical=len(logical),unique=len(unique),GPU_wall_to_unload=time.monotonic()-gpu_start,peak_allocated=peak,image_count=image_count,text_count=text_count))
    except Exception as e:
        write(root/'inference-failure.json',dict(type=type(e).__name__,diagnostic=str(e)[:1500],generate_attempts=generated,returns=len(records),image_count=image_count,text_count=text_count,GPU_elapsed=None if gpu_start is None else time.monotonic()-gpu_start))
    finally:
        k.ReleaseMutex(mutex);k.CloseHandle(mutex)
        import msvcrt
        file_lock.seek(0);msvcrt.locking(file_lock.fileno(),msvcrt.LK_UNLCK,1);file_lock.close()


def aggregate(questions, source_aliases, slots):
    per_source={};unknown=False
    for source in source_aliases:
        ids=[i for i,q in enumerate(questions) if q['source']==source];n=len(ids);arms={}
        for c in CONDITIONS:
            vals=[slots[i,c] for i in ids];known=all(v['correct'] is not None for v in vals)
            arms[c]=dict(N=n,correct=None if not known else sum(v['correct'] for v in vals),counts={state:sum(v['state']==state for v in vals) for state in ('VALID_CORRECT','VALID_WRONG','INVALID','FAILED','NOT_RUN','SCORING_UNKNOWN')})
        unknown=unknown or any(arms[c]['correct'] is None for c in CONDITIONS)
        ds=[];inter=[];pairs=dict(correction=0,harm=0,both_correct=0,both_wrong=0,unknown=0)
        own=source_aliases.index(source)+1
        for i in ids:
            g=[slots[i,'G'+str(s)]['correct'] for s in range(1,5)]
            ds.append(None if None in g else Fraction(g[own-1])-Fraction(sum(g[j] for j in range(4) if j!=own-1),3))
            vals=[slots[i,c]['correct'] for c in ('UO','UR','SO','SR')]
            inter.append(None if None in vals else Fraction((vals[2]-vals[0])-(vals[3]-vals[1])))
            so,sr=vals[2:];label='unknown' if so is None or sr is None else 'both_correct' if so and sr else 'correction' if so else 'harm' if sr else 'both_wrong';pairs[label]+=1
        per_source[source]=dict(n=n,arms=arms,D=None if None in ds else sum(ds)/n,I=None if None in inter else sum(inter)/n,SO_SR_pairs=pairs)
    D=None if unknown else sum(x['D'] for x in per_source.values())/4
    I=None if unknown else sum(x['I'] for x in per_source.values())/4
    if unknown:decision='INCOMPLETE_OR_UNKNOWN'
    else:
        h1=D>=Fraction(2,25) and sum(x['D']>0 for x in per_source.values())>=3
        h2=abs(I)>=Fraction(1,20) and sum((x['I']>0)==(I>0) and x['I']!=0 for x in per_source.values())>=3
        decision='DEVELOPMENT_GO_TO_OWNER_REVIEW' if h1 and h2 else 'CHANNEL_ONLY' if h1 else 'REPRESENTATION_SENSITIVITY_ONLY' if h2 else 'STOP_CURRENT_HYPOTHESIS'
    # Missing/failed observations retain scores0 for known labels, but never yield GO.
    incomplete=any(v['state'] in ('FAILED','NOT_RUN','SCORING_UNKNOWN') for v in slots.values())
    for item in per_source.values():
        for name in ('D','I'):
            item[name+'_exact']=None if item[name] is None else str(item[name]);item[name]=None if item[name] is None else float(item[name])
    return dict(per_source=per_source,D=None if D is None else float(D),I=None if I is None else float(I),D_exact=None if D is None else str(D),I_exact=None if I is None else str(I),decision='INCOMPLETE_OR_UNKNOWN' if incomplete else decision,complete=not incomplete)


def score(root):
    root=Path(root);cfg=read(root/'coordinator-config.json');closure=read(root/'infer-phase.json')
    need(closure['active']==0,'MODELS_NOT_EXITED')
    questions=read(root/'nongold-projected.json');selection=read(root/'source-selection.json')
    originals=read(root/'selected-source-private.json');uids={s['alias']:s['uid'] for s in originals}
    raw=Path(cfg['annotation']).read_bytes();need(len(raw)<=4*1024**2 and sha(raw)==cfg['annotation_sha256'],'GOLD_SNAPSHOT')
    wanted={}
    for q in questions:wanted.setdefault(uids[q['source']],set()).add(q['ordinal'])
    data,gold_decoded=projected_json(raw,wanted,{'correct_answer_label','question','options'})
    need(gold_decoded<=24,'GOLD_VALUE_CAP')
    queue=read(root/'input-queue-seal.json');pred=read(root/'predictions-current-private.json') if (root/'predictions-current-private.json').exists() else {}
    started={x['identity'] for x in [json.loads(line) for line in (root/'049-call-ledger.jsonl').read_text().splitlines()] if x['stage']=='GENERATE_INTENT'}
    bindings={(r['question'],r['condition']):r['identity'] for r in queue['logical']};slots={}
    for i,q in enumerate(questions):
        try:
            original=data[uids[q['source']]][q['ordinal']]
            label=original['correct_answer_label'];label=str(label).strip().upper();need(label in tuple('ABCDE'),'GOLD_ENCODING')
            need(original.get('question',q['question'])==q['question'],'GOLD_QUESTION_JOIN')
            need(original.get('options',q['options'])==q['options'],'GOLD_OPTIONS_JOIN')
        except Exception:label=None
        for condition in CONDITIONS:
            r=pred.get(bindings[i,condition]);state=('FAILED' if bindings[i,condition] in started else 'NOT_RUN') if r is None else r['state']
            if label is None:correct=None;state='SCORING_UNKNOWN'
            else:
                correct=int(r is not None and r['state']=='VALID' and r['prediction']==label)
                if state=='VALID':state='VALID_CORRECT' if correct else 'VALID_WRONG'
            slots[i,condition]=dict(state=state,correct=correct)
    result=aggregate(questions,selection['aliases'],slots)
    result.update(N=len(questions),logical_cells=10*len(questions),actual_recorded_predictions=len(pred),source_count=4,gold_open_count=1,gold_values_decoded=gold_decoded,gold_bytes=len(raw),status='FULL_DEVELOPMENT_COMPARISON' if result['complete'] else 'INCOMPLETE_OR_UNKNOWN',novelty='RETAIN0',development_only=True)
    write(root/'score-private.json',dict(result=result,slots=[dict(question=i,condition=c,**r) for (i,c),r in slots.items()]))


if __name__=='__main__':
    role,folder,*other=sys.argv[1:]
    if role=='bootstrap':bootstrap(folder)
    elif role=='prepare':prepare(folder)
    elif role=='cache':cache(folder,other[0])
    elif role=='infer':infer(folder)
    elif role=='score':score(folder)
    else:raise ValueError('ROLE')
