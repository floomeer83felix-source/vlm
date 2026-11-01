"""071 explicit frozen CPU intervention roles; no research operation on import."""
import argparse,collections,csv,hashlib,importlib.util,io,json,math,os,random,time
from pathlib import Path
SEEDS=(137,263,419,557,733,911);ARMS=('CONCAT','FACTOR','REVERSE','ANCHOR');SPLITS=('source_holdout50','item_transfer50');MODES=('TRAIN_MEAN','UNIFORM');CONDITIONS=('ORIGINAL_CACHED',)+MODES
CONTEXT={}
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(dict(at_unix=time.time(),**x),ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def require(root,ok,code,actual,limit):
 if not ok:event(root/'failures.jsonl',reason_code=code,actual=actual,limit=limit,context=dict(CONTEXT));raise RuntimeError(code)
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def helper():
 p=Path(__file__).with_name('semantic_role_factor_070.py');s=importlib.util.spec_from_file_location('architecture070',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def codecheck(root):
 for x in read(root/'code-seal.json')['files']:assert sha(Path(x['path']).read_bytes())==x['sha256'],'CODE_IDENTITY'
class Access:
 def __init__(self,root,role):self.root=root;self.role=role;self.cache={};self.counts=collections.Counter();self.files=[]
 def data(self,p,kind='metadata',expected=None):
  p=Path(p);key=str(p.resolve())
  if kind=='metadata' and p.resolve().is_relative_to(self.root.resolve()):kind='new_metadata'
  if key not in self.cache:
   b=p.read_bytes();self.cache[key]=b;self.counts[kind]+=len(b);self.files.append(dict(path=key,kind=kind,bytes=len(b),sha256=sha(b)));(self.root/(self.role+'-access-progress.json')).write_text(json.dumps(dict(counts=self.counts,files=self.files)))
   prior=collections.Counter()
   for old in self.root.glob('*-access.json'):prior.update(read(old)['counts'])
   for k,cap in dict(feature=256*1024**2,state=128*1024**2,metadata=64*1024**2).items():require(self.root,prior[k]+self.counts[k]<=cap,'READ_LIMIT',{'kind':k,'bytes':prior[k]+self.counts[k]},cap)
  b=self.cache[key]
  if expected:require(self.root,sha(b)==expected,'CONTENT_IDENTITY',{'file':p.name,'matched':sha(b)==expected},'registered content seal')
  return b
 def meta(self,p,expected=None):return json.loads(self.data(p,expected=expected).decode('utf-8-sig'))
 def tensor(self,p,kind='feature',expected=None):
  import torch
  return torch.load(io.BytesIO(self.data(p,kind,expected)),map_location='cpu',weights_only=True)
 def finish(self):save(self.root/(self.role+'-access.json'),dict(counts=self.counts,files=self.files))
def tensorbytes(x):return x.detach().contiguous().numpy().tobytes()
def loadhead(state):
 import torch
 assert all(v.dtype==torch.float32 and torch.isfinite(v).all() for v in state.values())
 m=helper().headclass()(2560,2560);m.load_state_dict(state,strict=True);m.eval();m.requires_grad_(False);assert sum(p.numel() for p in m.parameters())==356673;return m
class Projections:
 def __init__(self,m,views,anchors,counts,caches=None):self.m=m;self.views=views;self.anchors=anchors;self.counts=counts;self.cache=caches if caches is not None else dict(A={},B={})
 def piece(self,branch,q):
  import torch
  if q not in self.cache[branch]:
   ix=slice(0,32) if branch=='A' else slice(32,64);v=self.views['S' if branch=='A' else 'R'][q][None];z=torch.nn.functional.linear(v,self.m.question.weight[ix],self.m.question.bias[ix]);self.counts['question_'+branch+'_linear']+=1;z=torch.nn.functional.gelu(z);self.counts['question_'+branch+'_GELU']+=1;self.cache[branch][q]=z[0].clone()
  return self.cache[branch][q][None]
 def vectors(self,q,arm,need_read=True):
  import torch
  if arm=='CONCAT':g=torch.cat((self.piece('A',q),self.piece('B',q)),-1);return g,g if need_read else None
  if arm=='REVERSE':x=self.piece('B',q);select=torch.cat((x,x),-1);x=self.piece('A',q) if need_read else None
  else:x=self.piece('A',self.anchors[q] if arm=='ANCHOR' else q);select=torch.cat((x,x),-1);x=self.piece('B',q) if need_read else None
  return select,torch.cat((x,x),-1) if need_read else None
def hidden(m,v,counts):
 import torch
 pos=torch.arange(6,dtype=v.dtype).unsqueeze(1);freq=torch.exp(torch.arange(0,64,2,dtype=v.dtype)*(-math.log(10000)/64));pe=torch.zeros(6,64,dtype=v.dtype);pe[:,0::2]=torch.sin(pos*freq);pe[:,1::2]=torch.cos(pos*freq);x=m.video(v[None])+pe;counts['video_linear']+=1;y=m.norm(x);counts['video_LN']+=1;y=m.conv(y.transpose(1,2)).transpose(1,2);counts['video_conv']+=1;counts['video_GELU']+=1;return torch.nn.functional.gelu(x+y)
def alpha(H,select):
 import torch
 return torch.softmax((H*select[:,None,:]).sum(-1)/8,dim=1)
def mlpinput(H,g,weights):
 import torch
 u=(weights[:,:,None]*H).sum(1);xi=torch.linspace(-1,1,6,dtype=H.dtype);o=(weights[:,:,None]*xi[None,:,None]*H).sum(1);return torch.cat((u,o,g,u*g),-1)
def fixture(root):
 t=cpu();codecheck(root);base=helper().headclass()(2560,2560);v=t.randn(6,2560);S=t.randn(2560);R=t.randn(2560);A=t.randn(2560);views=dict(S={'q':S,'a':A},R={'q':R});counts=collections.Counter();p=Projections(base,views,{'q':'a'},counts);calls=0
 with t.no_grad():
  H=hidden(base,v,counts)
  for arm in ARMS:
   original=base(v[None],S[None],R[None],A[None],arm);calls+=1;s,g=p.vectors('q',arm);w=alpha(H,s);X=mlpinput(H,g,w);override=mlpinput(H,g,alpha(H,s));assert t.equal(X,override);uniform=t.full((1,6),1/6,dtype=t.float32);U=mlpinput(H,g,uniform);assert t.equal(X[:,128:192],U[:,128:192]) and t.equal(U[:,128:192],g)
   if arm=='FACTOR':
    z=base.mlp(override);calls+=1;assert t.all(t.abs(z.reshape(-1)-original)<=1e-6+1e-5*t.abs(original));assert t.isfinite(base.mlp(U)).all();calls+=1
  synthetic=t.randn(84,64);mean=synthetic.double().mean(0).float();assert t.equal(mean,t.stack([row.double() for row in synthetic]).mean(0).float())
 assert calls==6 and not t.cuda.is_initialized();save(root/'fixture.json',dict(status='PASS',synthetic_answer_calls=calls,original_synthetic_full_head=4,explicit_synthetic_MLP=2,optimizer=0,backward=0,override_equivalence=True,readout_shared=True,uniform=True,mean_algorithm=True,manual_partial_counts=counts,total_submodule_counts=dict(video_linear=5,video_LN=5,video_conv=5,video_GELU=5,question_A_linear=6,question_A_GELU=6,question_B_linear=5,question_B_GELU=5,MLP=6,MLP_linear1=6,MLP_GELU=6,MLP_linear2=6)))
def prepare(root):
 t=cpu();codecheck(root);a=Access(root,'preparation');p=Path(a.meta(root/'parent.json')['prior070']);require(root,a.meta(p/'parent-closed.json')['push']=='SUCCEEDED','PRIOR_NOT_CLOSED',False,True)
 for name in ('training','prediction','scoring','independent-review'):
  j=a.meta(p/(name+'-job.json'));require(root,j['active']==j['exit_code']==0,'PRIOR_JOB',j,'active0/exit0')
 oldcode=a.meta(p/'code-seal.json')
 for x in oldcode['files']:require(root,sha(a.data(x['path']))==x['sha256'],'SOURCE_CODE_IDENTITY',Path(x['path']).name,'original seal')
 ins=a.meta(p/'input-seal.json');outs=a.meta(p/'output-seal.json');train=a.meta(p/'training-seal.json',outs['training_seal_sha256']);require(root,sha(a.data(p/'input-seal.json'))==outs['input_seal_sha256'],'SOURCE_INPUT_SEAL',False,True)
 allowed=('video.pt','views.pt','observations.json','transform-bindings.json','sources.json');ex={x['name']:x for x in ins['files'] if x['name'] in allowed};require(root,len(ex)==5,'REQUIRED_INPUTS',len(ex),5)
 def meta(n):return a.meta(p/n,ex[n]['sha256'])
 obsall=meta('observations.json');obs={s:obsall[s] for s in SPLITS};bind=meta('transform-bindings.json');sources=meta('sources.json');rawV=a.tensor(p/'video.pt',expected=ex['video.pt']['sha256']);rawviews=a.tensor(p/'views.pt',expected=ex['views.pt']['sha256']);trainq=bind['train'];require(root,len(trainq)==84 and trainq==sorted(set(trainq),key=lambda q:q.encode()) and all(len(obs[s])==50 for s in SPLITS),'FIXED_MEMBERSHIP',{'train':len(trainq),'splits':[len(obs[s]) for s in SPLITS]},'84/50/50')
 evalq={q for rows in obs.values() for row in rows for q in row['questions']};neededq=evalq|set(trainq)|{bind['anchors'][q] for q in evalq|set(trainq)};neededV={v for rows in obs.values() for row in rows for v in row['videos']};data=dict(V={k:rawV[k] for k in neededV},views={kind:{k:rawviews[kind][k] for k in neededq} for kind in ('S','R')});require(root,all(v.shape==(6,2560) and v.dtype==t.float32 and t.isfinite(v).all() for v in data['V'].values()) and all(x.shape==(2560,) and x.dtype==t.float32 and t.isfinite(x).all() for vs in data['views'].values() for x in vs.values()),'INPUT_TENSORS',{'V':len(neededV),'q':len(neededq)},'finite float32 original shapes')
 states={x['path']:x['sha256'] for x in train['files']};means={};counts=collections.Counter()
 with t.no_grad():
  for seed in SEEDS:
   for arm in ARMS:
    tag=f'{arm}-{seed}';path=p/'training'/tag/'final.pt';digest=states[str(path)];CONTEXT.update(stage='TRAIN_MEAN',head=tag,completed=len(means),remaining=24-len(means));event(root/'mean-ledger.jsonl',event='STARTED',head=tag,state_sha256=digest);m=loadhead(a.tensor(path,'state',digest));proj=Projections(m,data['views'],bind['anchors'],counts);vectors=t.cat([proj.vectors(q,arm,False)[0] for q in trainq],0);mean=vectors.double().mean(0).float();require(root,mean.shape==(64,) and t.isfinite(mean).all(),'MEAN_SELECT_FINITE',list(mean.shape),'finite[64]');means[tag]=dict(train_select=vectors,mean_select=mean,projection_cache=proj.cache,state_path=str(path),state_sha256=digest);event(root/'mean-ledger.jsonl',event='CLOSED',head=tag,train_select=84)
 t.save(data,root/'inputs.pt');t.save(means,root/'means.pt');save(root/'observations.json',obs);save(root/'bindings.json',dict(train=trainq,anchors={q:bind['anchors'][q] for q in neededq}));save(root/'sources.json',dict(prior070=str(p),needed_source_inputs=ex,source_output=outs,source_scoring=sources,source_train_seal_sha256=outs['training_seal_sha256'],code070=oldcode));files=[]
 for name,kind in [('inputs.pt','feature'),('means.pt','feature'),('observations.json','metadata'),('bindings.json','metadata'),('sources.json','metadata')]:files.append(dict(name=name,kind=kind,sha256=sha(a.data(root/name,kind))))
 save(root/'input-seal.json',dict(status='CLOSED',files=files,means=24,mean_method='84individual float32 selectors -> ordered float64 mean -> float32'));save(root/'preparation-counts.json',dict(counts=counts,full_head=0,MLP=0,mean_selectors=2016,source_V_container=466,projected_V=len(neededV),source_view_questions=320,projected_questions=len(neededq)));a.finish();assert not t.cuda.is_initialized();print('PREPARED24_FROZEN_MEANS',flush=True)
def inputcheck(root,a):
 seal=a.meta(root/'input-seal.json')
 for x in seal['files']:a.data(root/x['name'],x['kind'],x['sha256'])
def predict(root):
 t=cpu();codecheck(root);a=Access(root,'prediction');inputcheck(root,a);data=a.tensor(root/'inputs.pt');means=a.tensor(root/'means.pt');obs=a.meta(root/'observations.json');bind=a.meta(root/'bindings.json');counts=collections.Counter();outputs=[];geometry=[];attention_only={};start=time.monotonic();directory=root/'geometry';directory.mkdir()
 with t.no_grad():
  for seed in SEEDS:
   for arm in ARMS:
    tag=f'{arm}-{seed}';item=means[tag];m=loadhead(a.tensor(item['state_path'],'state',item['state_sha256']));m.register_forward_pre_hook(lambda *args:(_ for _ in ()).throw(RuntimeError('FORBIDDEN_ORIGINAL_FULL_HEAD')));event(root/'geometry-ledger.jsonl',event='STARTED',head=tag);proj=Projections(m,data['views'],bind['anchors'],counts,item['projection_cache']);keys=[];H={};select={};readout={};origX=[];original_alpha=[]
    for split in SPLITS:
     for row in obs[split]:
      for vi,v in enumerate(row['videos']):
       if v not in H:H[v]=hidden(m,data['V'][v],counts)
       for qi,q in enumerate(row['questions']):
        if q not in select:select[q],readout[q]=proj.vectors(q,arm)
        w=alpha(H[v],select[q]);origX.append(mlpinput(H[v],readout[q],w));original_alpha.append(w);keys.append([arm,seed,split,row['index'],vi,qi,v,q])
    origX=t.cat(origX);original_alpha=t.cat(original_alpha);require(root,origX.shape==(400,256) and original_alpha.shape==(400,6) and t.isfinite(origX).all() and t.isfinite(original_alpha).all(),'ORIGINAL_GEOMETRY_FINITE',{'X':list(origX.shape),'alpha':list(original_alpha.shape)},'finite[400,256]/[400,6]');origmap=collections.defaultdict(list)
    for i,x in enumerate(origX):origmap[sha(tensorbytes(x))].append(i)
    X={mode:t.empty_like(origX) for mode in MODES};weights={mode:t.empty_like(original_alpha) for mode in MODES};newmap={}
    for split in SPLITS:
     for mode in MODES:
      for i,k in enumerate(keys):
       if k[2]!=split:continue
       require(root,time.monotonic()-start<680,'PREDICTION_DEADLINE',time.monotonic()-start,680);key=[arm,seed,split,mode,k[3],k[4],k[5]];CONTEXT.update(stage='INTERVENTION',key=key,completed=len(outputs),remaining=19200-len(outputs));w=alpha(H[k[6]],item['mean_select'][None]) if mode=='TRAIN_MEAN' else t.full((1,6),1/6,dtype=t.float32);x=mlpinput(H[k[6]],readout[k[7]],w);X[mode][i]=x[0];weights[mode][i]=w[0];digest=sha(tensorbytes(x[0]));event(root/'prediction.jsonl',event='STARTED',key=key,input_sha256=digest,state_sha256=item['state_sha256']);result=dict(head_arm=arm,seed=seed,split=split,condition=mode,index=k[3],video=k[4],question=k[5],geometry_index=i,key=key,status='CLOSED',input_sha256=digest,prediction=None,logit=None)
       if digest in origmap:
        refs=origmap[digest];require(root,all(t.equal(x[0],origX[j]) for j in refs),'IDENTITY_CONFLICT_ORIGINAL',digest,'same bytes and element equality');result.update(source_kind='original_alias',original_refs=[keys[j][:6] for j in refs])
       elif digest in newmap:
        previous=newmap[digest];require(root,t.equal(x[0],previous['x']),'IDENTITY_CONFLICT_NEW',digest,'exact equality');result.update(source_kind='new_alias',new_ref=previous['key'])
       else:
        require(root,counts['new_MLP']<19200,'NEW_MLP_CAP',counts['new_MLP'],19200);z=m.mlp(x);counts['new_MLP']+=1;counts['MLP_linear1']+=1;counts['MLP_GELU']+=1;counts['MLP_linear2']+=1;require(root,z.numel()==1 and t.isfinite(z).all(),'NEW_LOGIT_FINITE',list(z.shape),'finite scalar');result.update(source_kind='new_actual',prediction=int(z.item()>0),logit=float(z.item()))
       outputs.append(result);event(root/'prediction.jsonl',event='CLOSED',key=key,source_kind=result['source_kind']);newmap.setdefault(digest,dict(key=key,x=x[0].clone()))
    require(root,all(not p.requires_grad and p.grad is None for p in m.parameters()),'FROZEN_STATE',False,True);require(root,all(t.equal(v,m.state_dict()[k]) for k,v in a.tensor(item['state_path'],'state',item['state_sha256']).items()),'STATE_UNCHANGED',False,True);path=directory/(tag+'.pt');t.save(dict(keys=keys,H=H,g_select=select,g_read=readout,original_X=origX,original_alpha=original_alpha,X=X,alpha=weights,state_sha256=item['state_sha256'],projection_cache=proj.cache,provenance='071_NOW_MEASURED'),path);geometry.append(dict(path=str(path),sha256=sha(a.data(path,'feature'))));attention_only[tag]=dict(original_alpha=original_alpha,alpha=weights,split_indices={split:[i for i,k in enumerate(keys) if k[2]==split] for split in SPLITS});event(root/'geometry-ledger.jsonl',event='CLOSED',head=tag,cells=400);print('INTERVENTIONS_CLOSED',tag,'MLP',counts['new_MLP'],flush=True)
 require(root,len(outputs)==19200,'LOGICAL_OUTPUT_COUNT',len(outputs),19200);t.save(attention_only,root/'attention-only.pt');save(root/'new-outputs.json',outputs);save(root/'output-seal.json',dict(status='CLOSED',outputs_sha256=sha(a.data(root/'new-outputs.json')),geometry=geometry,attention_file=dict(path=str(root/'attention-only.pt'),sha256=sha(a.data(root/'attention-only.pt','feature'))),input_seal_sha256=sha(a.data(root/'input-seal.json')),logical_cells=19200,counts=counts,orig_complete_answer=0,orig_MLP=0));save(root/'prediction-counts.json',dict(counts=counts,kinds=collections.Counter(x['source_kind'] for x in outputs),full_head=0,original_MLP=0));a.finish();assert not t.cuda.is_initialized()
def quant(values,p):
 v=sorted(values);x=(len(v)-1)*p;i=int(x);return v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
def metrics(ps,ys):
 c=collections.Counter();ds=[]
 for p,y in zip(ps,ys):
  cor=[p[2*v+q]==y[v][q] for v in range(2) for q in range(2)];k=sum(cor);iv=int(p[0]==p[1] and p[2]==p[3]);pattern='CONSTANT' if len(set(p))==1 else 'VIDEO_ONLY' if iv else 'QUESTION_ONLY' if p[0]==p[2] and p[1]==p[3] else 'CHECKERBOARD' if p[0]==p[3] and p[1]==p[2] else 'MIXED';c.update(correct_cells=k,four_way_correct=int(k==4),question_invariant=iv,video_pair_correct=int(cor[0] and cor[2])+int(cor[1] and cor[3]),question_pair_correct=int(cor[0] and cor[1])+int(cor[2] and cor[3]));c['K'+str(k)]+=1;c[pattern]+=1;ds.append((int(k==4),iv))
 return c,ds
def bootstrap(hist,pairs):
 rows=[]
 for split,G in zip(SPLITS,(25,50)):
  rng=random.Random(55072);draws=[rng.choices(range(G),k=G) for _ in range(10000)];rng=random.Random(55073);seeddraws=[rng.choices(range(6),k=6) for _ in range(10000)]
  for arm in ARMS:
   for mode in MODES:
    bins=sorted([x for x in hist if x['head_arm']==arm and x['split']==split and x['condition']==mode],key=lambda x:x['seed_sum']);vector=[x['seed_sum'] for x in bins for _ in range(x['count'])];nets=[next(x['net'] for x in pairs if x['head_arm']==arm and x['split']==split and x['condition']==mode and x['seed']==s) for s in SEEDS];assert len(vector)==G and sum(vector)==sum(nets)
    for axis,samples in [('file_family' if G==25 else 'file_pair',[100*sum(vector[i] for i in d)/300 for d in draws]),('seed',[100*sum(nets[i] for i in d)/300 for d in seeddraws])]:rows.append(dict(head_arm=arm,split=split,condition=mode,axis=axis,status='CLOSED',point_pp=100*sum(nets)/300,lower_pp=quant(samples,.025),upper_pp=quant(samples,.975),draws=10000,planned_draws=10000))
 return rows
def score(root):
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);codecheck(root);a=Access(root,'scoring');j=a.meta(root/'prediction-job.json');require(root,j['active']==j['exit_code']==0,'PREDICTION_JOB',j,'actualactive0exit0');seal=a.meta(root/'output-seal.json');new=a.meta(root/'new-outputs.json',seal['outputs_sha256']);source=a.meta(root/'sources.json');p=Path(source['prior070']);raw=a.meta(p/'new-outputs.json',source['source_output']['files'][0]['sha256']);original=[x for x in raw if x['split'] in SPLITS and x['method'] in ARMS and x['seed'] in SEEDS];require(root,len(original)==9600,'ORIGINAL_COUNT',len(original),9600);old={(x['method'],x['seed'],x['split'],x['index'],x['video'],x['question']):x for x in original};require(root,len(old)==9600 and all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) for x in original),'ORIGINAL_KEYS_STATE',len(old),'9600valid');lookup={tuple(x['key']):x for x in new};require(root,len(lookup)==len(new)==19200,'NEW_KEYS',len(lookup),19200);resolved={};ordinal={tuple(x['key']):i for i,x in enumerate(new)}
 def resolve(k):
  k=tuple(k)
  if k in resolved:return resolved[k]
  x=lookup[k]
  if x['source_kind']=='new_actual':require(root,math.isfinite(x['logit']) and x['prediction']==int(x['logit']>0),'LOGIT_THRESHOLD',x['prediction'],'strict>0');value=x['prediction']
  elif x['source_kind']=='original_alias':
   values={old[tuple(ref)]['prediction'] for ref in x['original_refs']};require(root,len(values)==1,'STOP_IDENTITY_CONFLICT',list(values),'one original answer');value=values.pop()
  else:ref=tuple(x['new_ref']);require(root,ref[:2]==k[:2] and ordinal[ref]<ordinal[k],'ALIAS_CYCLE_OR_STATE',ref,'earlier same-head key');value=resolve(ref)
  resolved[k]=value;return value
 for k in lookup:resolve(k)
 s=source['source_scoring'];expected=s['expected'];ys={SPLITS[0]:[x['labels'] for x in a.meta(Path(s['source_labels_path'])/(SPLITS[0]+'-labels.json'),expected[str((Path(s['source_labels_path'])/(SPLITS[0]+'-labels.json')).resolve())])]};publisher=a.meta(s['raw_publisher']['path'],s['raw_publisher']['sha256']);obs=a.meta(root/'observations.json');grids=[]
 for row,positions in zip(obs[SPLITS[1]],s['raw_publisher']['positions']):
  byvideo={publisher[i]['video']:publisher[i] for i in positions};grid=[]
  for name in row['videos']:
   x=byvideo[name];assert x['candidates']==['First action 1, then action 2','First action 2, then action 1'] and x['answer'] in x['candidates'];y=int(x['answer']==x['candidates'][0]);grid.append([y,1-y])
  grids.append(grid)
 ys[SPLITS[1]]=grids;groups=a.meta(s['groups_path'],expected[str(Path(s['groups_path']).resolve())])['groups'];require(root,len(set(groups[SPLITS[0]]))==25 and all(groups[SPLITS[0]].count(g)==2 for g in set(groups[SPLITS[0]])),'FAMILIES',len(set(groups[SPLITS[0]])),25);save(root/'scoring-labels.json',ys)
 attention_data=a.tensor(seal['attention_file']['path'],expected=seal['attention_file']['sha256']);conditions=[];pairs=[];attention=[];details={};original_table=list(csv.DictReader((Path(__file__).parent.parent/'docs/codex-artifacts/VLM-SEMANTIC-ROLE-FACTOR-070/condition-summary.csv').open(encoding='utf-8-sig')))
 for seed in SEEDS:
  for arm in ARMS:
   g=attention_data[f'{arm}-{seed}']
   for split in SPLITS:
    for mode in CONDITIONS:
     ps=[];counts=collections.Counter()
     for i in range(50):
      values=[]
      for v in range(2):
       for q in range(2):
        if mode=='ORIGINAL_CACHED':values.append(old[arm,seed,split,i,v,q]['prediction']);counts['original_cached']+=1
        else:k=(arm,seed,split,mode,i,v,q);values.append(resolved[k]);counts[lookup[k]['source_kind']]+=1
      ps.append(values)
     c,ds=metrics(ps,ys[split]);row=dict(head_arm=arm,seed=seed,split=split,condition=mode,status='CLOSED',planned_items=50,planned_cells=200,new_actual=counts['new_actual'],original_alias=counts['original_alias'],new_alias=counts['new_alias'],original_cached=counts['original_cached'],CLOSED=200,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,**{k:c[k] for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4','CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')});row.update(cell_accuracy_pct=c['correct_cells']/2,video_pair_accuracy_pct=c['video_pair_correct'],question_pair_accuracy_pct=c['question_pair_correct'],four_way_accuracy_pct=2*c['four_way_correct'],question_invariant_pct=2*c['question_invariant']);conditions.append(row);details[arm,seed,split,mode]=dict(items=ds,pred=ps)
     if mode=='ORIGINAL_CACHED':
      previous=next(x for x in original_table if x['method']==arm and int(x['seed'])==seed and x['split']==split)
      for k in c:assert c[k]==int(previous[k]),('ORIGINAL_REPRODUCTION',k)
      for k in ('cell_accuracy_pct','video_pair_accuracy_pct','question_pair_accuracy_pct','four_way_accuracy_pct','question_invariant_pct'):assert row[k]==float(previous[k])
     else:
      current=ds;baseline=details[arm,seed,split,'ORIGINAL_CACHED'];L=current;B=baseline['items'];lo=sum(x[0]>y[0] for x,y in zip(L,B));ro=sum(x[0]<y[0] for x,y in zip(L,B));iv=sum(x[1]-y[1] for x,y in zip(L,B));changed=sum(x!=y for rowp,rowb in zip(ps,baseline['pred']) for x,y in zip(rowp,rowb));pairs.append(dict(head_arm=arm,seed=seed,split=split,condition=mode,planned_items=50,evaluated_items=50,left_only=lo,right_only=ro,both_correct=sum(x[0] and y[0] for x,y in zip(L,B)),both_wrong=sum(not x[0] and not y[0] for x,y in zip(L,B)),unknown=0,net=lo-ro,delta_four_way_pp=2*(lo-ro),invariant_net=iv,question_invariant_delta_pp=2*iv,changed_cells=changed,changed_pct=changed/2,status='CLOSED'))
      ids=g['split_indices'][split];orig=g['original_alpha'][ids];newalpha=g['alpha'][mode][ids];dist=(newalpha-orig).abs().sum(-1).double().tolist();entropy=lambda w:float(-(torch.where(w>0,w*torch.log(w),torch.zeros_like(w))).sum(-1).double().mean());attention.append(dict(head_arm=arm,seed=seed,split=split,condition=mode,planned_items=50,planned_cells=200,L1_mean=sum(dist)/200,L1_median=quant(dist,.5),L1_p95=quant(dist,.95),original_entropy_mean=entropy(orig),intervention_entropy_mean=entropy(newalpha),changed_cells=changed,changed_pct=changed/2,status='CLOSED'))
 hist=[]
 for split,G,extent in zip(SPLITS,(25,50),(12,6)):
  for arm in ARMS:
   for mode in MODES:
    net=[sum(details[arm,s,split,mode]['items'][i][0]-details[arm,s,split,'ORIGINAL_CACHED']['items'][i][0] for s in SEEDS) for i in range(50)];values=[sum(v for v,gp in zip(net,groups[split]) if gp==family) for family in sorted(set(groups[split]))] if G==25 else net;c=collections.Counter(values);hist.extend(dict(head_arm=arm,split=split,condition=mode,seed_sum=k,count=c[k],status='CLOSED') for k in range(-extent,extent+1))
 save(root/'resolved-new-outputs.json',[dict(x,prediction=resolved[tuple(x['key'])]) for x in new]);save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,attention=attention,histogram=hist,intervals=bootstrap(hist,pairs),conclusion='COMPLETE_FROZEN_SELECTOR_INTERVENTION',disposition='RETROSPECTIVE_DIAGNOSTIC',original_conditions_reproduced=48));a.finish();assert not torch.cuda.is_initialized();print('SCORED28800_ALL_CONDITIONS',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('role',choices=('fixture','prepare','predict','score'));p.add_argument('--root',required=True);args=p.parse_args();root=Path(args.root);CONTEXT.update(stage=args.role,completed=0,remaining='fixed matrix')
 try:globals()[args.role](root)
 except Exception as e:event(root/'stops.jsonl',reason_code=str(e) or type(e).__name__,actual=dict(CONTEXT),limit='sealed071contract',stage=args.role);raise
