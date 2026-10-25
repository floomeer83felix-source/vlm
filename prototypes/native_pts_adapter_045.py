"""045 request-local native timestamp adapter, owned CPU inputs only.

Native formatting/tokenization remains upstream Transformers4.57.6:
https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_vl/processing_qwen3_vl.py
No upstream implementation is copied; subclass calls the installed native chain.
No model weights, forward/generate, media, decoder or network is used.
"""
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import sys
import time
from types import MappingProxyType

SOURCE_BLOB='17bdd975eef337371aa763824edc7e6ec1987dbf'
SLOTS=(('Q01','native','CFR'),('Q02','P','CFR'),('Q03','native','A'),('Q04','P','A'),('Q05','P','B'),('Q06','native','A'),('Q07','P','A'),('Q08','native','Q'),('Q09','P','Q'))
VISUAL={'pixel_values','pixel_values_videos','image_grid_thw','video_grid_thw'}
def require(ok,reason):
    if not ok:raise ValueError(reason)
def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(x):return hashlib.sha256(pack(x)).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def write(p,x):
    data=pack(x);require(len(data)<8*1024**2,'RECEIPT_CAP')
    with open(p,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def append(p,x):
    with open(p,'ab') as f:f.write(pack(x)+b'\n');f.flush();os.fsync(f.fileno())
def selected():return tuple(round(Fraction(j*95,47)) for j in range(48))
def number(value):
    require(not isinstance(value,bool) and isinstance(value,(int,float,Fraction)),'NON_NUMERIC')
    require(math.isfinite(float(value)),'NONFINITE');return Fraction(value)

class RequestClock:
    """Immutable full96-source map; raw metadata indices/fps remain unchanged."""
    __slots__=('indices','fps','mapping','identity','_locked')
    def __setattr__(self,name,value):
        if getattr(self,'_locked',False):raise AttributeError('IMMUTABLE_REQUEST')
        object.__setattr__(self,name,value)
    def __init__(self,mapping,indices,fps):
        require(mapping is not None and set(mapping)==set(range(96)),'MISSING_SOURCE_MAPPING')
        require(all(type(k) is int for k in mapping),'NON_INTEGER_SOURCE_KEY')
        require(isinstance(indices,(list,tuple)),'MISSING_INDICES');self.indices=tuple(indices);require(len(self.indices)==48 and all(type(i) is int for i in self.indices),'INTEGER48_INDICES')
        require(all(0<=i<96 for i in self.indices) and all(a<b for a,b in zip(self.indices,self.indices[1:])),'SOURCE_INDEX_ORDER')
        self.fps=number(fps);require(self.fps>0,'NONPOSITIVE_FPS')
        values=[number(mapping[i]) for i in range(96)]
        require(values[0]>=0 and all(a<b for a,b in zip(values,values[1:])),'PTS_NONNEGATIVE_STRICT_ORDER')
        self.mapping=MappingProxyType(dict(enumerate(values)))
        self.identity=digest(dict(indices=self.indices,fps=str(self.fps),mapping=[str(x) for x in values]));self._locked=True
    def resolve(self,indices,fps,merge_size):
        if hasattr(indices,'tolist'):indices=indices.tolist()
        require(isinstance(indices,(list,tuple)) and len(indices)==48 and all(type(i) is int for i in indices),'ACTUAL_INTEGER48_INDICES')
        require(tuple(indices)==self.indices,'ACTUAL_SOURCE_INDEX_MISMATCH')
        require(type(merge_size) is int and merge_size==2,'MERGE_SIZE_2_ONLY')
        actual=number(fps);require(actual>0 and actual==self.fps,'ACTUAL_FPS_MISMATCH')
        return tuple((self.mapping[indices[j]]+self.mapping[indices[j+1]])/2 for j in range(0,48,2))

def validate_inputs(request,args,kwargs,merge_size):
    require(not args,'KEYWORD_SINGLE_VIDEO_ONLY')
    required={'text','videos','video_metadata','do_sample_frames','do_resize','return_tensors'}
    require(set(kwargs)==required,'EXACT_INPUT_CONTRACT')
    require(isinstance(kwargs['text'],list) and len(kwargs['text'])==1,'SINGLE_TEXT_ONLY')
    videos=kwargs['videos'];require(isinstance(videos,list) and len(videos)==1,'SINGLE_VIDEO_ONLY')
    require(tuple(videos[0].shape)==(48,192,288,3),'RGB48_SHAPE')
    metadata=kwargs['video_metadata'];require(isinstance(metadata,list) and len(metadata)==1,'SINGLE_METADATA_ONLY');m=metadata[0]
    require(m.total_num_frames==96 and m.duration==96 and m.width==288 and m.height==192,'FIXED_SOURCE_METADATA')
    require(kwargs['do_sample_frames'] is False and kwargs['do_resize'] is False and kwargs['return_tensors']=='pt','NATIVE_PREPROCESS_CONTRACT')
    request.resolve(m.frames_indices,m.fps,merge_size)

def bind_processor(base,request):
    """Fresh subclass instance, shared readonly assets; base is never patched."""
    require(type(base).__name__=='Qwen3VLProcessor','EXPECTED_PROCESSOR_CLASS')
    class RequestBoundQwen3VLProcessor(type(base)):
        def __call__(self,*args,**kwargs):
            require(not self._used,'SINGLE_USE_REQUEST');self._used=True
            validate_inputs(self._clock,args,kwargs,self.video_processor.merge_size)
            self._active=True
            try:return super().__call__(**kwargs)
            finally:self._active=False
        def _calculate_timestamps(self,indices,video_fps,merge_size=2):
            require(self._active,'CALLBACK_OUTSIDE_REQUEST')
            raw=self._clock.resolve(indices,video_fps,merge_size)
            self._trace.append(dict(indices=list(indices),fps=float(video_fps),fps_type=type(video_fps).__name__,merge_size=merge_size,mapping_identity=self._clock.identity,raw=[str(x) for x in raw],returned=[float(x) for x in raw]))
            return [float(x) for x in raw]
    instance=RequestBoundQwen3VLProcessor(image_processor=base.image_processor,tokenizer=base.tokenizer,video_processor=base.video_processor,chat_template=base.chat_template)
    instance._clock=request;instance._trace=[];instance._used=False;instance._active=False;return instance

def fixture(name):
    if name=='CFR':durations=[1000]*96
    elif name=='A':durations=[500]*48+[1500]*48
    elif name=='B':durations=[1500]*48+[500]*48
    elif name=='Q':durations=[1010]+[1000]*94+[990]
    else:raise ValueError('FIXTURE_NAME')
    pts=[];at=0
    for d in durations:pts.append(at);at+=d
    require(at==96000,'FIXTURE_END')
    return dict(pts=pts,durations=durations,time_base='1/1000',total=96)

def policy(root,config):
    root=Path(root).resolve();allowed=[root,Path(config['model']).resolve(),Path(config['site']).resolve(),Path(sys.base_prefix).resolve(),Path(__file__).resolve().parent]
    def within(p,roots):return any(p==r or r in p.parents for r in roots)
    def audit(event,args):
        if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.startfile'):raise PermissionError('NO_NETWORK_OR_CHILD_045')
        if event=='import' and args[0].split('.')[0] in ('av','torchcodec'):
            # torchvision.io.video explicitly catches ImportError for optional
            # PyAV. Keep the decoder unavailable without aborting CPU imports.
            append(root/'denied-decoder-imports.jsonl',dict(module=args[0],denied=True))
            raise ImportError('NO_DECODER_045')
        if event=='open' and not isinstance(args[0],int):
            value=os.fsdecode(args[0])
            if os.path.normcase(value)==os.path.normcase(os.devnull):return
            p=Path(value).resolve();mode=args[1];flags=args[2]
            writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_CREAT|os.O_WRONLY|os.O_RDWR))
            if writing:require(within(p,[root]),'WRITE_SCOPE')
            else:
                require(p.suffix.lower() not in ('.safetensors','.bin','.pt','.pth','.gguf','.onnx','.mp4','.webm','.wav'),'WEIGHT_MEDIA_BODY_DENIED')
                require(within(p,allowed),'READ_SCOPE')
    sys.addaudithook(audit)

