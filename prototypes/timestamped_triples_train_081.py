"""081 persistent bounded Range recovery; unchanged science and public supervisor.

Perception Test: Google DeepMind; data CC-BY-4.0, software Apache-2.0.
Derived RGB sampling/permutation and supervision are local modifications.
No import-time data/model access. Execute roles under the sealed OS supervisor.
"""
import argparse,collections,hashlib,io,itertools,json,math,os,random,re,struct,time,bz2,zlib,gc,sys
from pathlib import Path
SEEDS=(19,73,101,137,181,229)
ARMS=('A','I','S')
PERMS=list(itertools.permutations(range(3)))
QP=list(itertools.permutations(range(3),2))
EDGES=[(i,j) for i,p in enumerate(PERMS) for j,q in enumerate(PERMS) if sum(a!=b for a,b in zip(p,q))==2 and next(k for k in range(3) if p[k]!=q[k])+1==max(k for k in range(3) if p[k]!=q[k])]
UEDGES=[e for e in EDGES if e[0]<e[1]]
CAPS={'prepared':12881150647,'old':6504611,'media':4279196643,'model':0}

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 with open(p,'xb') as f:f.write(packed(x)+b'\n');f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'ab') as f:f.write(packed(dict(epoch=time.time(),**x))+b'\n');f.flush();os.fsync(f.fileno())
def check(v,why):
 if not v:raise ValueError(why)
