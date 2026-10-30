"""058 explicit CPU order control. Import has no data/model/optimizer actions."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import time

SPLITS=('train','validation','development_test')
PERMUTATIONS=((5,4,3,2,1,0),(1,2,3,4,5,0),(2,5,1,4,0,3),(0,2,4,1,3,5))


def save(path,data):
    with open(path,'x',encoding='utf-8') as f:
        json.dump(data,f,sort_keys=True,indent=2);f.flush();os.fsync(f.fileno())


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def head_module():
    path=Path(__file__).with_name('question_temporal_056.py')
    spec=importlib.util.spec_from_file_location('head056',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def row_bytes(V):
    import numpy as np
    import torch
    if V.device.type!='cpu' or V.dtype!=torch.float32 or V.shape!=(6,2560) or not torch.isfinite(V).all():raise ValueError('VISUAL_FEATURE_CONTRACT')
    return [np.ascontiguousarray(row.detach().numpy(),dtype='<f4').tobytes(order='C') for row in V]


def content_order(V):
    import torch
    rows=row_bytes(V)
    order=sorted(range(6),key=lambda i:(hashlib.sha256(rows[i]).digest(),rows[i]))
    return torch.stack([V[i] for i in order])


def predict(model,V,q):
    """Current video and question only; no metadata/other predictions."""
    return head_module().predict(model,content_order(V),q)


def prepare(root,prior):
    import torch
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized() or os.environ.get('CUDA_VISIBLE_DEVICES')!='':raise ValueError('CPU_ONLY')
    root=Path(root);prior=Path(prior);assets=[];checks=0
    def check(ok):
        nonlocal checks
        if not ok:raise ValueError('INPUT_OR_TRANSFORM_CHECK_'+str(checks))
        checks+=1
    def record(path):
        path=Path(path);assets.append(dict(path=str(path),sha256=digest(path),bytes=path.stat().st_size))
    check(json.loads((prior/'parent-closed.json').read_text(encoding='utf-8-sig'))['push']=='SUCCEEDED')
    check(json.loads((prior/'training-job.json').read_text())['active']==0)
    index=json.loads((prior/'feature-index.json').read_text());check(len(index['video'])==102 and len(index['text'])==54)
    original_seal=json.loads((prior/'evaluation-input-seal.json').read_text())
    known={str(Path(x['path']).resolve()):x['sha256'] for x in original_seal['files']}
    for path in [prior/'feature-index.json',prior/'head-outputs-sealed.json',prior/'all-outputs-seal.json']:
        check(digest(path)==known[str(path.resolve())]);record(path)
    predictions=json.loads((prior/'head-outputs-sealed.json').read_text());a=[x for x in predictions if x['arm']=='A']
    check(len(a)==408 and all(x['status']=='CLOSED' for x in a));save(root/'a-cached-sealed.json',a)
    closure=json.loads((prior/'all-outputs-seal.json').read_text());check(closure['outputs_sha256']==digest(prior/'head-outputs-sealed.json') and closure['complete'])
    # Strip answer arrays lexically before decoding source-group metadata.
    body=(prior/'pilot-input-seal.json').read_text()
    body,n=re.subn(r'"labels"\s*:\s*\[\s*\[\s*[01]\s*,\s*[01]\s*\]\s*,\s*\[\s*[01]\s*,\s*[01]\s*\]\s*\]', '"labels":null',body)
    check(n==51)
    source=json.loads(body)['selected'];observations={};group_sets={};bindings={}
    record(prior/'pilot-input-seal.json')
    for split,expected_n in zip(SPLITS,[25,2,24]):
        path=prior/(split+'-observations.json');rows=json.loads(path.read_text());record(path)
        check(len(rows)==expected_n and [x['index'] for x in rows]==list(range(expected_n)))
        check(all(row['videos']==src['videos'] and row['questions']==src['questions'] for row,src in zip(rows,source[split])))
        observations[split]=rows;group_sets[split]={x['group_key'] for x in source[split]}
        bindings[split]=[dict(index=i,group_key=x['group_key']) for i,x in enumerate(source[split])]
        save(root/(split+'-observations.json'),rows)
    check([len(group_sets[s]) for s in SPLITS]==[16,2,15])
    for a_split,b_split in [('train','validation'),('train','development_test'),('validation','development_test')]:check(not group_sets[a_split]&group_sets[b_split])
    labels=prior/'train-labels.json';record(labels)
    with open(root/'train-labels.json','xb') as f:f.write(labels.read_bytes())
    save(root/'source-bindings.json',bindings)
    folder=root/'h-features';folder.mkdir();hindex={};changed=0
    for i,(name,row) in enumerate(index['video'].items()):
        path=prior/'features'/row['path'];check(digest(path)==known[str(path.resolve())]);record(path)
        V=torch.load(path,map_location='cpu',weights_only=True);before=row_bytes(V);H=content_order(V)
        check(Counter(row_bytes(H))==Counter(before));check(row_bytes(content_order(H))==row_bytes(H))
        for permutation in PERMUTATIONS:check(row_bytes(content_order(V[list(permutation)]))==row_bytes(H))
        check(row_bytes(V)==before)
        changed+=int(row_bytes(H)!=before)
        target=folder/(str(i)+'.pt');torch.save(H,target);hindex[name]=dict(path=target.name,sha256=digest(target))
    for row in index['text'].values():
        path=prior/'features'/row['path'];check(digest(path)==known[str(path.resolve())]);record(path)
        q=torch.load(path,map_location='cpu',weights_only=True)
        check(q.shape==(2560,) and q.dtype==torch.float32 and q.device.type=='cpu' and bool(torch.isfinite(q).all()))
    plans={}
    for seed in [19,73]:
        path=prior/('pretrain-seed'+str(seed)+'.pt');other=prior/'training'/('plan-'+str(seed)+'.pt')
        original=torch.load(path,map_location='cpu',weights_only=True);repeated=torch.load(other,map_location='cpu',weights_only=True)
        check(torch.equal(original['sequence'],repeated['sequence']) and original['sequence'].shape==(250,8))
        check(set(original['state'])==set(repeated['state']) and all(torch.equal(original['state'][k],repeated['state'][k]) for k in original['state']))
        record(path);record(other)
        target=root/('initial-seed'+str(seed)+'.pt')
        with open(target,'xb') as f:torch.save(original,f)
        plans[str(seed)]=dict(path=target.name,sha256=digest(target))
    head=Path(__file__).with_name('question_temporal_056.py');old_code=known[str(head.resolve())]
    check(digest(head)==old_code);record(head)
    source057=Path(__file__).with_name('question_temporal_train_057.py')
    record(source057);check(digest(source057)==known[str(source057.resolve())])
    check(not torch.cuda.is_initialized())
    save(root/'h-index.json',hindex)
    save(root/'training-config.json',dict(prior=str(prior),text_index=index['text'],plans=plans,arm='H',loss_arm='A',parameters=356673,steps=250,seeds=[19,73]))
    save(root/'input-seal.json',dict(status='SEALED_BEFORE_H_STARTED',assets=assets,code_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        checks=checks,videos=102,text_features=54,changed_video_orders=changed,permutations=PERMUTATIONS,
        transform='sort rows by(SHA256(little-endian contiguous float32 row bytes).digest(),row bytes)',
        research_updates=0,fixture_updates=0,cuda_initialized=False))
    print('INPUT_AND_TRANSFORM_PASS',checks,'changed orders',changed,flush=True)


def training(root):
    import torch
    root=Path(root);torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized() or os.environ.get('CUDA_VISIBLE_DEVICES')!='':raise ValueError('CPU_ONLY')
    config=json.loads((root/'training-config.json').read_text());prior=Path(config['prior'])
    head=head_module();index=json.loads((root/'h-index.json').read_text())
    observations={s:json.loads((root/(s+'-observations.json')).read_text()) for s in SPLITS}
    def v(name):return torch.load(root/'h-features'/index[name]['path'],map_location='cpu',weights_only=True)
    def q(text):return torch.load(prior/'features'/config['text_index'][text]['path'],map_location='cpu',weights_only=True)
    V=torch.stack([torch.stack([v(name) for name in r['videos']]) for r in observations['train']])
    Q=torch.stack([torch.stack([q(text) for text in r['questions']]) for r in observations['train']])
    labels=torch.tensor([x['labels'] for x in json.loads((root/'train-labels.json').read_text())],dtype=torch.float32)
    output=root/'training';output.mkdir();records=[];predictions=[];deadline=time.monotonic()+530
    for seed in [19,73]:
        claim=root/('058-H-seed'+str(seed)+'.claim')
        save(claim,dict(status='STARTED',task='058',arm='H',loss_arm='A',seed=seed))
        original=torch.load(root/config['plans'][str(seed)]['path'],map_location='cpu',weights_only=True)
        state,sequence=original['state'],original['sequence'];start=time.monotonic()
        try:
            model=head.train(V,Q,labels,'A',seed,state,sequence,output/('058-H-seed'+str(seed)),deadline)
            parameter_count=sum(p.numel() for p in model.parameters())
            if parameter_count!=356673:raise ValueError('PARAMETERS')
            change=sum(float((model.state_dict()[k]-state[k]).abs().sum()) for k in state)
            for split,rows in observations.items():
                for row in rows:
                    for vi,name in enumerate(row['videos']):
                        for qi,text in enumerate(row['questions']):
                            if time.monotonic()>deadline:raise TimeoutError('CPU_EVAL_DEADLINE')
                            # Idempotent fixed current-video view; q is untouched.
                            pred=head.predict(model,content_order(v(name)),q(text))
                            predictions.append(dict(arm='H',seed=seed,split=split,index=row['index'],video=vi,question=qi,status='CLOSED',prediction=int(pred)))
            records.append(dict(arm='H',loss_arm='A',seed=seed,status='CLOSED',parameters=parameter_count,parameter_l1_change=change,outer_s=time.monotonic()-start))
            del model
        except Exception as error:records.append(dict(arm='H',loss_arm='A',seed=seed,status='FAILED',reason=str(error),outer_s=time.monotonic()-start))
        save(root/('058-H-seed'+str(seed)+'.terminal'),records[-1]);print('H_CONFIG',seed,records[-1]['status'],flush=True)
    save(root/'h-outputs-sealed.json',predictions);save(root/'training-summary.json',records)
    identities=[root/'h-outputs-sealed.json',root/'input-seal.json',root/'h-index.json',Path(__file__)]+list(output.glob('*/final.pt'))
    save(root/'outputs-identity-seal.json',dict(status='SEALED_BEFORE_SCORING',files=[dict(path=str(p),sha256=digest(p)) for p in identities],cuda_initialized=torch.cuda.is_initialized()))


def scoring(root):
    import csv
    root=Path(root);config=json.loads((root/'training-config.json').read_text());prior=Path(config['prior'])
    job=json.loads((root/'training-job.json').read_text())
    if job['active']!=0:raise RuntimeError('TRAINING_NOT_EXITED')
    for record in json.loads((root/'outputs-identity-seal.json').read_text())['files']:
        if digest(record['path'])!=record['sha256']:raise ValueError('OUTPUT_SEAL')
    labels={s:json.loads((prior/(s+'-labels.json')).read_text()) for s in SPLITS}
    old=json.loads((root/'a-cached-sealed.json').read_text());new=json.loads((root/'h-outputs-sealed.json').read_text())
    lookup={}
    for row in old+new:
        arm='A_CACHED' if row['arm']=='A' else 'H';key=(row['split'],arm,row['seed'],row['index'],row['video'],row['question'])
        if key in lookup:raise ValueError('DUPLICATE_OUTPUT')
        lookup[key]=row
    bindings=json.loads((root/'source-bindings.json').read_text());conditions=[];four={};integers=[]
    for split,n in zip(SPLITS,[25,2,24]):
        for seed in [19,73]:
            for arm in ['A_CACHED','H']:
                row=dict(dataset='DyBench_Breakfast_058',split=split,arm=arm,seed=seed,n_instances=n,n_cells=4*n,complete_cells=0,correct_cells=0,video_pair_correct=0,question_pair_correct=0,four_way_correct=0,failed_cells=0,invalid_cells=0,not_run_cells=0,status='COMPLETE',prediction_origin='057_CACHED' if arm=='A_CACHED' else '058_NEW')
                four[(split,arm,seed)]=[]
                for i in range(n):
                    correct=[];unknown=False
                    for vi in range(2):
                        for qi in range(2):
                            prediction=lookup.get((split,arm,seed,i,vi,qi),dict(status='NOT_RUN',prediction=None))
                            status=prediction['status']
                            if status=='NOT_RUN':row['not_run_cells']+=1;unknown=True
                            elif status=='FAILED':row['failed_cells']+=1;unknown=True
                            elif status=='INVALID':row['invalid_cells']+=1;unknown=True
                            elif status=='CLOSED':row['complete_cells']+=1
                            else:raise ValueError('UNKNOWN_STATUS')
                            flag=int(status=='CLOSED' and prediction['prediction']==labels[split][i]['labels'][vi][qi]);correct.append(flag);row['correct_cells']+=flag
                            integers.append(dict(split=split,arm=arm,seed=seed,index=i,video=vi,question=qi,correct=flag,status=status))
                    row['video_pair_correct']+=correct[0]*correct[2]+correct[1]*correct[3]
                    row['question_pair_correct']+=correct[0]*correct[1]+correct[2]*correct[3]
                    row['four_way_correct']+=int(all(correct));four[(split,arm,seed)].append(None if unknown else int(all(correct)))
                if row['not_run_cells'] or row['failed_cells'] or row['invalid_cells']:row['status']='INCOMPLETE'
                if arm=='A_CACHED' and row['four_way_correct']!={'train':{19:24,73:20},'validation':{19:2,73:2},'development_test':{19:5,73:7}}[split][seed]:raise ValueError('ORIGINAL_A_BINDING_FAILED')
                conditions.append(row)
    groups={}
    for row in bindings['development_test']:groups.setdefault(row['group_key'],[]).append(row['index'])
    pairs=[];profile=[]
    for seed in [19,73]:
        a=four[('development_test','A_CACHED',seed)];h=four[('development_test','H',seed)]
        row=dict(seed=seed,n_instances=24,a_only=0,h_only=0,both_correct=0,both_wrong=0,unknown=0,net_instances='NA',delta_four_way_pp='NA',bootstrap_low_pp='NA',bootstrap_high_pp='NA')
        for av,hv in zip(a,h):
            if av is None or hv is None:row['unknown']+=1
            else:row['a_only' if av and not hv else 'h_only' if hv and not av else 'both_correct' if av else 'both_wrong']+=1
        if not row['unknown']:
            row['net_instances']=row['a_only']-row['h_only'];row['delta_four_way_pp']=100*row['net_instances']/24
            rng=random.Random(55058);keys=sorted(groups);boot=[]
            for _ in range(10000):
                ids=[i for g in rng.choices(keys,k=15) for i in groups[g]];boot.append(100*sum(a[i]-h[i] for i in ids)/len(ids))
            boot.sort()
            for name,p in [('bootstrap_low_pp',.025),('bootstrap_high_pp',.975)]:
                position=9999*p;i=int(position);row[name]=boot[i]+(position-i)*(boot[min(i+1,9999)]-boot[i])
        pairs.append(row)
        for k,key in enumerate(sorted(groups)):
            ids=groups[key];known=all(a[i] is not None and h[i] is not None for i in ids)
            item=dict(source='S'+str(k+1).zfill(2),seed=seed,n=len(ids),a_only=0,h_only=0,both_correct=0,both_wrong=0,unknown=0,net='NA')
            for i in ids:
                if a[i] is None or h[i] is None:item['unknown']+=1
                else:item['a_only' if a[i] and not h[i] else 'h_only' if h[i] and not a[i] else 'both_correct' if a[i] else 'both_wrong']+=1
            if known:item['net']=item['a_only']-item['h_only']
            profile.append(item)
    complete=all(r['status']=='COMPLETE' for r in conditions) and all(not p['unknown'] for p in pairs)
    gate=complete and all(p['net_instances']>=2 for p in pairs)
    status='ORDER_BENEFIT_DEVELOPMENT_SIGNAL' if gate else 'NO_CLEAR_ORDER_BENEFIT_IN_THIS_PILOT' if complete else 'INCOMPLETE'
    for name,rows in [('condition-summary.csv',conditions),('paired-summary.csv',pairs)]:
        with open(root/name,'x',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    save(root/'score-integers.json',integers);save(root/'scoring-summary.json',dict(status=status,gate=gate,complete=complete,conditions=conditions,paired=pairs,source_profile=profile))
    print(status,[(x['seed'],x['net_instances']) for x in pairs],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','training','scoring']);parser.add_argument('--root',required=True);parser.add_argument('--prior')
    args=parser.parse_args()
    if args.phase=='prepare':prepare(args.root,args.prior)
    else:globals()[args.phase](args.root)
