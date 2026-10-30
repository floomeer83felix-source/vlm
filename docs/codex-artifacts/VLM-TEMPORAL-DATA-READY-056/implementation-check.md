# 056 implementation and independent review

Actual CPU software checks:128 fixture assertions PASS,8 optimizer updates total
(A/V/S/I×seed19,73 once each), plus7 no-update checks PASS. All eight synthetic
heads have30145 parameters at Dv8,Dq10. A CPU-only architecture instantiation at
Dv=Dq=2560 has356673 parameters per frozen formula; these are fixture dimensions,
not measured Qwen feature dimensions. All parameter tensors had finite nonzero
gradients and changed after their one clipped AdamW update. No dummy parameters.

Full shared state equality and initial-logit equality were checked per seed.
Each arm exposed the same8 sampled groups/32 cells. The shared sampler produces
250×8 with-replacement groups, but only the first batch was updated in software
fixtures. S canonicalizes according to unchanged labels and circularly assigns
columns; all32 logits are used once, labels remain positive/negative/negative/
positive. V/S/I objectives differ from BCE. Independent Python scalar formulas
reconstructed A/V/I and S losses to1e-6 without optimizer calls.

Single-cell predict accepts only(model,V,q); invalid/nonfinite input is rejected.
An invalid-arm explicit train() call persisted STARTED then FAILED and made0
updates. Existing output directories cannot restart a configuration. Injected
failure fixtures remain on disk. No checkpoint was saved or used for science.
Full250-step runtime/checkpoint and real interruption handling remain untested.

Data module implements fixed revision acquisition, persistent single-attempt
body ledgers/caps, publisher hashes, limited tar reading, original XML joins,
fixed participant splits, gated event download, limited ZIP extraction/CRC,
bounded CPU nearest-frame caching, and separate-label handoff. Only acquisition,
annotation integrity, join and split paths were exercised on real metadata;
media, ZIP and real decode/cache routines remain runtime-unverified. The broader
data pipeline is PARTIAL, not DATA_AND_HEAD_READY.

Independent source/split review:522 assertions PASS; no tested implementation
imports or new network/media/decode. Reconstructed133 joins,51 unique pairs,
all exclusion counts, participant memberships, hash allocation, caps and no
cross-split groups. Checked published archive checksums, new-body identities,
metadata accounting and fixture-count declarations. This verifies ANNOTATION_JOIN
consistency; physical/kitchen/media/feature independence is not certified.

Independent no-update software check source:

```python
import importlib.util
import json
import math
from pathlib import Path
import sys
import time

root=Path(sys.argv[1])
path=Path(sys.argv[2])
spec=importlib.util.spec_from_file_location('head056',path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t=m.torch; t.set_num_threads(1); t.set_num_interop_threads(1)
checks=0
def check(ok):
    global checks
    assert ok; checks+=1
z=t.linspace(-2,3,32).reshape(8,2,2); y=t.tensor([[[1.,0.],[0.,1.]],[[0.,1.],[1.,0.]]]*4)
flat=z.tolist(); truth=y.tolist()
softplus=lambda x:math.log1p(math.exp(x))
bce=sum(softplus(-(2*truth[k][i][j]-1)*flat[k][i][j]) for k in range(8) for i in range(2) for j in range(2))/32
video=sum(softplus(1-(2*truth[k][0][j]-1)*(flat[k][0][j]-flat[k][1][j])/2) for k in range(8) for j in range(2))/16
joint=0
for k in range(8):
    margins=[(2*truth[k][i][j]-1)*flat[k][i][j] for i in range(2) for j in range(2)]
    c=sum(margins)/4; joint+=(softplus(1-c)+sum((x-c)**2 for x in margins)/4)/8
for arm,expected in [('A',bce),('V',bce+.25*video),('I',bce+.25*joint)]:
    check(abs(float(m.objective(z,y,arm))-expected)<1e-6)
canonical=[]
for k in range(8):
    values=[flat[k][i][j] for i in range(2) for j in range(2)]
    canonical.append(values if truth[k][0][0]==1 else [values[j] for j in [1,0,3,2]])
pseudo=[[canonical[(k+j)%8][j] for j in range(4)] for k in range(8)]
sj=0
for values in pseudo:
    margins=[values[j]*[1,-1,-1,1][j] for j in range(4)]; c=sum(margins)/4
    sj+=(softplus(1-c)+sum((x-c)**2 for x in margins)/4)/8
check(abs(float(m.objective(z,y,'S'))-(bce+.25*sj))<1e-6)
try: m.train(t.zeros(1,2,6,8),t.zeros(1,2,10),y[:1],'BAD',19,{},t.zeros(250,8,dtype=t.int64),root/'failure-entry',time.monotonic()+10)
except ValueError: check(True)
events=[json.loads(x) for x in (root/'failure-entry/steps.jsonl').read_text().splitlines()]
check([x['event'] for x in events]==['STARTED','FAILED'])
check(not t.cuda.is_initialized())
with open(root/'additional-checks.json','x') as f:json.dump(dict(status='PASS',checks=checks,optimizer_steps=0),f)
print(checks)

```

