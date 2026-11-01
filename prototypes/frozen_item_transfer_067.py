"""067 bounded frozen item transfer. No import-time data/model operations."""
import argparse,ast,hashlib,io,json,os,re,time
from pathlib import Path
SEEDS=(137,263,419,557,733,911)
METHODS=('C_NATIVE','D_NATIVE')
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def hashbytes(b):return hashlib.sha256(b).hexdigest()
def tau(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 if not m:raise ValueError('QUESTION_PARSE')
 return f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.'
def catalog(root,prior066,prior063):
 root=Path(root);raw={};objects={};records=[];used=0
 def meta(path):
  nonlocal used
  path=Path(path).resolve();key=str(path)
  if key not in raw:
   assert path.suffix in ('.json','.jsonl','.py') and not any(s in path.name for s in ('labels','all-outputs','new-outputs','prediction.jsonl','steps.jsonl','data-bindings','plan-')),'FORBIDDEN_OLD_CONTENT'
   n=path.stat().st_size;assert used+n<=32*1024**2;data=path.read_bytes();used+=len(data);raw[key]=data;records.append(dict(path=key,bytes=len(data),sha256=hashbytes(data),kind='OLD_METADATA'))
   (root/'catalog-progress.json').write_text(json.dumps(dict(bytes=used,files=records)),encoding='utf-8')
   print('META',path.name,'bytes',n,flush=True)
  if key not in objects:objects[key]=json.loads(raw[key].decode('utf-8-sig'))
  return objects[key]
 p66=Path(prior066);p63=Path(prior063);c66=meta(p66/'parent-closed.json')
 if c66['push']!='SUCCEEDED':assert meta(p66/'push-retry-1.json')['push']=='SUCCEEDED'
 assert meta(p63/'parent-closed.json')['push']=='SUCCEEDED'
 a=meta(p66/'admission-private.json');seal66=meta(p66/'admission-seal.json');assert hashbytes(raw[str((p66/'admission-private.json').resolve())])==seal66['admission_sha256']
 acquired=meta(p66/'acquisition-closed.json');projected=meta(p66/'dy-observations.json');assert hashbytes(raw[str((p66/'dy-observations.json').resolve())])==next(x['sha256'] for x in acquired['projection_files'] if x['name']=='dy-observations.json')
 assert meta(p66/'publisher-structure.json')['results']['DyBench']['selected']['publisher_four_cell_consistent']==50
 meta(p66/'pre-read-rule-code-seal.json');meta(p66/'pre-details-code-seal.json');meta(p66/'independent-review.json')
 selected=a['selected'];assert len(selected)==50 and all(x['category']=='VIDHALLUC' for x in selected)
 obs=[dict(index=i,videos=x['videos'],questions=x['questions']) for i,x in enumerate(selected)]
 assert len({v for x in obs for v in x['videos']})==len({q for x in obs for q in x['questions']})==100
 assert all(tau(x['questions'][0])==x['questions'][1] and tau(x['questions'][1])==x['questions'][0] for x in obs)
 old63=meta(p63/'old-assets.json');p62=Path(old63['prior062']);p60=Path(old63['prior060']);meta(p63/'input-seal.json');out63=meta(p63/'output-seal.json');code63=meta(p63/'code-seal.json')
 for p in (p62,p60):assert meta(p/'parent-closed.json')['push']=='SUCCEEDED'
 old62=meta(p62/'old-assets.json');out62=meta(p62/'output-seal.json');meta(p62/'input-seal.json');prior60=meta(p60/'prior-assets.json');p57=Path(prior60['prior057']);assert meta(p57/'parent-closed.json')['push']=='SUCCEEDED'
 pre60=meta(p60/'pre-consumption-seal.json');meta(p60/'outputs-identity-seal.json');rt60=meta(p60/'runtime-input-seal.json');rt57=meta(p57/'runtime-input-seal.json');plan57=meta(p57/'media-plan.json')
 media60=meta(p60/'media-manifest.json');cache60=meta(p60/'cache-manifest.json');media57=meta(p57/'media-manifest.json');cache57=meta(p57/'cache-manifest.json')
 heads=[];expected63={str(Path(x['path']).resolve()):x['sha256'] for x in out63['files']};expected62={str(Path(x['path']).resolve()):x['sha256'] for x in out62['files']}
 for seed in SEEDS:
  for method in METHODS:
   path=p63/'training'/f'{method}-{seed}'/'final.pt';expected=expected63[str(path.resolve())];assert path.is_file();heads.append(dict(seed=seed,method=method,path=str(path),expected_sha256=expected,bytes=path.stat().st_size))
 normalizer=p62/'normalizer.pt';assert str(normalizer.resolve()) in expected62
 assert rt60['model_file_sha256']==rt57['model_file_sha256']
 archive=p57/'event_sequence_zip.body';assert archive.is_file() and archive.stat().st_size==2783546023
 assert plan57['size']==2783546023 and len(plan57['publisher_content_sha256'])==64
 save(root/'observations.json',obs)
 save(root/'asset-catalog.json',dict(prior066=str(p66),prior063=str(p63),prior062=str(p62),prior060=str(p60),prior057=str(p57),heads=heads,normalizer=dict(path=str(normalizer),expected_sha256=expected62[str(normalizer.resolve())]),archive=dict(path=str(archive),bytes=2783546023,expected_sha256=plan57['publisher_content_sha256']),model_root=rt60['model_root'],model_file_sha256=rt60['model_file_sha256'],runtime60=rt60,runtime57=rt57,old_media_records=media60+media57,old_cache_records=[cache60,cache57],metadata_files=records,old_metadata_logical_bytes=used,raw_DyBench_identity=next(x for x in acquired['files'] if x['name']=='dy.body'),selected_positions=[x['positions'] for x in selected],source_key_level='TWO_VIDEO_INSTANCE_ONLY'))
 save(root/'old-metadata-access.json',dict(bytes=used,files=records))
 save(root/'catalog-schema.json',dict(pre60_keys=list(pre60),old62_keys=list(old62),rt57_keys=list(rt57),code63_files=[x['path'] for x in code63['files']],pre60_code_entries={k:v for k,v in pre60.items() if 'code' in k or 'model' in k or 'lock' in k or 'ledger' in k},pre60_python_entries=[x for x in pre60.get('files',[]) if str(x.get('path','')).endswith('.py')]))
 print('CATALOG_CLOSED','HEADS',len(heads),'META_BYTES',used,flush=True)
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
 sealed(root);a=read(root/'asset-catalog.json');used=0;checks=[]
 for item in a['heads']+[a['normalizer']]:
  data=Path(item['path']).read_bytes();used+=len(data);assert used<=32*1024**2
  assert hashbytes(data)==item['expected_sha256'],'OLD_STATE_IDENTITY'
  state=torch.load(io.BytesIO(data),map_location='cpu',weights_only=True)
  if 'seed' in item:
   h=helper('head056',Path(__file__).with_name('question_temporal_056.py')).TemporalHead(2560,2560);h.load_state_dict(state,strict=True)
   assert sum(p.numel() for p in h.parameters())==356673
   assert all(torch.isfinite(v).all() and v.dtype==torch.float32 for v in state.values())
  else:
   for arm in ('C_CENTER','D_ROLE'):
    s=state[arm];assert s['mu'].shape==(2560,) and s['mu'].dtype==torch.float64 and s['scale'].ndim==0 and s['scale'].dtype==torch.float64 and torch.isfinite(s['mu']).all() and torch.isfinite(s['scale']) and s['scale']>1e-8
  checks.append(dict(path=item['path'],sha256=hashbytes(data),bytes=len(data)))
 hashes={};weightbytes=0
 for name,expected in a['model_file_sha256'].items():
  p=Path(a['model_root'])/name
  if name.endswith('.safetensors'):weightbytes+=p.stat().st_size
  assert weightbytes<=12*1024**3
  hashes[name]=digest(p);assert hashes[name]==expected,'MODEL_IDENTITY'
 for name,expected in a['runtime60']['installed_sources'].items():
  p=Path(sys.prefix)/'Lib/site-packages/transformers/models/qwen3_vl'/name;assert digest(p)==expected,'NATIVE_IDENTITY'
 oldmeta=0;ledger=[]
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
 save(root/'asset-checks.json',dict(status='CLOSED',state_logical_bytes=used,state_checks=checks,weight_hash_bytes=weightbytes,model_hashes=hashes,ledger_logical_bytes=oldmeta,ledger=ledger,cuda_initialized=False))
 print('ASSETS_CLOSED',len(checks),weightbytes,flush=True)

def media(root):
 """One archive hash, selected CRC extraction and one linear decode per video."""
 import zipfile,stat,zlib,av,numpy as np,torch,inspect
 from collections import defaultdict
 from transformers import AutoProcessor
 from transformers.video_utils import VideoMetadata
 from transformers.models.qwen3_vl import modeling_qwen3_vl
 start=time.monotonic();sealed(root);a=read(root/'asset-catalog.json');check=read(root/'asset-checks.json');obs=read(root/'observations.json')
 event(root/'media-ledger.jsonl',phase='ARCHIVE_HASH',event='STARTED',bytes=a['archive']['bytes'])
 assert digest(a['archive']['path'])==a['archive']['expected_sha256'],'STOP_ARCHIVE_IDENTITY'
 event(root/'media-ledger.jsonl',phase='ARCHIVE_HASH',event='CLOSED',bytes=a['archive']['bytes'])
 names=[v for x in obs for v in x['videos']];assert len(names)==len(set(names))==100
 destination=root/'media';destination.mkdir();frames=root/'frames';frames.mkdir();prepared=root/'prepared';prepared.mkdir()
 entries=[];compressed=uncompressed=0
 oldmedia={x['sha256'] for x in a['old_media_records']};oldrgb={x['sha256'] for m in a['old_cache_records'] for x in m['records'].values()}
 with zipfile.ZipFile(a['archive']['path']) as z:
  assert z.start_dir>=0 and Path(a['archive']['path']).stat().st_size-z.start_dir<=16*1024**2
  infos=z.infolist();assert len(infos)<=4096;seen=set();bybase=defaultdict(list)
  for x in infos:
   p=Path(x.filename);parts=x.filename.replace('\\','/').split('/')
   assert not p.is_absolute() and not re.match(r'^[A-Za-z]:',x.filename) and '..' not in parts and not (x.flag_bits&1) and not stat.S_ISLNK(x.external_attr>>16) and x.filename not in seen,'UNSAFE_ZIP'
   assert x.file_size/max(1,x.compress_size)<=100,'ZIP_RATIO';seen.add(x.filename);bybase[p.name].append(x)
  selected=[]
  for name in names:
   assert len(bybase[name])==1,'MEMBER_MAP';x=bybase[name][0]
   assert x.compress_size<=32*1024**2 and x.file_size<=64*1024**2
   compressed+=x.compress_size;uncompressed+=x.file_size;selected.append(x)
  assert compressed<=512*1024**2 and uncompressed<=1024**3
  save(root/'selected-directory.json',dict(entries=[dict(name=x.filename,size=x.file_size,compressed=x.compress_size,crc=x.CRC) for x in selected],compressed=compressed,uncompressed=uncompressed))
  for i,x in enumerate(selected):
   event(root/'media-ledger.jsonl',phase='EXTRACT',index=i,event='STARTED');path=destination/f'{i}.mp4';h=hashlib.sha256();crc=n=0
   with z.open(x) as src,open(path,'xb') as dst:
    for block in iter(lambda:src.read(1024**2),b''):
     n+=len(block);assert n<=x.file_size;crc=zlib.crc32(block,crc);h.update(block);dst.write(block)
   assert n==x.file_size and (crc&0xffffffff)==x.CRC
   entry=dict(name=names[i],path=str(path),bytes=n,sha256=h.hexdigest());entries.append(entry)
   event(root/'media-ledger.jsonl',phase='EXTRACT',index=i,event='CLOSED',bytes=n)
   assert h.hexdigest() not in oldmedia,'INPUT_ALREADY_CONSUMED'
 save(root/'media-manifest.json',entries)
 torch.set_num_threads(4);torch.set_num_interop_threads(1);proc=AutoProcessor.from_pretrained(a['model_root'],local_files_only=True,trust_remote_code=False)
 for obj in (modeling_qwen3_vl,type(proc.video_processor)):
  p=Path(inspect.getfile(obj));assert digest(p)==a['runtime60']['installed_sources'][p.name]
 source=inspect.getsource(type(proc.video_processor)._preprocess)
 assert 'permute(0, 1, 4, 7, 5, 8, 3, 2, 6, 9)' in source and 'temporal_patch_size' in source
 vsource=inspect.getsource(modeling_qwen3_vl.Qwen3VLVisionModel.forward)
 assert 'merger' in vsource and 'grid_thw' in vsource
 records=[];total=0;rgbknown={};pixelsknown={};oldpixels={x.get('prepared_sha256') for x in a['old_cache_records']};oldledger={x['input_identity'] for x in check['ledger'] if x['mode']=='video_feature'}
 for i,entry in enumerate(entries):
  event(root/'decode-ledger.jsonl',index=i,event='STARTED',input_sha256=entry['sha256'])
  with av.open(entry['path']) as f:
   s=f.streams.video[0];s.thread_count=1;assert s.duration is not None
   base=float(s.start_time or 0)*float(s.time_base);duration=float(s.duration*s.time_base);fps=float(s.average_rate);nf=s.frames;targets=base+(np.arange(12)+.5)*duration/12
   best=[None]*12;dist=np.full(12,np.inf);indices=[None]*12;stamps=[None]*12;traversed=0
   for j,frame in enumerate(f.decode(s)):
    total+=1;traversed+=1;assert total<=200000 and time.monotonic()-start<870,'DECODE_BUDGET'
    if frame.pts is None:continue
    stamp=float(frame.pts*s.time_base);delta=np.abs(targets-stamp);update=np.where(delta<dist)[0]
    if len(update):
     rgb=frame.reformat(width=224,height=224,format='rgb24').to_ndarray()
     for k in update:best[k]=rgb;dist[k]=delta[k];indices[k]=j;stamps[k]=stamp
   assert all(x is not None for x in best) and len(set(indices))==12
   assert fps>0 and max(abs(t-base-j/fps) for t,j in zip(stamps,indices))<=1/fps,'FRAME_INDEX_CLOCK_NOT_CFR'
   array=np.stack(best);assert array.shape==(12,224,224,3) and array.dtype==np.uint8
   path=frames/f'{i}.npy'
   with open(path,'xb') as out:np.save(out,array,allow_pickle=False)
   rgbhash=digest(path);assert rgbhash not in oldrgb|oldledger,'INPUT_ALREADY_CONSUMED'
   meta=dict(total_num_frames=nf,fps=fps,duration=duration,width=224,height=224,frames_indices=indices)
   data=proc.video_processor(videos=[array],video_metadata=[VideoMetadata(**meta)],do_sample_frames=False,do_resize=False,return_tensors='pt')
   assert data['video_grid_thw'].tolist()==[[6,14,14]] and data['pixel_values_videos'].shape==(1176,1536) and torch.isfinite(data['pixel_values_videos']).all()
   data=dict(pixel_values_videos=data['pixel_values_videos'].to(torch.bfloat16),video_grid_thw=data['video_grid_thw'])
   pixelhash=hashbytes(data['pixel_values_videos'].view(torch.uint8).numpy().tobytes()+data['video_grid_thw'].numpy().tobytes())
   outpath=prepared/f'{i}.pt'
   with open(outpath,'xb') as out:torch.save(data,out)
   alias=pixelsknown.get(pixelhash);pixelsknown.setdefault(pixelhash,i)
   records.append(dict(index=i,name=entry['name'],rgb_sha256=rgbhash,pixels_sha256=pixelhash,path=str(outpath),array_path=str(path),alias=alias,indices=indices,timestamps=stamps,targets=targets.tolist(),base=base,time_base=str(s.time_base),traversed=traversed,**meta))
  event(root/'decode-ledger.jsonl',index=i,event='CLOSED',frames_total=total)
  if (i+1)%10==0:print('DECODE_PROCESSOR',i+1,'frames',total,flush=True)
 qs=[q for x in obs for q in x['questions']];tokens={}
 for q in qs:
  b=proc.tokenizer(q,return_tensors='pt');assert int(b['attention_mask'].sum())<=128
  tokens[q]=dict(tokens=int(b['attention_mask'].sum()),identity=hashbytes(json.dumps({k:v.tolist() for k,v in b.items()},sort_keys=True).encode()))
 assert not torch.cuda.is_initialized()
 save(root/'prepared-inputs.json',dict(records=records,questions=qs,tokens=tokens,decoded_frames=total,archive_hash_bytes=a['archive']['bytes'],compressed_bytes=compressed,uncompressed_bytes=uncompressed,outer_s=time.monotonic()-start))
 print('MEDIA_INPUTS_CLOSED',100,len(qs),total,flush=True)

def gpu(root):
 import torch,gc
 from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
 sealed(root);a=read(root/'asset-catalog.json');p=read(root/'prepared-inputs.json');start=read(root/'gpu-clock.json')['start_monotonic'];deadline=start+480
 features=root/'features';features.mkdir();calls=root/'model-calls';calls.mkdir();counts=dict(video_feature=0,text_feature=0,root_forward=0,visual_forward=0,decoder_forward=0,decoder_layer_forward=0);index=dict(video={},text={});model=None
 def hook(name):
  def inc(*args,**kwargs):counts[name]+=1
  return inc
 def call(mode,identity,fn):
  assert time.monotonic()<deadline and counts[mode]<100 and counts['video_feature']+counts['text_feature']<200,'GPU_CALL_OR_TIME_LIMIT'
  key=hashbytes(json.dumps([mode,identity,a['runtime60']['model_config_sha256']],sort_keys=True).encode());claim=calls/(key+'.started');closed=calls/(key+'.closed');assert not claim.exists()
  save(claim,dict(status='STARTED',mode=mode,input_identity=identity));counts[mode]+=1
  try:
   tensor=fn();torch.cuda.synchronize();assert torch.isfinite(tensor).all() and torch.cuda.max_memory_allocated()<=16*1024**3
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
     assert isinstance(main,(tuple,list)) and len(main)==1 and main[0].shape==(294,2560)
     return main[0].reshape(6,49,2560).mean(1).float().cpu()
    index['video'][row['name']]=call('video_feature',row['rgb_sha256'],video)
    if counts['video_feature']%20==0:print('V_CLOSED',counts['video_feature'],flush=True)
   for q in p['questions']:
    def text(q=q):
     b=proc.tokenizer(q,return_tensors='pt').to('cuda');o=model.model(**b,use_cache=False,return_dict=True);t=o.last_hidden_state[0,int(b['attention_mask'].sum())-1].float().cpu();assert t.shape==(2560,);return t
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
 a=read(root/'asset-catalog.json');obs=read(root/'observations.json');index=read(root/'feature-index.json');used=0;states=0
 def load(p,expected=None,kind='feature'):
  nonlocal used,states
  b=Path(p).read_bytes()
  if kind=='feature':used+=len(b);assert used<=48*1024**2
  else:states+=len(b);assert states<=24*1024**2
  if expected:assert hashbytes(b)==expected
  return torch.load(io.BytesIO(b),map_location='cpu',weights_only=True)
 V={q:load(r['path'],r['sha256']) for q,r in index['video'].items()};Q={q:load(r['path'],r['sha256']) for q,r in index['text'].items()};stats=load(a['normalizer']['path'],a['normalizer']['expected_sha256'],'state');views={}
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
      key=[item['method'],item['seed'],row['index'],vi,qi];event(root/'prediction-ledger.jsonl',event='STARTED',key=key)
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
  for axis,values in [('paired_unit',[100*sum(vector[j] for j in d)/300 for d in draws]),('seed',[sum(2*seed[j] for j in d)/6 for d in sd])]:rows.append(dict(metric=metric,axis=axis,point_pp=point,lower_pp=qt(values,.025),upper_pp=qt(values,.975),draws=10000,status='CLOSED'))
 return rows

def score(root):
 from collections import Counter
 sealed(root);assert read(root/'prediction-job.json')['active']==0 and read(root/'prediction-job.json')['exit_code']==0;seal=read(root/'prediction-seal.json');assert seal['outputs_sha256']==digest(root/'outputs.json')
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
   c=dict(method=method,seed=seed,status='CLOSED',planned_items=50,planned_cells=200,new_cells=200,cached_cells=0,CLOSED=200,INVALID=0,FAILED=0,NOT_RUN=0,unknown=0,**{k:cnt[k] for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4','CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')});c.update(cell_accuracy_pct=cnt['correct_cells']/2,video_pair_accuracy_pct=cnt['video_pair_correct'],question_pair_accuracy_pct=cnt['question_pair_correct'],four_way_accuracy_pct=cnt['four_way_correct']*2,question_invariant_pct=cnt['question_invariant']*2);conditions.append(c);detail[method,seed]=ds
 pairs=[]
 for seed in SEEDS:
  left=detail['D_NATIVE',seed];right=detail['C_NATIVE',seed];lo=sum(l['four'] and not r['four'] for l,r in zip(left,right));ro=sum(r['four'] and not l['four'] for l,r in zip(left,right));net=lo-ro;iv=sum(l['inv']-r['inv'] for l,r in zip(left,right));pairs.append(dict(seed=seed,left='D_NATIVE',right='C_NATIVE',planned_items=50,status='CLOSED',left_only=lo,right_only=ro,both_correct=sum(l['four'] and r['four'] for l,r in zip(left,right)),both_wrong=sum(not l['four'] and not r['four'] for l,r in zip(left,right)),unknown=0,net=net,delta_four_way_pp=2*net,invariant_net=iv,question_invariant_delta_pp=2*iv))
 hist=[]
 for metric,key in (('four_way','four'),('question_invariant','inv')):
  counts=Counter(sum(detail['D_NATIVE',s][i][key]-detail['C_NATIVE',s][i][key] for s in SEEDS) for i in range(50))
  hist.extend(dict(metric=metric,seed_sum=k,count=counts[k],status='CLOSED') for k in range(-6,7))
 means=intervals(hist,pairs);save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,histogram=hist,intervals=means,conclusion='POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE' if sum(p['net'] for p in pairs)>0 else 'NO_POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE'))
 print('SCORED',[(p['seed'],p['net']) for p in pairs],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('role',choices=('catalog','assets','media','gpu','predict','score'));p.add_argument('--root',required=True);p.add_argument('--prior066');p.add_argument('--prior063');args=p.parse_args();r=Path(args.root)
 try:
  if args.role=='catalog':catalog(r,args.prior066,args.prior063)
  else:globals()[args.role](r)
 except Exception as e:
  event(r/'stops.jsonl',role=args.role,event='STOP',reason=str(e),type=type(e).__name__);raise
