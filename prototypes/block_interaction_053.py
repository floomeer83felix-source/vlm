"""Frozen 053 block-interaction development comparison; no old main invoked."""
import ctypes as C
from ctypes import wintypes as W
import csv
import gc
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
import selection_channel_049 as pure049
from hourvideo_mcq_schema_051 import bind_original_nongold

MIB=1024**2
METHODS=('F','M','A','I','C','R')
SINGLES=(1,2,4,8)
PAIRS=(3,5,6,9,10,12)
TRIPLES=(7,11,13,14)
OBS=(0,1,2,3,4,5,6,8,9,10,12,15)
LETTERS='ABCDE'
PREFIX='Answer:'
CONTINUATIONS=(' A',' B',' C',' D',' E')


def need(ok,reason):
    if not ok:raise ValueError(reason)


def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())


def write(p,x,replace=False):
    p=Path(p);b=pack(x);need(len(b)<=16*MIB,'OUTPUT_FILE_CAP');tmp=p.with_name(p.name+'.writing') if replace else p
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    if replace:os.replace(tmp,p)


def event(root,x):
    with (Path(root)/'053-call-ledger.jsonl').open('ab') as f:f.write(pack(x)+b'\n');f.flush();os.fsync(f.fileno())


def regular(p,cap):
    p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=cap,'FILE_TYPE_SIZE')
    for q in [p,*p.parents]:
        a=q.lstat();need(not stat.S_ISLNK(a.st_mode) and not getattr(a,'st_file_attributes',0)&1024,'FILE_REPARSE')
    return s


def metadata(root,path,parent):
    root=Path(root);path=Path(path);s=regular(path,2*MIB);budget=read(root/'read-budget.json');need(budget['metadata_returned']+s.st_size<=16*MIB,'METADATA_BUDGET')
    with path.open('rb') as f:b=f.read(s.st_size);after=os.fstat(f.fileno())
    budget['metadata_returned']+=len(b);budget['metadata_opens'].append(dict(parent=parent,name=path.name,bytes=len(b),role='prepare'));write(root/'read-budget.json',budget,True)
    need(len(b)==s.st_size and (s.st_ino,s.st_size,s.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns),'METADATA_CHANGED')
    return b


def top(v):
    finite(v);return max(range(5),key=lambda a:(v[a],-a))


def finite(v):need(isinstance(v,(list,tuple)) and len(v)==5 and all(type(x) in (int,float) and math.isfinite(x) for x in v),'NONFINITE_OR_MISSING_SCORE')
def margin(v,a):return v[a]-max(v[b] for b in range(5) if b!=a)
def bits(mask):return bin(mask).count('1')
def r_masks(qi):return tuple(sorted({15}|{1+((qi+k)%14) for k in range(12)}))


def estimate(obs,mask,interaction=True,override_full=True):
    if mask==15 and override_full:return list(obs[15])
    use=[i for i in range(4) if mask&(1<<i)];out=[]
    for a in range(5):
        value=obs[0][a]+sum(obs[1<<i][a]-obs[0][a] for i in use)
        if interaction:
            value+=sum(obs[(1<<i)|(1<<j)][a]-obs[1<<i][a]-obs[1<<j][a]+obs[0][a] for i,j in itertools.combinations(use,2))
        out.append(value)
    return out


def best(candidates):
    # Exact comparisons only: margin, more blocks, smaller integer mask, A first.
    return max(candidates,key=lambda x:(x['margin'],bits(x['mask']),-x['mask'],-x['a']))


def route(obs,method,qi):
    expected=set(r_masks(qi)) if method=='R' else set(OBS);need(set(obs)==expected,'POLICY_OBSERVATION_INTERFACE')
    required=(0,*SINGLES,15) if method=='A' else tuple(x for x in OBS if x) if method=='C' else tuple(expected)
    for mask in required:finite(obs[mask])
    candidates=[]
    if method in ('I','A'):
        for mask in range(1,16):
            v=estimate(obs,mask,method=='I')
            for a in range(5):candidates.append(dict(a=a,mask=mask,margin=margin(v,a)))
    else:
        for mask in sorted(expected-{0}):
            v=obs[mask];a=top(v);candidates.append(dict(a=a,mask=mask,margin=margin(v,a)))
    return best(candidates)


def gate(selection,full,first=None,second=None):
    f=top(full);a=selection['a'];mask=selection['mask'];g=margin(full,f)
    if a==f:return dict(a=f,reason='SAME_AS_F',changed=False,fallback=False)
    if mask==15:return dict(a=f,reason='FULL_REUSE',changed=False,fallback=True)
    finite(first);finite(second)
    tops=(top(first),top(second));margins=(margin(first,a),margin(second,a));accept=tops==(a,a) and min(margins)>g
    return dict(a=a if accept else f,reason='VERIFIED_CHANGE' if accept else 'VERIFICATION_REJECTED',changed=accept,fallback=not accept,fill_top_disagreement=tops[0]!=tops[1],both_fills_selected=tops==(a,a),first_margin=margins[0],second_margin=margins[1],full_margin=g)


def vote(single_scores):
    choices=[top(single_scores[m]) for m in SINGLES];counts={a:choices.count(a) for a in choices};maximum=max(counts.values());return next(a for a in choices if counts[a]==maximum)


def required(method,qi):
    return (15,) if method=='F' else SINGLES if method=='M' else (0,*SINGLES,15) if method=='A' else tuple(m for m in OBS if m) if method=='C' else OBS if method=='I' else r_masks(qi)


