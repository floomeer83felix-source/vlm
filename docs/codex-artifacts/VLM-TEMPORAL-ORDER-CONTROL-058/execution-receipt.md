# 058 execution receipt

2026-10-30 Asia/Shanghai. **COMPLETE_CPU_ORDER_CONTROL / ORDER_BENEFIT_DEVELOPMENT_SIGNAL.**

Clean independent docs status/fetch/ff-only advanced to ecad879c2a01839814ece01507b3cba3e67cb66d.
AGENTS/058 README/current board+overview and057 acceptance read, results searched
for058 and complete057 entry read; unique unreported READY058 confirmed.057 train
code/056 head, public057 condition/summary and receipt's initial-plan/seal notes
read. Exact prior057 root came from existing run registration; parent closed and
training Job active0. New058 root exclusively created, free disk
345702244352B>1GiB. No scans/unrelated task files or old task main.

Only actual reused feature/index/plan/observation/code/output identities and
their seals were hashed.170 old asset hashes matched before/after. No ZIP,
media, frames, Qwen weights or original whole workspace was copied or rehashed.
Original102 V tensors finite CPUfloat32[6,2560],54 q[2560], source partitions
25/2/24, participant groups16/2/15 with no cross-split groups. Original seed19/73
pretrain states and training plans matched tensor-by-tensor; new initial copies
preserve the old tensor storage bytes. They are used as actual training inputs;
the old train helper's regenerated plan is used only for its equality check,
not substituted for unavailable originals.

Original head-output body matches its057 closure/evaluation seal; exactly408
closed A cells projected as A_CACHED. No A/B0 prediction is read by the H training
role. Preparation source-group projection strips51 answer arrays lexically before
JSON decoding the old mixed pilot seal; evaluation labels are read only by the
post-training scoring/review roles. Trainer reads only three independent unlabeled
observations, sorted/current V,q, the original state/sequence and train-label file.
Role/code/file separation is not an OS-level no-access proof.

Fixed H: each2560-value row converted numerically unchanged to contiguous little-
endian float32 bytes b; lexicographic key(SHA256(b).digest(),b). No time index,
metadata, question, label or source in key. All six rows retained, q unchanged.
All102 orders changed.950 actual input/transform checksPASS: four prescribed
permutations, byte equality of sorted result, row multiset, idempotence, shapes,
finite tensors and old identities. No fixture optimizer or model calls. Input,
transform, old bindings, both original plans, new code and configuration sealed
before first058/H configuration STARTED. No post-start code or recipe changes.

H external keys058/H/seed19 and058/H/seed73, internal loss_arm=A only for original
BCE helper. Every new directory names H; old A directory untouched. Both actual
250-step logs start/close exactly once,500 real backward/optimizer.step total,
no restarts/retries/additional seed or steps. Same356673 parameters, original
initial state/250脳8 samples, AdamW lr.001/wd.01/betas(.9,.999)/eps1e-8, clip1,
CPUfloat32/thread4. Each config2000 group/8000cell exposures; no validation
selection, early stopping or checkpoint search. Only last-step checkpoint saved.
Final parameter L1 changes and first/last/min/max loss are in JSON.

All H408 single-cell predictions+final checkpoints/transform/code identities
sealed before scoring, training Job actualactive0 first. Prediction inputs only
current sorted V and current q; no paired outputs, label flipping or voting.
A original cached outputs only, new A forward/training0, I/V/S/B0 work0. Scorer
then read old split labels and checked original A train24/20,validation2/2,test5/7.
All816 combined cells valid; fixed12/2 tables and30 anonymous source rows retained.
058 gate passes A鈭扝 net2/3; this used development-set follow-up does not become
a new blind test or restore the stopped joint-supervision recipe.

