"""041 owned CPU processor/cache probe. No model execution or network.

The unchanged vendored ResponseCache is loaded by package namespaces only.
Run `export ROOT CSV` to independently reconstruct the 288 sequence rows.
"""
import argparse
import csv
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import time
import types

FAMILIES=('EXACT_VIDEO','EQUIVALENT_TIMELINE','FPS_NUMERIC','VIDEO_PIXEL','VIDEO_ORDER','VIDEO_FPS','VIDEO_SHIFT','IMAGE_PIXEL','TEXT_CONTROL')
PROFILES=('UPSTREAM','SOURCE_NAMESPACE','EFFECTIVE_INPUT','NO_CACHE')
GEN=dict(temperature=0,do_sample=False,max_new_tokens=16)
TASK='vlm_cache_input_041'
VISUAL={'pixel_values','pixel_values_videos'}

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def digest(x):return sha(packed(x))
def read(p):return json.loads(Path(p).read_bytes())
def write(p,x):
    with open(p,'xb') as f:f.write(packed(x));f.flush();os.fsync(f.fileno())
def append(p,x):
    with open(p,'ab') as f:f.write(packed(x)+b'\n');f.flush();os.fsync(f.fileno())
def require(x,s):
    if not x:raise ValueError(s)

def queue(clean=False):
    out=[]
    for fi,family in enumerate(FAMILIES):
        for s in range(4):
            if clean and (s!=0 or family not in ('EXACT_VIDEO','VIDEO_FPS')):continue
            for oi,order in enumerate(('AB','BA')):
                if clean and oi:continue
                rotation=(fi+s+oi)%4
                for profile in PROFILES[rotation:]+PROFILES[:rotation]:
                    out.append(dict(case=len(out),family=family,s=s,order=order,profile=profile))
    return out

def load_component(fixture):
    for name,relative in (('lmms_eval','lmms_eval'),('lmms_eval.api','lmms_eval/api'),('lmms_eval.caching','lmms_eval/caching')):
        module=types.ModuleType(name);module.__path__=[str(Path(fixture)/relative)];sys.modules[name]=module
    adapter=False
    try:import loguru
    except ImportError:
        import logging
        module=types.ModuleType('loguru');module.logger=logging.getLogger('041');sys.modules['loguru']=module;adapter=True
    from lmms_eval.api.instance import Instance
    from lmms_eval.caching.response_cache import ResponseCache
    return Instance,ResponseCache,adapter

def policy(root,config):
    """Deny child processes/network, weight bodies and writes outside new roots."""
    roots=[Path(root).resolve(),Path(config['budget_root']).resolve()]
    allowed=roots+[Path(config['model']).resolve(),Path(config['runtime']['site']).resolve(),Path(sys.base_prefix).resolve(),Path(__file__).resolve().parent,Path(config['fixture']).resolve()]
    def inside(p,rs):return any(p==r or r in p.parents for r in rs)
    def audit(event,args):
        if event.startswith(('socket.','subprocess.')) or event in ('os.system','os.startfile','os.exec','os.spawn'):raise PermissionError('041_NO_NETWORK_OR_CHILD')
        if event=='open' and not isinstance(args[0],int):
            name=os.fsdecode(args[0])
            if os.path.normcase(name)==os.path.normcase(os.devnull):return
            p=Path(name).resolve();mode=args[1];flags=args[2]
            writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT))
            if writing and not inside(p,roots):raise PermissionError('041_WRITE_OUTSIDE_ROOT')
            if not writing:
                if p.suffix.lower() in ('.safetensors','.bin','.pt','.pth','.gguf','.onnx'):raise PermissionError('041_WEIGHT_BODY_DENIED')
                if not inside(p,allowed):raise PermissionError('041_READ_OUTSIDE_ALLOWLIST')
    sys.addaudithook(audit)