def identity(base,versions):
    return digest(dict(model='Qwen3-VL-4B',versions=versions,image=base.image_processor.to_dict(),video=base.video_processor.to_dict(),chat=base.chat_template,tokenizer_sha=hashlib.sha256(base.tokenizer.backend_tokenizer.to_str().encode()).hexdigest(),special_tokens=base.tokenizer.special_tokens_map))

def boundary(batch,torch,base_identity):
    tensors={k:v.to(torch.bfloat16) if k in ('pixel_values','pixel_values_videos') and torch.is_tensor(v) and v.is_floating_point() else v for k,v in batch.items()}
    parts={}
    for k,v in tensors.items():
        if torch.is_tensor(v):
            require(v.device.type=='cpu','CPU_ONLY')
            parts[k]=dict(shape=list(v.shape),dtype=str(v.dtype),device=str(v.device),sha256=hashlib.sha256(v.contiguous().view(torch.uint8).numpy().tobytes()).hexdigest())
        else:parts[k]=dict(value=v)
    return tensors,dict(kwargs=parts,full_hash=digest(dict(kwargs=parts,base_identity=base_identity)),visual_hash=digest({k:v for k,v in parts.items() if k in VISUAL}),text_hash=digest({k:v for k,v in parts.items() if k not in VISUAL}))

