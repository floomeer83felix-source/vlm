# 062 execution receipt

2026-10-31 Asia/Shanghai. Complete6-configuration CPU experiment. Synced clean independent main to d325aa0; fullAGENTS/062 contract/design/061 acceptance and required current board/overview/results read. Unique unreportedREADY062, no pre-existing062 root. Exact known060/061 roots only; no scanning or old task restart. All original133+50 members,68/11/54/50 and25/4/20/25 groups, complementary bindings and observations matched060/061 seals. Evidence remains PUBLISHER_COMPOSITE_QA. Existing environment preserved.

Preparation CPU verified finite indexed366V/220q, tensor file≤2MiB, old plans≤4MiB, relevant hashes only; no old final checkpoints or main weights. Old plan payloads containP1 but only A and sequence used, P1 never instantiated. Train84 UTF-8-byte-sorted questions tau-closed; SHA prefix/8-byte big-endian modulo84 cyclic anchor rule excludesq/tau. Each arm's train-onlyfloat64 mean/scalar RMS finite>1e−8; transformed float32 train mean near0/RMS near1, rawD exchange antisymmetry and non-equivalence to rawA68 passed. No head forward or optimizer in preparation. Code,views,normalizer,bindings/subsets,original A states and n68 sequences sealed before first configuration STARTED. All68 covered eachseed. Public code LF SHA256:`25d78d83f0bace3a337d124e6cf65a3f15332fd3402188c47645a2e80bc18097`; unchanged since seal.

Training role read only train labels/observations/train views and neededV/initial plans, no evaluation labels/source groups/old results. Same356673-parameter056 A/pack/AdamW,CPUfloat32/threads4/interop1,lr.001/wd.01/betas(.9,.999)/eps1e−8/clip1. Seed19 C/D/N then seed73 C/D/N,250 true forward/BCE/backward/optimizer steps each=1500,48000 training cell exposures. Every STEP_STARTED/CLOSED retained with finite loss/each non-None finite parameter gradient. Initial and final states retained, actual positive parameter L1 changes/loss summaries inJSON. Only last step checkpoint; no extra head forward/fixture optimization/early stop. CUDA_VISIBLE_DEVICES empty before torch; CUDA uninitialized.

Training Job actualactive0 before separate prediction role.4392 independent single-V/current-q predictions persisted STARTED/CLOSED in oneJSONL, outputs and all initial/final/transform/code identities sealed. Prediction Job actualactive0 before score role read/projected1464 oldA68+200singleB0, no old head forward.6056 complete valid cells/33conditions/8pairs/32subsets/200families/16intervals. Cache metrics reproduced060 and061. No prediction flips, vote, oracle repair, failures or retries.

Independent verifier did not import tested experiment/scorer or forward/optimize:11203 checks of actualmu/RMS/anchors/views, originalA states/sequences, all6 actual initial/final states and1500 logs,4392new/1664cached records,33/8/32 tables and16 common-bootstrap intervals. Supplemental4602 checks independently reconstructed coverage membership from frozen question strings/train-only reference, reproduced061 cache response histograms, checked pair marginals and4392 prediction journals, code seal and parameter-change summaries. Total15805 PASS; no repeated research. Verifier scripts below are read-only, not OS access enforcement.

| Role | outer seconds | peak commit bytes | exit/active/killed |
|---|---:|---:|---|
| annex-job | 2.109 | 733499392 | 0/0/False |
| prediction-job | 37.500 | 735285248 | 0/0/False |
| preparation-job | 2.640 | 735703040 | 0/0/False |
| review-job | 2.406 | 703148032 | 0/0/False |
| scoring-job | 0.797 | 22634496 | 0/0/False |
| training-job | 25.813 | 825470976 | 0/0/False |


Train+prediction+scoring outer64.110s/1200; other preparation/review/annex7.155s/600, all owned Jobs active0/exit0/no kill,8GiB/active-process4. Report/validation closure charged to same envelopes after this snapshot. Initialfree342943477760B≥256MiB. Snapshot61files/33258673B≤512/128MiB; initial/final/plan copies20050658B≤32MiB; parent elapsed at snapshot329.189s/7200. Logical feature read accounting110184594B/256MiB includes prep hash+load,trainV,predictV,review identity+q reads. Old initial plans recorded5751970B per complete pair of files, four logical read passes including hash/review; separately counted. Metadata conservative source-path accounting≤24MiB/32MiB, not a physical-I/O measurement. Actual OS read-cache amplification is UNKNOWN. Old actually used assets matched before/after; no entire old-root/model/media hashing.

