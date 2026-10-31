# 061 execution receipt

2026-10-31 Asia/Shanghai. **COMPLETE_CACHED_RESPONSE_AUDIT / CAUSAL_BOTTLENECK_UNRESOLVED / NO_NEW_METHOD_CLAIM.** Clean independent documentation checkout safely fetched/fast-forwarded876eded→26a9c27. Full AGENTS/061 README/exploration decision/060 acceptance and required current061/060 board/overview/result sections read; unique unreported READY061 verified. Exact known060 root/closed registration checked, no old-root traversal; no existing061 root. New exclusive private parent, initial free343067377664B≥256MiB.

## Freeze and narrow input access

Before reading060 bindings/prediction/label/question values, froze061 code, independent verifier/supervisor identities, all formulas/schemas/thresholds, plan33 conditions/225 source rows/26 intervals and6056 cells/1514 fourways. Frozen code LF SHA256:`8d53b3428801f1f1ace759e04d34178b570df92662edeaf143a14c9aa5da6ac7`. Before formal STARTED, the16-pattern synthetic truth table passed145 independent exhaustiveness/cardinality/edge/correct-count checks (2/2/2/2/8). No real QA or model work in fixture. No software failure, repair or retry; code/formulas/thresholds unchanged after STARTED.

Only060's allowed parent/job closures, bindings, four observation/label files, index, all-outputs and two seal files were read, plus indexed366V/220q and the public060 aggregate table. No unused seal targets were opened or hashed. The060 pre-consumption code identities match committed876eded source; relevant output/pre-consumption seals verified before deserialization. Chain roots/post-execution closure records are checked against their retained registrations and matching two-pass hashes, not a public cryptographic signature or OS audit. Old133/50 membership,68/11/54/50 and25/4/20/25 groups, no cross-split group overlap, two-trial holdout families, complementary labels and816+5040+200 origins checked. All6056 inputs were CLOSED strict binary; no missing/invalid/unknown entries treated as wrong or removed. B0 appears once at N50.

Feature files loaded only as CPU weights_only tensors from the exact bytes hashed once in each role, each finite float32 V[6,2560]/q[2560], no checkpoint/model imports. Main analysis resolved/cache-deduplicated paths and closed serialized identities;586 paths/586 distinct serialized loads. No repeated tensor load per main path. Read byte counters include file headers/serialization, not merely tensor payload:25,418,126B analysis +25,418,126B independent review =50,836,252B≤64MiB; max tensor file62620B≤2MiB. Metadata/old prediction reads1,894,861B per role,3,789,722B total≤32MiB. Each pass read604 actual input files including the public aggregate table; actual file SHA/size/mtime checked across passes and post-read stat unchanged. Only indexed057 feature paths actually reused by060 were resolved, no old directory traversal or whole-asset audit.

CUDA_VISIBLE_DEVICES empty before torch import; torch threads4/interop1, CUDA never initialized. No nn.Module,057–060 module import, processor/tokenizer or head state. Feature arithmetic float64 is numerical analysis, not a model forward. Exact q/V collision unions and720-row-permutation minima plus temporal variation/quantiles computed; no data-dependent threshold or normalization change. Vocabulary uses only question strings/train68 reference and fixed normalization; no label-selected coverage or stratified accuracy.

## Execution and independent verification

Formal diagnostic persisted STARTED before protected values; CLOSED after complete output/manifests. Analysis produced33 original-metric-preserving rows and225 label-blind source rows. Exactly one seeded stream/common10000 draws used for26 intervals, positive differences meaning more invariance. No test-answer repair, confidence/oracle projection, source relabeling or new scientific gate.