def equal(a,b,torch,keys=None):
    keys=set(a) if keys is None else set(keys)
    if keys!=set(b) and keys==set(a):return False
    for k in keys:
        if k not in a or k not in b:return False
        x,y=a[k],b[k]
        if torch.is_tensor(x):
            if not torch.is_tensor(y) or x.dtype!=y.dtype or x.shape!=y.shape or x.device!=y.device or not torch.equal(x,y):return False
        elif x!=y:return False
    return True

def worker(root):
    root=Path(root);config=read(root/'config.json');policy(root,config)
    import torch,numpy as np,transformers
    require(transformers.__version__=='4.57.6','API_VERSION_HOLD')
    from transformers import AutoProcessor
    from transformers.video_utils import VideoMetadata
    torch.set_num_threads(4);torch.set_num_interop_threads(1);require(not torch.cuda.is_initialized(),'CUDA_INITIALIZED')
    base=AutoProcessor.from_pretrained(config['model'],local_files_only=True,trust_remote_code=False)
    versions=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=np.__version__)
    source=Path(sys.modules[type(base).__module__].__file__).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest();require(blob==SOURCE_BLOB,'PROCESSOR_SOURCE_HOLD')
    common=identity(base,versions);base_class=type(base);original_method=type(base)._calculate_timestamps
    write(root/'runtime.json',dict(versions=versions,base_identity=common,processor_class=base_class.__name__,source_bytes=len(source),source_sha256=hashlib.sha256(source).hexdigest(),source_blob=blob,threads=torch.get_num_threads(),cuda_initialized=torch.cuda.is_initialized()))
    calls=0
    def prepare(path,table,slot,phase):
        nonlocal calls
        require(calls<12 and (phase!='probe' or calls<2),'PROCESSOR_BUDGET');calls+=1
        append(root/'calls.jsonl',dict(ordinal=calls,slot=slot,phase=phase,table=table,path=path))
        indices=selected();f=fixture(table)
        rgb=((17*np.array(indices,dtype=np.uint16)[:,None,None,None]+3*np.arange(192,dtype=np.uint16)[None,:,None,None]+5*np.arange(288,dtype=np.uint16)[None,None,:,None]+29*np.arange(3,dtype=np.uint16)[None,None,None,:])%256).astype(np.uint8)
        metadata=VideoMetadata(total_num_frames=96,fps=1,duration=96,width=288,height=192,frames_indices=list(indices))
        request=RequestClock({i:Fraction(t,1000) for i,t in enumerate(f['pts'])},indices,1)
        processor=bind_processor(base,request) if path=='P' else base
        messages=[dict(role='system',content='You are a helpful assistant.'),dict(role='user',content=[dict(type='video'),dict(type='text',text='Describe the video.')])]
        text=base.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
        kwargs=dict(text=[text],videos=[rgb],video_metadata=[metadata],do_sample_frames=False,do_resize=False,return_tensors='pt')
        trace=[]
        def profile(frame,event,arg):
            if frame.f_code.co_name!='_calculate_timestamps':return
            if event=='call':
                values=frame.f_locals;ix=values['indices'];ix=ix.tolist() if hasattr(ix,'tolist') else list(ix)
                trace.append(dict(indices=ix,fps=float(values['video_fps']),fps_type=type(values['video_fps']).__name__,merge_size=values['merge_size'],implementation='adapter' if path=='P' else 'native'))
            elif event=='return' and trace:trace[-1]['returned']=list(arg) if arg is not None else None
        sys.setprofile(profile);start=time.perf_counter()
        try:batch=processor(**kwargs)
        finally:sys.setprofile(None)
        elapsed=time.perf_counter()-start
        require(not torch.cuda.is_initialized(),'CUDA_INITIALIZED')
        state,receipt=boundary(batch,torch,common);ids=state['input_ids'][0].tolist();decoded=base.tokenizer.decode(ids,skip_special_tokens=False,clean_up_tokenization_spaces=False)
        grid=state['video_grid_thw'].tolist();tokens=int(state['video_grid_thw'].prod().item())//4
        receipt.update(slot=slot,phase=phase,path=path,fixture=table,indices=list(indices),indices_hash=digest(indices),pts_hash=digest(f),mapping_identity=request.identity,callback=trace,request_trace=processor._trace if path=='P' else [],raw_times=trace[0].get('returned',[]) if trace else [],native_timecodes=re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded),decoded=decoded,without_timecodes=re.sub(r'<[0-9]+\.[0-9] seconds>','<TIME>',decoded),input_ids=ids,attention_mask=state['attention_mask'].tolist(),grid=grid,visual_tokens=tokens,wall=elapsed,base_identity_before=common,base_identity_after=identity(base,versions),base_class_unchanged=type(base) is base_class and type(base)._calculate_timestamps is original_method and '_calculate_timestamps' not in base.__dict__)
        return state,receipt
    try:
        _,probe=prepare('P','CFR','PROBE01','probe')
        require(len(probe['callback'])==1 and len(probe['raw_times'])==24 and probe['callback'][0]['indices']==list(selected()) and len(probe['request_trace'])==1,'PROBE_CALLBACK_NOT_CONNECTED')
        write(root/'probe-ready.json',dict(status='PASS',callback=probe['callback'],request_trace=probe['request_trace'],base_identity=common,source_blob=blob,calls=calls))
    except Exception as e:
        write(root/'probe-failed.json',dict(type=type(e).__name__,error=str(e)[:400],calls=calls));raise
    wait_until=min(time.perf_counter()+120,read(root/'worker-config.json')['work_deadline']-10)
    while not (root/'formal-go.json').exists():
        require(time.perf_counter()<wait_until,'FORMAL_HANDSHAKE_TIMEOUT');time.sleep(.02)
    seal=read(root/'formal-go.json')
    require(seal['source_sha256']==hashlib.sha256(Path(__file__).read_bytes()).hexdigest() and seal['slots']==[list(x) for x in SLOTS] and seal['base_identity']==common,'FORMAL_SEAL_MISMATCH')
    states={};receipts=[]
    for slot,path,table in SLOTS:
        try:
            state,receipt=prepare(path,table,slot,'formal');states[slot]=state;receipt['state']='EXECUTED';receipts.append(receipt);append(root/'formal.jsonl',receipt)
        except Exception as e:
            receipt=dict(slot=slot,path=path,fixture=table,state='FAILED',error=type(e).__name__+':'+str(e)[:400]);receipts.append(receipt);append(root/'formal.jsonl',receipt)
    sys.path.insert(0,str(Path(__file__).resolve().parent));from test_native_pts_adapter_045 import validate_formal
    result=validate_formal(receipts,states,torch,base.tokenizer)
    write(root/'verification.json',dict(rows=result,calls=calls,base_identity_before=common,base_identity_after=identity(base,versions),base_unchanged=type(base) is base_class and type(base)._calculate_timestamps is original_method,cuda_initialized=torch.cuda.is_initialized()))

