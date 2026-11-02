"""076 explicit full-root constrained Yes/No screening; no import-time I/O.

Native Qwen processor components, fixed default chat template, 32 real frames,
matched-clock RGB black frames, and text-only. No generation or optimization.
"""
import argparse, collections, hashlib, io, itertools, json, math, os, re, time
from pathlib import Path

CONDITIONS=('REAL32','CLOCK_BLACK32','TEXT_ONLY')
PATTERN=r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.'
TEMPLATE='Does the event "{}" happen before the event "{}"? Answer Yes or No.'
MIB=1024**2
LIMITS={'old_metadata':32*MIB,'prepared':1024*MIB,'media_hash':128*MIB,'media_decode':128*MIB,'model_hash':12*1024**3}

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:f.write(packed(x)+'\n');f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(packed(dict(epoch=time.time(),**x))+'\n');f.flush();os.fsync(f.fileno())
def require(root,ok,reason,actual=None,limit=None):
 if not ok:event(Path(root)/'failures.jsonl',reason=reason,actual=actual,limit=limit);raise RuntimeError(reason)
def sealed(root):
 for x in read(Path(root)/'code-seal.json')['files']:assert sha(Path(x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256'],'CODE_CHANGED'
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def tau(q):
 m=re.fullmatch(PATTERN,q)
 if not m:raise ValueError('STRICT_QUESTION_PARSE')
 return TEMPLATE.format(m[2],m[1])
def rawtensor(t):return t.detach().contiguous().view(__import__('torch').uint8).numpy().tobytes()
def tensor_header(d):return {k:dict(dtype=str(v.dtype),shape=list(v.shape)) for k,v in sorted(d.items())}
def nonpixel_bytes(d):return packed(tensor_header(d)).encode()+b'\0'+b''.join(rawtensor(v) for k,v in sorted(d.items()))

class IO:
 """Explicit buffered logical reads; reusing one buffer is not a file reread."""
 def __init__(self,root,role):
  IO.current=self;self.root=Path(root);self.role=role;self.cache={};self.counts=collections.Counter();self.files=[];self.extra_catalog=None;self.previous=collections.Counter()
  for p in self.root.glob('*-io.json'):self.previous.update(read(p)['counts'])
 def charge(self,kind,n):
  self.counts[kind]+=n;require(self.root,self.previous[kind]+self.counts[kind]<=LIMITS[kind],'LOGICAL_READ_LIMIT',dict(kind=kind,bytes=self.previous[kind]+self.counts[kind]),LIMITS[kind])
 def data(self,p,kind='prepared',expected=None):
  p=Path(p).resolve();key=str(p)
  if kind=='old_metadata':
   par=read(self.root/'parent.json');allowed=p.is_relative_to(Path(par['prior074']).resolve()) or p==Path(par['prior075']).resolve()/'parent-closed.json' or p==self.extra_catalog
   require(self.root,allowed and (p.suffix in ('.json','.jsonl') or p.suffix=='.started' and p.parent.name=='model-calls'),'OLD_PATH_SCOPE',p.name,'registered metadata only')
   require(self.root,p.name not in ('api.json','answer_final.json','outputs.json'),'FORBIDDEN_OLD_PAYLOAD',p.name,'metadata/identity only')
  if key not in self.cache:
   n=p.stat().st_size;require(self.root,n<=LIMITS[kind],'OBJECT_READ_LIMIT',n,LIMITS[kind]);b=p.read_bytes();self.charge(kind,len(b));self.cache[key]=b;self.files.append(dict(path=key,kind=kind,bytes=len(b),sha256=sha(b)))
   (self.root/(self.role+'-io-progress.json')).write_text(packed(dict(counts=self.counts,files=self.files)),encoding='utf-8')
  b=self.cache[key]
  if expected:require(self.root,sha(b)==expected,'CONTENT_IDENTITY',p.name,'registered content digest')
  return b
 def meta(self,p,kind='prepared',expected=None):return json.loads(self.data(p,kind,expected).decode('utf-8-sig'))
 def tensor(self,p,expected=None):
  import torch
  return torch.load(io.BytesIO(self.data(p,'prepared',expected)),map_location='cpu',weights_only=True)
 def streamhash(self,p,kind):
  h=hashlib.sha256();n=0
  with open(p,'rb') as f:
   for b in iter(lambda:f.read(MIB),b''):n+=len(b);self.charge(kind,len(b));h.update(b)
  self.files.append(dict(path=str(p),kind=kind,bytes=n,sha256=h.hexdigest()));return h.hexdigest(),n
 def finish(self):save(self.root/(self.role+'-io.json'),dict(counts=self.counts,files=self.files))

def write_tensor(root,path,value):
 import torch
 b=io.BytesIO();torch.save(value,b);body=b.getvalue()
 with open(path,'xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
 return dict(path=str(path),file_sha256=sha(body),file_bytes=len(body))
def prompt(proc,q,video):
 content=([{'type':'video'}] if video else [])+[{'type':'text','text':q}]
 s=proc.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True)
 assert s.endswith('<|im_start|>assistant\n') and '<think>' not in s[s.rfind('<|im_start|>assistant'):],'INCOMPATIBLE_ASSISTANT_PREFIX'
 assert s.count(q)==1
 return s
def components(proc,q,video_fields=None,metadata=None):
 """Exact installed processor timestamp expansion, without recomputing pixels.

    The one native end-to-end CPU fixture compares every output tensor with this
    split implementation. Native video_processor and tokenizer remain unchanged.
 """
 s=prompt(proc,q,video_fields is not None)
 if video_fields is not None:
  grid=video_fields['video_grid_thw'];m=proc.video_processor.merge_size
  timestamps=proc._calculate_timestamps(list(metadata.frames_indices),metadata.fps,m)
  assert len(timestamps)==int(grid[0,0]);spatial=int(grid[0,1:].prod())//(m*m)
  expansion=''.join(f'<{tm:.1f} seconds>'+proc.vision_start_token+proc.video_token*spatial+proc.vision_end_token for tm in timestamps)
  placeholder=proc.vision_start_token+proc.video_token+proc.vision_end_token
  assert s.count(placeholder)==1;s=s.replace(placeholder,expansion,1)
 d=dict(proc.tokenizer(s,return_tensors='pt'))
 if video_fields is not None:
  assert not set(d)&set(video_fields);d.update(video_fields)
 assert all(__import__('torch').is_tensor(v) for v in d.values());assert d['input_ids'].shape[0]==1 and d['attention_mask'].shape==d['input_ids'].shape and bool((d['attention_mask']==1).all()) and d['input_ids'].shape[1]<=2048
 end=proc.tokenizer('<|im_start|>assistant\n',add_special_tokens=False)['input_ids'];assert d['input_ids'][0,-len(end):].tolist()==end
 if video_fields is None:assert int((d['input_ids']==proc.video_token_id).sum())==0
 else:assert int((d['input_ids']==proc.video_token_id).sum())==784
 return d,s

def assets(root):
 t=cpu();root=Path(root);sealed(root);a=IO(root,'assets');par=read(root/'parent.json');p=Path(par['prior074']);p75=Path(par['prior075'])
 old=a.meta(p/'parent-closed.json','old_metadata');assert old['push']=='SUCCEEDED' and old['all_jobs_actual_active_zero']
 old75=a.meta(p75/'parent-closed.json','old_metadata');assert old75['push']=='SUCCEEDED' and old75['gpu_operations']==0
 for name in ('decode','gpu','prediction','scoring','independent-review'):
  j=a.meta(p/(name+'-job.json'),'old_metadata');assert j['active']==j['exit_code']==0
 ins=a.meta(p/'input-seal.json','old_metadata');ds=a.meta(p/'decode-input-seal.json','old_metadata');cat=a.meta(p/'asset-catalog.json','old_metadata',ins['assets']);obs=a.meta(p/'observations.json','old_metadata',ins['observations']);media=a.meta(p/'media-manifest.json','old_metadata',ds['media_manifest'])
 assert len(obs)==len(media['records'])==24 and [x['index'] for x in obs]==list(range(24)) and sum(x['size'] for x in media['records'])==103041283
 qs=sorted({q for o in obs for q in o['questions']},key=lambda s:s.encode());assert len(qs)==28 and all(len(o['questions'])==6 for o in obs) and all(tau(q) in qs and tau(tau(q))==q for q in qs)
 fs=a.meta(p/'feature-seal.json','old_metadata');assert fs['status']=='CLOSED' and fs['counts']['root_forward']==0
 # Registered074calls are separated features, never full root QA.
 for f in sorted((p/'model-calls').glob('*.started')):
  x=a.meta(f,'old_metadata')
  assert x['mode'] in ('video_feature','text_feature') and f.with_suffix('.closed').is_file() and not f.with_suffix('.failed').exists()
 access=a.meta(p/'assets-access.json','old_metadata');registration=next(x for x in access['files'] if Path(x['path']).name=='asset-catalog.json' and Path(x['path']).parent.name=='vlm-private-068');a.extra_catalog=Path(registration['path']).resolve();parentcat=a.meta(a.extra_catalog,'old_metadata',registration['sha256'])
 assert parentcat['model_root']==cat['model_root'] and parentcat['model_file_sha256']==cat['source_model_identity']
 model_root=Path(cat['model_root']);hashes=cat['source_model_identity'];start=time.monotonic();weight_bytes=0
 for name,expected in hashes.items():
  actual,n=a.streamhash(model_root/name,'model_hash');weight_bytes+=n;require(root,actual==expected,'MODEL_IDENTITY',dict(file=name,matched=False,bytes=n),'registered identity')
 source_hashes=parentcat['runtime60']['installed_sources'];import sys
 for name,expected in source_hashes.items():assert sha((Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/name).read_bytes())==expected,'INSTALLED_SOURCE_IDENTITY'
 mediafacts=[]
 for x in media['records']:
  actual,n=a.streamhash(x['path'],'media_hash');require(root,actual==x['sha256'] and n==x['size'],'MEDIA_IDENTITY',dict(index=x['index'],size=n),dict(size=x['size']));st=Path(x['path']).stat();mediafacts.append(dict(x,mtime_ns=st.st_mtime_ns))
 cleanobs=[dict(index=x['index'],questions=x['questions']) for x in obs];save(root/'observations.json',cleanobs);save(root/'questions.json',qs);save(root/'media-source.json',mediafacts)
 gate=a.meta(p/'gate.json','old_metadata');member=next(n for n in gate['metadata_members'] if Path(n).name=='labels.json');manifest=next(n for n in gate['metadata_members'] if Path(n).name=='source-package-manifest.json')
 # Registration hashes the root derived-label copy without parsing truth.
 label_raw=a.data(p/'scoring-labels.json','old_metadata');save(root/'scoring-registration.json',dict(labels_path=str(p/'scoring-labels.json'),labels_sha256=sha(label_raw),handed_labels=str(p/'package'/member),manifest=str(p/'package'/manifest),member=member))
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 import numpy as np
 proc=AutoProcessor.from_pretrained(model_root,local_files_only=True,trust_remote_code=False)
 yes=proc.tokenizer('Yes',add_special_tokens=False)['input_ids'];no=proc.tokenizer('No',add_special_tokens=False)['input_ids'];require(root,len(yes)==len(no)==1 and yes!=no,'YES_NO_NOT_DISTINCT_SINGLE_TOKENS',dict(yes_n=len(yes),no_n=len(no)),1)
 synthetic=np.zeros((32,224,224,3),dtype=np.uint8);meta=VideoMetadata(total_num_frames=32,fps=32,duration=1,width=224,height=224,frames_indices=list(range(32)))
 save(root/'processor-fixture-started.json',dict(state='STARTED',calls=1,model_loads=0))
 fixtureq='Is this a software fixture? Answer Yes or No.'
 native=proc(text=[prompt(proc,fixtureq,True)],videos=[synthetic],video_metadata=[meta],do_sample_frames=False,do_resize=False,return_tensors='pt')
 assert native['video_grid_thw'].tolist()==[[16,14,14]] and list(native['pixel_values_videos'].shape)==[3136,1536]
 vf={k:v for k,v in native.items() if k!='pixel_values_videos'};split,_=components(proc,fixtureq,{k:v for k,v in vf.items() if k not in ('input_ids','attention_mask','token_type_ids')},meta)
 require(root,set(split)==set(vf) and all(t.equal(split[k],vf[k]) for k in vf),'SPLIT_PROCESSOR_FIXTURE_MISMATCH',list(vf),'native identical nonpixel fields')
 save(root/'processor-fixture.json',dict(status='PASS',calls=1,grid=[16,14,14],pixels=[3136,1536],visual_placeholders=784,split_component_matches_native=True,model_loads=0,root_forward=0))
 graph=dict(model_files=hashes,installed_sources=source_hashes,model_class='Qwen3VLForConditionalGeneration',dtype='bfloat16',attention='sdpa',use_cache=False,logits_to_keep=1,position='last_valid_assistant_first_continuation',yes_id=yes[0],no_id=no[0],decoder_layers=fs['counts']['decoder_layer_forward']//fs['counts']['decoder_forward']);save(root/'model-registration.json',dict(model_root=str(model_root),graph=graph,graph_sha256=sha(packed(graph).encode()),model_hash_bytes=weight_bytes,model_file_stats={n:dict(size=(model_root/n).stat().st_size,mtime_ns=(model_root/n).stat().st_mtime_ns) for n in hashes},asset_seconds=time.monotonic()-start,registered_prior_root_calls=0))
 save(root/'decode-plan-seal.json',dict(code_sha256=sha(a.data(root/'code-seal.json')),observations_sha256=sha(a.data(root/'observations.json')),media_source_sha256=sha(a.data(root/'media-source.json')),model_sha256=sha(a.data(root/'model-registration.json')),frames_per_video=32))
 a.finish();assert not t.cuda.is_initialized();print('ASSETS_TEMPLATE_SINGLE_TOKEN_ADMISSION_CLOSED',flush=True)

def decode(root):
 t=cpu();root=Path(root);sealed(root);a=IO(root,'decode');model=a.meta(root/'model-registration.json');obs=a.meta(root/'observations.json');qs=a.meta(root/'questions.json');source=a.meta(root/'media-source.json');plan=a.meta(root/'decode-plan-seal.json')
 for key,name in [('observations_sha256','observations.json'),('media_source_sha256','media-source.json'),('model_sha256','model-registration.json')]:assert sha(a.data(root/name))==plan[key]
 import av,numpy as np
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 proc=AutoProcessor.from_pretrained(model['model_root'],local_files_only=True,trust_remote_code=False)
 (root/'rgb').mkdir();(root/'pixels').mkdir();(root/'tokens').mkdir();pixels={};pixmemory={};tokens={};tokmemory={};frames=[];matrix=[];bycondition={c:[] for c in CONDITIONS};total=0;started=time.monotonic()
 def pixel_record(value):
  value=value.to(t.bfloat16);raw=rawtensor(value);key=sha(packed(dict(dtype=str(value.dtype),shape=list(value.shape))).encode()+b'\0'+raw)
  if key in pixels:assert pixmemory[key]==raw;return key
  rec=write_tensor(root,root/'pixels'/(key+'.pt'),value);rec.update(raw_sha256=sha(raw),shape=list(value.shape),dtype=str(value.dtype));pixels[key]=rec;pixmemory[key]=raw;return key
 def token_record(fields):
  raw=nonpixel_bytes(fields);key=sha(raw)
  if key in tokens:assert tokmemory[key]==raw;return key
  rec=write_tensor(root,root/'tokens'/(key+'.pt'),fields);rec.update(raw_sha256=key,header=tensor_header(fields),last_valid_position=int(fields['attention_mask'].sum())-1);tokens[key]=rec;tokmemory[key]=raw;return key
 class MediaReader:
  def __init__(self,path):self.f=open(path,'rb');self.bytes=0
  def read(self,n=-1):
   b=self.f.read(n);self.bytes+=len(b);a.charge('media_decode',len(b));return b
  def seek(self,*x):return self.f.seek(*x)
  def tell(self):return self.f.tell()
  def seekable(self):return True
 for src in source:
  i=src['index'];st=Path(src['path']).stat();assert st.st_size==src['size'] and st.st_mtime_ns==src['mtime_ns'];event(root/'decode-ledger.jsonl',event='STARTED',index=i)
  streamio=MediaReader(src['path'])
  with av.open(streamio) as container:
   s=container.streams.video[0];fps=float(s.average_rate or 0);nf=s.frames;duration=float(s.duration*s.time_base) if s.duration else float(container.duration/av.time_base) if container.duration else None;base=float((s.start_time or 0)*s.time_base)
   require(root,fps>0 and duration is not None and duration>0,'MEDIA_CLOCK_METADATA',dict(index=i,fps=fps,duration=duration),'positive known')
   targets=base+(np.arange(32)+.5)*duration/32;dist=np.full(32,np.inf);best=[None]*32;indices=[None]*32;stamps=[None]*32;n=0
   for j,frame in enumerate(container.decode(s)):
    n+=1;total+=1;require(root,total<=100000 and time.monotonic()-started<850,'DECODE_FRAME_OR_TIME_BUDGET',dict(frames=total,seconds=time.monotonic()-started),dict(frames=100000,seconds=900))
    if frame.pts is None:continue
    stamp=float(frame.pts*s.time_base);delta=np.abs(targets-stamp);update=np.where(delta<dist)[0]
    if len(update):
     rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
     for k in update:best[k]=rgb;indices[k]=j;stamps[k]=stamp;dist[k]=delta[k]
   require(root,all(v is not None for v in best) and len(set(indices))==32,'INSUFFICIENT_32_UNIQUE_FRAMES',dict(index=i,unique=len(set(indices)),traversed=n),32)
   error=max(abs(tm-base-idx/fps) for tm,idx in zip(stamps,indices));require(root,error<=1/fps,'FRAME_INDEX_CLOCK_NOT_CFR',dict(index=i,max_error=error),1/fps)
   real=np.stack(best);assert real.shape==(32,224,224,3) and real.dtype==np.uint8
   b=io.BytesIO();np.save(b,real,allow_pickle=False);rgbbody=b.getvalue();rgbpath=root/'rgb'/f'{i}.npy'
   with open(rgbpath,'xb') as out:out.write(rgbbody);out.flush();os.fsync(out.fileno())
   md=dict(total_num_frames=nf,fps=fps,duration=duration,width=224,height=224,frames_indices=indices)
   pairs=[]
   for condition,array in [('REAL32',real),('CLOCK_BLACK32',np.zeros_like(real))]:
    vd=proc.video_processor(videos=[array],video_metadata=[VideoMetadata(**md)],do_sample_frames=False,do_resize=False,return_metadata=True,return_tensors='pt');metadata=vd.pop('video_metadata')[0]
    assert list(metadata.frames_indices)==indices and metadata.fps==fps and metadata.duration==duration
    pixels_tensor=vd.pop('pixel_values_videos');assert list(pixels_tensor.shape)==[3136,1536] and t.isfinite(pixels_tensor).all();assert vd['video_grid_thw'].tolist()==[[16,14,14]] and all(t.is_tensor(v) for v in vd.values())
    pk=pixel_record(pixels_tensor);rows=[]
    for qi,q in enumerate(obs[i]['questions']):
     fields,_=components(proc,q,dict(vd),metadata);tk=token_record(fields);rows.append(dict(condition=condition,index=i,question=qi,token_key=tk,pixel_key=pk));bycondition[condition].append(rows[-1])
    pairs.append(rows)
   require(root,all(x['token_key']==y['token_key'] and tokmemory[x['token_key']]==tokmemory[y['token_key']] for x,y in zip(*pairs)),'REAL_BLACK_NONPIXEL_MISMATCH',i,'all actual nonpixel bytes equal')
   frames.append(dict(index=i,rgb_path=str(rgbpath),rgb_sha256=sha(rgbbody),rgb_bytes=len(rgbbody),container_frames=nf,actual_frames=n,fps=fps,duration=duration,base=base,time_base=str(s.time_base),indices=indices,timestamps=stamps,targets=targets.tolist(),max_clock_error=error,metadata=md,decode_input_bytes=streamio.bytes,real_pixel_key=pairs[0][0]['pixel_key'],black_pixel_key=pairs[1][0]['pixel_key']))
  streamio.f.close();event(root/'decode-ledger.jsonl',event='CLOSED',index=i,actual_frames=n,total_frames=total)
 textkeys={q:token_record(components(proc,q)[0]) for q in qs}
 for o in obs:
  for qi,q in enumerate(o['questions']):bycondition['TEXT_ONLY'].append(dict(condition='TEXT_ONLY',index=o['index'],question=qi,token_key=textkeys[q],pixel_key=None))
 for c in CONDITIONS:matrix.extend(bycondition[c])
 assert len(matrix)==432
 save(root/'prepared-index.json',dict(pixels=pixels,tokens=tokens,frames=frames,matrix=matrix,actual_decode_frames=total,real_black_nonpixel_pairs_checked=144,source_question_count=28,text_keys=textkeys))
 save(root/'prepared-seal.json',dict(status='CLOSED',index_sha256=sha(a.data(root/'prepared-index.json')),model_registration_sha256=sha(a.data(root/'model-registration.json')),observations_sha256=sha(a.data(root/'observations.json')),all_logical=432,pixel_blobs=len(pixels),token_blobs=len(tokens)))
 a.finish();assert not t.cuda.is_initialized();print('DECODE32_PREPARED_CLOSED',total,'pixelblobs',len(pixels),flush=True)

def input_gate(root):
 """Independent CPU input oracle before any Qwen weight load/forward."""
 t=cpu();root=Path(root);sealed(root);a=IO(root,'input-gate');ps=a.meta(root/'prepared-seal.json');p=a.meta(root/'prepared-index.json',expected=ps['index_sha256']);reg=a.meta(root/'model-registration.json',expected=ps['model_registration_sha256']);obs=a.meta(root/'observations.json',expected=ps['observations_sha256']);checks=0
 def test(v,why):
  nonlocal checks
  checks+=1;require(root,v,why,'independent pre-GPU input validation',True)
 from transformers import AutoProcessor
 import numpy as np
 proc=AutoProcessor.from_pretrained(reg['model_root'],local_files_only=True,trust_remote_code=False)
 y=proc.tokenizer('Yes',add_special_tokens=False)['input_ids'];n=proc.tokenizer('No',add_special_tokens=False)['input_ids'];test(y==[reg['graph']['yes_id']] and n==[reg['graph']['no_id']] and y!=n,'YES_NO_IDENTITY')
 pixelraw={};fields={}
 for key,r in p['pixels'].items():
  v=a.tensor(r['path'],r['file_sha256']);b=rawtensor(v);test(v.dtype==t.bfloat16 and v.shape==(3136,1536) and bool(t.isfinite(v).all()),'PIXEL_SHAPE_DTYPE_FINITE');test(sha(b)==r['raw_sha256'] and sha(packed(dict(dtype=str(v.dtype),shape=list(v.shape))).encode()+b'\0'+b)==key,'PIXEL_RAW_IDENTITY');pixelraw[key]=b
 for key,r in p['tokens'].items():
  d=a.tensor(r['path'],r['file_sha256']);test(sha(nonpixel_bytes(d))==key and tensor_header(d)==r['header'],'TOKEN_FIELD_IDENTITY');test(bool((d['attention_mask']==1).all()) and r['last_valid_position']==d['input_ids'].shape[1]-1,'LAST_VALID_TOKEN');fields[key]=d
 test(len(p['frames'])==24 and p['actual_decode_frames']==sum(x['actual_frames'] for x in p['frames'])<=100000,'FRAME_DENOMINATOR')
 for f in p['frames']:
  b=a.data(f['rgb_path'],expected=f['rgb_sha256']);rgb=np.load(io.BytesIO(b),allow_pickle=False);test(rgb.shape==(32,224,224,3) and rgb.dtype==np.uint8,'RGB32_SHAPE');test(len(f['indices'])==len(set(f['indices']))==32 and all(x<y for x,y in zip(f['indices'],f['indices'][1:])),'32_DISTINCT_INDICES');test(f['fps']>0 and f['max_clock_error']<=1/f['fps'] and f['metadata']['frames_indices']==f['indices'],'NATIVE_CLOCK')
 logical=[];unique=[];seen={};raws={};counts=collections.Counter()
 for row in p['matrix']:
  c=row['condition'];i=row['index'];qi=row['question'];q=obs[i]['questions'][qi];d=fields[row['token_key']];video=c!='TEXT_ONLY'
  content=([{'type':'video'}] if video else [])+[{'type':'text','text':q}]
  rendered=proc.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True)
  test(rendered.endswith('<|im_start|>assistant\n') and '<think>' not in rendered[rendered.rfind('<|im_start|>assistant'):],'ASSISTANT_POSITION')
  if video:
   f=p['frames'][i];idx=f['indices'];fps=f['fps'];times=[(idx[k]/fps+idx[k+1]/fps)/2 for k in range(0,32,2)]
   expansion=''.join('<%.1f seconds>'%tm+proc.vision_start_token+proc.video_token*49+proc.vision_end_token for tm in times);marker=proc.vision_start_token+proc.video_token+proc.vision_end_token;test(rendered.count(marker)==1,'ONE_VIDEO_PLACEHOLDER');rendered=rendered.replace(marker,expansion,1)
  expected=dict(proc.tokenizer(rendered,return_tensors='pt'))
  test(all(k in d and t.equal(v,d[k]) for k,v in expected.items()),'INDEPENDENT_DEFAULT_TEMPLATE_TOKENS')
  if video:test(d['video_grid_thw'].tolist()==[[16,14,14]] and int((d['input_ids']==proc.video_token_id).sum())==784,'GRID_AND_VISUAL_TOKENS')
  else:test(set(d)==set(expected) and row['pixel_key'] is None and int((d['input_ids']==proc.video_token_id).sum())==0,'TEXT_NO_VISION_CLOCK')
  header=dict(graph=reg['graph_sha256'],fields=tensor_header(d),pixel_dtype='torch.bfloat16' if video else None,pixel_shape=[3136,1536] if video else None)
  non=nonpixel_bytes(d);raw=pixelraw[row['pixel_key']] if video else None;signature=sha(packed(header).encode()+non+(sha(raw).encode() if raw is not None else b'NO_PIXEL'));full=(packed(header),non,raw)
  if signature in seen:test(raws[signature]==full,'FULL_BYTES_DEDUP');uid=seen[signature]
  else:
   uid=len(unique);seen[signature]=uid;raws[signature]=full;unique.append(dict(uid=uid,signature=signature,condition=c,index=i,question=qi,token_key=row['token_key'],pixel_key=row['pixel_key']));counts[c]+=1
  logical.append(dict(row,uid=uid,signature=signature))
 test(len(logical)==432 and len(unique)<=316,'FULL_FORWARD_CAP')
 bykey={(x['condition'],x['index'],x['question']):x for x in logical};test(set(bykey)==set(itertools.product(CONDITIONS,range(24),range(6))),'ALL_LOGICAL_KEYS')
 for i in range(24):
  for q in range(6):
   r=bykey['REAL32',i,q];b=bykey['CLOCK_BLACK32',i,q];test(nonpixel_bytes(fields[r['token_key']])==nonpixel_bytes(fields[b['token_key']]),'ALL_NONPIXEL_REAL_BLACK_EQUAL')
   test(p['frames'][i]['metadata']['frames_indices']==p['frames'][i]['indices'],'MATCHED_REAL_TIME_METADATA')
 save(root/'inference-plan.json',dict(unique=unique,logical=logical,unique_counts=dict(counts),root_upper_bound=316));save(root/'input-gate.json',dict(status='PASS',checks=checks,unique_inputs=len(unique),logical_inputs=432,real_black_pairs=144,weights_loaded=0,root_forward=0,plan_sha256=sha(a.data(root/'inference-plan.json'))))
 a.finish();assert not t.cuda.is_initialized();print('INDEPENDENT_INPUT_GATE_PASS',checks,'rootplan',len(unique),flush=True)

def gpu(root):
 import torch as t,gc
 from transformers import Qwen3VLForConditionalGeneration
 root=Path(root);sealed(root);a=IO(root,'gpu');gate=a.meta(root/'input-gate.json');assert gate['status']=='PASS' and read(root/'input-gate-job.json')['exit_code']==read(root/'input-gate-job.json')['active']==0
 plan=a.meta(root/'inference-plan.json',expected=gate['plan_sha256']);ps=a.meta(root/'prepared-seal.json');reg=a.meta(root/'model-registration.json',expected=ps['model_registration_sha256']);p=a.meta(root/'prepared-index.json',expected=ps['index_sha256']);start=read(root/'gpu-clock.json')['start_monotonic'];counts=dict(root_forward=0,visual_forward=0,decoder_forward=0,decoder_layer_forward=0,lm_head_forward=0);model=None;pxgpu={};tokgpu={};results=[];attempted=0
 for n,expected in reg['model_file_stats'].items():
  st=(Path(reg['model_root'])/n).stat();assert st.st_size==expected['size'] and st.st_mtime_ns==expected['mtime_ns'],'MODEL_FILE_CHANGED_AFTER_HASH'
 def hook(k):
  def increment(*args,**kwargs):counts[k]+=1
  return increment
 try:
  save(root/'weight-load-started.json',dict(state='STARTED',epoch=time.time()))
  model=Qwen3VLForConditionalGeneration.from_pretrained(reg['model_root'],local_files_only=True,trust_remote_code=False,torch_dtype=t.bfloat16,attn_implementation='sdpa').to('cuda');model.eval();model.requires_grad_(False)
  model.register_forward_pre_hook(hook('root_forward'));model.model.visual.register_forward_pre_hook(hook('visual_forward'));model.model.language_model.register_forward_pre_hook(hook('decoder_forward'));model.lm_head.register_forward_pre_hook(hook('lm_head_forward'))
  assert len(model.model.language_model.layers)==reg['graph']['decoder_layers']
  for layer in model.model.language_model.layers:layer.register_forward_pre_hook(hook('decoder_layer_forward'))
  with t.inference_mode():
   for u in plan['unique']:
    require(root,attempted<316 and time.monotonic()-start<540,'GPU_NEW_CALL_DEADLINE',dict(calls=attempted,elapsed=time.monotonic()-start),dict(calls=316,new_call_s=540,outer_s=600))
    tk=u['token_key'];pk=u['pixel_key']
    if tk not in tokgpu:
     rec=p['tokens'][tk];d=a.tensor(rec['path'],rec['file_sha256']);assert sha(nonpixel_bytes(d))==tk;tokgpu[tk]={k:v.to('cuda') for k,v in d.items()}
    fields=dict(tokgpu[tk])
    if pk is not None:
     if pk not in pxgpu:
      rec=p['pixels'][pk];v=a.tensor(rec['path'],rec['file_sha256']);assert sha(rawtensor(v))==rec['raw_sha256'];pxgpu[pk]=v.to('cuda')
     fields['pixel_values_videos']=pxgpu[pk]
    event(root/'forward-ledger.jsonl',event='STARTED',uid=u['uid'],signature=u['signature'],condition=u['condition'],elapsed=time.monotonic()-start);attempted+=1
    try:
     o=model(**fields,use_cache=False,return_dict=True,logits_to_keep=1);assert o.logits.shape[0:2]==(1,1)
     y=float(o.logits[0,0,reg['graph']['yes_id']].float().cpu());n=float(o.logits[0,0,reg['graph']['no_id']].float().cpu());margin=y-n;t.cuda.synchronize()
     require(root,math.isfinite(y) and math.isfinite(n) and math.isfinite(margin),'NONFINITE_YES_NO',u['uid'],'finite')
     require(root,t.cuda.max_memory_allocated()<=16*1024**3,'GPU_ALLOCATED_LIMIT',t.cuda.max_memory_allocated(),16*1024**3)
     results.append(dict(uid=u['uid'],signature=u['signature'],yes_logit=y,no_logit=n,margin=margin,prediction=int(margin>0),status='CLOSED'));event(root/'forward-ledger.jsonl',event='CLOSED',uid=u['uid'],signature=u['signature'])
    except Exception as e:event(root/'forward-ledger.jsonl',event='FAILED',uid=u['uid'],signature=u['signature'],reason=str(e));raise
    if attempted%40==0:print('COMPLETE_ROOT_CLOSED',attempted,flush=True)
  assert len(results)==len(plan['unique']) and counts['root_forward']==attempted and all(not v.requires_grad and v.grad is None for v in model.parameters())
  outputs=[];used=set()
  for row in plan['logical']:
   uid=row['uid'];kind='NEW' if uid not in used else 'ALIAS';used.add(uid);outputs.append(dict(condition=row['condition'],index=row['index'],question=row['question'],uid=uid,kind=kind,**{k:v for k,v in results[uid].items() if k not in ('uid','signature')}))
  assert len(outputs)==432;save(root/'unique-results.json',results);save(root/'outputs.json',outputs);save(root/'output-seal.json',dict(status='CLOSED',unique_sha256=sha(a.data(root/'unique-results.json')),outputs_sha256=sha(a.data(root/'outputs.json')),root_forward=attempted,logical=432,aliases=432-attempted,counts=counts,peak_allocated_bytes=t.cuda.max_memory_allocated(),weight_loads=1,generate=0,backward=0,optimizer=0))
 finally:
  peak=t.cuda.max_memory_allocated() if t.cuda.is_initialized() else 0;save(root/'gpu-counts.json',dict(attempted_root=attempted,counts=counts,peak_allocated_bytes=peak,elapsed=time.monotonic()-start,closed=len(results)))
  pxgpu.clear();tokgpu.clear();del model;gc.collect()
  if t.cuda.is_initialized():t.cuda.empty_cache();t.cuda.synchronize()
  a.finish()

def scoring(root):
 root=Path(root);sealed(root);a=IO(root,'scoring');j=a.meta(root/'gpu-job.json');assert j['active']==j['exit_code']==0 and not j['killed'];s=a.meta(root/'output-seal.json');assert s['status']=='CLOSED'
 out=a.meta(root/'outputs.json',expected=s['outputs_sha256']);obs=a.meta(root/'observations.json');look={(x['condition'],x['index'],x['question']):x for x in out};assert len(look)==len(out)==432 and set(look)==set(itertools.product(CONDITIONS,range(24),range(6)))
 sr=a.meta(root/'scoring-registration.json');ysroot=a.meta(sr['labels_path'],'old_metadata',sr['labels_sha256']);mf=a.meta(sr['manifest'],'old_metadata');entry=next(x for x in mf['members'] if x['path']==sr['member']);handed=a.meta(sr['handed_labels'],'old_metadata',entry['sha256']);ys=[]
 for i,(row,ref) in enumerate(zip(ysroot,handed)):
  assert row['index']==i and ref['order_valid'] is True and [x['question'] for x in ref['questions']]==obs[i]['questions'] and [x['label'] for x in ref['questions']]==row['labels'];ys.append(row['labels'])
 assert len(ys)==24 and all(len(x)==6 and sum(x)==3 for x in ys)
 canonical=collections.defaultdict(lambda:[[],[]])
 for i,o in enumerate(obs):
  for qi,q in enumerate(o['questions']):
   tq=tau(q);ti=o['questions'].index(tq);assert ys[i][qi]+ys[i][ti]==1
   if q.encode()<tq.encode():canonical[q][ys[i][qi]].append((i,qi,ti))
 quartets=[]
 for q in sorted(canonical,key=lambda q:q.encode()):
  neg,pos=canonical[q]
  for p0 in sorted(pos):
   for n0 in sorted(neg):quartets.append(dict(question=q,cells=[[p0[0],p0[1]],[p0[0],p0[2]],[n0[0],n0[1]],[n0[0],n0[2]]]))
 assert len(canonical)==14 and sum(bool(x[0] and x[1]) for x in canonical.values())==7 and len(quartets)==55
 conditions=[];detail={}
 for c in CONDITIONS:
  cnt=collections.Counter();items=[];videos=[];quads=[]
  for i,o in enumerate(obs):
   rows=[look[c,i,q] for q in range(6)];assert all(x['status']=='CLOSED' and math.isfinite(x['margin']) and x['margin']==x['yes_logit']-x['no_logit'] and x['prediction']==int(x['margin']>0) for x in rows)
   p=[x['prediction'] for x in rows];bits=[x==y for x,y in zip(p,ys[i])];items.extend(map(int,bits));videos.append(int(all(bits)));cnt['constant_videos']+=len(set(p))==1;cnt['complementary_pairs']+=sum(p[q]!=p[o['questions'].index(tau(o['questions'][q]))] for q in range(6))//2
   ev=sorted({x for q in o['questions'] for x in re.fullmatch(PATTERN,q).groups()},key=lambda s:s.encode());patterns={tuple(int(perm.index(m[1])<perm.index(m[2])) for m in (re.fullmatch(PATTERN,q) for q in o['questions'])) for perm in itertools.permutations(ev)};cnt['coherent_videos']+=tuple(p) in patterns
  for quad in quartets:quads.append(int(all(look[c,i,q]['prediction']==ys[i][q] for i,q in quad['cells'])))
  kinds=collections.Counter(x['kind'] for x in out if x['condition']==c);conditions.append(dict(condition=c,status='CLOSED',planned_items=144,planned_videos=24,planned_reverse_pairs=72,planned_quartets=55,CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,actual_new=kinds['NEW'],reused=0,aliases=kinds['ALIAS'],finite_items=144,parse_status='PASS',token_status='SINGLE_DISTINCT_YES_NO',correct_items=sum(items),correct_videos=sum(videos),correct_quartets=sum(quads),quartet_unknown=0,complementary_pairs=cnt['complementary_pairs'],coherent_videos=cnt['coherent_videos'],constant_videos=cnt['constant_videos'],item_accuracy_pct=100*sum(items)/144,six_way_accuracy_pct=100*sum(videos)/24,quartet_accuracy_pct=100*sum(quads)/55,complementary_pct=100*cnt['complementary_pairs']/72));detail[c]=dict(items=items,videos=videos,quartets=quads)
 require(root,sum(detail['TEXT_ONLY']['quartets'])==0,'TEXT_ONLY_QUARTET_LEAKAGE',sum(detail['TEXT_ONLY']['quartets']),0)
 pairs=[]
 for c in CONDITIONS[1:]:
  row=dict(left='REAL32',right=c,status='CLOSED')
  for measure,n in [('items',144),('videos',24),('quartets',55)]:
   l=detail['REAL32'][measure];r=detail[c][measure];lo=sum(x and not y for x,y in zip(l,r));ro=sum(y and not x for x,y in zip(l,r));row.update({measure+'_'+k:v for k,v in dict(planned=n,left_only=lo,right_only=ro,both_correct=sum(x and y for x,y in zip(l,r)),both_wrong=sum(not x and not y for x,y in zip(l,r)),unknown=0,net=lo-ro,delta_pp=100*(lo-ro)/n).items()})
  pairs.append(row)
 byc={x['condition']:x for x in conditions};passes=all(byc['REAL32']['correct_quartets']>byc[c]['correct_quartets'] and byc['REAL32']['correct_items']>=byc[c]['correct_items'] for c in CONDITIONS[1:])
 save(root/'quartets-private.json',quartets);save(root/'scoring-labels.json',ys);save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,canonical_questions=14,mixed_label_questions=7,quartets=55,text_quartet_guard='PASS',screen_passes=passes,conclusion='FULL_MODEL_RGB_EVIDENCE_PILOT_SIGNAL / NEW_MECHANISM_UNCONFIRMED' if passes else 'NO_SATISFYING_FULL_MODEL_VISUAL_SCREEN / STOP_NEW_ADAPTER_TRAINING_ON_THIS_ENTRY'))
 a.finish();print('SCORED_COMPLETE_ROOT_SCREEN',[(x['condition'],x['correct_items'],x['correct_quartets']) for x in conditions],flush=True)