def prepare(root):
    root=Path(root);cfg=read(root/'coordinator-config.json');old52=Path(cfg['old52']);old51=Path(cfg['old51'])
    names52=('coordinator-config.json','classification-private.json','classification-seal.json','nongold-projection-private.json','analysis-receipt.json','classify-phase.json','analyze-phase.json','verify-phase.json')
    names51=('coordinator-config.json','runtime-config.json','nongold.json','source-selection.json','source-map-private.json','worker-input.json','input-queue-seal.json','inference-complete.json','infer-phase.json')
    raw52={n:metadata(root,old52/n,'052') for n in names52};raw51={n:metadata(root,old51/n,'051') for n in names51};d52={n:json.loads(b) for n,b in raw52.items()};d51={n:json.loads(b) for n,b in raw51.items()}
    q=d51['nongold.json'];selection=d51['source-selection.json'];mapping=d51['source-map-private.json'];worker=d51['worker-input.json'];oldq=d51['input-queue-seal.json'];cl=d52['classification-private.json'];seal=d52['classification-seal.json'];projection=d52['nongold-projection-private.json']['projection']
    need(len(q)==24 and len(selection['aliases'])==4 and [x['id'] for x in q]==['Q'+str(i+1).zfill(2) for i in range(24)],'FROZEN_COHORT')
    need(all(sum(x['source']==s for x in q)==6 for s in selection['aliases']),'FOUR_SOURCE_N')
    need(sha(raw52['classification-private.json'])==seal['classification_sha'] and sha(raw52['nongold-projection-private.json'])==seal['projection_sha'],'052_SEALS')
    need(sha(raw51['nongold.json'])==oldq['nongold_sha']==seal['nongold_sha'],'QUESTION_BYTE_IDENTITY')
    need(d52['coordinator-config.json']['annotation']==d51['coordinator-config.json']['annotation']==cfg['annotation'] and d52['coordinator-config.json']['annotation_sha256']==d51['coordinator-config.json']['annotation_sha256']==cfg['annotation_sha256'],'ORIGINAL_REFERENCE_IDENTITY')
    need(sha(Path(__file__).with_name('question_protocol_audit_052.py').read_bytes())=='7825e6e0b4b34c2b9ae2d4d6fd5326a63b3059f1dc92c79b81954c1e78758612','052_LF_SOURCE_IDENTITY')
    for data in (d52['classify-phase.json'],d52['analyze-phase.json'],d52['verify-phase.json'],d51['infer-phase.json']):need(data['active']==0 and data['exitcode']==0 and not data['killed'],'OLD_JOB_NOT_CLOSED')
    need(d51['inference-complete.json']['new_attempts']==d51['inference-complete.json']['new_returns']==120,'051_CLOSED_RETURNS')
    need(d52['analysis-receipt.json']['status']=='TASK_PROTOCOL_REVIEW_REQUIRED' and seal['status']=='PASS' and len(cl['rows'])==24,'052_CLOSURE')
    for i,x in enumerate(q):
        c=cl['rows'][i];need((c['question_index'],c['id'],c['source'],c['ordinal'])==(i,x['id'],x['source'],x['ordinal']),'052_INDEX_JOIN')
        original=projection[mapping['uids'][x['source']]][str(x['ordinal'])];bind_original_nongold(original,x['question'],x['options'])
    legacy_raw=metadata(root,old51/'old-natural-worker.json','051');legacy=select_top(legacy_raw,{'closed_hashes'})['closed_hashes'];historic=set(legacy)|set(oldq['unique']);need(all(type(x) is str and len(x)==64 for x in historic),'HISTORIC_IDENTITY_INDEX')
    need(len(worker['caches'])==4 and sum(x['bytes'] for x in worker['caches'])<=64*MIB,'CACHE_REFERENCE_BUDGET')
    for c in worker['caches']:need(regular(c['path'],64*MIB).st_size==c['bytes'],'CACHE_DECLARED_FILE_SIZE')
    model_questions=[{k:x[k] for k in ('id','source','ordinal','question','options')} for x in q]
    write(root/'nongold.json',model_questions);write(root/'source-selection.json',dict(aliases=selection['aliases']));write(root/'scoring-map-private.json',dict(uids=mapping['uids'],wanted=mapping['wanted']))
    write(root/'worker-input.json',dict(caches=worker['caches'],common=worker['old_common'],historic_hashes=sorted(historic),r_observations=[list(r_masks(i)) for i in range(24)]))
    write(root/'binding-receipt.json',dict(status='PASS',N=24,n_s={s:6 for s in selection['aliases']},old_metadata_identity_pass=True,scope_caveat_count=sum(c['protocol_class']=='OUTSIDE_049_TIME_SCOPE' for c in cl['rows']),gold_values_decoded=0,original_payload_opens=0,local_historic_hashes=len(historic),nongold_sha=sha(raw51['nongold.json']),code_sha=sha(Path(__file__).read_bytes())))


def select_top(raw,names):
    """Only decode requested top-level values; skip old predictions as text."""
    text=raw.decode('utf-8-sig');n=len(text)
    def ws(p):
        while p<n and text[p] in ' \r\n\t':p+=1
        return p
    def string(p):
        need(text[p]=='"','JSON_STRING');p+=1
        while p<n:
            if text[p]=='\\':p+=2
            elif text[p]=='"':return p+1
            else:p+=1
        raise ValueError('JSON_STRING_EOF')
    def skip(p):
        p=ws(p)
        if text[p]=='"':return string(p)
        if text[p] in '{[':
            obj=text[p]=='{';end='}' if obj else ']';p=ws(p+1)
            if text[p]==end:return p+1
            while True:
                if obj:p=ws(string(p));need(text[p]==':','JSON_COLON');p=ws(p+1)
                p=ws(skip(p))
                if text[p]==end:return p+1
                need(text[p]==',','JSON_COMMA');p=ws(p+1)
        end=p
        while end<n and text[end] not in ',]} \r\n\t':end+=1
        need(end>p,'JSON_ATOM');return end
    p=ws(0);need(text[p]=='{','JSON_OBJECT');p=ws(p+1);out={};seen=set()
    while text[p]!='}':
        end=string(p);key=json.loads(text[p:end]);need(key not in seen,'JSON_DUPLICATE');seen.add(key);p=ws(end);need(text[p]==':','JSON_COLON');a=ws(p+1);b=skip(a)
        if key in names:out[key]=json.loads(text[a:b],parse_constant=lambda _:(_ for _ in ()).throw(ValueError('RETAINED_NONFINITE')))
        p=ws(b)
        if text[p]=='}':break
        need(text[p]==',','JSON_COMMA');p=ws(p+1)
    need(ws(p+1)==n,'JSON_TRAILING');return out


def runtime(root):
    cfg=read(Path(root)/'runtime-config.json')
    import numpy as np
    import torch
    import transformers
    from transformers import AutoProcessor
    need((torch.__version__,transformers.__version__,np.__version__)==('2.5.1','4.57.6','1.26.4'),'RUNTIME_VERSION');torch.set_num_threads(1);torch.set_num_interop_threads(1)
    p=AutoProcessor.from_pretrained(cfg['qwen'],local_files_only=True,trust_remote_code=False);index=read(Path(cfg['qwen'])/'model.safetensors.index.json');weights=[]
    for name in sorted(set(index['weight_map'].values())):
        need(Path(name).name==name,'WEIGHT_STAT_BASENAME');s=(Path(cfg['qwen'])/name).stat();weights.append(dict(name=name,size=s.st_size,mtime_ns=s.st_mtime_ns))
    assets={name:sha((Path(cfg['qwen'])/name).read_bytes()) for name in ('config.json','generation_config.json','model.safetensors.index.json')}
    # Preserve historical fingerprint namespace to forbid mode-only replay.
    common=sha(pack(dict(processor_image=p.image_processor.to_dict(),processor_video=p.video_processor.to_dict(),tokenizer=p.tokenizer.backend_tokenizer.to_str(),chat=p.chat_template,versions=[torch.__version__,transformers.__version__,np.__version__],assets=assets,weight_stat_bindings=weights,generation=dict(greedy=True,max_new_tokens=64,seed=19,bf16=True,attention='sdpa',fresh=True,use_cache=True,num_beams=1))))
    need(common==read(Path(root)/'worker-input.json')['common'],'MODEL_PROCESSOR_TOKENIZER_IDENTITY');return cfg,np,torch,p,common