class Inputs:
    def __init__(self,root,config,phase):
        self.root=Path(root);self.config=config;self.phase=phase;self.calls=0
        import torch,numpy,transformers
        from transformers import AutoProcessor
        from transformers.video_utils import VideoMetadata
        self.torch=torch;self.np=numpy;self.Metadata=VideoMetadata
        torch.set_num_threads(4);torch.set_num_interop_threads(1)
        require(not torch.cuda.is_initialized(),'CUDA_INITIALIZED')
        self.processor=AutoProcessor.from_pretrained(config['model'],local_files_only=True,trust_remote_code=False)
        p=self.processor
        self.identity=digest(dict(model='Qwen3-VL-4B',versions=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=numpy.__version__),image=p.image_processor.to_dict(),video=p.video_processor.to_dict(),tokenizer=sha(p.tokenizer.backend_tokenizer.to_str().encode()),chat_template=p.chat_template))
        self.versions=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=numpy.__version__)
        sources=[]
        for obj in (type(p),type(p.video_processor),type(p.image_processor),VideoMetadata):
            path=Path(sys.modules[obj.__module__].__file__)
            if str(path) not in [x['path'] for x in sources]:
                data=path.read_bytes();sources.append(dict(path=str(path),size=len(data),sha256=sha(data)))
        require(len(sources)<=4 and sum(x['size'] for x in sources)<=4*1024**2,'SOURCE_LIMIT')
        write(self.root/(phase+'-runtime.json'),dict(versions=self.versions,identity=self.identity,sources=sources,cuda_initialized=torch.cuda.is_initialized(),threads=torch.get_num_threads()))
    def reserve(self):
        path=Path(self.config['budget_root'])/'processor-calls.jsonl'
        entries=[json.loads(x) for x in path.read_bytes().splitlines()] if path.exists() else []
        require(len(entries)<720,'PROCESSOR_TOTAL_CAP')
        cap=16 if self.phase in ('suite','clean') else 648
        require(sum(x['phase']==self.phase for x in entries)<cap,'PROCESSOR_PHASE_CAP')
        append(path,dict(phase=self.phase,ordinal=len(entries)+1));self.calls+=1
    def raw(self,family,s,side):
        np=self.np;t=np.arange(12,dtype=np.uint16)[:,None,None,None];y=np.arange(192,dtype=np.uint16)[None,:,None,None];x=np.arange(288,dtype=np.uint16)[None,None,:,None];c=np.arange(3,dtype=np.uint16)[None,None,None,:]
        rgb=((17*t+3*y+5*x+29*c+37*s)%256).astype(np.uint8)
        meta=dict(total_num_frames=48,fps=4,duration=12.0,width=288,height=192,frames_indices=list(range(0,48,4)))
        question='Describe the image.' if family=='IMAGE_PIXEL' else 'Describe the video.'
        if side=='B':
            if family=='EQUIVALENT_TIMELINE':meta.update(total_num_frames=96,fps=8,frames_indices=list(range(0,96,8)))
            elif family=='FPS_NUMERIC':meta['fps']=4.0
            elif family in ('VIDEO_PIXEL','IMAGE_PIXEL'):rgb=255-rgb
            elif family=='VIDEO_ORDER':rgb=rgb[::-1].copy()
            elif family=='VIDEO_FPS':meta.update(fps=8,duration=6.0)
            elif family=='VIDEO_SHIFT':meta['frames_indices']=[i+2 for i in meta['frames_indices']]
            elif family=='TEXT_CONTROL':question='Describe this video briefly.'
        if family=='IMAGE_PIXEL':rgb=rgb[0].copy()
        return dict(rgb=rgb,metadata=meta,question=question,image=family=='IMAGE_PIXEL')
    def prepare(self,raw):
        self.reserve();start=time.perf_counter();p=self.processor
        messages=[dict(role='system',content='You are a helpful assistant.'),dict(role='user',content=[dict(type='image' if raw['image'] else 'video'),dict(type='text',text=raw['question'])])]
        rendered=p.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
        if raw['image']:batch=p(text=[rendered],images=[raw['rgb']],do_resize=False,return_tensors='pt')
        else:batch=p(text=[rendered],videos=[raw['rgb']],video_metadata=[self.Metadata(**raw['metadata'])],do_sample_frames=False,do_resize=False,return_tensors='pt')
        boundary={k:(v.to(self.torch.bfloat16) if k in VISUAL and self.torch.is_tensor(v) and v.is_floating_point() else v) for k,v in batch.items()}
        prep=time.perf_counter()-start;start=time.perf_counter();parts={}
        for k,v in boundary.items():
            if self.torch.is_tensor(v):
                require(v.device.type=='cpu','NON_CPU');parts[k]=dict(shape=list(v.shape),dtype=str(v.dtype),sha256=sha(v.contiguous().view(self.torch.uint8).numpy().tobytes()))
            else:parts[k]=dict(value=v)
        full=digest(dict(kwargs=parts,generation=GEN,identity=self.identity))
        ids=boundary['input_ids'][0].tolist();decoded=p.tokenizer.decode(ids,skip_special_tokens=False)
        gridkey='image_grid_thw' if raw['image'] else 'video_grid_thw';grid=boundary[gridkey].tolist()
        tokens=sum(a*b*c//4 for a,b,c in grid)
        require(len(ids)<=2048 and tokens<=512,'TOKEN_BOUND')
        expected=[1,12,18] if raw['image'] else [6,12,18]
        require(grid==[expected],'NATIVE_GRID')
        require(not self.torch.cuda.is_initialized(),'CUDA_INITIALIZED')
        receipt=dict(H=full,kwargs=parts,input_ids=ids,timecodes=re.findall(r'<([0-9.]+) seconds>',decoded),grid=grid,visual_tokens=tokens,visual_hash=digest({k:v for k,v in parts.items() if k in VISUAL or 'grid' in k}),text_hash=digest({k:v for k,v in parts.items() if k not in VISUAL and 'grid' not in k}),preprocess_seconds=prep,serialization_seconds=time.perf_counter()-start)
        return boundary,receipt
    def equal(self,a,b):
        if a.keys()!=b.keys():return False
        for k in a:
            x,y=a[k],b[k]
            if self.torch.is_tensor(x):
                if not self.torch.is_tensor(y) or x.dtype!=y.dtype or x.shape!=y.shape or not self.torch.equal(x,y):return False
            elif x!=y:return False
        return True

class Timings:
    """Non-mutating profiler; inclusive Python and SQLite C-call costs."""
    def __init__(self):self.stack={};self.totals={}
    def hook(self,frame,event,arg):
        name=None
        if event in ('call','return') and frame.f_code.co_filename.endswith('response_cache.py'):
            if frame.f_code.co_name in ('compute_cache_key','_extract_content_hash','_serialize_response'):name='key_serialization_seconds'
        if event in ('c_call','c_return','c_exception') and getattr(arg,'__module__',None)=='sqlite3':name='sqlite_seconds'
        if event in ('c_call','c_return','c_exception') and type(getattr(arg,'__self__',None)).__module__=='sqlite3':name='sqlite_seconds'
        if name:
            key=(id(frame),str(arg) if event.startswith('c_') else frame.f_code.co_name)
            if event in ('call','c_call'):self.stack[key]=(name,time.perf_counter())
            elif key in self.stack:
                label,t=self.stack.pop(key);self.totals[label]=self.totals.get(label,0)+time.perf_counter()-t

def oracle(inputs,root):
    records={};pairs=[]
    for fi,family in enumerate(FAMILIES):
        for s in range(4):
            a,ra=inputs.prepare(inputs.raw(family,s,'A'));b,rb=inputs.prepare(inputs.raw(family,s,'B'))
            actual='EQUAL' if inputs.equal(a,b) else 'DIFFERENT';expected='EQUAL' if fi<3 else 'DIFFERENT'
            for side,r in (('A',ra),('B',rb)):records[f'{family}/{s}/{side}']=r
            pairs.append(dict(family=family,s=s,actual=actual,expected=expected,status='PASS' if actual==expected else 'RELATION_MISMATCH'))
            del a,b
    result=dict(states=records,pairs=pairs);write(Path(root)/'oracle.json',result);return result

def sequences(inputs,config,root,plans,truth):
    Instance,Cache,adapter=load_component(config['fixture']);allrows=[]
    for plan in plans:
        case=plan['case'];directory=Path(root)/f'case-{case:03d}';directory.mkdir();queries=[]
        relation=next(x for x in truth['pairs'] if x['family']==plan['family'] and x['s']==plan['s'])
        for side in plan['order']:
            q=dict(side=side,attempted=True,status='FAILED',processor_calls=0,callback_calls=0,content_hash_calls=0,backend_calls=0,hit=0,miss=0,prepared_H=None,returned=None,oracle_H=truth['states'][f"{plan['family']}/{plan['s']}/{side}"]['H'],relation=relation['actual'],relation_status=relation['status'])
            started=time.perf_counter();cache=None;timer=Timings();before=inputs.calls
            try:
                raw=inputs.raw(plan['family'],plan['s'],side);prepared=None;namespace=inputs.identity
                if plan['profile']=='SOURCE_NAMESPACE':
                    t=time.perf_counter();namespace=digest(dict(rgb=sha(raw['rgb'].tobytes()),metadata=raw['metadata'],question=raw['question'],gen=GEN,identity=inputs.identity));q['content_hash_calls']=1;q['content_hash_seconds']=time.perf_counter()-t
                if plan['profile']=='EFFECTIVE_INPUT':
                    _,prepared=inputs.prepare(raw);namespace=prepared['H'];q['prepared_H']=prepared['H']
                def callback(doc):q['callback_calls']+=1;return doc
                class Backend:
                    def generate_until(self,requests):
                        answers=[]
                        for request in requests:
                            q['backend_calls']+=1;current=request.args[2](request.doc)
                            nonlocal prepared
                            if prepared is None:
                                sys.setprofile(None)
                                try:_,prepared=inputs.prepare(current)
                                finally:sys.setprofile(timer.hook if plan['profile']!='NO_CACHE' else None)
                            q['prepared_H']=prepared['H'];answers.append('INPUT_SHA256:'+prepared['H'])
                        return answers
                req=Instance(request_type='generate_until',arguments=(raw['question'],dict(GEN),callback,4*FAMILIES.index(plan['family'])+plan['s'],TASK,'test'),idx=0,metadata=dict(task=TASK,doc_id=4*FAMILIES.index(plan['family'])+plan['s'],repeats=1));req.doc=raw
                if plan['profile']=='NO_CACHE':answer=Backend().generate_until([req])[0];q['decision']='BYPASS'
                else:
                    sys.setprofile(timer.hook)
                    cache=Cache(str(directory/'cache.sqlite'),str(directory/'audit.jsonl'),model_fingerprint='Qwen3-VL-4B:'+inputs.identity,task_fingerprints={TASK:namespace},eval_version='041-8f400975')
                    answer=cache.execute(Backend(),'generate_until',[req])[0];stats=cache.get_stats();q['hit']=stats['hits'];q['miss']=stats['misses'];q['decision']='HIT' if q['hit'] else 'MISS'
                q['returned']=answer
                stable=q['prepared_H'] is None or q['prepared_H']==q['oracle_H']
                q['status']='UNSTABLE' if not stable else ('INCOMPATIBLE_REUSE' if answer!='INPUT_SHA256:'+q['oracle_H'] else ('CORRECT_REUSE' if q['hit'] else 'CORRECT_NEW'))
                if relation['status']!='PASS':q['status']='RELATION_MISMATCH'
                if prepared:q.update(preprocess_seconds=prepared['preprocess_seconds'],serialization_seconds=prepared['serialization_seconds'])
            except Exception as e:q['error']=type(e).__name__+':'+str(e)[:200]
            finally:
                if cache is not None:cache.close()
                sys.setprofile(None);q.update(timer.totals);q['processor_calls']=inputs.calls-before;q['wall_seconds']=time.perf_counter()-started
                append(Path(root)/'queries.jsonl',dict(case=case,**q));queries.append(q)
        row=dict(**plan,relation=relation['actual'],relation_status=relation['status'],queries=queries);allrows.append(row);append(Path(root)/'rows.jsonl',row)
        # A sequence has no subsequent use; remove only its own SQLite auxiliary files.
        for p in directory.iterdir():p.unlink()
        directory.rmdir()
    write(Path(root)/'execution.json',dict(rows=len(allrows),processor_calls=inputs.calls,logging_adapter=adapter,cuda_initialized=inputs.torch.cuda.is_initialized()))
    return allrows

def worker(root,config,phase):
    root=Path(root);config=read(config);policy(root,config)
    try:
        inputs=Inputs(root,config,phase)
        if phase=='suite':
            from test_cache_input_contract_041 import suite
            suite(inputs,config,root);return
        plans=read(root/'queue.json')
        truth=read(config['oracle']) if phase=='clean' else oracle(inputs,root)
        sequences(inputs,config,root,plans,truth)
    except Exception as e:
        append(root/'errors.jsonl',dict(type=type(e).__name__,error=str(e)[:600]));raise

def export(root,target):
    root=Path(root);plans=read(root/'queue.json');rows={}
    if (root/'rows.jsonl').exists():rows={x['case']:x for x in map(json.loads,(root/'rows.jsonl').read_bytes().splitlines())}
    partial={}
    if (root/'queries.jsonl').exists():
        for line in (root/'queries.jsonl').read_bytes().splitlines():
            q=json.loads(line);partial.setdefault(q.pop('case'),[]).append(q)
    fields=['case','family','s','order','profile','relation','relation_status','queries']
    with open(target,'w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for p in plans:
            row=rows.get(p['case'],dict(**p,relation='UNKNOWN',relation_status='NOT_RUN',queries=[dict(side=s,attempted=False,status='NOT_RUN') for s in p['order']]))
            if p['case'] not in rows and p['case'] in partial:
                known={q['side']:q for q in partial[p['case']]};row['queries']=[known.get(s,dict(side=s,attempted=False,status='NOT_RUN')) for s in p['order']]
            writer.writerow({**row,'queries':packed(row['queries']).decode()})

def recompute(target):
    from collections import Counter
    groups={}
    with open(target,newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    for row in rows:
        stats=groups.setdefault(row['profile'],Counter(sequences=0));stats['sequences']+=1
        queries=json.loads(row['queries'])
        for q in queries:
            stats['queries']+=1;stats[q['status']]+=1
            for key in ('processor_calls','callback_calls','backend_calls','content_hash_calls','hit','miss'):stats[key]+=q.get(key,0)
        if row['relation']=='EQUAL' and queries[1].get('decision')=='MISS':stats['equal_opportunity_missed']+=1
    return dict(rows=len(rows),queries=sum(x['queries'] for x in groups.values()),profiles=groups)

def supervise(root,config,phase,seconds):
    root=Path(root);cfg=read(config)
    intake=read(Path(cfg['budget_root'])/'intake.json')
    require(time.time()+seconds<intake['deadline'],'PARENT_DEADLINE')
    prior=list(Path(cfg['budget_root']).glob('*-supervisor.json'))
    if root!=Path(cfg['budget_root']):prior+=list(root.glob('*-supervisor.json'))
    require(sum(read(p)['wall_seconds'] for p in prior)+seconds<=1000,'SUPERVISED_WALL_CAP')
    spec=importlib.util.spec_from_file_location('platform040',Path(__file__).with_name('auditable_runner_040.py'));platform=importlib.util.module_from_spec(spec);spec.loader.exec_module(platform)
    bootstrap="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES='',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',HF_HOME="+repr(str(root/'hf'))+",TEMP="+repr(str(root))+",TMP="+repr(str(root))+");sys.path.insert(0,"+repr(cfg['runtime']['site'])+");sys.path.insert(0,"+repr(str(Path(__file__).parent))+");sys.argv="+repr([str(Path(__file__)),'worker',str(root),str(config),phase])+";runpy.run_path(sys.argv[0],run_name='__main__')"
    started=time.monotonic();j=platform.Job(memory=4*1024**3);p=None;error=None;code=None
    try:
        p=platform.Process([cfg['runtime']['python'],'-I','-S','-B','-c',bootstrap],root/(phase+'-stdout.txt'),job=j);code=p.wait(started+seconds-2)
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if not j.empty(min(started+seconds-1,time.monotonic()+.3)):j.kill()
        require(j.empty(started+seconds),'JOB_NOT_EMPTY');snapshot=j.snapshot()
        if p:p.close()
        j.close()
    write(root/(phase+'-supervisor.json'),dict(exitcode=code,error=error,wall_seconds=time.monotonic()-started,**snapshot))

def main():
    a=sys.argv[1:]
    if a[0]=='worker':worker(a[1],a[2],a[3])
    elif a[0]=='supervise':supervise(a[1],a[2],a[3],float(a[4]))
    elif a[0]=='export':export(a[1],a[2])
    elif a[0]=='recompute':print(json.dumps(recompute(a[1]),sort_keys=True))
    else:raise ValueError('UNKNOWN_COMMAND')

if __name__=='__main__':main()