Independent verifier PASS **14680 checks**, without importing the analysis module: independently encoded16 patterns; re-read old sealed outputs/labels and rebuilt all33 response/histogram/edge rows; re-read the public225-row table and reconstructed all26 common-draw intervals using direct random indices; checked366V/220q from original bytes, recomputed all four geometry/coverage summaries. Geometry used a separate scalar720-assignment search, row dot products and variance-based centered energy, fixed predeclared numerical tolerance.112 geometry scalar checks and32 coverage scalar checks passed. All old actually read file hashes unchanged; no extra hash pass beyond the two budgeted feature reads. It did not read weights/checkpoints/ZIP/media/RGB, repeat a model/head forward, optimize or decode. The read-only verifier source is embedded below.

| Role | outer seconds | peak Job commit bytes | exit | active | killed |
|---|---:|---:|---:|---:|---|
| analysis | 13.516 | 720637952 | 0 | 0 | False |
| fixture | 0.187 | 11722752 | 0 | 0 | False |
| inspection | 0.125 | 8269824 | 0 | 0 | False |
| review | 3.922 | 734814208 | 0 | 0 | False |


Supervised CPU outer at report=17.750s/300 (analysis13.516s; review3.922s). All roles use owned Windows Jobs,2GiB RAM/active-process limit4, suspended creation→assignment→resume, actualactive0/exit0/no kill. Final report/validation Job costs follow the snapshot and are charged to the same300s envelope. Parent elapsed at snapshot596.505s/3600, including interactive/code preparation; no budget reset. Private-root snapshot24files/496041B≤256/32MiB; final closure retained privately.

Model/Qwen/head forward, model load, optimizer/update, weights/checkpoint/ZIP/video/RGB reads, GPU/nvidia-smi/locks, processor/tokenizer, download/decode/research-data network, TimeBlind and environment changes:all0. Only Git document synchronization uses the network. Program roles and private seal chains are not OS-access or physical-I/O certification.

## Delivery and stop

Seven permitted files only: new audit source, this receipt/scientific results/33-condition CSV/225-label-blind source CSV/summary JSON, one append-only061 result. No raw QA/event text/labels/predictions/item correctness, family correctness/K, source maps/private paths/model-data identity hashes or tensors/weights/media uploaded. Planning/AGENTS/contracts/historical code/results unchanged. One ordinary safe main push, then STOP; no automatic062, no continued mechanism search or old GPU budget use.

### Independent verifier (private inputs passed as arguments)