Independent stdlib reviewer3297 checksPASS, no tested transform/train/scorer
imports or torch/model/network/decode. Parsed only stored tensor ZIP payloads to
rebuild102 exact hash-row sorts, all four permutation invariants/idempotence/
multisets,54 unchanged q payloads and finite values. Matched original/copied plan
storage bytes, source partition and all old asset hashes,500 closed steps,
408cached+408new predictions/labels,12conditions/2pairs,30source rows, and group
bootstrap10000/Random55058 intervals. New/old label bindings matched original057
seal after prediction sealing. Review-source code is included below; OS-level
action auditing and kitchen/physical independence remain outside its scope.

Resources: train+prediction+score Job outer 11.797s/600s;
other preparation/review 7.454s/600s, peak Job
commit 811868160B/8GiB. Five owned Jobs active0/exit0/no
kill, active-process limit4. CUDA_VISIBLE_DEVICES empty, CUDA uninitialized after
torch import/end checks. GPU/Qwen/encoder weights or forward/backward/update,
feature extraction/nvidia-smi/data download/media decode/environment changes0.
New synthetic updates0;500 actual H updates only.

Parent elapsed at report 708.440s/3600s. Root
snapshot 147files/12604208B<512/512MiB; checkpoints
+initial plans 5752026B<32MiB. Snapshots
are not hard quotas or exhaustive OS/physical I/O audit. Report wall is not exact
post-push wall. Git traffic is separate from forbidden research-data network.

Only seven allowlist paths, old result prefix preserved, one058 append. No raw
QA/labels/prediction/correctness/source map or data identity hashes, features,
weights/checkpoints or private paths uploaded. Ordinary safe push then STOP;
no automatic059 or background continuation. No innovation certification.

Independent reviewer source (explicit private root argument):