def native(p,q,array,torch,common):
    from transformers.video_utils import VideoMetadata
    need(array.shape==(48,192,288,3),'ARRAY_SHAPE');text=pure049.template(p,q,True)+PREFIX;trace=[]
    def profile(frame,event,value):
        if frame.f_code.co_name!='_calculate_timestamps':return
        if event=='call':
            d=frame.f_locals;ix=d['indices'];trace.append(dict(indices=ix.tolist() if hasattr(ix,'tolist') else list(ix),fps=float(d['video_fps']),merge=d['merge_size']))
        elif event=='return':trace[-1]['times']=list(value)
    meta=VideoMetadata(total_num_frames=48,fps=1.,duration=48.,width=288,height=192,frames_indices=list(range(48)));tick=time.monotonic();sys.setprofile(profile)
    try:batch=p(text=[text],videos=[array],video_metadata=[meta],do_sample_frames=False,do_resize=False,return_tensors='pt')
    finally:sys.setprofile(None)
    state,info=pure049.cpu_boundary(batch,torch,common);need(set(state)=={'input_ids','attention_mask','pixel_values_videos','video_grid_thw'},'ACTUAL_KWARGS')
    need(state['video_grid_thw'].tolist()==[[24,12,18]] and int(state['video_grid_thw'].prod())//4==1296,'NATIVE_GRID_TOKENS')
    need(state['input_ids'].dtype==state['attention_mask'].dtype==torch.int64 and state['pixel_values_videos'].dtype==torch.bfloat16,'FINAL_DTYPES');need(state['input_ids'].shape[1]<=4096,'TOKEN_LENGTH')
    expected=[.5+2*m for m in range(24)];need(len(trace)==1 and trace[0]==dict(indices=list(range(48)),fps=1.,merge=2,times=expected),'ACTUAL_NATIVE_METADATA')
    ids=state['input_ids'][0].tolist();decoded=p.tokenizer.decode(ids,skip_special_tokens=False,clean_up_tokenization_spaces=False);need(decoded.endswith(PREFIX) and p.tokenizer.encode(decoded,add_special_tokens=False)==ids,'PREFIX_OR_ROUNDTRIP')
    need(re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded)==[f'{v:.1f}' for v in expected],'ACTUAL_TIMECODES');candidates=[]
    for suffix in CONTINUATIONS:
        one=p.tokenizer.encode(suffix,add_special_tokens=False);need(len(one)==1 and one[0] not in p.tokenizer.all_special_ids,'READOUT_SINGLE_TOKEN')
        need(p.tokenizer.encode(decoded+suffix,add_special_tokens=False)==ids+one and p.tokenizer.decode(ids+one,skip_special_tokens=False,clean_up_tokenization_spaces=False)==decoded+suffix,'READOUT_CONTEXT_BOUNDARY');candidates.append(one[0])
    need(len(set(candidates))==5,'READOUT_TOKEN_DISTINCT');info.update(grid=[24,12,18],visual_tokens=1296,times=expected,indices=list(range(48)),tokens=len(ids),candidate_ids=candidates,prefix_in_actual_ids=True,context_boundary_pass=True,wall=time.monotonic()-tick)
    return state,info


def probe(root):
    root=Path(root);need(read(root/'binding-receipt.json')['status']=='PASS','BINDING_REQUIRED');cfg,np,torch,p,common=runtime(root);need(not torch.cuda.is_initialized(),'CPU_CUDA_INITIALIZED');q=dict(question='Which color fills the plain surface?',options=['Gray','Red','Blue','Green','Yellow']);rows=[]
    for fill in (128,0):state,info=native(p,q,np.full((48,192,288,3),fill,dtype=np.uint8),torch,common);rows.append(info)
    need(not torch.cuda.is_initialized(),'CPU_CUDA_INITIALIZED');write(root/'probe-receipt.json',dict(status='PASS',calls=2,rows=rows,CUDA_initialized=False,forward_calls=0))


class CacheReader:
    def __init__(self,path,budget):self.f=Path(path).open('rb');self.budget=budget
    def read(self,n=-1):
        need(n>=0 and self.budget['array_reserved']+n<=64*MIB,'ARRAY_READ_BUDGET');self.budget['array_reserved']+=n;b=self.f.read(n);self.budget['array_returned']+=len(b);return b
    def seek(self,n,whence=0):return self.f.seek(n,whence)
    def tell(self):return self.f.tell()
    def close(self):self.f.close()


def masked(original,mask,fill,np):
    need(type(mask) is int and 0<=mask<=15 and fill in (0,128),'FROZEN_INTERVENTION')
    if mask==15:return original
    a=np.full_like(original,fill)
    for i in range(4):
        if mask&(1<<i):a[12*i:12*i+12]=original[12*i:12*i+12]
    for i in range(4):need(np.array_equal(a[12*i:12*i+12],original[12*i:12*i+12]) if mask&(1<<i) else bool((a[12*i:12*i+12]==fill).all()),'PRESERVED_OR_FILLED_BYTES')
    return a


def suite(root):
    count=0
    def check(ok):
        nonlocal count
        count+=1;need(ok,'FIXTURE_ASSERTION')
    def refuse(fn):
        try:fn()
        except ValueError:check(True)
        else:check(False)
    obs={m:[0.,0.,0.,0.,0.] for m in OBS};obs[1]=[1.,0.,0.,0.,0.];obs[2]=[2.,0.,0.,0.,0.];obs[3]=[7.,0.,0.,0.,0.]
    for m in (5,9):obs[m]=[1.,0.,0.,0.,0.]
    for m in (6,10):obs[m]=[2.,0.,0.,0.,0.]
    check(estimate(obs,3,True)==[7.,0.,0.,0.,0.] and estimate(obs,3,False)==[3.,0.,0.,0.,0.]);check(estimate(obs,7,True)==[7.,0.,0.,0.,0.])
    check(estimate(obs,15,True)==obs[15] and estimate(obs,15,True,False)[0]==7.)
    check(best([dict(a=0,mask=1,margin=1),dict(a=4,mask=3,margin=1)])['mask']==3)
    check(best([dict(a=4,mask=5,margin=1),dict(a=3,mask=3,margin=1),dict(a=0,mask=3,margin=1)])==dict(a=0,mask=3,margin=1))
    refuse(lambda:route(dict(obs,**{'extra':[0]*5}),'I',0));refuse(lambda:route({m:[0]*5 for m in range(16)},'I',0))
    aobs=dict(obs);aobs.update({m:None for m in PAIRS});check(route(aobs,'A',0)==route(obs,'A',0));refuse(lambda:route(aobs,'I',0))
    check(len(r_masks(0))==13 and r_masks(0)==tuple(list(range(1,13))+[15]));check(r_masks(14)==r_masks(0))
    check(top([1,1,0,0,0])==0);check(vote({1:[0,1,0,0,0],2:[1,0,0,0,0],4:[1,0,0,0,0],8:[0,1,0,0,0]})==1)
    full=[2.,1.,0.,0.,0.];sel=dict(a=1,mask=3,margin=5.)
    check(gate(sel,full,[0,3,0,0,0],[0,3,0,0,0])['a']==1)
    check(gate(sel,full,[0,1,0,0,0],[0,3,0,0,0])['a']==0)
    check(gate(sel,full,[0,3,0,0,0],[4,0,0,0,0])['a']==0)
    check(gate(dict(a=0,mask=7),full)['reason']=='SAME_AS_F')
    check(select_top(b'{"predictions":{"forbidden":"not retained"},"closed_hashes":["owned"]}',{'closed_hashes'})=={'closed_hashes':['owned']})
    check(len(list(dict.fromkeys(['same','same','other'])))==2 and len(['same','same','other'])==3)
    for qi in range(24):check(len(required('R',qi))==13 and 15 in required('R',qi))
    write(Path(root)/'necessary-tests.json',dict(status='PASS',assertions=count,owned_only=True));print('NECESSARY_FIXTURES_PASS',count)