```python
"""Read-only independent verifier. Never imports the analysis/tested models."""
import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import csv
from collections import Counter,defaultdict
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import random
import re
import sys
import torch
torch.set_num_threads(4);torch.set_num_interop_threads(1)
ROOT=Path(sys.argv[1]);PUBLIC=Path(sys.argv[2]);PRIOR=Path(sys.argv[3]);checks=0
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def check(v):
 global checks
 if not v:raise AssertionError('INDEPENDENT_'+str(checks))
 checks+=1
def near(a,b):check(abs(a-b)<=3e-12+3e-10*abs(b))
access=read(ROOT/'access-manifest.json');observed={str(Path(r['path']).resolve()):r for r in access['files']};records={};cache={};tensors={};meta_bytes=tensor_bytes=0
def raw(p,tensor=False):
 global meta_bytes,tensor_bytes
 p=Path(p).resolve();key=str(p)
 if key not in cache:
  stat=p.stat();size=stat.st_size
  if tensor:
   check(size<=2*1024**2);tensor_bytes+=size;check(tensor_bytes+access['tensor_bytes']<=64*1024**2)
  else:meta_bytes+=size;check(meta_bytes+access['metadata_bytes']<=32*1024**2)
  b=p.read_bytes();h=hashlib.sha256(b).hexdigest();cache[key]=b
  check(key in observed and observed[key]['sha256']==h and observed[key]['bytes']==size and observed[key]['mtime_ns']==stat.st_mtime_ns)
  records[key]=dict(path=key,sha256=h,bytes=size,mtime_ns=stat.st_mtime_ns,kind='tensor' if tensor else 'metadata')
 return cache[key]
def oldjson(name):return json.loads(raw(PRIOR/name).decode('utf-8-sig'))
outputsseal=oldjson('outputs-identity-seal.json');pre=oldjson('pre-consumption-seal.json')
expected={}
for x in outputsseal['files']+pre['files']:
 key=str(Path(x['path']).resolve());check(key not in expected or expected[key]==x['sha256']);expected[key]=x['sha256']
plan=read(ROOT/'analysis-plan.json');check(pre['code']==plan['prior060_code_lf_sha256'])
closed=oldjson('parent-closed.json');check(closed['commit']=='876ededdcaa4038363fc92f9761462c42435e41c' and closed['push']=='SUCCEEDED')
for name in ('training','prediction','gpu'):
 j=oldjson(name+'-job.json');check(j['active']==j['exit_code']==0 and not j['killed'])
bind=oldjson('data-bindings.json');splits=('train_pool68','validation11','development54','source_holdout50');ns=(68,11,54,50);methods=('A25','P1_25','A68','P1_68');kinds=('CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED')
truth_table={0:'CONSTANT',3:'VIDEO_ONLY',5:'QUESTION_ONLY',6:'CHECKERBOARD',9:'CHECKERBOARD',10:'QUESTION_ONLY',12:'VIDEO_ONLY',15:'CONSTANT'}
for pattern in range(16):
 p=tuple(int(bool(pattern&(8>>j))) for j in range(4));kind=truth_table.get(pattern,'MIXED')
 qe=int(p[0]!=p[1])+int(p[2]!=p[3]);ve=int(p[0]!=p[2])+int(p[1]!=p[3]);check(qe==2*int(kind in ('QUESTION_ONLY','CHECKERBOARD'))+int(kind=='MIXED'));check(ve==2*int(kind in ('VIDEO_ONLY','CHECKERBOARD'))+int(kind=='MIXED'))
 for y in ((1,0,0,1),(0,1,1,0)):
  count=sum(a==b for a,b in zip(p,y));check((count==2)==(kind in kinds[:3]) and (count in (1,3))==(kind=='MIXED') and (count in (0,4))==(kind=='CHECKERBOARD'))
check(Counter(truth_table.get(i,'MIXED') for i in range(16))==dict(CONSTANT=2,VIDEO_ONLY=2,QUESTION_ONLY=2,CHECKERBOARD=2,MIXED=8))
pools=bind['pools'];check(tuple(len(pools[s]) for s in splits)==ns)
groups=[{r['group_key'] for r in pools[s]} for s in splits];check([len(x) for x in groups]==[25,4,20,25])
for i,g in enumerate(groups):
 for h in groups[i+1:]:check(not g&h)
obs={s:oldjson(s+'-observations.json') for s in splits};labels={s:oldjson(s+'-labels.json') for s in splits}
for s,n in zip(splits,ns):
 for i,r in enumerate(pools[s]):
  check(obs[s][i]==dict(index=i,videos=r['videos'],questions=r['questions']) and labels[s][i]==dict(index=i,labels=r['labels']))
  y=[a for row in labels[s][i]['labels'] for a in row];check(all(type(v) is int and v in (0,1) for v in y) and y[0]==y[3] and y[1]==y[2] and y[0]+y[1]==1)
allout=oldjson('all-outputs-sealed.json');lookup={};origins=Counter()
for r in allout:
 key=(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question']);check(key not in lookup and r['status']=='CLOSED' and type(r['prediction']) is int and r['prediction'] in (0,1));lookup[key]=r['prediction'];origins[r['origin']]+=1
check(len(lookup)==6056 and origins==dict(CACHED=816,NEW_HEAD=5040,NEW_B0=200))
summary=read(ROOT/'audit-summary.json');check(len(summary['conditions'])==33 and summary['four_way_instances']==1514)
condition_csv=list(csv.DictReader((PUBLIC/'condition-summary.csv').open(encoding='utf-8',newline='')))
source_csv=list(csv.DictReader((PUBLIC/'source-profile.csv').open(encoding='utf-8',newline='')))
check(len(condition_csv)==33 and len(source_csv)==225 and set(source_csv[0])=={'method','seed','family','n',*kinds})
oldbaseline=Path(next(k for k in observed if Path(k).name=='condition-summary.csv'))
baseline=list(csv.DictReader(io.StringIO(raw(oldbaseline).decode('utf-8'))));families=sorted(groups[3]);reconstructed_profile=[]
for split,n in zip(splits,ns):
 configs=[(m,s) for m in methods for s in (19,73)]+([('B0','NA')] if n==50 else [])
 for method,seed in configs:
  counts=Counter();hist=Counter();correct=vp=qp=0;itypes=[]
  for i in range(n):
   p=[lookup[(method,seed,split,i,v,q)] for v in (0,1) for q in (0,1)];code=sum(v*(8>>j) for j,v in enumerate(p));kind=truth_table.get(code,'MIXED');counts[kind]+=1;itypes.append(kind)
   y=[v for row in labels[split][i]['labels'] for v in row];c=[int(a==b) for a,b in zip(p,y)];hist[sum(c)]+=1;correct+=sum(c);vp+=c[0]*c[2]+c[1]*c[3];qp+=c[0]*c[1]+c[2]*c[3]
  row=next(r for r in summary['conditions'] if (r['method'],r['seed'],r['split'])==(method,seed,split));oldrow=next(r for r in baseline if (r['method'],r['seed'],r['split'])==(method,str(seed),split))
  want=dict(n_instances=n,n_cells=4*n,complete_cells=4*n,valid_cells=4*n,unknown_cells=0,status='COMPLETE',correct_cells=correct,video_pair_correct=vp,question_pair_correct=qp,four_way_correct=hist[4],checkerboard_correct=hist[4],checkerboard_inverted=hist[0],**{k:counts[k] for k in kinds},**{'K'+str(k):hist[k] for k in range(5)})
  want.update(question_invariant=counts['CONSTANT']+counts['VIDEO_ONLY'],video_invariant=counts['CONSTANT']+counts['QUESTION_ONLY'],qflip_edges=2*(counts['QUESTION_ONLY']+counts['CHECKERBOARD'])+counts['MIXED'],vflip_edges=2*(counts['VIDEO_ONLY']+counts['CHECKERBOARD'])+counts['MIXED'])
  for k,v in want.items():check(row[k]==v)
  for k in ('n_instances','n_cells','complete_cells','valid_cells','unknown_cells','correct_cells','video_pair_correct','question_pair_correct','four_way_correct'):check(row[k]==int(oldrow[k]))
  for k,den in [('question_invariant',n),('video_invariant',n),('qflip_edge',2*n),('vflip_edge',2*n)]:near(row[k+'_rate'],want[k if den==n else k+'s']/den)
  public=next(r for r in condition_csv if (r['method'],r['seed'],r['split'])==(method,str(seed),split));check(all(public[k]==str(v) for k,v in row.items()))
  if split==splits[3]:
   for number,key in enumerate(families,1):
    ids=[i for i,r in enumerate(pools[split]) if r['group_key']==key];check(len(ids)==2);c=Counter(itypes[i] for i in ids)
    public=next(r for r in source_csv if (r['method'],r['seed'],r['family'])==(method,str(seed),f'F{number:02}'));check(int(public['n'])==2)
    for k in kinds:check(int(public[k])==c[k])
    reconstructed_profile.append(dict(method=method,seed=seed,family=f'F{number:02}',n=2,**{k:c[k] for k in kinds}))
check(reconstructed_profile==summary['source_profile'])
# Re-read the public label-blind family table, using only its five type counts.
rng=random.Random(55061);draws=[[math.floor(rng.random()*25) for j in range(25)] for i in range(10000)]
check(len(summary['intervals'])==26)
expected_stats={('marginal',metric,m,s,'NA') for m,s in [(m,s) for m in methods for s in (19,73)]+[('B0','NA')] for metric in ('question_invariant','video_invariant')}|{('paired_difference',metric,m,s,comp) for m,comp in [('A68','A25'),('P1_68','P1_25')] for s in (19,73) for metric in ('question_invariant','video_invariant')}
check({(r['kind'],r['metric'],r['method'],r['seed'],r['comparator']) for r in summary['intervals']}==expected_stats)
def vector(method,seed,metric):
 rows=sorted([r for r in source_csv if (r['method'],r['seed'])==(method,str(seed))],key=lambda r:r['family']);check(len(rows)==25)
 return [int(r['CONSTANT'])+int(r['VIDEO_ONLY' if metric=='question_invariant' else 'QUESTION_ONLY']) for r in rows]
for row in summary['intervals']:
 v=vector(row['method'],row['seed'],row['metric'])
 if row['kind']=='paired_difference':v=[a-b for a,b in zip(v,vector(row['comparator'],row['seed'],row['metric']))]
 near(row['estimate'],sum(v)/50);vals=sorted(math.fsum(v[k] for k in indices)/(2*len(indices)) for indices in draws)
 for p,key in ((.025,'ci_low'),(.975,'ci_high')):
  x=9999*p;lo=math.floor(x);near(row[key],vals[lo]*(lo+1-x)+vals[min(lo+1,9999)]*(x-lo))
 check(row['n_instances']==50 and row['n_families']==25 and row['unit']==('proportion' if row['kind']=='marginal' else 'proportion_difference'))
index=oldjson('feature-index.json');check(len(index['video'])==366 and len(index['text'])==220)
def value(path,shape):
 key=str(Path(path).resolve())
 if key not in observed:
  # Closed identical serialized cache input: use the same actually read file.
  identity=expected[key];matches=[k for k,r in observed.items() if r['kind']=='tensor' and r['sha256']==identity];check(bool(matches));key=matches[0];path=key
 if key not in tensors:
  t=torch.load(io.BytesIO(raw(path,tensor=True)),map_location='cpu',weights_only=True);check(t.dtype==torch.float32 and t.device.type=='cpu' and tuple(t.shape)==shape and bool(torch.isfinite(t).all()));tensors[key]=t
 return tensors[key]
videos={n:value(r['path'],(6,2560)) for n,r in index['video'].items()};questions={q:value(r['path'],(2560,)) for q,r in index['text'].items()}
def normevents(row):
 q0,q1=row['questions'];first=q0.removeprefix('Does the event "').removesuffix('"? Answer Yes or No.');a,b=first.rsplit('" happen before the event "',1)
 check(q1==f'Does the event "{b}" happen before the event "{a}"? Answer Yes or No.')
 return tuple(' '.join(x.replace('_',' ').split()).casefold() for x in (a,b))
train=[normevents(r) for r in obs[splits[0]]];eventset=set(itertools.chain.from_iterable(train));pairset={tuple(sorted(p)) for p in train}
def qtiles(xs):
 xs=sorted(xs);result={}
 for p in (0,.25,.5,.75,1):
  x=(len(xs)-1)*p;lo=math.floor(x);result[str(p)]=xs[lo]*(lo+1-x)+xs[min(lo+1,len(xs)-1)]*(x-lo)
 return result
perms=tuple(itertools.permutations(range(6)));geom_checks=coverage_checks=0
for split,n in zip(splits,ns):
 qds=[];ods=[];mins=[];tv=[];eq_q=eq_v=small=union=0;unique=set();cover=Counter();strings=[];same=0
 for r in obs[split]:
  a,b=normevents(r);same+=a==b;seen=int(a in eventset)+int(b in eventset);cover['PAIR_SEEN' if tuple(sorted((a,b))) in pairset else 'BOTH_EVENTS_SEEN_PAIR_NEW' if seen==2 else 'ONE_EVENT_SEEN' if seen==1 else 'NO_EVENT_SEEN']+=1;strings+=r['questions']
  qa,qb=(questions[q].double() for q in r['questions']);va,vb=(videos[k].double() for k in r['videos'])
  qe=bool((qa==qb).all());ve=bool((va==vb).all());eq_q+=qe;eq_v+=ve;union+=qe or ve
  qd=float((qa-qb).square().sum().sqrt()/(qa.square().sum().sqrt()+qb.square().sum().sqrt()+1e-12));qds.append(qd);small+=qd<=1e-4
  den=float(va.square().sum().sqrt()+vb.square().sum().sqrt()+1e-12);ods.append(float((va-vb).square().sum().sqrt())/den)
  costs=[[float(torch.dot(va[i]-vb[j],va[i]-vb[j])) for j in range(6)] for i in range(6)]
  mins.append(math.sqrt(min(math.fsum(costs[i][p[i]] for i in range(6)) for p in perms))/den)
  for name,v in zip(r['videos'],(va,vb)):
   tv.append(float(v.var(dim=0,correction=0).sum()*6/(v.square().sum()+1e-12)))
   t=videos[name].clone();t[t==0]=0;unique.add(hashlib.sha256(t.numpy().tobytes()).hexdigest())
 geom=next(x for x in summary['geometry'] if x['split']==split);coverage=next(x for x in summary['coverage'] if x['split']==split)
 for k,v in dict(n_instances=n,q_exact_equal_instances=eq_q,q_distance_le_1e_minus4_instances=small,ordered_v_exact_equal_instances=eq_v,exact_collision_instance_union=union,deterministic_head_four_way_upper_bound=n-union,temporal_video_slots=2*n,unique_video_tensors=len(unique)).items():check(geom[k]==v);geom_checks+=1
 for k,xs in [('question_swap_relative_distance',qds),('ordered_video_relative_distance',ods),('min_720_row_permutation_relative_distance',mins),('temporal_variation_ratio',tv)]:
  for p,x in qtiles(xs).items():near(geom[k][p],x);geom_checks+=1
 for k,v in dict(n_instances=n,raw_question_slots=2*n,unique_question_strings=len(set(strings)),normalized_same_event_instances=same,**{k:cover[k] for k in ('PAIR_SEEN','BOTH_EVENTS_SEEN_PAIR_NEW','ONE_EVENT_SEEN','NO_EVENT_SEEN')}).items():check(coverage[k]==v);coverage_checks+=1
for key,r in records.items():
 if key in expected:check(r['sha256']==expected[key])
 stat=Path(key).stat();check(stat.st_size==r['bytes'] and stat.st_mtime_ns==r['mtime_ns'])
check(set(records)==set(observed))
check(meta_bytes+access['metadata_bytes']<=32*1024**2 and tensor_bytes+access['tensor_bytes']<=64*1024**2)
check(not torch.cuda.is_initialized())
report=dict(status='PASS',checks=checks,condition_rows=33,source_rows=225,intervals=26,formal_cells=6056,four_way_instances=1514,geometry_split_summaries=4,coverage_split_summaries=4,geometry_scalar_checks=geom_checks,coverage_scalar_checks=coverage_checks,metadata_bytes=meta_bytes,tensor_bytes=tensor_bytes,cumulative_metadata_bytes=meta_bytes+access['metadata_bytes'],cumulative_tensor_bytes=tensor_bytes+access['tensor_bytes'],actual_old_files_hashes_match_before_and_after=True,independent_from_tested_module=True,forward=0,updates=0,cuda_initialized=False)
with open(ROOT/'independent-review.json','x',encoding='utf-8') as f:json.dump(report,f,sort_keys=True,indent=2)
with open(ROOT/'review-access-manifest.json','x',encoding='utf-8') as f:json.dump(dict(files=list(records.values())),f,sort_keys=True,indent=2)
print('INDEPENDENT_REVIEW_PASS',checks,'33/225/26;geometry4;coverage4',flush=True)

```