```python
"""Independent stdlib058 review: no tested code, torch, training or inference."""
import csv
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
import random
import struct
import zipfile

root=Path(sys.argv[1]);checks=0
def check(ok):
    global checks
    assert ok;checks+=1
def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
seal=read(root/'input-seal.json');config=read(root/'training-config.json');prior=Path(config['prior'])
for record in seal['assets']:check(sha(record['path'])==record['sha256'])
for record in read(root/'outputs-identity-seal.json')['files']:check(sha(record['path'])==record['sha256'])
source=Path(__file__).parent # not an input lookup; all inputs below use explicit seals
bindings=read(root/'source-bindings.json');groups={s:{x['group_key'] for x in rows} for s,rows in bindings.items()}
check([len(groups[s]) for s in ['train','validation','development_test']]==[16,2,15])
for a,b in [('train','validation'),('train','development_test'),('validation','development_test')]:check(not groups[a]&groups[b])
plan=read(prior/'pilot-input-seal.json')
labels={s:read(prior/(s+'-labels.json')) for s in groups}
for s in groups:
    check([x['labels'] for x in labels[s]]==[x['labels'] for x in plan['selected'][s]])
    check(bindings[s]==[dict(index=i,group_key=x['group_key']) for i,x in enumerate(plan['selected'][s])])
    check(read(root/(s+'-observations.json'))==read(prior/(s+'-observations.json')))
def payloads(path):
    with zipfile.ZipFile(path) as f:return {x.split('/data/',1)[1]:f.read(x) for x in f.namelist() if '/data/' in x}
index=read(prior/'feature-index.json');hindex=read(root/'h-index.json');perms=[[5,4,3,2,1,0],[1,2,3,4,5,0],[2,5,1,4,0,3],[0,2,4,1,3,5]]
for name,entry in index['video'].items():
    original=payloads(prior/'features'/entry['path']);changed=payloads(root/'h-features'/hindex[name]['path'])
    check(len(original)==len(changed)==1)
    raw=next(iter(original.values()));actual=next(iter(changed.values()));check(len(raw)==len(actual)==6*2560*4)
    check(all(math.isfinite(x) for x in struct.unpack('<15360f',raw)))
    rows=[raw[i*10240:(i+1)*10240] for i in range(6)]
    expected=sorted(rows,key=lambda b:(hashlib.sha256(b).digest(),b))
    check(actual==b''.join(expected));check(Counter(rows)==Counter(expected))
    check(sorted(expected,key=lambda b:(hashlib.sha256(b).digest(),b))==expected)
    for permutation in perms:check(sorted([rows[i] for i in permutation],key=lambda b:(hashlib.sha256(b).digest(),b))==expected)
for entry in index['text'].values():
    data=payloads(prior/'features'/entry['path']);check(len(data)==1)
    raw=next(iter(data.values()));check(len(raw)==10240 and all(math.isfinite(x) for x in struct.unpack('<2560f',raw)))
steps=0;loss=[]
for seed in [19,73]:
    paths=[prior/('pretrain-seed'+str(seed)+'.pt'),prior/'training'/('plan-'+str(seed)+'.pt'),root/('initial-seed'+str(seed)+'.pt')]
    check(payloads(paths[0])==payloads(paths[1])==payloads(paths[2]))
    directory=root/'training'/('058-H-seed'+str(seed))
    records=[json.loads(x) for x in (directory/'steps.jsonl').read_text().splitlines()]
    check(records[0]['event']=='STARTED' and records[0]['arm']=='A' and records[-1]['event']=='CLOSED')
    check(read(root/('058-H-seed'+str(seed)+'.claim'))['arm']=='H')
    check((root/'input-seal.json').stat().st_mtime<=(root/('058-H-seed'+str(seed)+'.claim')).stat().st_mtime)
    starts=[x['step'] for x in records if x['event']=='STEP_STARTED'];closed=[x for x in records if x['event']=='STEP_CLOSED']
    check(starts==list(range(250)) and [x['step'] for x in closed]==starts);check(all(math.isfinite(x['loss']) for x in closed))
    check((directory/'final.pt').is_file());steps+=len(closed)
    loss.append(dict(seed=seed,steps=len(closed),first=closed[0]['loss'],last=closed[-1]['loss'],minimum=min(x['loss'] for x in closed),maximum=max(x['loss'] for x in closed)))
check(steps==500)
old=read(root/'a-cached-sealed.json');new=read(root/'h-outputs-sealed.json')
check(len(old)==len(new)==408);check(old==[x for x in read(prior/'head-outputs-sealed.json') if x['arm']=='A'])
look={}
for row in old+new:
    key=(row['split'],'A_CACHED' if row['arm']=='A' else 'H',str(row['seed']),row['index'],row['video'],row['question'])
    check(key not in look);look[key]=row
four={};expected={};integers=[]
for s,n in [('train',25),('validation',2),('development_test',24)]:
    for seed in ['19','73']:
        for arm in ['A_CACHED','H']:
            values=[];correct_count=0;vp=qp=0
            for i in range(n):
                c={}
                for vi in [0,1]:
                    for qi in [0,1]:
                        row=look[(s,arm,seed,i,vi,qi)];check(row['status']=='CLOSED' and row['prediction'] in [0,1])
                        c[vi,qi]=int(row['prediction']==labels[s][i]['labels'][vi][qi]);integers.append((s,arm,seed,i,vi,qi,c[vi,qi]))
                correct_count+=sum(c.values());values.append(int(sum(c.values())==4));vp+=sum(c[0,q]*c[1,q] for q in [0,1]);qp+=sum(c[v,0]*c[v,1] for v in [0,1])
            four[s,arm,seed]=values;expected[s,arm,seed]=dict(n_instances=n,n_cells=4*n,complete_cells=4*n,correct_cells=correct_count,video_pair_correct=vp,question_pair_correct=qp,four_way_correct=sum(values),failed_cells=0,invalid_cells=0,not_run_cells=0)
with open(root/'condition-summary.csv',newline='') as f:conditions=list(csv.DictReader(f))
check(len(conditions)==12)
for row in conditions:
    for key,value in expected[row['split'],row['arm'],row['seed']].items():check(int(row[key])==value)
    check(row['prediction_origin']==('057_CACHED' if row['arm']=='A_CACHED' else '058_NEW'))
scored=read(root/'score-integers.json');check(sorted(integers)==sorted((x['split'],x['arm'],str(x['seed']),x['index'],x['video'],x['question'],x['correct']) for x in scored))
group_ids={}
for row in bindings['development_test']:group_ids.setdefault(row['group_key'],[]).append(row['index'])
with open(root/'paired-summary.csv',newline='') as f:pairs=list(csv.DictReader(f))
check(len(pairs)==2);net=[]
for row in pairs:
    a=four['development_test','A_CACHED',row['seed']];h=four['development_test','H',row['seed']]
    ao=sum(x==1 and y==0 for x,y in zip(a,h));ho=sum(x==0 and y==1 for x,y in zip(a,h));bc=sum(x==y==1 for x,y in zip(a,h));bw=sum(x==y==0 for x,y in zip(a,h))
    check([int(row[x]) for x in ['a_only','h_only','both_correct','both_wrong','unknown']]==[ao,ho,bc,bw,0]);check(int(row['net_instances'])==ao-ho);net.append(ao-ho)
    check(abs(float(row['delta_four_way_pp'])-100*(ao-ho)/24)<1e-10)
    rng=random.Random(55058);keys=sorted(group_ids);values=[]
    for _ in range(10000):
        selected=[keys[int(rng.random()*15)] for _ in range(15)];ids=sum((group_ids[k] for k in selected),[])
        values.append(100*sum(a[i]-h[i] for i in ids)/len(ids))
    values.sort()
    for field,p in [('bootstrap_low_pp',.025),('bootstrap_high_pp',.975)]:
        position=9999*p;lo=math.floor(position);hi=math.ceil(position)
        wanted=values[lo]*(hi-position)+values[hi]*(position-lo) if hi!=lo else values[lo]
        check(abs(float(row[field])-wanted)<1e-9)
score=read(root/'scoring-summary.json');check(score['gate']==all(x>=2 for x in net));check(score['status']=='ORDER_BENEFIT_DEVELOPMENT_SIGNAL')
check(len(score['source_profile'])==30)
for row in score['source_profile']:
    key=sorted(group_ids)[int(row['source'][1:])-1];ids=group_ids[key];a=four['development_test','A_CACHED',str(row['seed'])];h=four['development_test','H',str(row['seed'])]
    check(row['n']==len(ids));check(row['a_only']==sum(a[i]==1 and h[i]==0 for i in ids));check(row['h_only']==sum(a[i]==0 and h[i]==1 for i in ids))
    check(row['both_correct']==sum(a[i]==h[i]==1 for i in ids));check(row['both_wrong']==sum(a[i]==h[i]==0 for i in ids));check(row['net']==sum(a[i]-h[i] for i in ids))
for path in root.glob('*-job.json'):
    job=read(path);check(job['active']==0 and job['exit_code']==0 and not job['killed'] and job['peak_commit']<8*1024**3)
result=dict(status='PASS',checks=checks,steps=steps,net_instances=net,loss_summary=loss,transform_videos=102,text_unchanged=54,
    old_asset_hashes_verified=len(seal['assets']),scope='New/old sealed CPU tensors, predictions, label bindings, tables and logs; no model/training/media/GPU/network repeated')
with open(root/'independent-review.json','x') as f:json.dump(result,f,indent=2)
print(json.dumps(result))

```

Additional independent stdlib checkpoint-storage review:4 checks PASS. Each
final head has exactly356673 finite float32 storage values, confirming the
actual parameter count separately from training metadata. No model import or
forward/update. Its extra owned Job is included in the resources JSON.

A delivery-text formatting read initially used the host default GBK and failed;
explicit UTF-8 corrected it. No training/scoring configuration was rerun.
