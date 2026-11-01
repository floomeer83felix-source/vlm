"""068 bounded fixed-member readmission and frozen item transfer. No import-time data/model operations."""
import argparse,ast,hashlib,io,json,os,re,time
from pathlib import Path
SEEDS=(137,263,419,557,733,911)
METHODS=('C_NATIVE','D_NATIVE')
CONTEXT={}
def context(stage,**facts):
 CONTEXT.clear();CONTEXT.update(stage=stage,**facts)
def require(root,ok,reason,actual,limit,**facts):
 if not ok:
  event(root/'failures.jsonl',reason_code=reason,actual=actual,limit=limit,**dict(CONTEXT,**facts))
  raise RuntimeError(reason)
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def tau(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 if not m:raise ValueError('QUESTION_PARSE')
 return f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.'
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024**2),b''):h.update(b)
 return h.hexdigest()

def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(dict(at_unix=time.time(),**x),ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())

def helper(name,path):
 import importlib.util
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def sealed(root):
 for r in read(root/'complete-code-seal.json')['files']:assert digest(r['path'])==r['sha256'],'CODE_IDENTITY'

def assets(root):
 """Identity checks only: no model construction, media or historic features."""
 import sys,torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1)
 sealed(root);a=read(root/'asset-catalog.json');used=0;checks=[];context('ASSET_IDENTITY',completed=0,remaining=13)
 oldmeta=0
 for item in a['metadata_files']:
  oldmeta+=Path(item['path']).stat().st_size
  require(root,digest(item['path'])==item['sha256'],'OLD_CHAIN_IDENTITY',{'path_kind':Path(item['path']).name},'original sealed digest')
 for item in a['heads']+[a['normalizer']]:
  context('OLD_STATE_IDENTITY',completed=len(checks),remaining=13-len(checks),kind=Path(item['path']).name,seed=item.get('seed'),method=item.get('method'))
  data=Path(item['path']).read_bytes();used+=len(data);require(root,used<=32*1024**2,'ASSET_STATE_READ_BUDGET',used,32*1024**2)
  require(root,hashbytes(data)==item['expected_sha256'],'OLD_STATE_IDENTITY',{'matched':hashbytes(data)==item['expected_sha256']},'original content seal')
  state=torch.load(io.BytesIO(data),map_location='cpu',weights_only=True)
  if 'seed' in item:
   h=helper('head056',Path(__file__).with_name('question_temporal_056.py')).TemporalHead(2560,2560);h.load_state_dict(state,strict=True)
   require(root,sum(p.numel() for p in h.parameters())==356673,'HEAD_PARAMETER_COUNT',sum(p.numel() for p in h.parameters()),356673)
   require(root,all(torch.isfinite(v).all() and v.dtype==torch.float32 for v in state.values()),'HEAD_STATE_FINITE_DTYPE',{'finite':all(bool(torch.isfinite(v).all()) for v in state.values()),'dtypes':sorted(set(str(v.dtype) for v in state.values()))},'finite float32')
  else:
   for arm in ('C_CENTER','D_ROLE'):
    s=state[arm];require(root,s['mu'].shape==(2560,) and s['mu'].dtype==torch.float64 and s['scale'].ndim==0 and s['scale'].dtype==torch.float64 and torch.isfinite(s['mu']).all() and torch.isfinite(s['scale']) and s['scale']>1e-8,'NORMALIZER_SHAPE_FINITE',{'arm':arm,'mu_shape':list(s['mu'].shape),'scale_shape':list(s['scale'].shape),'mu_dtype':str(s['mu'].dtype),'scale_dtype':str(s['scale'].dtype),'scale':s['scale'].item()},{'mu_shape':[2560],'scale_shape':[],'dtype':'float64','scale_min':1e-8})
  checks.append(dict(path=item['path'],sha256=hashbytes(data),bytes=len(data)))
 hashes={};weightbytes=0
 for name,expected in a['model_file_sha256'].items():
  context('MODEL_FILE_IDENTITY',file=name,completed=len(hashes),remaining=len(a['model_file_sha256'])-len(hashes))
  p=Path(a['model_root'])/name
  if name.endswith('.safetensors'):weightbytes+=p.stat().st_size
  require(root,weightbytes<=12*1024**3,'WEIGHT_HASH_READ_BUDGET',weightbytes,12*1024**3)
  hashes[name]=digest(p);require(root,hashes[name]==expected,'MODEL_IDENTITY',{'file':name,'matched':hashes[name]==expected},'original sealed digest')
 for name,expected in a['runtime60']['installed_sources'].items():
  p=Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/name;assert digest(p)==expected,'NATIVE_IDENTITY'
 chainbytes=oldmeta;oldmeta=0;ledger=[]
 for prior,rt in ((a['prior057'],a['runtime57']),(a['prior060'],a['runtime60'])):
  calls=Path(prior)/'model-calls';assert calls.is_dir(),'MISSING_PERSISTENT_LEDGER'
  # Only bounded registered ledger directory; never open historic B0 closures.
  starts=list(calls.glob('*.started'));assert len(starts)<=1088
  for p in starts:
   oldmeta+=p.stat().st_size;assert oldmeta<8*1024**2
   x=read(p);closed=p.with_suffix('.closed');failed=p.with_suffix('.failed')
   assert closed.is_file() and not failed.exists(),'UNRESOLVED_OLD_STARTED'
   ledger.append(dict(path=str(p),sha256=digest(p),mode=x['mode'],input_identity=x['input_identity'],closed_path=str(closed)))
  assert starts,'EMPTY_OLD_LEDGER'
 oldqs={x['input_identity'] for x in ledger if x['mode']=='text_feature'}
 assert not oldqs&{q for x in read(root/'observations.json') for q in x['questions']},'INPUT_ALREADY_CONSUMED'
 assert not torch.cuda.is_initialized()
 from transformers import AutoProcessor
 import numpy as np
 from transformers.video_utils import VideoMetadata
 context('CPU_PROCESSOR_FIXTURE',completed=0,remaining=1)
 proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
 save(root/'processor-fixture-started.json',dict(at_unix=time.time(),calls=1,synthetic=True))
 fixture=proc.video_processor(videos=[np.zeros((12,224,224,3),dtype=np.uint8)],video_metadata=[VideoMetadata(total_num_frames=12,fps=12,duration=1,width=224,height=224,frames_indices=list(range(12)))],do_sample_frames=False,do_resize=False,return_tensors='pt')
 require(root,fixture['video_grid_thw'].tolist()==[[6,14,14]] and list(fixture['pixel_values_videos'].shape)==[1176,1536],'FIXTURE_PROCESSOR_SHAPE',{'grid':fixture['video_grid_thw'].tolist(),'pixels':list(fixture['pixel_values_videos'].shape)},{'grid':[[6,14,14]],'pixels':[1176,1536]})
 save(root/'processor-fixture-closed.json',dict(status='CLOSED',calls=1,grid=[[6,14,14]],pixels=[1176,1536],weight_loads=0,head_forward=0))
 save(root/'asset-checks.json',dict(status='CLOSED',state_logical_bytes=used,state_checks=checks,weight_hash_bytes=weightbytes,model_hashes=hashes,chain_metadata_bytes=chainbytes,ledger_logical_bytes=oldmeta,ledger=ledger,cuda_initialized=False,fixture_calls=1))
 print('ASSETS_CLOSED',len(checks),weightbytes,flush=True)