def independent(root):
 """No producer scorer, Qwen call, processor call or second media decode.

    The independently coded input gate ran before weight load; this final pass
    rechecks persisted tensors/identities, all logits, aliases and outcome tables.
 """
 T=cpu();root=Path(root);sealed(root);a=IO(root,'independent-review');checks=0
 def test(x,reason):
  nonlocal checks
  checks+=1;require(root,x,reason,'independent verification',True)
 if not (root/'output-seal.json').exists() or not (root/'gpu-job.json').exists() or read(root/'gpu-job.json')['exit_code']!=0:
  save(root/'independent-review.json',dict(status='INCOMPLETE_STATE_REVIEW',checks=0,labels_read=0,root_forward_replay=0,reason='complete GPU output/exit0 absent'));a.finish();return
 gs=a.meta(root/'gpu-job.json');test(gs['active']==0 and not gs['killed'],'GPU_ACTUAL_ACTIVE_ZERO')
 ps=a.meta(root/'prepared-seal.json');p=a.meta(root/'prepared-index.json',expected=ps['index_sha256']);reg=a.meta(root/'model-registration.json',expected=ps['model_registration_sha256']);obs=a.meta(root/'observations.json',expected=ps['observations_sha256']);gate=a.meta(root/'input-gate.json');plan=a.meta(root/'inference-plan.json',expected=gate['plan_sha256']);s=a.meta(root/'output-seal.json');results=a.meta(root/'unique-results.json',expected=s['unique_sha256']);outputs=a.meta(root/'outputs.json',expected=s['outputs_sha256'])
 test(len(outputs)==432 and len(results)==len(plan['unique'])==s['root_forward']<=316,'ROOT_AND_LOGICAL_DENOMINATORS')
 tensors={};raws={}
 for key,record in p['pixels'].items():
  x=a.tensor(record['path'],record['file_sha256']);raw=x.detach().contiguous().view(T.uint8).numpy().tobytes();test(x.shape==(3136,1536) and x.dtype==T.bfloat16 and T.isfinite(x).all() and hashlib.sha256(raw).hexdigest()==record['raw_sha256'],'PIXEL_CONTENT_RECHECK');raws[key]=raw
 for key,record in p['tokens'].items():
  d=a.tensor(record['path'],record['file_sha256']);test(bool((d['attention_mask']==1).all()) and record['last_valid_position']==d['input_ids'].shape[1]-1,'FINAL_POSITION');tensors[key]=d
 import numpy as np
 for f in p['frames']:
  x=np.load(io.BytesIO(a.data(f['rgb_path'],expected=f['rgb_sha256'])),allow_pickle=False);test(x.dtype==np.uint8 and x.shape==(32,224,224,3) and len(set(f['indices']))==32,'REAL32_PERSISTED');test(f['max_clock_error']<=1/f['fps'],'FRAME_CLOCK_BOUND')
 def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
 sigraw={};unique_ids={}
 for u in plan['unique']:
  d=tensors[u['token_key']];head={k:dict(dtype=str(v.dtype),shape=list(v.shape)) for k,v in sorted(d.items())};non=canon(head).encode()+b'\0'+b''.join(v.detach().contiguous().view(T.uint8).numpy().tobytes() for k,v in sorted(d.items()));pixel=raws[u['pixel_key']] if u['pixel_key'] is not None else None
  h=dict(graph=reg['graph_sha256'],fields=head,pixel_dtype='torch.bfloat16' if pixel is not None else None,pixel_shape=[3136,1536] if pixel is not None else None);sig=hashlib.sha256(canon(h).encode()+non+(hashlib.sha256(pixel).hexdigest().encode() if pixel is not None else b'NO_PIXEL')).hexdigest();test(sig==u['signature'] and sig not in unique_ids,'COMPLETE_ROOT_INPUT_IDENTITY');unique_ids[sig]=u['uid'];sigraw[u['uid']]=(canon(h),non,pixel)
 lookup={(x['condition'],x['index'],x['question']):x for x in outputs};test(len(lookup)==len(outputs)==432 and set(lookup)==set(itertools.product(CONDITIONS,range(24),range(6))),'432_KEYS')
 used=set()
 for logical in plan['logical']:
  uid=logical['uid'];u=plan['unique'][uid];r=results[uid];o=lookup[logical['condition'],logical['index'],logical['question']]
  test(logical['signature']==u['signature']==r['signature'],'ALIAS_SIGNATURE');test(logical['token_key']==u['token_key'] and logical['pixel_key']==u['pixel_key'],'ALIAS_COMPLETE_FIELDS')
  test(r['status']=='CLOSED' and math.isfinite(r['yes_logit']) and math.isfinite(r['no_logit']) and r['margin']==r['yes_logit']-r['no_logit'] and r['prediction']==int(r['margin']>0),'FINITE_FIXED_YES_NO_RULE')
  test(all(o[k]==r[k] for k in ['yes_logit','no_logit','margin','prediction','status']),'LOGICAL_VALUE_EXACT_REUSE');test(o['kind']==('NEW' if uid not in used else 'ALIAS'),'LOGICAL_COST_BINDING');used.add(uid)
 bylogical={(x['condition'],x['index'],x['question']):x for x in plan['logical']}
 for i in range(24):
  for qi in range(6):
   rr=bylogical['REAL32',i,qi];bb=bylogical['CLOCK_BLACK32',i,qi];d=tensors[rr['token_key']];e=tensors[bb['token_key']];test(set(d)==set(e) and all(T.equal(d[k],e[k]) for k in d),'144_NONPIXEL_PAIRS')
 ledger=[json.loads(x) for x in a.data(root/'forward-ledger.jsonl').decode().splitlines()];beg=[x for x in ledger if x['event']=='STARTED'];end=[x for x in ledger if x['event']=='CLOSED'];test([x['uid'] for x in beg]==[x['uid'] for x in end]==list(range(len(results))) and len(ledger)==2*len(results),'STARTED_CLOSED_NO_RETRY')
 counts=s['counts'];test(counts['root_forward']==counts['decoder_forward']==counts['lm_head_forward']==len(results),'ROOT_DECODER_LMHEAD_COUNTS');test(counts['decoder_layer_forward']==len(results)*reg['graph']['decoder_layers'] and counts['visual_forward']==sum(u['pixel_key'] is not None for u in plan['unique']),'LOWER_LEVEL_COUNTS');test(s['peak_allocated_bytes']<=16*1024**3 and s['weight_loads']==1,'GPU_RESOURCE_GUARD')
 sr=a.meta(root/'scoring-registration.json');labels=a.meta(sr['labels_path'],'old_metadata',sr['labels_sha256']);mf=a.meta(sr['manifest'],'old_metadata');entry=next(x for x in mf['members'] if x['path']==sr['member']);handed=a.meta(sr['handed_labels'],'old_metadata',entry['sha256']);ys=[];reverseindices=[];coherence=[];canonical={}
 for i,o in enumerate(obs):
  test(labels[i]['index']==i and handed[i]['order_valid'] is True and [x['question'] for x in handed[i]['questions']]==o['questions'] and [x['label'] for x in handed[i]['questions']]==labels[i]['labels'],'LABEL_BINDING');y=labels[i]['labels'];ys.append(y);rev=[];events=set()
  for qi,q in enumerate(o['questions']):
   m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);test(m is not None,'STRICT_PARSE');events.update(m.groups());tq='Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(m[2],m[1]);ti=o['questions'].index(tq);test(y[qi]+y[ti]==1,'LABEL_COMPLEMENT');rev.append(ti)
   if q.encode()<tq.encode():canonical.setdefault(q,{0:[],1:[]})[y[qi]].append((i,qi,ti))
  reverseindices.append(rev);patterns=set()
  for perm in itertools.permutations(sorted(events,key=lambda x:x.encode())):
   pos={x:j for j,x in enumerate(perm)};patterns.add(tuple(int(pos[m[1]]<pos[m[2]]) for m in [re.fullmatch(PATTERN,q) for q in o['questions']]))
  test(len(events)==3 and len(patterns)==6 and tuple(y) in patterns,'VALID_COMPLETE_ORDER_LABELS');coherence.append(patterns)
 quartets=[]
 for q in sorted(canonical,key=lambda x:x.encode()):
  for pi,pq,pt in sorted(canonical[q][1]):
   for ni,nq,nt in sorted(canonical[q][0]):quartets.append(dict(question=q,cells=[[pi,pq],[pi,pt],[ni,nq],[ni,nt]]))
 test(len(canonical)==14 and sum(bool(v[0] and v[1]) for v in canonical.values())==7 and len(quartets)==55,'55_OBSERVATIONAL_QUARTETS');test(quartets==a.meta(root/'quartets-private.json'),'ALL_QUARTET_BINDINGS')
 agg=a.meta(root/'aggregates.json');detail={}
 for c in CONDITIONS:
  items=[];videos=[];quads=[];comp=constant=coherent=0
  for i,o in enumerate(obs):
   pred=[lookup[c,i,q]['prediction'] for q in range(6)];bits=[x==y for x,y in zip(pred,ys[i])];items.extend(map(int,bits));videos.append(int(all(bits)));comp+=sum(pred[q]!=pred[reverseindices[i][q]] for q in range(6))//2;constant+=len(set(pred))==1;coherent+=tuple(pred) in coherence[i]
  for q in quartets:quads.append(int(all(lookup[c,i,qi]['prediction']==ys[i][qi] for i,qi in q['cells'])))
  detail[c]=dict(items=items,videos=videos,quartets=quads);actual=next(x for x in agg['conditions'] if x['condition']==c);values=dict(correct_items=sum(items),correct_videos=sum(videos),correct_quartets=sum(quads),quartet_unknown=0,complementary_pairs=comp,coherent_videos=coherent,constant_videos=constant,CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,actual_new=sum(x['kind']=='NEW' for x in outputs if x['condition']==c),aliases=sum(x['kind']=='ALIAS' for x in outputs if x['condition']==c),reused=0,item_accuracy_pct=100*sum(items)/144,six_way_accuracy_pct=100*sum(videos)/24,quartet_accuracy_pct=100*sum(quads)/55)
  for k,v in values.items():test(abs(actual[k]-v)<1e-10,'CONDITION_'+k)
 test(sum(detail['TEXT_ONLY']['quartets'])==0,'TEXT_ONLY_ZERO_QUARTET_GUARD')
 textbyq={}
 for i,o in enumerate(obs):
  for qi,q in enumerate(o['questions']):
   pred=lookup['TEXT_ONLY',i,qi]['prediction']
   if q in textbyq:test(textbyq[q]==pred,'TEXT_ONLY_NO_VIDEO_DEPENDENCE')
   textbyq[q]=pred
 for control in CONDITIONS[1:]:
  actual=next(x for x in agg['pairs'] if x['right']==control)
  for measure,n in [('items',144),('videos',24),('quartets',55)]:
   l=detail['REAL32'][measure];r=detail[control][measure];lo=sum(x and not y for x,y in zip(l,r));ro=sum(y and not x for x,y in zip(l,r));values=dict(planned=n,left_only=lo,right_only=ro,both_correct=sum(x and y for x,y in zip(l,r)),both_wrong=sum(not x and not y for x,y in zip(l,r)),unknown=0,net=lo-ro,delta_pp=100*(lo-ro)/n)
   for k,v in values.items():test(abs(actual[measure+'_'+k]-v)<1e-10,'PAIR_'+measure+'_'+k)
 expected=all(sum(detail['REAL32']['quartets'])>sum(detail[c]['quartets']) and sum(detail['REAL32']['items'])>=sum(detail[c]['items']) for c in CONDITIONS[1:]);test(agg['screen_passes']==expected,'FROZEN_SCREEN_GATE')
 for phase in ['assets','decode','input-gate','gpu','scoring']:
  j=a.meta(root/(phase+'-job.json'));test(j['active']==j['exit_code']==0 and not j['killed'],'STAGE_CLOSURE')
 save(root/'independent-review.json',dict(status='PASS',checks=checks,pre_gpu_independent_checks=gate['checks'],producer_scorer_imports=0,root_forward_replay=0,media_decode_replay=0,text_quartet_zero=True,screen_passes=expected));a.finish();assert not T.cuda.is_initialized();print('INDEPENDENT_SCREEN_PASS',checks,flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('role',choices=['assets','decode','input_gate','gpu','scoring','independent']);p.add_argument('--root',required=True);args=p.parse_args();root=Path(args.root)
 try:globals()[args.role](root)
 except Exception as e:
  if hasattr(IO,'current') and not (root/(IO.current.role+'-io.json')).exists():IO.current.finish()
  event(root/'stops.jsonl',stage=args.role,reason=str(e) or type(e).__name__,error_type=type(e).__name__,action='STOP_NO_INPUT_RETRY');raise
if __name__=='__main__':main()