No Qwen/visual encoder/processor/tokenizer/new text encoding/GPU/nvidia-smi/mediaRGB/ZIP/download/decode/research-network/TimeBlind or environment changes. Standard task formulas are followed, not a general crash/power-loss durable quota certification. Code/data roles do not certify OS non-access. No raw data identities/paths/questions/events/labels/predictions/normalizer/weights/feature arrays published. Eight allowed paths only, results append once; planning/history unchanged. One ordinary safe main push then STOP; no automatic063.

## Independent verifier source

```python
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import csv,hashlib,io,itertools,json,math,random,re,sys
from pathlib import Path
import torch as t
t.set_num_threads(4);t.set_num_interop_threads(1)
R=Path(sys.argv[1]);checks=0
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def load(p):return t.load(p,map_location='cpu',weights_only=True)
def check(x):
 global checks
 assert x,checks
 checks+=1
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assets=read(R/'old-assets.json');prior=Path(assets['prior']);audit=Path(assets['audit'])
for x in assets['files']:check(sha(x['path'])==x['sha256'])
bindings=read(R/'transform-bindings.json');train=bindings['train'];check(len(train)==84 and train==sorted(set(train),key=lambda q:q.encode()))
index=read(R/'feature-index.json');h={q:load(x['path']).double() for q,x in index['text'].items()};views=load(R/'views.pt');stats=load(R/'normalizer.pt');arms=('C_CENTER','D_ROLE','N_UNMATCHED');splits=('train_pool68','validation11','development54','source_holdout50')
def swap(q):
 a,b=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q).groups();return f'Does the event "{b}" happen before the event "{a}"? Answer Yes or No.'
for q in h:
 k=int.from_bytes(hashlib.sha256(('VLM062/anchor/'+q).encode()).digest()[:8],'big')%84
 a=next(train[(k+j)%84] for j in range(84) if train[(k+j)%84] not in {q,swap(q)});check(bindings['anchors'][q]==a)
for arm in arms:
 raw={q:h[q] if arm=='C_CENTER' else (h[q]-h[swap(q) if arm=='D_ROLE' else bindings['anchors'][q]])*.5 for q in h};stack=t.stack([raw[q] for q in train]);mu=stack.mean(0);s=((stack-mu).square().sum()/stack.numel()).sqrt();check(t.equal(mu,stats[arm]['mu']) and t.allclose(s,stats[arm]['scale'],rtol=1e-14,atol=1e-14))
 for q in h:check(t.equal(((raw[q]-mu)/stats[arm]['scale']).float(),views[arm][q]))
for seed in (19,73):
 p=load(R/f'plan-{seed}.pt');old=load(prior/f'plan-{seed}.pt');check(t.equal(p['sequence'],old['sequence']) and len(t.unique(p['sequence']))==68)
 for arm in arms:
  d=R/'training'/f'{arm}-{seed}';initial=load(d/'initial.pt');final=load(d/'final.pt');check(sum(x.numel() for x in final.values())==356673)
  for k in initial:check(t.equal(initial[k],old['A'][k]) and t.isfinite(final[k]).all())
  check(sum(float((initial[k]-final[k]).abs().sum()) for k in initial)>0)
  lines=[json.loads(x) for x in (d/'steps.jsonl').read_text().splitlines()];check(len(lines)==502 and lines[0]['event']=='STARTED' and lines[-1]['steps']==250)
  for j in range(250):check(lines[2*j+1]==dict(event='STEP_STARTED',step=j) and lines[2*j+2]['step']==j and lines[2*j+2]['event']=='STEP_CLOSED' and math.isfinite(lines[2*j+2]['loss']))
outputs=read(R/'all-outputs.json');check(len(outputs)==6056);oldout=read(prior/'all-outputs-sealed.json');oldmap={(x['method'],x['seed'],x['split'],x['index'],x['video'],x['question']):x for x in oldout};lookup={}
for x in outputs:
 key=(x['method'],x['seed'],x['split'],x['index'],x['video'],x['question']);check(key not in lookup and x['status']=='CLOSED');lookup[key]=x['prediction']
 if x['origin']=='CACHED':check(x['prediction']==oldmap[('A68' if x['method']=='A68_CACHED' else 'B0',)+key[1:]]['prediction'])
check(sum(x['origin']=='NEW' for x in outputs)==4392)
summary=read(R/'scoring-summary.json');labels={s:read(prior/(s+'-labels.json')) for s in splits};db={};pattern={0:'CONSTANT',3:'VIDEO_ONLY',5:'QUESTION_ONLY',6:'CHECKERBOARD',9:'CHECKERBOARD',10:'QUESTION_ONLY',12:'VIDEO_ONLY',15:'CONSTANT'}
for row in summary['conditions']:
 m,seed,s=row['method'],row['seed'],row['split'];items=[];types={k:0 for k in ('CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')};hist=[0]*5;vp=qp=0
 for i in range(row['n_instances']):
  p=[lookup[(m,seed,s,i,v,q)] for v in (0,1) for q in (0,1)];gold=sum(labels[s][i]['labels'],[]);correct=[int(a==b) for a,b in zip(p,gold)];k=sum(correct);typ=pattern.get(sum(x*(8>>j) for j,x in enumerate(p)),'MIXED');types[typ]+=1;hist[k]+=1;vp+=correct[0]*correct[2]+correct[1]*correct[3];qp+=correct[0]*correct[1]+correct[2]*correct[3];items.append((k,int(k==4),int(typ in ('CONSTANT','VIDEO_ONLY'))))
 check(row['correct_cells']==sum(k*hist[k] for k in range(5)) and row['four_way_correct']==hist[4] and row['question_invariant']==sum(x[2] for x in items) and row['video_pair_correct']==vp and row['question_pair_correct']==qp)
 check(all(row[k]==v for k,v in types.items()) and all(row['K'+str(k)]==hist[k] for k in range(5)));db[(m,seed,s)]=items
b=read(R/'scoring-bindings.json')
for row in summary['subsets']:
 ids=[i for i,x in enumerate(b['subsets']['development54']) if x==row['subset']];v=[db[(row['method'],row['seed'],'development54')][i] for i in ids];check(len(v)==row['n_instances'] and sum(x[0] for x in v)==row['correct_cells'] and sum(x[1] for x in v)==row['four_way_correct'] and sum(x[2] for x in v)==row['question_invariant'])
rng=random.Random(55062);draws=[[int(rng.random()*25) for j in range(25)] for _ in range(10000)];groups=b['groups']['source_holdout50'];keys=sorted(set(groups))
for row in summary['paired']:
 seed,comp=row['seed'],row['right'];L=db[('D_ROLE',seed,'source_holdout50')];Q=db[(comp,'NA' if comp=='B0' else seed,'source_holdout50')];profile=sorted([x for x in summary['source_profile'] if x['seed']==seed and x['right']==comp],key=lambda x:x['family'])
 for j,g in enumerate(profile):
  ids=[i for i,x in enumerate(groups) if x==keys[j]];lc=sum(L[i][1] and not Q[i][1] for i in ids);rc=sum(Q[i][1] and not L[i][1] for i in ids);bc=sum(L[i][1] and Q[i][1] for i in ids);check(g['left_only']==lc and g['right_only']==rc and g['both_correct']==bc and g['both_wrong']==2-lc-rc-bc and g['left_question_invariant']==sum(L[i][2] for i in ids) and g['right_question_invariant']==sum(Q[i][2] for i in ids))
 for name,vals in [('answer',[g['left_only']-g['right_only'] for g in profile]),('question_invariant',[g['left_question_invariant']-g['right_question_invariant'] for g in profile])]:
  samples=sorted(2*sum(vals[k] for k in draw) for draw in draws)
  for p,label in ((.025,'low'),(.975,'high')):
   x=9999*p;i=int(x);check(abs(row[name+'_ci_'+label+'_pp']-(samples[i]*(1-x+i)+samples[min(i+1,9999)]*(x-i)))<1e-10)
answer=all(sum(x[1] for x in db[('D_ROLE',s,'source_holdout50')])>=10 and all(sum(x[1] for x in db[('D_ROLE',s,'source_holdout50')])-sum(x[1] for x in db[(c,s,'source_holdout50')])>=n for c,n in [('C_CENTER',3),('N_UNMATCHED',2)]) for s in (19,73));response=all(sum(x[2] for x in db[('C_CENTER',s,'source_holdout50')])-sum(x[2] for x in db[('D_ROLE',s,'source_holdout50')])>=10 for s in (19,73));check(summary['answer_gate']==answer and summary['response_gate']==response)
for name,key in [('condition-summary.csv','conditions'),('paired-summary.csv','paired'),('subset-summary.csv','subsets')]:
 rows=list(csv.DictReader((R/name).open(encoding='utf-8')));check(len(rows)==len(summary[key]))
 for a,b in zip(rows,summary[key]):check(all(a[k]==str(v) for k,v in b.items()))
check(not t.cuda.is_initialized());report=dict(status='PASS',checks=checks,answer_gate=answer,response_gate=response,head_forward=0,updates=0,feature_bytes=sum(Path(x['path']).stat().st_size for x in index['text'].values()),plan_bytes=sum((prior/f'plan-{s}.pt').stat().st_size for s in (19,73)))
with open(R/'independent-review.json','x',encoding='utf-8') as f:json.dump(report,f,indent=2)
print('INDEPENDENT_PASS',checks,flush=True)

```

