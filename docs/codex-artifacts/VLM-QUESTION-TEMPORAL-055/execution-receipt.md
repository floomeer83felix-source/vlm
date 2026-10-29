# 055 execution receipt

**2026-10-29 Asia/Shanghai — PARTIAL_SAFE_STOP_INPUT_NOT_QUALIFIED.**

Clean independent documentation checkout, ordinary fetch and safe ff-only check
matched main `54c2783dfd210a0cccd532f17ae1376c95606889`; current board names only
055 READY and the complete results-file ID search found no prior 055 entry.
AGENTS, task README, frozen protocol and 054 disposition were read in full.
The three large historical coordination files were inspected in current relevant
sections and searched; their requested complete historical reading was not
finished. This procedural limitation is disclosed, not described as full review.
The user authorized the exact private run root after project-local search.
No previous 055 directory or matching Python job was found; root creation was
exclusive. Original experiment directory was not reset, cleaned or uploaded.

Five owned Windows Job runs performed bounded metadata acquisition, references,
file-size inspection, qualification and independent stdlib review. They reused
only the existing 040 platform Job/Process definitions; no historical main/tests
or research jobs ran. Each child was created suspended and assigned before
resume, with 16 GiB Job/process commit limit and no new dependencies. Metadata
code uses a single Python control thread and no native numerical libraries;
OMP/MKL were set to one. No OS-wide thread-count certification is claimed.

15 unique persistent STARTED requests, 15 HTTP200 closures, zero failed requests
and no retries. Redirect response bodies and successful bodies were charged:
1,098,994 bytes total, below 16 MiB. Pinned dataset/code revisions are in the JSON.
Public CRPO README at its pinned revision was a generic website-template README,
so it did not supply the missing source map. No unrelated linked template pages
were followed. No raw annotations or exact source identities are delivered.

DyBench's only event-sequence media object exceeds both authorized media caps;
no individual video objects or explicit original-recording map were found in
the retrieved fixed official material. The executor did not infer original
recording independence from filenames. Per README section 1, required-input/
source qualification failure stopped the run before media/GPU. This is not a
proof that all possible future retrieval/provenance routes are impossible.

Actual resources at report: preparation Job outer total
25.077s /7200s, peak Job commit
17600512 bytes /16GiB. All five Jobs active0, exit0,
no owned kill. GPU outer0, model loads/calls/forward0, media0, decode0,
training/evaluation0, backward/optimizer.step0, checkpoints0. GPU lock was never
acquired and no peer lock/process was modified. Existing model and interpreter
entry files were confirmed; model identity and installed processor were not
validated because the earlier data gate failed. Parent elapsed at report
293.856s /14400s; this is not an exact post-push wall measurement.
Initial free disk 349198016512 bytes exceeded 4GiB.
Private output snapshot 42 files,
1179456 bytes, below 2048 files/3GiB. Directory
snapshots are not a filesystem hard quota; OS/import/control I/O is not exhaustive.

Independent review: **839 assertions PASS**, from acquired bodies, ledger and
new qualification JSON, without importing the tested parser/aggregator. It
reconstructed pair structure, counts, subcategories, response byte total and
body integrity, archive cap failure, TimeBlind tag count and first four Job
closures. Its own fifth closure was subsequently checked by the delivery role.
This is metadata consistency only, not physical provenance or scientific scoring.
No CPU fixture was used as experimental evidence. No head implementation is
delivered because the mandatory prerequisite stopped before that stage; seven
of the eight allowed paths are used, with question_temporal_055.py NOT_IMPLEMENTED.

Independent reviewer source (argument is a private output directory; raw input
values/results stay private):

```python
"""Independent stdlib reconstruction; does not import data055 or its aggregates."""
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

root = Path(sys.argv[1])
checks = 0
def check(value):
    global checks
    assert value
    checks += 1

rows = json.loads((root/'dybench_annotations.body').read_bytes())
counts = Counter(x['source_subcategory'] for x in rows)
members = {}
for x in rows:
    name = x['video']
    if name.endswith('_reversed.mp4'):
        name = name[:-len('_reversed.mp4')]+'.mp4'
    members.setdefault((x['source_subcategory'], name), []).append(x)
consistent = 0
unresolved = 0
for pair in members.values():
    check(len(pair)==2)
    question = pair[0]['question']
    parts = question.split('\n')
    ok = (len(parts)==4 and parts[1].startswith('Action 1. ') and
          parts[2].startswith('Action 2. ') and parts[3]=='Please output their order.' and
          parts[1][10:].strip()!=parts[2][10:].strip() and pair[1]['question']==question)
    if not ok:
        unresolved += 1
        continue
    check({x['answer'] for x in pair} == {'First action 1, then action 2', 'First action 2, then action 1'})
    consistent += 1
report = json.loads((root/'qualification.json').read_text())
check(len(rows)==report['dybench']['rows'])
check(len(members)==report['dybench']['candidate_pairs'])
check(dict(counts)==report['dybench']['category_rows'])
check(consistent==report['dybench']['pair_audit']['annotation_pair_consistent'])
check(unresolved==report['dybench']['pair_audit']['unresolved_events_or_question'])
network = [json.loads(line) for line in (root/'network.jsonl').read_text().splitlines()]
starts = [x['key'] for x in network if x['event']=='STARTED']
closes = [x for x in network if x['event']=='CLOSED']
check(len(starts)==len(set(starts))==len(closes))
check(sum(x.get('bytes',0) for x in network)==report['network']['metadata_bytes']<16*1024**2)
for event in closes:
    check(event['status']==200)
    check(hashlib.sha256((root/(event['key']+'.body')).read_bytes()).hexdigest()==event['sha256'])
tree = json.loads((root/'dybench_file_sizes.body').read_bytes())
size = [x['size'] for x in tree if x['path']=='video/event_sequence.zip'][0]
check(size==report['dybench']['archive_bytes']>1536*1024**2>64*1024**2)
files = json.loads((root/'dybench_revision.json').read_text())['files']
check(not any(x.lower().endswith('.mp4') for x in files))
check(set(k for x in rows for k in x)==set(report['dybench']['annotation_fields']))
tags = json.loads((root/'timeblind_code_tags_json.body').read_bytes())
tb = [json.loads(x) for x in (root/'timeblind_annotations.body').read_text().splitlines()]
check(len(tb)==2400)
check(sum(x['index'] in tags['Temporal_Relation'] for x in tb)==432)
jobs = [json.loads(x.read_text()) for x in root.glob('*-job.json')]
check(len(jobs)==4)
for job in jobs:
    check(job['active']==0 and job['exit_code']==0 and not job['killed'])
    check(job['peak_commit']<=16*1024**3)
check(report['model_calls']==report['optimizer_steps']==0)
check(report['scientific_gate']=='INCOMPLETE')
result = dict(status='PASS', checks=checks, rows=len(rows), candidate_pairs=len(members),
              consistent=consistent, unresolved=unresolved, metadata_bytes=report['network']['metadata_bytes'],
              jobs=jobs, limitation='Metadata consistency only; no physical provenance, media, model or scientific effect certification.')
with open(root/'independent-review.json','x',encoding='utf-8') as stream:
    json.dump(result,stream,indent=2)
print(json.dumps(result))

```