def telemetry_check(root,text,name):
    cfg=read(Path(root)/'runtime-config.json');rows=[s.strip().split(', ') for s in text.splitlines() if s.strip()];need(len(rows)==1 and len(rows[0])==5 and '3090' in rows[0][0],'GPU_DEVICE')
    d=dict(name=rows[0][0],uuid=rows[0][1],bus=rows[0][2],free_mib=float(rows[0][3]),util=float(rows[0][4]));need(d['uuid']==cfg['gpu_expected']['uuid'] and d['bus'].lower().split(':')[-2:]==cfg['gpu_expected']['bus'].lower().split(':')[-2:] and d['free_mib']>=18432,'GPU_IDENTITY_FREE18');write(Path(root)/(name+'.json'),d);return d


GPU_QUERY=['nvidia-smi','--query-gpu=name,uuid,pci.bus_id,memory.free,utilization.gpu','--format=csv,noheader,nounits']


def infer(root,remaining):
    root=Path(root);deadline=time.monotonic()+remaining-60;need(read(root/'probe-receipt.json')['status']=='PASS','CPU_GATE_REQUIRED');cfg,np,torch,p,common=runtime(root);questions=read(root/'nongold.json');inputs=read(root/'worker-input.json');historic=set(inputs['historic_hashes']);need(not torch.cuda.is_initialized(),'PREPARATION_CUDA')
    budget=read(root/'read-budget.json');arrays={};states={};meta_by_id={};logical=[];records={};started=set();attempts=0;steps=[0];model=None;gpu_start=None
    def save():write(root/'scores-private.json',records,True)
    def run_one(identity):
        nonlocal attempts
        if identity in records:return
        if identity in historic:
            records[identity]=dict(state='HISTORIC_INPUT_UNAVAILABLE');return
        need(identity not in started and attempts<480 and time.monotonic()<deadline,'FORWARD_BUDGET_OR_DEADLINE');started.add(identity);attempts+=1;event(root,dict(stage='STARTED',ordinal=attempts,identity=identity))
        tick=time.monotonic();before=steps[0];batch={k:v.to('cuda') for k,v in states[identity].items()}
        with torch.inference_mode():
            output=model(**batch,use_cache=False)
            logits=output.logits[0,-1,meta_by_id[identity]['candidate_ids']].float();scores=torch.log_softmax(logits,dim=-1).detach().cpu().tolist()
        torch.cuda.synchronize();finite(scores);need(steps[0]-before==1,'ACTUAL_FORWARD_STEPS');need(torch.cuda.max_memory_allocated()<=18*1024**3,'ALLOCATED18')
        record=dict(state='RETURNED',scores=scores,wall=time.monotonic()-tick,forward_steps=steps[0]-before,score_dtype='torch.float32');records[identity]=record;event(root,dict(stage='RETURNED',identity=identity,**record));save();del batch,output,logits
    try:
        for cache in inputs['caches']:
            regular(cache['path'],64*MIB);need(budget['array_opens']<4,'ARRAY_REOPEN');budget['array_opens']+=1;write(root/'read-budget.json',budget,True);meter=CacheReader(cache['path'],budget)
            try:a=np.load(meter,allow_pickle=False)
            finally:meter.close();write(root/'read-budget.json',budget,True)
            need(a.shape==(48,192,288,3) and a.dtype==np.uint8 and sha(a.tobytes())==cache['array_sha'],'ARRAY_CONTENT_IDENTITY');a.setflags(write=False);arrays[cache['alias']]=a
        write(root/'array-read-receipt.json',dict(opens=budget['array_opens'],reserved=budget['array_reserved'],returned=budget['array_returned'],file_payload=sum(c['bytes'] for c in inputs['caches']),content_SHA_match=True))
        prep_tick=time.monotonic()
        for qi,q in enumerate(questions):
            for mask in list(range(qi%16,16))+list(range(qi%16)):
                need(time.monotonic()<deadline,'INITIAL_PREPARATION_DEADLINE');state,info=native(p,q,masked(arrays[q['source']],mask,128,np),torch,common);identity=info['identity'];states.setdefault(identity,state);meta_by_id.setdefault(identity,info);logical.append(dict(question=qi,mask=mask,fill=128,identity=identity,info=info))
        need(not torch.cuda.is_initialized(),'FORMAL_PREPARATION_CUDA');unique=list(dict.fromkeys(x['identity'] for x in logical));write(root/'initial-input-seal.json',dict(logical=logical,unique=unique,common=common,code_sha=sha(Path(__file__).read_bytes()),nongold_sha=sha((root/'nongold.json').read_bytes()),historical_overlap=sorted(set(unique)&historic),R_observations=[list(r_masks(i)) for i in range(24)],CPU_preparation_wall=time.monotonic()-prep_tick,readout=dict(prefix=PREFIX,continuations=CONTINUATIONS,use_cache=False,normalization='FIVE_LOGITS_FLOAT32_LOG_SOFTMAX'),fingerprint_namespace='SAME_049_BOTTOM_INPUT_NAMESPACE_NOT_MODE_OR_TASK_NONCE'))
        need(len(logical)==384 and time.monotonic()<deadline,'INITIAL_INPUT_GATE');raw=subprocess.run(GPU_QUERY,capture_output=True,text=True,timeout=8,check=True);telemetry_check(root,raw.stdout,'telemetry-worker');need(time.monotonic()<deadline,'LOAD_DEADLINE')
        from transformers import Qwen3VLForConditionalGeneration
        torch.manual_seed(19);torch.cuda.set_per_process_memory_fraction(18/24,0);gpu_start=time.monotonic();event(root,dict(stage='WEIGHT_LOAD_INTENT'))
        model=Qwen3VLForConditionalGeneration.from_pretrained(cfg['qwen'],torch_dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True,trust_remote_code=False).to('cuda').eval()
        def hook(module,args):steps[0]+=1
        handle=model.register_forward_pre_hook(hook)
        for identity in unique:run_one(identity)
        mapping={(x['question'],x['mask']):x['identity'] for x in logical};selections=[]
        for qi in range(24):
            methods={}
            for method in ('I','A','C','R'):
                wanted=r_masks(qi) if method=='R' else OBS;obs={m:records.get(mapping[qi,m],{}).get('scores') for m in wanted}
                try:choice=route(obs,method,qi);methods[method]=dict(state='VALID',**choice,observed_masks=list(wanted))
                except ValueError:methods[method]=dict(state='FAILED' if any(mapping[qi,m] in started and records.get(mapping[qi,m],{}).get('state')!='RETURNED' for m in required(method,qi)) else 'NOT_RUN')
            selections.append(dict(question=qi,methods=methods))
        write(root/'selection-seal.json',dict(rows=selections,code_sha=sha(Path(__file__).read_bytes()),initial_queue_sha=sha((root/'initial-input-seal.json').read_bytes()),observations_structurally_limited=True,selected_before_triplet_validation_and_zero=True))
        zero=[]
        for qi,selection in enumerate(selections):
            masks=sorted({v['mask'] for v in selection['methods'].values() if v['state']=='VALID'})
            zero.extend(dict(question=qi,mask=mask,fill=0,identity=mapping[qi,15] if mask==15 else None,full_reuse=mask==15) for mask in masks)
        write(root/'zero-input-map.json',zero,True)
        for row in zero:
            if row['mask']==15:continue
            if time.monotonic()>=deadline:break
            qi=row['question'];q=questions[qi];state,info=native(p,q,masked(arrays[q['source']],row['mask'],0,np),torch,common);identity=info['identity'];row.update(identity=identity,info=info);states.setdefault(identity,state);meta_by_id.setdefault(identity,info);write(root/'zero-input-map.json',zero,True);run_one(identity)
        handle.remove();save();write(root/'inference-complete.json',dict(status='CLOSED',initial_logical=384,initial_unique=len(unique),zero_logical=len(zero),zero_nonfull=sum(not x['full_reuse'] for x in zero),attempts=attempts,returns=sum(x['state']=='RETURNED' for x in records.values()),forward_steps=steps[0],peak_allocated=torch.cuda.max_memory_allocated(),weight_intent_through_loop=time.monotonic()-gpu_start))
    except Exception as e:
        save();write(root/'inference-failure.json',dict(type=type(e).__name__,diagnostic=str(e)[:1200],attempts=attempts,returned=sum(x['state']=='RETURNED' for x in records.values()),actual_steps=steps[0]))
    finally:
        if model is not None:del model
        gc.collect()
        if torch.cuda.is_initialized():torch.cuda.empty_cache()


