"""061 explicit cached-data audit; import performs no task I/O or model work.

Only CPU feature arithmetic and sealed response analysis. No tested head,
processor, tokenizer, checkpoint, model forward or optimizer is imported.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import itertools
import json
import math
import os
from pathlib import Path
import random
import re
import time

SPLITS = ('train_pool68', 'validation11', 'development54', 'source_holdout50')
NS = (68, 11, 54, 50)
METHODS = ('A25', 'P1_25', 'A68', 'P1_68')
TYPES = ('CONSTANT', 'VIDEO_ONLY', 'QUESTION_ONLY', 'CHECKERBOARD', 'MIXED')
CONDITION_FIELDS = ('method','seed','split','n_instances','n_cells','complete_cells','valid_cells','unknown_cells','status','correct_cells','video_pair_correct','question_pair_correct','four_way_correct') + TYPES + ('checkerboard_correct','checkerboard_inverted','K0','K1','K2','K3','K4','question_invariant','video_invariant','question_invariant_rate','video_invariant_rate','qflip_edges','vflip_edges','qflip_edge_rate','vflip_edge_rate')
SOURCE_FIELDS = ('method','seed','family','n') + TYPES


def save(path, data):
    with open(path, 'x', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=2); f.flush(); os.fsync(f.fileno())


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def lf_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def category(p):
    a,b,c,d = p
    if a == b == c == d: return 'CONSTANT'
    if a == b and c == d and a != c: return 'VIDEO_ONLY'
    if a == c and b == d and a != b: return 'QUESTION_ONLY'
    if a == d and b == c and a != b: return 'CHECKERBOARD'
    return 'MIXED'


def fixture(root):
    # Independent exhaustive truth table; no real QA or tensors.
    expected = ('CONSTANT','MIXED','MIXED','VIDEO_ONLY','MIXED','QUESTION_ONLY','CHECKERBOARD','MIXED','MIXED','CHECKERBOARD','QUESTION_ONLY','MIXED','VIDEO_ONLY','MIXED','MIXED','CONSTANT')
    counts=Counter(); checks=0
    for number,p in enumerate(itertools.product((0,1),repeat=4)):
        kind=category(p);assert kind==expected[number];checks+=1;counts[kind]+=1
        qedges=int(p[0]!=p[1])+int(p[2]!=p[3]);vedges=int(p[0]!=p[2])+int(p[1]!=p[3])
        assert qedges==2*int(kind in ('QUESTION_ONLY','CHECKERBOARD'))+int(kind=='MIXED');checks+=1
        assert vedges==2*int(kind in ('VIDEO_ONLY','CHECKERBOARD'))+int(kind=='MIXED');checks+=1
        for gold in ((1,0,0,1),(0,1,1,0)):
            k=sum(a==b for a,b in zip(p,gold))
            assert (k in (0,4))==(kind=='CHECKERBOARD');checks+=1
            assert (k==2)==(kind in ('CONSTANT','VIDEO_ONLY','QUESTION_ONLY'));checks+=1
            assert (k in (1,3))==(kind=='MIXED');checks+=1
    assert counts==dict(CONSTANT=2,VIDEO_ONLY=2,QUESTION_ONLY=2,CHECKERBOARD=2,MIXED=8);checks+=1
    save(Path(root)/'fixture.json',dict(status='PASS',checks=checks,patterns=16,classes=dict(counts),real_data_read=False,forward=0,updates=0))
    print('FIXTURE_PASS',checks,flush=True)


class AccessBook:
    """One byte read per resolved path; hash before deserialize, bounded I/O.

    tensor files are loaded from those exact hashed bytes, not reopened.
    Equal serialized identities and repeated paths share a load/cache.
    """
    def __init__(self):
        self.expected={}; self.raw_cache={}; self.records={}; self.meta_bytes=0; self.tensor_bytes=0; self.values={}; self.by_sha={}

    def raw(self,path,tensor=False):
        p=Path(path).resolve();key=str(p)
        if key in self.raw_cache:return self.raw_cache[key]
        stat=p.stat();size=stat.st_size
        if tensor:
            if size>2*1024**2 or self.tensor_bytes+size>32*1024**2:raise ValueError('TENSOR_READ_CAP')
            self.tensor_bytes+=size
        else:
            if self.meta_bytes+size>16*1024**2:raise ValueError('METADATA_READ_CAP')
            self.meta_bytes+=size
        body=p.read_bytes();sha=hashlib.sha256(body).hexdigest()
        if size!=len(body) or (key in self.expected and sha!=self.expected[key]):raise ValueError('READ_SEAL_IDENTITY')
        self.raw_cache[key]=body;self.records[key]=dict(path=key,sha256=sha,bytes=size,mtime_ns=stat.st_mtime_ns,kind='tensor' if tensor else 'metadata',sealed=key in self.expected)
        return body

    def json(self,path):return json.loads(self.raw(path).decode('utf-8-sig'))

    def add_seal(self,records):
        for r in records:
            key=str(Path(r['path']).resolve())
            if key in self.expected and self.expected[key]!=r['sha256']:raise ValueError('CONFLICTING_SEAL')
            self.expected[key]=r['sha256']
            if key in self.records and self.records[key]['sha256']!=r['sha256']:raise ValueError('ALREADY_READ_SEAL_MISMATCH')

    def tensor(self,path,shape,torch):
        key=str(Path(path).resolve())
        if key not in self.values:
            # A closed equal serialized identity need not be read/load again.
            identity=self.expected.get(key)
            if identity in self.by_sha:
                self.values[key]=self.by_sha[identity]
            else:
                body=self.raw(path,tensor=True)
                value=torch.load(io.BytesIO(body),map_location='cpu',weights_only=True)
                if value.device.type!='cpu' or value.dtype!=torch.float32 or tuple(value.shape)!=shape or not bool(torch.isfinite(value).all()):raise ValueError('FEATURE_CONTRACT')
                self.values[key]=value;self.by_sha[self.records[key]['sha256']]=value
        value=self.values[key]
        if tuple(value.shape)!=shape:raise ValueError('FEATURE_ALIAS_SHAPE')
        return value

    def unchanged(self):
        for r in self.records.values():
            stat=Path(r['path']).stat()
            if stat.st_size!=r['bytes'] or stat.st_mtime_ns!=r['mtime_ns']:raise ValueError('OLD_FILE_CHANGED_DURING_READ')


def quantiles(values):
    v=sorted(values);result={}
    for p in (0,.25,.5,.75,1):
        x=(len(v)-1)*p;i=int(x);result[str(p)]=v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
    return result


def interval_rows(profile):
    configurations=[(m,s) for m in METHODS for s in (19,73)]+[('B0','NA')]
    grouped={(m,s):{r['family']:r for r in profile if (r['method'],r['seed'])==(m,s)} for m,s in configurations}
    keys=[f'F{i:02}' for i in range(1,26)];stats=[]
    def vectors(m,s,metric):
        rows=grouped[(m,s)]
        return [rows[k]['CONSTANT']+rows[k]['VIDEO_ONLY' if metric=='question_invariant' else 'QUESTION_ONLY'] for k in keys]
    for m,s in configurations:
        for metric in ('question_invariant','video_invariant'):
            stats.append(dict(kind='marginal',metric=metric,method=m,seed=s,comparator='NA',unit='proportion',values=vectors(m,s,metric)))
    for seed in (19,73):
        for left,right in (('A68','A25'),('P1_68','P1_25')):
            for metric in ('question_invariant','video_invariant'):
                a=vectors(left,seed,metric);b=vectors(right,seed,metric)
                stats.append(dict(kind='paired_difference',metric=metric,method=left,seed=seed,comparator=right,unit='proportion_difference',values=[x-y for x,y in zip(a,b)]))
    # One initialized stream, same10000 draws for all26 statistics.
    rng=random.Random(55061);draws=[rng.choices(range(25),k=25) for _ in range(10000)];answer=[]
    for stat in stats:
        v=stat.pop('values');samples=sorted(sum(v[k] for k in draw)/sum(2 for _ in draw) for draw in draws)
        def q(p):
            position=9999*p;k=int(position);return samples[k]+(position-k)*(samples[min(k+1,9999)]-samples[k])
        answer.append(dict(**stat,n_instances=50,n_families=25,estimate=sum(v)/50,ci_low=q(.025),ci_high=q(.975)))
    return answer


def geometry_and_coverage(observations,index,reader,torch):
    video={name:reader.tensor(r['path'],(6,2560),torch) for name,r in index['video'].items()}
    text={q:reader.tensor(r['path'],(2560,),torch) for q,r in index['text'].items()}
    if len(video)!=366 or len(text)!=220:raise ValueError('FEATURE_SLOT_COUNTS')
    def tensor_identity(t):
        v=t.clone();v[v==0]=0 # canonical signed zero for exact value identity
        return hashlib.sha256(v.numpy().tobytes()).hexdigest()
    video_identity={n:tensor_identity(v) for n,v in video.items()}
    parsed={};questions={};normalize=lambda x:' '.join(x.replace('_',' ').split()).casefold()
    for split,rows in observations.items():
        parsed[split]=[];questions[split]=[]
        for r in rows:
            q0,q1=r['questions'];m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q0)
            if m is None or q1!=f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.':raise ValueError('QUESTION_EVENT_PARSE')
            parsed[split].append((normalize(m[1]),normalize(m[2])));questions[split].extend((q0,q1))
    events={x for pair in parsed[SPLITS[0]] for x in pair};pairs={tuple(sorted(pair)) for pair in parsed[SPLITS[0]]}
    permutations=torch.tensor(list(itertools.permutations(range(6))),dtype=torch.long);rowsidx=torch.arange(6)[None,:];geometry=[];coverage=[]
    for split in SPLITS:
        qdist=[];vdist=[];pdist=[];variation=[];qexact=vexact=small=union=0;unique_v=set();norm_collision=0;covered=Counter()
        for r,(a,b) in zip(observations[split],parsed[split]):
            q0,q1=(text[q].to(torch.float64) for q in r['questions']);v0,v1=(video[n].to(torch.float64) for n in r['videos'])
            qeq=bool(torch.equal(q0,q1));veq=bool(torch.equal(v0,v1));qexact+=qeq;vexact+=veq;union+=qeq or veq
            qr=float(torch.linalg.vector_norm(q0-q1)/(torch.linalg.vector_norm(q0)+torch.linalg.vector_norm(q1)+1e-12));qdist.append(qr);small+=qr<=1e-4
            denominator=torch.linalg.vector_norm(v0)+torch.linalg.vector_norm(v1)+1e-12
            vdist.append(float(torch.linalg.vector_norm(v0-v1)/denominator))
            cost=(v0[:,None,:]-v1[None,:,:]).square().sum(-1)
            pdist.append(float(torch.sqrt(cost[rowsidx,permutations].sum(-1).min())/denominator))
            for name,v in zip(r['videos'],(v0,v1)):
                variation.append(float((v-v.mean(0,keepdim=True)).square().sum()/(v.square().sum()+1e-12)));unique_v.add(video_identity[name])
            norm_collision+=a==b
            count=int(a in events)+int(b in events)
            covered['PAIR_SEEN' if tuple(sorted((a,b))) in pairs else 'BOTH_EVENTS_SEEN_PAIR_NEW' if count==2 else 'ONE_EVENT_SEEN' if count==1 else 'NO_EVENT_SEEN']+=1
        n=len(observations[split])
        geometry.append(dict(split=split,n_instances=n,question_swap_relative_distance=quantiles(qdist),q_exact_equal_instances=qexact,q_distance_le_1e_minus4_instances=small,ordered_video_relative_distance=quantiles(vdist),min_720_row_permutation_relative_distance=quantiles(pdist),ordered_v_exact_equal_instances=vexact,exact_collision_instance_union=union,deterministic_head_four_way_upper_bound=n-union,temporal_variation_ratio=quantiles(variation),temporal_video_slots=2*n,unique_video_tensors=len(unique_v)))
        coverage.append(dict(split=split,n_instances=n,**{k:covered[k] for k in ('PAIR_SEEN','BOTH_EVENTS_SEEN_PAIR_NEW','ONE_EVENT_SEEN','NO_EVENT_SEEN')},raw_question_slots=2*n,unique_question_strings=len(set(questions[split])),normalized_same_event_instances=norm_collision,reference='TRAIN68_ONLY;normalized strings;unordered length2 tuple with positions retained'))
    return geometry,coverage


def analyze(root,prior):
    os.environ['CUDA_VISIBLE_DEVICES']=''
    import torch
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized():raise RuntimeError('CUDA_INITIALIZED')
    root=Path(root);prior=Path(prior);plan=read(root/'analysis-plan.json')
    if lf_sha(__file__)!=plan['code_lf_sha256']:raise ValueError('CODE_NOT_FROZEN')
    claim=root/'diagnostic-started.json'
    save(claim,dict(status='STARTED',at_unix=time.time(),code_lf_sha256=plan['code_lf_sha256']))
    reader=AccessBook();start=time.monotonic()
    try:
        outputsseal=reader.json(prior/'outputs-identity-seal.json');reader.add_seal(outputsseal['files'])
        pre=reader.json(prior/'pre-consumption-seal.json');reader.add_seal(pre['files'])
        if pre['code']!=plan['prior060_code_lf_sha256']:raise ValueError('060_COMMITTED_CODE_IDENTITY')
        closed=reader.json(prior/'parent-closed.json')
        if closed['commit']!='876ededdcaa4038363fc92f9761462c42435e41c' or closed['push']!='SUCCEEDED':raise ValueError('060_CLOSURE_IDENTITY')
        for name in ('training','prediction','gpu'):
            j=reader.json(prior/(name+'-job.json'))
            if j['active']!=0 or j['exit_code']!=0 or j['killed']:raise ValueError('060_JOB_NOT_CLOSED')
        bindings=reader.json(prior/'data-bindings.json');pools=bindings['pools']
        if tuple(len(pools[s]) for s in SPLITS)!=NS or [len({r['group_key'] for r in pools[s]}) for s in SPLITS]!=[25,4,20,25]:raise ValueError('MEMBERS_GROUPS')
        groups=[{r['group_key'] for r in pools[s]} for s in SPLITS]
        if any(a&b for i,a in enumerate(groups) for b in groups[i+1:]):raise ValueError('SOURCE_OVERLAP')
        if len({r['recording'] for s in SPLITS[:3] for r in pools[s]})!=133 or len({r['recording'] for r in pools[SPLITS[3]]})!=50:raise ValueError('RECORD_MEMBERSHIP')
        observations={s:reader.json(prior/(s+'-observations.json')) for s in SPLITS};labels={s:reader.json(prior/(s+'-labels.json')) for s in SPLITS}
        for s,n in zip(SPLITS,NS):
            if len(observations[s])!=n or len(labels[s])!=n:raise ValueError('OBS_LABEL_COUNTS')
            for i,(o,l,r) in enumerate(zip(observations[s],labels[s],pools[s])):
                if o!=dict(index=i,videos=r['videos'],questions=r['questions']) or l!=dict(index=i,labels=r['labels']):raise ValueError('OBS_BINDING')
                a,b=l['labels'][0];c,d=l['labels'][1]
                if any(x not in (0,1) for x in (a,b,c,d)) or a!=d or b!=c or a+b!=1:raise ValueError('FOUR_LABEL_RELATION')
        outputs=reader.json(prior/'all-outputs-sealed.json');lookup={};origins=Counter()
        for r in outputs:
            key=(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question'])
            if key in lookup or r['status']!='CLOSED' or type(r['prediction']) is not int or r['prediction'] not in (0,1):raise ValueError('PREDICTION_CONTRACT')
            lookup[key]=r['prediction'];origins[r['origin']]+=1
        if len(lookup)!=6056 or origins!=dict(CACHED=816,NEW_HEAD=5040,NEW_B0=200):raise ValueError('6056_CONSERVATION')
        baseline=Path(__file__).parent.parent/'docs/codex-artifacts/VLM-POOL-TRANSFER-060/condition-summary.csv'
        original=list(csv.DictReader(io.StringIO(reader.raw(baseline).decode('utf-8'))));conditions=[];types={};profile=[]
        family_keys=sorted(groups[3])
        if len(family_keys)!=25 or any(sum(r['group_key']==k for r in pools[SPLITS[3]])!=2 for k in family_keys):raise ValueError('FAMILY25_TWO')
        for split,n in zip(SPLITS,NS):
            configurations=[(m,s) for m in METHODS for s in (19,73)]+([('B0','NA')] if split==SPLITS[3] else [])
            for method,seed in configurations:
                row={k:0 for k in CONDITION_FIELDS};row.update(method=method,seed=seed,split=split,n_instances=n,n_cells=4*n,complete_cells=4*n,valid_cells=4*n,status='COMPLETE');instance_types=[]
                for i in range(n):
                    p=[lookup[(method,seed,split,i,v,q)] for v in (0,1) for q in (0,1)];gold=[labels[split][i]['labels'][v][q] for v in (0,1) for q in (0,1)]
                    kind=category(p);row[kind]+=1;instance_types.append(kind);c=[int(a==b) for a,b in zip(p,gold)];k=sum(c);row['K'+str(k)]+=1;row['correct_cells']+=k
                    row['video_pair_correct']+=c[0]*c[2]+c[1]*c[3];row['question_pair_correct']+=c[0]*c[1]+c[2]*c[3];row['four_way_correct']+=int(k==4)
                    row['checkerboard_correct']+=int(kind=='CHECKERBOARD' and k==4);row['checkerboard_inverted']+=int(kind=='CHECKERBOARD' and k==0)
                row['question_invariant']=row['CONSTANT']+row['VIDEO_ONLY'];row['video_invariant']=row['CONSTANT']+row['QUESTION_ONLY']
                row['qflip_edges']=2*(row['QUESTION_ONLY']+row['CHECKERBOARD'])+row['MIXED'];row['vflip_edges']=2*(row['VIDEO_ONLY']+row['CHECKERBOARD'])+row['MIXED']
                for k,den in [('question_invariant',n),('video_invariant',n),('qflip_edge',2*n),('vflip_edge',2*n)]:row[k+'_rate']=row[k if den==n else k+'s']/den
                if row['K0']!=row['checkerboard_inverted'] or row['K4']!=row['checkerboard_correct'] or row['K2']!=sum(row[k] for k in TYPES[:3]) or row['K1']+row['K3']!=row['MIXED'] or sum(k*row['K'+str(k)] for k in range(5))!=row['correct_cells']:raise ValueError('RESPONSE_IDENTITY')
                old=next(x for x in original if (x['method'],x['seed'],x['split'])==(method,str(seed),split))
                for k in ('n_instances','n_cells','complete_cells','valid_cells','unknown_cells','correct_cells','video_pair_correct','question_pair_correct','four_way_correct'):
                    if row[k]!=int(old[k]):raise ValueError('ORIGINAL_060_METRIC_CHANGED')
                conditions.append(row);types[(method,seed,split)]=instance_types
                if split==SPLITS[3]:
                    for j,key in enumerate(family_keys,1):
                        ids=[i for i,r in enumerate(pools[split]) if r['group_key']==key];counts=Counter(instance_types[i] for i in ids)
                        profile.append(dict(method=method,seed=seed,family=f'F{j:02}',n=2,**{k:counts[k] for k in TYPES}))
        if len(conditions)!=33 or sum(r['n_instances'] for r in conditions)!=1514 or len(profile)!=225:raise ValueError('AUDIT_DENOMINATOR')
        index=reader.json(prior/'feature-index.json');geometry,coverage=geometry_and_coverage(observations,index,reader,torch)
        intervals=interval_rows(profile);reader.unchanged()
        if len(intervals)!=26 or torch.cuda.is_initialized():raise ValueError('INTERVAL_OR_CUDA')
        for name,rows,fields in [('condition-summary.csv',conditions,CONDITION_FIELDS),('source-profile.csv',profile,SOURCE_FIELDS)]:
            with open(root/name,'x',newline='',encoding='utf-8') as f:
                writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
        save(root/'audit-summary.json',dict(status='COMPLETE_CACHED_RESPONSE_AUDIT',causal_status='CAUSAL_BOTTLENECK_UNRESOLVED',novelty='NO_NEW_METHOD_CLAIM',conditions=conditions,source_profile=profile,intervals=intervals,geometry=geometry,coverage=coverage,formal_cells=6056,four_way_instances=1514,metadata_bytes=reader.meta_bytes,tensor_bytes=reader.tensor_bytes,feature_paths_loaded=len(reader.values),unique_serialized_tensor_loads=len(reader.by_sha),analysis_outer_s=time.monotonic()-start,cuda_initialized=False,code_lf_sha256=plan['code_lf_sha256']))
        save(root/'access-manifest.json',dict(files=list(reader.records.values()),metadata_bytes=reader.meta_bytes,tensor_bytes=reader.tensor_bytes,hashes_before_deserialization=True,post_read_stats_unchanged=True))
        save(root/'diagnostic-closed.json',dict(status='CLOSED',at_unix=time.time(),formal_cells=6056,rows=33))
        print('AUDIT_CLOSED:6056 cells;1514 fourways;33/225/26;366V/220q',flush=True)
    except Exception as e:
        save(root/'diagnostic-failed.json',dict(status='BLOCKED',reason=str(e),metadata_bytes=reader.meta_bytes,tensor_bytes=reader.tensor_bytes))
        rows=[]
        for split,n in zip(SPLITS,NS):
            for method,seed in [(m,s) for m in METHODS for s in (19,73)]+([('B0','NA')] if split==SPLITS[3] else []):
                row={k:'NA' for k in CONDITION_FIELDS};row.update(method=method,seed=seed,split=split,n_instances=n,n_cells=4*n,complete_cells='NA',valid_cells='NA',unknown_cells=4*n,status='UNKNOWN');rows.append(row)
        with open(root/'blocked-condition-summary.csv','x',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=CONDITION_FIELDS);writer.writeheader();writer.writerows(rows)
        raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=('fixture','analyze'));p.add_argument('--root',required=True);p.add_argument('--prior')
    a=p.parse_args()
    if a.phase=='fixture':fixture(a.root)
    else:analyze(a.root,a.prior)
