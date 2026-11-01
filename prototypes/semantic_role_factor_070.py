"""070 explicit CPU roles; importing performs no research I/O or model work."""
import argparse,collections,hashlib,importlib.util,io,json,math,os,random,re,time
from pathlib import Path
SEEDS=(137,263,419,557,733,911)
ARMS=('CONCAT','FACTOR','REVERSE','ANCHOR')
METHODS=('C_CACHED','D_CACHED')+ARMS
SPLITS=('train_pool68','validation11','development54','source_holdout50','item_transfer50')
NS=(68,11,54,50,50)
MAINS=SPLITS[3:]
RIGHTS=('C_CACHED','D_CACHED','CONCAT','REVERSE','ANCHOR')
CONTEXT={}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(dict(at_unix=time.time(),**x),ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def require(root,ok,code,actual,limit):
 if not ok:
  event(root/'failures.jsonl',reason_code=code,actual=actual,limit=limit,context=dict(CONTEXT));raise RuntimeError(code)
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def helper(name):
 p=Path(__file__).with_name(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def tau(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 if not m:raise ValueError('QUESTION_PARSE')
 return f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.'
def pair(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 return tuple(sorted(' '.join(x.replace('_',' ').split()).casefold() for x in m.groups()))
def anchor(q,canon):
 q=min(q,tau(q),key=lambda x:x.encode('utf-8'));k=int.from_bytes(hashlib.sha256(b'VLM070/c-anchor/'+q.encode('utf-8')).digest()[:8],'big')%42
 return next(canon[(k+i)%42] for i in range(42) if pair(canon[(k+i)%42])!=pair(q))
def codecheck(root):
 for x in read(root/'code-seal.json')['files']:assert sha(Path(x['path']).read_bytes())==x['sha256'],'CODE_IDENTITY'
class Access:
 """Logical payload reads; same-role repeated reads use the same closed buffer."""
 def __init__(self,root,role):self.root=root;self.role=role;self.cache={};self.counts=collections.Counter();self.files=[]
 def data(self,p,kind='metadata',expected=None):
  p=Path(p);key=str(p.resolve())
  if kind=='metadata' and p.resolve().is_relative_to(self.root.resolve()):kind='new_metadata'
  if key not in self.cache:
   b=p.read_bytes();self.counts[kind]+=len(b);self.cache[key]=b;self.files.append(dict(path=key,kind=kind,bytes=len(b),sha256=sha(b)))
   savepath=self.root/(self.role+'-access-progress.json');savepath.write_text(json.dumps(dict(counts=self.counts,files=self.files)))
   prior=collections.Counter()
   for old in self.root.glob('*-access.json'):prior.update(read(old)['counts'])
   for category,cap in dict(feature=512*1024**2,state=128*1024**2,metadata=64*1024**2,checkpoint=128*1024**2).items():require(self.root,prior[category]+self.counts[category]<=cap,'READ_BUDGET',dict(kind=category,bytes=prior[category]+self.counts[category]),cap)
  b=self.cache[key]
  if expected:require(self.root,sha(b)==expected,'CONTENT_IDENTITY',dict(file=p.name,matched=sha(b)==expected),'original sealed digest')
  return b
 def meta(self,p,expected=None):return json.loads(self.data(p,'metadata',expected).decode('utf-8-sig'))
 def tensor(self,p,kind='feature',expected=None):
  import torch
  return torch.load(io.BytesIO(self.data(p,kind,expected)),map_location='cpu',weights_only=True)
 def finish(self):save(self.root/(self.role+'-access.json'),dict(counts=self.counts,files=self.files))
def statehash(state):
 h=hashlib.sha256()
 for k,v in sorted(state.items()):h.update(k.encode());h.update(str(tuple(v.shape)).encode());h.update(str(v.dtype).encode());h.update(v.detach().contiguous().numpy().tobytes())
 return h.hexdigest()
def headclass():
 import torch
 from torch.nn import functional as F
 base=helper('question_temporal_056')
 class Head(base.TemporalHead):
  def forward(self,V,S,R,A,arm):
   assert arm in ARMS and V.device.type==S.device.type==R.device.type==A.device.type=='cpu'
   assert V.shape[1:]==(6,2560) and S.shape==R.shape==A.shape==(V.shape[0],2560)
   assert all(x.dtype==torch.float32 and torch.isfinite(x).all() for x in (V,S,R,A))
   pos=torch.arange(6,dtype=V.dtype).unsqueeze(1);freq=torch.exp(torch.arange(0,64,2,dtype=V.dtype)*(-math.log(10000)/64));pe=torch.zeros(6,64,dtype=V.dtype);pe[:,0::2]=torch.sin(pos*freq);pe[:,1::2]=torch.cos(pos*freq)
   x=self.video(V)+pe;H=F.gelu(x+self.conv(self.norm(x).transpose(1,2)).transpose(1,2))
   a=F.gelu(F.linear(A if arm=='ANCHOR' else S,self.question.weight[:32],self.question.bias[:32]));b=F.gelu(F.linear(R,self.question.weight[32:],self.question.bias[32:]))
   if arm=='CONCAT':select=readout=torch.cat((a,b),-1)
   elif arm=='REVERSE':select=torch.cat((b,b),-1);readout=torch.cat((a,a),-1)
   else:select=torch.cat((a,a),-1);readout=torch.cat((b,b),-1)
   alpha=torch.softmax((H*select[:,None,:]).sum(-1)/8,dim=1);u=(alpha[:,:,None]*H).sum(1);xi=torch.linspace(-1,1,6,dtype=V.dtype);o=(alpha[:,:,None]*xi[None,:,None]*H).sum(1)
   return self.mlp(torch.cat((u,o,readout,u*readout),-1)).squeeze(-1)
 return Head
def fixture(root):
 t=cpu();codecheck(root);Head=headclass();base=helper('question_temporal_056').TemporalHead(2560,2560);state=base.state_dict();v=t.randn(3,6,2560);x=t.randn(3,2560);a=t.randn(3,2560);calls=0;results={}
 with t.no_grad():
  reference=base(v,x);calls+=1
  for arm in ARMS:
   model=Head(2560,2560);model.load_state_dict(state,strict=True);assert set(model.state_dict())==set(state);assert sum(p.numel() for p in model.parameters())==356673
   assert [sum(p.numel() for p in module.parameters()) for module in (model.video,model.question,model.conv,model.mlp)]==[163904,163904,12352,16513]
   z=model(v,x,x,a,arm);calls+=1;assert z.shape==(3,) and t.isfinite(z).all();results[arm]=True
   if arm=='CONCAT':assert t.all(t.abs(z-reference)<=1e-6+1e-5*t.abs(reference))
 assert calls==5 and not t.cuda.is_initialized();save(root/'fixture.json',dict(status='PASS',synthetic_head_forward=calls,backward=0,optimizer=0,all_routes=results,concat_reference_equivalence=True,parameter_count=356673,parameter_participation='Static paths; all gradients checked on every actual training update'))
def prepare(root):
 t=cpu();codecheck(root);a=Access(root,'prepare');parent=a.meta(root/'parent.json');p63=Path(parent['prior063']);p68=Path(parent['prior068']);expected={}
 for p in (p63,p68):require(root,a.meta(p/'parent-closed.json')['push']=='SUCCEEDED','PRIOR_NOT_CLOSED',str(p),'pushSUCCEEDED')
 for name in ('training','prediction','scoring'):
  j=a.meta(p63/(name+'-job.json'));require(root,j['active']==j['exit_code']==0,'PRIOR_JOB',j,'active0/exit0')
 for name in ('gpu','prediction','scoring','independent-review'):
  j=a.meta(p68/(name+'-job.json'));require(root,j['active']==j['exit_code']==0,'PRIOR_JOB',j,'active0/exit0')
 for name in ('input-seal.json','output-seal.json'):
  for x in a.meta(p63/name)['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 old=a.meta(p63/'old-assets.json');p62=Path(old['prior062']);p60=Path(old['prior060'])
 for x in old['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 for prior in (p62,p60):require(root,a.meta(prior/'parent-closed.json')['push']=='SUCCEEDED','SOURCE_PARENT_CLOSURE',str(prior),'SUCCEEDED')
 originals62=a.meta(p62/'output-seal.json');originals60=a.meta(p60/'outputs-identity-seal.json')
 for x in originals62['files']+originals60['files']:
  key=str(Path(x['path']).resolve())
  if key in expected:require(root,expected[key]==x['sha256'],'ORIGINAL_SEAL_CONFLICT',Path(key).name,'identical historical content identity')
  expected[key]=x['sha256']
 require(root,all(str((p60/(sp+'-labels.json')).resolve()) in expected for sp in SPLITS[:4]) and str((p63/'scoring-bindings.json').resolve()) in expected,'SCORE_ASSET_REGISTRATION',False,True)
 def meta(p):return a.meta(p,expected.get(str(Path(p).resolve())))
 def tensor(p,kind='feature'):
  key=str(Path(p).resolve());require(root,key in expected,'MISSING_ORIGINAL_IDENTITY',Path(p).name,'original content seal');return a.tensor(p,kind,expected[key])
 code63=a.meta(p63/'code-seal.json')
 for x in code63['files']:require(root,sha(a.data(x['path']).replace(b'\r\n',b'\n'))==x['lf_sha256'],'OLD_CODE_IDENTITY',Path(x['path']).name,'original LF digest')
 c68=a.meta(p68/'complete-code-seal.json');i68=a.meta(p68/'input-seal.json');f68=a.meta(p68/'feature-seal.json');ps68=a.meta(p68/'prediction-seal.json')
 obs={s:meta(p63/(s+'-observations.json')) for s in SPLITS[:4]};obs[SPLITS[4]]=a.meta(p68/'observations.json',i68['observations_sha256']);require(root,[len(obs[s]) for s in SPLITS]==list(NS),'SPLIT_COUNTS',[len(obs[s]) for s in SPLITS],NS)
 index=meta(p63/'feature-index.json');idx68=a.meta(p68/'feature-index.json',f68['index_sha256']);merged={k:dict(index[k]) for k in ('video','text')}
 for kind in merged:
  for key,r in idx68[kind].items():
   if key in merged[kind]:require(root,expected.get(str(Path(merged[kind][key]['path']).resolve()))==r['sha256'],'SAME_KEY_IDENTITY_CONFLICT',kind,'same original identity')
   merged[kind][key]=r;expected[str(Path(r['path']).resolve())]=r['sha256']
 require(root,len(merged['video'])<=466 and len(merged['text'])<=320,'FEATURE_COUNTS',{k:len(v) for k,v in merged.items()},{'video':466,'text':320})
 neededV={v for rows in obs.values() for row in rows for v in row['videos']};neededQ={q for rows in obs.values() for row in rows for q in row['questions']};require(root,set(merged['video'])==neededV and set(merged['text'])==neededQ,'FEATURE_MEMBERSHIP',{'V':len(neededV),'q':len(neededQ)},'exact registered fixed observations')
 V={k:tensor(r['path']) for k,r in merged['video'].items()};h={k:tensor(r['path']) for k,r in merged['text'].items()}
 require(root,all(v.shape==(6,2560) and v.dtype==t.float32 and t.isfinite(v).all() for v in V.values()) and all(v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all() for v in h.values()),'FEATURE_SHAPE_FINITE',{'V':len(V),'h':len(h)},'V[6,2560]/h[2560]finite float32')
 train=sorted({q for row in obs[SPLITS[0]] for q in row['questions']},key=lambda q:q.encode());canon=sorted({min(q,tau(q),key=lambda x:x.encode()) for q in train},key=lambda q:q.encode());require(root,len(train)==84 and len(canon)==42 and {tau(q) for q in train}==set(train) and all(tau(tau(q))==q and tau(q) in h for q in h),'TAU_TRAIN84',{'train':len(train),'canonical':len(canon)},'84/42/tau closed')
 norm=tensor(p62/'normalizer.pt','state');stats=norm['D_ROLE'];require(root,stats['mu'].shape==(2560,) and stats['mu'].dtype==t.float64 and stats['scale'].ndim==0 and stats['scale'].dtype==t.float64 and t.isfinite(stats['mu']).all() and t.isfinite(stats['scale']) and stats['scale']>1e-8,'D_NORMALIZER',{'mu_shape':list(stats['mu'].shape),'scale':float(stats['scale'])},'original finite float64 mu/scalarRMS>1e-8')
 cr={q:(v.double()+h[tau(q)].double())/2 for q,v in h.items()};z=t.stack([cr[q] for q in train]);mu=z.mean(0);scale=(z-mu).square().mean().sqrt();require(root,t.isfinite(mu).all() and t.isfinite(scale) and scale>1e-8,'C_NORMALIZER',{'scale':float(scale)},'finite train84scalarRMS>1e-8')
 S={q:((v-mu)/scale).float() for q,v in cr.items()};R={q:(((v.double()-h[tau(q)].double())/2-stats['mu'])/stats['scale']).float() for q,v in h.items()};anchors={q:anchor(q,canon) for q in h};require(root,all(t.equal(S[q],S[tau(q)]) and anchors[q]==anchors[tau(q)] and pair(q)!=pair(anchors[q]) for q in h),'ANCHOR_OR_SYMMETRY',False,True)
 plans={}
 for seed in SEEDS:
  plan=tensor(p63/f'plan-{seed}.pt','state');require(root,plan['sequence'].shape==(250,8) and plan['sequence'].dtype==t.int64 and int(plan['sequence'].min())>=0 and int(plan['sequence'].max())<68 and len(t.unique(plan['sequence']))==68,'ORIGINAL_SEQUENCE',{'seed':seed,'shape':list(plan['sequence'].shape)},'original250x8/68')
  model=headclass()(2560,2560);model.load_state_dict(plan['state'],strict=True);plans[seed]=dict(state_hash=statehash(model.state_dict()),source_sha256=expected[str((p63/f'plan-{seed}.pt').resolve())]);t.save(plan,root/f'plan-{seed}.pt')
 labels=meta(p63/'train-labels.json');require(root,len(labels)==68 and all(x['index']==i for i,x in enumerate(labels)),'TRAIN_LABEL_BINDING',len(labels),68)
 trainbundle=dict(V=t.stack([t.stack([V[v] for v in x['videos']]) for x in obs[SPLITS[0]]]),S=t.stack([t.stack([S[q] for q in x['questions']]) for x in obs[SPLITS[0]]]),R=t.stack([t.stack([R[q] for q in x['questions']]) for x in obs[SPLITS[0]]]),A=t.stack([t.stack([S[anchors[q]] for q in x['questions']]) for x in obs[SPLITS[0]]]),y=t.tensor([x['labels'] for x in labels],dtype=t.float32))
 require(root,trainbundle['y'].shape==(68,2,2) and t.all((trainbundle['y']==0)|(trainbundle['y']==1)),'TRAIN_LABEL_SHAPE',list(trainbundle['y'].shape),[68,2,2])
 for name,value in [('video.pt',V),('h.pt',h),('views.pt',dict(S=S,R=R)),('new-normalizer.pt',dict(mu=mu,scale=scale)),('train.pt',trainbundle)]:t.save(value,root/name)
 save(root/'observations.json',obs);save(root/'transform-bindings.json',dict(train=train,canonical=canon,anchors=anchors));save(root/'plans.json',plans)
 catalog68=a.meta(p68/'asset-catalog.json',c68['asset_catalog_sha256'])
 save(root/'sources.json',dict(prior063=str(p63),prior062=str(p62),prior060=str(p60),prior068=str(p68),expected=expected,old_index=merged,normalizer_path=str(p62/'normalizer.pt'),original_068_prediction_seal=ps68,raw_publisher=dict(path=str(Path(catalog68['prior066'])/'dy.body'),sha256=catalog68['raw_DyBench_identity']['sha256'],positions=catalog68['selected_positions']),source_labels_path=str(p60),groups_path=str(p63/'scoring-bindings.json')))
 records=[]
 for name,kind in [('video.pt','feature'),('h.pt','feature'),('views.pt','feature'),('new-normalizer.pt','state'),('train.pt','feature')]+[(f'plan-{s}.pt','state') for s in SEEDS]+[(n,'metadata') for n in ('observations.json','transform-bindings.json','plans.json','sources.json')]:records.append(dict(name=name,kind=kind,sha256=sha(a.data(root/name,kind))))
 save(root/'input-seal.json',dict(status='CLOSED',files=records,train_files=['train.pt','plans.json']+[f'plan-{s}.pt' for s in SEEDS],planned_updates=6000,planned_new_cells=22368,planned_cached_cells=11184,planned_total_cells=33552));a.finish();require(root,not t.cuda.is_initialized(),'CUDA_INITIALIZED',True,False);print('PREPARED_070',len(V),len(h),'train84/canon42',flush=True)
def inputs(root,a,train=False):
 seal=a.meta(root/'input-seal.json');require(root,seal['status']=='CLOSED','INPUT_SEAL_STATE',seal['status'],'CLOSED')
 for x in seal['files']:
  if not train or x['name'] in seal['train_files']:a.data(root/x['name'],x['kind'],x['sha256'])
 return seal
def train(root):
 t=cpu();codecheck(root);a=Access(root,'training');inputs(root,a,True);data=a.tensor(root/'train.pt');plans=a.meta(root/'plans.json');Head=headclass();directory=root/'training';directory.mkdir();start=time.monotonic();total=0
 for seed in SEEDS:
  plan=a.tensor(root/f'plan-{seed}.pt','state')
  for arm in ARMS:
   CONTEXT.update(stage='TRAIN_CONFIGURATION',seed=seed,arm=arm,completed=total,remaining=6000-total);d=directory/f'{arm}-{seed}';d.mkdir();j=d/'steps.jsonl';event(j,event='STARTED',seed=seed,arm=arm);model=Head(2560,2560);model.load_state_dict(plan['state']);initial=statehash(model.state_dict());require(root,initial==plans[str(seed)]['state_hash'],'INITIAL_SHARED_IDENTITY',initial,plans[str(seed)]['state_hash']);opt=helper('question_temporal_056').optimizer(model)
   for step,ids in enumerate(plan['sequence']):
    CONTEXT.update(stage='TRAIN_STEP',step=step,completed=total,remaining=6000-total);require(root,time.monotonic()-start<1450,'TRAIN_DEADLINE',time.monotonic()-start,1450);event(j,event='STEP_STARTED',step=step)
    v=data['V'][ids][:,:,None].expand(-1,-1,2,-1,-1).reshape(32,6,2560);qs=[data[k][ids][:,None].expand(-1,2,-1,-1).reshape(32,2560) for k in ('S','R','A')];out=model(v,*qs,arm).reshape(8,2,2);loss=t.nn.functional.softplus(-(2*data['y'][ids]-1)*out).mean();require(root,t.isfinite(loss),'NONFINITE_LOSS',float(loss.detach()),'finite');opt.zero_grad(set_to_none=True);loss.backward();ok=all(p.grad is not None and t.isfinite(p.grad).all() for p in model.parameters());require(root,ok,'GRADIENTS',ok,'all10 nonNone finite');gn=t.nn.utils.clip_grad_norm_(model.parameters(),1);require(root,t.isfinite(gn),'GRADIENT_NORM',float(gn),'finite');opt.step();total+=1;event(j,event='STEP_CLOSED',step=step,loss=float(loss.detach()),grad_norm=float(gn),all_grad_finite=True,non_none=10,backward=1,optimizer_step=1,exposures=32)
   final=statehash(model.state_dict());require(root,final!=initial,'UNCHANGED_PARAMETERS',final,initial);t.save(model.state_dict(),d/'final.pt');event(j,event='CLOSED',steps=250,initial_state_hash=initial,final_state_hash=final);print('TRAIN_CLOSED',seed,arm,'TOTAL',total,flush=True)
 require(root,total==6000 and not t.cuda.is_initialized(),'TRAIN_TOTAL_OR_CUDA',total,6000);save(root/'training-seal.json',dict(status='CLOSED',updates=total,backward=total,optimizer=total,exposures=total*32,files=[dict(path=str(p),sha256=sha(a.data(p,'checkpoint'))) for p in directory.glob('*/final.pt')]));a.finish();print('6000_REAL_UPDATES_CLOSED',flush=True)
def predict(root):
 t=cpu();codecheck(root);a=Access(root,'prediction');j=a.meta(root/'training-job.json');require(root,j['active']==j['exit_code']==0,'TRAIN_JOB_NOT_CLOSED',j,'active0exit0');inputs(root,a);V=a.tensor(root/'video.pt');views=a.tensor(root/'views.pt');obs=a.meta(root/'observations.json');anchors=a.meta(root/'transform-bindings.json')['anchors'];seal=a.meta(root/'training-seal.json');expected={x['path']:x['sha256'] for x in seal['files']};Head=headclass();outputs=[]
 for seed in SEEDS:
  for arm in ARMS:
   path=root/'training'/f'{arm}-{seed}'/'final.pt';model=Head(2560,2560);model.load_state_dict(a.tensor(path,'checkpoint',expected[str(path)]));model.eval();model.requires_grad_(False)
   with t.no_grad():
    for split in SPLITS:
     for row in obs[split]:
      for vi,name in enumerate(row['videos']):
       for qi,q in enumerate(row['questions']):
        key=[arm,seed,split,row['index'],vi,qi];CONTEXT.update(stage='PREDICTION',key=key,completed=len(outputs),remaining=22368-len(outputs));event(root/'prediction.jsonl',event='STARTED',key=key);z=model(V[name][None],views['S'][q][None],views['R'][q][None],views['S'][anchors[q]][None],arm);require(root,z.numel()==1 and t.isfinite(z).all(),'PREDICTION_FINITE_SHAPE',{'shape':list(z.shape),'finite':bool(t.isfinite(z).all())},'finite scalar');outputs.append(dict(method=arm,seed=seed,split=split,index=row['index'],video=vi,question=qi,status='CLOSED',prediction=int(z.item()>0)));event(root/'prediction.jsonl',event='CLOSED',key=key)
   assert all(not p.requires_grad and p.grad is None for p in model.parameters());print('PREDICT_CLOSED',seed,arm,flush=True)
 require(root,len(outputs)==22368 and not t.cuda.is_initialized(),'PREDICTION_TOTAL_OR_CUDA',len(outputs),22368);save(root/'new-outputs.json',outputs);files=[dict(name='new-outputs.json',kind='metadata',sha256=sha(a.data(root/'new-outputs.json')))];save(root/'output-seal.json',dict(status='CLOSED',files=files,training_seal_sha256=sha(a.data(root/'training-seal.json')),input_seal_sha256=sha(a.data(root/'input-seal.json')),cells=22368));a.finish()
def metrics(pred,labels):
 count=collections.Counter();details=[]
 for p,y in zip(pred,labels):
  correct=[p[2*v+q]==y[v][q] for v in range(2) for q in range(2)];k=sum(correct);iv=int(p[0]==p[1] and p[2]==p[3]);kind='CONSTANT' if len(set(p))==1 else 'VIDEO_ONLY' if iv else 'QUESTION_ONLY' if p[0]==p[2] and p[1]==p[3] else 'CHECKERBOARD' if p[0]==p[3] and p[1]==p[2] else 'MIXED';count.update(correct_cells=k,video_pair_correct=int(correct[0] and correct[2])+int(correct[1] and correct[3]),question_pair_correct=int(correct[0] and correct[1])+int(correct[2] and correct[3]),four_way_correct=int(k==4),question_invariant=iv);count['K'+str(k)]+=1;count[kind]+=1;details.append(dict(four=int(k==4),inv=iv))
 return count,details
def quantile(values,p):
 v=sorted(values);x=(len(v)-1)*p;i=int(x);return v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
def intervals(hist,pairs):
 rows=[]
 for split,G in zip(MAINS,(25,50)):
  rng=random.Random(55070);draws=[rng.choices(range(G),k=G) for _ in range(10000)];rng=random.Random(55071);seeddraws=[rng.choices(range(6),k=6) for _ in range(10000)]
  for right in RIGHTS[1:]:
   hs=sorted([x for x in hist if x['split']==split and x['right']==right],key=lambda x:x['seed_sum']);vector=[x['seed_sum'] for x in hs for _ in range(x['count'])];nets=[next(x['net'] for x in pairs if x['split']==split and x['right']==right and x['seed']==s) for s in SEEDS];assert len(vector)==G and sum(vector)==sum(nets)
   for axis,vals in [('file_family' if G==25 else 'file_pair',[100*sum(vector[i] for i in d)/300 for d in draws]),('seed',[100*sum(nets[i] for i in d)/300 for d in seeddraws])]:rows.append(dict(split=split,right=right,axis=axis,status='CLOSED',point_pp=100*sum(nets)/300,lower_pp=quantile(vals,.025),upper_pp=quantile(vals,.975),draws=10000,planned_draws=10000))
 return rows
def score(root):
 import csv
 codecheck(root);a=Access(root,'scoring');CONTEXT.update(stage='SCORING',completed=0,remaining=33552)
 for n in ('training','prediction'):
  j=a.meta(root/(n+'-job.json'));require(root,j['active']==j['exit_code']==0,'JOB_NOT_CLOSED',j,'active0exit0')
 osseal=a.meta(root/'output-seal.json');new=a.meta(root/'new-outputs.json',osseal['files'][0]['sha256']);expectedkeys={(m,s,sp,i,v,q) for m in ARMS for s in SEEDS for sp,n in zip(SPLITS,NS) for i in range(n) for v in range(2) for q in range(2)}
 key=lambda x:(x['method'],x['seed'],x['split'],x['index'],x['video'],x['question'])
 require(root,len(new)==len(expectedkeys)==22368 and {key(x) for x in new}==expectedkeys and all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) for x in new),'NEW_OUTPUT_KEYS',len(new),22368)
 src=a.meta(root/'sources.json');p63=Path(src['prior063']);p68=Path(src['prior068']);expected=src['expected'];old63=a.meta(p63/'new-outputs.json',expected[str((p63/'new-outputs.json').resolve())]);baseline=[dict(x,method='C_CACHED' if x['method']=='C_NATIVE' else 'D_CACHED') for x in old63 if x['method'] in ('C_NATIVE','D_NATIVE') and x['seed'] in SEEDS];require(root,len(baseline)==8784,'BASELINE063_COUNT',len(baseline),8784)
 old68=a.meta(p68/'outputs.json',src['original_068_prediction_seal']['outputs_sha256']);baseline.extend(dict(x,method='C_CACHED' if x['method']=='C_NATIVE' else 'D_CACHED',split=SPLITS[4]) for x in old68);require(root,len(baseline)==11184,'BASELINE_TOTAL',len(baseline),11184)
 labels={sp:[x['labels'] for x in a.meta(Path(src['source_labels_path'])/(sp+'-labels.json'),expected.get(str((Path(src['source_labels_path'])/(sp+'-labels.json')).resolve())))] for sp in SPLITS[:4]}
 # No historical standalone seal exists for the derived068 labels: rebuild from registered original metadata.
 raw=a.meta(src['raw_publisher']['path'],src['raw_publisher']['sha256']);obs=a.meta(root/'observations.json');ys=[]
 for row,positions in zip(obs[SPLITS[4]],src['raw_publisher']['positions']):
  lookup={raw[i]['video']:raw[i] for i in positions};y=[]
  for name in row['videos']:
   x=lookup[name];assert x['candidates']==['First action 1, then action 2','First action 2, then action 1'] and x['answer'] in x['candidates'];b=int(x['answer']==x['candidates'][0]);y.append([b,1-b])
  ys.append(y)
 require(root,ys==a.meta(p68/'scoring-labels.json'),'PUBLISHER_DERIVED_LABELS',False,True);labels[SPLITS[4]]=ys;save(root/'scoring-labels.json',labels);groups=a.meta(src['groups_path'],expected[str(Path(src['groups_path']).resolve())])['groups'];require(root,len(set(groups[MAINS[0]]))==25 and all(groups[MAINS[0]].count(g)==2 for g in set(groups[MAINS[0]])),'SOURCE_FAMILY_25X2',len(set(groups[MAINS[0]])),25)
 outputs=new+baseline;lookup={key(x):x for x in outputs};require(root,len(lookup)==len(outputs)==33552,'ALL_KEYS',len(lookup),33552);conditions=[];detail={}
 for method in METHODS:
  for seed in SEEDS:
   for split,n in zip(SPLITS,NS):
    ps=[]
    for i in range(n):
     rows=[lookup[method,seed,split,i,v,q] for v in range(2) for q in range(2)];assert all(x['status']=='CLOSED' and x['prediction'] in (0,1) for x in rows);ps.append([x['prediction'] for x in rows])
    c,ds=metrics(ps,labels[split]);cached=method.endswith('CACHED');row=dict(method=method,seed=seed,split=split,status='CLOSED',planned_items=n,planned_cells=4*n,new_cells=0 if cached else 4*n,cached_cells=4*n if cached else 0,CLOSED=4*n,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown_cells=0,scoring_unknown_cells=0,**{k:c[k] for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4','CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')});row.update(cell_accuracy_pct=25*c['correct_cells']/n,video_pair_accuracy_pct=50*c['video_pair_correct']/n,question_pair_accuracy_pct=50*c['question_pair_correct']/n,four_way_accuracy_pct=100*c['four_way_correct']/n,question_invariant_pct=100*c['question_invariant']/n);conditions.append(row);detail[method,seed,split]=ds
 # Reproduce all60 cached published conditions; public tables contain no per-item data.
 pub=Path(__file__).parent.parent/'docs/codex-artifacts';oldtables=list(csv.DictReader((pub/'VLM-ROLE-CONTRAST-REPLICATION-063/condition-summary.csv').open(encoding='utf-8-sig')));tab68=list(csv.DictReader((pub/'VLM-FROZEN-TRANSFER-READMISSION-068/condition-summary.csv').open(encoding='utf-8-sig')))
 for row in conditions:
  if not row['method'].endswith('CACHED'):continue
  original='C_NATIVE' if row['method']=='C_CACHED' else 'D_NATIVE';table=tab68 if row['split']==SPLITS[4] else oldtables;matches=[x for x in table if x['method']==original and str(x['seed'])==str(row['seed']) and (row['split']==SPLITS[4] or x['split']==row['split'])];assert len(matches)==1
  for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4'):assert row[k]==int(matches[0][k]),('BASELINE_AGGREGATE',k)
 pairs=[];hist=[];gates={}
 for split in MAINS:
  for seed in SEEDS:
   L=detail['FACTOR',seed,split]
   for right in RIGHTS:
    R=detail[right,seed,split];lo=sum(l['four'] and not r['four'] for l,r in zip(L,R));ro=sum(r['four'] and not l['four'] for l,r in zip(L,R));iv=sum(l['inv']-r['inv'] for l,r in zip(L,R));pairs.append(dict(split=split,seed=seed,left='FACTOR',right=right,status='CLOSED',planned_items=50,evaluated_items=50,left_only=lo,right_only=ro,both_correct=sum(l['four'] and r['four'] for l,r in zip(L,R)),both_wrong=sum(not l['four'] and not r['four'] for l,r in zip(L,R)),unknown=0,net=lo-ro,delta_four_way_pp=2*(lo-ro),invariant_net=iv,question_invariant_delta_pp=2*iv))
  for right in RIGHTS[1:]:
   nets=[sum(detail['FACTOR',s,split][i]['four']-detail[right,s,split][i]['four'] for s in SEEDS) for i in range(50)]
   if split==MAINS[0]:values=[sum(v for v,g in zip(nets,groups[split]) if g==group) for group in sorted(set(groups[split]))];extent=12
   else:values=nets;extent=6
   counts=collections.Counter(values);hist.extend(dict(split=split,right=right,seed_sum=k,count=counts[k],status='CLOSED') for k in range(-extent,extent+1))
  checks={}
  for right in RIGHTS[1:]:
   nets=[p['net'] for p in pairs if p['split']==split and p['right']==right];positive=sum(x>0 for x in nets);total=sum(nets);strict=right in ('D_CACHED','CONCAT');checks[right]=dict(positive_seeds=positive,total_net=total,required_positive=5 if strict else 4,required_total_net=18 if strict else 9,pass_gate=positive>=(5 if strict else 4) and total>=(18 if strict else 9))
  total=sum(x['four_way_correct'] for x in conditions if x['split']==split and x['method']=='FACTOR');checks['absolute']=dict(total_correct=total,required=60,pass_gate=total>=60);gates[split]=dict(checks=checks,pass_gate=all(x['pass_gate'] for x in checks.values()))
 save(root/'cached-outputs-projected.json',baseline);save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,histogram=hist,intervals=intervals(hist,pairs),gates=gates,conclusion='SEMANTIC_ROLE_FACTOR_PILOT_SIGNAL' if all(x['pass_gate'] for x in gates.values()) else 'NO_SUPPORT_FOR_THIS_FACTORED_ROUTING',disposition='SELECTIVITY_AND_NOVELTY_UNCONFIRMED' if all(x['pass_gate'] for x in gates.values()) else 'STOP_THIS_RECIPE',baseline_reproduced_conditions=60));a.finish();print('SCORED_33552',json.dumps(gates),flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('role',choices=('fixture','prepare','train','predict','score'));parser.add_argument('--root',required=True);args=parser.parse_args();root=Path(args.root);CONTEXT.update(stage=args.role,completed=0,remaining='planned matrix')
 try:globals()[args.role](root)
 except Exception as e:event(root/'stops.jsonl',reason_code=str(e) or type(e).__name__,actual=dict(CONTEXT),limit='sealed070contract',stage=args.role,error_type=type(e).__name__);raise