def close_outputs(root):
    root=Path(root);phase=read(root/'infer-phase.json');need(phase['active']==0,'MODEL_JOB_NOT_EXITED');questions=read(root/'nongold.json');initial=read(root/'initial-input-seal.json');need(initial['code_sha']==sha(Path(__file__).read_bytes()) and initial['nongold_sha']==sha((root/'nongold.json').read_bytes()),'CURRENT_INPUT_CODE_SEAL')
    scores=read(root/'scores-private.json');selection=read(root/'selection-seal.json') if (root/'selection-seal.json').exists() else dict(rows=[]);zero=read(root/'zero-input-map.json') if (root/'zero-input-map.json').exists() else [];mapping={(x['question'],x['mask']):x['identity'] for x in initial['logical']};zmap={(x['question'],x['mask']):x['identity'] for x in zero};starts={x['identity'] for x in [json.loads(s) for s in (root/'053-call-ledger.jsonl').read_text().splitlines()] if x['stage']=='STARTED'}
    if selection['rows']:need(selection['code_sha']==initial['code_sha'] and selection['initial_queue_sha']==sha((root/'initial-input-seal.json').read_bytes()),'SELECTION_SEAL_BINDING')
    def value(qi,mask,fill=128):
        identity=mapping.get((qi,mask)) if fill==128 or mask==15 else zmap.get((qi,mask));record=scores.get(identity,{})
        if record.get('state')!='RETURNED':raise ValueError('FAILED' if identity in starts else 'NOT_RUN')
        finite(record['scores']);return record['scores']
    output=[];cost=[];residuals={method:{group:[] for group in ('triples','raw_full','routed_full')} for method in ('I','A')};mechanism=[]
    def component_cost(qi,components):
        identities=[mapping.get((qi,m)) if fill==128 or m==15 else zmap.get((qi,m)) for fill,m in components];ids=list(dict.fromkeys(identities));ok=all(i is not None and scores.get(i,{}).get('state')=='RETURNED' for i in ids)
        return dict(logical_components=len(components),unique_components=len(ids),forward_wall=sum(scores[i]['wall'] for i in ids) if ok else None,complete=ok)
    for qi in range(24):
        choices=selection['rows'][qi]['methods'] if len(selection['rows'])==24 else {};per={}
        for method in METHODS:
            components=[(128,m) for m in (OBS if method in ('I','A','C') else required(method,qi))];natural_components=[(128,m) for m in required(method,qi)];row=dict(question=qi,method=method,source=questions[qi]['source'])
            try:
                for m in required(method,qi):value(qi,m)
                full=value(qi,15) if method!='M' else None
                if method=='F':result=dict(a=top(full),reason='FULL',changed=False,fallback=False)
                elif method=='M':result=dict(a=vote({m:value(qi,m) for m in SINGLES}),reason='SINGLE_BLOCK_VOTE',fallback=False)
                else:
                    choice=choices.get(method,dict(state='NOT_RUN'));need(choice['state']=='VALID',choice['state']);m=choice['mask'];result=gate(choice,full) if choice['a']==top(full) or m==15 else gate(choice,full,value(qi,m),value(qi,m,0))
                    if choice['a']!=top(full) and m!=15:
                        components=list(dict.fromkeys(components+[(128,m),(0,m)]));natural_components=list(dict.fromkeys(natural_components+[(128,m),(0,m)]))
                    row.update(selected_mask=m,selected_a=choice['a'])
                row.update(state='VALID',prediction=LETTERS[result['a']],**{k:v for k,v in result.items() if k!='a'})
            except ValueError as e:row.update(state=str(e) if str(e) in ('FAILED','NOT_RUN') else 'SCORING_UNKNOWN',prediction=None,reason=str(e))
            per[method]=row;output.append(row);cost.append(dict(question=qi,method=method,common_diagnostic_path=component_cost(qi,components),natural_minimal_path=component_cost(qi,natural_components)))
        mechanism.append(dict(question=qi,selection_different=None if any(m not in choices or choices[m]['state']!='VALID' for m in ('I','A')) else (choices['I']['mask'],choices['I']['a'])!=(choices['A']['mask'],choices['A']['a']),mask_different=None if any(m not in choices or choices[m]['state']!='VALID' for m in ('I','A')) else choices['I']['mask']!=choices['A']['mask'],output_different=None if per['I']['state']!='VALID' or per['A']['state']!='VALID' else per['I']['prediction']!=per['A']['prediction']))
        try:
            obs={m:value(qi,m) for m in OBS}
            for method in ('I','A'):
                for mask in TRIPLES+(15,):
                    measured=value(qi,mask);raw=estimate(obs,mask,method=='I',False);residuals[method]['triples' if mask!=15 else 'raw_full'].extend(raw[a]-measured[a] for a in range(5))
                residuals[method]['routed_full'].extend(estimate(obs,15,method=='I')[a]-value(qi,15)[a] for a in range(5))
        except ValueError:pass
    need(len(output)==144,'FULL_OUTPUT_DENOMINATOR');write(root/'outputs-private.json',output);write(root/'policy-cost-private.json',cost);write(root/'mechanism-private.json',mechanism);write(root/'residuals-private.json',residuals)
    write(root/'output-seal.json',dict(N=24,logical_outputs=144,code_sha=sha(Path(__file__).read_bytes()),nongold_sha=sha((root/'nongold.json').read_bytes()),scoring_map_sha=sha((root/'scoring-map-private.json').read_bytes()),outputs_sha=sha((root/'outputs-private.json').read_bytes()),scores_sha=sha((root/'scores-private.json').read_bytes()),cost_sha=sha((root/'policy-cost-private.json').read_bytes()),model_job_active0=True,new_returns=sum(x['state']=='RETURNED' for x in scores.values()),all_outputs_valid=all(x['state']=='VALID' for x in output)))
    print('OUTPUTS_SEALED',len(output),'valid',sum(x['state']=='VALID' for x in output))