def media(root):
 import zipfile,stat,zlib,av,numpy as np,torch,inspect
 from collections import defaultdict
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 from transformers.models.qwen3_vl import modeling_qwen3_vl
 start=time.monotonic();sealed(root);a=read(root/'asset-catalog.json');check=read(root/'asset-checks.json');obs=read(root/'observations.json');context('ARCHIVE_IDENTITY',completed=0,remaining=1)
 event(root/'media-ledger.jsonl',phase='ARCHIVE_HASH',event='STARTED',bytes=a['archive']['bytes'])
 actual=digest(a['archive']['path']);require(root,actual==a['archive']['expected_sha256'],'STOP_ARCHIVE_IDENTITY',{'matched':actual==a['archive']['expected_sha256'],'bytes':Path(a['archive']['path']).stat().st_size},'registered publisher content SHA256,2783546023B')
 event(root/'media-ledger.jsonl',phase='ARCHIVE_HASH',event='CLOSED',bytes=a['archive']['bytes'])
 names=[v for x in obs for v in x['videos']];require(root,len(names)==len(set(names))==100,'FIXED_MEMBER_COUNT',len(names),100)
 destination=root/'media';destination.mkdir();frames=root/'frames';frames.mkdir();prepared=root/'prepared';prepared.mkdir();entries=[];compressed=uncompressed=0
 oldmedia={x['sha256'] for x in a['old_media_records']};oldrgb={x['sha256'] for m in a['old_cache_records'] for x in m['records'].values()}
 class Measured:
  def __init__(self,p):self.file=open(p,'rb');self.logical_read_bytes=0
  def read(self,n=-1):
   b=self.file.read(n);self.logical_read_bytes+=len(b);return b
  def seek(self,*args):return self.file.seek(*args)
  def tell(self):return self.file.tell()
  def seekable(self):return True
 measured=Measured(a['archive']['path']);context('ZIP_DIRECTORY',completed=0,remaining=100)
 try:
  with zipfile.ZipFile(measured) as z:
   infos=z.infolist();seen=set();bybase=defaultdict(list);unsafe=[]
   for x in infos:
    parts=x.filename.replace('\\','/').split('/');name=x.filename;key=name.casefold()
    safe=not name.startswith(('/','\\')) and not re.match(r'^[A-Za-z]:',name) and '..' not in parts and not (x.flag_bits&1) and not stat.S_ISLNK(x.external_attr>>16) and key not in seen and x.file_size/max(1,x.compress_size)<=100
    if not safe:unsafe.append(dict(name=name,ratio=x.file_size/max(1,x.compress_size),flags=x.flag_bits,external_attr=x.external_attr))
    seen.add(key);bybase[Path(name).name].append(x)
   selected=[];records=[]
   for i,name in enumerate(names):
    matches=bybase[name];x=matches[0] if len(matches)==1 else None
    records.append(dict(index=i,requested=name,matches=len(matches),member=x.filename if x else None,compressed=x.compress_size if x else None,uncompressed=x.file_size if x else None,crc=x.CRC if x else None,method=x.compress_type if x else None,flags=x.flag_bits if x else None));selected.append(x)
   directory_bytes=measured.logical_read_bytes
   save(root/'selected-directory.json',dict(status='COMPLETE_RECORDS_PERSISTED',identity='VERIFIED_CURRENT_ARCHIVE',records=records,global_entries=len(infos),directory_logical_read_bytes=directory_bytes,global_unsafe_entries=unsafe))
   mapped=[x for x in selected if x is not None];cs=[x.compress_size for x in mapped];us=[x.file_size for x in mapped];missing=sum(x['matches']==0 for x in records);ambiguous=sum(x['matches']>1 for x in records);compressed=sum(cs);uncompressed=sum(us)
   summary=dict(planned_members=100,mapped_members=len(mapped),missing_members=missing,ambiguous_members=ambiguous,registered_records=100,complete_private_directory_saved=True,archive_identity='PASS_FRESH_HASH',global_entries=len(infos),directory_logical_read_bytes=directory_bytes,directory_limit_bytes=16*1024**2,entry_limit=4096,unsafe_entries=len(unsafe),compressed_min_bytes=min(cs) if cs else None,compressed_max_bytes=max(cs) if cs else None,compressed_total_bytes=compressed,uncompressed_min_bytes=min(us) if us else None,uncompressed_max_bytes=max(us) if us else None,uncompressed_total_bytes=uncompressed,old_32MiB_compressed_exceed_count=sum(x>32*1024**2 for x in cs),old_64MiB_uncompressed_exceed_count=sum(x>64*1024**2 for x in us),old_either_bound_exceed_count=sum(x.compress_size>32*1024**2 or x.file_size>64*1024**2 for x in mapped),compressed_limit_bytes=3*1024**3,uncompressed_limit_bytes=4*1024**3,measurement_round='068_NEW_DIRECTORY_NOT_RETROACTIVE_067')
   reasons=[]
   if directory_bytes>16*1024**2 or len(infos)>4096:reasons.append('ZIP_DIRECTORY_BUDGET')
   if unsafe:reasons.append('ZIP_GLOBAL_SAFETY')
   if missing or ambiguous:reasons.append('FIXED_MAPPING_INCOMPLETE')
   if compressed>3*1024**3:reasons.append('SELECTED_COMPRESSED_TOTAL_LIMIT')
   if uncompressed>4*1024**3:reasons.append('SELECTED_UNCOMPRESSED_TOTAL_LIMIT')
   summary.update(status='PASS' if not reasons else 'FAIL',reason_codes=reasons)
   save(root/'media-admission-summary.json',summary)
   require(root,not reasons,'MEDIA_ADMISSION_FAILED',summary,{'compressed':3*1024**3,'uncompressed':4*1024**3,'directory':16*1024**2,'entries':4096},completed=len(mapped),remaining=100-len(mapped))
   written=0
   for i,x in enumerate(selected):
    context('EXTRACT',completed=i,remaining=100-i,index=i,actual_compressed_total=compressed,limit_compressed_total=3*1024**3,actual_written_total=written,limit_uncompressed_total=4*1024**3)
    event(root/'media-ledger.jsonl',phase='EXTRACT',index=i,event='STARTED',expected_size=x.file_size,expected_compressed=x.compress_size);path=destination/f'{i}.mp4';h=hashlib.sha256();crc=n=0
    with z.open(x) as src,open(path,'xb') as dst:
     for block in iter(lambda:src.read(1024**2),b''):
      n+=len(block);written+=len(block);require(root,n<=x.file_size and written<=4*1024**3,'EXTRACT_SIZE_LIMIT',{'member':n,'total':written},{'member':x.file_size,'total':4*1024**3});crc=zlib.crc32(block,crc);h.update(block);dst.write(block)
    require(root,n==x.file_size and (crc&0xffffffff)==x.CRC,'EXTRACT_CRC_SIZE',{'size':n,'crc':crc&0xffffffff},{'size':x.file_size,'crc':x.CRC})
    entry=dict(name=names[i],path=str(path),bytes=n,sha256=h.hexdigest());entries.append(entry);event(root/'media-ledger.jsonl',phase='EXTRACT',index=i,event='CLOSED',bytes=n,crc=crc&0xffffffff)
    require(root,h.hexdigest() not in oldmedia,'INPUT_ALREADY_CONSUMED',{'old_media_collision':h.hexdigest() in oldmedia},False)
   save(root/'zip-io.json',dict(directory_logical_bytes=directory_bytes,total_zip_logical_bytes=measured.logical_read_bytes,selected_compressed_payload_bytes=compressed,extracted_bytes=written,physical_IO='UNKNOWN'))
 finally:measured.file.close()
 save(root/'media-manifest.json',entries)
 headers=[]
 for i,entry in enumerate(entries):
  context('CONTAINER_HEADERS',index=i,completed=i,remaining=100-i)
  with av.open(entry['path']) as f:
   s=f.streams.video[0];headers.append(dict(index=i,total_num_frames=s.frames if s.frames>0 else None,fps=float(s.average_rate) if s.average_rate else None,duration=float(s.duration*s.time_base) if s.duration is not None else None,time_base=str(s.time_base),base=float(s.start_time or 0)*float(s.time_base),width=s.width,height=s.height))
 save(root/'container-headers.json',headers)
 torch.set_num_threads(4);torch.set_num_interop_threads(1);proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
 for obj in (modeling_qwen3_vl,type(proc.video_processor)):
  path=Path(inspect.getfile(obj));require(root,digest(path)==a['runtime60']['installed_sources'][path.name],'NATIVE_IDENTITY',path.name,'original source digest')
 source=inspect.getsource(type(proc.video_processor)._preprocess);require(root,'permute(0, 1, 4, 7, 5, 8, 3, 2, 6, 9)' in source and 'temporal_patch_size' in source,'TUBELET_NATIVE_MAPPING','native source','time-major original tubelets')
 vsource=inspect.getsource(modeling_qwen3_vl.Qwen3VLVisionModel.forward);require(root,'merger' in vsource and 'grid_thw' in vsource,'MAIN_MERGER_NATIVE','native source','original main merger')
 records=[];total=0;pixelsknown={};oldledger={x['input_identity'] for x in check['ledger'] if x['mode']=='video_feature'}
 for i,entry in enumerate(entries):
  context('DECODE',index=i,completed=i,remaining=100-i,actual_frames=total,limit_frames=500000,outer_s=time.monotonic()-start,limit_outer_s=1800)
  event(root/'decode-ledger.jsonl',index=i,event='STARTED',input_sha256=entry['sha256'])
  with av.open(entry['path']) as f:
   s=f.streams.video[0];s.thread_count=1;meta0=headers[i];require(root,meta0['duration'] is not None and meta0['fps'] is not None,'CONTAINER_TIME_UNKNOWN',meta0,{'duration':'known','fps':'known'})
   base=meta0['base'];duration=meta0['duration'];fps=meta0['fps'];nf=meta0['total_num_frames'];targets=base+(np.arange(12)+.5)*duration/12
   best=[None]*12;dist=np.full(12,np.inf);indices=[None]*12;stamps=[None]*12;traversed=0
   for j,frame in enumerate(f.decode(s)):
    total+=1;traversed+=1;CONTEXT.update(actual_frames=total,member_traversed=traversed,outer_s=time.monotonic()-start)
    require(root,total<=500000 and time.monotonic()-start<1760,'DECODE_BUDGET',{'frames':total,'outer_s':time.monotonic()-start},{'frames':500000,'new_decode_deadline_s':1760,'outer_s':1800})
    if total%1000==0:(root/'decode-progress.json').write_text(json.dumps(CONTEXT))
    if frame.pts is None:continue
    stamp=float(frame.pts*s.time_base);delta=np.abs(targets-stamp);update=np.where(delta<dist)[0]
    if len(update):
     rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
     for k in update:best[k]=rgb;dist[k]=delta[k];indices[k]=j;stamps[k]=stamp
   require(root,all(x is not None for x in best) and len(set(indices))==12,'INSUFFICIENT_UNIQUE_TIMESTEPS',{'unique':len(set(indices)),'missing':sum(x is None for x in best),'traversed':traversed},12)
   clock=max(abs(t-base-j/fps) for t,j in zip(stamps,indices));require(root,fps>0 and clock<=1/fps,'FRAME_INDEX_CLOCK_NOT_CFR',{'max_error_s':clock,'fps':fps,'traversed':traversed},{'error_s':1/fps})
   array=np.stack(best);require(root,array.shape==(12,224,224,3) and array.dtype==np.uint8,'RGB_ARRAY_SHAPE',{'shape':list(array.shape),'dtype':str(array.dtype)},'[12,224,224,3]uint8')
   path=frames/f'{i}.npy'
   with open(path,'xb') as out:np.save(out,array,allow_pickle=False)
   rgbhash=digest(path);require(root,rgbhash not in oldrgb|oldledger,'INPUT_ALREADY_CONSUMED',{'old_RGB_or_ledger_collision':rgbhash in oldrgb|oldledger},False)
   meta=dict(total_num_frames=nf,fps=fps,duration=duration,width=224,height=224,frames_indices=indices);context('PROCESSOR',index=i,completed=i,remaining=100-i,actual_frames=total,limit_frames=500000)
   data=proc.video_processor(videos=[array],video_metadata=[VideoMetadata(**meta)],do_sample_frames=False,do_resize=False,return_tensors='pt')
   shape=list(data['pixel_values_videos'].shape);grid=data['video_grid_thw'].tolist();require(root,grid==[[6,14,14]] and shape==[1176,1536] and torch.isfinite(data['pixel_values_videos']).all(),'PROCESSOR_SHAPE_FINITE',{'grid':grid,'shape':shape,'finite':bool(torch.isfinite(data['pixel_values_videos']).all())},{'grid':[[6,14,14]],'shape':[1176,1536],'finite':True})
   data=dict(pixel_values_videos=data['pixel_values_videos'].to(torch.bfloat16),video_grid_thw=data['video_grid_thw']);pixelhash=hashbytes(data['pixel_values_videos'].view(torch.uint8).numpy().tobytes()+data['video_grid_thw'].numpy().tobytes());outpath=prepared/f'{i}.pt'
   with open(outpath,'xb') as out:torch.save(data,out)
   alias=pixelsknown.get(pixelhash);pixelsknown.setdefault(pixelhash,i)
   records.append(dict(index=i,name=entry['name'],rgb_sha256=rgbhash,pixels_sha256=pixelhash,path=str(outpath),prepared_file_sha256=digest(outpath),array_path=str(path),alias=alias,indices=indices,timestamps=stamps,targets=targets.tolist(),base=base,time_base=str(s.time_base),traversed=traversed,**meta))
  event(root/'decode-ledger.jsonl',index=i,event='CLOSED',frames_total=total,member_frames=traversed)
  if (i+1)%10==0:print('DECODE_PROCESSOR',i+1,'frames',total,flush=True)
 qs=[q for x in obs for q in x['questions']];tokens={};context('TOKENIZER',completed=0,remaining=100)
 for q in qs:
  b=proc.tokenizer(q,return_tensors='pt');length=int(b['attention_mask'].sum());require(root,length<=128,'QUESTION_TOKEN_LIMIT',length,128)
  tokens[q]=dict(tokens=length,identity=hashbytes(json.dumps({k:v.tolist() for k,v in b.items()},sort_keys=True).encode()))
 require(root,not torch.cuda.is_initialized(),'CPU_GPU_ISOLATION',torch.cuda.is_initialized(),False)
 save(root/'prepared-inputs.json',dict(records=records,questions=qs,tokens=tokens,decoded_frames=total,archive_hash_bytes=a['archive']['bytes'],compressed_bytes=compressed,uncompressed_bytes=uncompressed,outer_s=time.monotonic()-start,collisions=dict(old_media='NO_EXACT_MATCH',old_RGB='NO_EXACT_MATCH',old_logical_ledger='NO_EXACT_MATCH',old_pixels='UNKNOWN_NO_REGISTERED_SUMMARY',old_tokens='UNKNOWN_NO_REGISTERED_SUMMARY')))
 save(root/'input-seal.json',dict(status='CLOSED',observations_sha256=digest(root/'observations.json'),prepared_inputs_sha256=digest(root/'prepared-inputs.json'),media_manifest_sha256=digest(root/'media-manifest.json'),directory_sha256=digest(root/'selected-directory.json'),asset_checks_sha256=digest(root/'asset-checks.json')))
 print('MEDIA_INPUTS_CLOSED',100,len(qs),total,flush=True)