def supervise(root,role,seconds,python=None):
    root=Path(root);cfg=read(root/'config.json');require(time.time()+seconds<cfg['deadline'],'PARENT_DEADLINE')
    spec=importlib.util.spec_from_file_location('platform040',Path(__file__).with_name('auditable_runner_040.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    start=time.perf_counter();deadline=start+seconds-2;write(root/(role+'-config.json'),dict(start=start,work_deadline=deadline))
    j=p.Job(memory=4*1024**3,active_limit=2);child=None;kill=None;zero=None;code=None;error=None
    bootstrap="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES='',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',HF_HOME="+repr(str(root/'hf'))+",TEMP="+repr(str(root))+",TMP="+repr(str(root))+");sys.path.insert(0,"+repr(cfg['site'])+");sys.path.insert(0,"+repr(str(Path(__file__).parent))+");sys.argv="+repr([str(Path(__file__).resolve()),role,str(root)])+";runpy.run_path(sys.argv[0],run_name='__main__')"
    try:
        child=p.Process([python or cfg['python'],'-I','-S','-B','-c',bootstrap],root/(role+'.log'),j)
        while j.active():
            now=time.perf_counter()
            if now>=deadline and kill is None:kill=now;j.kill()
            if now>=start+seconds-1:raise TimeoutError('DRAIN_DEADLINE')
            time.sleep(.005)
        zero=time.perf_counter();code=child.poll()
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if zero is None:
            if kill is None:kill=time.perf_counter();j.kill()
            while j.active() and time.perf_counter()<start+seconds:time.sleep(.005)
            if not j.active():zero=time.perf_counter()
        snapshot=j.snapshot()
        if child:child.close()
        j.close()
    require(zero is not None and snapshot['active']==0,'OWN_JOB_NOT_EMPTY')
    write(root/(role+'-supervisor.json'),dict(start=start,active0=zero,kill=kill,exitcode=code,error=error,wall=time.perf_counter()-start,**snapshot))

if __name__=='__main__':
    role,root=sys.argv[1:]
    if role=='worker':worker(root)
    elif role=='suite':
        policy(root,read(Path(root)/'config.json'))
        sys.path.insert(0,str(Path(__file__).resolve().parent));from test_native_pts_adapter_045 import suite
        suite(root)
    else:raise ValueError('ROLE')