def score(root):
    root=Path(root);cfg=read(root/'coordinator-config.json');seal=read(root/'output-seal.json');phase=read(root/'infer-phase.json');need(phase['active']==0 and seal['model_job_active0'] and seal['new_returns']>0,'NO_REAL_RETURN_OR_MODEL_NOT_EXITED');need(seal['code_sha']==sha(Path(__file__).read_bytes()) and seal['outputs_sha']==sha((root/'outputs-private.json').read_bytes()) and seal['scores_sha']==sha((root/'scores-private.json').read_bytes()),'OUTPUT_SCORE_SEAL')
    need(seal['nongold_sha']==sha((root/'nongold.json').read_bytes()) and seal['scoring_map_sha']==sha((root/'scoring-map-private.json').read_bytes()),'SCORING_INPUT_SEALS')
    q=read(root/'nongold.json');mapping=read(root/'scoring-map-private.json');budget=read(root/'read-budget.json');need(budget['original_opens']==0,'GOLD_REOPEN_FORBIDDEN');s=regular(cfg['annotation'],4*MIB);budget['original_opens']=1;write(root/'read-budget.json',budget,True)
    with open(cfg['annotation'],'rb') as f:raw=f.read(s.st_size)
    budget['original_returned']=len(raw);write(root/'read-budget.json',budget,True);need(len(raw)==s.st_size and sha(raw)==cfg['annotation_sha256'],'GOLD_SNAPSHOT');wanted={k:set(v) for k,v in mapping['wanted'].items()};originals,decoded=pure049.projected_json(raw,wanted,{'question','mcq_test','correct_answer_label'});need(decoded<=24,'GOLD_COUNT');del raw
    outputs=read(root/'outputs-private.json');scored=[]
    for qi,x in enumerate(q):
        try:
            original=originals[mapping['uids'][x['source']]][x['ordinal']];bind_original_nongold(original,x['question'],x['options']);label=original['correct_answer_label'];need(type(label) is str and label.strip().upper() in tuple(LETTERS),'GOLD_FORMAT');label=label.strip().upper()
        except Exception:label=None
        for row in [r for r in outputs if r['question']==qi]:
            state=row['state'];correct=None if label is None or state!='VALID' else int(row['prediction']==label)
            scored.append(dict(question=qi,source=x['source'],method=row['method'],state='SCORING_UNKNOWN' if label is None else 'VALID_CORRECT' if correct else 'VALID_WRONG' if state=='VALID' else state,correct=correct))
    write(root/'scored-derived-private.json',scored);write(root/'scoring-receipt.json',dict(original_opens=1,original_bytes=budget['original_returned'],gold_values_decoded=decoded,output_seal_sha=sha((root/'output-seal.json').read_bytes()),N=24,cells=144,all_known=all(x['correct'] is not None for x in scored)))
    summarize(root)


def summarize(root):
    root=Path(root);rows=read(root/'scored-derived-private.json');aliases=read(root/'source-selection.json')['aliases'];conditions=[];pairs=[];cells={(x['question'],x['method']):x for x in rows};q=read(root/'nongold.json')
    need(len(cells)==144,'SCORED_JOIN')
    for source in ['ALL']+aliases:
        ids=[i for i,x in enumerate(q) if source=='ALL' or x['source']==source]
        for method in METHODS:
            rs=[cells[i,method] for i in ids];conditions.append(dict(source=source,method=method,N=len(ids),correct=None if any(x['correct'] is None for x in rs) else sum(x['correct'] for x in rs),**{state:sum(x['state']==state for x in rs) for state in ('VALID_CORRECT','VALID_WRONG','FAILED','INVALID','NOT_RUN','SCORING_UNKNOWN')}))
        for baseline in ('F','A','C','R','M'):
            counts=dict(correction=0,harm=0,both_correct=0,both_wrong=0,unknown=0)
            for i in ids:
                a,b=cells[i,'I']['correct'],cells[i,baseline]['correct'];counts['unknown' if a is None or b is None else 'both_correct' if a and b else 'correction' if a else 'harm' if b else 'both_wrong']+=1
            pairs.append(dict(source=source,comparison='I_'+baseline,N=len(ids),**counts))
    full=all(x['correct'] is not None for x in rows);all_counts={x['method']:x['correct'] for x in conditions if x['source']=='ALL'};positive=sum(p['correction']>p['harm'] for p in pairs if p['source']!='ALL' and p['comparison']=='I_F');gates={}
    for baseline in ('F','A','C','R','M'):
        net=None if not full else all_counts['I']-all_counts[baseline];gates[baseline]=dict(net_correct=net,required_net=4 if baseline=='F' else 2,positive_sources=positive if baseline=='F' else None,passed=None if not full else net>=(4 if baseline=='F' else 2) and (positive>=3 if baseline=='F' else True))
    decision='INCOMPLETE_OR_UNKNOWN' if not full else 'OBSERVED_DEVELOPMENT_GAIN / OWNER_REVIEW_REQUIRED' if all(x['passed'] for x in gates.values()) else 'STOP_CURRENT_ROUTER';write(root/'condition-table.json',conditions);write(root/'pair-table.json',pairs);write(root/'scientific-summary.json',dict(N=24,decision=decision,novelty='UNRESOLVED',gates=gates,complete=full,correct=all_counts,conditions=len(conditions),pairs=len(pairs)))


def lock_gpu(root):
    import msvcrt
    cfg=read(Path(root)/'runtime-config.json');f=open(cfg['global_lock'],'r+b');f.seek(0)
    try:msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
    except Exception:f.close();raise
    k=C.WinDLL('kernel32',use_last_error=True);k.CreateMutexW.argtypes=[W.LPVOID,W.BOOL,W.LPCWSTR];k.CreateMutexW.restype=W.HANDLE;k.CloseHandle.argtypes=[W.HANDLE];k.ReleaseMutex.argtypes=[W.HANDLE]
    h=k.CreateMutexW(None,True,cfg['legacy_mutex'])
    if not h or C.get_last_error()==183:
        if h:k.CloseHandle(h)
        f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1);f.close();raise ValueError('GPU_BUSY_MUTEX')
    return f,k,h