def gpu(root):
 import torch,gc
 from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
 sealed(root);context('GPU_INPUT_ADMISSION',completed=0,remaining=200);a=read(root/'asset-catalog.json');p=read(root/'prepared-inputs.json');start=read(root/'gpu-clock.json')['start_monotonic'];deadline=start+480
 seal=read(root/'input-seal.json');require(root,seal['status']=='CLOSED','INPUT_SEAL_STATE',seal['status'],'CLOSED')
 for key,name in [('observations_sha256','observations.json'),('prepared_inputs_sha256','prepared-inputs.json'),('media_manifest_sha256','media-manifest.json'),('directory_sha256','selected-directory.json'),('asset_checks_sha256','asset-checks.json')]:require(root,digest(root/name)==seal[key],'INPUT_SEAL_IDENTITY',name,'sealed digest')
 require(root,len(p['records'])==len(p['questions'])==100 and {x['name'] for x in p['records']}=={v for x in read(root/'observations.json') for v in x['videos']},'INPUT_KEYS',{'V':len(p['records']),'q':len(p['questions'])},100)
 for row in p['records']:require(root,digest(row['path'])==row['prepared_file_sha256'],'PREPARED_FILE_IDENTITY',row['index'],'sealed digest')
 features=root/'features';features.mkdir();calls=root/'model-calls';calls.mkdir();counts=dict(video_feature=0,text_feature=0,root_forward=0,visual_forward=0,decoder_forward=0,decoder_layer_forward=0);index=dict(video={},text={});model=None
 def hook(name):
  def inc(*args,**kwargs):counts[name]+=1
  return inc
 def call(mode,identity,fn):
  context('GPU_CALL',mode=mode,completed=counts['video_feature']+counts['text_feature'],remaining=200-counts['video_feature']-counts['text_feature'])
  require(root,time.monotonic()<deadline and counts[mode]<100 and counts['video_feature']+counts['text_feature']<200,'GPU_CALL_OR_TIME_LIMIT',{'elapsed_s':time.monotonic()-start,'counts':counts},{'new_call_s':480,'mode_calls':100,'total':200})
  key=hashbytes(json.dumps([mode,identity,a['runtime60']['model_config_sha256']],sort_keys=True).encode());claim=calls/(key+'.started');closed=calls/(key+'.closed');assert not claim.exists()
  save(claim,dict(status='STARTED',mode=mode,input_identity=identity));counts[mode]+=1
  try:
   tensor=fn();torch.cuda.synchronize();require(root,torch.isfinite(tensor).all() and torch.cuda.max_memory_allocated()<=16*1024**3,'GPU_FINITE_OR_ALLOCATED',{'finite':bool(torch.isfinite(tensor).all()),'peak_bytes':torch.cuda.max_memory_allocated()},{'finite':True,'peak_bytes':16*1024**3})
   path=features/(key+'.pt')
   with open(path,'xb') as f:torch.save(tensor,f)
   r=dict(path=str(path),sha256=digest(path),shape=list(tensor.shape));save(closed,dict(status='CLOSED',result=r));return r
  except Exception as e:save(calls/(key+'.failed'),dict(status='FAILED',reason=str(e)));raise
 try:
  save(root/'weight-load-started.json',dict(status='STARTED',at_unix=time.time()))
  model=Qwen3VLForConditionalGeneration.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to('cuda');model.eval();model.requires_grad_(False)
  model.register_forward_pre_hook(hook('root_forward'));model.model.visual.register_forward_pre_hook(hook('visual_forward'));model.model.language_model.register_forward_pre_hook(hook('decoder_forward'))
  for layer in model.model.language_model.layers:layer.register_forward_pre_hook(hook('decoder_layer_forward'))
  proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
  with torch.no_grad():
   for row in p['records']:
    if row['alias'] is not None:index['video'][row['name']]=dict(index['video'][p['records'][row['alias']]['name']],alias=True);continue
    def video(row=row):
     data=torch.load(row['path'],map_location='cpu',weights_only=True);out=model.get_video_features(**{k:v.to('cuda') for k,v in data.items()});main=out[0]
     require(root,isinstance(main,(tuple,list)) and len(main)==1,'VISUAL_RETURN_TYPE',{'type':str(type(main)),'length':len(main)},'tuple/list length1')
     require(root,main[0].shape==(294,2560),'VISUAL_AXIS_SHAPE',list(main[0].shape),[294,2560])
     return main[0].reshape(6,49,2560).mean(1).float().cpu()
    index['video'][row['name']]=call('video_feature',row['rgb_sha256'],video)
    if counts['video_feature']%20==0:print('V_CLOSED',counts['video_feature'],flush=True)
   for q in p['questions']:
    def text(q=q):
     b=proc.tokenizer(q,return_tensors='pt').to('cuda');o=model.model(**b,use_cache=False,return_dict=True);t=o.last_hidden_state[0,int(b['attention_mask'].sum())-1].float().cpu();require(root,t.shape==(2560,),'TEXT_FEATURE_SHAPE',list(t.shape),[2560]);return t
    index['text'][q]=call('text_feature',q,text)
    if counts['text_feature']%20==0:print('Q_CLOSED',counts['text_feature'],flush=True)
  assert len(index['video'])==len(index['text'])==100 and all(not p.requires_grad and p.grad is None for p in model.parameters())
  save(root/'feature-index.json',index);save(root/'feature-seal.json',dict(status='CLOSED',index_sha256=digest(root/'feature-index.json'),counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),loads=1,b0=0,backward=0,optimizer=0))
 finally:
  save(root/'gpu-counts.json',dict(counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),outer_s=time.monotonic()-start))
  del model;gc.collect()
  if torch.cuda.is_initialized():torch.cuda.empty_cache();torch.cuda.synchronize()

