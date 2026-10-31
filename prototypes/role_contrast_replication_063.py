"""063 explicit CPU replication roles. No task I/O or model work on import."""
import argparse
from collections import Counter
import copy
import csv
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import random
import statistics
import time
NEW=(137,263,419,557,733,911)
ALL=(19,73)+NEW
SPLITS=('train_pool68','validation11','development54','source_holdout50')
METHODS=('C_NATIVE','D_NATIVE','C_HASH','D_HASH')
def helper(name):
 s=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,sort_keys=True,indent=2);f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(x)+'\n');f.flush();os.fsync(f.fileno())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lfsha(p):return hashlib.sha256(Path(p).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def load(p):
 import torch
 return torch.load(p,map_location='cpu',weights_only=True)
def matrix():return [(s,m) for s in (19,73) for m in ('C_HASH','D_HASH')]+[(s,m) for s in NEW for m in ('C_NATIVE','D_NATIVE')]
def content_order(v):
 rows=[v[i].contiguous().numpy().astype('<f4',copy=False).tobytes() for i in range(6)]
 return sorted(range(6),key=lambda i:(hashlib.sha256(rows[i]).digest(),rows[i]))
def check_code(root):
 for x in read(Path(root)/'code-seal.json')['files']:assert lfsha(x['path'])==x['lf_sha256']
def prepare(root,prior):
 t=cpu();root=Path(root);prior=Path(prior);old=read(prior/'old-assets.json');base=Path(old['prior']);expected={};assets={};cache={}
 for n in ('input-seal.json','output-seal.json'):
  for x in read(prior/n)['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 for n in ('pre-consumption-seal.json','outputs-identity-seal.json'):
  for x in read(base/n)['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 for x in old['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 def data(p,kind='metadata'):
  p=Path(p);key=str(p.resolve())
  if key not in cache:
   b=p.read_bytes();h=hashlib.sha256(b).hexdigest();assert key not in expected or expected[key]==h;cache[key]=b;assets[key]=dict(path=key,sha256=h,bytes=len(b),kind=kind)
  return cache[key]
 def meta(p):return json.loads(data(p).decode('utf-8-sig'))
 def tensor(p,kind='feature'):return t.load(io.BytesIO(data(p,kind)),map_location='cpu',weights_only=True)
 assert meta(prior/'parent-closed.json')['push']=='SUCCEEDED'
 for n in ('training','prediction','scoring'):
  j=meta(prior/(n+'-job.json'));assert j['active']==j['exit_code']==0
 for n in ('input-seal.json','output-seal.json','old-assets.json'):meta(prior/n)
 index=meta(prior/'feature-index.json');assert len(index['video'])==366 and len(index['text'])==220
 bindings=meta(base/'data-bindings.json');pools=bindings['pools'];assert [len(pools[s]) for s in SPLITS]==[68,11,54,50]
 groups=[{r['group_key'] for r in pools[s]} for s in SPLITS];assert list(map(len,groups))==[25,4,20,25] and all(not a&b for i,a in enumerate(groups) for b in groups[i+1:])
 for split in SPLITS:
  obs=meta(prior/(split+'-observations.json'));labels=meta(base/(split+'-labels.json'));assert len(obs)==len(labels)==len(pools[split])
  for i,(o,l,p) in enumerate(zip(obs,labels,pools[split])):
   assert o==dict(index=i,videos=p['videos'],questions=p['questions']) and l==dict(index=i,labels=p['labels']);a,b=l['labels'][0];c,d=l['labels'][1];assert a==d and b==c and a+b==1
  save(root/(split+'-observations.json'),obs)
 save(root/'train-labels.json',meta(prior/'train-labels.json'));save(root/'scoring-bindings.json',meta(prior/'scoring-bindings.json'))
 views=tensor(prior/'views.pt','view');trainviews=tensor(prior/'train-views.pt','view');stats=tensor(prior/'normalizer.pt','view');tb=meta(prior/'transform-bindings.json');train=tb['train'];rawh={q:tensor(r['path']) for q,r in index['text'].items()};assert all(v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all() for v in rawh.values());h={q:v.double() for q,v in rawh.items()};u=helper('question_role_contrast_062');assert len(train)==84 and train==sorted(set(train),key=lambda q:q.encode()) and {u.tau(q) for q in train}==set(train)
 assert all(tb['anchors'][q]==u.anchor(q,train) for q in h)
 for arm in ('C_CENTER','D_ROLE'):
  raw={q:h[q] if arm=='C_CENTER' else (h[q]-h[u.tau(q)])/2 for q in h};z=t.stack([raw[q] for q in train]);mu=z.mean(0);scale=(z-mu).square().mean().sqrt();assert t.equal(mu,stats[arm]['mu']) and t.equal(scale,stats[arm]['scale']) and scale>1e-8
  for q in h:assert t.equal(((raw[q]-mu)/scale).float(),views[arm][q])
  assert all(t.equal(views[arm][q],trainviews[arm][q]) for q in train)
 t.save({a:views[a] for a in ('C_CENTER','D_ROLE')},root/'views.pt');t.save({a:trainviews[a] for a in ('C_CENTER','D_ROLE')},root/'train-views.pt')
 permutations=((5,4,3,2,1,0),(1,2,3,4,5,0),(2,5,1,4,0,3),(0,2,4,1,3,5));orders={};changed=0
 for name,r in index['video'].items():
  v=tensor(r['path']);assert v.dtype==t.float32 and v.shape==(6,2560) and t.isfinite(v).all() and Path(r['path']).stat().st_size<=2*1024**2
  order=content_order(v);sortedv=v[order];orders[name]=order;changed+=not t.equal(v,sortedv);assert sorted(order)==list(range(6)) and t.equal(sortedv,sortedv[content_order(sortedv)])
  for perm in permutations:
   w=v[list(perm)];assert t.equal(sortedv,w[content_order(w)])
 assert changed>0;save(root/'hash-orders.json',dict(orders=orders,changed=changed,total=366,permutations=permutations))
 head=helper('question_temporal_056')
 for seed in ALL:
  if seed in (19,73):p=tensor(prior/f'plan-{seed}.pt','plan')
  else:
   t.manual_seed(seed);model=head.TemporalHead(2560,2560);p=dict(state=copy.deepcopy(model.state_dict()),sequence=t.randint(68,(250,8),generator=t.Generator().manual_seed(seed)));del model
  assert p['sequence'].shape==(250,8) and len(t.unique(p['sequence']))==68;t.save(p,root/f'plan-{seed}.pt')
 save(root/'feature-index.json',index);save(root/'old-assets.json',dict(files=list(assets.values()),prior062=str(prior),prior060=str(base),logical_bytes_by_kind={k:sum(x['bytes'] for x in assets.values() if x['kind']==k) for k in ('feature','view','plan','metadata')}))
 save(root/'preparation-closed.json',dict(hash_changed=changed,video_inputs=366,questions=220,train_questions=84,normalizer='VERIFIED_FROZEN_062_NOT_REFIT',cuda_initialized=t.cuda.is_initialized()))
 print('PREPARED_FROZEN_VIEWS_HASH_PLANS',changed,flush=True)
def freeze(root):
 root=Path(root);assert not (root/'training').exists();paths=[Path(__file__),Path(__file__).with_name('question_role_contrast_062.py'),Path(__file__).with_name('question_temporal_056.py'),Path(__file__).with_name('auditable_runner_040.py'),root/'supervise.py',root/'review.py']
 save(root/'code-seal.json',dict(files=[dict(path=str(p),lf_sha256=lfsha(p)) for p in paths],at_unix=time.time()))
 save(root/'input-seal.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in root.iterdir() if p.is_file() and p.suffix in ('.json','.pt','.py')],matrix=matrix(),gates=dict(positive_seeds=5,mean_net=4,mean_D=10,mean_Q_reduction=10,D_order_each=2,interaction_each=1),bootstrap=[55063,55064,10000],planned=[4000,11712,3128,14840,81,14,2,350,34],at_unix=time.time()));print('FULL_CODE_INPUT_SEAL_CLOSED',flush=True)
def train(root):
 t=cpu();root=Path(root);check_code(root);head=helper('question_temporal_056');index=read(root/'feature-index.json');obs=read(root/(SPLITS[0]+'-observations.json'));views=load(root/'train-views.pt');orders=read(root/'hash-orders.json')['orders'];V=t.stack([t.stack([load(index['video'][n]['path']) for n in r['videos']]) for r in obs]);VH=t.stack([t.stack([load(index['video'][n]['path'])[orders[n]] for n in r['videos']]) for r in obs]);y=t.tensor([r['labels'] for r in read(root/'train-labels.json')],dtype=t.float32);directory=root/'training';directory.mkdir()
 for seed,method in matrix():
  p=load(root/f'plan-{seed}.pt');d=directory/f'{method}-{seed}';d.mkdir();j=d/'steps.jsonl';event(j,event='STARTED',at_unix=time.time());model=head.TemporalHead(2560,2560);model.load_state_dict(p['state']);t.save(model.state_dict(),d/'initial.pt');opt=head.optimizer(model);Q=t.stack([t.stack([views['C_CENTER' if method[0]=='C' else 'D_ROLE'][q] for q in r['questions']]) for r in obs]);visual=VH if method.endswith('HASH') else V
  for step,ids in enumerate(p['sequence']):
   event(j,event='STEP_STARTED',step=step);v,q=head.pack(visual,Q,ids);z=model(v,q).reshape(8,2,2);loss=t.nn.functional.softplus(-(2*y[ids]-1)*z).mean();assert t.isfinite(loss);opt.zero_grad(set_to_none=True);loss.backward();assert all(p.grad is not None and t.isfinite(p.grad).all() for p in model.parameters());t.nn.utils.clip_grad_norm_(model.parameters(),1);opt.step();event(j,event='STEP_CLOSED',step=step,loss=float(loss.detach()))
  t.save(model.state_dict(),d/'final.pt');event(j,event='CLOSED',steps=250);print('TRAIN_CLOSED',seed,method,flush=True)
def predict(root):
 t=cpu();root=Path(root);check_code(root);assert read(root/'training-job.json')['active']==read(root/'training-job.json')['exit_code']==0;head=helper('question_temporal_056');index=read(root/'feature-index.json');V={n:load(r['path']) for n,r in index['video'].items()};views=load(root/'views.pt');orders=read(root/'hash-orders.json')['orders'];outputs=[]
 for seed,method in matrix():
  model=head.TemporalHead(2560,2560);model.load_state_dict(load(root/'training'/f'{method}-{seed}'/'final.pt'))
  for split in SPLITS:
   for r in read(root/(split+'-observations.json')):
    for vi,n in enumerate(r['videos']):
     v=V[n][orders[n]] if method.endswith('HASH') else V[n]
     for qi,q in enumerate(r['questions']):
      key=[method,seed,split,r['index'],vi,qi];event(root/'prediction.jsonl',event='STARTED',key=key);p=int(head.predict(model,v,views['C_CENTER' if method[0]=='C' else 'D_ROLE'][q]));outputs.append(dict(method=method,seed=seed,split=split,index=r['index'],video=vi,question=qi,prediction=p,status='CLOSED',phase='NEW_063'));event(root/'prediction.jsonl',event='CLOSED',key=key)
 assert len(outputs)==11712;save(root/'new-outputs.json',outputs);save(root/'output-seal.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [root/'new-outputs.json',root/'code-seal.json',root/'input-seal.json',root/'views.pt',root/'hash-orders.json']+list((root/'training').glob('*/*.pt'))]));print('OUTPUTS_SEALED_11712',flush=True)
def quantile(v,p):
 v=sorted(v);x=(len(v)-1)*p;i=int(x);return v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
def metrics(outputs,labels,groups):
 u=helper('question_role_contrast_062');lookup={(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question']):r for r in outputs};assert len(lookup)==14840;conditions=[];details={}
 for split,n in zip(SPLITS,(68,11,54,50)):
  for method,seed in [(m,s) for s in ALL for m in ('C_NATIVE','D_NATIVE')]+[(m,s) for s in (19,73) for m in ('C_HASH','D_HASH')]+([('B0','NA')] if split==SPLITS[3] else []):
   row=dict(method=method,seed=seed,split=split,phase='CACHED_062' if method=='B0' or method.endswith('NATIVE') and seed in (19,73) else 'NEW_063',n_instances=n,n_cells=4*n,complete_cells=4*n,valid_cells=4*n,invalid_cells=0,failed_cells=0,not_run_cells=0,unknown_cells=0,correct_cells=0,video_pair_correct=0,question_pair_correct=0,four_way_correct=0,question_invariant=0,status='COMPLETE',**{k:0 for k in u.KINDS},**{'K'+str(k):0 for k in range(5)});detail=[]
   for i in range(n):
    rs=[lookup[(method,seed,split,i,v,q)] for v in (0,1) for q in (0,1)];assert all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) for x in rs);p=[x['prediction'] for x in rs];gold=sum(labels[split][i]['labels'],[]);c=[int(a==b) for a,b in zip(p,gold)];k=sum(c);typ=u.kind(p);inv=int(typ in ('CONSTANT','VIDEO_ONLY'));row[typ]+=1;row['K'+str(k)]+=1;row['correct_cells']+=k;row['four_way_correct']+=int(k==4);row['question_invariant']+=inv;row['video_pair_correct']+=c[0]*c[2]+c[1]*c[3];row['question_pair_correct']+=c[0]*c[1]+c[2]*c[3];detail.append(dict(four=int(k==4),inv=inv))
   row['cached_cells']=4*n if row['phase']=='CACHED_062' else 0;row['new_cells']=4*n-row['cached_cells']
   for key,count,den in [('item_accuracy','correct_cells',4*n),('video_pair_accuracy','video_pair_correct',2*n),('question_pair_accuracy','question_pair_correct',2*n),('four_way_accuracy','four_way_correct',n),('question_invariant_rate','question_invariant',n)]:row[key]=row[count]/den
   conditions.append(row);details[(method,seed,split)]=detail
 keys=sorted(set(groups));assert len(keys)==25 and all(groups.count(k)==2 for k in keys);rng=random.Random(55063);draws=[rng.choices(range(25),k=25) for _ in range(10000)];paired=[];profile=[];vectors={}
 configurations=[(s,'D_NATIVE','C_NATIVE') for s in ALL]+[(s,l,r) for s in (19,73) for l,r in [('D_HASH','C_HASH'),('D_NATIVE','D_HASH'),('C_NATIVE','C_HASH')]]
 for seed,left,right in configurations:
  L=details[(left,seed,SPLITS[3])];R=details[(right,seed,SPLITS[3])];gs=[]
  for j,key in enumerate(keys,1):
   ids=[i for i,k in enumerate(groups) if k==key];g=dict(family=f'F{j:02}',seed=seed,left=left,right=right,n=2,left_only=0,right_only=0,both_correct=0,both_wrong=0,unknown=0,left_question_invariant=0,right_question_invariant=0)
   for i in ids:
    a,b=L[i]['four'],R[i]['four'];g['left_only' if a and not b else 'right_only' if b and not a else 'both_correct' if a else 'both_wrong']+=1;g['left_question_invariant']+=L[i]['inv'];g['right_question_invariant']+=R[i]['inv']
   gs.append(g);profile.append(g)
  row=dict(seed=seed,left=left,right=right,n=50,**{k:sum(g[k] for g in gs) for k in ('left_only','right_only','both_correct','both_wrong','unknown','left_question_invariant','right_question_invariant')});row['net']=row['left_only']-row['right_only'];row['delta_four_way_pp']=row['net']*2;row['question_invariant_delta_pp']=2*(row['left_question_invariant']-row['right_question_invariant'])
  for metric,f in [('answer',lambda g:g['left_only']-g['right_only']),('question_invariant',lambda g:g['left_question_invariant']-g['right_question_invariant'])]:
   v=[f(g) for g in gs];vectors[(seed,left,right,metric)]=v;samples=[100*sum(v[k] for k in draw)/(2*len(draw)) for draw in draws]
   row[metric+'_ci_low_pp']=quantile(samples,.025);row[metric+'_ci_high_pp']=quantile(samples,.975)
  paired.append(row)
 interactions=[];extra=[]
 for seed in (19,73):
  v=[a-b for a,b in zip(vectors[(seed,'D_NATIVE','C_NATIVE','answer')],vectors[(seed,'D_HASH','C_HASH','answer')])];samples=[2*sum(v[k] for k in draw) for draw in draws];interactions.append(dict(seed=seed,net_instances=sum(v),delta_pp=2*sum(v),ci_low_pp=quantile(samples,.025),ci_high_pp=quantile(samples,.975)))
 for metric in ('answer','question_invariant'):
  vs=[vectors[(s,'D_NATIVE','C_NATIVE',metric)] for s in NEW];sample=[sum(2*sum(v[k] for k in draw) for v in vs)/6 for draw in draws];extra.append(dict(kind='new_six_family',metric=metric,estimate_pp=sum(map(sum,vs))*2/6,ci_low_pp=quantile(sample,.025),ci_high_pp=quantile(sample,.975)))
 srng=random.Random(55064);sd=[srng.choices(range(6),k=6) for _ in range(10000)]
 for metric in ('answer','question_invariant'):
  v=[sum(vectors[(s,'D_NATIVE','C_NATIVE',metric)])*2 for s in NEW];sample=[sum(v[k] for k in draw)/6 for draw in sd];extra.append(dict(kind='new_six_seed',metric=metric,estimate_pp=sum(v)/6,ci_low_pp=quantile(sample,.025),ci_high_pp=quantile(sample,.975)))
 seed_summary=[]
 for seed in ALL:
  for split in (SPLITS[2],SPLITS[3]):
   c=details[('C_NATIVE',seed,split)];d=details[('D_NATIVE',seed,split)];seed_summary.append(dict(seed=seed,split=split,C_correct=sum(x['four'] for x in c),D_correct=sum(x['four'] for x in d),net=sum(x['four'] for x in d)-sum(x['four'] for x in c),C_question_invariant=sum(x['inv'] for x in c),D_question_invariant=sum(x['inv'] for x in d)))
 aggregates=[]
 for selected,name in [(NEW,'NEW_SIX'),(ALL,'ALL_EIGHT_DESCRIPTIVE')]:
  for split in (SPLITS[2],SPLITS[3]):
   rows=[r for r in seed_summary if r['seed'] in selected and r['split']==split];a=dict(group=name,split=split,n_seeds=len(rows))
   for k in ('C_correct','D_correct','net','C_question_invariant','D_question_invariant'):
    values=[r[k] for r in rows];a[k]=dict(mean=statistics.mean(values),median=statistics.median(values),min=min(values),max=max(values))
   aggregates.append(a)
 new=[r for r in seed_summary if r['seed'] in NEW and r['split']==SPLITS[3]];stability=sum(r['net']>0 for r in new)>=5 and statistics.mean(r['net'] for r in new)>=4 and statistics.mean(r['D_correct'] for r in new)>=10 and statistics.mean(r['C_question_invariant']-r['D_question_invariant'] for r in new)>=10
 order=all(next(r for r in paired if (r['seed'],r['left'],r['right'])==(seed,'D_NATIVE','D_HASH'))['net']>=2 for seed in (19,73));interaction=all(r['net_instances']>=1 for r in interactions)
 return dict(conditions=conditions,paired=paired,source_profile=profile,interactions=interactions,extra_intervals=extra,seed_summary=seed_summary,seed_aggregates=aggregates,stability_gate=stability,D_order_gate=order,interaction_gate=interaction,status='ROLE_CONTRAST_MULTI_SEED_DEVELOPMENT_SIGNAL' if stability else 'NOT_ROBUST_UNDER_FIXED_REPLICATION_GATE',explicit_order_status='EXPLICIT_ORDER_INTERACTION_DEVELOPMENT_SIGNAL' if stability and order and interaction else 'NOT_SUPPORTED_BY_ALL_THREE_GATES')
def score(root):
 root=Path(root);check_code(root);assert all(read(root/(n+'-job.json'))['active']==read(root/(n+'-job.json'))['exit_code']==0 for n in ('training','prediction'))
 for x in read(root/'output-seal.json')['files']:assert sha(x['path'])==x['sha256']
 a=read(root/'old-assets.json');prior=Path(a['prior062']);base=Path(a['prior060']);p=prior/'all-outputs.json';expected=read(prior/'scoring-summary.json')
 #062 all-outputs was created during scoring; its closure is checked with its
 #cached condition metrics and an exclusive current receipt, not retro-sealed.
 old=[]
 for r in read(p):
  if r['method'] not in ('C_CENTER','D_ROLE','B0'):continue
  old.append(dict(r,method={'C_CENTER':'C_NATIVE','D_ROLE':'D_NATIVE','B0':'B0'}[r['method']],phase='CACHED_062'))
 sealed_new=prior/'new-outputs.json';assert sha(sealed_new)==next(x['sha256'] for x in read(prior/'output-seal.json')['files'] if Path(x['path']).resolve()==sealed_new.resolve());authoritative={(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question']):r for r in read(sealed_new)}
 for r in old:
  if r['method']!='B0':assert r['prediction']==authoritative[('C_CENTER' if r['method']=='C_NATIVE' else 'D_ROLE',r['seed'],r['split'],r['index'],r['video'],r['question'])]['prediction']
 assert len(old)==3128;save(root/'cache-read-seal.json',dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size));outputs=read(root/'new-outputs.json')+old;save(root/'all-outputs.json',outputs);labels={s:read(base/(s+'-labels.json')) for s in SPLITS};result=metrics(outputs,labels,read(root/'scoring-bindings.json')['groups'][SPLITS[3]])
 for row in result['conditions']:
  if row['phase']=='CACHED_062':
   m={'C_NATIVE':'C_CENTER','D_NATIVE':'D_ROLE','B0':'B0'}[row['method']];x=next(x for x in expected['conditions'] if (x['method'],x['seed'],x['split'])==(m,row['seed'],row['split']));assert all(row[k]==x[k] for k in ('n_cells','correct_cells','video_pair_correct','question_pair_correct','four_way_correct','question_invariant','K0','K1','K2','K3','K4'))
 for name,key in [('condition-summary.csv','conditions'),('paired-summary.csv','paired')]:
  with open(root/name,'x',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(result[key][0]));w.writeheader();w.writerows(result[key])
 save(root/'scoring-summary.json',result);print('SCORE_CLOSED',result['status'],result['D_order_gate'],result['interaction_gate'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('prepare','freeze','train','predict','score'));p.add_argument('--root',required=True);p.add_argument('--prior');a=p.parse_args()
 if a.phase=='prepare':prepare(a.root,a.prior)
 else:globals()[a.phase](a.root)