def supervise(root,role):
    root=Path(root);cfg=read(root/'coordinator-config.json');need(time.time()<cfg['deadline_epoch'],'PARENT_DEADLINE');path=Path(__file__).with_name('auditable_runner_040.py');b=path.read_bytes().replace(b'\r\n',b'\n');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='3e56faf30afea1bed850c085bceb2afcc4fb257c','JOB_PLATFORM_IDENTITY');spec=importlib.util.spec_from_file_location('platform053',path);platform=importlib.util.module_from_spec(spec);spec.loader.exec_module(platform)
    caps=dict(suite=60,prepare=120,probe=180,review_setup=30,infer=1200,close=120,score=120,verify=120);used=sum(read(p)['wall'] for p in root.glob('*-phase.json') if read(p)['role']!='infer');cap=min(caps[role],cfg['deadline_epoch']-time.time(),1800-used if role!='infer' else 1200);need(cap>65 if role=='infer' else cap>5,'BUDGET');need(not (root/(role+'-phase.json')).exists(),'PHASE_RESTART_FORBIDDEN')
    f=k=h=None;job=None;child=None;empty=False;start=time.monotonic()
    try:
        if role=='infer':f,k,h=lock_gpu(root)
        job=platform.Job(memory=32*1024**3,active_limit=4);limit=platform.Extended();need(job.api.QueryInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit),None),'JOB_QUERY');limit.basic.flags|=0x10;limit.basic.affinity=1;need(job.api.SetInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit)),'JOB_AFFINITY');start=time.monotonic()
        if role=='infer':
            diagnostic=platform.Process(GPU_QUERY,root/'parent-gpu-query.log',job)
            try:diagnostic.wait(start+8);need(job.empty(start+9) and diagnostic.poll()==0,'PARENT_GPU_QUERY_EXIT');telemetry_check(root,(root/'parent-gpu-query.log').read_text(),'telemetry-parent')
            finally:diagnostic.close()
        script=root/'independent-review-053.py' if role=='verify' else Path(__file__).resolve();argv=[str(script),str(root)] if role=='verify' else [str(script),role,str(root)]+([str(cap-(time.monotonic()-start))] if role=='infer' else [])
        env="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES="+repr('0' if role=='infer' else '')+",HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',HF_HOME="+repr(str(root/'hf'))+",TORCH_HOME="+repr(str(root/'torch'))+",XDG_CACHE_HOME="+repr(str(root/'cache'))+",TEMP="+repr(str(root))+",TMP="+repr(str(root))+");sys.path.insert(0,"+repr(cfg['site'])+");sys.path.insert(0,"+repr(str(Path(__file__).resolve().parent))+");sys.argv="+repr(argv)+";runpy.run_path(sys.argv[0],run_name='__main__')"
        child=platform.Process([cfg['python'],'-I','-S','-B','-c',env],root/(role+'.log'),job)
        while job.active():
            if time.monotonic()-start>cap-3:job.kill();break
            time.sleep(.005)
        empty=job.empty(start+cap-1);need(empty,'OWN_JOB_EXIT_UNKNOWN');result=dict(role=role,wall=time.monotonic()-start,exitcode=child.poll(),**job.snapshot());write(root/(role+'-phase.json'),result);print(json.dumps(result));print((root/(role+'.log')).read_text(encoding='utf-8',errors='replace')[-1400:].encode('ascii','backslashreplace').decode())
    except Exception as e:
        if role=='infer' and child is None:
            if job:empty=job.empty(start+10)
            write(root/'GPU-admission-failure.json',dict(type=type(e).__name__,reason=str(e),model_launched=False))
        raise
    finally:
        if child:child.close()
        if job:job.close()
        if h:
            if empty:k.ReleaseMutex(h)
            k.CloseHandle(h)
            import msvcrt
            f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1);f.close()