def predict(root):
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);sealed(root);assert read(root/'gpu-job.json')['active']==0 and read(root/'gpu-job.json')['exit_code']==0
 context('CPU_PREDICTION_ADMISSION',completed=0,remaining=2400);a=read(root/'asset-catalog.json');obs=read(root/'observations.json');index=read(root/'feature-index.json');used=0;states=0
 fs=read(root/'feature-seal.json');require(root,fs['status']=='CLOSED' and digest(root/'feature-index.json')==fs['index_sha256'],'FEATURE_INDEX_SEAL',{'status':fs['status'],'digest_matched':digest(root/'feature-index.json')==fs['index_sha256']},'CLOSED matched index')
 require(root,set(index['video'])=={v for x in obs for v in x['videos']} and set(index['text'])=={q for x in obs for q in x['questions']},'FEATURE_KEYS',{'V':len(index['video']),'q':len(index['text'])},100)
 def load(p,expected=None,kind='feature'):
  nonlocal used,states
  b=Path(p).read_bytes()
  if kind=='feature':used+=len(b);assert used<=48*1024**2
  else:states+=len(b);assert states<=24*1024**2
  if expected:require(root,hashbytes(b)==expected,'TENSOR_IDENTITY',{'kind':kind,'bytes':len(b)},'sealed digest')
  return torch.load(io.BytesIO(b),map_location='cpu',weights_only=True)
 V={q:load(r['path'],r['sha256']) for q,r in index['video'].items()};Q={q:load(r['path'],r['sha256']) for q,r in index['text'].items()};stats=load(a['normalizer']['path'],a['normalizer']['expected_sha256'],'state');views={}
 require(root,all(t.shape==(6,2560) and t.dtype==torch.float32 and torch.isfinite(t).all() for t in V.values()) and all(t.shape==(2560,) and t.dtype==torch.float32 and torch.isfinite(t).all() for t in Q.values()),'FEATURE_TENSORS',{'V_count':len(V),'q_count':len(Q)},{'V_shape':[6,2560],'q_shape':[2560],'dtype':'float32','finite':True})
 for arm in ('C_CENTER','D_ROLE'):
  views[arm]={q:(((v.double() if arm=='C_CENTER' else (v.double()-Q[tau(q)].double())/2)-stats[arm]['mu'])/stats[arm]['scale']).float() for q,v in Q.items()}
 with open(root/'views.pt','xb') as f:torch.save(views,f)
 head=helper('head056',Path(__file__).with_name('question_temporal_056.py'));outputs=[];forward=0
 for item in a['heads']:
  model=head.TemporalHead(2560,2560);model.load_state_dict(load(item['path'],item['expected_sha256'],'state'));model.eval();model.requires_grad_(False);arm='C_CENTER' if item['method']=='C_NATIVE' else 'D_ROLE'
  with torch.no_grad():
   for row in obs:
    for vi,v in enumerate(row['videos']):
     for qi,q in enumerate(row['questions']):
      key=[item['method'],item['seed'],row['index'],vi,qi];context('CPU_HEAD_FORWARD',completed=forward,remaining=2400-forward,key=key);event(root/'prediction-ledger.jsonl',event='STARTED',key=key)
      z=model(V[v].unsqueeze(0),views[arm][q].unsqueeze(0));assert z.numel()==1 and torch.isfinite(z).all();pred=int(z.item()>0);forward+=1
      outputs.append(dict(method=item['method'],seed=item['seed'],index=row['index'],video=vi,question=qi,prediction=pred,status='CLOSED'));event(root/'prediction-ledger.jsonl',event='CLOSED',key=key)
  assert all(not p.requires_grad and p.grad is None for p in model.parameters());print('HEAD_CLOSED',item['method'],item['seed'],flush=True)
 assert forward==2400 and not torch.cuda.is_initialized();save(root/'outputs.json',outputs)
 save(root/'prediction-seal.json',dict(status='CLOSED',outputs_sha256=digest(root/'outputs.json'),views_sha256=digest(root/'views.pt'),forward=forward,feature_read_bytes=used,old_state_read_bytes=states,backward=0,optimizer=0))

