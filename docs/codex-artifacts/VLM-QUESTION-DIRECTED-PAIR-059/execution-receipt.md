# 059 execution receipt

2026-10-30 Asia/Shanghai. **COMPLETE_CPU_2X2_EXPERIMENT / STOP_THIS_MECHANISM.**

Clean independent docs status/fetch/ff-only advanced to ee35d6b41343cf39e18cf9e433384577b5831d40.
AGENTS/059 contract/058 disposition read in full; current059/058 board/overview
and complete057/058 result entries checked, results searched for059. Sole
unreported READY059. Read required056head/057training/058input+role logic; old
code not modified or invoked as a task. Exact057 registered root closed,
training Job active0, new059 root exclusively created. Initial disk free
345615638528B>1GiB. No unrelated scans or old task reexecution.

Input preparation348checksPASS:102finite CPUfloat32 V[6,2560],54q[2560], original
25/2/24 instance/cell order, participant groups16/2/15 disjoint.170actual reused
old asset hashes match before/after, including feature/index/observations/plans/
code and original output seals. Only those assets were hashed; no ZIP/media/
frames/encoder or Qwen weights.058H view not used.408original A closed outputs
projected, body identity matched057 evaluation/output seal. All original A six
condition rows later matched every count, not only four-way totals.

Group/observation verifier lexically removes51answer arrays before JSON decoding
the mixed old pilot seal. It hands off group bindings separately; training role
reads only original untransformed V/q, independent unlabeled observations, train
labels and initial state/sequence. It does not open A/B0/H outputs, validation/
development labels, source-group tables or mixed answer seal. These are actual
program/file-role boundaries, not OS-level access-audit assertions. Evaluation
labels/A cache were used only by verification/scoring roles, not training.

Two actual original pretrain state/sequence files matched original training plans
tensor-by-tensor; no regenerated replacement. Initial map:video/question unchanged;
hidden.weight=conv.weight[:,:,0],hidden.bias=conv.bias,a/b.weight=slices1/2;
f.weight/bias=mlp.0,output.weight=mlp.2.weight,tau=mlp.2.bias[0]. No transpose,
random replacement or unused padding parameter. Four new heads per seed initialize
identically from this mapping. Mapped plans, code/formulas/input identity sealed
before first configuration STARTED. New per-config initial-used states retained.

Actual model follows fixed r64 pointwise LN/GELU common encoder, no position
encoding/time convolution. All15t<s pairs used. P uses first-order differences,
R antisymmetric products;0uniform1/15 weights/no g in a/b,1±g modulation and
(alpha_t+alpha_s)/5 weights. All pair weights sum1 algebraically. Common alpha/u
and readout still access q in every arm. Normalizer and odd f(o)−f(−o) positive
tau readout exactly fixed; no formula/key/normalization or loss search.

Eight configurations executed seed19 then73, each P0/P1/R0/R1. Each STARTED
preceded three fixed training-instance0 batch4 software calls:original, feature
reversal and repeated-first-vector. All24calls/96cells finite and PASS, no
labels scored and no optimizer update. Maximum reversal residual
7.45058059692e-08, repeated residual0;
configured tolerance1e-5+1e-5*abs(z), repeat1e-6. These are software properties
shared by all arms, not scientific QA or real-video counterfactual tests.

Each config250 STEP_STARTED/STEP_CLOSED with actual forward/BCE/backward, finite
non-None gradients for every parameter, clip/AdamW step;2000total. Same original
250×8 sampled groups,2000group/8000cell exposures per config; parameters356673,
all float32/4threads, BCE mean only, AdamW lr.001/wd.01/betas(.9,.999)/eps1e-8,
clip1. Tau actually used in positive temperature, no canceled output bias.
Only final250th-step checkpoint; no early stop, validation choice, restarts,
extra seed/update or post-STARTED formula repair. Loss ranges/parameter changes
are recorded independently in JSON; they do not establish answer benefit.

