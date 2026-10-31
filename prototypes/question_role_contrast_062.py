"""Explicit062 CPU roles. Import does not read task data or run models."""
import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import io
import itertools
import json
import os
from pathlib import Path
import random
import re
import time
SPLITS=('train_pool68','validation11','development54','source_holdout50')
ARMS=('C_CENTER','D_ROLE','N_UNMATCHED')
KINDS=('CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,indent=2,sort_keys=True);f.flush();os.fsync(f.fileno())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def codesha():return hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(x)+'\n');f.flush();os.fsync(f.fileno())
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized()
 return torch
def head():
 s=importlib.util.spec_from_file_location('head056',Path(__file__).with_name('question_temporal_056.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def load(p):
 import torch
 return torch.load(p,map_location='cpu',weights_only=True)
def tau(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 if not m:raise ValueError('QUESTION_PARSE')
 return f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.'
def anchor(q,train):
 k=int.from_bytes(hashlib.sha256(b'VLM062/anchor/'+q.encode('utf-8')).digest()[:8],'big')%84
 return next(train[(k+i)%84] for i in range(84) if train[(k+i)%84] not in (q,tau(q)))
def kind(p):
 a,b,c,d=p
 return 'CONSTANT' if a==b==c==d else 'VIDEO_ONLY' if a==b and c==d else 'QUESTION_ONLY' if a==c and b==d else 'CHECKERBOARD' if a==d and b==c else 'MIXED'
def prepare(root,prior,audit):
 t=cpu();root=Path(root);prior=Path(prior);audit=Path(audit);assets={};meta=feature=plansbytes=0
 expected={}
 for name in ('outputs-identity-seal.json','pre-consumption-seal.json'):
  for x in read(prior/name)['files']:expected[str(Path(x['path']).resolve())]=x['sha256']
 known={x['path']:x['sha256'] for x in read(audit/'access-manifest.json')['files']}
 def record(p,category='meta'):
  nonlocal meta,feature,plansbytes
  p=Path(p);k=str(p.resolve());h=sha(p);n=p.stat().st_size
  if k in expected:assert expected[k]==h
  if k in known:assert known[k]==h
  assets[k]=dict(path=k,sha256=h,bytes=n,category=category)
  if category=='feature':assert n<=2*1024**2;feature+=n
  elif category=='plan':assert n<=4*1024**2;plansbytes+=n
  else:meta+=n
  return p
 for p in (prior,audit):assert read(record(p/'parent-closed.json'))['push']=='SUCCEEDED'
 assert read(record(prior/'training-job.json'))['active']==read(record(prior/'prediction-job.json'))['active']==0
 for n in ('outputs-identity-seal.json','pre-consumption-seal.json','training-config.json'):record(prior/n)
 for n in ('audit-summary.json','analysis-plan.json','access-manifest.json'):record(audit/n)
 bindings=read(record(prior/'data-bindings.json'));pools=bindings['pools'];assert [len(pools[s]) for s in SPLITS]==[68,11,54,50]
 groups=[{x['group_key'] for x in pools[s]} for s in SPLITS];assert list(map(len,groups))==[25,4,20,25] and all(not a&b for i,a in enumerate(groups) for b in groups[i+1:])
 obs={s:read(record(prior/(s+'-observations.json'))) for s in SPLITS}
 for s in SPLITS:
  labels=read(record(prior/(s+'-labels.json')))
  for i,(r,l,o) in enumerate(zip(pools[s],labels,obs[s])):
   assert o==dict(index=i,videos=r['videos'],questions=r['questions']) and l==dict(index=i,labels=r['labels'])
   a,b=l['labels'][0];c,d=l['labels'][1];assert a==d and b==c and a+b==1
  save(root/(s+'-observations.json'),obs[s])
 save(root/'train-labels.json',[dict(index=i,labels=r['labels']) for i,r in enumerate(pools[SPLITS[0]])])
 index=read(record(prior/'feature-index.json'));assert len(index['video'])==366 and len(index['text'])==220
 values={}
 for k,shape in [('video',(6,2560)),('text',(2560,))]:
  values[k]={}
  for name,r in index[k].items():
   v=load(record(r['path'],'feature'));assert tuple(v.shape)==shape and v.dtype==t.float32 and t.isfinite(v).all();values[k][name]=v
 train=sorted({q for r in obs[SPLITS[0]] for q in r['questions']},key=lambda x:x.encode('utf-8'));assert len(train)==84 and {tau(q) for q in train}==set(train)
 h=values['text'];assert all(tau(q) in h and tau(tau(q))==q for q in h)
 views={};stats={};anchors={q:anchor(q,train) for q in h}
 for arm in ARMS:
  raw={q:h[q].double() if arm=='C_CENTER' else (h[q].double()-h[tau(q) if arm=='D_ROLE' else anchors[q]].double())/2 for q in h}
  z=t.stack([raw[q] for q in train]);mu=z.mean(0);scale=(z-mu).square().mean().sqrt();assert t.isfinite(scale) and scale>1e-8
  views[arm]={q:((v-mu)/scale).float() for q,v in raw.items()};stats[arm]=dict(mu=mu,scale=scale)
  norm=t.stack([views[arm][q].double() for q in train]);assert norm.mean(0).abs().max()<1e-6 and abs(float(norm.square().mean())-1)<1e-6
  assert any(not t.equal(views[arm][q],h[q]) for q in h)
  if arm=='D_ROLE':assert all(t.equal(raw[q],-raw[tau(q)]) for q in h)
 for seed in (19,73):
  p=record(prior/f'plan-{seed}.pt','plan');v=load(p);assert t.equal(v['sequence'],t.randint(68,(250,8),generator=t.Generator().manual_seed(seed))) and len(t.unique(v['sequence']))==68
  model=head().TemporalHead(2560,2560);model.load_state_dict(v['A']);assert sum(p.numel() for p in model.parameters())==356673
  t.save(dict(state=v['A'],sequence=v['sequence']),root/f'plan-{seed}.pt')
 t.save(views,root/'views.pt');t.save(stats,root/'normalizer.pt')
 t.save({arm:{q:views[arm][q] for q in train} for arm in ARMS},root/'train-views.pt')
 def pair(q):
  m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);return tuple(' '.join(x.replace('_',' ').split()).casefold() for x in m.groups())
 ep={x for q in train for x in pair(q)};pp={tuple(sorted(pair(q))) for q in train}
 def coverage(q):
  a,b=pair(q);n=int(a in ep)+int(b in ep);return 'PAIR_SEEN' if tuple(sorted((a,b))) in pp else 'BOTH_EVENTS_SEEN_PAIR_NEW' if n==2 else 'ONE_EVENT_SEEN' if n==1 else 'NO_EVENT_SEEN'
 subsets={s:[coverage(r['questions'][0]) for r in obs[s]] for s in SPLITS};assert Counter(subsets[SPLITS[2]])==dict(PAIR_SEEN=28,BOTH_EVENTS_SEEN_PAIR_NEW=19,ONE_EVENT_SEEN=7) and Counter(subsets[SPLITS[3]])==dict(NO_EVENT_SEEN=50)
 save(root/'scoring-bindings.json',dict(groups={s:[r['group_key'] for r in pools[s]] for s in SPLITS},subsets=subsets))
 save(root/'transform-bindings.json',dict(train=train,anchors=anchors))
 save(root/'feature-index.json',index)
 record(Path(__file__).with_name('question_temporal_056.py'))
 assert feature<=256*1024**2 and meta<=32*1024**2
 save(root/'old-assets.json',dict(files=list(assets.values()),metadata_bytes=meta,feature_bytes=feature,plan_bytes=plansbytes,prior=str(prior),audit=str(audit)))
 save(root/'input-seal.json',dict(code_sha256=codesha(),files=[dict(path=str(p),sha256=sha(p)) for p in root.iterdir() if p.is_file() and p.suffix in ('.json','.pt')],steps=1500,new_predictions=4392,total=6056,answer_gate=[10,3,2],response_gate=10,bootstrap=[55062,10000],at_unix=time.time()))
 print('PREPARATION_SEALED',flush=True)
def train(root):
 t=cpu();root=Path(root);assert codesha()==read(root/'input-seal.json')['code_sha256'];h=head();index=read(root/'feature-index.json');obs=read(root/(SPLITS[0]+'-observations.json'));views=load(root/'train-views.pt')
 V=t.stack([t.stack([load(index['video'][n]['path']) for n in r['videos']]) for r in obs]);y=t.tensor([r['labels'] for r in read(root/'train-labels.json')],dtype=t.float32);directory=root/'training';directory.mkdir()
 for seed in (19,73):
  plan=load(root/f'plan-{seed}.pt')
  for arm in ARMS:
   d=directory/f'{arm}-{seed}';d.mkdir();journal=d/'steps.jsonl';event(journal,event='STARTED');model=h.TemporalHead(2560,2560);model.load_state_dict(plan['state']);t.save(model.state_dict(),d/'initial.pt');opt=h.optimizer(model);Q=t.stack([t.stack([views[arm][q] for q in r['questions']]) for r in obs])
   for step,ids in enumerate(plan['sequence']):
    event(journal,event='STEP_STARTED',step=step);v,q=h.pack(V,Q,ids);z=model(v,q).reshape(8,2,2);loss=t.nn.functional.softplus(-(2*y[ids]-1)*z).mean();assert t.isfinite(loss);opt.zero_grad(set_to_none=True);loss.backward();assert all(p.grad is not None and t.isfinite(p.grad).all() for p in model.parameters());t.nn.utils.clip_grad_norm_(model.parameters(),1);opt.step();event(journal,event='STEP_CLOSED',step=step,loss=float(loss.detach()))
   t.save(model.state_dict(),d/'final.pt');event(journal,event='CLOSED',steps=250);print('TRAIN_CLOSED',arm,seed,flush=True)
def predict(root):
 t=cpu();root=Path(root);assert read(root/'training-job.json')['active']==0 and codesha()==read(root/'input-seal.json')['code_sha256'];h=head();index=read(root/'feature-index.json');views=load(root/'views.pt');V={n:load(r['path']) for n,r in index['video'].items()};outputs=[]
 for seed in (19,73):
  for arm in ARMS:
   model=h.TemporalHead(2560,2560);model.load_state_dict(load(root/'training'/f'{arm}-{seed}'/'final.pt'))
   for split in SPLITS:
    for r in read(root/(split+'-observations.json')):
     for vi,n in enumerate(r['videos']):
      for qi,q in enumerate(r['questions']):
       key=[arm,seed,split,r['index'],vi,qi];event(root/'prediction.jsonl',event='STARTED',key=key);p=int(h.predict(model,V[n],views[arm][q]));o=dict(method=arm,seed=seed,split=split,index=r['index'],video=vi,question=qi,prediction=p,status='CLOSED',origin='NEW');outputs.append(o);event(root/'prediction.jsonl',event='CLOSED',key=key)
 assert len(outputs)==4392;save(root/'new-outputs.json',outputs);save(root/'output-seal.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in [root/'new-outputs.json',root/'views.pt',root/'normalizer.pt',root/'input-seal.json']+list((root/'training').glob('*/*.pt'))],code_sha256=codesha()));print('OUTPUTS_SEALED_4392',flush=True)
def tables(outputs,labels,bindings):
 lookup={(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question']):r for r in outputs};assert len(lookup)==6056
 conditions=[];details={};subsets=[]
 for split,n in zip(SPLITS,(68,11,54,50)):
  for arm,seed in [(m,s) for m in ('A68_CACHED',)+ARMS for s in (19,73)]+([('B0','NA')] if n==50 else []):
   row=dict(method=arm,seed=seed,split=split,n_instances=n,n_cells=4*n,cached_cells=0,new_cells=0,complete_cells=0,valid_cells=0,invalid_cells=0,failed_cells=0,not_run_cells=0,unknown_cells=0,correct_cells=0,video_pair_correct=0,question_pair_correct=0,four_way_correct=0,question_invariant=0,status='COMPLETE',**{k:0 for k in KINDS},**{'K'+str(i):0 for i in range(5)});detail=[]
   for i in range(n):
    cells=[lookup[(arm,seed,split,i,v,q)] for v in (0,1) for q in (0,1)];assert all(r['status']=='CLOSED' and r['prediction'] in (0,1) for r in cells);p=[r['prediction'] for r in cells];gold=sum(labels[split][i]['labels'],[]);c=[int(a==b) for a,b in zip(p,gold)];k=sum(c);typ=kind(p);inv=int(typ in ('CONSTANT','VIDEO_ONLY'));row[typ]+=1;row['K'+str(k)]+=1;row['question_invariant']+=inv;row['correct_cells']+=k;row['four_way_correct']+=int(k==4);row['video_pair_correct']+=c[0]*c[2]+c[1]*c[3];row['question_pair_correct']+=c[0]*c[1]+c[2]*c[3];row['cached_cells']+=sum(r['origin']=='CACHED' for r in cells);row['new_cells']+=sum(r['origin']=='NEW' for r in cells);detail.append(dict(correct=k,four=int(k==4),inv=inv))
   row['valid_cells']=row['complete_cells']=4*n
   for k,den in [('item_accuracy',4*n),('video_pair_accuracy',2*n),('question_pair_accuracy',2*n),('four_way_accuracy',n),('question_invariant_rate',n)]:row[k]=row[dict(item_accuracy='correct_cells',video_pair_accuracy='video_pair_correct',question_pair_accuracy='question_pair_correct',four_way_accuracy='four_way_correct',question_invariant_rate='question_invariant')[k]]/den
   conditions.append(row);details[(arm,seed,split)]=detail
   if split==SPLITS[2]:
    for layer in ('PAIR_SEEN','BOTH_EVENTS_SEEN_PAIR_NEW','ONE_EVENT_SEEN','NO_EVENT_SEEN'):
     chosen=[v for i,v in enumerate(detail) if bindings['subsets'][split][i]==layer];nsub=len(chosen);s=dict(method=arm,seed=seed,subset=layer,n_instances=nsub,correct_cells=sum(x['correct'] for x in chosen),four_way_correct=sum(x['four'] for x in chosen),question_invariant=sum(x['inv'] for x in chosen),status='COMPLETE' if chosen else 'EMPTY');s.update(item_accuracy=s['correct_cells']/(4*nsub) if nsub else 'NA',four_way_accuracy=s['four_way_correct']/nsub if nsub else 'NA',question_invariant_rate=s['question_invariant']/nsub if nsub else 'NA');subsets.append(s)
 groups=bindings['groups'][SPLITS[3]];keys=sorted(set(groups));profile=[];paired=[];rng=random.Random(55062);draws=[rng.choices(range(25),k=25) for _ in range(10000)]
 for seed in (19,73):
  for comp in ('C_CENTER','N_UNMATCHED','A68_CACHED','B0'):
   L=details[('D_ROLE',seed,SPLITS[3])];R=details[(comp,'NA' if comp=='B0' else seed,SPLITS[3])];stats=[]
   for number,key in enumerate(keys,1):
    ids=[i for i,g in enumerate(groups) if g==key];g=dict(family=f'F{number:02}',seed=seed,left='D_ROLE',right=comp,n=2,left_only=0,right_only=0,both_correct=0,both_wrong=0,unknown=0,left_question_invariant=0,right_question_invariant=0)
    for i in ids:
     a,b=L[i]['four'],R[i]['four'];g['left_only' if a and not b else 'right_only' if b and not a else 'both_correct' if a else 'both_wrong']+=1;g['left_question_invariant']+=L[i]['inv'];g['right_question_invariant']+=R[i]['inv']
    stats.append(g);profile.append(g)
   row=dict(seed=seed,left='D_ROLE',right=comp,n=50,**{k:sum(g[k] for g in stats) for k in ('left_only','right_only','both_correct','both_wrong','unknown','left_question_invariant','right_question_invariant')});row['net']=row['left_only']-row['right_only'];row['delta_four_way_pp']=2*row['net'];row['question_invariant_delta_pp']=2*(row['left_question_invariant']-row['right_question_invariant'])
   for name,f in [('answer',lambda g:g['left_only']-g['right_only']),('question_invariant',lambda g:g['left_question_invariant']-g['right_question_invariant'])]:
    values=sorted(100*sum(f(stats[k]) for k in draw)/sum(stats[k]['n'] for k in draw) for draw in draws)
    for p,label in ((.025,'low'),(.975,'high')):
     x=9999*p;i=int(x);row[name+'_ci_'+label+'_pp']=values[i]+(x-i)*(values[min(i+1,9999)]-values[i])
   paired.append(row)
 answer=all(details[('D_ROLE',s,SPLITS[3])] and sum(x['four'] for x in details[('D_ROLE',s,SPLITS[3])])>=10 and all(next(r for r in paired if r['seed']==s and r['right']==c)['net']>=threshold for c,threshold in [('C_CENTER',3),('N_UNMATCHED',2)]) for s in (19,73));response=all(sum(x['inv'] for x in details[('C_CENTER',s,SPLITS[3])])-sum(x['inv'] for x in details[('D_ROLE',s,SPLITS[3])])>=10 for s in (19,73))
 status='ROLE_CONTRAST_DEVELOPMENT_SIGNAL' if answer and response else 'QUESTION_RESPONSE_WITHOUT_REQUIRED_ANSWER_GAIN' if response else 'ANSWER_GAIN_WITHOUT_TARGET_RESPONSE_EVIDENCE' if answer else 'NO_SUPPORT_FOR_THIS_ROLE_CONTRAST'
 return dict(conditions=conditions,paired=paired,subsets=subsets,source_profile=profile,answer_gate=answer,response_gate=response,status=status)
def score(root):
 root=Path(root);assert read(root/'prediction-job.json')['active']==read(root/'training-job.json')['active']==0
 for x in read(root/'output-seal.json')['files']:assert sha(x['path'])==x['sha256']
 prior=Path(read(root/'old-assets.json')['prior']);seal=read(prior/'outputs-identity-seal.json');expected={str(Path(x['path']).resolve()):x['sha256'] for x in seal['files']};p=prior/'all-outputs-sealed.json';assert sha(p)==expected[str(p.resolve())]
 old=[dict(r,method='A68_CACHED' if r['method']=='A68' else 'B0',origin='CACHED') for r in read(p) if r['method'] in ('A68','B0')];assert len(old)==1664
 outputs=read(root/'new-outputs.json')+old;save(root/'all-outputs.json',outputs);labels={s:read(prior/(s+'-labels.json')) for s in SPLITS};result=tables(outputs,labels,read(root/'scoring-bindings.json'))
 baseline=read(Path(__file__).parent.parent/'docs/codex-artifacts/VLM-POOL-TRANSFER-060/execution-summary.json')['conditions']
 for r in result['conditions']:
  if r['method'] in ('A68_CACHED','B0'):
   b=next(x for x in baseline if (x['method'],x['seed'],x['split'])==('A68' if r['method']=='A68_CACHED' else 'B0',r['seed'],r['split']));assert all(r[k]==b[k] for k in ('n_cells','correct_cells','video_pair_correct','question_pair_correct','four_way_correct'))
 for filename,key in [('condition-summary.csv','conditions'),('paired-summary.csv','paired'),('subset-summary.csv','subsets')]:
  with open(root/filename,'x',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(result[key][0]));w.writeheader();w.writerows(result[key])
 save(root/'scoring-summary.json',result);print('SCORING_CLOSED',result['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('prepare','train','predict','score'));p.add_argument('--root',required=True);p.add_argument('--prior');p.add_argument('--audit');a=p.parse_args()
 if a.phase=='prepare':prepare(a.root,a.prior,a.audit)
 else:globals()[a.phase](a.root)
