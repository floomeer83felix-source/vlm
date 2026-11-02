"""078 bounded real-RGB triples, frozen complete Qwen, matched A/I/S experiment.

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
CAPS={'prepared':12*1024**3,'old':32*1024**2,'media':4*1024**3,'model':12*1024**3}

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
 def __init__(self,r,role):self.r=r;self.role=role;self.cache={};self.counts=collections.Counter();self.previous=collections.Counter()
 def charge(self,kind,n):
  self.counts[kind]+=n;check(self.previous[kind]+self.counts[kind]<=CAPS[kind],'READ_CAP_'+kind)
 def file(self,p,kind='prepared'):
  p=str(p)
  if self.role=='train':check(Path(p).parent==self.r/'train' or Path(p).name in ('all-code-seals.json','parent.json'),'TRAIN_READ_ISOLATION')
  if p not in self.cache:self.cache[p]=Path(p).read_bytes();self.charge(kind,len(self.cache[p]))
  return self.cache[p]
 def meta(self,p,kind='prepared'):return json.loads(self.file(p,kind).decode('utf-8-sig'))
 def tensor(self,rec):
  import torch
  b=self.file(rec['path']);check(sha(b)==rec['sha256'],'TENSOR_FILE_HASH');return torch.load(io.BytesIO(b),map_location='cpu',weights_only=True)
 def finish(self):save(self.r/(self.role+'-io.json'),dict(counts=self.counts,scope='explicit logical buffered reads; not native/OS physical IO'))

def seals(r):
 records=json.loads((r/'all-code-seals.json').read_text(encoding='utf-8'))['files']
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

def registration(r,a):
 old=a.meta(Path(a.meta(r/'parent.json')['prior076'])/'model-registration.json','old');base=Path(old['model_root']);n=0
 for name,expected in old['graph']['model_files'].items():
  h=hashlib.sha256()
  with open(base/name,'rb') as f:
   for b in iter(lambda:f.read(1024**2),b''):h.update(b);n+=len(b);a.charge('model',len(b))
  check(h.hexdigest()==expected,'MODEL_IDENTITY')
 installed={}
 for name,expected in old['graph']['installed_sources'].items():
  path=Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/name;b=path.read_bytes();a.charge('prepared',len(b));check(sha(b)==expected,'INSTALLED_IDENTITY');installed[name]=expected
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 import torch as t,numpy as np
 t.set_num_threads(4);t.set_num_interop_threads(1)
 proc=AutoProcessor.from_pretrained(base,local_files_only=True,trust_remote_code=False)
 check(proc.tokenizer('Yes',add_special_tokens=False)['input_ids']==[old['graph']['yes_id']] and proc.tokenizer('No',add_special_tokens=False)['input_ids']==[old['graph']['no_id']],'YES_NO_IDENTITY')
 sample=np.zeros((36,224,224,3),dtype=np.uint8);md=VideoMetadata(total_num_frames=36,fps=12,duration=3,width=224,height=224,frames_indices=list(range(36)));q='Is this a software fixture? Answer Yes or No.'
 native=proc(text=[prompt(proc,q,True)],videos=[sample],video_metadata=[md],do_sample_frames=False,do_resize=False,return_tensors='pt');check(native['video_grid_thw'].tolist()==[[18,14,14]] and tuple(native['pixel_values_videos'].shape)==(3528,1536),'NATIVE36_GRID')
 video={k:v for k,v in native.items() if k not in ('input_ids','attention_mask','token_type_ids','pixel_values_videos')};d=components(proc,q,video,md);check(set(d)==set(native)-{'pixel_values_videos'} and all(t.equal(d[k],native[k]) for k in d),'NATIVE_SPLIT_TOKEN_FIXTURE')
 check(n==8887284080 and not t.cuda.is_initialized(),'MODEL_SIZE_AND_CPU');save(r/'model-registration.json',old);save(r/'processor-fixture.json',dict(status='PASS',grid=[18,14,14],pixels=[3528,1536],visual_tokens=882,synthetic_calls=1,model_loads=0,model_hash_bytes=n,hook_binding='Qwen3VLVisionModel output tuple[0] after main merger; temporal-major then spatial merge blocks; text output.last_hidden_state last valid token',runtime_sources=installed));a.finish()

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
 z=zipfile.ZipFile(io.BytesIO(a.file(meta/'action_localisation_train_annotations.zip')));b=z.read('action_localisation_train.json');a.charge('prepared',len(b));source=json.loads(b);records=[]
 for g in selected:
  m=g['media'];check(m['method']==12 and m['flags']==0 and m['compressed']<=80*1024**2 and m['uncompressed']<=80*1024**2,'MEMBER_FLAGS_SIZE');md=source[g['observation']['video_id']]['metadata'];records.append(dict(group=g['rank'],split=g['split'],media=m,fps=md['frame_rate'],num_frames=md['num_frames'],events=g['observation']['events'],sampling=g['sampling'],questions=g['questions']))
 save(r/'media-plan.json',records);save(r/'observations.json',[dict(group=g['rank'],split=g['split'],questions=g['questions']) for g in selected]);save(r/'truth.json',answers);save(r/'relations.json',relations);save(r/'manifest-seal.json',dict(groups=32,source_frames=sum(x['num_frames'] for x in records),compressed=sum(x['media']['compressed'] for x in records),uncompressed=sum(x['media']['uncompressed'] for x in records),media_plan_sha256=sha(a.file(r/'media-plan.json'))));a.finish()

def network(r,a):
 import http.client,ssl,urllib.request,urllib.parse,socket
 records=a.meta(r/'media-plan.json');host='storage.googleapis.com';path='/dm-perception-test/zip_data/train_videos.zip?generation=1685446268139925';etag='"-CJXz5tD4nP8CEAE="';total=28404087974;readbytes=0;requests=0;unpacked=0
 def state(**kw):
  body=packed(dict(epoch=time.time(),monotonic=time.monotonic(),**kw));tmp=r/'network-state.tmp';tmp.write_bytes(body);os.replace(tmp,r/'network-state.json')
 def get(start,length,kind):
  nonlocal readbytes,requests
  check(length>0 and requests<96 and length<=80*1024**2,'RANGE_LIMIT');requests+=1;begin=time.monotonic();outer=239.5 if kind=='body' else 29.5;state(phase='CONNECT',deadline=begin+14.5,response_deadline=begin+outer,request=requests,read_bytes=readbytes);event(r/'network-ledger.jsonl',event='STARTED',request=requests,start=start,length=length,kind=kind)
  proxy=urllib.request.getproxies().get('https');conn=None;response=None
  try:
   if proxy:
    u=urllib.parse.urlsplit(proxy);check(u.scheme=='http','UNSUPPORTED_PROXY_TRANSPORT');conn=http.client.HTTPSConnection(u.hostname,u.port or 80,timeout=60,context=ssl.create_default_context());headers={}
    if u.username is not None:
     import base64
     headers['Proxy-Authorization']='Basic '+base64.b64encode((urllib.parse.unquote(u.username)+':'+urllib.parse.unquote(u.password or '')).encode()).decode()
    conn.set_tunnel(host,443,headers=headers)
   else:conn=http.client.HTTPSConnection(host,443,timeout=60,context=ssl.create_default_context())
   conn.connect();state(phase='HEADERS',deadline=begin+outer,response_deadline=begin+outer,request=requests,read_bytes=readbytes);conn.request('GET',path,headers={'Range':f'bytes={start}-{start+length-1}','If-Match':etag,'Accept-Encoding':'identity','Connection':'close'});response=conn.getresponse();h={k.lower():v for k,v in response.getheaders()}
   check(response.status==206,'HTTP_NOT_206');check(h.get('content-range')==f'bytes {start}-{start+length-1}/{total}' and int(h.get('content-length','-1'))==length,'RANGE_RESPONSE_IDENTITY');check(h.get('x-goog-generation')=='1685446268139925' and h.get('etag')==etag and h.get('content-encoding','identity')=='identity','REMOTE_VERSION_OR_ENCODING');chunks=[];got=0
   while got<length:
    state(phase='BODY',deadline=min(begin+outer,time.monotonic()+60),response_deadline=begin+outer,request=requests,read_bytes=readbytes);b=response.read(min(1024**2,length-got));check(bool(b),'TRUNCATED_RANGE');got+=len(b);readbytes+=len(b);check(readbytes<=768*1024**2,'NETWORK_BYTES');chunks.append(b)
   check(time.monotonic()-begin<outer,'RESPONSE_OUTER');event(r/'network-ledger.jsonl',event='CLOSED',request=requests,bytes=got,status=206,seconds=time.monotonic()-begin);return b''.join(chunks)
  except Exception as e:event(r/'network-ledger.jsonl',event='FAILED',request=requests,kind=kind,read_bytes=readbytes,reason=type(e).__name__+':'+str(e));raise
  finally:
   if response is not None:response.close()
   if conn is not None:conn.close()
   state(phase='IDLE',deadline=time.monotonic()+1800,response_deadline=time.monotonic()+1800,request=requests,read_bytes=readbytes)
 out=[];(r/'media').mkdir()
 try:
  for g in records:
   m=g['media'];h=get(m['offset'],30,'header');v=struct.unpack('<4s5H3I2H',h);check(v[0]==b'PK\x03\x04' and v[2]==m['flags']==0 and v[3]==12 and v[6]==m['crc'],'LOCAL_HEADER');nl,el=v[-2:];body=get(m['offset']+30,nl+el,'fields');name=body[:nl].decode('utf-8' if m['flags']&2048 else 'cp437');check(name==m['name'],'LOCAL_NAME');extra=body[nl:];u,c=v[8],v[7];at=0;z64=None
   while at<len(extra):
    tag,n=struct.unpack_from('<HH',extra,at);at+=4;check(at+n<=len(extra),'LOCAL_EXTRA_BOUNDS')
    if tag==1:z64=extra[at:at+n]
    at+=n
   cursor=0;values=[]
   for x in (u,c):
    if x==0xffffffff:check(z64 is not None and cursor+8<=len(z64),'LOCAL_ZIP64');x=struct.unpack_from('<Q',z64,cursor)[0];cursor+=8
    values.append(x)
   check(values==[m['uncompressed'],m['compressed']],'LOCAL_SIZE');compressed=get(m['offset']+30+nl+el,m['compressed'],'body');decoder=bz2.BZ2Decompressor();data=decoder.decompress(compressed,max_length=m['uncompressed']+1);check(decoder.eof and not decoder.unused_data and len(data)==m['uncompressed'],'BZIP2_SIZE_EOF');check((zlib.crc32(data)&0xffffffff)==m['crc'],'MEDIA_CRC');unpacked+=len(data);check(unpacked<=640*1024**2,'UNPACKED_TOTAL');target=r/'media'/f"{g['group']}.mp4"
   with open(target,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
   out.append(dict(group=g['group'],path=str(target),sha256=sha(data),bytes=len(data),compressed_sha256=sha(compressed),crc=m['crc']));event(r/'media-ledger.jsonl',event='CLOSED',group=g['group'],bytes=len(data));del data,compressed
  save(r/'media-manifest.json',out)
 finally:save(r/'network-summary.json',dict(requests_started=requests,response_body_bytes=readbytes,uncompressed_closed_bytes=unpacked,members_closed=len(out),network_limit_bytes=768*1024**2,requests_limit=96));a.finish()
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
   b=self.f.read(n);a.charge('media',len(b));self.read_bytes+=len(b);return b
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

def independent(r,a):
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

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--role',required=True,choices=('fixture','registration','manifest','network','decode_prepare','input_gate','gpu','feature_pack','train','predict','scoring','independent'));args=p.parse_args();r=Path(args.root);seals(r);a=Reads(r,args.role)
 for path in r.glob('*-io.json'):
  if path.name!=args.role+'-io.json':a.previous.update(json.loads(path.read_text())['counts'])
 try:globals()[args.role](r,a)
 except Exception as e:
  event(r/'failures.jsonl',role=args.role,exception=type(e).__name__,reason=str(e),status='FAILED_NO_RETRY')
  if not(r/(args.role+'-io.json')).exists():a.finish()
  raise
if __name__=='__main__':main()