1632new per-cell outputs plus checkpoints/code/mapped initial states sealed
before scoring; training Job actualactive0 first. predict(model,V,q) receives
current6×2560 V and current2560q only. No paired output flip/repair or source/
boundary/label inputs. Original A408predictions reused without any A forward.
Scorer after seals read original split labels, retained all2040formal cells,
30conditions/8pairs/2interactions/120anonymous group rows. All complete valid;
failed/INVALID/NOT_RUN/unknown0. No B0 or other old model was run.

Result: R1test7/24,9/24 vs A5/24,7/24 but P1=6/24,12/24; R1−P1=+1/−3 misses
≥2both-seed gate. R1−R0=+7/+9, Delta=+9/−3; second Delta misses≥1. Complete
gateFAIL, scientificNO_SUPPORT_FOR_THIS_DIRECTED_PAIR_RECIPE, STOP_THIS_MECHANISM.
No alternative control/seed is renamed a new contribution and057joint loss
does not resume. Known-used development set, no new/external confirmation.

Independent reviewer5910checksPASS: no tested module import/forward/train/scorer
or extra software forward. It uses torch only for read-only CPU tensor/state
comparison:all old state/sequence copies, exact12-key slice mapping, eight actual
initials identical per seed, every final finite356673-parameter state and L1
change. From recorded software arrays it recomputes parity/zero tolerances and
24call count without replaying forward. Rebuilt2000steps, source separation,
1632new+408cached label joins, all30/8tables,2Delta,120source rows and group
bootstrap10000/Random55059 including joint group sampling for Delta. Raw old
label bindings checked against original057seal after new output sealing.
170old hashes unchanged; no ZIP/media/model/decoder/network action repeated.

Resources: training+prediction+scoring Job outer
39.328s/1200s; other prep/review
5.390s/600s; max Job commit
832827392B/8GiB. Four owned Jobs active0/exit0/no kill,
active-process limit4. CUDA_VISIBLE_DEVICES empty; CUDA uninitialized checked
after import and at Job endings. GPU/Qwen/encoder load or forward/backward/
update, feature extraction,nvidia-smi,media decode,research-data network and
environment modification0. Newhead software forward24, research update2000,
synthetic updates0. Git synchronization is separate from research-data traffic.

Parent elapsed at report 731.980s/5400s;
new root snapshot 72files/29783141B<1024/512MiB,
all final/initial/checkpoint/plan copies 28671336B<32MiB.
Snapshot is not a hard filesystem quota or exhaustive OS/physical-I/O audit;
report wall is not exact post-push elapsed. No stage failed or was retried.

Seven allowlist paths only, unchanged historical results prefix and one059
append. QA/labels/logits/predictions/correctness/source maps/identity hashes,
features/media/weights/checkpoints and private paths remain private. Ordinary
safe push then STOP; no automatic060 or background continuation. Core novelty
remains unresolved, stopped structure not universal temporal-learning verdict.

Independent reviewer source (explicit private-root argument):