Independent stdlib data reviewer source (root is the caller-supplied private root):

```python
"""Stdlib reconstruction; imports neither tested module nor torch."""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import sys
import tarfile
import xml.etree.ElementTree as ET

root=Path(sys.argv[1]); checks=0
def check(ok):
    global checks
    assert ok; checks+=1
checksums=dict(line.split()[::-1] for line in (root/'breakfast_SHA256SUMS.body').read_text().splitlines())
index={}; expanded=0
for level in ['coarse','fine']:
    name='segmentation_'+level+'.tar.gz'; path=root/('breakfast_'+name.replace('.','_')+'.body')
    check(hashlib.sha256(path.read_bytes()).hexdigest()==checksums[name])
    with tarfile.open(path) as archive:
        for member in archive:
            if not member.isfile(): continue
            expanded+=member.size
            if level=='coarse' and member.name.endswith('.xml'):
                index.setdefault(Path(member.name).stem,[]).append((member.name,ET.fromstring(archive.extractfile(member).read())))
check(expanded<64*1024**2)
rows=json.loads((root/'prior_dybench_annotations.body').read_bytes()); pairs=defaultdict(list)
for row in rows:
    if row['source_subcategory']=='Breakfast': pairs[row['video'].replace('_reversed.mp4','.mp4')].append(row)
source=json.loads((root/'source-table.json').read_text()); summary=json.loads((root/'source-summary.json').read_text())
norm=lambda x:' '.join(x.replace('_',' ').split())
counts=Counter(); qualified={}; joins=0
for filename,pair in sorted(pairs.items()):
    lines=pair[0]['question'].splitlines(); reason=None
    if len(pair)!=2 or len({x['video'] for x in pair})!=2 or pair[0]['question']!=pair[1]['question']:reason='PAIR_STRUCTURE'
    elif len(lines)!=4 or not lines[1].startswith('Action 1. ') or not lines[2].startswith('Action 2. ') or lines[3]!='Please output their order.' or norm(lines[1][10:])==norm(lines[2][10:]):reason='EVENT_PARSE'
    elif len(index.get(Path(filename).stem,[]))!=1:reason='ORIGINAL_RECORDING_NOT_UNIQUE'
    else:
        _,tree=index[Path(filename).stem][0]
        participant=tree.attrib['motionSequenceName']; pieces=Path(filename).stem.split('_')
        check(pieces[0]==participant==pieces[2]);check(tree.attrib['motionFile'].replace('\\','/').startswith(participant+'/'))
        joins+=1
        seg=list(tree.iter('MotionLabel'))
        a=[i for i,x in enumerate(seg) if norm(x.attrib['name'])==norm(lines[1][10:])]
        b=[i for i,x in enumerate(seg) if norm(x.attrib['name'])==norm(lines[2][10:])]
        if len(a)!=1 or len(b)!=1:reason='EVENT_MISSING_OR_REPEATED'
        elif abs(a[0]-b[0])<2 or not (int(seg[a[0]].attrib['endPoint'])<int(seg[b[0]].attrib['startPoint']) or int(seg[b[0]].attrib['endPoint'])<int(seg[a[0]].attrib['startPoint'])):reason='NOT_NONADJACENT_STRICT_ORDER'
        else:
            original=next(x for x in pair if not x['video'].endswith('_reversed.mp4'))
            answer=int(original['answer']=='First action 1, then action 2')
            check({x['answer'] for x in pair}=={'First action 1, then action 2','First action 2, then action 1'})
            check((int(seg[a[0]].attrib['startPoint'])<int(seg[b[0]].attrib['startPoint']))==bool(answer))
            qualified[Path(filename).stem]=(participant,[[answer,1-answer],[1-answer,answer]])
    if reason:counts[reason]+=1
check(len(pairs)==147);check(joins==summary['recording_joins']==133)
check(dict(counts)==summary['exclusions']);check(len(qualified)==summary['qualified_before_split']==51)
for record in source['qualified']:
    check((record['participant'],record['labels'])==qualified[record['recording']])
    check(record['group_key']=='Breakfast/participant='+record['participant'])
groups=defaultdict(list)
for key,(participant,labels) in qualified.items():groups['Breakfast/participant='+participant].append(key)
selected={x:[] for x in ['train','validation','development_test']}; selected_groups={x:[] for x in selected}
caps={'train':96,'validation':16,'development_test':48}
for group in sorted(groups,key=lambda x:hashlib.sha256(('VLM055/'+x).encode()).digest()):
    bucket=int.from_bytes(hashlib.sha256(('VLM055/'+group).encode()).digest()[:4],'big')%10
    split='train' if bucket<=5 else 'validation' if bucket==6 else 'development_test'
    if len(selected[split])+len(groups[group])<=caps[split]:selected[split]+=groups[group];selected_groups[split].append(group)
plan=json.loads((root/'candidate-split.json').read_text())
for split in selected:
    check(set(selected[split])=={x['recording'] for x in plan['selected'][split]})
    check(len(selected[split])==summary['split_instances'][split]);check(len(selected_groups[split])==summary['split_groups'][split])
for a,b in [('train','validation'),('train','development_test'),('validation','development_test')]:check(not set(selected_groups[a])&set(selected_groups[b]))
check(not summary['media_permitted'] and not plan['frozen_for_media'])
net=[json.loads(x) for x in (root/'network.jsonl').read_text().splitlines()]
check(not any(x.get('category')=='media' for x in net));check(sum(x.get('bytes',0) for x in net)<16*1024**2)
starts=[x['key'] for x in net if x['event']=='STARTED'];check(len(starts)==len(set(starts)))
for record in net:
    if record['event']=='CLOSED':check(hashlib.sha256((root/(record['key']+'.body')).read_bytes()).hexdigest()==record['sha256'])
old=json.loads((root/'prior-copies.json').read_text())
check(old['bytes']<8*1024**2)
for file in old['files']:check(hashlib.sha256((root/('prior_'+file['name'])).read_bytes()).hexdigest()==file['sha256'])
fixture=json.loads((root/'implementation.json').read_text()); check(fixture['fixture_optimizer_steps']==8)
for record in fixture['records']:
    check(record['parameters']==30145 and record['fixture_updates']==1 and record['exposed_cells']==32)
check(not fixture['cuda_initialized'] and fixture['research_optimizer_steps']==0)
for jobfile in root.glob('*-job.json'):
    job=json.loads(jobfile.read_text());check(job['active']==0 and job['exit_code']==0 and not job['killed'])
result=dict(status='PASS',checks=checks,original_joins=joins,qualified=len(qualified),split_instances={k:len(v) for k,v in selected.items()},exclusions=dict(counts),
            metadata_body_bytes=sum(x.get('bytes',0) for x in net),annotation_expanded_bytes=expanded,
            boundary='ANNOTATION_JOIN only; media/cache/actual Qwen features not inspected or certified')
with open(root/'independent-review.json','x') as f:json.dump(result,f,indent=2)
print(json.dumps(result))

```
