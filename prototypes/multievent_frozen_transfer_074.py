"""074 explicit offline native evaluation; import performs no research I/O.

No downloader, optimizer, generation or fit entry. Registration sees publisher
metadata; GPU and head workers receive only prepared inputs and frozen assets.
"""
import argparse, collections, hashlib, importlib.util, io, itertools, json, os
from pathlib import Path
import random, re, shutil, stat, time, zipfile, zlib

SEEDS=(137,263,419,557,733,911)
METHODS=('C_NATIVE','D_NATIVE','CONCAT','FACTOR','REVERSE','ANCHOR')
COMPARISONS=(('D_NATIVE','C_NATIVE'),('FACTOR','D_NATIVE'),('FACTOR','CONCAT'),('FACTOR','REVERSE'),('FACTOR','ANCHOR'))
REV='da3065053d958c38151304e33a42e138b1899eaf'
TEMPLATE='Does the event "{}" happen before the event "{}"? Answer Yes or No.'
PATTERN=r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.'
MIB=1024**2
CAPS={'api.json':2*MIB,'README.md':32*1024,'answer_final.json':2*MIB}

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:f.write(canonical(x)+'\n');f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(canonical(dict(epoch=time.time(),**x))+'\n');f.flush();os.fsync(f.fileno())
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(MIB),b''):h.update(b)
 return h.hexdigest()
def require(root,ok,reason,actual=None,limit=None):
 if not ok:
  if Path(root).exists():event(Path(root)/'failures.jsonl',reason=reason,actual=actual,limit=limit)
  raise RuntimeError(reason)
def tau(q):
 m=re.fullmatch(PATTERN,q)
 if not m:raise ValueError('QUESTION_PARSE')
 return TEMPLATE.format(m[2],m[1])
