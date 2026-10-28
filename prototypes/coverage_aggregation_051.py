"""051 F48 vs complementary-view plurality. No media decode or SigLIP.

Separate binding/scoring roles see the annotation path. The inference role
receives only anonymous nongold, four exact arrays, and closed natural outputs.
"""
import ctypes as C
from ctypes import wintypes as W
from fractions import Fraction as F
import gc
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time

import selection_channel_049 as api049
from hourvideo_mcq_schema_051 import bind_original_nongold

OLD_SOURCE_SHA = 'e24bb6fa4ff1285900cbbbeeda4bccb0e1bbddd9f1a849693db722899f6272d1'
ARMS = ['F48','P0','P1','P2','P3']
BASES = ['SO','UO','UR','SR']


def need(ok, code):
    if not ok: raise ValueError(code)


def sha(b): return hashlib.sha256(b).hexdigest()
def pack(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def read(p): return json.loads(Path(p).read_bytes())


def write(p,x,replace=False):
    p=Path(p);b=pack(x);need(len(b)<16*1024**2,'RECEIPT_CAP')
    q=p.with_name(p.name+'.writing') if replace else p
    with q.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
    if replace:os.replace(q,p)


def event(root,x):
    with (Path(root)/'051-call-ledger.jsonl').open('ab') as h:
        h.write(pack(x)+b'\n');h.flush();os.fsync(h.fileno())


class JSONView:
    """Skip unselected serialized values without decoding their contents."""
    def __init__(self,b): self.s=b.decode('utf-8-sig');self.n=len(self.s)
    def ws(self,p):
        while p<self.n and self.s[p] in ' \n\r\t':p+=1
        return p
    def string_end(self,p):
        need(self.s[p]=='"','JSON_STRING');p+=1
        while p<self.n:
            if self.s[p]=='\\':p+=2
            elif self.s[p]=='"':return p+1
            else:p+=1
        raise ValueError('JSON_STRING_EOF')
    def skip(self,p):
        p=self.ws(p);need(p<self.n,'JSON_EOF');s=self.s
        if s[p]=='"':return self.string_end(p)
        if s[p]=='{':
            p=self.ws(p+1)
            if s[p]=='}':return p+1
            while True:
                p=self.ws(self.string_end(p));need(s[p]==':','JSON_COLON');p=self.ws(self.skip(p+1))
                if s[p]=='}':return p+1
                need(s[p]==',','JSON_COMMA');p=self.ws(p+1)
        if s[p]=='[':
            p=self.ws(p+1)
            if s[p]==']':return p+1
            while True:
                p=self.ws(self.skip(p))
                if s[p]==']':return p+1
                need(s[p]==',','JSON_COMMA');p=self.ws(p+1)
        end=p
        while end<self.n and s[end] not in ',]} \t\r\n':end+=1
        token=s[p:end]
        need(token in ('true','false','null','NaN','Infinity','-Infinity') or re.fullmatch(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?',token),'JSON_TOKEN')
        return end
    def members(self,p=0):
        p=self.ws(p);need(self.s[p]=='{','JSON_OBJECT');p=self.ws(p+1);seen=set()
        if self.s[p]=='}':return
        while True:
            e=self.string_end(p);key=json.loads(self.s[p:e]);need(key not in seen,'JSON_DUPLICATE');seen.add(key)
            p=self.ws(e);need(self.s[p]==':','JSON_COLON');a=self.ws(p+1);b=self.skip(a)
            yield key,a,b
            p=self.ws(b)
            if self.s[p]=='}':return
            need(self.s[p]==',','JSON_COMMA');p=self.ws(p+1)
    def elements(self,p):
        p=self.ws(p);need(self.s[p]=='[','JSON_ARRAY');p=self.ws(p+1)
        if self.s[p]==']':return
        while True:
            e=self.skip(p);yield p,e;p=self.ws(e)
            if self.s[p]==']':return
            need(self.s[p]==',','JSON_COMMA');p=self.ws(p+1)
    def atom(self,a,b):
        return json.loads(self.s[a:b],parse_constant=lambda _:(_ for _ in ()).throw(ValueError('RETAINED_NONFINITE')))
    def fields(self,p,names):return {k:self.atom(a,b) for k,a,b in self.members(p) if k in names}


def bind_display(row,q):
    return bind_original_nongold(row,q['question'],q['options'])


def safe_file(p,limit):
    p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=limit,'INPUT_TYPE_OR_SIZE')
    for n in [p,*p.parents]:
        a=n.lstat();need(not stat.S_ISLNK(a.st_mode) and not getattr(a,'st_file_attributes',0)&1024,'INPUT_REPARSE')
    return s


def positions(arm): return list(range(48)) if arm=='F48' else list(range(int(arm[1]),48,4))


def plurality(records):
    valid=[(j,r['prediction']) for j,r in enumerate(records) if r and r.get('state')=='VALID' and r.get('eos') and r.get('prediction') in tuple('ABCDE')]
    if not valid:return dict(state='INVALID',prediction=None,valid_votes=0,tied=False)
    counts={v:sum(x==v for _,x in valid) for _,v in valid};best=max(counts.values());tied={v for v,n in counts.items() if n==best}
    winner=next(v for _,v in valid if v in tied)
    return dict(state='VALID',prediction=winner,eos=True,valid_votes=len(valid),tied=len(tied)>1)


def bind(root):
    root=Path(root);cfg=read(root/'coordinator-config.json');old=Path(cfg['old_root'])
    need(sha(Path(api049.__file__).read_bytes())==OLD_SOURCE_SHA,'OLD_CODE_IDENTITY')
    names=['runtime-config.json','coordinator-config.json','source-selection.json','nongold-projected.json','selected-source-private.json','preparation-seal.json','input-queue-seal.json','inference-complete.json','infer-phase.json','score-private.json','independent-review.json','legacy-identity-index.json','049-call-ledger.jsonl','predictions-current-private.json']
    total=sum(safe_file(old/name,32*1024**2).st_size for name in names);need(total<=32*1024**2,'METADATA_TOTAL_CAP')
    hashes={name:sha((old/name).read_bytes()) for name in names if name not in ('predictions-current-private.json','score-private.json','049-call-ledger.jsonl')}
    questions=read(old/'nongold-projected.json');selection=read(old/'source-selection.json');queue=read(old/'input-queue-seal.json');done=read(old/'inference-complete.json');phase=read(old/'infer-phase.json');prior=read(old/'preparation-seal.json');closed=read(old/'independent-review.json')
    need(len(questions)==24 and len(selection['aliases'])==4 and len(set(selection['aliases']))==4,'FIXED_COHORT')
    need(all(re.fullmatch('[A-Za-z0-9_-]+',s) for s in selection['aliases']),'SAFE_ALIAS')
    need([q['id'] for q in questions]==['Q'+str(i+1).zfill(2) for i in range(24)],'QUESTION_ORDER')
    need(all(sum(q['source']==s for q in questions)==6 for s in selection['aliases']),'SOURCE_DENOMINATOR')
    need(done['logical']==240 and done['returns']==done['generate_attempts']==216 and phase['active']==0 and phase['exitcode']==0 and closed['status']=='PASS','OLD_EXECUTION_NOT_CLOSED')
    need(queue['code_sha']==OLD_SOURCE_SHA and queue['nongold_sha']==sha((old/'nongold-projected.json').read_bytes())==prior['nongold_sha'],'OLD_INPUT_BINDING')
    need(len(queue['logical'])==240 and len(queue['unique'])==216,'OLD_QUEUE')
    source_map=read(old/'selected-source-private.json');uids={s['alias']:s['uid'] for s in source_map};wanted={}
    for q in questions:wanted.setdefault(uids[q['source']],set()).add(q['ordinal'])
    safe_file(cfg['annotation'],4*1024**2)
    b=Path(cfg['annotation']).read_bytes();need(len(b)<=4*1024**2 and sha(b)==cfg['annotation_sha256'],'ANNOTATION_SNAPSHOT')
    original_bytes=len(b)
    originals,decoded=api049.projected_json(b,wanted,{'question','mcq_test'});need(decoded==0,'NONGOLD_GOLD_ISOLATION')
    schemas={}
    for q in questions:
        row=originals[uids[q['source']]][q['ordinal']]
        try:bound=bind_display(row,q)
        except ValueError as e:
            write(root/'input-binding-failure.json',dict(reason=str(e),question_id=q['id'],original_question_present='question' in row,question_type=type(row.get('question')).__name__,mcq_test_present='mcq_test' in row,mcq_test_type=type(row.get('mcq_test')).__name__,nongold_opens=1,gold_values_decoded=0));raise
        schemas[q['id']]={k:bound[k] for k in ('schema','parse_mode','option_order','frozen_option_boundary_normalization_count','interior_normalization')}
    natural=[x for x in queue['logical'] if x['condition'] in BASES];needed={x['identity'] for x in natural}
    doc=JSONView((old/'predictions-current-private.json').read_bytes());pred={k:doc.atom(a,b) for k,a,b in doc.members() if k in needed}
    need(set(pred)==needed,'BASELINE_RESULT_MISSING')
    for identity,r in pred.items():need(r['identity']==identity and r['state']=='VALID' and r['eos'] and r['prediction'] in tuple('ABCDE'),'BASELINE_NOT_CANONICAL_CLOSED')
    old_correct={};doc=JSONView((old/'score-private.json').read_bytes())
    for key,a,b in doc.members():
        if key!='slots':continue
        for x,y in doc.elements(a):
            attrs=doc.fields(x,{'question','condition'})
            if attrs['condition'] in BASES:
                row=doc.fields(x,{'question','condition','correct','state'});need(row['correct'] in (0,1) and row['state'] in ('VALID_CORRECT','VALID_WRONG'),'OLD_DERIVED_SCORE_UNKNOWN')
                identity=str(row['question'])+':'+row['condition'];need(identity not in old_correct,'OLD_DUPLICATE_DERIVED_SLOT');old_correct[identity]=row['correct']
    need(set(old_correct)=={str(i)+':'+c for i in range(24) for c in BASES},'BASELINE_DERIVED_DENOMINATOR')
    starts=set();returns=set()
    for line in (old/'049-call-ledger.jsonl').read_bytes().splitlines():
        view=JSONView(line);meta=view.fields(0,{'stage','identity'})
        if meta['stage']=='GENERATE_INTENT':need(meta['identity'] not in starts,'OLD_DUPLICATE_START');starts.add(meta['identity'])
        elif meta['stage']=='GENERATE_RETURNED':need(meta['identity'] not in returns,'OLD_DUPLICATE_RETURN');returns.add(meta['identity'])
    need(starts==returns==set(queue['unique']),'OLD_CALL_BINDING')
    caches=[]
    for alias in selection['aliases']:
        path=old/(alias+'-candidates.npy');s=safe_file(path,64*1024**2);safe_file(old/(alias+'-cache-receipt.json'),1024**2);receipt=read(old/(alias+'-cache-receipt.json'))
        need(receipt['count']==48 and receipt['shape']==[48,192,288,3] and receipt['dtype']=='uint8','OLD_CACHE_DECLARATION')
        caches.append(dict(alias=alias,path=str(path),bytes=s.st_size,array_sha=receipt['array_sha']))
    need(sum(c['bytes'] for c in caches)<=64*1024**2,'CACHE_PAYLOAD_TOTAL')
    write(root/'nongold.json',questions);write(root/'source-selection.json',selection)
    write(root/'source-map-private.json',dict(uids=uids,wanted={k:sorted(v) for k,v in wanted.items()},schemas=schemas))
    write(root/'old-natural-private.json',dict(logical=natural,predictions=pred,correct=old_correct,closed_hashes=sorted(starts)))
    write(root/'old-natural-worker.json',dict(predictions=pred,closed_hashes=sorted(starts)))
    write(root/'worker-input.json',dict(caches=caches,old_common=queue['common'],old_code_sha=OLD_SOURCE_SHA))
    write(root/'binding-receipt.json',dict(status='PASS',N=24,sources=4,old_logical=240,old_returns=216,natural_closed_records=len(pred),natural_logical=96,old_metadata_payload_bytes=total,cache_payload_bytes=sum(c['bytes'] for c in caches),original_nongold_file_opens=1,original_nongold_file_bytes=original_bytes,gold_values_decoded=0,schemas=schemas,original_file_hash=cfg['annotation_sha256'],old_metadata_hashes=hashes,nongold_sha=sha((root/'nongold.json').read_bytes())))


def finish_binding_receipt(root):
    """Finish the receipt-only shadowed-length failure without annotation reopen."""
    root=Path(root);phase=read(root/'bind-phase.json');log=(root/'bind.log').read_text(encoding='utf-8',errors='replace')
    need(phase['active']==0 and phase['exitcode']==1 and not phase['killed'] and 'TypeError: object of type' in log and "len(b)" in log and 'binding-receipt.json' in log,'EXACT_RECEIPT_FAILURE_REQUIRED')
    need(not (root/'binding-receipt.json').exists() and not (root/'input-binding-failure.json').exists(),'RECEIPT_ONLY_RECOVERY')
    cfg=read(root/'coordinator-config.json');questions=read(root/'nongold.json');selection=read(root/'source-selection.json');mapping=read(root/'source-map-private.json');natural=read(root/'old-natural-private.json');worker=read(root/'worker-input.json')
    need(len(questions)==24 and len(selection['aliases'])==4 and set(mapping['schemas'])=={q['id'] for q in questions},'COMPLETE_SAVED_BINDING')
    need(all(v['schema']=='official_mcq_test' and v['option_order']=='ABCDE' and not v['interior_normalization'] for v in mapping['schemas'].values()),'OFFICIAL_SAVED_BINDING')
    old=Path(cfg['old_root']);queue=read(old/'input-queue-seal.json');need(queue['nongold_sha']==sha((root/'nongold.json').read_bytes()) and len(queue['unique'])==216 and worker['old_common']==queue['common'],'SAVED_COHORT_IDENTITY')
    need(len(natural['logical'])==96 and len(natural['correct'])==96 and len(natural['closed_hashes'])==216,'SAVED_BASELINE_BINDING')
    size=safe_file(cfg['annotation'],4*1024**2).st_size
    write(root/'binding-receipt.json',dict(status='PASS',N=24,sources=4,old_logical=240,old_returns=216,natural_closed_records=len(natural['predictions']),natural_logical=96,cache_payload_bytes=sum(c['bytes'] for c in worker['caches']),original_nongold_file_opens=1,original_nongold_file_bytes=size,gold_values_decoded=0,schemas=mapping['schemas'],original_file_hash=cfg['annotation_sha256'],nongold_sha=sha((root/'nongold.json').read_bytes()),receipt_recovery=True,recovery_original_payload_opens=0,original_snapshot_check='PASSED_BEFORE_SAVED_24_BINDINGS',size_counter_evidence='RECOVERY_LSTAT_WITH_INITIAL_FROZEN_FULL_READ_SHA_MATCH',original_bind_phase_exit=1))


def native_input(p,q,array,indices,torch,common):
    from transformers.video_utils import VideoMetadata
    need(array.shape==(len(indices),192,288,3) and len(indices) in (12,48),'VIDEO_PAYLOAD')
    traces=[]
    def profile(frame,event,value):
        if frame.f_code.co_name!='_calculate_timestamps':return
        if event=='call':
            d=frame.f_locals;ix=d['indices'];traces.append(dict(indices=ix.tolist() if hasattr(ix,'tolist') else list(ix),fps=float(d['video_fps']),merge=d['merge_size']))
        elif event=='return' and traces:traces[-1]['times']=list(value)
    text=api049.template(p,q,True);metadata=VideoMetadata(total_num_frames=48,fps=1.,duration=48.,width=288,height=192,frames_indices=list(indices));tick=time.monotonic();sys.setprofile(profile)
    try:batch=p(text=[text],videos=[array],video_metadata=[metadata],do_sample_frames=False,do_resize=False,return_tensors='pt')
    finally:sys.setprofile(None)
    state,info=api049.cpu_boundary(batch,torch,common);expected_grid=[[len(indices)//2,12,18]];tokens=1296 if len(indices)==48 else 324
    need(set(state)=={'input_ids','attention_mask','pixel_values_videos','video_grid_thw'},'UNQUALIFIED_RETURNED_FIELDS')
    need(state['video_grid_thw'].tolist()==expected_grid and int(state['video_grid_thw'].prod())//4==tokens,'GRID_OR_TOKEN_GATE')
    need(state['input_ids'].dtype==state['attention_mask'].dtype==torch.int64 and state['pixel_values_videos'].dtype==torch.bfloat16,'INPUT_DTYPES')
    need(state['input_ids'].shape[1]<=4096,'INPUT_LENGTH')
    need(len(traces)==1 and traces[0]['indices']==list(indices) and traces[0]['fps']==1. and traces[0]['merge']==2,'ACTUAL_NATIVE_CALLBACK')
    expected=[(indices[j]+indices[j+1])/2 for j in range(0,len(indices),2)]
    need(traces[0]['times']==expected,'ACTUAL_NATIVE_TIMES')
    decoded=p.tokenizer.decode(state['input_ids'][0].tolist(),skip_special_tokens=False,clean_up_tokenization_spaces=False)
    need(re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded)==[f'{t:.1f}' for t in expected],'NATIVE_TIMECODE_TEXT')
    need(p.tokenizer.encode(decoded,add_special_tokens=False)==state['input_ids'][0].tolist(),'TOKEN_ROUNDTRIP')
    info.update(indices=indices,grid=expected_grid,visual_tokens=tokens,times=expected,roundtrip=True,tokens=state['input_ids'].shape[1],wall=time.monotonic()-tick)
    return state,info


def probe(root):
    root=Path(root);need(read(root/'binding-receipt.json')['status']=='PASS','BINDING_REQUIRED');cfg,np,torch,p,common=api049.runtime(root);expected=read(root/'worker-input.json')
    need(common==expected['old_common'],'MODEL_PROCESSOR_GENERATION_IDENTITY')
    need(not torch.cuda.is_initialized(),'CPU_PROBE_CUDA')
    q=dict(question='Which color covers the plain surface?',options=['Gray','Red','Blue','Green','Yellow']);rows=[]
    for arm in ('P0','F48'):
        ix=positions(arm);array=np.full((len(ix),192,288,3),128,dtype=np.uint8);state,info=native_input(p,q,array,ix,torch,common);rows.append(info)
    need(not torch.cuda.is_initialized(),'CPU_PROBE_CUDA')
    write(root/'probe-result.json',dict(status='PASS',calls=2,CUDA_initialized=False,rows=rows,common=common))


class CacheReader:
    def __init__(self,p,budget):self.f=Path(p).open('rb');self.budget=budget;self.returned=0;self.reads=0
    def read(self,n=-1):
        need(n>=0 and self.budget['reserved']+n<=64*1024**2,'CACHE_READ_CAP');self.budget['reserved']+=n
        b=self.f.read(n);self.returned+=len(b);self.budget['returned']+=len(b);self.reads+=1;return b
    def seek(self,n,whence=0):return self.f.seek(n,whence)
    def tell(self):return self.f.tell()
    def close(self):self.f.close()


def telemetry(root,name):
    root=Path(root);cfg=read(root/'runtime-config.json')
    p=subprocess.run(['nvidia-smi','--query-gpu=name,uuid,pci.bus_id,memory.free,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=8,check=True)
    rows=[x.strip().split(', ') for x in p.stdout.splitlines() if x.strip()]
    need(len(rows)==1 and len(rows[0])==5 and '3090' in rows[0][0],'GPU_DEVICE')
    r=dict(name=rows[0][0],uuid=rows[0][1],bus=rows[0][2],free_mib=float(rows[0][3]),util=float(rows[0][4]))
    need(r['uuid']==cfg['gpu_expected']['uuid'] and r['bus'].lower().split(':')[-2:]==cfg['gpu_expected']['bus'].lower().split(':')[-2:] and r['free_mib']>=18432,'GPU_IDENTITY_OR_FREE18')
    write(root/(name+'.json'),r);return r


def infer(root):
    root=Path(root);need(read(root/'binding-receipt.json')['status']=='PASS' and read(root/'probe-result.json')['status']=='PASS','CPU_ADMISSION_REQUIRED');cfg,np,torch,p,common=api049.runtime(root);inputs=read(root/'worker-input.json');questions=read(root/'nongold.json');old=read(root/'old-natural-worker.json')
    need(common==inputs['old_common'],'MODEL_PROCESSOR_GENERATION_IDENTITY')
    arrays={};budget=dict(reserved=0,returned=0);records={};attempts=0;gpu_start=None
    try:
        for c in inputs['caches']:
            meter=CacheReader(c['path'],budget)
            try:a=np.load(meter,allow_pickle=False)
            finally:meter.close()
            need(a.shape==(48,192,288,3) and a.dtype==np.uint8 and sha(a.tobytes())==c['array_sha'],'CACHE_CONTENT_BINDING')
            a.setflags(write=False);arrays[c['alias']]=a
        write(root/'cache-read-receipt.json',dict(**budget,payload_bytes=sum(c['bytes'] for c in inputs['caches']),file_reads=4,content_sha_matched=True))
        start=time.monotonic();logical=[];states={};info=[]
        for qi,q in enumerate(questions):
            by={}
            for arm in ARMS:
                ix=positions(arm);state,meta=native_input(p,q,arrays[q['source']][ix],ix,torch,common);identity=meta['identity'];states.setdefault(identity,state);by[arm]=identity;info.append(dict(question=qi,arm=arm,**meta))
            order=ARMS[qi%5:]+ARMS[:qi%5]
            logical.extend(dict(question=qi,source=q['source'],arm=arm,identity=by[arm]) for arm in order)
        unique=list(dict.fromkeys(x['identity'] for x in logical));need(len(unique)<=120,'GENERATE_CAP')
        reusable={i:old['predictions'][i] for i in unique if i in old['predictions']};blocked=set(unique)&set(old['closed_hashes'])-set(reusable)
        frozen=dict(logical=logical,unique=unique,info=info,common=common,nongold_sha=sha((root/'nongold.json').read_bytes()),code_sha=sha(Path(__file__).read_bytes()),schema_sha=sha(Path(__file__).with_name('hourvideo_mcq_schema_051.py').read_bytes()),test_sha=sha(Path(__file__).with_name('test_coverage_aggregation_051.py').read_bytes()),old_code_sha=OLD_SOURCE_SHA,reused=list(reusable),legacy_unavailable=sorted(blocked),CPU_full_input_preparation_wall=time.monotonic()-start,generation=dict(max_new_tokens=64,do_sample=False,use_cache=True,num_beams=1,seed=19,fresh_context=True))
        write(root/'input-queue-seal.json',frozen)
        need(not torch.cuda.is_initialized(),'CPU_PREPARATION_CUDA_INITIALIZED')
        telemetry(root,'telemetry-worker')
        from transformers import Qwen3VLForConditionalGeneration
        torch.manual_seed(19);torch.cuda.set_per_process_memory_fraction(18/24,0)
        gpu_start=time.monotonic();event(root,dict(stage='WEIGHT_LOAD_INTENT',relative=0))
        model=Qwen3VLForConditionalGeneration.from_pretrained(cfg['qwen'],torch_dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).to('cuda').eval()
        eos=model.generation_config.eos_token_id;eos=[eos] if isinstance(eos,int) else list(eos)
        timing=dict(step=0,prefill=0.,decode=0.,tick=0.)
        def pre(module,args):torch.cuda.synchronize();timing['tick']=time.monotonic()
        def post(module,args,value):
            torch.cuda.synchronize();timing['prefill' if timing['step']==0 else 'decode']+=time.monotonic()-timing['tick'];timing['step']+=1
        h0=model.register_forward_pre_hook(pre);h1=model.register_forward_hook(post)
        for identity in unique:
            if identity in blocked:continue
            if identity in reusable:
                records[identity]=dict(reusable[identity],origin='049_REUSED_CLOSED');continue
            need(attempts<120 and time.monotonic()-gpu_start<1140,'GPU_OR_GENERATE_CAP');attempts+=1
            event(root,dict(stage='GENERATE_INTENT',ordinal=attempts,identity=identity,relative=time.monotonic()-gpu_start))
            batch={k:v.to('cuda') if torch.is_tensor(v) else v for k,v in states[identity].items()};tick=time.monotonic();timing.update(step=0,prefill=0.,decode=0.)
            with torch.inference_mode():output=model.generate(**batch,do_sample=False,max_new_tokens=64,use_cache=True,num_beams=1)
            new=output[0,batch['input_ids'].shape[1]:];tokens=new.tolist();text=p.tokenizer.decode(tokens,skip_special_tokens=True).strip();ended=bool(tokens) and tokens[-1] in eos
            valid=ended and text in tuple('ABCDE')
            r=dict(identity=identity,state='VALID' if valid else 'INVALID',prediction=text if valid else None,eos=ended,generated_tokens=len(tokens),origin='051_NEW',wall=time.monotonic()-tick,prefill=timing['prefill'],decode=timing['decode'],forward_steps=timing['step'])
            records[identity]=r;event(root,dict(stage='GENERATE_RETURNED',**r));write(root/'predictions-private.json',records,True)
            need(torch.cuda.max_memory_allocated()<=18*1024**3,'ALLOCATED_CAP')
        peak=torch.cuda.max_memory_allocated();h0.remove();h1.remove();del model,batch,output,new;gc.collect();torch.cuda.empty_cache()
        write(root/'inference-complete.json',dict(status='CLOSED',logical=120,unique=len(unique),new_attempts=attempts,new_returns=sum(r['origin']=='051_NEW' for r in records.values()),reused=len(reusable),blocked=len(blocked),peak_allocated=peak,weight_intent_to_unload=time.monotonic()-gpu_start))
    except Exception as e:
        write(root/'inference-failure.json',dict(type=type(e).__name__,diagnostic=str(e)[:1600],attempts=attempts,returned=len(records),GPU_elapsed=None if gpu_start is None else time.monotonic()-gpu_start))


def paired(a,b):
    out=dict(correction=0,harm=0,both_correct=0,both_wrong=0,unknown=0)
    for x,y in zip(a,b):out['unknown' if x is None or y is None else 'both_correct' if x and y else 'correction' if x else 'harm' if y else 'both_wrong']+=1
    return out


def aggregate(questions,aliases,slots,diagnostics,baseline_ok,execution_complete):
    conditions=ARMS+['V4']+BASES+['O4','O5'];sources={};unknown=False
    for source in aliases:
        ids=[i for i,q in enumerate(questions) if q['source']==source];n=len(ids);arms={}
        for c in conditions:
            rows=[slots[i,c] for i in ids];values=[r['correct'] for r in rows]
            arms[c]=dict(N=n,correct=None if None in values else sum(values),counts={state:sum(r['state']==state for r in rows) for state in ('VALID_CORRECT','VALID_WRONG','INVALID','FAILED','NOT_RUN','SCORING_UNKNOWN')},kind='FINITE_ORACLE_NOT_DEPLOYABLE' if c.startswith('O') else '049_READ_ONLY_BASELINE' if c in BASES else '051_VOTE_NO_GENERATION' if c=='V4' else '051_GENERATED')
        pairs={name:paired([slots[i,a]['correct'] for i in ids],[slots[i,b]['correct'] for i in ids]) for name,a,b in [('F48_SO','F48','SO'),('V4_SO','V4','SO'),('V4_F48','V4','F48')]}
        delta={c:None if arms[c]['correct'] is None or arms['SO']['correct'] is None else F(arms[c]['correct']-arms['SO']['correct'],n) for c in ('F48','V4')}
        unknown=unknown or any(v['correct'] is None for v in arms.values())
        sources[source]=dict(n=n,arms=arms,pairs=pairs,net_vs_SO_exact={c:None if d is None else str(d) for c,d in delta.items()},diagnostics={k:None if any(diagnostics[i][k] is None for i in ids) else sum(diagnostics[i][k] for i in ids) for k in ('full_only','split_only','split_only_recovered_by_vote','vote_missed','all_five_wrong')})
    gates={}
    for c in ('F48','V4'):
        ds=[None if s['net_vs_SO_exact'][c] is None else F(s['net_vs_SO_exact'][c]) for s in sources.values()]
        mean=None if None in ds else sum(ds)/4;positive=None if None in ds else sum(x>0 for x in ds)
        gates[c]=dict(mean_net=None if mean is None else float(mean),mean_net_exact=None if mean is None else str(mean),positive_sources=positive,passed=None if unknown or not baseline_ok or not execution_complete else mean>=F(1,6) and positive>=3)
    incomplete=unknown or not baseline_ok or not execution_complete or any(r['state'] in ('FAILED','NOT_RUN','SCORING_UNKNOWN') for r in slots.values())
    decision='INCOMPLETE_OR_UNKNOWN' if incomplete else 'OBSERVED_HEADROOM / OWNER_REVIEW_REQUIRED' if any(g['passed'] for g in gates.values()) else 'NO_MATERIAL_DEPLOYABLE_GAIN'
    return dict(status='FULL_COVERAGE_AGGREGATION_COMPARISON' if not incomplete else 'INCOMPLETE_OR_UNKNOWN',N=len(questions),source_count=len(aliases),new_logical_cells=5*len(questions),per_source=sources,gates=gates,decision=decision,baseline_scoring_match=baseline_ok,execution_complete=execution_complete,novelty='RETAIN0')


def phase_costs(receipts,inner):
    need(receipts and len({r['role'] for r in receipts})==len(receipts),'COST_MISSING_OR_DUPLICATE')
    need(all(type(r['wall']) in (int,float) and math.isfinite(r['wall']) and r['wall']>=0 for r in receipts),'COST_DURATION')
    return dict(supervised_outer_wall_sum=sum(r['wall'] for r in receipts),CPU_supervised_wall=sum(r['wall'] for r in receipts if r['role']!='infer'),GPU_supervised_outer=sum(r['wall'] for r in receipts if r['role']=='infer'),contained_diagnostics=inner,inner_not_added_to_outer=True,end_to_end_parent_elapsed_from_separate_window=True)


def score(root):
    root=Path(root);cfg=read(root/'coordinator-config.json');phase=read(root/'infer-phase.json');need(phase['active']==0,'MODEL_JOB_NOT_EXITED')
    questions=read(root/'nongold.json');selection=read(root/'source-selection.json');mapping=read(root/'source-map-private.json');queue=read(root/'input-queue-seal.json');old=read(root/'old-natural-private.json')
    predictions=read(root/'predictions-private.json') if (root/'predictions-private.json').exists() else {}
    # Refuse protected scoring before any annotation open if the real-return,
    # completed Job and current input/code bindings are unavailable.
    ledger=[json.loads(s) for s in (root/'051-call-ledger.jsonl').read_text().splitlines()]
    returned=[r for r in ledger if r['stage']=='GENERATE_RETURNED'];intents=[r for r in ledger if r['stage']=='GENERATE_INTENT']
    need(phase['exitcode']==0 and not phase['killed'] and bool(returned),'NO_VERIFIED_REAL_RETURN')
    need(queue['code_sha']==sha(Path(__file__).read_bytes()) and queue['nongold_sha']==sha((root/'nongold.json').read_bytes()) and queue['schema_sha']==sha(Path(__file__).with_name('hourvideo_mcq_schema_051.py').read_bytes()) and queue['test_sha']==sha(Path(__file__).with_name('test_coverage_aggregation_051.py').read_bytes()),'CURRENT_SCORING_BINDING')
    need(len({r['identity'] for r in intents})==len(intents) and len({r['identity'] for r in returned})==len(returned),'CALL_DUPLICATE')
    started={r['identity'] for r in intents}
    need(all(r['identity'] in started and r['identity'] in queue['unique'] and all(predictions[r['identity']].get(k)==v for k,v in r.items() if k!='stage') for r in returned),'RAW_RETURN_BINDING')
    safe_file(cfg['annotation'],4*1024**2)
    raw=Path(cfg['annotation']).read_bytes();need(len(raw)<=4*1024**2 and sha(raw)==cfg['annotation_sha256'],'GOLD_SNAPSHOT')
    wanted={k:set(v) for k,v in mapping['wanted'].items()};gold,decoded=api049.projected_json(raw,wanted,{'question','mcq_test','correct_answer_label'});need(decoded<=24,'GOLD_COUNT_CAP')
    selected={(r['question'],r['arm']):r['identity'] for r in queue['logical']};old_selected={(r['question'],r['condition']):r['identity'] for r in old['logical']}
    slots={};diagnostics=[];vote_stats=[];baseline_mismatches=[]
    for i,q in enumerate(questions):
        try:
            row=gold[mapping['uids'][q['source']]][q['ordinal']];bound=bind_display(row,q)
            need({k:bound[k] for k in mapping['schemas'][q['id']]}==mapping['schemas'][q['id']],'STRICT_GOLD_JOIN')
            label=row['correct_answer_label'];need(type(label) is str and label.strip().upper() in tuple('ABCDE'),'GOLD_ENCODING');label=label.strip().upper()
        except Exception:label=None
        parts=[]
        for c in ARMS:
            identity=selected[i,c];r=predictions.get(identity)
            state=('FAILED' if identity in started else 'NOT_RUN') if r is None else r['state'];correct=None if label is None or r is None else int(r['state']=='VALID' and r['prediction']==label)
            if label is None:state='SCORING_UNKNOWN'
            elif state=='VALID':state='VALID_CORRECT' if correct else 'VALID_WRONG'
            slots[i,c]=dict(state=state,correct=correct)
            if c!='F48':parts.append(r)
        v=plurality(parts);vote_stats.append(dict(valid_votes=v['valid_votes'],tied=v['tied']))
        missing=any(r is None for r in parts)
        correct=None if label is None or missing else int(v['state']=='VALID' and v['prediction']==label)
        slots[i,'V4']=dict(state='SCORING_UNKNOWN' if label is None else 'NOT_RUN' if missing else 'VALID_CORRECT' if correct else 'VALID_WRONG' if v['state']=='VALID' else 'INVALID',correct=correct)
        for c in BASES:
            r=old['predictions'][old_selected[i,c]];correct=None if label is None else int(r['prediction']==label)
            slots[i,c]=dict(state='SCORING_UNKNOWN' if label is None else 'VALID_CORRECT' if correct else 'VALID_WRONG',correct=correct)
            if correct!=old['correct'][str(i)+':'+c]:baseline_mismatches.append(dict(question=i,condition=c))
        if label is None or any(slots[i,c]['correct'] is None for c in ARMS):
            for c in ('O4','O5'):slots[i,c]=dict(state='SCORING_UNKNOWN',correct=None)
            diagnostics.append({k:None for k in ('full_only','split_only','split_only_recovered_by_vote','vote_missed','all_five_wrong')})
        else:
            f=slots[i,'F48']['correct'];o4=int(any(slots[i,'P'+str(j)]['correct'] for j in range(4)));o5=int(f or o4);v4=slots[i,'V4']['correct']
            need(o5>=max(f,v4) and o4>=v4,'FINITE_ORACLE_BOUNDS')
            for c,value in [('O4',o4),('O5',o5)]:slots[i,c]=dict(state='VALID_CORRECT' if value else 'VALID_WRONG',correct=value)
            diagnostics.append(dict(full_only=int(f and not o4),split_only=int(not f and o4),split_only_recovered_by_vote=int(not f and o4 and v4),vote_missed=int(o4 and not v4),all_five_wrong=int(not o5)))
    completed=(root/'inference-complete.json').exists() and phase['exitcode']==0 and not phase['killed']
    result=aggregate(questions,selection['aliases'],slots,diagnostics,not baseline_mismatches,completed)
    result.update(gold_open_count=1,gold_bytes=len(raw),gold_values_decoded=decoded,baseline_mismatch_count=len(baseline_mismatches),vote_tie_questions=sum(v['tied'] for v in vote_stats),valid_vote_distribution={str(j):sum(v['valid_votes']==j for v in vote_stats) for j in range(5)},no_valid_vote_questions=sum(v['valid_votes']==0 for v in vote_stats))
    write(root/'score-private.json',dict(result=result,slots=[dict(question=i,condition=c,**s) for (i,c),s in slots.items()],diagnostics=diagnostics,vote_stats=vote_stats,baseline_mismatches=baseline_mismatches))


def supervise(root,role):
    """Current public Job wrapper; never executes the old task main."""
    root=Path(root);cfg=read(root/'coordinator-config.json');need(time.time()<cfg['deadline_epoch'],'PARENT_DEADLINE')
    path=Path(__file__).with_name('auditable_runner_040.py');b=path.read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='3e56faf30afea1bed850c085bceb2afcc4fb257c','PLATFORM_IDENTITY')
    spec=importlib.util.spec_from_file_location('platform040',path);platform=importlib.util.module_from_spec(spec);spec.loader.exec_module(platform)
    caps=dict(bind=120,bind_finalize=120,probe=120,suite=60,suite2=60,preflight_gpu=20,infer=1200,score=120,verify=60)
    prior=[read(p) for p in root.glob('*-phase.json')];used=sum(x['wall'] for x in prior if x['role']!='infer');cap=min(caps[role],cfg['deadline_epoch']-time.time(),1800-used if role!='infer' else 1200)
    need(cap>5 and not (root/(role+'-phase.json')).exists(),'PHASE_RESTART_OR_BUDGET')
    lock_file=mutex=kernel=None
    if role=='infer':lock_file,kernel,mutex=api049.lock_gpu(root)
    job=platform.Job(memory=32*1024**3,active_limit=4);limit=platform.Extended();need(job.api.QueryInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit),None),'JOB_QUERY');limit.basic.flags|=0x10;limit.basic.affinity=15;need(job.api.SetInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit)),'JOB_AFFINITY')
    script=Path(__file__).with_name('test_coverage_aggregation_051.py') if role in ('suite','suite2','verify') else Path(__file__)
    argv=[str(script.resolve()),'suite' if role=='suite2' else role,str(root)];env_visibility='0' if role=='infer' else ''
    bootstrap="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES="+repr(env_visibility)+",HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',DO_NOT_TRACK='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',HF_HOME="+repr(str(root/'hf'))+",TORCH_HOME="+repr(str(root/'torch'))+",XDG_CACHE_HOME="+repr(str(root/'cache'))+",TEMP="+repr(str(root))+",TMP="+repr(str(root))+");sys.path.insert(0,"+repr(cfg['site'])+");sys.path.insert(0,"+repr(str(Path(__file__).resolve().parent))+");sys.argv="+repr(argv)+";runpy.run_path(sys.argv[0],run_name='__main__')"
    start=time.monotonic();child=None;kill=None;empty=False
    try:
        child=platform.Process([cfg['python'],'-I','-S','-B','-c',bootstrap],root/(role+'.log'),job)
        while job.active():
            if time.monotonic()>=start+cap-4:kill=time.monotonic();job.kill();break
            time.sleep(.005)
        empty=job.empty(start+cap-1);need(empty,'OWN_JOB_EXIT_UNKNOWN')
        result=dict(role=role,start=start,active0=time.monotonic(),exitcode=child.poll(),kill=kill,**job.snapshot());result['wall']=time.monotonic()-start
        write(root/(role+'-phase.json'),result)
        print(json.dumps({k:result[k] for k in ('role','wall','active','exitcode','peak_commit','killed')}))
        tail=(root/(role+'.log')).read_text(encoding='utf-8',errors='replace')[-1600:];print(tail.encode('ascii','backslashreplace').decode())
    finally:
        if child:child.close()
        job.close()
        if mutex:
            if empty:kernel.ReleaseMutex(mutex)
            kernel.CloseHandle(mutex)
            import msvcrt
            lock_file.seek(0);msvcrt.locking(lock_file.fileno(),msvcrt.LK_UNLCK,1);lock_file.close()


if __name__=='__main__':
    role,folder,*extra=sys.argv[1:]
    if role=='launch':supervise(folder,extra[0])
    elif role=='bind':bind(folder)
    elif role=='bind_finalize':finish_binding_receipt(folder)
    elif role=='probe':probe(folder)
    elif role=='preflight_gpu':telemetry(folder,'telemetry-parent')
    elif role=='infer':infer(folder)
    elif role=='score':score(folder)
    else:raise ValueError('ROLE')
