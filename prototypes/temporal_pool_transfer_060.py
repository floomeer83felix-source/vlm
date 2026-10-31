"""060 explicit preparation, CPU training, prediction and scoring roles.

Import defines functions only. No network, model load, task I/O or updates.
Protected labels and cached predictions are never read by train().
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import time

SPLITS = ('train_pool68', 'validation11', 'development54', 'source_holdout50')
NS = (68, 11, 54, 50)
METHODS = ('A25', 'P1_25', 'A68', 'P1_68')
REVISION = 'fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    with open(path, 'x', encoding='utf-8') as f:
        json.dump(value, f, sort_keys=True, indent=2)
        f.flush(); os.fsync(f.fileno())


def event(path, **value):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(value, sort_keys=True) + '\n')
        f.flush(); os.fsync(f.fileno())


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def code_sha(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def cpu():
    import torch
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized() or os.environ.get('CUDA_VISIBLE_DEVICES') != '':
        raise RuntimeError('CPU_ROLE_ONLY')
    return torch


def prepare(root, prior056, prior057, prior059):
    torch = cpu(); root = Path(root)
    p56, p57, p59 = map(Path, (prior056, prior057, prior059))
    checks = 0; assets = {}
    def check(value, reason):
        nonlocal checks
        if not value: raise ValueError(reason)
        checks += 1
    def asset(path, expected=None):
        path = Path(path); got = digest(path)
        check(expected is None or got == expected, 'PRIOR_ASSET_IDENTITY')
        assets[str(path.resolve())] = dict(path=str(path.resolve()), sha256=got, bytes=path.stat().st_size)
        return got
    for p in (p56, p57, p59):
        check((p/'parent-closed.json').exists(), 'PRIOR_PARENT_NOT_CLOSED')
        asset(p/'parent-closed.json')
    for p in (p57, p59):
        check(read(p/'training-job.json')['active'] == 0, 'PRIOR_JOB_ACTIVE')
    s57 = read(p57/'evaluation-input-seal.json')
    s59 = read(p59/'outputs-identity-seal.json')
    for seal in (s57, s59):
        for a in seal['files']: asset(a['path'], a['sha256'])
    for a in read(p59/'input-seal.json')['assets']: asset(a['path'], a['sha256'])
    check(read(p57/'all-outputs-seal.json')['outputs_sha256'] == digest(p57/'head-outputs-sealed.json'), 'OLD_A_SEAL')
    source = read(p56/'source-table.json'); asset(p56/'source-table.json')
    check(digest(p56/'source-table.json') == digest(p57/'prior_source-table.json'), 'JOIN_COPY_IDENTITY')
    rawpath = p56/'prior_dybench_annotations.body'; asset(rawpath)
    check(rawpath.stat().st_size == 388049, 'FIXED_JSON_SIZE')
    check(read(p56/'prior_dybench_revision.json')['revision'] == REVISION, 'FIXED_REVISION')
    rows = read(rawpath); check(len(rows) == 814, 'FIXED_ROWS')
    records = {x['recording']: x for x in source['records']}
    check(len(records) == len(source['records']) == 133, 'ORIGINAL_JOIN_133')
    pools = {s: [] for s in SPLITS}; excluded = Counter(); join_count = 0
    for category in ('Breakfast', '50Salads'):
        pairs = defaultdict(list)
        for row in rows:
            if row['source_subcategory'] == category:
                check(row['source_category'] == 'event_sequence', 'SOURCE_FIELD')
                pairs[re.sub(r'_reversed(?=\.mp4$)', '', row['video'])].append(row)
        check(len(pairs) == (147 if category == 'Breakfast' else 50), 'PAIR_COUNT')
        for filename, pair in sorted(pairs.items()):
            check(len(pair) == 2 and len({x['video'] for x in pair}) == 2 and pair[0]['question'] == pair[1]['question'], 'PAIR_STRUCTURE')
            parsed = re.fullmatch(r'.*\nAction 1\. (.+)\nAction 2\. (.+)\nPlease output their order\.', pair[0]['question'], re.S)
            check(parsed is not None, 'EVENT_PARSE')
            a, b = parsed.groups(); normalize = lambda x: ' '.join(x.replace('_', ' ').split())
            if normalize(a) == normalize(b):
                check(category == 'Breakfast', 'HOLDOUT_IDENTICAL_EVENTS'); excluded['SAME_EVENT'] += 1; continue
            original = [x for x in pair if x['video'] == filename]
            reverse = [x for x in pair if x['video'] == filename[:-4] + '_reversed.mp4']
            options = ['First action 1, then action 2', 'First action 2, then action 1']
            check(len(original) == len(reverse) == 1 and all(x['candidates'] == options for x in pair) and {x['answer'] for x in pair} == set(options), 'PUBLISHER_LABEL_BINDING')
            if category == 'Breakfast':
                match = re.fullmatch(r'(P\d+)_(cam\d+|webcam\d+|stereo\d+)_(P\d+)_(.+)\.mp4', filename)
                if not match or match[1] != match[3] or not re.fullmatch(r'P(?:0[3-9]|[1-4][0-9]|5[0-4])', match[1]):
                    excluded['RECORD_NUMBER'] += 1; continue
                key = filename[:-4]; check(key in records, 'JOIN_MEMBER_MISSING')
                record = records[key]
                expected = dict(recording=key, participant=match[1], camera=match[2], group_key='Breakfast/participant=' + match[1])
                check(all(record[k] == v for k, v in expected.items()) and record['motion_file'].startswith(match[1] + '/'), 'JOIN_FIELDS')
                bucket = int(hashlib.sha256(('VLM055/' + record['group_key']).encode()).hexdigest()[:8], 16) % 10
                split = SPLITS[0 if bucket < 6 else 1 if bucket == 6 else 2]
                identity = dict(record); join_count += 1
            else:
                match = re.fullmatch(r'rgb-(\d{2})-([12])\.mp4', filename)
                check(match is not None, 'HOLDOUT_FILE_FAMILY')
                split = SPLITS[3]; identity = dict(recording=filename[:-4], group_key='50Salads/family=' + match[1], trial=match[2])
            yes = int(original[0]['answer'] == options[0])
            questions = [f'Does the event "{a}" happen before the event "{b}"? Answer Yes or No.', f'Does the event "{b}" happen before the event "{a}"? Answer Yes or No.']
            pools[split].append(dict(**identity, source=category, videos=[original[0]['video'], reverse[0]['video']], questions=questions, events=[a, b], labels=[[yes, 1-yes], [1-yes, yes]], evidence='PUBLISHER_COMPOSITE_QA'))
    check(join_count == 133 and excluded == dict(SAME_EVENT=9, RECORD_NUMBER=5), '133_JOIN_EXCLUSIONS')
    check(tuple(len(pools[s]) for s in SPLITS) == NS, 'FIXED_68_11_54_50')
    groups = {s: {r['group_key'] for r in pools[s]} for s in SPLITS}
    check([len(groups[s]) for s in SPLITS] == [25, 4, 20, 25], 'GROUP_COUNTS')
    check(all(not groups[a] & groups[b] for i, a in enumerate(SPLITS) for b in SPLITS[i+1:]), 'CROSS_SPLIT_GROUP')
    check(Counter(r['group_key'] for r in pools[SPLITS[3]]) == {k: 2 for k in groups[SPLITS[3]]}, 'FAMILY_TRIAL_COUNTS')
    oldplan = read(p57/'pilot-input-seal.json')['selected']; mapping = []
    for oldsplit, newsplit, n in zip(('train', 'validation', 'development_test'), SPLITS, (25, 2, 24)):
        check(len(oldplan[oldsplit]) == n, 'OLD_SPLIT_SIZE')
        for i, row in enumerate(oldplan[oldsplit]):
            found = [(j, r) for j, r in enumerate(pools[newsplit]) if r['recording'] == row['recording']]
            check(len(found) == 1, 'OLD_MEMBER_NESTING'); j, now = found[0]
            check(all(now[k] == row[k] for k in ('videos', 'questions', 'labels', 'recording', 'participant', 'camera', 'group_key', 'annotation', 'motion_file')), 'OLD_EXACT_BINDING')
            mapping.append(dict(old_split=oldsplit, old_index=i, split=newsplit, index=j))
    save(root/'data-bindings.json', dict(pools=pools, old_mapping=mapping, exclusions=dict(excluded), evidence='PUBLISHER_COMPOSITE_QA', holdout_groups='FILE_FAMILY_CLUSTER'))
    for split in SPLITS:
        save(root/(split + '-observations.json'), [dict(index=i, videos=r['videos'], questions=r['questions']) for i, r in enumerate(pools[split])])
        save(root/(split + '-labels.json'), [dict(index=i, labels=r['labels']) for i, r in enumerate(pools[split])])
    # Prepare role projects old predictions; training never reads this file.
    old_a = [x for x in read(p57/'head-outputs-sealed.json') if x['arm'] == 'A']
    old_p = [x for x in read(p59/'new-outputs-sealed.json') if x['arm'] == 'P1']
    cached = []
    for method, records_pred in [('A25', old_a), ('P1_25', old_p)]:
        check(len(records_pred) == 408 and all(x['status'] == 'CLOSED' for x in records_pred), 'OLD_PRED_COMPLETE')
        for x in records_pred:
            binding = next(m for m in mapping if (m['old_split'], m['old_index']) == (x['split'], x['index']))
            cached.append(dict(method=method, seed=x['seed'], split=binding['split'], index=binding['index'], video=x['video'], question=x['question'], prediction=x['prediction'], status=x['status'], origin='CACHED'))
    check(len({(x['method'],x['seed'],x['split'],x['index'],x['video'],x['question']) for x in cached}) == 816, 'CACHE_UNIQUE')
    save(root/'cached-outputs.json', cached)
    h56 = module('question_temporal_056'); h59 = module('question_directed_pair_059'); plans = {}; old_models = {}
    for seed in (19, 73):
        original = torch.load(p57/f'pretrain-seed{seed}.pt', map_location='cpu', weights_only=True)
        used57 = torch.load(p57/'training'/f'plan-{seed}.pt', map_location='cpu', weights_only=True)
        used59 = torch.load(p59/'training'/f'059-P1-seed{seed}'/'initial-used.pt', map_location='cpu', weights_only=True)
        mapped = torch.load(p59/f'mapped-seed{seed}.pt', map_location='cpu', weights_only=True)['state']
        expected = h59.mapped_initial(original['state'])
        check(all(torch.equal(original['state'][k], used57['state'][k]) for k in original['state']), 'A_INITIAL_EXACT')
        check(set(expected) == set(mapped) == set(used59) and all(torch.equal(expected[k], mapped[k]) and torch.equal(mapped[k], used59[k]) for k in mapped), 'P1_INITIAL_EXACT_MAPPING')
        sequence = torch.randint(68, (250, 8), generator=torch.Generator().manual_seed(seed))
        check(len(torch.unique(sequence)) == 68, 'TRAIN_POOL_COVERAGE')
        path = root/f'plan-{seed}.pt'
        with open(path, 'xb') as f: torch.save(dict(A=original['state'], P1=mapped, sequence=sequence), f)
        plans[str(seed)] = dict(path=path.name, sha256=digest(path))
        for method, state, model in [('A68', original['state'], h56.TemporalHead(2560,2560)), ('P1_68', mapped, h59.PairHead('P1'))]:
            model.load_state_dict(state)
            check(sum(p.numel() for p in model.parameters()) == 356673 and all(torch.equal(model.state_dict()[k], state[k]) for k in state), 'HEAD_STATIC_STATE')
        old_models[str(seed)] = dict(A25=str(p57/'training'/f'A-{seed}'/'final.pt'), P1_25=str(p59/'training'/f'059-P1-seed{seed}'/'final.pt'))
    old_index = read(p57/'feature-index.json')
    check(len(old_index['video']) == 102 and len(old_index['text']) == 54, 'OLD_FEATURE_COUNTS')
    for kind, shape in [('video', (6,2560)), ('text', (2560,))]:
        for row in old_index[kind].values():
            value = torch.load(p57/'features'/row['path'], map_location='cpu', weights_only=True)
            check(value.shape == shape and value.dtype == torch.float32 and bool(torch.isfinite(value).all()), 'OLD_FEATURE_FINITE')
    for path in [p57/'cache-manifest.json', p57/'media-manifest.json', p57/'runtime-input-seal.json', p57/'media-plan.json', p57/'model-calls']:
        if path.is_file(): asset(path)
    for p in (p57/'model-calls').glob('*.started'):
        check(p.with_suffix('.closed').exists(), 'HISTORICAL_STARTED_UNCLOSED')
    for name in ('question_temporal_056.py','question_temporal_data_056.py','question_temporal_train_057.py','question_temporal_runtime_057.py','question_directed_pair_059.py'):
        asset(Path(__file__).with_name(name))
    save(root/'training-config.json', dict(plans=plans, old_models=old_models, parameters=356673, steps=250, loss='BCE', seeds=[19,73]))
    save(root/'prior-assets.json', dict(files=list(assets.values()), checks=checks, prior056=str(p56), prior057=str(p57), prior059=str(p59)))
    print('PREPARE_PASS', checks, '133+50;68/11/54;old51 exact;816 cache', flush=True)


def freeze(root):
    root = Path(root)
    if (root/'model-calls').exists() or (root/'training').exists(): raise RuntimeError('CONSUMED_BEFORE_FREEZE')
    files = [p for p in root.iterdir() if p.is_file() and p.suffix in ('.json','.pt','.py') and p.name != 'parent.json']
    files += list((root/'prepared').glob('*.pt')) + list((root/'frames').glob('*.npy'))
    codes = [Path(__file__), Path(__file__).with_name('temporal_pool_runtime_060.py')]
    save(root/'pre-consumption-seal.json', dict(status='SEALED_BEFORE_FIRST_CONSUMPTION', files=[dict(path=str(p),sha256=digest(p)) for p in files], code={p.name:code_sha(p) for p in codes}, gate=dict(min_a68=10,min_net_a25=4,mean_a68_b0_gt=0), planned=dict(formal_cells=6056,cached_cells=816,new_head_cells=5040,b0_cells=200,research_steps=1000,software_forward=0), at_unix=time.time()))


def check_frozen(root):
    seal = read(root/'pre-consumption-seal.json')
    for name, expected in seal['code'].items():
        if code_sha(Path(__file__).with_name(name)) != expected: raise ValueError('CODE_CHANGED_AFTER_SEAL')
    return seal


def train(root):
    torch = cpu(); root = Path(root); check_frozen(root)
    if read(root/'gpu-job.json')['active'] != 0 or read(root/'gpu-job.json')['exit_code'] != 0 or not (root/'gpu-success.json').exists(): raise RuntimeError('GPU_NOT_CLOSED')
    h56 = module('question_temporal_056'); h59 = module('question_directed_pair_059')
    index = read(root/'feature-index.json'); observations = read(root/(SPLITS[0]+'-observations.json'))
    def load(kind,key): return torch.load(index[kind][key]['path'],map_location='cpu',weights_only=True)
    V=torch.stack([torch.stack([load('video',n) for n in r['videos']]) for r in observations])
    Q=torch.stack([torch.stack([load('text',q) for q in r['questions']]) for r in observations])
    y=torch.tensor([r['labels'] for r in read(root/(SPLITS[0]+'-labels.json'))],dtype=torch.float32)
    if V.shape!=(68,2,6,2560) or Q.shape!=(68,2,2560) or y.shape!=(68,2,2): raise ValueError('TRAIN68_SHAPES')
    config=read(root/'training-config.json'); directory=root/'training';directory.mkdir(); records=[]; deadline=time.monotonic()+1000
    for seed in (19,73):
        plan=torch.load(root/config['plans'][str(seed)]['path'],map_location='cpu',weights_only=True)
        if digest(root/config['plans'][str(seed)]['path'])!=config['plans'][str(seed)]['sha256']:raise ValueError('PLAN_IDENTITY')
        for method in ('A68','P1_68'):
            output=directory/f'{method}-{seed}';output.mkdir();journal=output/'steps.jsonl'
            event(journal,event='STARTED',method=method,seed=seed);start=time.monotonic()
            try:
                initial=plan['A' if method=='A68' else 'P1'];model=h56.TemporalHead(2560,2560) if method=='A68' else h59.PairHead('P1')
                model.load_state_dict(initial);model.train();opt=h56.optimizer(model)
                with open(output/'initial-used.pt','xb') as f:torch.save(model.state_dict(),f)
                for step,ids in enumerate(plan['sequence']):
                    if time.monotonic()>deadline:raise TimeoutError('CPU_TRAIN_DEADLINE')
                    event(journal,event='STEP_STARTED',step=step)
                    video,text=h56.pack(V,Q,ids);z=model(video,text).reshape(8,2,2)
                    loss=torch.nn.functional.softplus(-(2*y[ids]-1)*z).mean()
                    if not torch.isfinite(loss):raise ValueError('NONFINITE_LOSS')
                    opt.zero_grad(set_to_none=True);loss.backward()
                    if any(p.grad is None or not torch.isfinite(p.grad).all() for p in model.parameters()):raise ValueError('GRADIENT')
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1);opt.step()
                    event(journal,event='STEP_CLOSED',step=step,loss=float(loss.detach()))
                with open(output/'final.pt','xb') as f:torch.save(model.state_dict(),f);f.flush();os.fsync(f.fileno())
                event(journal,event='CLOSED',optimizer_steps=250)
                records.append(dict(method=method,seed=seed,status='CLOSED',steps=250,parameters=sum(p.numel() for p in model.parameters()),parameter_l1_change=sum(float((model.state_dict()[k]-initial[k]).abs().sum()) for k in initial),outer_s=time.monotonic()-start))
                print('TRAIN_CLOSED',method,seed,250,flush=True);del model,opt
            except Exception as e:
                event(journal,event='FAILED',reason=str(e));save(root/'training-failed.json',dict(method=method,seed=seed,reason=str(e)));raise
    save(root/'training-summary.json',dict(configurations=records,real_updates=1000,software_updates=0,software_forward=0,cuda_initialized=torch.cuda.is_initialized()))


def predict(root):
    torch=cpu();root=Path(root);check_frozen(root)
    if read(root/'training-job.json')['active']!=0 or read(root/'training-job.json')['exit_code']!=0:raise RuntimeError('TRAIN_NOT_CLOSED')
    h56=module('question_temporal_056');h59=module('question_directed_pair_059');config=read(root/'training-config.json')
    index=read(root/'feature-index.json');observations={s:read(root/(s+'-observations.json')) for s in SPLITS}
    features={k:{key:torch.load(r['path'],map_location='cpu',weights_only=True) for key,r in index[k].items()} for k in ('video','text')}
    outputs=read(root/'cached-outputs.json');cached={(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question']) for r in outputs}
    if len(cached)!=816:raise ValueError('CACHE816')
    journal=root/'prediction-calls.jsonl';n=0;deadline=time.monotonic()+900
    for seed in (19,73):
        for method in METHODS:
            model=h56.TemporalHead(2560,2560) if method.startswith('A') else h59.PairHead('P1')
            path=Path(config['old_models'][str(seed)][method]) if method.endswith('25') else root/'training'/f'{method}-{seed}'/'final.pt'
            model.load_state_dict(torch.load(path,map_location='cpu',weights_only=True));model.eval()
            for split,rows in observations.items():
                for row in rows:
                    for vi,name in enumerate(row['videos']):
                        for qi,text in enumerate(row['questions']):
                            key=(method,seed,split,row['index'],vi,qi)
                            if key in cached:continue
                            if time.monotonic()>deadline:raise TimeoutError('PREDICTION_DEADLINE')
                            event(journal,event='STARTED',key=key)
                            prediction=(h56.predict if method.startswith('A') else h59.predict)(model,features['video'][name],features['text'][text]);n+=1
                            result=dict(method=method,seed=seed,split=split,index=row['index'],video=vi,question=qi,prediction=int(prediction),status='CLOSED',origin='NEW_HEAD')
                            outputs.append(result);event(journal,event='CLOSED',key=key,prediction=int(prediction))
            del model
    if n!=5040 or len(outputs)!=5856:raise ValueError('HEAD_CELL_CONSERVATION')
    outputs+=read(root/'b0-sealed.json')
    if len(outputs)!=6056:raise ValueError('TOTAL6056')
    save(root/'all-outputs-sealed.json',outputs)
    paths=[root/'all-outputs-sealed.json',root/'feature-index.json',root/'pre-consumption-seal.json']+list((root/'training').glob('*/*.pt'))
    paths += [Path(p) for r in config['old_models'].values() for p in r.values()]
    paths += [Path(r['path']) for kind in index.values() for r in kind.values()]
    save(root/'outputs-identity-seal.json',dict(status='SEALED_BEFORE_SCORING',files=[dict(path=str(p),sha256=digest(p)) for p in paths],new_head_cells=n,cached_cells=816,b0_cells=200,total=6056,cuda_initialized=torch.cuda.is_initialized()))
    print('OUTPUTS_SEALED',6056,flush=True)


def bootstrap(groups):
    keys=sorted(groups);rng=random.Random(55060);values=[]
    for _ in range(10000):
        selected=rng.choices(keys,k=25)
        values.append(100*sum(groups[k]['net'] for k in selected)/sum(groups[k]['n'] for k in selected))
    values.sort();result=[]
    for p in (.025,.975):
        position=9999*p;i=int(position);result.append(values[i]+(position-i)*(values[min(i+1,9999)]-values[i]))
    return result


def score(root):
    root=Path(root);executed=(root/'outputs-identity-seal.json').exists()
    if executed:
        for name in ('training','prediction'):
            if read(root/(name+'-job.json'))['active']!=0:raise RuntimeError('JOB_ACTIVE_BEFORE_SCORE')
        for r in read(root/'outputs-identity-seal.json')['files']:
            if digest(r['path'])!=r['sha256']:raise ValueError('SEALED_OUTPUT_CHANGED')
        outputs=read(root/'all-outputs-sealed.json');bindings=read(root/'data-bindings.json');pools=bindings['pools']
        labels={s:read(root/(s+'-labels.json')) for s in SPLITS}
    else:
        outputs=[];pools=read(root/'data-bindings.json')['pools'] if (root/'data-bindings.json').exists() else {s:[None]*n for s,n in zip(SPLITS,NS)};labels={}
    lookup={}
    for r in outputs:
        key=(r['method'],r['seed'],r['split'],r['index'],r['video'],r['question'])
        if key in lookup:raise ValueError('DUPLICATE_OUTPUT')
        lookup[key]=r
    conditions=[];four={};integers=[]
    for split,n in zip(SPLITS,NS):
        configurations=[(m,s) for m in METHODS for s in (19,73)]+([('B0','NA')] if split==SPLITS[3] else [])
        for method,seed in configurations:
            row=dict(method=method,seed=seed,split=split,training_pool_n='NA' if method=='B0' else 25 if method.endswith('25') else 68,n_instances=n,n_cells=4*n,cached_cells=0,new_cells=0,complete_cells=0,valid_cells=0,correct_cells=0,video_pair_correct=0,question_pair_correct=0,four_way_correct=0,invalid_cells=0,failed_cells=0,not_run_cells=0,unknown_cells=0,status='COMPLETE')
            values=[]
            for i in range(n):
                cells=[];unknown=False
                for vi in (0,1):
                    for qi in (0,1):
                        r=lookup.get((method,seed,split,i,vi,qi),dict(status='NOT_RUN'));state=r['status'];correct=0
                        row['cached_cells' if r.get('origin')=='CACHED' else 'new_cells']+=int('origin' in r)
                        if state in ('CLOSED','INVALID'):
                            row['complete_cells']+=1
                            if state=='CLOSED':
                                if r['prediction'] not in (0,1):raise ValueError('INVALID_BINARY_PREDICTION')
                                row['valid_cells']+=1;correct=int(r['prediction']==labels[split][i]['labels'][vi][qi])
                            else:row['invalid_cells']+=1
                        elif state in ('FAILED','NOT_RUN'):
                            row['failed_cells' if state=='FAILED' else 'not_run_cells']+=1;row['unknown_cells']+=1;unknown=True
                        else:row['unknown_cells']+=1;unknown=True
                        row['correct_cells']+=correct;cells.append(correct)
                        integers.append(dict(method=method,seed=seed,split=split,index=i,video=vi,question=qi,status=state,correct=correct))
                row['video_pair_correct']+=cells[0]*cells[2]+cells[1]*cells[3]
                row['question_pair_correct']+=cells[0]*cells[1]+cells[2]*cells[3]
                success=int(all(cells));row['four_way_correct']+=success;values.append(None if unknown else success)
            if row['unknown_cells']:
                row['status']='INCOMPLETE'
                for k in ('correct_cells','video_pair_correct','question_pair_correct','four_way_correct'):row[k]='NA'
            for k,den in [('item_accuracy',4*n),('video_pair_accuracy',2*n),('question_pair_accuracy',2*n),('four_way_accuracy',n)]:
                count={'item_accuracy':'correct_cells','video_pair_accuracy':'video_pair_correct','question_pair_accuracy':'question_pair_correct','four_way_accuracy':'four_way_correct'}[k]
                row[k]=row[count]/den if row['status']=='COMPLETE' else 'NA'
            conditions.append(row);four[(method,seed,split)]=values
    comparisons=[('A68','A25'),('P1_68','P1_25'),('A68','B0'),('P1_68','B0'),('P1_68','A68')]
    paired=[];profile=[]
    for seed in (19,73):
        for left,right in comparisons:
            L=four[(left,seed,SPLITS[3])];R=four[(right,'NA' if right=='B0' else seed,SPLITS[3])]
            row=dict(seed=seed,left=left,right=right,n=50,left_only=0,right_only=0,both_correct=0,both_wrong=0,unknown=0,net='NA',delta_four_way_pp='NA',bootstrap_low_pp='NA',bootstrap_high_pp='NA')
            groupstats={}
            if pools[SPLITS[3]][0] is not None:
                for k in sorted({x['group_key'] for x in pools[SPLITS[3]]}):
                    ids=[i for i,r in enumerate(pools[SPLITS[3]]) if r['group_key']==k];stats=dict(n=len(ids),left_only=0,right_only=0,both_correct=0,both_wrong=0,unknown=0,net=0)
                    for i in ids:
                        a,b=L[i],R[i];field='unknown' if a is None or b is None else 'left_only' if a and not b else 'right_only' if b and not a else 'both_correct' if a else 'both_wrong'
                        stats[field]+=1
                    stats['net']=stats['left_only']-stats['right_only'] if not stats['unknown'] else None;groupstats[k]=stats
                    profile.append(dict(family=f'F{len(groupstats):02}',seed=seed,left=left,right=right,**stats))
            for a,b in zip(L,R):row['unknown' if a is None or b is None else 'left_only' if a and not b else 'right_only' if b and not a else 'both_correct' if a else 'both_wrong']+=1
            if not row['unknown']:
                row['net']=row['left_only']-row['right_only'];row['delta_four_way_pp']=2*row['net']
                row['bootstrap_low_pp'],row['bootstrap_high_pp']=bootstrap(groupstats)
            paired.append(row)
    complete=all(r['status']=='COMPLETE' for r in conditions)
    gate=None
    if complete:
        gate=all(next(r for r in conditions if r['method']=='A68' and r['seed']==s and r['split']==SPLITS[3])['four_way_correct']>=10 for s in (19,73)) and all(r['net']>=4 for r in paired if (r['left'],r['right'])==('A68','A25')) and sum(r['net'] for r in paired if (r['left'],r['right'])==('A68','B0'))>0
    old_reproduction=[]
    if executed:
        assets=read(root/'prior-assets.json');oldroots=dict(A25=Path(assets['prior057']),P1_25=Path(assets['prior059']))
        for method,prior in oldroots.items():
            expected=read(prior/'scoring-summary.json')['conditions']
            for oldsplit in ('train','validation','development_test'):
                for seed in (19,73):
                    maps=[r for r in bindings['old_mapping'] if r['old_split']==oldsplit];subset=[r for r in integers if r['method']==method and r['seed']==seed and any((r['split'],r['index'])==(m['split'],m['index']) for m in maps)]
                    target=next(r for r in expected if r['split']==oldsplit and int(r['seed'])==seed and r['arm']==('A' if method=='A25' else 'P1'))
                    cells={(r['split'],r['index'],r['video'],r['question']):r['correct'] for r in subset}
                    counts=dict(correct_cells=sum(cells.values()),video_pair_correct=0,question_pair_correct=0,four_way_correct=0)
                    for m in maps:
                        c=[cells[(m['split'],m['index'],v,q)] for v in (0,1) for q in (0,1)]
                        counts['video_pair_correct']+=c[0]*c[2]+c[1]*c[3];counts['question_pair_correct']+=c[0]*c[1]+c[2]*c[3];counts['four_way_correct']+=int(all(c))
                    if any(counts[k]!=target[k] for k in counts):raise ValueError('OLD_CACHE_METRICS_CHANGED')
                    old_reproduction.append(dict(method=method,seed=seed,old_split=oldsplit,n=len(maps),**counts,status='PASS'))
    for name,records in [('condition-summary.csv',conditions),('paired-summary.csv',paired)]:
        with open(root/name,'x',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    save(root/'score-integers.json',integers)
    status='A_POOL_EXPANSION_TRANSFER_SIGNAL' if gate else 'NO_PRIMARY_A_TRANSFER_SIGNAL' if complete else 'INCOMPLETE/UNKNOWN'
    save(root/'scoring-summary.json',dict(status=status,complete=complete,gate=gate,conditions=conditions,paired=paired,source_profile=profile,old_cache_reproduction=old_reproduction,timeblind='NOT_RUN'))
    print('SCORE_CLOSED',status,flush=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=('prepare','freeze','train','predict','score'));p.add_argument('--root',required=True)
    for name in ('prior056','prior057','prior059'):p.add_argument('--'+name)
    a=p.parse_args()
    if a.phase=='prepare':prepare(a.root,a.prior056,a.prior057,a.prior059)
    else:globals()[a.phase](a.root)