def helper(name):
 p=Path(__file__).with_name(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sealed(root):
 for x in read(Path(root)/'code-seal.json')['files']:assert sha(Path(x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256'],'CODE_CHANGED'
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def snapshot(root):
 ps=[p for p in Path(root).rglob('*') if p.is_file()];n=sum(p.stat().st_size for p in ps)
 require(root,len(ps)<=2048 and n<=3*1024**3,'ROOT_LIMIT',{'files':len(ps),'bytes':n},{'files':2048,'bytes':3*1024**3})
 return dict(files=len(ps),bytes=n)

def choose(api,bundle):
 """Known source schema, root invalid flags before any other ordering filter."""
 old=helper('multievent_offline_073')
 path,rows=old.collection(bundle);counts=collections.Counter(r['qa_id'] for r in rows)
 invalid=bundle['repair_summary']['a3_kept_invalid_qa_ids']
 assert isinstance(invalid,list) and all(isinstance(q,str) for q in invalid) and len(invalid)==len(set(invalid))==2
 assert all(counts[q]==1 and next(r for r in rows if r['qa_id']==q)['format'] in ('ordering_3','ordering_4') for q in invalid)
 partition=collections.Counter();candidates=[];excluded=[]
 for i,r in enumerate(rows):
  if r['format'] not in ('ordering_3','ordering_4'):reason='NOT_ORDERING';record=None
  elif r['qa_id'] in invalid:reason='PUBLISHER_ROOT_INVALID';record=None
  else:reason,record=old.eligible(r,counts,api)
  partition[reason]+=1
  if record is None:excluded.append(dict(index=i,qa_id=r['qa_id'],reason=reason));continue
  observation=record['observation'];payload=canonical(observation).encode()
  candidates.append(dict(index=i,observation=observation,media=record['media'],events=record['events'],digest=sha(b'VLM072/select/'+payload)))
 candidates.sort(key=lambda x:(x['digest'],canonical(x['observation']).encode()))
 unique={}
 for x in candidates:unique.setdefault(x['observation']['video_id'],x)
 selected=list(unique.values())[:24]
 assert dict(partition)=={'NOT_ORDERING':2218,'PUBLISHER_ROOT_INVALID':2,'EXPLICIT_TEMPORAL_WORD_IN_EVENT':12,'ELIGIBLE_OBSERVATION':91},'PARTITION_DIFFERS'
 assert len(selected)==24 and len(unique)==91 and path==['items']
 return rows,dict(selected=selected,partition=dict(partition),exclusions=excluded,root_invalid=invalid)

def input_gate(source,root,control):
 """One bounded directory/three-original gate; missing inputs do not start a run."""
 start=time.monotonic();source=Path(source);root=Path(root);control=Path(control)
 assert not root.exists(),'EXISTING_ROOT_DO_NOT_RESTART'
 assert source.is_file() and source.stat().st_size<=516*MIB,'MISSING_OR_OVERSIZE_PACKAGE'
 seal=read(control/'code-seal.json')
 for x in seal['files']:assert sha(Path(x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256']
 with zipfile.ZipFile(source) as z:
  infos=z.infolist();names=[x.filename for x in infos];files=[x for x in infos if not x.is_dir()]
  assert len(infos)<=256 and sum(len(n.encode())+46 for n in names)<=8*MIB
  seen=set()
  for x in infos:
   parts=x.filename.replace('\\','/').split('/');key=x.filename.casefold()
   assert key not in seen and not x.filename.startswith(('/','\\')) and not re.match(r'^[A-Za-z]:',x.filename) and '..' not in parts and not(x.flag_bits&1) and not stat.S_ISLNK(x.external_attr>>16) and x.file_size/max(1,x.compress_size)<=100,'UNSAFE_DIRECTORY'
   seen.add(key)
  assert len(files)==33,'PACKAGE_NOT_33_FILES'
  def unique(name):
   matches=[x for x in files if Path(x.filename).name==name];assert len(matches)==1,'MISSING_OR_AMBIGUOUS_'+name;return matches[0]
  src={}
  for name,cap in CAPS.items():
   entry=unique(name);assert entry.file_size<=cap;src[name]=z.read(entry)
   assert not src[name].lstrip().lower().startswith((b'<html',b'<!doctype html'))
  assert sum(map(len,src.values()))==1847197
  api=json.loads(src['api.json']);assert api['sha']==REV and api['private'] is False and api['gated'] is False
  for name in ('README.md','answer_final.json'):
   e=[x for x in api['siblings'] if x['rfilename']==name];assert len(e)==1;e=e[0];b=src[name];assert e['size']==len(b)
   if e.get('lfs'):assert e['lfs']['sha256']==sha(b) and e['lfs']['size']==len(b)
   else:assert e['blobId']==hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  # Only metadata selection; no video payload or source label consumed by workers.
  bundle=json.loads(src['answer_final.json']);rows,selection=choose(api,bundle)
  media=[]
  for item in selection['selected']:
   e=item['media'];assert e['status']=='UNIQUE_EXACT_VIDEO_ID_TO_API_FILENAME_STEM'
   entry=unique(Path(e['path']).name);assert entry.file_size==e['size'];media.append(entry)
  assert len(set(x.filename for x in media))==24 and sum(x.file_size for x in media)==103041283
  nonmedia=[x for x in files if x not in media];assert len(nonmedia)==9
  assert sum(x.file_size for x in nonmedia)<=8*MIB
  package_meta={x.filename:(src[Path(x.filename).name] if Path(x.filename).name in src else z.read(x)) for x in nonmedia}
  manifest_entry=unique('source-package-manifest.json');manifest=json.loads(package_meta[manifest_entry.filename])
  # Declared allowlist may be nested; require every complete member string to
  # occur in this explicit package manifest, with self-name allowed separately.
  strings=set()
  def strings_in(v):
   if isinstance(v,str):strings.add(v)
   elif isinstance(v,dict):
    for k,x in v.items():strings.add(k);strings_in(x)
   elif isinstance(v,list):
    for x in v:strings_in(x)
  strings_in(manifest)
  assert all(x.filename in strings or x.filename==manifest_entry.filename for x in files),'MANIFEST_ALLOWLIST_MISSING'
  assert time.monotonic()-start<=30,'INPUT_GATE_TIME'
  free=shutil.disk_usage(root.parent).free;assert free>=4*1024**3
  # Only the bounded private preflight control area exists here. Freeze the
  # observation-only list before binding order; move it after full admission.
  save(control/'selection-frozen.json',selection)
  observations=[];labels=[];questions=set()
  for i,x in enumerate(selection['selected']):
   r=rows[x['index']];order=r['correct_order'];assert isinstance(order,list) and len(order)==len(set(order))==len(x['events']) and set(order)==set(x['events'])
   events=x['observation']['events'];ids=sorted(events,key=lambda s:s.encode());filtered=[s for s in order if s in ids]
   qs=[TEMPLATE.format(events[a],events[b]) for a,b in itertools.permutations(ids,2)];ys=[int(filtered.index(a)<filtered.index(b)) for a,b in itertools.permutations(ids,2)]
   assert len(qs)==6 and sum(ys)==3 and all(tau(tau(q))==q and tau(q) in qs for q in qs)
   observations.append(dict(index=i,video=x['observation']['video_id'],media=x['media'],questions=qs));labels.append(dict(index=i,labels=ys));questions.update(qs)
  assert len(questions)==28 and collections.Counter(rows[x['index']]['format'] for x in selection['selected'])=={'ordering_3':6,'ordering_4':18}
  # Check explicit handed-off selection candidates without interpreting original
  # QA prose. Require some declared 24-list with the same ordered QA identities.
  expected=[x['observation']['qa_id'] for x in selection['selected']];declared=[]
  def ids_in(v):
   if isinstance(v,dict):
    if 'qa_id' in v and isinstance(v['qa_id'],str):return [v['qa_id']]
    out=[]
    for x in v.values():out.extend(ids_in(x))
    return list(dict.fromkeys(out))
   if isinstance(v,list):
    out=[]
    for x in v:out.extend(ids_in(x))
    return list(dict.fromkeys(out))
   return []
  def declared_lists(v):
   if isinstance(v,list):
    if len(v)==24:declared.append(ids_in(v))
    for x in v:declared_lists(x)
   elif isinstance(v,dict):
    for x in v.values():declared_lists(x)
  for name,b in package_meta.items():
   if Path(name).name not in CAPS and name.endswith('.json'):declared_lists(json.loads(b))
  assert expected in declared,'HANDED_SELECTION_MISMATCH'
  assert time.monotonic()-start<=30,'INPUT_GATE_TIME'
  # All input checks passed; now create the one exclusive research root.
  root.mkdir();save(root/'parent-clock.json',read(control/'parent-clock.json'))
  save(root/'code-seal.json',seal);(root/'package').mkdir()
  for name,b in package_meta.items():
   p=root/'package'/name;p.parent.mkdir(parents=True,exist_ok=True)
   with open(p,'xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
   os.chmod(p,0o444)
  shutil.move(str(control/'selection-frozen.json'),str(root/'selection.json'))
  save(root/'gate.json',dict(status='PASS',seconds=time.monotonic()-start,initial_free_bytes=free,source_logical_bytes=sum(map(len,src.values())),package_metadata_bytes=sum(map(len,package_meta.values())),zip_bytes=source.stat().st_size,source=str(source),source_member_names={k:unique(k).filename for k in CAPS},metadata_members=[x.filename for x in nonmedia],media_directory=[dict(member=x.filename,compressed=x.compress_size,size=x.file_size,crc=x.CRC) for x in media],provenance='USER_SUPPLIED_FIXED_REVISION_COPY / OFFLINE_CROSS_FILE_IDENTITIES_MATCH'))
  save(root/'observations.json',observations);save(root/'scoring-labels.json',labels)
  save(root/'admission-private.json',dict(status='PASS',partition=selection['partition'],selected_k=24,valid=24,unknown=0,questions=144,unique_q=28,media_bytes=103041283,provenance='USER_SUPPLIED_FIXED_REVISION_COPY',raw_root_metadata={k:v for k,v in bundle.items() if k!='items'}))
 print('INPUT_GATE_AND_REGISTERED_SELECTION_CLOSED',flush=True)

def unpack(root):
 root=Path(root);sealed(root);g=read(root/'gate.json');p=Path(g['source']);start=time.monotonic();save(root/'archive-hash-started.json',dict(state='STARTED',bytes=p.stat().st_size))
 h=digest(p);save(root/'archive-identity.json',dict(sha256=h,bytes=p.stat().st_size,seconds=time.monotonic()-start,kind='USER_SUPPLIED_CONTAINER_SELF_IDENTITY_NOT_UPSTREAM_ATTESTATION'))
 obs=read(root/'observations.json');(root/'media').mkdir();records=[];compressed=written=0
 with zipfile.ZipFile(p) as z:
  for i,(d,o) in enumerate(zip(g['media_directory'],obs)):
   event(root/'extraction.jsonl',event='STARTED',index=i)
   compressed+=d['compressed'];assert compressed<=512*MIB
   fpath=root/'media'/f'{i}.mp4';sh=hashlib.sha256();gh=hashlib.sha1();gh.update(b'blob '+str(d['size']).encode()+b'\0');crc=n=0
   with z.open(d['member']) as f,open(fpath,'xb') as out:
    for b in iter(lambda:f.read(MIB),b''):
     n+=len(b);written+=len(b);assert n<=d['size'] and written<=512*MIB;sh.update(b);gh.update(b);crc=zlib.crc32(b,crc);out.write(b)
    out.flush();os.fsync(out.fileno())
   assert n==d['size'] and (crc&0xffffffff)==d['crc']
   identity=o['media']['identity'];assert identity['value']==(sh.hexdigest() if identity['kind']=='LFS_SHA256' else gh.hexdigest())
   records.append(dict(index=i,path=str(fpath),sha256=sh.hexdigest(),size=n,crc=crc&0xffffffff));os.chmod(fpath,0o444);event(root/'extraction.jsonl',event='CLOSED',index=i)
 save(root/'media-manifest.json',dict(records=records,compressed_bytes=compressed,uncompressed_bytes=written));snapshot(root)

class Access:
 def __init__(self,root,role):self.root=Path(root);self.role=role;self.cache={};self.counts=collections.Counter();self.files=[]
 def data(self,p,kind='metadata',expected=None):
  p=Path(p);key=str(p.resolve())
  if key not in self.cache:
   b=p.read_bytes();self.cache[key]=b;self.counts[kind]+=len(b);self.files.append(dict(path=key,kind=kind,bytes=len(b),sha256=sha(b)))
   earlier=collections.Counter()
   for f in self.root.glob('*-access.json'):earlier.update(read(f)['counts'])
   for k,cap in [('feature',128*MIB),('state',64*MIB),('metadata',64*MIB)]:require(self.root,earlier[k]+self.counts[k]<=cap,'OLD_READ_LIMIT',dict(kind=k,bytes=earlier[k]+self.counts[k]),cap)
   (self.root/(self.role+'-access-progress.json')).write_text(canonical(dict(counts=self.counts,files=self.files)),encoding='utf-8')
  b=self.cache[key]
  if expected:require(self.root,sha(b)==expected,'OLD_CONTENT_IDENTITY',p.name,'original sealed identity')
  return b
 def meta(self,p,expected=None):return json.loads(self.data(p,'metadata',expected).decode('utf-8-sig'))
 def tensor(self,p,kind,expected):
  import torch
  return torch.load(io.BytesIO(self.data(p,kind,expected)),map_location='cpu',weights_only=True)
 def finish(self):save(self.root/(self.role+'-access.json'),dict(counts=self.counts,files=self.files))

def assets(root):
 t=cpu();root=Path(root);sealed(root);a=Access(root,'assets');base=root.parent
 p68=base/'vlm-private-068';p70=base/'vlm-private-070';p63=base/'vlm-private-063'
 for p in (p68,p70,p63):assert a.meta(p/'parent-closed.json')['push']=='SUCCEEDED'
 cseal=a.meta(p68/'complete-code-seal.json');cat=a.meta(p68/'asset-catalog.json',cseal['asset_catalog_sha256'])
 ins=a.meta(p70/'input-seal.json');outs=a.meta(p70/'output-seal.json');assert sha(a.data(p70/'input-seal.json'))==outs['input_seal_sha256']
 tr=a.meta(p70/'training-seal.json',outs['training_seal_sha256']);assert tr['updates']==6000
 ex={x['name']:x['sha256'] for x in ins['files']}
 norm=a.tensor(cat['normalizer']['path'],'state',cat['normalizer']['expected_sha256'])
 snorm=a.tensor(p70/'new-normalizer.pt','state',ex['new-normalizer.pt'])
 views=a.tensor(p70/'views.pt','feature',ex['views.pt']);oldh=a.tensor(p70/'h.pt','feature',ex['h.pt'])
 bindings=a.meta(p70/'transform-bindings.json',ex['transform-bindings.json']);sources=a.meta(p70/'sources.json',ex['sources.json'])
 canon=bindings['canonical'];assert len(canon)==len(set(canon))==42 and canon==sorted(canon,key=lambda q:q.encode())
 assert len(bindings['train'])==84 and all(q in views['S'] for q in canon)
 for stats in (norm['C_CENTER'],norm['D_ROLE'],snorm):
  assert stats['mu'].shape==(2560,) and stats['mu'].dtype==t.float64 and stats['scale'].shape==() and stats['scale'].dtype==t.float64 and t.isfinite(stats['mu']).all() and t.isfinite(stats['scale']) and stats['scale']>1e-8
 heads=list(cat['heads']);heads.extend(dict(method=Path(x['path']).parent.name.rsplit('-',1)[0],seed=int(Path(x['path']).parent.name.rsplit('-',1)[1]),path=x['path'],expected_sha256=x['sha256']) for x in tr['files'])
 assert {(x['method'],x['seed']) for x in heads}==set(itertools.product(METHODS,SEEDS)) and len(heads)==36
 (root/'states').mkdir();newheads=[];stateclasses=helper('question_temporal_056').TemporalHead
 for x in sorted(heads,key=lambda x:(METHODS.index(x['method']),SEEDS.index(x['seed']))):
  b=a.data(x['path'],'state',x['expected_sha256']);state=t.load(io.BytesIO(b),map_location='cpu',weights_only=True)
  assert all(v.dtype==t.float32 and t.isfinite(v).all() for v in state.values())
  model=stateclasses(2560,2560);model.load_state_dict(state,strict=True);assert sum(p.numel() for p in model.parameters())==356673
  dest=root/'states'/f"{x['method']}-{x['seed']}.pt";dest.write_bytes(b);newheads.append(dict(method=x['method'],seed=x['seed'],path=str(dest),sha256=sha(b)))
 obs=read(root/'observations.json');qs=sorted({q for x in obs for q in x['questions']},key=lambda q:q.encode())
 # Closed text feature reuse uses exactly the old model/cache chain; no recompute.
 reused={q:oldh[q] for q in qs if q in oldh}
 for q,v in reused.items():assert v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all()
 t.save(dict(normalizer=norm,S_normalizer=snorm,canonical=canon,anchor_S={q:views['S'][q] for q in canon},reused_text=reused),root/'frozen-statistics.pt')
 modelbytes=0;start=time.monotonic()
 for name,expected in cat['model_file_sha256'].items():
  p=Path(cat['model_root'])/name;modelbytes+=p.stat().st_size;assert modelbytes<=12*1024**3;assert digest(p)==expected,'MODEL_IDENTITY'
 save(root/'model-identity.json',dict(bytes=modelbytes,seconds=time.monotonic()-start,status='PASS'))
 import sys
 for name,expected in cat['runtime60']['installed_sources'].items():assert digest(Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/name)==expected
 ledgers=[]
 for prior in (Path(cat['prior057']),Path(cat['prior060']),p68):
  calls=prior/'model-calls';starts=list(calls.glob('*.started'));assert starts and len(starts)<=1088
  for f in starts:
   record=a.meta(f);closed=f.with_suffix('.closed');assert closed.is_file() and not f.with_suffix('.failed').exists(),'UNRESOLVED_OLD_STARTED'
   # Do not open B0 results; identities only.
   ledgers.append(dict(mode=record['mode'],identity=record['input_identity'],closed=str(closed)))
 # If a matching historical call lacks the sealed070 text cache, do not ask again.
 for q in qs:
  assert q in reused or not any(x['mode']=='text_feature' and x['identity']==q for x in ledgers),'MISSING_CLOSED_OLD_TEXT_CACHE'
 old68=a.meta(p68/'prepared-inputs.json');oldpix={x['pixels_sha256']:x for x in old68['records']};oldrgb={x['rgb_sha256'] for x in old68['records']}
 for c in cat['old_cache_records']:oldrgb.update(x['sha256'] for x in c['records'].values())
 oldmedia={x['sha256'] for x in cat['old_media_records']}
 for x in read(root/'media-manifest.json')['records']:assert x['sha256'] not in oldmedia,'OLD_MEDIA_COLLISION_REQUIRES_EXACT_REUSE_ADMISSION'
 save(root/'asset-catalog.json',dict(model_root=cat['model_root'],heads=newheads,source_model_identity=cat['model_file_sha256'],old_rgb=list(oldrgb),old_pixels=list(oldpix),old_pixel_details={k:dict(index=v['index'],name=v['name']) for k,v in oldpix.items()},reused_questions=list(reused),statistics_sha256=digest(root/'frozen-statistics.pt'),old_feature_cache='070 h original sealed; anchor_S from070 original views',ledger_count=len(ledgers),old_pixel_057060='UNKNOWN_NO_REGISTERED_SUMMARY',old_text_token_057060='UNKNOWN_NO_REGISTERED_SUMMARY'))
 # One CPU processor-only fixture, never a learned head forward.
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 import numpy as np
 proc=AutoProcessor.from_pretrained(cat['model_root'],local_files_only=True,trust_remote_code=False)
 save(root/'processor-fixture-started.json',dict(calls=1))
 data=proc.video_processor(videos=[np.zeros((12,224,224,3),dtype=np.uint8)],video_metadata=[VideoMetadata(total_num_frames=12,fps=12,duration=1,width=224,height=224,frames_indices=list(range(12)))],do_sample_frames=False,do_resize=False,return_tensors='pt')
 assert data['video_grid_thw'].tolist()==[[6,14,14]] and list(data['pixel_values_videos'].shape)==[1176,1536]
 save(root/'processor-fixture-closed.json',dict(status='PASS',calls=1,model_loads=0,head_forward=0))
 # Full prepared-input plan/code identity before any real DECODE STARTED.
 save(root/'decode-input-seal.json',dict(observations=digest(root/'observations.json'),media_manifest=digest(root/'media-manifest.json'),assets=digest(root/'asset-catalog.json'),code_seal=digest(root/'code-seal.json')))
 a.finish();assert not t.cuda.is_initialized();print('FROZEN36_ASSETS_CLOSED',flush=True)

def decode(root):
 t=cpu();root=Path(root);sealed(root)
 import av,numpy as np
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 a=read(root/'asset-catalog.json');seal=read(root/'decode-input-seal.json')
 for key,name in [('observations','observations.json'),('media_manifest','media-manifest.json'),('assets','asset-catalog.json'),('code_seal','code-seal.json')]:assert digest(root/name)==seal[key]
 proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
 (root/'frames').mkdir();(root/'prepared').mkdir();records=[];total=0;start=time.monotonic();seen={}
 for entry in read(root/'media-manifest.json')['records']:
  i=entry['index'];event(root/'decode-ledger.jsonl',event='STARTED',index=i)
  with av.open(entry['path']) as container:
   stream=container.streams.video[0];fps=float(stream.average_rate or 0);nf=stream.frames;duration=float(stream.duration*stream.time_base) if stream.duration else float(container.duration/av.time_base) if container.duration else None
   base=float((stream.start_time or 0)*stream.time_base);assert duration and duration>0 and fps>0
   targets=base+(np.arange(12)+.5)*duration/12;best=[None]*12;dist=np.full(12,np.inf);indices=[None]*12;stamps=[None]*12;traversed=0
   for j,frame in enumerate(container.decode(stream)):
    total+=1;traversed+=1;require(root,total<=100000 and time.monotonic()-start<850,'DECODE_BUDGET',{'frames':total,'seconds':time.monotonic()-start},{'frames':100000,'seconds':900})
    if frame.pts is None:continue
    stamp=float(frame.pts*stream.time_base);delta=np.abs(targets-stamp);update=np.where(delta<dist)[0]
    if len(update):
     rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
     for k in update:best[k]=rgb;dist[k]=delta[k];indices[k]=j;stamps[k]=stamp
   require(root,all(x is not None for x in best) and len(set(indices))==12,'INSUFFICIENT_UNIQUE_TIMESTEPS',len(set(indices)),12)
   clock=max(abs(s-base-j/fps) for s,j in zip(stamps,indices));require(root,clock<=1/fps,'FRAME_INDEX_CLOCK_NOT_CFR',clock,1/fps)
   array=np.stack(best);assert array.shape==(12,224,224,3) and array.dtype==np.uint8
   path=root/'frames'/f'{i}.npy'
   with open(path,'xb') as f:np.save(f,array,allow_pickle=False)
   rgbhash=digest(path)
   require(root,rgbhash not in set(a['old_rgb']),'OLD_RGB_INPUT_COLLISION',True,False)
   data=proc.video_processor(videos=[array],video_metadata=[VideoMetadata(total_num_frames=nf,fps=fps,duration=duration,width=224,height=224,frames_indices=indices)],do_sample_frames=False,do_resize=False,return_tensors='pt')
   assert data['video_grid_thw'].tolist()==[[6,14,14]] and list(data['pixel_values_videos'].shape)==[1176,1536] and t.isfinite(data['pixel_values_videos']).all()
   data=dict(pixel_values_videos=data['pixel_values_videos'].to(t.bfloat16),video_grid_thw=data['video_grid_thw']);pixelhash=sha(data['pixel_values_videos'].view(t.uint8).numpy().tobytes()+data['video_grid_thw'].numpy().tobytes())
   require(root,pixelhash not in set(a['old_pixels']),'OLD_PREPARED_INPUT_COLLISION',True,False)
   prepared=root/'prepared'/f'{i}.pt'
   with open(prepared,'xb') as f:t.save(data,f)
   alias=seen.get(pixelhash);seen.setdefault(pixelhash,i)
   records.append(dict(index=i,path=str(prepared),sha256=digest(prepared),rgb_sha256=rgbhash,pixels_sha256=pixelhash,alias=alias,frames=traversed,indices=indices,timestamps=stamps,targets=targets.tolist(),fps=fps,duration=duration,base=base,max_clock_error=clock))
  event(root/'decode-ledger.jsonl',event='CLOSED',index=i,frames_total=total)
 qs=sorted({q for x in read(root/'observations.json') for q in x['questions']},key=lambda q:q.encode());tokens={}
 for q in qs:
  b=proc.tokenizer(q,return_tensors='pt');n=int(b['attention_mask'].sum());assert n<=128;tokens[q]=dict(length=n,identity=sha(canonical({k:v.tolist() for k,v in b.items()}).encode()))
 save(root/'prepared-inputs.json',dict(records=records,questions=qs,tokens=tokens,decoded_frames=total,seconds=time.monotonic()-start))
 save(root/'input-seal.json',dict(status='CLOSED',prepared_inputs=digest(root/'prepared-inputs.json'),assets=digest(root/'asset-catalog.json'),observations=digest(root/'observations.json')));assert not t.cuda.is_initialized();snapshot(root);print('DECODED24_CLOSED',total,flush=True)

def gpu(root):
 import torch as t,gc
 from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
 root=Path(root);sealed(root);a=read(root/'asset-catalog.json');p=read(root/'prepared-inputs.json');seal=read(root/'input-seal.json');start=read(root/'gpu-clock.json')['start_monotonic'];deadline=start+480
 for key,name in [('prepared_inputs','prepared-inputs.json'),('assets','asset-catalog.json'),('observations','observations.json')]:assert digest(root/name)==seal[key]
 for x in p['records']:assert digest(x['path'])==x['sha256']
 counts=dict(video_feature=0,text_feature=0,root_forward=0,visual_forward=0,decoder_forward=0,decoder_layer_forward=0)
 stats=t.load(root/'frozen-statistics.pt',map_location='cpu',weights_only=True);index=dict(video={},text={});(root/'features').mkdir();(root/'model-calls').mkdir();model=None
 def hook(k):
  def inc(*args,**kwargs):counts[k]+=1
  return inc
 def call(kind,identity,fn):
  require(root,time.monotonic()<deadline and counts['video_feature']+counts['text_feature']<52 and counts[kind]<(24 if kind=='video_feature' else 28),'GPU_LIMIT',counts,52)
  key=sha(canonical([kind,identity,a['source_model_identity']]).encode());base=root/'model-calls'/key
  save(str(base)+'.started',dict(status='STARTED',mode=kind,input_identity=identity));counts[kind]+=1
  try:
   v=fn();t.cuda.synchronize();assert t.isfinite(v).all();require(root,t.cuda.max_memory_allocated()<=16*1024**3,'GPU_ALLOCATED',t.cuda.max_memory_allocated(),16*1024**3)
   path=root/'features'/(key+'.pt');t.save(v,path);r=dict(path=str(path),sha256=digest(path),shape=list(v.shape),kind='NEW');save(str(base)+'.closed',dict(status='CLOSED',result=r));return r
  except Exception as e:save(str(base)+'.failed',dict(status='FAILED',reason=str(e)));raise
 try:
  save(root/'weight-load-started.json',dict(state='STARTED',epoch=time.time()))
  model=Qwen3VLForConditionalGeneration.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False,torch_dtype=t.bfloat16,attn_implementation='sdpa').to('cuda');model.eval();model.requires_grad_(False)
  model.register_forward_pre_hook(hook('root_forward'));model.model.visual.register_forward_pre_hook(hook('visual_forward'));model.model.language_model.register_forward_pre_hook(hook('decoder_forward'))
  for layer in model.model.language_model.layers:layer.register_forward_pre_hook(hook('decoder_layer_forward'))
  proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
  with t.no_grad():
   for x in p['records']:
    if x['alias'] is not None:index['video'][str(x['index'])]=dict(index['video'][str(x['alias'])],kind='ALIAS');continue
    def video(x=x):
     data=t.load(x['path'],map_location='cpu',weights_only=True);out=model.get_video_features(**{k:v.to('cuda') for k,v in data.items()});main=out[0]
     assert isinstance(main,(list,tuple)) and len(main)==1 and main[0].shape==(294,2560)
     return main[0].reshape(6,49,2560).mean(1).float().cpu()
    index['video'][str(x['index'])]=call('video_feature',x['pixels_sha256'],video)
   for q in p['questions']:
    if q in stats['reused_text']:
     path=root/'features'/('reused-'+sha(q.encode())+'.pt');t.save(stats['reused_text'][q],path);index['text'][q]=dict(path=str(path),sha256=digest(path),shape=[2560],kind='REUSED');continue
    def text(q=q):
     b=proc.tokenizer(q,return_tensors='pt').to('cuda');o=model.model(**b,use_cache=False,return_dict=True);v=o.last_hidden_state[0,int(b['attention_mask'].sum())-1].float().cpu();assert v.shape==(2560,);return v
    index['text'][q]=call('text_feature',q,text)
  assert len(index['video'])==24 and len(index['text'])==28 and all(not p.requires_grad and p.grad is None for p in model.parameters())
  save(root/'feature-index.json',index);save(root/'feature-seal.json',dict(status='CLOSED',index_sha256=digest(root/'feature-index.json'),counts=counts,peak_allocated_bytes=t.cuda.max_memory_allocated(),loads=1,b0=0,backward=0,optimizer=0))
 finally:
  save(root/'gpu-counts.json',dict(counts=counts,peak_allocated_bytes=t.cuda.max_memory_allocated(),outer_seconds=time.monotonic()-start));del model;gc.collect()
  if t.cuda.is_initialized():t.cuda.empty_cache();t.cuda.synchronize()

def predict(root):
 t=cpu();root=Path(root);sealed(root);j=read(root/'gpu-job.json');assert j['active']==j['exit_code']==0
 a=read(root/'asset-catalog.json');ix=read(root/'feature-index.json');assert digest(root/'feature-index.json')==read(root/'feature-seal.json')['index_sha256']
 def tensor(r):
  assert digest(r['path'])==r['sha256'];return t.load(r['path'],map_location='cpu',weights_only=True)
 V={int(k):tensor(v) for k,v in ix['video'].items()};Q={q:tensor(v) for q,v in ix['text'].items()}
 assert all(v.shape==(6,2560) and v.dtype==t.float32 and t.isfinite(v).all() for v in V.values()) and all(v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all() for v in Q.values())
 assert digest(root/'frozen-statistics.pt')==a['statistics_sha256'];stats=t.load(root/'frozen-statistics.pt',map_location='cpu',weights_only=True);normal=stats['normalizer'];sn=stats['S_normalizer'];obs=read(root/'observations.json');old=helper('semantic_role_factor_070')
 C={q:((v.double()-normal['C_CENTER']['mu'])/normal['C_CENTER']['scale']).float() for q,v in Q.items()}
 R={q:(((v.double()-Q[tau(q)].double())/2-normal['D_ROLE']['mu'])/normal['D_ROLE']['scale']).float() for q,v in Q.items()}
 S={q:(((v.double()+Q[tau(q)].double())/2-sn['mu'])/sn['scale']).float() for q,v in Q.items()}
 anchors={q:old.anchor(q,stats['canonical']) for q in Q};assert all(anchors[q] in stats['anchor_S'] for q in Q)
 outputs=[];new=aliases=0
 with t.no_grad():
  for item in a['heads']:
   model=old.headclass()(2560,2560) if item['method'] in METHODS[2:] else helper('question_temporal_056').TemporalHead(2560,2560)
   assert digest(item['path'])==item['sha256'];model.load_state_dict(t.load(item['path'],map_location='cpu',weights_only=True));model.eval();model.requires_grad_(False);cache={}
   for row in obs:
    i=row['index']
    for qi,q in enumerate(row['questions']):
     key=[item['method'],item['seed'],i,qi];event(root/'prediction-ledger.jsonl',event='STARTED',key=key)
     method=item['method'];vectors=[V[i],C[q] if method=='C_NATIVE' else R[q]] if method in METHODS[:2] else [V[i],S[q],R[q],stats['anchor_S'][anchors[q]]]
     signature=b''.join(x.contiguous().numpy().tobytes() for x in vectors);sig=sha(signature)
     if sig in cache:
      assert cache[sig]['input']==signature;z=cache[sig]['logit'];kind='ALIAS';aliases+=1
     else:
      if method in METHODS[:2]:o=model(vectors[0][None],vectors[1][None])
      else:o=model(*(x[None] for x in vectors),method)
      assert o.numel()==1 and t.isfinite(o).all();z=float(o.item());cache[sig]=dict(input=signature,logit=z);new+=1;kind='NEW'
     outputs.append(dict(method=method,seed=item['seed'],index=i,question=qi,prediction=int(z>0),logit=z,kind=kind,status='CLOSED'));event(root/'prediction-ledger.jsonl',event='CLOSED',key=key,kind=kind)
   assert all(not p.requires_grad and p.grad is None for p in model.parameters());print('FROZEN_HEAD_CLOSED',method,item['seed'],flush=True)
 assert len(outputs)==5184 and new+aliases==5184 and not t.cuda.is_initialized();save(root/'outputs.json',outputs);save(root/'prediction-seal.json',dict(status='CLOSED',output_sha256=digest(root/'outputs.json'),new_forward=new,aliases=aliases,reused=0,logical=5184,backward=0,optimizer=0))

def quantile(values,p):
 v=sorted(values);x=(len(v)-1)*p;i=int(x);return v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
def score(root):
 root=Path(root);sealed(root);j=read(root/'prediction-job.json');assert j['active']==j['exit_code']==0
 assert digest(root/'outputs.json')==read(root/'prediction-seal.json')['output_sha256']
 outputs=read(root/'outputs.json');lookup={(x['method'],x['seed'],x['index'],x['question']):x for x in outputs};assert len(lookup)==len(outputs)==5184 and set(lookup)==set(itertools.product(METHODS,SEEDS,range(24),range(6)))
 labels=read(root/'scoring-labels.json');conditions=[];detail={};obs=read(root/'observations.json')
 for method in METHODS:
  for seed in SEEDS:
   cnt=collections.Counter();ds=[]
   for i,row in enumerate(obs):
    ps=[lookup[method,seed,i,q] for q in range(6)];assert all(x['status']=='CLOSED' and x['prediction'] in (0,1) for x in ps)
    p=[x['prediction'] for x in ps];y=labels[i]['labels'];correct=sum(x==z for x,z in zip(p,y));allcorrect=int(correct==6);cnt['correct_cells']+=correct;cnt['six_way_correct']+=allcorrect;cnt['constant_videos']+=len(set(p))==1
    qs=row['questions'];cnt['complementary_pairs']+=sum(p[q]+p[qs.index(tau(qs[q]))]==1 for q in range(6))/2
    cnt['new_cells']+=sum(x['kind']=='NEW' for x in ps);cnt['alias_cells']+=sum(x['kind']=='ALIAS' for x in ps);ds.append(allcorrect)
   detail[method,seed]=ds;conditions.append(dict(method=method,seed=seed,status='CLOSED',planned_items=24,planned_cells=144,new_cells=cnt['new_cells'],reused_cells=0,alias_cells=cnt['alias_cells'],CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,correct_cells=cnt['correct_cells'],six_way_correct=cnt['six_way_correct'],complementary_pairs=int(cnt['complementary_pairs']),constant_videos=cnt['constant_videos'],cell_accuracy_pct=100*cnt['correct_cells']/144,six_way_accuracy_pct=100*cnt['six_way_correct']/24,complementary_pct=100*cnt['complementary_pairs']/72))
 pairs=[];hist=[];intervals=[]
 for left,right in COMPARISONS:
  nets=[]
  for seed in SEEDS:
   a=detail[left,seed];b=detail[right,seed];lo=sum(x and not y for x,y in zip(a,b));ro=sum(y and not x for x,y in zip(a,b));net=lo-ro;nets.append(net)
   pairs.append(dict(left=left,right=right,seed=seed,status='CLOSED',planned_items=24,evaluated_items=24,left_only=lo,right_only=ro,both_correct=sum(x and y for x,y in zip(a,b)),both_wrong=sum(not x and not y for x,y in zip(a,b)),unknown=0,net=net,delta_six_way_pp=100*net/24))
  sums=[sum(detail[left,seed][i]-detail[right,seed][i] for seed in SEEDS) for i in range(24)];count=collections.Counter(sums);hist.extend(dict(left=left,right=right,seed_sum=k,count=count[k],status='CLOSED') for k in range(-6,7));vector=[k for k in range(-6,7) for _ in range(count[k])];assert sum(vector)==sum(nets)
  for axis,items,rngseed in [('video',vector,55074),('seed',nets,55075)]:
   rng=random.Random(rngseed);n=len(items);values=[100*sum(items[i] for i in rng.choices(range(n),k=n))/144 for _ in range(10000)]
   intervals.append(dict(left=left,right=right,axis=axis,status='CLOSED',point_pp=100*sum(nets)/144,lower_pp=quantile(values,.025),upper_pp=quantile(values,.975),draws=10000,planned_draws=10000))
 main=[p['net'] for p in pairs if p['left']=='D_NATIVE'];passed=sum(main)>0 and sum(x>0 for x in main)>=5
 save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,histogram=hist,intervals=intervals,main_positive_seeds=sum(x>0 for x in main),main_total_net=sum(main),conclusion='NATIVE_MULTIQUERY_TRANSFER_PILOT_SIGNAL / SELECTIVITY_AND_NOVELTY_UNCONFIRMED' if passed else 'STOP_CURRENT_D_MULTIEVENT_TRANSFER',accuracy_complete=True));print('SCORED_5184',main,flush=True)

def independent(root):
 """Separate oracle entry: no producer selector/scorer calls or learned forward.

    Uses original source buffers and independently written projection/eligibility;
    checks labels and all counts/intervals from frozen predictions, not new calls.
 """
 import json as J,hashlib as H,re as R,itertools as IT,random as RNG
 from collections import Counter as CT
 from pathlib import Path as P
 r=P(root);checks=0
 def test(ok,reason):
  nonlocal checks
  checks+=1
  if not ok:raise AssertionError(reason)
 def get(p):return J.loads(P(p).read_bytes())
 def canon(x):return J.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
 gate=get(r/'gate.json');raw={n:(r/'package'/name).read_bytes() for n,name in gate['source_member_names'].items()};api=J.loads(raw['api.json']);b=J.loads(raw['answer_final.json']);rows=b['items'];flags=b['repair_summary']['a3_kept_invalid_qa_ids'];test(len(flags)==len(set(flags))==2,'root_markers')
 test(api['sha']=='da3065053d958c38151304e33a42e138b1899eaf','revision')
 for n in ['README.md','answer_final.json']:
  e=[x for x in api['siblings'] if x['rfilename']==n];test(len(e)==1,'registered_once');e=e[0];data=raw[n];test(e['size']==len(data),'size')
  test(e.get('lfs',{}).get('sha256')==H.sha256(data).hexdigest() if e.get('lfs') else e['blobId']==H.sha1(('blob %d\0'%len(data)).encode()+data).hexdigest(),'content_id')
 counts=CT(x['qa_id'] for x in rows);test(all(counts[q]==1 for q in flags),'marker_binding');partition=CT();candidates=[]
 for i,x in enumerate(rows):
  if x['format'] not in ['ordering_3','ordering_4']:partition['NOT_ORDERING']+=1;continue
  if x['qa_id'] in flags:partition['PUBLISHER_ROOT_INVALID']+=1;continue
  es=x['events'];texts={e['label']:' '.join(e['event_text'].split()) for e in es};test(len(texts)==len(es) and len(set(texts.values()))==len(texts),'mapping')
  if any(R.search(r'\b(before|after|first|second|third|fourth|then|earlier|later|finally)\b',v,R.I) for v in texts.values()):partition['EXPLICIT_TEMPORAL_WORD_IN_EVENT']+=1;continue
  test(all(v and not R.fullmatch(r'event[ _-]*\d+',v,R.I) for v in texts.values()),'semantic_text')
  # All optional unresolved markers are independently checked rather than defaulted.
  stack=[{k:v for k,v in x.items() if k not in ('correct_order','question','correct_answer')}]
  while stack:
   v=stack.pop()
   if isinstance(v,dict):
    for key,val in v.items():
     test(not(R.search('uncertain|unresolved|pending|ambiguous',key,R.I) and val not in (None,False,0,'',[],{})),'marker_field');stack.append(val)
   elif isinstance(v,list):stack.extend(v)
   elif isinstance(v,str):test(not R.search(r'\b(uncertain|unresolved|pending|ambiguous)\b',v,R.I),'marker_value')
  ids=sorted(texts,key=lambda v:v.encode())[:3];media=[f for f in api['siblings'] if f['rfilename'].startswith('videos/') and P(f['rfilename']).stem==x['video_id'] and P(f['rfilename']).suffix.lower() in ('.mp4','.avi','.mov','.webm','.mkv')];test(len(media)==1,'locator');f=media[0]
  obs={'source_namespace':str(P(f['rfilename']).parent).replace('\\','/'),'video_id':x['video_id'],'qa_id':x['qa_id'],'media_path':f['rfilename'],'events':{k:texts[k] for k in ids}}
  payload=canon(obs).encode();candidates.append((H.sha256(b'VLM072/select/'+payload).hexdigest(),payload,i,obs));partition['ELIGIBLE_OBSERVATION']+=1
 candidates.sort();seen=set();selected=[]
 for c in candidates:
  if c[3]['video_id'] not in seen:seen.add(c[3]['video_id']);selected.append(c)
 selected=selected[:24];frozen=get(r/'selection.json');test(dict(partition)==frozen['partition'],'partition');test([c[3] for c in selected]==[x['observation'] for x in frozen['selected']],'ordered_selection');test(len(selected)==24,'K')
 labels=[];ob=get(r/'observations.json');questions=set()
 for index,c in enumerate(selected):
  x=rows[c[2]];order=x['correct_order'];test(len(order)==len(set(order))==len(x['events']) and set(order)=={e['label'] for e in x['events']},'full_order');es=c[3]['events'];ids=sorted(es,key=lambda k:k.encode());qs=[];ys=[]
  for aa in ids:
   for bb in ids:
    if aa==bb:continue
    q='Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(es[aa],es[bb]);m=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);test(m is not None and m.groups()==(es[aa],es[bb]),'tau_binding');qs.append(q);ys.append(int(order.index(aa)<order.index(bb)));questions.add(q)
  test(qs==ob[index]['questions'],'question_strings');test(sum(ys)==3,'balance');labels.append(dict(index=index,labels=ys))
 test(labels==get(r/'scoring-labels.json') and len(questions)==28,'labels_and_unique_q')
 ps=get(r/'outputs.json');test(len(ps)==5184,'outputs_n');lut={(x['method'],x['seed'],x['index'],x['question']):x for x in ps};test(len(lut)==5184,'unique_keys')
 agg=get(r/'aggregates.json');methods=['C_NATIVE','D_NATIVE','CONCAT','FACTOR','REVERSE','ANCHOR'];seeds=[137,263,419,557,733,911];detail={}
 for method in methods:
  for seed in seeds:
   row=next(x for x in agg['conditions'] if x['method']==method and x['seed']==seed);good=constant=cp=new=alias=0;ds=[]
   for i in range(24):
    pp=[lut[method,seed,i,q] for q in range(6)];test(all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) for x in pp),'closed_binary');pred=[x['prediction'] for x in pp];correct=[x==y for x,y in zip(pred,labels[i]['labels'])];good+=sum(correct);ds.append(int(all(correct)));constant+=len(set(pred))==1
    qs=ob[i]['questions'];checked=set()
    for qi,q in enumerate(qs):
     m=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);other=qs.index('Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(m[2],m[1]));edge=tuple(sorted([qi,other]))
     if edge not in checked:cp+=pred[qi]!=pred[other];checked.add(edge)
    new+=sum(x['kind']=='NEW' for x in pp);alias+=sum(x['kind']=='ALIAS' for x in pp)
   detail[method,seed]=ds
   for key,val in dict(correct_cells=good,six_way_correct=sum(ds),constant_videos=constant,complementary_pairs=cp,new_cells=new,alias_cells=alias,reused_cells=0,CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0).items():test(row[key]==val,'condition_'+key)
 for pair in agg['pairs']:
  aa=detail[pair['left'],pair['seed']];bb=detail[pair['right'],pair['seed']];lo=sum(x and not y for x,y in zip(aa,bb));ro=sum(y and not x for x,y in zip(aa,bb))
  for key,val in dict(left_only=lo,right_only=ro,both_correct=sum(x and y for x,y in zip(aa,bb)),both_wrong=sum(not x and not y for x,y in zip(aa,bb)),unknown=0,net=lo-ro).items():test(pair[key]==val,'paired_'+key)
 for left,right in [('D_NATIVE','C_NATIVE'),('FACTOR','D_NATIVE'),('FACTOR','CONCAT'),('FACTOR','REVERSE'),('FACTOR','ANCHOR')]:
  net=[sum(detail[left,s])-sum(detail[right,s]) for s in seeds];bins=CT(sum(detail[left,s][i]-detail[right,s][i] for s in seeds) for i in range(24));vector=[]
  for k in range(-6,7):
   row=next(x for x in agg['histogram'] if x['left']==left and x['right']==right and x['seed_sum']==k);test(row['count']==bins[k],'histogram');vector.extend([k]*bins[k])
  for axis,values,seed in [('video',vector,55074),('seed',net,55075)]:
   rng=RNG.Random(seed);n=len(values);draws=sorted(100*sum(values[j] for j in rng.choices(range(n),k=n))/144 for _ in range(10000))
   row=next(x for x in agg['intervals'] if x['left']==left and x['right']==right and x['axis']==axis)
   for p,key in [(.025,'lower_pp'),(.975,'upper_pp')]:
    where=9999*p;k=int(where);answer=draws[k]*(1-(where-k))+draws[min(k+1,9999)]*(where-k);test(abs(answer-row[key])<1e-10,'bootstrap_quantile')
   test(abs(row['point_pp']-100*sum(net)/144)<1e-10 and row['draws']==10000,'bootstrap_point')
 # Recheck new-copy old states/statistics and original identity registration only;
 # no learned inference, and no second old-state payload read.
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1)
 assets=get(r/'asset-catalog.json')
 for x in assets['heads']:
  data=P(x['path']).read_bytes();test(H.sha256(data).hexdigest()==x['sha256'],'state_seal');state=torch.load(io.BytesIO(data),map_location='cpu',weights_only=True);test(sum(v.numel() for v in state.values())==356673 and all(torch.isfinite(v).all() for v in state.values()),'state_shape_finite')
 for name in ['assets','unpack','decode','gpu','prediction','scoring']:
  j=get(r/(name+'-job.json'));test(j['active']==j['exit_code']==0 and not j['killed'],'job_closed')
 test(not torch.cuda.is_initialized(),'review_no_gpu')
 save(r/'independent-review.json',dict(status='PASS',checks=checks,source_logical_bytes=sum(map(len,raw.values())),producer_selector_or_scorer_imports=0,new_forward=0))
 print('INDEPENDENT_PASS',checks,flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('role',choices=['gate','unpack','assets','decode','gpu','predict','score','independent']);p.add_argument('--root',required=True);p.add_argument('--source');p.add_argument('--control');a=p.parse_args();root=Path(a.root)
 try:
  if a.role=='gate':return input_gate(a.source,root,a.control)
  return globals()[dict(predict='predict',score='score').get(a.role,a.role)](root)
 except Exception as e:
  if root.exists():event(root/'stops.jsonl',stage=a.role,reason=str(e) or type(e).__name__,error_type=type(e).__name__)
  raise
if __name__=='__main__':main()