## Supplemental read-only verifier

```python
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import hashlib,json,re,sys
from collections import Counter
from pathlib import Path
import torch as t
t.set_num_threads(4);t.set_num_interop_threads(1)
r=Path(sys.argv[1]);read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'));s=read(r/'scoring-summary.json');a=read(r/'old-assets.json');prior=Path(a['prior']);audit=Path(a['audit']);checks=0
def check(x):
 global checks
 assert x,checks
 checks+=1
def events(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);return tuple(' '.join(x.replace('_',' ').split()).casefold() for x in m.groups())
obs={p:read(prior/(p+'-observations.json')) for p in ('train_pool68','validation11','development54','source_holdout50')};train=[events(x['questions'][0]) for x in obs['train_pool68']];es={x for pair in train for x in pair};ps={tuple(sorted(pair)) for pair in train};actual={}
for split,rows in obs.items():
 values=[]
 for row in rows:
  pair=events(row['questions'][0]);n=sum(x in es for x in pair);values.append('PAIR_SEEN' if tuple(sorted(pair)) in ps else 'BOTH_EVENTS_SEEN_PAIR_NEW' if n==2 else 'ONE_EVENT_SEEN' if n==1 else 'NO_EVENT_SEEN')
 actual[split]=values
check(actual==read(r/'scoring-bindings.json')['subsets'])
for split,values in actual.items():
 old=next(x for x in read(audit/'audit-summary.json')['coverage'] if x['split']==split)
 for k in ('PAIR_SEEN','BOTH_EVENTS_SEEN_PAIR_NEW','ONE_EVENT_SEEN','NO_EVENT_SEEN'):check(values.count(k)==old[k])
old=read(audit/'audit-summary.json')['conditions']
for x in s['conditions']:
 if x['method'] in ('A68_CACHED','B0'):
  y=next(z for z in old if (z['method'],z['seed'],z['split'])==('A68' if x['method']=='A68_CACHED' else 'B0',x['seed'],x['split']))
  for k in ('correct_cells','four_way_correct','question_invariant','CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED','K0','K1','K2','K3','K4'):check(x[k]==y[k])
for x in s['paired']:
 rows=[g for g in s['source_profile'] if g['seed']==x['seed'] and g['right']==x['right']];check(len(rows)==25)
 for k in ('left_only','right_only','both_correct','both_wrong','unknown','left_question_invariant','right_question_invariant'):check(x[k]==sum(g[k] for g in rows))
 check(x['net']==x['left_only']-x['right_only'] and x['question_invariant_delta_pp']==2*(x['left_question_invariant']-x['right_question_invariant']))
configs=[]
for seed in (19,73):
 for arm in ('C_CENTER','D_ROLE','N_UNMATCHED'):
  d=r/'training'/f'{arm}-{seed}';initial=t.load(d/'initial.pt',weights_only=True,map_location='cpu');final=t.load(d/'final.pt',weights_only=True,map_location='cpu');logs=[json.loads(v) for v in (d/'steps.jsonl').read_text().splitlines()];loss=[x['loss'] for x in logs if x['event']=='STEP_CLOSED'];configs.append(dict(method=arm,seed=seed,steps=len(loss),parameters=sum(v.numel() for v in final.values()),parameter_l1_change=sum(float((final[k]-initial[k]).abs().sum()) for k in initial),first_loss=loss[0],last_loss=loss[-1],min_loss=min(loss),max_loss=max(loss)))
logs=[json.loads(v) for v in (r/'prediction.jsonl').read_text().splitlines()];check(len(logs)==8784)
for i in range(4392):check(logs[2*i]['event']=='STARTED' and logs[2*i+1]['event']=='CLOSED' and logs[2*i]['key']==logs[2*i+1]['key'])
seal=read(prior/'outputs-identity-seal.json');p=prior/'all-outputs-sealed.json';check(hashlib.sha256(p.read_bytes()).hexdigest()==next(x['sha256'] for x in seal['files'] if Path(x['path']).resolve()==p.resolve()))
plan=read(r/'input-seal.json');check(hashlib.sha256((Path(sys.argv[2])/'prototypes/question_role_contrast_062.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==plan['code_sha256']);check(sum(x['steps'] for x in configs)==1500 and not t.cuda.is_initialized())
json.dump(dict(status='PASS',checks=checks,configurations=configs),open(r/'annex-review.json','x',encoding='utf-8'),indent=2);print('ANNEX_PASS',checks)

```

Code-seal scope caveat: the public scientific module/dependency identities/input artifacts were sealed before training; private supervisor and independently written reviewer source were retained but not separately covered by that initial code seal. Their logs and embedded review source do not replace that missing provenance coverage. A later editorial-only annotation command initially used the locale text encoding and failed before writing; corrected to explicit UTF-8, without any research input or computation retry.