def raw(t):return t.detach().contiguous().view(__import__('torch').uint8).numpy().tobytes()
def header(d):return {k:dict(dtype=str(v.dtype),shape=list(v.shape)) for k,v in sorted(d.items())}
def nonbytes(d):return packed(header(d))+b'\0'+b''.join(raw(v) for k,v in sorted(d.items()))
def tsave(p,x):
 import torch
 b=io.BytesIO();torch.save(x,b);body=b.getvalue()
 with open(p,'xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
 return dict(path=str(p),bytes=len(body),sha256=sha(body))
class Reads:
 """Read-before durable reservations, with unknown outstanding reads retained."""
 def __init__(self,r,role):
  self.r=r;self.role=role;self.cache={};self.counts=collections.Counter();self.previous=collections.Counter();self.effective=collections.Counter();self.serial=0;reserved={};settled=set()
  ledger=r/'io-reservations.jsonl'
  if ledger.exists():
   for line in ledger.read_bytes().splitlines():
    x=json.loads(line);self.serial=max(self.serial,x['id'])
    if x['event']=='RESERVED':reserved[x['id']]=x;self.effective[x['kind']]+=x['reserved_bytes']
    elif x['event']=='SETTLED':
     z=reserved[x['id']];self.effective[z['kind']]+=x['actual_bytes']-z['reserved_bytes'];settled.add(x['id'])
  self.pending={i:x for i,x in reserved.items() if i not in settled}
 def reserve(self,kind,n,reference):
  check(kind in CAPS and isinstance(n,int) and n>=0 and self.effective[kind]+n<=CAPS[kind],'READ_RESERVATION_CAP_'+kind);self.serial+=1;ticket=(self.serial,kind,n);event(self.r/'io-reservations.jsonl',event='RESERVED',id=ticket[0],role=self.role,kind=kind,reserved_bytes=n,reference=str(reference),actual_bytes='UNKNOWN_UNTIL_SETTLED');self.effective[kind]+=n;self.pending[ticket[0]]=dict(kind=kind,reserved_bytes=n);return ticket
 def settle(self,ticket,n):
  ident,kind,maximum=ticket;check(0<=n<=maximum,'READ_ACTUAL_GT_RESERVED');event(self.r/'io-reservations.jsonl',event='SETTLED',id=ident,role=self.role,kind=kind,actual_bytes=n);self.effective[kind]+=n-maximum;self.counts[kind]+=n;self.pending.pop(ident,None)
 def file(self,p,kind='prepared'):
  p=str(p)
  if self.role=='train':check(Path(p).parent==self.r/'train' or Path(p).name in ('all-code-seals.json','parent.json'),'TRAIN_READ_ISOLATION')
  check(not p.endswith(('.safetensors','.bin')) or Path(p).name in ('central-directory.bin','archive-tail.bin'),'NO_WEIGHT_PAYLOAD_HASH_READ')
  if p not in self.cache:
   size=Path(p).stat().st_size;ticket=self.reserve(kind,size+1,p)
   with open(p,'rb') as f:body=f.read(size+1)
   self.settle(ticket,len(body));check(len(body)==size and Path(p).stat().st_size==size,'FILE_SIZE_CHANGED');self.cache[p]=body
  return self.cache[p]
 def meta(self,p,kind='prepared'):return json.loads(self.file(p,kind).decode('utf-8-sig'))
 def tensor(self,rec):
  import torch
  b=self.file(rec['path']);check(sha(b)==rec['sha256'],'TENSOR_FILE_HASH');return torch.load(io.BytesIO(b),map_location='cpu',weights_only=True)
 def finish(self):save(self.r/(self.role+'-io.json'),dict(counts=self.counts,effective_cumulative=self.effective,outstanding=list(self.pending.values()),scope='durable preread reserves and settled explicit logical buffered reads; not native/OS physical IO'))


def seals(r):
 records=json.loads((r/('all-code-seals-v2.json' if (r/'all-code-seals-v2.json').exists() else 'all-code-seals.json')).read_text(encoding='utf-8'))['files']
 for x in records:check(sha(Path(x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256'],'CODE_CHANGED')
def torchcpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch as t
 t.set_num_threads(4);t.set_num_interop_threads(1);check(not t.cuda.is_initialized(),'CPU_CUDA_INITIALIZED');return t

def head_class(t):
 class Head(t.nn.Module):
  def __init__(self):
   super().__init__();self.v=t.nn.Linear(2560,64);self.q=t.nn.Linear(2560,64);self.vn=t.nn.LayerNorm(64);self.qn=t.nn.LayerNorm(64);self.pos=t.nn.Parameter(t.zeros(18,64));self.read=t.nn.Linear(192,64);self.out=t.nn.Linear(64,1)
  def forward(self,v,q):
   v=self.vn(self.v(v))+self.pos;q=self.qn(self.q(q));a=((v*q.unsqueeze(-2)).sum(-1)/8).softmax(-1);z=(a.unsqueeze(-1)*v).sum(-2);q=q.expand_as(z);return self.out(t.nn.functional.gelu(self.read(t.cat((z,q,z*q),-1)))).squeeze(-1)
 return Head

def relation(t,logits,y,shuffled=False):
 p=logits.sigmoid();left=t.stack([p[:,a,:] for a,b in EDGES],1);right=t.stack([p[:,b,:] for a,b in EDGES],1);delta=t.stack([y[:,b,:]-y[:,a,:] for a,b in EDGES],1)
 if shuffled:delta=delta[:,:,[1,2,3,4,5,0]]
 return ((right-left-delta)**2).mean()

def fixture(r,a):
 t=torchcpu();H=head_class(t);t.manual_seed(3);m=H();check(sum(p.numel() for p in m.parameters())==341633,'HEAD_PARAMETER_COUNT');v=t.zeros(2,6,1,18,2560);q=t.ones(2,1,6,2560);y=t.tensor([[[int(p.index(x)<p.index(z)) for x,z in QP] for p in PERMS]]*2,dtype=t.float32);o=m(v,q);check(o.shape==(2,6,6),'HEAD_SHAPE')
 for i,j in EDGES:
  d=y[0,j]-y[0,i];s=d[[1,2,3,4,5,0]];check(int((d!=0).sum())==2 and not bool(((d!=0)&(s!=0)).any()),'SHUFFLE_RELEVANCE');check(sorted(d.tolist())==sorted(s.tolist()),'SHUFFLE_SIGNS')
 bce=t.nn.functional.binary_cross_entropy_with_logits(o,y);rel=relation(t,o,y);srel=relation(t,o,y,True);loss=bce+.25*rel;loss.backward();check(all(p.grad is not None and bool(t.isfinite(p.grad).all()) for p in m.parameters()),'SYNTHETIC_BACKWARD');check(any(bool((p.grad!=0).any()) for p in m.parameters()),'SYNTHETIC_NONZERO_GRAD')
 save(r/'head-fixture.json',dict(status='PASS',parameters=341633,synthetic_backward=1,optimizer_steps=0,edges=len(EDGES),unoriented_edges=len(UEDGES),shuffled_support_disjoint=True,real_data_read=0));a.finish()

def progress(r,stage,**kw):event(r/'progress.jsonl',role=os.environ.get('VLM_ROLE','unknown'),pid=os.getpid(),ppid=os.getppid(),stage=stage,**kw)








def prompt(proc,q,video):
 s=proc.apply_chat_template([{'role':'user','content':([{'type':'video'}] if video else [])+[{'type':'text','text':q}]}],tokenize=False,add_generation_prompt=True);check(s.endswith('<|im_start|>assistant\n'),'ASSISTANT_PREFIX');return s

def components(proc,q,video=None,md=None):
 s=prompt(proc,q,video is not None)
 if video is not None:
  times=proc._calculate_timestamps(list(md.frames_indices),md.fps,proc.video_processor.merge_size);check(len(times)==18,'TIMESTAMP_TUBELETS');s=s.replace(proc.vision_start_token+proc.video_token+proc.vision_end_token,''.join(f'<{x:.1f} seconds>'+proc.vision_start_token+proc.video_token*49+proc.vision_end_token for x in times))
 d=dict(proc.tokenizer(s,return_tensors='pt'))
 if video is not None:d.update(video)
 check(all(__import__('torch').is_tensor(x) for x in d.values()) and bool((d['attention_mask']==1).all()),'INPUT_FIELDS')
 check(int((d['input_ids']==proc.video_token_id).sum())==(882 if video is not None else 0),'VISUAL_PLACEHOLDERS');return d

def manifest(r,a):
 meta=r/'metadata';s=a.meta(meta/'summary.json');check(s['counts']==dict(videos=2135,actions=13644,eligible_segments=2678,candidate_triples=1376,eligible_videos=280),'METADATA_COUNTS');selected=a.meta(meta/'selected.json');answers=a.meta(meta/'answers.json');relations=a.meta(meta/'relations.json');check(len(selected)==32 and len(answers)==1152 and len(relations)==2304,'METADATA_MATRIX')
 import zipfile
 z=zipfile.ZipFile(io.BytesIO(a.file(meta/'action_localisation_train_annotations.zip')));ticket=a.reserve('prepared',z.getinfo('action_localisation_train.json').file_size,'annotation inflation');b=z.read('action_localisation_train.json');a.settle(ticket,len(b));source=json.loads(b);records=[]
 for g in selected:
  m=g['media'];check(m['method']==12 and m['flags']==0 and m['compressed']<=80*1024**2 and m['uncompressed']<=80*1024**2,'MEMBER_FLAGS_SIZE');md=source[g['observation']['video_id']]['metadata'];records.append(dict(group=g['rank'],split=g['split'],media=m,fps=md['frame_rate'],num_frames=md['num_frames'],events=g['observation']['events'],sampling=g['sampling'],questions=g['questions']))
 save(r/'media-plan.json',records);save(r/'observations.json',[dict(group=g['rank'],split=g['split'],questions=g['questions']) for g in selected]);save(r/'truth.json',answers);save(r/'relations.json',relations);save(r/'manifest-seal.json',dict(groups=32,source_frames=sum(x['num_frames'] for x in records),compressed=sum(x['media']['compressed'] for x in records),uncompressed=sum(x['media']['uncompressed'] for x in records),media_plan_sha256=sha(a.file(r/'media-plan.json'))));a.finish()


def decode_prepare(r,a):
 t=torchcpu();import av,numpy as np
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 reg=a.meta(r/'model-registration.json');proc=AutoProcessor.from_pretrained(reg['model_root'],local_files_only=True,trust_remote_code=False);plan=a.meta(r/'media-plan.json');media=a.meta(r/'media-manifest.json');check(len(media)==32,'ALL_MEDIA_REQUIRED');(r/'blocks').mkdir();(r/'pixels').mkdir();(r/'tokens').mkdir();pixels={};tokens={};pixelraw={};tokenraw={};frames=[];realrows=[];blackrows=[];textrows=[];total=0
 def px(v):
  v=v.to(t.bfloat16).contiguous();b=raw(v);key=sha(packed(dict(dtype=str(v.dtype),shape=list(v.shape)))+b'\0'+b)
  if key in pixels:check(pixelraw[key]==b,'PIXEL_COLLISION');return key
  rec=tsave(r/'pixels'/(key+'.pt'),v);rec.update(raw_sha256=sha(b),dtype=str(v.dtype),shape=list(v.shape));pixels[key]=rec;pixelraw[key]=b;return key
 def tok(d):
  b=nonbytes(d);key=sha(b)
  if key in tokens:check(tokenraw[key]==b,'TOKEN_COLLISION');return key
  rec=tsave(r/'tokens'/(key+'.pt'),d);rec.update(header=header(d),last_valid=int(d['attention_mask'].sum())-1);tokens[key]=rec;tokenraw[key]=b;return key
 class Source:
  def __init__(self,p):self.f=open(p,'rb');self.read_bytes=0
  def read(self,n=-1):
   maximum=n if n>=0 else os.fstat(self.f.fileno()).st_size-self.f.tell();ticket=a.reserve('media',maximum,'decoder media chunk');b=self.f.read(n);a.settle(ticket,len(b));self.read_bytes+=len(b);return b
  def seek(self,*args):return self.f.seek(*args)
  def tell(self):return self.f.tell()
  def seekable(self):return True
 runtime=VideoMetadata(total_num_frames=36,fps=12,duration=3,width=224,height=224,frames_indices=list(range(36)));black=np.zeros((36,224,224,3),dtype=np.uint8);vd=proc.video_processor(videos=[black],video_metadata=[runtime],do_sample_frames=False,do_resize=False,return_metadata=True,return_tensors='pt');md=vd.pop('video_metadata')[0];bp=px(vd.pop('pixel_values_videos'));vf=dict(vd);qtexts=sorted({q for x in plan for q in x['questions']},key=lambda x:x.encode());vt={q:tok(components(proc,q,vf,md)) for q in qtexts};tt={q:tok(components(proc,q)) for q in qtexts}
 for g,m in zip(plan,media):
  check(m['group']==g['group'],'MEDIA_GROUP');source=Source(m['path']);event(r/'decode-ledger.jsonl',event='STARTED',group=g['group']);targets=[x for z in g['sampling'] for x in z['seconds']];dist=[float('inf')]*36;best=[None]*36;indices=[None]*36;stamps=[None]*36;pts=[];tb=None
  with av.open(source) as container:
   stream=container.streams.video[0];stream.codec_context.thread_count=1;check(stream.codec_context.thread_count==1,'CODEC_THREAD_CONFIGURATION');fps=float(stream.average_rate or 0);check(abs(fps-g['fps'])<1e-3 and fps>0,'SOURCE_FPS');base=None
   for j,frame in enumerate(container.decode(stream)):
    total+=1;check(total<=100000,'DECODE_FRAME_CAP');check(stream.codec_context.thread_count==1 and frame.pts is not None,'DECODE_CLOCK_OR_THREADS');tb=str(stream.time_base);absolute=float(frame.pts*stream.time_base)
    if base is None:base=absolute
    stamp=absolute-base;check(math.isfinite(stamp) and (not pts or stamp>pts[-1]),'NONMONOTONIC_PTS');pts.append(stamp);updates=[k for k,v in enumerate(targets) if abs(stamp-v)<dist[k]]
    if updates:
     rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
     for k in updates:best[k]=rgb;indices[k]=j;stamps[k]=stamp;dist[k]=abs(stamp-targets[k])
   check(abs(len(pts)-g['num_frames'])<=1 and len(pts)>=2,'ACTUAL_FRAME_COUNT');actual_frame=max(pts[k+1]-pts[k] for k in range(len(pts)-1));check(actual_frame>0,'ACTUAL_FRAME_INTERVAL');endpoint_errors=[]
   for e in g['events']:
    for timestamp,index in zip(e['timestamps_us'],e['frame_ids']):
     check(int(index)==index and 0<=index<len(pts),'ANNOTATED_FRAME_ENDPOINT');error=abs(pts[int(index)]-timestamp/1e6);endpoint_errors.append(error);check(error<=actual_frame+1e-6,'ANNOTATION_PTS_ENDPOINT')
   order=sorted(g['events'],key=lambda e:e['timestamps_us'][0]);check(all(order[j+1]['timestamps_us'][0]-order[j]['timestamps_us'][1]>=100000 for j in (0,1)),'ACTUAL_SEGMENT_GAP')
   blocks=[];brecs=[]
   for slot,e in enumerate(g['events']):
    si=indices[slot*12:slot*12+12];st=stamps[slot*12:slot*12+12];check(len(set(si))==12 and all(e['timestamps_us'][0]/1e6<=v<=e['timestamps_us'][1]/1e6 for v in st),'INSUFFICIENT_SEGMENT_REAL_FRAMES');block=np.stack(best[slot*12:slot*12+12]);check(block.shape==(12,224,224,3) and block.dtype==np.uint8,'RGB_BLOCK');blocks.append(block);rec=tsave(r/'blocks'/f"{g['group']}-{slot}.pt",t.from_numpy(block));rec.update(rgb_raw_sha256=sha(block.tobytes()));brecs.append(rec)
   for pi,perm in enumerate(PERMS):
    rgb=np.concatenate([blocks[k] for k in perm],axis=0);d=proc.video_processor(videos=[rgb],video_metadata=[runtime],do_sample_frames=False,do_resize=False,return_metadata=True,return_tensors='pt');runtime_actual=d.pop('video_metadata')[0];pk=px(d.pop('pixel_values_videos'));check(d['video_grid_thw'].tolist()==[[18,14,14]],'REAL_GRID');check(all(t.equal(d[k],vf[k]) for k in vf),'ALL_RUNTIME_NONPIXEL_VIDEO_FIELDS')
    for qi,q in enumerate(g['questions']):
     fields=components(proc,q,d,runtime_actual);check(nonbytes(fields)==tokenraw[vt[q]],'REAL_BLACK_NONPIXEL_PAIR');realrows.append(dict(condition='REAL',group=g['group'],permutation=pi,question=qi,token_key=vt[q],pixel_key=pk));blackrows.append(dict(condition='BLACK',group=g['group'],permutation=pi,question=qi,token_key=vt[q],pixel_key=bp));textrows.append(dict(condition='TEXT',group=g['group'],permutation=pi,question=qi,token_key=tt[q],pixel_key=None))
   frames.append(dict(group=g['group'],actual_frames=len(pts),metadata_frames=g['num_frames'],fps=fps,time_base=tb,first_pts=base,relative_pts=pts,targets=targets,indices=indices,timestamps=stamps,actual_source_frame_tolerance=actual_frame+1e-6,endpoint_errors=endpoint_errors,codec_thread_count=1,blocks=brecs,media_read_bytes=source.read_bytes));event(r/'decode-ledger.jsonl',event='CLOSED',group=g['group'],frames=len(pts),codec_threads=1,total_traversed=total)
  source.f.close()
  if g['group']%4==3:print('RGB_PREPARED_SOURCE',g['group']+1,flush=True)
 save(r/'prepared-index.json',dict(pixels=pixels,tokens=tokens,frames=frames,matrix=realrows+blackrows+textrows,questions=qtexts,black_pixel_key=bp,total_frames=total));save(r/'prepared-seal.json',dict(index_sha256=sha(a.file(r/'prepared-index.json')),logical=3456,real_variants=192,real_blocks=96,all_runtime_clock='36frames/12fps/3seconds',nonpixel_pairs=1152));a.finish()

def input_gate(r,a):
 t=torchcpu();import numpy as np
 from transformers import AutoProcessor
 p=a.meta(r/'prepared-index.json');observations=a.meta(r/'observations.json');truth=a.meta(r/'truth.json');media=a.meta(r/'media-plan.json');reg=a.meta(r/'model-registration.json');proc=AutoProcessor.from_pretrained(reg['model_root'],local_files_only=True,trust_remote_code=False);checks=0
 def demand(v,why):
  nonlocal checks;checks+=1;check(v,'INPUT_ORACLE_'+why)
 pixelraw={};fields={}
 for key,rec in p['pixels'].items():
  v=a.tensor(rec);body=raw(v);demand(v.dtype==t.bfloat16 and tuple(v.shape)==(3528,1536) and bool(t.isfinite(v).all()),'PIXEL_SHAPE');demand(sha(body)==rec['raw_sha256'] and sha(packed(dict(dtype=str(v.dtype),shape=list(v.shape)))+b'\0'+body)==key,'PIXEL_HASH');pixelraw[key]=body
 for key,rec in p['tokens'].items():
  d=a.tensor(rec);demand(sha(nonbytes(d))==key and header(d)==rec['header'],'TOKEN_HASH');demand(bool((d['attention_mask']==1).all()) and rec['last_valid']==d['input_ids'].shape[1]-1,'LAST_VALID');fields[key]=d
 demand(len(p['frames'])==32 and sum(f['actual_frames'] for f in p['frames'])==p['total_frames']<=100000,'SOURCE_DENOMINATOR')
 for f,g in zip(p['frames'],media):
  demand(f['group']==g['group'] and f['codec_thread_count']==1 and abs(f['actual_frames']-g['num_frames'])<=1,'FRAME_CLOCK');pts=f['relative_pts'];demand(all(y>x for x,y in zip(pts,pts[1:])),'MONOTONIC')
  for k,target in enumerate(f['targets']):
   winner=min(range(len(pts)),key=lambda j:(abs(pts[j]-target),j));demand(winner==f['indices'][k] and pts[winner]==f['timestamps'][k],'NEAREST_REAL_PTS')
  for slot,(e,block) in enumerate(zip(g['events'],f['blocks'])):
   rgb=a.tensor(block);demand(tuple(rgb.shape)==(12,224,224,3) and rgb.dtype==t.uint8 and sha(raw(rgb))==block['rgb_raw_sha256'],'RGB_BLOCK');idx=f['indices'][slot*12:slot*12+12];demand(len(set(idx))==12 and all(e['timestamps_us'][0]/1e6<=pts[j]<=e['timestamps_us'][1]/1e6 for j in idx),'SEGMENT_BOUNDS')
    # Endpoints checked from full real PTS, not a shape assumption.
   for tm,j in zip(e['timestamps_us'],e['frame_ids']):demand(abs(pts[int(j)]-tm/1e6)<=f['actual_source_frame_tolerance'],'ENDPOINT')
 logical=[];unique=[];seen={};byteidentity={};counter=collections.Counter();labels={(x['group'],x['permutation'],x['question']):x['yes'] for x in truth};real_labels={}
 rows=sorted(p['matrix'],key=lambda x:((0,x['group'],x['permutation'],x['question']) if x['condition']=='REAL' else (1 if x['condition']=='BLACK' else 2,observations[x['group']]['questions'][x['question']].encode(),x['group'],x['permutation'])))
 for row in rows:
  d=fields[row['token_key']];q=observations[row['group']]['questions'][row['question']];video=row['pixel_key'] is not None
  content=([{'type':'video'}] if video else [])+[{'type':'text','text':q}];rendered=proc.apply_chat_template([{'role':'user','content':content}],tokenize=False,add_generation_prompt=True);demand(rendered.endswith('<|im_start|>assistant\n'),'ASSISTANT')
  if video:
   expansion=''.join(f'<{((2*j/12)+((2*j+1)/12))/2:.1f} seconds>'+proc.vision_start_token+proc.video_token*49+proc.vision_end_token for j in range(18));rendered=rendered.replace(proc.vision_start_token+proc.video_token+proc.vision_end_token,expansion)
  expected=dict(proc.tokenizer(rendered,return_tensors='pt'));demand(all(k in d and t.equal(v,d[k]) for k,v in expected.items()),'INDEPENDENT_TEMPLATE');demand(int((d['input_ids']==proc.video_token_id).sum())==(882 if video else 0),'VIDEO_PAD_COUNT')
  h=dict(graph=reg['graph_sha256'],fields=header(d),pixel_dtype='torch.bfloat16' if video else None,pixel_shape=[3528,1536] if video else None);non=nonbytes(d);body=pixelraw[row['pixel_key']] if video else None;signature=sha(packed(h)+non+(sha(body).encode() if body is not None else b'NO_PIXEL'));identity=(packed(h),non,body)
  if signature in seen:demand(byteidentity[signature]==identity,'EXACT_BYTE_ALIAS');uid=seen[signature]
  else:uid=len(unique);seen[signature]=uid;byteidentity[signature]=identity;unique.append(dict(row,uid=uid,signature=signature));counter[row['condition']]+=1
  if row['condition']=='REAL':
   label=labels[row['group'],row['permutation'],row['question']];demand(signature not in real_labels or real_labels[signature]==label,'REAL_IDENTICAL_INPUT_CONTRADICTORY_GOLD');real_labels[signature]=label
  logical.append(dict(row,uid=uid,signature=signature))
 demand(len(logical)==3456 and len(unique)<=1428 and len(p['questions'])==138,'MODEL_CALL_MATRIX');demand(set((x['condition'],x['group'],x['permutation'],x['question']) for x in logical)==set(itertools.product(('REAL','BLACK','TEXT'),range(32),range(6),range(6))),'LOGICAL_KEYS')
 lookup={(x['condition'],x['group'],x['permutation'],x['question']):x for x in logical}
 for g,pi,qi in itertools.product(range(32),range(6),range(6)):demand(lookup['REAL',g,pi,qi]['token_key']==lookup['BLACK',g,pi,qi]['token_key'],'MATCHED_NONPIXELS')
 old=a.meta(Path(a.meta(r/'parent.json')['prior076'])/'inference-plan.json','old');oldledger=a.file(Path(a.meta(r/'parent.json')['prior076'])/'forward-ledger.jsonl','old');states=collections.defaultdict(list)
 for line in oldledger.splitlines():
  x=json.loads(line);states[x['signature']].append(x['event'])
 demand(all(v==['STARTED','CLOSED'] for v in states.values()),'OLD_NO_UNRESOLVED_STARTED');oldsignatures={x['signature'] for x in old['unique']};demand(not oldsignatures&set(seen),'HISTORICAL_IDENTICAL_INPUT_REQUIRES_CACHED_FEATURE_NOT_REFORWARD')
 save(r/'inference-plan.json',dict(unique=unique,logical=logical,counts=dict(counter),root_upper_bound=1428));save(r/'input-gate.json',dict(status='PASS',checks=checks,unique_inputs=len(unique),logical_inputs=3456,aliases=3456-len(unique),real_nonpixel_pairs=1152,real_gold_collision='PASS',controls_opposite_gold='INTENTIONAL_Q_ONLY_CONTROLS_NOT_REAL_ADMISSION',historical_signature_intersection=0,plan_sha256=sha(a.file(r/'inference-plan.json'))));a.finish()
def gpu(r,a):
 import torch as t
 from transformers import Qwen3VLForConditionalGeneration
 t.set_num_threads(4);t.set_num_interop_threads(1);reg=a.meta(r/'model-registration.json');plan=a.meta(r/'inference-plan.json');gate=a.meta(r/'input-gate.json');p=a.meta(r/'prepared-index.json');check(gate['status']=='PASS','INPUT_GATE');counts=dict(root=0,visual=0,decoder=0,decoder_layer=0,lm_head=0);features={};qfeatures={};results=[];model=None;px=None;pk_current=None;tokens={};context={};start=a.meta(r/'gpu-clock.json')['start_monotonic'];(r/'features').mkdir()
 def count(k):
  def h(*x):counts[k]+=1
  return h
 def visual(module,args,out):
  if not context.get('capture_v'):return
  check(isinstance(out,tuple) and len(out)==2 and t.is_tensor(out[0]) and tuple(out[0].shape)==(882,2560),'MAIN_MERGER_RETURN_BINDING');v=out[0].detach().float().reshape(18,49,2560).mean(1).cpu();check(bool(t.isfinite(v).all()),'FINITE_V');key=context['pixel_key'];features[key]=tsave(r/'features'/('v-'+key+'.pt'),v);context['captured_v']=True
 def text(module,args,out):
  if not context.get('capture_q'):return
  check(hasattr(out,'last_hidden_state') and tuple(out.last_hidden_state.shape)==(1,context['sequence'],2560),'TEXT_LAST_HIDDEN_BINDING');q=out.last_hidden_state[0,-1].detach().float().cpu();check(bool(t.isfinite(q).all()),'FINITE_Q');key=context['token_key'];qfeatures[key]=tsave(r/'features'/('q-'+key+'.pt'),q);context['captured_q']=True
 try:
  for n,stat in reg['model_file_stats'].items():
   st=(Path(reg['model_root'])/n).stat();check(st.st_size==stat['size'] and st.st_mtime_ns==stat['mtime_ns'],'MODEL_STAT_CHANGED')
  for source_name,expected_source_hash in reg['graph']['installed_sources'].items():check(sha(a.file(Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/source_name))==expected_source_hash,'GPU_INSTALLED_SOURCE_CONTINUITY')
  save(r/'weight-load-started.json',dict(epoch=time.time(),state='STARTED'));model=Qwen3VLForConditionalGeneration.from_pretrained(reg['model_root'],local_files_only=True,trust_remote_code=False,torch_dtype=t.bfloat16,attn_implementation='sdpa').to('cuda');model.eval();model.requires_grad_(False);check(len(model.model.language_model.layers)==36,'DECODER_LAYER_IDENTITY');model.register_forward_pre_hook(count('root'));model.model.visual.register_forward_pre_hook(count('visual'));model.model.language_model.register_forward_pre_hook(count('decoder'));model.lm_head.register_forward_pre_hook(count('lm_head'))
  for layer in model.model.language_model.layers:layer.register_forward_pre_hook(count('decoder_layer'))
  model.model.visual.register_forward_hook(visual);model.model.language_model.register_forward_hook(text)
  with t.inference_mode():
   for u in plan['unique']:
    check(time.monotonic()-start<3480 and counts['root']<1428,'GPU_NEW_CALL_CUTOFF');tk=u['token_key'];pk=u['pixel_key']
    if tk not in tokens:
     d=a.tensor(p['tokens'][tk]);check(sha(nonbytes(d))==tk,'GPU_TOKEN_IDENTITY');tokens[tk]={k:v.to('cuda') for k,v in d.items()}
    fields=dict(tokens[tk])
    if pk is not None:
     if pk!=pk_current:
      px=None;t.cuda.empty_cache();v=a.tensor(p['pixels'][pk]);check(sha(raw(v))==p['pixels'][pk]['raw_sha256'],'GPU_PIXEL_IDENTITY');px=v.to('cuda');pk_current=pk
     fields['pixel_values_videos']=px
    context.clear();context.update(pixel_key=pk,token_key=tk,sequence=fields['input_ids'].shape[1],capture_v=pk is not None and pk not in features,capture_q=u['condition']=='TEXT' and tk not in qfeatures,captured_v=False,captured_q=False)
    event(r/'forward-ledger.jsonl',event='STARTED',uid=u['uid'],signature=u['signature'],condition=u['condition'],elapsed=time.monotonic()-start)
    try:
     out=model(**fields,use_cache=False,return_dict=True,logits_to_keep=1);check(tuple(out.logits.shape[:2])==(1,1),'LAST_LOGIT_SHAPE');yes=float(out.logits[0,0,reg['graph']['yes_id']].float().cpu());no=float(out.logits[0,0,reg['graph']['no_id']].float().cpu());t.cuda.synchronize();check(math.isfinite(yes) and math.isfinite(no),'FINITE_LOGITS');check(t.cuda.max_memory_allocated()<=16*1024**3,'ALLOCATED_LIMIT');check(not context['capture_v'] or context['captured_v'],'MISSING_V_HOOK');check(not context['capture_q'] or context['captured_q'],'MISSING_Q_HOOK');record=dict(uid=u['uid'],signature=u['signature'],yes_logit=yes,no_logit=no,margin=yes-no,prediction=int(yes-no>0),status='CLOSED');results.append(record);event(r/'forward-ledger.jsonl',event='CLOSED',**record)
    except Exception as e:event(r/'forward-ledger.jsonl',event='FAILED',uid=u['uid'],signature=u['signature'],reason=str(e));raise
    if counts['root']%60==0:print('FULL_ROOT_CLOSED',counts['root'],flush=True)
  check(counts['root']==len(plan['unique']) and all(not x.requires_grad and x.grad is None for x in model.parameters()),'ROOT_COUNTS_FREEZE');logical=[];used=set()
  for row in plan['logical']:
   uid=row['uid'];logical.append(dict(condition=row['condition'],group=row['group'],permutation=row['permutation'],question=row['question'],uid=uid,kind='NEW' if uid not in used else 'ALIAS',prediction=results[uid]['prediction'],status='CLOSED'));used.add(uid)
  check(len(logical)==3456 and len(qfeatures)==138,'FEATURE_COMPLETENESS');save(r/'baseline-outputs.json',logical);save(r/'unique-root-results.json',results);save(r/'feature-index.json',dict(v=features,q=qfeatures,black_pixel_key=p['black_pixel_key']));save(r/'gpu-output-seal.json',dict(logical=3456,unique=counts['root'],aliases=3456-counts['root'],counts=counts,V=len(features),Q=len(qfeatures),weight_loads=1,allocated_peak_bytes=t.cuda.max_memory_allocated(),root_results_sha256=sha(a.file(r/'unique-root-results.json')),outputs_sha256=sha(a.file(r/'baseline-outputs.json')),features_sha256=sha(a.file(r/'feature-index.json')),frozen_no_grad=True,generate=0,independent_feature_forwards=0))
 finally:
  save(r/'gpu-counts.json',dict(counts=counts,closed=len(results),captured_V=len(features),captured_Q=len(qfeatures),peak_allocated_bytes=t.cuda.max_memory_allocated() if t.cuda.is_initialized() else 0,worker_seconds=time.monotonic()-start));px=None;tokens.clear();model=None;gc.collect()
  if t.cuda.is_initialized():t.cuda.empty_cache();t.cuda.synchronize()
  a.finish()

def feature_pack(r,a):
 t=torchcpu();check(a.meta(r/'gpu-job.json')['active']==0 and a.meta(r/'gpu-job.json')['exit_code']==0,'GPU_MUST_EXIT_BEFORE_TRAIN');idx=a.meta(r/'feature-index.json');p=a.meta(r/'prepared-index.json');obs=a.meta(r/'observations.json');truth=a.meta(r/'truth.json');fmap={(x['group'],x['permutation'],x['question']):x for x in p['matrix'] if x['condition']=='REAL'};tmap={obs[x['group']]['questions'][x['question']]:x['token_key'] for x in p['matrix'] if x['condition']=='TEXT'};vs=t.stack([t.stack([a.tensor(idx['v'][fmap[g,pi,0]['pixel_key']]) for pi in range(6)]) for g in range(32)]);qs=t.stack([t.stack([a.tensor(idx['q'][tmap[q]]) for q in o['questions']]) for o in obs]);ys=t.empty(32,6,6)
 for x in truth:ys[x['group'],x['permutation'],x['question']]=x['yes']
 mean=vs[:20].reshape(120,18,2560).to(t.float64).sum(0).div(120).to(t.float32);black=a.tensor(idx['v'][idx['black_pixel_key']]);(r/'train').mkdir();train=tsave(r/'train'/'training.pt',dict(V=vs[:20].clone(),Q=qs[:20].clone(),Y=ys[:20].clone()));predict=tsave(r/'prediction-inputs.pt',dict(V=vs,Q=qs,BLACK=black,TRAIN_MEAN=mean));save(r/'train'/'manifest.json',dict(training=train,groups=20,items=720,b0_predictions_access=False,dev_test_labels_access=False));save(r/'prediction-input-index.json',predict);save(r/'feature-pack-seal.json',dict(train=train,prediction=predict,train_mean_source_variants=120,train_mean_raw_sha256=sha(raw(mean))));a.finish()

def train(r,a):
 t=torchcpu();H=head_class(t);manifest=a.meta(r/'train'/'manifest.json');data=a.tensor(manifest['training']);V,Q,Y=data['V'],data['Q'],data['Y'];check(V.shape==(20,6,18,2560) and Q.shape==(20,6,2560) and Y.shape==(20,6,6),'TRAIN_ONLY_TENSOR_SCHEMA');configs=[];updates=0
 for seed in SEEDS:
  t.manual_seed(seed);base=H();initial={k:v.detach().clone() for k,v in base.state_dict().items()};check(sum(x.numel() for x in base.parameters())==341633 and bool((base.pos==0).all()),'TRAIN_PARAMETERS');initialrec=tsave(r/'train'/f'initial-{seed}.pt',initial);rng=random.Random(seed);batches=[[rng.randrange(20) for _ in range(4)] for _ in range(250)];batchsha=sha(packed(batches));save(r/'train'/f'batches-{seed}.json',batches)
  for arm in ARMS:
   m=H();m.load_state_dict(initial);check(all(t.equal(m.state_dict()[k],v) for k,v in initial.items()),'MATCHED_INITIALIZATION');opt=t.optim.AdamW(m.parameters(),lr=1e-3,betas=(.9,.999),eps=1e-8,weight_decay=.01);closed=0;last=None
   for step,b in enumerate(batches,1):
    event(r/'training-ledger.jsonl',event='STARTED',seed=seed,arm=arm,step=step,batch_sha256=sha(packed(b)));opt.zero_grad(set_to_none=True);logits=m(V[b].unsqueeze(2),Q[b].unsqueeze(1));bce=t.nn.functional.binary_cross_entropy_with_logits(logits,Y[b]);rel=relation(t,logits,Y[b],arm=='S');loss=bce+(0 if arm=='A' else .25)*rel;check(bool(t.isfinite(loss)),'TRAIN_NONFINITE_LOSS');loss.backward();check(all(x.grad is not None and bool(t.isfinite(x.grad).all()) for x in m.parameters()),'TRAIN_GRADIENT_FINITE');opt.step();updates+=1;closed+=1;last=dict(loss=float(loss.detach()),bce=float(bce.detach()),relation=float(rel.detach()));event(r/'training-ledger.jsonl',event='CLOSED',seed=seed,arm=arm,step=step,backward=1,optimizer_step=1,**last)
   final={k:v.detach().clone() for k,v in m.state_dict().items()};changed=any(not t.equal(final[k],v) for k,v in initial.items());check(closed==250 and changed,'REAL_UPDATED_STATE');state=tsave(r/'train'/f'{arm}-{seed}.pt',final);configs.append(dict(seed=seed,arm=arm,state=state,initial=initialrec,batch_sha256=batchsha,updates=250,parameters=341633,last=last,changed=changed));print('TRAIN_CONFIG_CLOSED',seed,arm,'250',flush=True)
 check(updates==4500,'TRAIN_TOTAL');save(r/'training-seal.json',dict(configs=configs,updates=updates,steps_each=250,parameters=341633,optimizer='AdamW',lr=.001,betas=[.9,.999],eps=1e-8,weight_decay=.01,train_only=True));a.finish()

def predict(r,a):
 t=torchcpu();H=head_class(t);states=a.meta(r/'training-seal.json');d=a.tensor(a.meta(r/'prediction-input-index.json'));outputs=[];unique=0;byconfig=[]
 with t.inference_mode():
  for c in states['configs']:
   m=H();m.load_state_dict(a.tensor(c['state']));m.eval();cache={};rawcache={};before=unique
   for condition in ('REAL','BLACK','TRAIN_MEAN'):
    for g,pi,qi in itertools.product(range(32),range(6),range(6)):
     v=d['V'][g,pi] if condition=='REAL' else d[condition];q=d['Q'][g,qi];vb=raw(v);qb=raw(q);signature=sha(vb+qb)
     if signature in cache:check(rawcache[signature]==(vb,qb),'HEAD_INPUT_HASH_COLLISION');prediction=cache[signature];kind='ALIAS'
     else:
      logit=float(m(v,q));check(math.isfinite(logit),'HEAD_PREDICTION_FINITE');prediction=int(logit>0);cache[signature]=prediction;rawcache[signature]=(vb,qb);unique+=1;kind='NEW'
     outputs.append(dict(arm=c['arm'],seed=c['seed'],condition=condition,group=g,permutation=pi,question=qi,prediction=prediction,status='CLOSED',kind=kind))
   byconfig.append(dict(arm=c['arm'],seed=c['seed'],actual_new=unique-before,logical=3456,aliases=3456-(unique-before)));print('HEAD_PREDICTIONS_CLOSED',c['seed'],c['arm'],flush=True)
 check(len(outputs)==62208 and unique<=25704,'HEAD_OUTPUT_CAP');save(r/'head-outputs.json',outputs);save(r/'prediction-seal.json',dict(logical=62208,actual_new=unique,aliases=62208-unique,configs=byconfig,outputs_sha256=sha(a.file(r/'head-outputs.json'))));a.finish()
def metrics(rows,truth,groups):
 values={(x['group'],x['permutation'],x['question']):x for x in rows};groupstats=[]
 for g in groups:
  correct={(p,q):values[g,p,q]['status']=='CLOSED' and values[g,p,q]['prediction']==truth[g,p,q] for p,q in itertools.product(range(6),range(6))};quartets=[]
  for left,right in UEDGES:
   for q,rev in ((0,2),(1,4),(3,5)):
    ok=all(correct[p,qi] for p,qi in ((left,q),(left,rev),(right,q),(right,rev)));flip=truth[g,left,q]!=truth[g,right,q];quartets.append((ok,flip))
  groupstats.append(dict(group=g,items=sum(correct.values()),native=sum(all(correct[p,q] for q in range(6)) for p in range(6)),sources=int(all(correct.values())),quartets=sum(v for v,f in quartets),FLIP=sum(v for v,f in quartets if f),HOLD=sum(v for v,f in quartets if not f)))
 n=len(groups);out=dict(planned_source_groups=n,planned_items=36*n,planned_native_variants=6*n,planned_quartets=18*n,planned_FLIP=6*n,planned_HOLD=12*n,closed=sum(x['status']=='CLOSED' for x in rows),unknown=sum(x['status']!='CLOSED' for x in rows),actual_new=sum(x['kind']=='NEW' for x in rows),aliases=sum(x['kind']=='ALIAS' for x in rows),status='CLOSED')
 for k,den in [('items',36*n),('native',6*n),('sources',n),('quartets',18*n),('FLIP',6*n),('HOLD',12*n)]:out['correct_'+k]=sum(x[k] for x in groupstats);out[k+'_pct']=100*out['correct_'+k]/den
 return out,groupstats

def scoring(r,a):
 truthrows=a.meta(r/'truth.json');truth={(x['group'],x['permutation'],x['question']):x['yes'] for x in truthrows};base=a.meta(r/'baseline-outputs.json');heads=a.meta(r/'head-outputs.json');check(len(base)==3456 and len(heads)==62208,'ALL_OUTPUTS_BEFORE_SCORE');splits=dict(train=list(range(20)),development=list(range(20,24)),test=list(range(24,32)));brows=[];hrows=[];groups={};guards=[]
 for split,gs in splits.items():
  for condition in ('REAL','BLACK','TEXT'):
   rs=[x for x in base if x['condition']==condition and x['group'] in gs];m,g=metrics(rs,truth,gs);brows.append(dict(split=split,condition=condition,**m));groups['B0/'+condition+'/'+split]=g
   if condition!='REAL':guards.append(m['correct_items']==18*len(gs) and m['correct_sources']==0)
  for condition,arm,seed in itertools.product(('REAL','BLACK','TRAIN_MEAN'),ARMS,SEEDS):
   rs=[x for x in heads if x['condition']==condition and x['arm']==arm and x['seed']==seed and x['group'] in gs];m,g=metrics(rs,truth,gs);hrows.append(dict(split=split,condition=condition,arm=arm,seed=seed,**m));groups[f'{arm}/{seed}/{condition}/{split}']=g
   if condition!='REAL':guards.append(m['correct_items']==18*len(gs) and m['correct_sources']==0)
 check(all(guards),'FIXED_INPUT_Q_ONLY_SOFTWARE_GUARD');pairs=[];uncertainty=[]
 for split,gs in splits.items():
  for other in ('A','S'):
   seedpairs=[]
   for seed in SEEDS:
    left=groups[f'I/{seed}/REAL/{split}'];right=groups[f'{other}/{seed}/REAL/{split}'];lc=sum(x['sources'] for x in left);rc=sum(x['sources'] for x in right);cor=sum(x['sources']==1 and y['sources']==0 for x,y in zip(left,right));harm=sum(x['sources']==0 and y['sources']==1 for x,y in zip(left,right));record=dict(split=split,left='I',right=other,seed=seed,seed_count=1,independent_source_groups=len(gs),left_correct_sources=lc,right_correct_sources=rc,corrected=cor,harmed=harm,net=lc-rc,delta_pp=100*(lc-rc)/len(gs),status='CLOSED');pairs.append(record);seedpairs.append(record)
   agg={k:sum(x[k] for x in seedpairs) for k in ('left_correct_sources','right_correct_sources','corrected','harmed','net')};pairs.append(dict(split=split,left='I',right=other,seed='mean',seed_count=6,independent_source_groups=len(gs),**agg,delta_pp=100*agg['net']/(6*len(gs)),status='CLOSED'))
   if split=='test':
    diff=[sum(groups[f'I/{s}/REAL/test'][i]['sources']-groups[f'{other}/{s}/REAL/test'][i]['sources'] for s in SEEDS) for i in range(8)];observed=sum(diff);extreme=sum(abs(sum(sign*x for sign,x in zip(signs,diff)))>=abs(observed) for signs in itertools.product((-1,1),repeat=8));uncertainty.append(dict(comparison='I-'+other,source_seed_sum_differences=diff,source_mean_differences=[x/6 for x in diff],exact_sign_flips=256,two_sided_tail_numerator=extreme,tail=extreme/256,scope='descriptive source-paired null reference; not independent seeds/confirmatory inference'))
 def row(arm,seed,condition='REAL'):return next(x for x in hrows if x['split']=='test' and x['arm']==arm and x['seed']==seed and x['condition']==condition)
 isum={k:sum(row('I',s)['correct_'+k] for s in SEEDS) for k in ('sources','items','FLIP','HOLD')};other={arm:{k:sum(row(arm,s)['correct_'+k] for s in SEEDS) for k in isum} for arm in ('A','S')};b0=next(x for x in brows if x['split']=='test' and x['condition']=='REAL');gate=dict(complete=True,software_guards='PASS',seeds_strictly_above_both=sum(row('I',s)['correct_sources']>row('A',s)['correct_sources'] and row('I',s)['correct_sources']>row('S',s)['correct_sources'] for s in SEEDS),I_test_source_sum=isum['sources'],net_source_sums={k:isum['sources']-v['sources'] for k,v in other.items()},item_flip_hold_not_lower=all(isum[k]>=v[k] for v in other.values() for k in ('items','FLIP','HOLD')),not_lower_B0_items=isum['items']>=6*b0['correct_items'],strictly_above_B0_sources=isum['sources']>6*b0['correct_sources'],above_own_fixed_controls=all(isum['sources']>sum(row('I',s,c)['correct_sources'] for s in SEEDS) for c in ('BLACK','TRAIN_MEAN')),I_item_at_least50pct=isum['items']>=6*144)
 gate['passes']=gate['seeds_strictly_above_both']>=5 and gate['I_test_source_sum']>=12 and all(x>=6 for x in gate['net_source_sums'].values()) and all(gate[k] for k in ('item_flip_hold_not_lower','not_lower_B0_items','strictly_above_B0_sources','above_own_fixed_controls','I_item_at_least50pct'))
 conclusion='QUESTION_RELEVANT_RELATION_PILOT_SIGNAL / NEW_MECHANISM_UNCONFIRMED' if gate['passes'] else 'NO_SATISFYING_JOINT_SUPERVISION_SIGNAL / STOP_THIS_RECIPE';check(len(brows)==9 and len(hrows)==162 and len(pairs)==42,'SUMMARY_ROW_COUNTS');save(r/'aggregate-results.json',dict(baseline=brows,heads=hrows,paired=pairs,gate=gate,conclusion=conclusion));save(r/'source-statistics.json',groups);save(r/'source-uncertainty.json',uncertainty);a.finish()

def independent_science(r,a):
 """Presealed independent oracle; never imports producer training/scorer functions.

 No head/model forward or media decode. On early failure, closure-only review.
 """
 checks=0
 def demand(v,why):
  nonlocal checks;checks+=1;check(v,'FINAL_ORACLE_'+why)
 jobs={p.name[:-9]:a.meta(p) for p in r.glob('*-job.json')}
 for name,j in jobs.items():demand(j['active']==0,'ACTUAL_JOB_ZERO_'+name)
 if not (r/'aggregate-results.json').exists():
  save(r/'independent-final.json',dict(status='STOP_STATE_ONLY_SCIENTIFIC_NOT_REVIEWED',checks=checks,phase_jobs=list(jobs),data_model_training_oracle='NOT_RUN',audit_code_presealed=True,model_head_decode_replays=0));a.finish();return
 import torch as t
 t.set_num_threads(4);t.set_num_interop_threads(1)
 answers=a.meta(r/'truth.json');lookup={(x['group'],x['permutation'],x['question']):x['yes'] for x in answers};base=a.meta(r/'baseline-outputs.json');heads=a.meta(r/'head-outputs.json');aggregate=a.meta(r/'aggregate-results.json');stored=a.meta(r/'source-statistics.json');plan=a.meta(r/'inference-plan.json');rootresults=a.meta(r/'unique-root-results.json');fseal=a.meta(r/'gpu-output-seal.json');hseal=a.meta(r/'prediction-seal.json');training=a.meta(r/'training-seal.json');ledger=[json.loads(x) for x in a.file(r/'training-ledger.jsonl').splitlines()];demand(len(base)==3456 and len(heads)==62208,'FULL_DENOMINATORS');demand(len(rootresults)==len(plan['unique'])==fseal['unique']<=1428,'ROOT_UNIQUE');demand(fseal['frozen_no_grad'] and fseal['independent_feature_forwards']==0 and fseal['generate']==0,'FROZEN_FULL_GRAPH');demand(fseal['counts']['root']==fseal['counts']['decoder']==fseal['counts']['lm_head']==len(rootresults) and fseal['counts']['decoder_layer']==36*len(rootresults),'HOOK_COUNTS')
 for x in rootresults:demand(math.isfinite(x['yes_logit']) and math.isfinite(x['no_logit']) and x['margin']==x['yes_logit']-x['no_logit'] and x['prediction']==int(x['margin']>0) and x['status']=='CLOSED','TWO_LOGIT_RULE')
 unique={x['uid']:x for x in rootresults};bindings={(x['condition'],x['group'],x['permutation'],x['question']):x['uid'] for x in plan['logical']};demand(len(bindings)==3456,'BASE_KEYS')
 for x in base:demand(x['prediction']==unique[bindings[x['condition'],x['group'],x['permutation'],x['question']]]['prediction'],'BASE_ALIAS_BINDING')
 demand(sum(x['kind']=='NEW' for x in heads)==hseal['actual_new']<=25704 and hseal['aliases']+hseal['actual_new']==62208,'HEAD_ALIAS_COUNTS');demand(len({(x['seed'],x['arm'],x['condition'],x['group'],x['permutation'],x['question']) for x in heads})==62208,'HEAD_LOGICAL_KEYS')
 steps=collections.defaultdict(list)
 for x in ledger:steps[x['seed'],x['arm'],x['step']].append(x)
 demand(len(steps)==4500 and training['updates']==4500,'TRAIN_UPDATE_COUNT')
 for (seed,arm,step),events in steps.items():demand([x['event'] for x in events]==['STARTED','CLOSED'] and events[1]['backward']==events[1]['optimizer_step']==1 and math.isfinite(events[1]['loss']),'STEP_LEDGER')
 for seed in (19,73,101,137,181,229):
  configs=[x for x in training['configs'] if x['seed']==seed];demand(len(configs)==3 and {x['arm'] for x in configs}=={'A','I','S'} and len({x['initial']['sha256'] for x in configs})==len({x['batch_sha256'] for x in configs})==1,'SAME_INITIAL_AND_BATCH');rng=random.Random(seed);batch=[[rng.randrange(20) for _ in range(4)] for _ in range(250)];demand(sha(packed(batch))==configs[0]['batch_sha256'],'FIXED_BATCH_STREAM')
  initial=a.tensor(configs[0]['initial']);demand(sum(v.numel() for v in initial.values())==341633 and tuple(initial['pos'].shape)==(18,64) and bool((initial['pos']==0).all()),'ACTUAL_PARAMETER_STATE')
  for c in configs:
   final=a.tensor(c['state']);demand(sum(v.numel() for v in final.values())==341633 and c['updates']==250 and any(not t.equal(final[k],initial[k]) for k in initial),'UPDATED_FINAL_STATE')
 # Independent output reductions: build native truth vector directly and enumerate
 # swaps by adjacent position, never call metrics(), scoring(), relation() or Head.
 truth={}
 for g in range(32):
  for pi,p in enumerate(itertools.permutations((0,1,2))):
   for qi,(left,right) in enumerate(((0,1),(0,2),(1,0),(1,2),(2,0),(2,1))):truth[g,pi,qi]=int(list(p).index(left)<list(p).index(right));demand(truth[g,pi,qi]==lookup[g,pi,qi],'SYMBOLIC_TRUTH')
 def reduction(rows,groups):
  table={(x['group'],x['permutation'],x['question']):x for x in rows};answer=[]
  for g in groups:
   ok=[[table[g,pi,qi]['prediction']==truth[g,pi,qi] and table[g,pi,qi]['status']=='CLOSED' for qi in range(6)] for pi in range(6)];record=dict(group=g,items=sum(sum(x) for x in ok),native=sum(all(x) for x in ok),sources=int(all(all(x) for x in ok)),quartets=0,FLIP=0,HOLD=0);perms=list(itertools.permutations((0,1,2)))
   for pi,p in enumerate(perms):
    for swap in (0,1):
     order=list(p);order[swap],order[swap+1]=order[swap+1],order[swap];pj=perms.index(tuple(order))
     if pj<pi:continue
     for qi,qrev in ((0,2),(1,4),(3,5)):
      complete=ok[pi][qi] and ok[pi][qrev] and ok[pj][qi] and ok[pj][qrev];record['quartets']+=int(complete);record['FLIP' if truth[g,pi,qi]!=truth[g,pj,qi] else 'HOLD']+=int(complete)
   answer.append(record)
  return answer
 newgroups={}
 for row in aggregate['baseline']+aggregate['heads']:
  split=row['split'];gs=list(range(20)) if split=='train' else list(range(20,24)) if split=='development' else list(range(24,32));ishead='arm' in row;rows=[x for x in (heads if ishead else base) if x['condition']==row['condition'] and x['group'] in gs and (not ishead or x['arm']==row['arm'] and x['seed']==row['seed'])];out=reduction(rows,gs);key=f"{row['arm']}/{row['seed']}/{row['condition']}/{split}" if ishead else f"B0/{row['condition']}/{split}";demand(out==stored[key],'PER_SOURCE_REDUCTION');newgroups[key]=out
  for k in ('items','native','sources','quartets','FLIP','HOLD'):demand(sum(x[k] for x in out)==row['correct_'+k],'AGGREGATE_INTEGER')
  demand(row['closed']==len(rows)==len(gs)*36 and row['unknown']==0 and row['actual_new']+row['aliases']==len(rows),'ROW_DENOMINATORS')
  if row['condition']!='REAL':demand(sum(x['items'] for x in out)==18*len(gs) and sum(x['sources'] for x in out)==0,'CONTROL_SOFTWARE_GUARD')
 seeds=(19,73,101,137,181,229);source=lambda arm,s,c='REAL':newgroups[f'{arm}/{s}/{c}/test'];total=lambda arm,k:sum(sum(x[k] for x in source(arm,s)) for s in seeds);b0=newgroups['B0/REAL/test'];positive=sum(sum(x['sources'] for x in source('I',s))>max(sum(x['sources'] for x in source('A',s)),sum(x['sources'] for x in source('S',s))) for s in seeds);passes=positive>=5 and total('I','sources')>=12 and all(total('I','sources')-total(arm,'sources')>=6 for arm in ('A','S')) and all(total('I',k)>=total(arm,k) for arm in ('A','S') for k in ('items','FLIP','HOLD')) and total('I','sources')>6*sum(x['sources'] for x in b0) and total('I','items')>=6*sum(x['items'] for x in b0) and all(total('I','sources')>sum(sum(x['sources'] for x in source('I',s,c)) for s in seeds) for c in ('BLACK','TRAIN_MEAN')) and total('I','items')>=864;demand(bool(passes)==aggregate['gate']['passes'],'INDEPENDENT_COMPLETE_GATE')
 for row in aggregate['paired']:
  split=row['split'];ss=seeds if row['seed']=='mean' else [row['seed']];left=sum(sum(x['sources'] for x in newgroups[f'I/{s}/REAL/{split}']) for s in ss);right=sum(sum(x['sources'] for x in newgroups[f"{row['right']}/{s}/REAL/{split}"]) for s in ss);demand(row['left_correct_sources']==left and row['right_correct_sources']==right and row['net']==left-right and row['corrected']-row['harmed']==left-right,'PAIRED_COUNTS')
 uncertainty=a.meta(r/'source-uncertainty.json')
 for x in uncertainty:
  arm=x['comparison'].split('-')[1];diff=[sum(source('I',s)[i]['sources']-source(arm,s)[i]['sources'] for s in seeds) for i in range(8)];all_signs=list(itertools.product((-1,1),repeat=8));n=sum(abs(sum(v*sg for v,sg in zip(diff,sign)))>=abs(sum(diff)) for sign in all_signs);demand(diff==x['source_seed_sum_differences'] and x['two_sided_tail_numerator']==n and x['tail']==n/256,'SIGN_FLIP_REFERENCE')
 save(r/'independent-final.json',dict(status='PASS',checks=checks,scientific_gate=bool(passes),audit_code_presealed=True,producer_training_scoring_imports=0,model_head_decode_replays=0,source_groups_test=8));a.finish()





import ctypes as C
from ctypes import wintypes as W
import subprocess
MIB=1024**2
def require(ok,reason):
    if not ok:raise ValueError(reason)

class Basic(C.Structure):
    _fields_=[('process_time',C.c_int64),('job_time',C.c_int64),('flags',W.DWORD),
              ('min_ws',C.c_size_t),('max_ws',C.c_size_t),('active_limit',W.DWORD),
              ('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]

class IO(C.Structure):
    _fields_=[(n,C.c_uint64) for n in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]

class Extended(C.Structure):
    _fields_=[('basic',Basic),('io',IO),('process_memory',C.c_size_t),('job_memory',C.c_size_t),
              ('peak_process',C.c_size_t),('peak_job',C.c_size_t)]

class Accounting(C.Structure):
    _fields_=[('user',C.c_int64),('kernel',C.c_int64),('period_user',C.c_int64),('period_kernel',C.c_int64),
              ('faults',W.DWORD),('total',W.DWORD),('active',W.DWORD),('terminated',W.DWORD)]

class Startup(C.Structure):
    _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
              ('x',W.DWORD),('y',W.DWORD),('xsize',W.DWORD),('ysize',W.DWORD),('xchars',W.DWORD),
              ('ychars',W.DWORD),('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('reserved_size',W.WORD),
              ('reserved_ptr',C.POINTER(C.c_byte)),('stdin',W.HANDLE),('stdout',W.HANDLE),('stderr',W.HANDLE)]

class ProcessInfo(C.Structure):
    _fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]

def kernel():
    require(os.name=='nt','WINDOWS_ONLY')
    api=C.WinDLL('kernel32',use_last_error=True)
    signatures={
      'CreateJobObjectW':([W.LPVOID,W.LPCWSTR],W.HANDLE),
      'SetInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD],W.BOOL),
      'QueryInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD,W.LPVOID],W.BOOL),
      'AssignProcessToJobObject':([W.HANDLE,W.HANDLE],W.BOOL),
      'TerminateJobObject':([W.HANDLE,W.UINT],W.BOOL),
      'CloseHandle':([W.HANDLE],W.BOOL),
      'CreateProcessW':([W.LPCWSTR,W.LPWSTR,W.LPVOID,W.LPVOID,W.BOOL,W.DWORD,W.LPVOID,W.LPCWSTR,C.POINTER(Startup),C.POINTER(ProcessInfo)],W.BOOL),
      'ResumeThread':([W.HANDLE],W.DWORD),
      'GetExitCodeProcess':([W.HANDLE,C.POINTER(W.DWORD)],W.BOOL),
      'TerminateProcess':([W.HANDLE,W.UINT],W.BOOL),
      'OpenProcess':([W.DWORD,W.BOOL,W.DWORD],W.HANDLE),
      'IsProcessInJob':([W.HANDLE,W.HANDLE,C.POINTER(W.BOOL)],W.BOOL)}
    for name,(args,ret) in signatures.items():getattr(api,name).argtypes=args;getattr(api,name).restype=ret
    return api

class Job:
    def __init__(self,memory=512*MIB,active_limit=0):
        self.api=kernel();self.handle=self.api.CreateJobObjectW(None,None);require(self.handle,'JOB_CREATE')
        limits=Extended();limits.basic.flags=0x2000|0x100|0x200
        if active_limit:limits.basic.flags|=0x8;limits.basic.active_limit=active_limit
        limits.process_memory=limits.job_memory=memory
        require(self.api.SetInformationJobObject(self.handle,9,C.byref(limits),C.sizeof(limits)),'JOB_LIMITS')
        self.killed=False
    def assign(self,process):require(self.api.AssignProcessToJobObject(self.handle,process.handle),'JOB_ASSIGN')
    def snapshot(self):
        a=Accounting();e=Extended()
        require(self.api.QueryInformationJobObject(self.handle,1,C.byref(a),C.sizeof(a),None),'JOB_ACCOUNT')
        require(self.api.QueryInformationJobObject(self.handle,9,C.byref(e),C.sizeof(e),None),'JOB_MEMORY')
        return dict(active=a.active,total_processes=a.total,user_seconds=a.user/1e7,kernel_seconds=a.kernel/1e7,
                    peak_commit=e.peak_job,killed=self.killed)
    def active(self):return self.snapshot()['active']
    def empty(self,deadline):
        while self.active():
            if time.monotonic()>=deadline:return False
            time.sleep(.001)
        return True
    def kill(self):
        require(self.api.TerminateJobObject(self.handle,99),'OWN_JOB_TERMINATION');self.killed=True
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None

class Process:
    """CREATE_SUSPENDED -> assign Job -> ResumeThread, before Python user code."""
    def __init__(self,args,log,job=None):
        import msvcrt
        self.api=kernel();self.handle=None;self.pid=None
        si=Startup();si.cb=C.sizeof(si);si.flags=0x100
        pi=ProcessInfo();env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
        block=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
        command=C.create_unicode_buffer(subprocess.list2cmdline([str(x) for x in args]))
        with open(log,'xb') as output,open(os.devnull,'rb') as incoming:
            out=msvcrt.get_osfhandle(output.fileno());inp=msvcrt.get_osfhandle(incoming.fileno())
            os.set_handle_inheritable(out,True);os.set_handle_inheritable(inp,True)
            si.stdout=si.stderr=out;si.stdin=inp
            ok=self.api.CreateProcessW(None,command,None,None,True,0x08000000|0x4|0x400,block,None,C.byref(si),C.byref(pi))
            os.set_handle_inheritable(out,False);os.set_handle_inheritable(inp,False)
            require(ok,'CREATE_PROCESS_'+str(C.get_last_error()))
        self.handle,self.pid=pi.process,pi.pid
        try:
            if job is not None:job.assign(self)
            require(self.api.ResumeThread(pi.thread)!=0xffffffff,'RESUME_THREAD')
        except Exception:
            self.api.TerminateProcess(self.handle,98);raise
        finally:self.api.CloseHandle(pi.thread)
    @classmethod
    def registered(cls,pid,job):
        obj=cls.__new__(cls);obj.api=kernel();obj.pid=pid
        obj.handle=obj.api.OpenProcess(0x1000|0x100000,False,pid)
        require(obj.handle,'REGISTERED_PROCESS_OPEN')
        inside=W.BOOL();require(obj.api.IsProcessInJob(obj.handle,job.handle,C.byref(inside)) and inside.value,'REGISTERED_PROCESS_NOT_OWNED')
        return obj
    def poll(self):
        code=W.DWORD();require(self.api.GetExitCodeProcess(self.handle,C.byref(code)),'PROCESS_QUERY')
        return None if code.value==259 else code.value
    def wait(self,deadline):
        while self.poll() is None:
            if time.monotonic()>=deadline:raise TimeoutError('PROCESS_TIMEOUT')
            time.sleep(.001)
        return self.poll()
    def kill(self):require(self.api.TerminateProcess(self.handle,99),'OWN_PROCESS_TERMINATION')
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None




def communication(r):
 import importlib.util
 key='frozen_progress080'
 if key not in sys.modules:
  spec=importlib.util.spec_from_file_location(key,r/'communication.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);sys.modules[key]=m
 return sys.modules[key]














def ranges_module(r):
 import importlib.util
 name='frozen_ranges081'
 if name not in sys.modules:
  spec=importlib.util.spec_from_file_location(name,r/'ranges.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);sys.modules[name]=module
 return sys.modules[name]

class FixedHTTPAdapter:
 """Only fixed-object HTTP. Resolve local configuration before transport catches."""
 def __init__(self,r,*,connection_factory=None,proxy=None,context=None,nonlive=False):
  import http.client,ssl,urllib.request,urllib.parse
  self.r=r;self.m=ranges_module(r);self.context=ssl.create_default_context() if context is None else context;self.factory=connection_factory or http.client.HTTPSConnection;self.host='storage.googleapis.com';self.path='/dm-perception-test/zip_data/train_videos.zip?generation=1685446268139925';self.proxy=None;self.proxy_headers={};self.nonlive=nonlive
  if not nonlive:
   configured=urllib.request.getproxies().get('https') if proxy is None else proxy
   if configured:
    u=urllib.parse.urlsplit(configured);check(u.scheme=='http' and bool(u.hostname),'UNSUPPORTED_PROXY_CONFIGURATION');self.proxy=(u.hostname,u.port or 80)
    if u.username is not None:
     import base64
     self.proxy_headers['Proxy-Authorization']='Basic '+base64.b64encode((urllib.parse.unquote(u.username)+':'+urllib.parse.unquote(u.password or '')).encode()).decode()
 def __call__(self,request,on_connected):
  import ssl
  target=self.proxy or (self.host,443);timeout=min(10,max(.05,request['deadline']-time.monotonic()-2));conn=self.factory(target[0],target[1],timeout=timeout,context=self.context);response=None
  try:
   if self.proxy:conn.set_tunnel(self.host,443,headers=self.proxy_headers)
   try:conn.connect()
   except ssl.SSLCertVerificationError as exc:raise self.m.ResponseIdentityError('TLS_CERTIFICATE_IDENTITY_FAILURE') from exc
   on_connected();conn.sock.settimeout(min(20,max(.05,request['deadline']-time.monotonic()-2)));conn.request('GET',self.path,headers={'Range':f"bytes={request['start']}-{request['start']+request['length']-1}",'If-Match':self.m.ETAG,'Accept-Encoding':'identity'});response=conn.getresponse()
  except BaseException:
   conn.close();raise
  class BoundResponse:
   status=response.status
   def getheaders(self):return response.getheaders()
   def read(self,n):
    remaining=request['deadline']-time.monotonic()-2
    if remaining<=0:raise TimeoutError('SOFT_RESPONSE_DEADLINE_MARGIN')
    sock=conn.sock or getattr(getattr(getattr(response,'fp',None),'raw',None),'_sock',None)
    if sock is not None:sock.settimeout(min(20,remaining))
    return response.read(n)
   def close(self):
    try:response.close()
    finally:conn.close()
  return BoundResponse()

def transfer_totals(events):
 """New component schema, including recovered incomplete requests."""
 reserved=[e for e in events if e['event']=='REQUEST_RESERVED'];closed=[e for e in events if e['event']=='REQUEST_CLOSED'];incomplete=[e for e in events if e['event']=='REQUEST_INCOMPLETE'];check(len({e['request'] for e in reserved})==len(reserved),'REQUEST_IDS_UNIQUE');body=sum(e['kind']=='body' and e['retry'] for e in reserved);metadata=sum(e['kind']=='metadata' and e['retry'] for e in reserved);charge=134757960+sum(e['length'] for e in reserved)
 return dict(new_requests=len(reserved),cumulative_requests=21+len(reserved),new_range_charge=charge-134757960,cumulative_range_charge=charge,closed_requests=len(closed),incomplete_requests=len(incomplete),body_retries=body,metadata_retries=metadata)

def adapter_fixture(r,a):
 import http.client
 from unittest import mock
 m=ranges_module(r);folder=r/'NONLIVE-adapter-fixture';folder.mkdir();checks=0;recorded=[]
 def demand(v,why):
  nonlocal checks;checks+=1;check(v,'ADAPTER_FIXTURE_'+why)
 payload=b'abcdefghijklmno'
 for mode in ('EOF','TIMEOUT','INCOMPLETE_READ','METADATA_EOF','IDENTITY','LOCAL_FSYNC','LOCAL_LEDGER'):
  events=[];calls=[];states=[]
  class Socket:
   def settimeout(self,n):demand(0<n<=20,'SOFT_TIMEOUT_BOUND')
  class Connection:
   def __init__(self,*args,**kw):self.sock=Socket();self.n=len(calls);self.start=None;self.length=None;self.count=0;self.body=b''
   def connect(self):pass
   def request(self,method,path,headers):
    demand(method=='GET' and path.endswith('generation=1685446268139925') and headers['If-Match']==m.ETAG and headers['Accept-Encoding']=='identity','FIXED_REQUEST');start,end=map(int,headers['Range'][6:].split('-'));self.start=start;self.length=end-start+1;calls.append((start,self.length));self.body=payload[start-1000:start-1000+self.length]
   def getresponse(self):return self
   status=206
   def getheaders(self):return [('Content-Range',f'bytes {self.start}-{self.start+self.length-1}/{m.OBJECT_BYTES}'),('Content-Length',str(self.length)),('x-goog-generation','wrong' if mode=='IDENTITY' else m.GENERATION),('ETag',m.ETAG)]
   def read(self,n):
    self.count+=1
    if self.n==0 and mode in ('EOF','TIMEOUT','INCOMPLETE_READ','METADATA_EOF'):
     if mode=='INCOMPLETE_READ':raise http.client.IncompleteRead(self.body[:5],self.length-5)
     if self.count==1:return self.body[:5]
     if mode=='TIMEOUT':raise TimeoutError('NONLIVE_TIMEOUT')
     return b''
    b=self.body[:n];self.body=self.body[n:];return b
   def close(self):pass
  def commit(event_name,fields):
   if mode=='LOCAL_LEDGER':raise OSError('NONLIVE_LEDGER_FAILURE')
   events.append(dict(event=event_name,**fields,NONLIVE=True))
  budget=m.RangeBudget(commit,deadline=time.monotonic()+60);adapter=FixedHTTPAdapter(r,connection_factory=Connection,context='NONLIVE',nonlive=True);client=m.RangeClient(adapter,budget,lambda **kw:states.append(kw),sleep=lambda _:None);target=folder/(mode+'.part');error=None
  try:
   if mode=='LOCAL_FSYNC':
    with mock.patch('os.fsync',side_effect=OSError('NONLIVE_LOCAL_FSYNC')):client.member(1000,len(payload),target)
   elif mode=='METADATA_EOF':result=client.metadata(1000,len(payload))
   else:result=client.member(1000,len(payload),target)
  except (m.LocalStateError,m.ResponseIdentityError) as exc:error=type(exc).__name__
  if mode in ('EOF','TIMEOUT','INCOMPLETE_READ'):
   demand(target.read_bytes()==payload and calls==[(1000,15),(1005,10)],'SUFFIX_PRESERVES_PREFIX');totals=transfer_totals(events);demand(totals['new_requests']==2 and totals['cumulative_requests']==23 and totals['incomplete_requests']==1 and totals['closed_requests']==1 and totals['body_retries']==1,'NEW_SCHEMA_RECOVERED_INCOMPLETE');demand(result['compressed_sha256']==sha(payload),'COMPLETE_SHA');demand(all(e['NONLIVE'] for e in events),'NONLIVE_LEDGER')
  elif mode=='METADATA_EOF':
   totals=transfer_totals(events);demand(result==payload and calls==[(1000,15),(1000,15)] and totals['metadata_retries']==1 and totals['new_requests']==2,'METADATA_WHOLE_SMALL_RANGE_ONCE')
  else:demand(len(calls)==(0 if mode=='LOCAL_LEDGER' else 1) and error==('ResponseIdentityError' if mode=='IDENTITY' else 'LocalStateError'),'IDENTITY_LOCAL_NO_RETRY')
  if mode!='LOCAL_LEDGER':demand(any(s['phase']=='HEADERS' for s in states),'CONNECTED_CALLBACK');recorded.append(dict(case=mode,events=events,transport_calls=len(calls),NONLIVE=True))
 save(folder/'NONLIVE-events.json',recorded);save(r/'adapter-fixture.json',dict(status='PASS',checks=checks,cases=7,EOF_timeout_IncompleteRead_suffix='PASS',identity_local_write_no_retry='PASS',event_schema_and_prior_charge_mapping='PASS',real_HTTP_requests=0,model_media_operations=0,fixture_ledger='EXPLICIT_NONLIVE_SEPARATE_FROM_FORMAL_HTTP'));a.finish()
def reuse081(r,a):
 parent=a.meta(r/'parent.json');old=Path(parent['prior080']);records=[]
 def get(path):
  b=a.file(path,'old');records.append(dict(path=str(path),bytes=len(b),current_sha256=sha(b),provenance='CURRENT_REUSE_HASH_NOT_BACKDATED'));return b
 close=json.loads(get(old/'parent-closed.json'));check(close['current_jobs_all_active_zero'] and close['root_forward']==close['optimizer_updates']==0 and close['network_cumulative_requests']==21,'CLOSED080_NO_SCIENCE_STARTED');reuse=json.loads(get(old/'reuse080-manifest.json'));check(reuse['status']=='PASS','CLOSED_REUSE_CHAIN');seals=json.loads(get(old/'all-code-seals.json'));check(seals['files'][0]['lf_sha256']=='074498ef740ded1c869e845d686edbdf31e18957c201a48458a62dd0b58c555c','ORIGIN_PIPELINE_SEAL');copies={}
 for name in ('media-plan.json','observations.json','truth.json','relations.json','model-registration.json','processor-fixture.json'):
  b=get(old/name);ref=next(x for x in reuse['files'] if Path(x['path']).name==name and Path(x['path']).parent.name!='metadata');check(sha(b)==ref['current_sha256'],'DIRECT_REUSE_HASH');copies[name]=b
  with open(r/name,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 for name in ('summary.json','selected.json','answers.json','relations.json','independent.json','owner-comparison.json','source-registration.json'):
  b=get(old/'metadata'/name);ref=next(x for x in reuse['files'] if Path(x['path']).name==name and Path(x['path']).parent.name=='metadata');check(sha(b)==ref['current_sha256'],'METADATA_REUSE_HASH')
  with open(r/'metadata'/name,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 fixture=json.loads(get(old/'communication-fixture.json'));check(fixture['status']=='PASS' and fixture['checks']==218 and fixture['Windows_shared_handle'],'REUSED_WINDOWS_JOURNAL_PASS');reg=json.loads(copies['model-registration.json']);catalog=get(Path(parent['prior076'])/'model-registration.json');closed=json.loads(get(Path(parent['prior076'])/'prepared-seal.json'));check(sha(catalog)==closed['model_registration_sha256'] and json.loads(catalog)['graph']==reg['graph'],'CACHED_CATALOG_CHAIN')
 import importlib.util
 spec=importlib.util.spec_from_file_location('identity081',r/'identity.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);identity=module.validate_cached_model(reg,Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl',read_source=lambda path:a.file(path),progress=lambda **kw:progress(r,**kw));save(r/'identity-continuity081.json',identity)
 for name in ('network-summary.json','network-ledger.jsonl','network-job.json','independent080-bookkeeping.json','independent-final.json'):
  b=get(old/name);target=r/('origin080-'+name.replace('-job.json','-closure.json'))
  with open(target,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 net=json.loads((r/'origin080-network-summary.json').read_text(encoding='utf-8'));check(net['cumulative_request_upper']==21 and net['cumulative_conservative_range_charge']==134757960 and net['members_closed']==5,'PRIOR_NETWORK_ACCOUNTING');plan=json.loads(copies['media-plan.json']);reused=[]
 for group in range(5):
  body=get(old/f'member-{group}-closed.json');record=json.loads(body);entry=plan[group]['media'];check(record['group']==group and record['media_directory']==entry and record['bytes']==entry['uncompressed'] and record['source_generation']=='1685446268139925','OLD_MEMBER_SOURCE_BINDING');data=a.file(record['path'],'media');check(len(data)==entry['uncompressed'] and zlib.crc32(data)&0xffffffff==entry['crc'] and sha(data)==record['sha256'],'OLD_MEDIA_SIZE_CRC_SHA');new=dict(record,origin='REUSED080_COMPLETE_SEAL_WITH081_BYTE_CONTINUITY',origin_member_seal_current_sha256=sha(body),new_HTTP_requests=0,new_BZIP2_decompressions=0,pipeline_code_sha256=sha(Path(__file__).read_bytes().replace(b'\r\n',b'\n')));save(r/f'member-{group}-closed.json',new);reused.append(new)
 check(sum(x['bytes'] for x in reused)==78060287 and len(plan)==32,'FIVE_REUSED_TOTAL');chunks=[]
 for group in range(5,32):
  entry=plan[group]['media'];check(entry['method']==12 and entry['flags']==0,'MEMBER_METHOD_FLAGS')
  for ci,off in enumerate(range(0,entry['compressed'],4*1024**2)):chunks.append(dict(group=group,chunk=ci,member_relative_offset=off,length=min(4*1024**2,entry['compressed']-off)))
 check(len(chunks)==133 and sum(x['length'] for x in chunks)==503191554,'FIXED133_CHUNKS');save(r/'chunk-plan.json',dict(data=chunks,initial_data_requests=133,initial_metadata_requests=54,body_recovery_cap=16,metadata_recovery_cap=8,new_request_cap=211,cumulative_request_cap=232,initial_compressed_bytes=503191554));save(r/'reuse081-manifest.json',dict(status='PASS',files=records,groups=32,media_reused=5,reused_media_bytes=78060287,fixture_replays=0,historical_metadata_checks=22987,historical_binding_checks=3556,Windows_fixture218_reused=True,identity=identity,old_parent_seconds_078=reuse['old_parent_seconds_078'],old_parent_seconds_079=reuse['old_parent_seconds_079'],old_parent_seconds_080=close['parent080_seconds']));a.finish()

def network081(r,a):
 m=ranges_module(r);comm=communication(r);plan=a.meta(r/'media-plan.json');chunkplan=a.meta(r/'chunk-plan.json');started=a.meta(r/'network-started.json');global_deadline=started['start_monotonic']+started['effective_seconds']-1;writer=comm.ProgressWriter(r/'network-progress.jsonl','081-network-v1');writer.append(phase='BOOT',deadline=min(global_deadline,time.monotonic()+14.5),response_deadline=global_deadline,requests=21,range_charge=134757960,application_bytes=0);context=dict(group=None,member_object_start=None);closed_members=[a.meta(r/f'member-{i}-closed.json') for i in range(5)];new_unpacked=0
 def commit(name,fields):event(r/'range-ledger.jsonl',event=name,group=context['group'],member_object_start=context['member_object_start'],**fields)
 budget=m.RangeBudget(commit,deadline=global_deadline);adapter=FixedHTTPAdapter(r);client=m.RangeClient(adapter,budget,lambda **state:writer.append(**state));(r/'parts').mkdir();(r/'media').mkdir()
 try:
  for g in plan[5:]:
   group=g['group'];entry=g['media'];context.update(group=group,member_object_start=None);head=client.metadata(entry['offset'],30);v=struct.unpack('<4s5H3I2H',head);check(v[0]==b'PK\x03\x04' and v[2]==entry['flags']==0 and v[3]==12 and v[6]==entry['crc'],'LOCAL_HEADER');nl,el=v[-2:];fields=client.metadata(entry['offset']+30,nl+el);name=fields[:nl].decode('utf-8' if entry['flags']&2048 else 'cp437');check(name==entry['name'],'LOCAL_NAME');extra=fields[nl:];at=0;z64=None
   while at<len(extra):
    tag,n=struct.unpack_from('<HH',extra,at);at+=4;check(at+n<=len(extra),'LOCAL_EXTRA')
    if tag==1:z64=extra[at:at+n]
    at+=n
   values=[];cursor=0
   for x in (v[8],v[7]):
    if x==0xffffffff:check(z64 is not None and cursor+8<=len(z64),'LOCAL_ZIP64');x=struct.unpack_from('<Q',z64,cursor)[0];cursor+=8
    values.append(x)
   check(values==[entry['uncompressed'],entry['compressed']],'LOCAL_SIZES');object_start=entry['offset']+30+nl+el;context['member_object_start']=object_start;part=r/'parts'/f'{group}.compressed.part';compressed=client.member(object_start,entry['compressed'],part);check(part.stat().st_size==entry['compressed'],'COMPRESSED_PART_SIZE');target=r/'media'/f'{group}.mp4';decoder=bz2.BZ2Decompressor();chash=hashlib.sha256();rhash=hashlib.sha256();crc=0;produced=0;remaining=entry['compressed']
   with open(part,'rb') as source,open(target,'xb') as out:
    def emit(data):
     nonlocal crc,produced
     produced+=len(data);check(produced<=entry['uncompressed'] and new_unpacked+produced+78060287<=640*1024**2,'RAW_SIZE_CAP');crc=zlib.crc32(data,crc);rhash.update(data);out.write(data)
    while remaining:
     length=min(256*1024,remaining);ticket=a.reserve('media',length,'complete compressed part verification/decompression');block=source.read(length);a.settle(ticket,len(block));check(len(block)==length,'COMPRESSED_FILE_TRUNCATED');remaining-=len(block);chash.update(block);emit(decoder.decompress(block,max_length=min(1024**2,entry['uncompressed']-produced+1)))
     while not decoder.needs_input and not decoder.eof:emit(decoder.decompress(b'',max_length=min(1024**2,entry['uncompressed']-produced+1)))
     check(not decoder.eof or remaining==0,'TRAILING_COMPRESSED_BYTES')
    out.flush();os.fsync(out.fileno())
   check(decoder.eof and not decoder.unused_data and produced==entry['uncompressed'] and crc&0xffffffff==entry['crc'] and chash.hexdigest()==compressed['compressed_sha256'],'COMPRESSED_SHA_BZIP2_RAW_CRC_SIZE');new_unpacked+=produced;record=dict(group=group,path=str(target),bytes=produced,sha256=rhash.hexdigest(),crc=entry['crc'],media_directory=entry,source_generation=m.GENERATION,compressed_part=str(part),compressed_sha256=chash.hexdigest(),object_start=object_start,origin='NEW081_PERSISTENT_STREAM',pipeline_code_sha256=sha(Path(__file__).read_bytes().replace(b'\r\n',b'\n')));save(r/f'member-{group}-closed.json',record);closed_members.append(record);event(r/'media-ledger.jsonl',event='CLOSED',group=group,bytes=produced,sha256=record['sha256'],compressed_sha256=chash.hexdigest());print('MEDIA_MEMBER_SEALED',len(closed_members),'of32',flush=True)
  rebuilt=[]
  for g in plan:
   record=a.meta(r/f"member-{g['group']}-closed.json");check(record['group']==g['group'] and record['media_directory']==g['media'] and record['crc']==g['media']['crc'] and record['bytes']==g['media']['uncompressed'] and Path(record['path']).stat().st_size==record['bytes'],'GLOBAL_MEMBER_SEAL_BINDING');rebuilt.append(record)
  check(len(rebuilt)==32 and sum(x['bytes'] for x in rebuilt)==579702574,'FULL32_MEDIA');save(r/'media-manifest.json',rebuilt);save(r/'media-manifest-gate.json',dict(status='PASS',members=32,reused=5,new=27,member_seals_independently_rebuilt=True,manifest_sha256=sha(a.file(r/'media-manifest.json'))));writer.append(phase='DONE',deadline=global_deadline,response_deadline=global_deadline,**budget.snapshot())
 except BaseException as exc:
  event(r/'network-errors.jsonl',exception=type(exc).__name__,reason=str(exc),group=context['group'],**budget.snapshot())
  if not writer.failed:writer.append(phase='FAILED',deadline=global_deadline,response_deadline=global_deadline,error=type(exc).__name__,**budget.snapshot())
  raise
 finally:
  save(r/'network-summary.json',dict(status='CLOSED32' if len(closed_members)==32 else 'PARTIAL',**budget.snapshot(),new_requests=budget.requests-21,new_range_charge=budget.range_charge-134757960,prior_requests=21,prior_range_charge=134757960,request_cap=232,new_request_cap=211,range_charge_cap=805306368,new_charge_cap=670548408,members_closed=len(closed_members),new_members_closed=len(closed_members)-5,reused_members=5,new_uncompressed_bytes=new_unpacked,cumulative_uncompressed_closed_bytes=new_unpacked+78060287,journal_records=writer.sequence,last_journal_hash=writer.previous,writer_failed=writer.failed));writer.close();a.finish()


def parent_elapsed(r,clock):
 elapsed=time.time()-clock['epoch_ms']/1000
 p=r/'infra-repair-v2.json'
 if p.exists():
  repair=json.loads(p.read_text(encoding='utf-8-sig'))
  check(repair['repair_number']==1 and repair['previous_job_active']==0 and repair['excluded_seconds']>0,'INVALID_IDLE_EXCLUSION')
  elapsed-=repair['excluded_seconds']
 return elapsed

def supervise(r,phase,args):
 """Actual079 Windows Job supervisor, public and inspectable with the worker."""
 start=time.monotonic();clock=json.loads((r/'parent-clock.json').read_text(encoding='utf-8-sig'));par=json.loads((r/'parent.json').read_text(encoding='utf-8-sig'));oldroots=[Path(par['prior078']),Path(par['prior079']),Path(par['prior080'])];oldfiles=[]
 for oldroot in oldroots:
  for path in oldroot.rglob('*'):
   if path.is_file():oldfiles.append(path);check(len(oldfiles)<=4096,'OLD_ROOT_COUNT_BOUND')
 oldbytes=sum(p.stat().st_size for p in oldfiles);check(oldbytes<8*1024**3,'OLD_ROOT_BYTES');groups=[({'adapter_fixture','reuse081','input_gate','feature_pack'},536.51),({'decode_prepare'},1800),({'network'},1544.45),({'gpu'},3600),({'train'},1796.25),({'predict','scoring','independent'},599.16)];group,cap=next((g,c) for g,c in groups if phase in g);prior=sum(json.loads(p.read_text(encoding='utf-8-sig'))['outer_seconds'] for p in r.glob('*-job.json') if p.name[:-9] in group);control=Reads(r,'control-'+phase+('-v2' if (r/('control-'+phase+'-io.json')).exists() else ''));closed78=control.meta(oldroots[0]/'parent-closed.json','old');closed79=control.meta(oldroots[1]/'parent-closed.json','old');closed80=control.meta(oldroots[2]/'parent-closed.json','old');control.finish();oldwall=closed78['parent_seconds']+closed79['new_parent_seconds']+closed80['parent080_seconds'];limit=min(cap-prior,12000-parent_elapsed(r,clock),14400-oldwall-parent_elapsed(r,clock));check(limit>1 and not(r/(phase+'-started.json')).exists(),'NO_BUDGET_OR_PRIOR_STARTED');os.environ['VLM_ROLE']=phase
 for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='4'
 for key in ('HF_HUB_OFFLINE','TRANSFORMERS_OFFLINE','HF_DATASETS_OFFLINE'):os.environ[key]='1'
 os.environ['TOKENIZERS_PARALLELISM']='false';lock=None
 if phase=='gpu':
  import importlib.util
  spec=importlib.util.spec_from_file_location('existing_jobs',par['gpu_jobs_module']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  try:lock=module.GPULock(par['gpu_lock_path']);lock.__enter__()
  except RuntimeError:save(r/'gpu-busy.json',dict(status='GPU_BUSY',stage='NONBLOCKING_LOCK'));return 2
  result=subprocess.run(['nvidia-smi','--query-gpu=memory.free','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10);free=int(result.stdout.strip().splitlines()[0]) if result.returncode==0 else None;save(r/'gpu-resource.json',dict(command_calls=1,free_mib=free,required_mib=18432,returncode=result.returncode))
  if free is None or free<18432:lock.__exit__();save(r/'gpu-busy.json',dict(status='GPU_BUSY',stage='FREE_MEMORY',actual_mib=free,required_mib=18432));return 2
  start=time.monotonic();save(r/'gpu-clock.json',dict(start_monotonic=start,outer_limit_seconds=3600))
 else:os.environ['CUDA_VISIBLE_DEVICES']=''
 save(r/(phase+'-started.json'),dict(epoch=time.time(),start_monotonic=start,effective_seconds=limit,group_prior=prior,group_cap=cap,scientific_workers=1));memory=32 if phase=='gpu' else 16;job=Job(memory=memory*1024**3,active_limit=8);e=Extended();require(job.api.QueryInformationJobObject(job.handle,9,C.byref(e),C.sizeof(e),None),'LIMIT_READBACK');readback=dict(flags=e.basic.flags,active_limit=e.basic.active_limit,job_memory=e.job_memory,process_memory=e.process_memory,kill_on_close=bool(e.basic.flags&0x2000));save(r/(phase+'-limit-readback.json'),readback);check(e.basic.active_limit==8 and e.job_memory==memory*1024**3 and readback['kill_on_close'],'LIMIT_READBACK_MISMATCH');process=Process(args,r/(phase+'.log'),job);peak_threads=0;peak_active=0;peak_population=0;stop_reason=None;seenpids=set();lastactive=None;network_reader=communication(r).ProgressReader(r/'network-progress.jsonl','081-network-v1') if phase=='network' else None;network_latest=None;network_seq=0
 class Thread(C.Structure):
  _fields_=[('size',W.DWORD),('use',W.DWORD),('tid',W.DWORD),('pid',W.DWORD),('base',W.LONG),('delta',W.LONG),('flags',W.DWORD)]
 api=job.api;api.CreateToolhelp32Snapshot.argtypes=[W.DWORD,W.DWORD];api.CreateToolhelp32Snapshot.restype=W.HANDLE;api.Thread32First.argtypes=[W.HANDLE,C.POINTER(Thread)];api.Thread32First.restype=W.BOOL;api.Thread32Next.argtypes=[W.HANDLE,C.POINTER(Thread)];api.Thread32Next.restype=W.BOOL;api.QueryFullProcessImageNameW.argtypes=[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)];api.QueryFullProcessImageNameW.restype=W.BOOL;api.GetProcessTimes.argtypes=[W.HANDLE,C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME)];api.GetProcessTimes.restype=W.BOOL
 def evidence(pid):
  record=dict(pid=pid,phase=phase,role='scientific_worker_or_runtime_auxiliary_UNKNOWN',executable_basename='UNKNOWN',ppid='UNKNOWN',created_epoch='UNKNOWN');h=api.OpenProcess(0x1000,False,pid)
  if h:
   try:
    size=W.DWORD(32768);name=C.create_unicode_buffer(size.value)
    if api.QueryFullProcessImageNameW(h,0,name,C.byref(size)):record['executable_path']=name.value;record['executable_basename']=Path(name.value).name
    created,exited,kern,user=W.FILETIME(),W.FILETIME(),W.FILETIME(),W.FILETIME()
    if api.GetProcessTimes(h,C.byref(created),C.byref(exited),C.byref(kern),C.byref(user)):record['created_epoch']=((created.dwHighDateTime<<32)|created.dwLowDateTime)/1e7-11644473600
    nt=C.WinDLL('ntdll');nt.NtQueryInformationProcess.argtypes=[W.HANDLE,C.c_ulong,W.LPVOID,C.c_ulong,C.POINTER(C.c_ulong)];nt.NtQueryInformationProcess.restype=C.c_long;pbi=(C.c_void_p*6)();ret=C.c_ulong()
    if nt.NtQueryInformationProcess(h,0,C.byref(pbi),C.sizeof(pbi),C.byref(ret))==0:record['ppid']=int(pbi[5] or 0)
   finally:api.CloseHandle(h)
  event(r/'owned-processes.jsonl',**record)
 try:
  while process.poll() is None:
   account=job.snapshot();active=account['active'];peak_active=max(peak_active,active);buf=C.create_string_buffer(8+8*16);require(api.QueryInformationJobObject(job.handle,3,buf,len(buf),None),'JOB_PID_LIST');population=int.from_bytes(buf.raw[4:8],'little');check(population<=16,'PID_BUFFER');pids=[int.from_bytes(buf.raw[8+8*i:16+8*i],'little') for i in range(population)];peak_population=max(peak_population,population)
   for pid in pids:
    if pid not in seenpids:evidence(pid);seenpids.add(pid)
   if active!=lastactive:event(r/'process-accounting.jsonl',phase=phase,accounting_active=active,pid_list_population=population,pids=pids);lastactive=active
   snap=api.CreateToolhelp32Snapshot(4,0);entry=Thread();entry.size=C.sizeof(entry);counts={p:0 for p in pids}
   try:
    ok=api.Thread32First(snap,C.byref(entry))
    while ok:
     if entry.pid in counts:counts[entry.pid]+=1
     ok=api.Thread32Next(snap,C.byref(entry))
   finally:api.CloseHandle(snap)
   peak_threads=max(peak_threads,max(counts.values(),default=0));files=[p for p in r.rglob('*') if p.is_file()]
   if time.monotonic()-start>=limit-1:stop_reason='PHASE_CUMULATIVE_DEADLINE'
   elif parent_elapsed(r,clock)>=11999:stop_reason='PARENT_DEADLINE'
   elif peak_active>8:stop_reason='ACTIVE_PROCESS_GT8'
   elif peak_threads>256:stop_reason='NATIVE_THREADS_GT256'
   elif len(files)+len(oldfiles)>4096 or sum(p.stat().st_size for p in files)+oldbytes>8*1024**3:stop_reason='COMBINED_ROOT_QUOTA'
   elif sum(p.stat().st_size for p in (r/'train').glob('*.pt') if p.name!='training.pt')>64*MIB:stop_reason='CHECKPOINT_QUOTA'
   if phase=='network':
    try:
     network_latest=network_reader.poll();network_seq=network_reader.sequence;deadline=communication(r).effective_deadline(network_latest,global_deadline=start+limit-1,bootstrap_deadline=start+14.5)
     if time.monotonic()>deadline:stop_reason='NETWORK_JOURNAL_EFFECTIVE_DEADLINE'
    except (ValueError,OSError) as exc:
     event(r/'supervisor-journal-errors.jsonl',phase=phase,exception=type(exc).__name__,reason=str(exc),last_complete_sequence=network_seq);stop_reason='NETWORK_JOURNAL_INTEGRITY_OR_READ'
   if stop_reason:save(r/(phase+'-supervisor-stop.json'),dict(reason=stop_reason,elapsed=time.monotonic()-start,accounting_active=active,pid_list_population=population,pids=pids));job.kill();break
   time.sleep(.02)
  code=process.wait(time.monotonic()+5)
  if not job.empty(time.monotonic()+5):job.kill();job.empty(time.monotonic()+5)
  result=job.snapshot();result.update(network_last_complete_records=network_seq if phase=='network' else None,network_last_complete_phase=network_latest['phase'] if network_latest else None,exit_code=code,outer_seconds=time.monotonic()-start,limit_seconds=limit,group_cap=cap,group_prior=prior,peak_observed_threads_per_job_process=peak_threads,native_thread_limit=256,peak_observed_active=peak_active,peak_pid_list_population=peak_population,owned_pids_observed=len(seenpids),memory_limit_bytes=memory*1024**3,stop_reason=stop_reason,limit_readback=readback,old_root_files=len(oldfiles),old_root_bytes=oldbytes,old_parent_seconds=oldwall,thread_scope='20ms own-Job snapshots; native auxiliaries distinct from compute4/interop1/codec1; no continuous OS hard thread quota');save(r/(phase+'-job.json'),result);print(json.dumps(result));return 0 if code==0 else 1
 finally:
  process.close();job.close()
  if network_reader is not None:network_reader.close()
  if lock is not None:lock.__exit__()
def independent(r,a):
 checks=0
 def demand(v,why):
  nonlocal checks;checks+=1;check(v,'STREAM_ORACLE_'+why)
 plan=a.meta(r/'media-plan.json') if (r/'media-plan.json').exists() else None
 if (r/'range-ledger.jsonl').exists():
  m=ranges_module(r);events=[json.loads(x) for x in a.file(r/'range-ledger.jsonl').splitlines()];totals=transfer_totals(events);summary=a.meta(r/'network-summary.json');demand(totals['new_requests']==summary['new_requests'] and totals['cumulative_requests']==summary['requests'] and totals['cumulative_range_charge']==summary['range_charge'],'SCHEMA_CUMULATIVE_TOTALS');demand(totals['new_requests']<=211 and totals['cumulative_requests']<=232 and totals['cumulative_range_charge']<=805306368 and totals['body_retries']<=16 and totals['metadata_retries']<=8,'REQUEST_BYTE_RECOVERY_CAPS');res={};settled={};prefix=collections.defaultdict(int);pending={};segments=collections.defaultdict(list);attempts=collections.defaultdict(list);metadata_attempts=collections.defaultdict(list);origin={};charge=134757960
  for event_ in events:
   ev=event_['event'];group=event_['group']
   if ev=='REQUEST_RESERVED':
    req=event_['request'];demand(req==22+len(res) and req not in res,'GLOBAL_IDS_NO_RESET');charge+=event_['length'];demand(charge==event_['range_charge'],'READ_AHEAD_RANGE_CHARGE');res[req]=event_
    if event_['kind']=='body':
     start=event_['member_object_start'];origin[group]=start;size=plan[group]['media']['compressed'];ci=prefix[group]//(4*1024**2);end=min(size,(ci+1)*4*1024**2);key=(group,ci);prior=attempts[key];demand(len(prior)<2 and event_['retry']==bool(prior),'ONE_SUFFIX_RECOVERY_ONLY');demand(event_['start']==start+prefix[group] and event_['length']==end-prefix[group]<=4*1024**2,'EXACT_MISSING_SUFFIX')
     if prior:demand(prior[-1] in settled and settled[prior[-1]]['event']=='REQUEST_INCOMPLETE','RECOVERY_FOLLOWS_INCOMPLETE')
     prior.append(req)
    else:
     key=(group,event_['start'],event_['length']);prior=metadata_attempts[key];demand(len(prior)<2 and event_['retry']==bool(prior) and event_['length']<=131070,'SMALL_METADATA_ONCE_RETRY');prior.append(req)
   elif ev=='PAYLOAD_WRITE_RESERVED':
    demand(group not in pending and event_['prefix']==prefix[group] and 0<event_['length']<=256*1024,'WRITE_RESERVE_CONTIGUOUS');pending[group]=event_
   elif ev=='PAYLOAD_COMMITTED':
    intent=pending.pop(group);demand(event_['prefix']==prefix[group]+intent['length'],'PREFIX_NO_GAP_OVERLAP');segments[group].append(dict(start=prefix[group],length=intent['length'],data_sha256=intent['data_sha256'],prefix_sha256=event_['prefix_sha256']));prefix[group]=event_['prefix']
   elif ev in ('REQUEST_CLOSED','REQUEST_INCOMPLETE'):
    req=event_['request'];demand(req in res and req not in settled and 0<=event_['received']<=event_['requested']==res[req]['length'],'HTTP_SETTLEMENT');demand(ev!='REQUEST_CLOSED' or event_['received']==event_['requested'],'CLOSED_EXACT_LENGTH');settled[req]=event_
  demand(len(res)==totals['new_requests'] and summary['application_bytes']>=sum(x['length'] for ss in segments.values() for x in ss),'BYTE_TOTALS')
  # Prefix hash and each write-intent hash are checked against disk, without
  # decompressing, decoding video, or replaying any model/head.
  for group,ss in segments.items():
   path=r/'parts'/f'{group}.compressed.part';demand(path.stat().st_size>=prefix[group],'DURABLE_PREFIX_EXISTS');digest=hashlib.sha256()
   with open(path,'rb') as file:
    for item in ss:
     ticket=a.reserve('media',item['length'],'independent committed compressed-prefix interval');body=file.read(item['length']);a.settle(ticket,len(body));demand(len(body)==item['length'] and sha(body)==item['data_sha256'],'WRITE_BYTES_MATCH_DISK');digest.update(body);demand(digest.hexdigest()==item['prefix_sha256'],'PREFIX_SHA_MATCH_DISK')
   if (r/f'member-{group}-closed.json').exists():
    seal=a.meta(r/f'member-{group}-closed.json');demand(prefix[group]==plan[group]['media']['compressed']==path.stat().st_size and digest.hexdigest()==seal['compressed_sha256'],'COMPLETE_COMPRESSED_IDENTITY')
  cm=communication(r)
  with cm.ProgressReader(r/'network-progress.jsonl','081-network-v1') as reader:
   while True:
    before=reader.bytes_read;reader.poll()
    if before==reader.bytes_read:break
   demand(not reader.pending and reader.sequence==summary['journal_records'] and reader.previous==summary['last_journal_hash'],'JOURNAL_CHAIN_FINAL')
   if (r/'media-manifest.json').exists():
    demand(reader.latest['phase']=='DONE' and len(pending)==0 and len(settled)==len(res),'COMPLETE_RECOVERED_TRANSFER');demand(sum(not x['retry'] and x['kind']=='body' for x in res.values())==133 and sum(not x['retry'] and x['kind']=='metadata' for x in res.values())==54,'FROZEN_INITIAL_REQUEST_PLAN')
 if (r/'media-manifest.json').exists():
  manifest=a.meta(r/'media-manifest.json');demand(len(manifest)==32,'FULL32')
  for group,rec in enumerate(manifest):
   seal=a.meta(r/f'member-{group}-closed.json');demand(rec==seal and rec['group']==group and rec['media_directory']==plan[group]['media'] and rec['bytes']==plan[group]['media']['uncompressed'] and rec['crc']==plan[group]['media']['crc'] and rec['source_generation']=='1685446268139925','MEMBER_RAW_SEAL_PLAN_BINDING')
  demand(sum(x['bytes'] for x in manifest)==579702574 and sum(x['group']>=5 for x in manifest)==27,'REUSED5_NEW27')
 save(r/'independent081-transfer.json',dict(status='PASS',checks=checks,code_presealed=True,compressed_prefix_disk_hash_review=True,model_head_video_decode_replays=0));independent_science(r,a)

def main():
 if len(sys.argv)>1 and sys.argv[1]=='supervise':sys.exit(supervise(Path(sys.argv[2]),sys.argv[3],sys.argv[4:]))
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--role',required=True,choices=('adapter_fixture','reuse081','network','decode_prepare','input_gate','gpu','feature_pack','train','predict','scoring','independent'));args=p.parse_args();r=Path(args.root);seals(r);a=Reads(r,args.role);progress(r,'ROLE_BEGIN')
 try:
  if args.role=='network':network081(r,a)
  else:globals()[args.role](r,a)
  progress(r,'ROLE_CLOSED')
 except Exception as e:
  event(r/'failures.jsonl',role=args.role,exception=type(e).__name__,reason=str(e),status='FAILED_WITH_PRESERVED_PREFIX_AND_BUDGET')
  if not(r/(args.role+'-io.json')).exists():a.finish()
  raise
if __name__=='__main__':main()