def intervals(hist,pairs):
 import random
 def qt(a,p):
  a=sorted(a);x=(len(a)-1)*p;i=int(x);return a[i]*(1-(x-i))+a[min(i+1,len(a)-1)]*(x-i)
 draws=list();rng=random.Random(55066)
 for _ in range(10000):draws.append(rng.choices(range(50),k=50))
 rng=random.Random(55067);sd=[rng.choices(range(6),k=6) for _ in range(10000)];rows=[]
 for metric,key in (('four_way','net'),('question_invariant','invariant_net')):
  vector=[x for x in range(-6,7) for _ in range(next(r['count'] for r in hist if r['metric']==metric and r['seed_sum']==x))];assert len(vector)==50
  seed=[x[key] for x in pairs];point=100*sum(seed)/300
  for axis,values in [('paired_unit',[100*sum(vector[j] for j in d)/300 for d in draws]),('seed',[sum(2*seed[j] for j in d)/6 for d in sd])]:rows.append(dict(metric=metric,axis=axis,point_pp=point,lower_pp=qt(values,.025),upper_pp=qt(values,.975),draws=10000,planned_draws=10000,status='CLOSED'))
 return rows

def score(root):
 from collections import Counter
 sealed(root);assert read(root/'prediction-job.json')['active']==0 and read(root/'prediction-job.json')['exit_code']==0;seal=read(root/'prediction-seal.json');assert seal['outputs_sha256']==digest(root/'outputs.json')
 context('SCORING_ADMISSION',completed=0,remaining=2400);preoutputs=read(root/'outputs.json');expected={(m,s,i,v,q) for m in METHODS for s in SEEDS for i in range(50) for v in range(2) for q in range(2)};keys={(x['method'],x['seed'],x['index'],x['video'],x['question']) for x in preoutputs}
 require(root,keys==expected and len(preoutputs)==2400 and all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) for x in preoutputs),'OUTPUT_KEYS_STATE',{'rows':len(preoutputs),'keys':len(keys),'missing':len(expected-keys),'extra':len(keys-expected)},2400)
 a=read(root/'asset-catalog.json');identity=a['raw_DyBench_identity'];path=Path(a['prior066'])/'dy.body';assert digest(path)==identity['sha256'];raw=read(path);obs=read(root/'observations.json');labels=[]
 # Native publisher choices refer to event1/event2, not the filenames' order.
 for row,positions in zip(obs,a['selected_positions']):
  members=[raw[i] for i in positions];mapping={x['video']:x for x in members};cell=[]
  for name in row['videos']:
   x=mapping[name];assert x['candidates']==['First action 1, then action 2','First action 2, then action 1'];y=int(x['answer']=='First action 1, then action 2');assert x['answer'] in x['candidates'];cell.append([y,1-y])
  assert cell[0][0]==cell[1][1] and cell[0][1]==cell[1][0];labels.append(cell)
 save(root/'scoring-labels.json',labels);outputs=read(root/'outputs.json');lookup={(x['method'],x['seed'],x['index'],x['video'],x['question']):x for x in outputs};assert len(lookup)==2400
 conditions=[];detail={}
 for seed in SEEDS:
  for method in METHODS:
   cnt=Counter();ds=[]
   for i,y in enumerate(labels):
    pred=[]
    for v in range(2):
     for q in range(2):
      x=lookup[method,seed,i,v,q];assert x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1);pred.append(x['prediction'])
    correct=[pred[2*v+q]==y[v][q] for v in range(2) for q in range(2)];k=sum(correct);inv=pred[0]==pred[1] and pred[2]==pred[3];videoonly=inv and pred[0]!=pred[2];questiononly=pred[0]==pred[2] and pred[1]==pred[3] and pred[0]!=pred[1];constant=len(set(pred))==1;checker=pred[0]==pred[3] and pred[1]==pred[2] and pred[0]!=pred[1]
    pattern='CONSTANT' if constant else 'VIDEO_ONLY' if videoonly else 'QUESTION_ONLY' if questiononly else 'CHECKERBOARD' if checker else 'MIXED'
    cnt['correct_cells']+=k;cnt['video_pair_correct']+=int(correct[0] and correct[2])+int(correct[1] and correct[3]);cnt['question_pair_correct']+=int(correct[0] and correct[1])+int(correct[2] and correct[3]);cnt['four_way_correct']+=k==4;cnt['question_invariant']+=inv;cnt[f'K{k}']+=1;cnt[pattern]+=1;ds.append(dict(four=int(k==4),inv=int(inv)))
   c=dict(method=method,seed=seed,status='CLOSED',planned_items=50,planned_cells=200,new_cells=200,cached_cells=0,CLOSED=200,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown_cells=0,scoring_unknown_cells=0,**{k:cnt[k] for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4','CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')});c.update(cell_accuracy_pct=cnt['correct_cells']/2,video_pair_accuracy_pct=cnt['video_pair_correct'],question_pair_accuracy_pct=cnt['question_pair_correct'],four_way_accuracy_pct=cnt['four_way_correct']*2,question_invariant_pct=cnt['question_invariant']*2);conditions.append(c);detail[method,seed]=ds
 pairs=[]
 for seed in SEEDS:
  left=detail['D_NATIVE',seed];right=detail['C_NATIVE',seed];lo=sum(l['four'] and not r['four'] for l,r in zip(left,right));ro=sum(r['four'] and not l['four'] for l,r in zip(left,right));net=lo-ro;iv=sum(l['inv']-r['inv'] for l,r in zip(left,right));pairs.append(dict(seed=seed,left='D_NATIVE',right='C_NATIVE',planned_items=50,evaluated_items=50,status='CLOSED',left_only=lo,right_only=ro,both_correct=sum(l['four'] and r['four'] for l,r in zip(left,right)),both_wrong=sum(not l['four'] and not r['four'] for l,r in zip(left,right)),unknown=0,net=net,delta_four_way_pp=2*net,invariant_net=iv,question_invariant_delta_pp=2*iv))
 hist=[]
 for metric,key in (('four_way','four'),('question_invariant','inv')):
  counts=Counter(sum(detail['D_NATIVE',s][i][key]-detail['C_NATIVE',s][i][key] for s in SEEDS) for i in range(50))
  hist.extend(dict(metric=metric,seed_sum=k,count=counts[k],status='CLOSED') for k in range(-6,7))
 means=intervals(hist,pairs);save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,histogram=hist,intervals=means,conclusion='POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE' if sum(p['net'] for p in pairs)>0 else 'NO_POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE'))
 print('SCORED',[(p['seed'],p['net']) for p in pairs],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('role',choices=('assets','media','gpu','predict','score'));p.add_argument('--root',required=True);args=p.parse_args();r=Path(args.root)
 try:
  globals()[args.role](r)
 except Exception as e:
  event(r/'stops.jsonl',role=args.role,event='STOP',reason_code=str(e) or type(e).__name__,type=type(e).__name__,actual=dict(CONTEXT),limit='Sealed phase and stage limits',stage=CONTEXT.get('stage',args.role));raise