REVIEW_SOURCE=r'''"""Independent 053 stdlib reconstruction; no tested-policy import or gold open."""
from pathlib import Path
import csv,hashlib,itertools,json,math,sys
r=Path(sys.argv[1]);rd=lambda n:json.loads((r/n).read_bytes());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();count=0
def check(ok):
 global count
 count+=1;assert ok
q=rd('nongold.json');initial=rd('initial-input-seal.json');scores=rd('scores-private.json');sel=rd('selection-seal.json');zeros=rd('zero-input-map.json');outputs=rd('outputs-private.json');derived=rd('scored-derived-private.json');cost=rd('policy-cost-private.json');seal=rd('output-seal.json');phase=rd('infer-phase.json');done=rd('inference-complete.json');scientific=rd('scientific-summary.json');ledger=[json.loads(x) for x in (r/'053-call-ledger.jsonl').read_text().splitlines()]
check(phase['active']==0 and phase['exitcode']==0 and not phase['killed']);check(len(q)==24 and len(initial['logical'])==384 and len(outputs)==len(derived)==144)
check(seal['outputs_sha']==h(r/'outputs-private.json') and seal['scores_sha']==h(r/'scores-private.json') and seal['cost_sha']==h(r/'policy-cost-private.json'))
check(initial['nongold_sha']==seal['nongold_sha']==h(r/'nongold.json'));check(initial['code_sha']==sel['code_sha']==seal['code_sha']==h(Path(rd('coordinator-config.json')['repo'])/'prototypes/block_interaction_053.py'))
check(sel['initial_queue_sha']==h(r/'initial-input-seal.json') and sel['selected_before_triplet_validation_and_zero'])
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
mapping={};info={}
for qi in range(24):
 rows=initial['logical'][16*qi:16*qi+16];check([x['mask'] for x in rows]==list(range(qi%16,16))+list(range(qi%16)) and all(x['question']==qi and x['fill']==128 for x in rows))
for row in initial['logical']:
 m=row['info'];identity=hashlib.sha256(canonical({'fields':m['fields'],'common':initial['common']})).hexdigest();check(identity==row['identity']);mapping[row['question'],row['mask']]=identity;info[identity]=m
 check(m['grid']==[24,12,18] and m['visual_tokens']==1296 and m['indices']==list(range(48)) and m['times']==[.5+2*k for k in range(24)] and m['tokens']<=4096 and len(set(m['candidate_ids']))==5 and m['context_boundary_pass'] and m['prefix_in_actual_ids'])
 check(set(m['fields'])=={'input_ids','attention_mask','pixel_values_videos','video_grid_thw'} and m['fields']['pixel_values_videos']['dtype']=='torch.bfloat16')
zmap={}
for row in zeros:
 zmap[row['question'],row['mask']]=row['identity']
 if row['mask']==15:check(row['full_reuse'] and row['identity']==mapping[row['question'],15])
 elif row['identity'] is not None:
  m=row['info'];check(hashlib.sha256(canonical({'fields':m['fields'],'common':initial['common']})).hexdigest()==row['identity']);info[row['identity']]=m
started=[x['identity'] for x in ledger if x['stage']=='STARTED'];returned=[x['identity'] for x in ledger if x['stage']=='RETURNED'];check(len(started)==len(set(started))<=480 and started==returned)
check(set(started).isdisjoint(rd('worker-input.json')['historic_hashes']));check(sum(x['stage']=='WEIGHT_LOAD_INTENT' for x in ledger)==1 and done['attempts']==done['returns']==done['forward_steps']==len(started))
check(all(x['state']=='RETURNED' and x['forward_steps']==1 and len(x['scores'])==5 and all(math.isfinite(v) for v in x['scores']) for x in scores.values()))
methods=['F','M','A','I','C','R'];obskeys=[0,1,2,3,4,5,6,8,9,10,12,15];singles=[1,2,4,8];trips=[7,11,13,14]
out={(x['question'],x['method']):x for x in outputs};truth={(x['question'],x['method']):x for x in derived};check(len(out)==len(truth)==144)
def v(qi,m,fill=128):return scores[(mapping if fill==128 or m==15 else zmap)[qi,m]]['scores']
def winner(xs):return min(range(5),key=lambda a:(-xs[a],a))
def gap(xs,a):return xs[a]-max(xs[b] for b in range(5) if b!=a)
def prediction(obs,mask,order,override=True):
 if mask==15 and override:return obs[15]
 indices=[i for i in range(4) if mask&(1<<i)];values=[]
 for a in range(5):
  d=sum(obs[1<<i][a]-obs[0][a] for i in indices)
  j=sum(obs[(1<<i)|(1<<k)][a]-obs[1<<i][a]-obs[1<<k][a]+obs[0][a] for i,k in itertools.combinations(indices,2)) if order==2 else 0
  values.append(obs[0][a]+d+j)
 return values
reconstructed={};residuals={m:{g:[] for g in ('triples','raw_full','routed_full')} for m in ('I','A')};mechanism=[]
for qi in range(24):
 obs={m:v(qi,m) for m in obskeys};full=obs[15];f=winner(full);choices={};rs=sorted({15}|{1+((qi+k)%14) for k in range(12)})
 for method in ('I','A','C','R'):
  candidates=[]
  if method in ('I','A'):
   for mask in range(1,16):
    vs=prediction(obs,mask,2 if method=='I' else 1)
    candidates.extend((gap(vs,a),mask,a) for a in range(5))
  else:
   for mask in ([m for m in obskeys if m] if method=='C' else rs):
    vs=v(qi,mask);a=winner(vs);candidates.append((gap(vs,a),mask,a))
  score,mask,a=min(candidates,key=lambda z:(-z[0],-bin(z[1]).count('1'),z[1],z[2]));choices[method]=(a,mask)
  actual=sel['rows'][qi]['methods'][method];check(actual['state']=='VALID' and (actual['a'],actual['mask'])==(a,mask) and actual['margin']==score)
  check(actual['observed_masks']==(rs if method=='R' else obskeys))
  answer=f
  if a!=f and mask!=15:
   first,second=v(qi,mask),v(qi,mask,0)
   if winner(first)==winner(second)==a and gap(first,a)>gap(full,f) and gap(second,a)>gap(full,f):answer=a
  reconstructed[qi,method]=answer
 votes=[winner(obs[m]) for m in singles];maximum=max(votes.count(a) for a in votes);reconstructed[qi,'M']=next(a for a in votes if votes.count(a)==maximum);reconstructed[qi,'F']=f
 for method in methods:
  actual=out[qi,method];check(actual['state']=='VALID' and actual['prediction']=='ABCDE'[reconstructed[qi,method]])
  row=truth[qi,method];check(type(row['correct']) is int and row['correct'] in (0,1) and row['state']==('VALID_CORRECT' if row['correct'] else 'VALID_WRONG'))
 check(len({out[qi,m]['prediction'] for m in methods if truth[qi,m]['correct']})<=1)
 for method in ('I','A'):
  for mask in trips+[15]:
   raw=prediction(obs,mask,2 if method=='I' else 1,False);residuals[method]['triples' if mask!=15 else 'raw_full'].extend(raw[a]-v(qi,mask)[a] for a in range(5))
  residuals[method]['routed_full'].extend(prediction(obs,15,2 if method=='I' else 1)[a]-full[a] for a in range(5))
 mechanism.append(dict(question=qi,selection_different=choices['I']!=choices['A'],mask_different=choices['I'][1]!=choices['A'][1],output_different=reconstructed[qi,'I']!=reconstructed[qi,'A']))
check(residuals==rd('residuals-private.json'));check(mechanism==rd('mechanism-private.json'))
for row in cost:
 qi,m=row['question'],row['method'];rs=sorted({15}|{1+((qi+k)%14) for k in range(12)});base=[15] if m=='F' else singles if m=='M' else [0]+singles+[15] if m=='A' else [x for x in obskeys if x] if m=='C' else obskeys if m=='I' else rs
 common=obskeys if m in ('I','A','C') else base
 for name,ks in [('common_diagnostic_path',common),('natural_minimal_path',base)]:
  components=[(128,k) for k in ks]
  if m in ('I','A','C','R'):
   choice=sel['rows'][qi]['methods'][m];a,mask=choice['a'],choice['mask']
   if a!=winner(v(qi,15)) and mask!=15:components=list(dict.fromkeys(components+[(128,mask),(0,mask)]))
  ids=list(dict.fromkeys((mapping if fill==128 or mask==15 else zmap)[qi,mask] for fill,mask in components));actual=row[name]
  check(actual['complete'] and actual['logical_components']==len(components) and actual['unique_components']==len(ids) and actual['forward_wall']==sum(scores[i]['wall'] for i in ids))
for row in rd('condition-table.json'):
 ids=[i for i,x in enumerate(q) if row['source']=='ALL' or x['source']==row['source']];rs=[truth[i,row['method']] for i in ids];check(row['N']==len(ids) and row['correct']==sum(x['correct'] for x in rs))
 for state in ('VALID_CORRECT','VALID_WRONG','FAILED','INVALID','NOT_RUN','SCORING_UNKNOWN'):check(row[state]==sum(x['state']==state for x in rs))
for row in rd('pair-table.json'):
 ids=[i for i,x in enumerate(q) if row['source']=='ALL' or x['source']==row['source']];b=row['comparison'][2:];expected=dict(correction=0,harm=0,both_correct=0,both_wrong=0,unknown=0)
 for i in ids:
  a,z=truth[i,'I']['correct'],truth[i,b]['correct'];expected['both_correct' if a and z else 'correction' if a else 'harm' if z else 'both_wrong']+=1
 check(row['N']==len(ids) and all(row[k]==v for k,v in expected.items()))
counts={m:sum(truth[i,m]['correct'] for i in range(24)) for m in methods};positive=sum(sum(truth[i,'I']['correct']-truth[i,'F']['correct'] for i,x in enumerate(q) if x['source']==s)>0 for s in rd('source-selection.json')['aliases']);checks=[]
for b in ('F','A','C','R','M'):
 gain=counts['I']-counts[b];passed=gain>=(4 if b=='F' else 2) and (positive>=3 if b=='F' else True);checks.append(passed);check(scientific['gates'][b]['net_correct']==gain and scientific['gates'][b]['passed']==passed)
expected='OBSERVED_DEVELOPMENT_GAIN / OWNER_REVIEW_REQUIRED' if all(checks) else 'STOP_CURRENT_ROUTER';check(scientific['decision']==expected and scientific['complete'])
budget=rd('read-budget.json');check(budget['original_opens']==1 and budget['original_returned']<=4*1024**2 and budget['metadata_returned']<=16*1024**2 and budget['array_returned']<=budget['array_reserved']<=64*1024**2)
check(rd('scoring-receipt.json')['gold_values_decoded']==24 and rd('scoring-receipt.json')['cells']==144)
phases=[json.loads(p.read_bytes()) for p in r.glob('*-phase.json')];check(all(x['active']==0 and not x['killed'] for x in phases));check(sum(x['wall'] for x in phases if x['role']!='infer')<=1800 and phase['wall']<=1200 and done['peak_allocated']<=18*1024**3 and max(x['peak_commit'] for x in phases)<=32*1024**3)
check(not any(x.split('.')[0] in ('torch','transformers','numpy','PIL') for x in sys.modules))
(r/'independent-review.json').write_text(json.dumps({'status':'PASS','assertions':count,'decision':expected,'policy_implementation_imported':False,'model_or_processor_imported':False,'original_reopens':0,'old_scores_or_predictions_opened':0,'full_inputs_recounted':len(mapping),'outputs_rebuilt':144,'conditions':30,'pairs':25,'cost_and_residuals_rebuilt':True}));print('INDEPENDENT_REVIEW_PASS',count)
'''


def review_setup(root):
    compile(REVIEW_SOURCE,'independent-review-053.py','exec')
    with (Path(root)/'independent-review-053.py').open('x',encoding='utf-8') as f:f.write(REVIEW_SOURCE)
    print('INDEPENDENT_STDLIB_REVIEW_EMITTED_AND_COMPILED')


if __name__=='__main__':
    role,path,*extra=sys.argv[1:];root=Path(path)
    if role=='launch':supervise(root,extra[0])
    elif role=='infer':infer(root,float(extra[0]))
    else:{'suite':suite,'prepare':prepare,'probe':probe,'review_setup':review_setup,'close':close_outputs,'score':score}[role](root)