```python
"""059 independent state/file/arithmetic review; no tested code/model forward."""
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import random
import torch

root=Path(sys.argv[1]);checks=0
torch.set_num_threads(4);torch.set_num_interop_threads(1)
def check(ok):
    global checks
    assert ok;checks+=1
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return torch.load(path,map_location='cpu',weights_only=True)
check(not torch.cuda.is_initialized())
seal=read(root/'input-seal.json');config=read(root/'training-config.json');prior=Path(config['prior'])
for row in seal['assets']:check(sha(row['path'])==row['sha256'])
for row in read(root/'outputs-identity-seal.json')['files']:check(sha(row['path'])==row['sha256'])
bindings=read(root/'source-bindings.json');groups={s:{r['group_key'] for r in rows} for s,rows in bindings.items()}
check([len(groups[s]) for s in ['train','validation','development_test']]==[16,2,15])
for a,b in [('train','validation'),('train','development_test'),('validation','development_test')]:check(not groups[a]&groups[b])
source=read(prior/'pilot-input-seal.json')['selected'];labels={s:read(prior/(s+'-labels.json')) for s in groups}
for split,n in [('train',25),('validation',2),('development_test',24)]:
    check(len(source[split])==n)
    check([x['labels'] for x in labels[split]]==[x['labels'] for x in source[split]])
    check(bindings[split]==[dict(index=i,group_key=r['group_key']) for i,r in enumerate(source[split])])
    check(read(root/(split+'-observations.json'))==read(prior/(split+'-observations.json')))
for kind,shape in [('video',(6,2560)),('text',(2560,))]:
    for row in config['features'][kind].values():
        t=load(prior/'features'/row['path']);check(t.dtype==torch.float32 and t.device.type=='cpu' and t.shape==shape and bool(torch.isfinite(t).all()))
steps=0;software=0;losses=[];state_results=[];symmetry=[]
for seed in [19,73]:
    original=load(prior/('pretrain-seed'+str(seed)+'.pt'));training_plan=load(prior/'training'/('plan-'+str(seed)+'.pt'));copied=load(root/('original-seed'+str(seed)+'.pt'))
    for other in [training_plan,copied]:
        check(torch.equal(original['sequence'],other['sequence']))
        check(set(original['state'])==set(other['state']) and all(torch.equal(original['state'][k],other['state'][k]) for k in original['state']))
    old=original['state'];slices=old['conv.weight'].unbind(-1)
    expected={'video.weight':old['video.weight'],'video.bias':old['video.bias'],'question.weight':old['question.weight'],'question.bias':old['question.bias'],
        'hidden.weight':slices[0],'hidden.bias':old['conv.bias'],'a.weight':slices[1],'b.weight':slices[2],
        'f.weight':old['mlp.0.weight'],'f.bias':old['mlp.0.bias'],'out.weight':old['mlp.2.weight'],'tau':old['mlp.2.bias'].reshape(())[()]}
    mapped=load(root/config['plans'][str(seed)]['path']);check(torch.equal(mapped['sequence'],original['sequence']))
    check(mapped['sequence'].shape==(250,8) and int(mapped['sequence'].min())>=0 and int(mapped['sequence'].max())<25)
    check(set(mapped['state'])==set(expected))
    for name,value in expected.items():check(torch.equal(value,mapped['state'][name]))
    check(sum(x.numel() for x in expected.values())==356673)
    for arm in ['P0','P1','R0','R1']:
        directory=root/'training'/('059-'+arm+'-seed'+str(seed));initial=load(directory/'initial-used.pt');final=load(directory/'final.pt')
        check(set(initial)==set(final)==set(expected));check(sum(x.numel() for x in final.values())==356673)
        for key,value in expected.items():
            check(torch.equal(initial[key],value));check(final[key].dtype==torch.float32 and bool(torch.isfinite(final[key]).all()))
        change=sum(float((final[k]-expected[k]).abs().sum()) for k in expected)
        report=next(x for x in read(root/'training-summary.json') if x['arm']==arm and x['seed']==seed)
        check(abs(report['parameter_l1_change']-change)<1e-5 and report['parameters']==356673)
        state_results.append(dict(arm=arm,seed=seed,parameters=356673,initial_mapping_equal=True,parameter_l1_change=change))
        records=[json.loads(x) for x in (directory/'steps.jsonl').read_text(encoding='utf-8').splitlines()]
        check(records[0]['event']=='STARTED' and records[0]['arm']==arm and records[-1]['event']=='CLOSED')
        check([x['step'] for x in records if x['event']=='STEP_STARTED']==list(range(250)))
        closed=[x for x in records if x['event']=='STEP_CLOSED'];check([x['step'] for x in closed]==list(range(250)))
        check(all(math.isfinite(x['loss']) for x in closed));steps+=len(closed)
        losses.append(dict(arm=arm,seed=seed,steps=len(closed),first=closed[0]['loss'],last=closed[-1]['loss'],minimum=min(x['loss'] for x in closed),maximum=max(x['loss'] for x in closed)))
        events=[json.loads(x) for x in (directory/'software.jsonl').read_text(encoding='utf-8').splitlines()]
        check([x['kind'] for x in events]==['original','reversed','repeated_first'] and all(x['batch_cells']==4 for x in events))
        evidence=read(directory/'software-check.json');check(evidence['status']=='PASS' and evidence['forward_calls']==3)
        check(all(len(evidence[k])==4 for k in ['original','reversed','repeated']))
        check(all(math.isfinite(v) for k in ['original','reversed','repeated'] for v in evidence[k]))
        check(all(abs(a+b)<=1e-5+1e-5*abs(a) for a,b in zip(evidence['original'],evidence['reversed'])))
        check(all(abs(x)<=1e-6 for x in evidence['repeated']));software+=3
        symmetry.append(dict(arm=arm,seed=seed,reverse_error=evidence['reverse_error'],repeated_error=evidence['repeated_error']))
check(steps==2000 and software==24);check(read(root/'outputs-identity-seal.json')['software_cells']==96)
old=read(root/'a-cached-sealed.json');new=read(root/'new-outputs-sealed.json');check(len(old)==408 and len(new)==1632)
check(old==[x for x in read(prior/'head-outputs-sealed.json') if x['arm']=='A'])
lookup={}
for row in old+new:
    key=(row['split'],'A_CACHED' if row['arm']=='A' else row['arm'],str(row['seed']),row['index'],row['video'],row['question'])
    check(key not in lookup);lookup[key]=row
four={};expected_counts={};integers=[]
for split,n in [('train',25),('validation',2),('development_test',24)]:
    for seed in ['19','73']:
        for arm in ['A_CACHED','P0','P1','R0','R1']:
            values=[];total=vp=qp=0
            for i in range(n):
                flags={}
                for vi in [0,1]:
                    for qi in [0,1]:
                        row=lookup[split,arm,seed,i,vi,qi];check(row['status']=='CLOSED' and row['prediction'] in [0,1])
                        flags[vi,qi]=int(row['prediction']==labels[split][i]['labels'][vi][qi]);integers.append((split,arm,seed,i,vi,qi,flags[vi,qi]))
                total+=sum(flags.values());values.append(int(sum(flags.values())==4));vp+=sum(flags[0,q]*flags[1,q] for q in [0,1]);qp+=sum(flags[v,0]*flags[v,1] for v in [0,1])
            four[split,arm,seed]=values;expected_counts[split,arm,seed]=dict(n_instances=n,n_cells=4*n,complete_cells=4*n,correct_cells=total,video_pair_correct=vp,question_pair_correct=qp,four_way_correct=sum(values),failed_cells=0,invalid_cells=0,not_run_cells=0,unknown_cells=0)
with open(root/'condition-summary.csv',encoding='utf-8',newline='') as f:conditions=list(csv.DictReader(f))
check(len(conditions)==30)
for row in conditions:
    for key,want in expected_counts[row['split'],row['arm'],row['seed']].items():check(int(row[key])==want)
    check(row['prediction_origin']==('057_CACHED' if row['arm']=='A_CACHED' else '059_NEW'))
recorded=read(root/'score-integers.json');check(sorted(integers)==sorted((x['split'],x['arm'],str(x['seed']),x['index'],x['video'],x['question'],x['correct']) for x in recorded))
ids={}
for row in bindings['development_test']:ids.setdefault(row['group_key'],[]).append(row['index'])
def interval(group_net):
    rng=random.Random(55059);keys=sorted(ids);values=[]
    for _ in range(10000):
        picked=[keys[int(rng.random()*15)] for _ in range(15)];values.append(100*sum(group_net[g] for g in picked)/sum(len(ids[g]) for g in picked))
    values.sort();out=[]
    for p in [.025,.975]:
        pos=9999*p;lo=math.floor(pos);hi=math.ceil(pos);out.append(values[lo] if lo==hi else values[lo]*(hi-pos)+values[hi]*(pos-lo))
    return out
with open(root/'paired-summary.csv',encoding='utf-8',newline='') as f:pairs=list(csv.DictReader(f))
check(len(pairs)==8)
for row in pairs:
    r=four['development_test','R1',row['seed']];c=four['development_test',row['comparator'],row['seed']]
    ro=sum(x==1 and y==0 for x,y in zip(r,c));co=sum(x==0 and y==1 for x,y in zip(r,c));bc=sum(x==y==1 for x,y in zip(r,c));bw=sum(x==y==0 for x,y in zip(r,c))
    check([int(row[k]) for k in ['r1_only','comparator_only','both_correct','both_wrong','unknown']]==[ro,co,bc,bw,0]);check(int(row['net_instances'])==ro-co)
    check(abs(float(row['delta_four_way_pp'])-100*(ro-co)/24)<1e-10)
    low,high=interval({g:sum(r[i]-c[i] for i in items) for g,items in ids.items()})
    check(abs(float(row['bootstrap_low_pp'])-low)<1e-9 and abs(float(row['bootstrap_high_pp'])-high)<1e-9)
score=read(root/'scoring-summary.json');deltas=[]
for row in score['interactions']:
    seed=str(row['seed']);r1=four['development_test','R1',seed];r0=four['development_test','R0',seed];p1=four['development_test','P1',seed];p0=four['development_test','P0',seed]
    net={g:sum(r1[i]-r0[i]-p1[i]+p0[i] for i in items) for g,items in ids.items()};delta=sum(net.values());deltas.append(delta)
    check(row['delta_instances']==delta and abs(row['delta_pp']-100*delta/24)<1e-10)
    low,high=interval(net);check(abs(row['bootstrap_low_pp']-low)<1e-9 and abs(row['bootstrap_high_pp']-high)<1e-9)
for row in score['source_profile']:
    g=sorted(ids)[int(row['source'][1:])-1];items=ids[g];r=four['development_test','R1',str(row['seed'])];c=four['development_test',row['comparator'],str(row['seed'])]
    check(row['n']==len(items));check(row['r1_only']==sum(r[i]==1 and c[i]==0 for i in items));check(row['comparator_only']==sum(r[i]==0 and c[i]==1 for i in items))
    check(row['both_correct']==sum(r[i]==c[i]==1 for i in items));check(row['both_wrong']==sum(r[i]==c[i]==0 for i in items));check(row['net']==sum(r[i]-c[i] for i in items))
check(len(score['source_profile'])==120)
gate=all(int(next(x for x in pairs if x['seed']==s and x['comparator']==c)['net_instances'])>=threshold for s in ['19','73'] for c,threshold in [('A_CACHED',2),('P1',2),('R0',1)]) and all(d>=1 for d in deltas)
check(score['complete'] and score['gate']==gate);check(score['status']==('DIRECTED_PAIR_DEVELOPMENT_SIGNAL' if gate else 'NO_SUPPORT_FOR_THIS_DIRECTED_PAIR_RECIPE'))
for path in root.glob('*-job.json'):
    job=read(path);check(job['active']==0 and job['exit_code']==0 and not job['killed'] and job['peak_commit']<8*1024**3)
check(not torch.cuda.is_initialized())
result=dict(status='PASS',checks=checks,steps=steps,software_forwards=software,software_cells=4*software,gate=gate,delta_instances=deltas,
    losses=losses,states=state_results,symmetry=symmetry,old_assets_verified=len(seal['assets']),cuda_initialized=False,
    scope='Independent CPU state/recorded-software/file/label/arithmetic checks only; no tested module imports or model forward/training; no data/GPU/media work')
with open(root/'independent-review.json','x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k not in ['losses','states','symmetry']}))

```
