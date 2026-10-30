"""057 pilot orchestration. All operations require an explicit entry call.

No import-time network, model, or optimizer work. Closed056 remains unchanged.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import time
import zipfile

REVISION='fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405'


def helper(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def save(path,data):
    import os
    with open(path,'x',encoding='utf-8') as f:
        json.dump(data,f,indent=2,sort_keys=True);f.flush();os.fsync(f.fileno())


def seal(root,prior):
    root=Path(root);prior=Path(prior); consumed=0; files={}; copied={}
    names=['training-handoff-local.json','source-summary.json','source-table.json','candidate-split.json',
           'prior-copies.json','independent-review.json','implementation.json','additional-checks.json',
           'breakfast-revision.json','acquisition-status.json','acquisition-job.json','implementation-job.json',
           'additional-job.json','sourcejoin-job.json','review-job.json']
    for name in names:
        size=(prior/name).stat().st_size
        if size>2*1024**2 or consumed+size>16*1024**2:raise ValueError('PRIOR_METADATA_CAP')
        body=(prior/name).read_bytes();consumed+=len(body)
        files[name]=hashlib.sha256(body).hexdigest();copied[name]=json.loads(body)
        with open(root/('prior_'+name),'xb') as f:f.write(body)
    plan=copied['candidate-split.json']['selected'];source=copied['source-table.json']['qualified']
    if {k:len(v) for k,v in plan.items()}!=dict(train=25,validation=2,development_test=24):raise ValueError('FIXED_SPLIT')
    if len(source)!=51 or sorted(x['recording'] for v in plan.values() for x in v)!=sorted(x['recording'] for x in source):raise ValueError('MEMBERSHIP')
    groups={k:{x['group_key'] for x in v} for k,v in plan.items()}
    if any(groups[a]&groups[b] for a,b in [('train','validation'),('train','development_test'),('validation','development_test')]):raise ValueError('SOURCE_OVERLAP')
    for entries in plan.values():
        for row in entries:
            if row['evidence']!='ANNOTATION_JOIN' or len(row['videos'])!=2 or row['labels'][0][0]!=row['labels'][1][1] or row['labels'][0][1]!=row['labels'][1][0] or sum(row['labels'][0])!=1:raise ValueError('SOURCE_LABEL_BINDING')
    public=Path(__file__).parent.parent/'docs/codex-artifacts/VLM-TEMPORAL-DATA-READY-056/readiness-summary.json'
    expected=json.loads(public.read_text())['source_code_sha256'];code={}
    for name,want in expected.items():
        body=Path(__file__).with_name(name).read_bytes(); lf=body.replace(b'\r\n',b'\n')
        if hashlib.sha256(lf).hexdigest()!=want:raise ValueError('PUBLIC_SOURCE_LF_MISMATCH')
        code[name]=dict(lf_sha256=want,actual_sha256=hashlib.sha256(body).hexdigest())
    record=dict(task='VLM-TEMPORAL-TRAIN-PILOT-057',scope='NEW_SMALL_PILOT_25_2_24',
                original056_gate='HOLD_UNCHANGED',media_permitted_057=True,selected=plan,
                prior_file_sha256=files,prior_bytes=consumed,public_code=code,
                thresholds=dict(i_a_pp=5,i_a_net_instances=2,i_v_gt=0,i_s_gt=0,mean_i_b0_gt=0),
                max_calls=dict(video=102,text=102,b0=96,total=300),max_optimizer_steps=2000)
    save(root/'pilot-input-seal.json',record)
    for split,rows in plan.items():
        save(root/(split+'-labels.json'),[dict(index=i,labels=r['labels']) for i,r in enumerate(rows)])
        save(root/(split+'-observations.json'),[dict(index=i,videos=r['videos'],questions=r['questions']) for i,r in enumerate(rows)])
    print('INPUT_SEAL_CLOSED:51 pairs;25/2/24;original056 unchanged',flush=True)


def download(root):
    root=Path(root);seal=json.loads((root/'pilot-input-seal.json').read_text())
    if seal['task']!='VLM-TEMPORAL-TRAIN-PILOT-057' or not seal['media_permitted_057']:raise ValueError('PILOT_PERMISSION')
    if shutil.disk_usage(root).free<10*1024**3:raise ValueError('DISK_GATE')
    data=helper('question_temporal_data_056');client=data.Fetcher(root)
    entry=json.loads(client.get('event_identity','https://huggingface.co/api/datasets/ddz16/DyBench/tree/'+REVISION+'/video?expand=false').read_bytes())
    matches=[x for x in entry if x['path']=='video/event_sequence.zip']
    if len(matches)!=1 or matches[0]['size']!=2783546023:raise ValueError('OFFICIAL_SIZE')
    content_sha=matches[0].get('lfs',{}).get('oid','')
    if len(content_sha)!=64 or any(c not in '0123456789abcdef' for c in content_sha):raise ValueError('PUBLISHER_CONTENT_SHA')
    save(root/'media-plan.json',dict(size=2783546023,publisher_content_sha256=content_sha,revision=REVISION))
    client.get('event_sequence_zip','https://huggingface.co/datasets/ddz16/DyBench/resolve/'+REVISION+'/video/event_sequence.zip',media=True,expected_size=2783546023,expected_sha=content_sha)
    print('MEDIA_SHA_SIZE_CLOSED',flush=True)


def extract(root):
    root=Path(root);data=helper('question_temporal_data_056')
    archive=root/'event_sequence_zip.body';plan=json.loads((root/'pilot-input-seal.json').read_text())
    names=[n for rows in plan['selected'].values() for r in rows for n in r['videos']]
    if len(names)!=102 or len(set(names))!=102:raise ValueError('FIXED102')
    with zipfile.ZipFile(archive) as f:
        selected=[]
        for name in names:
            matches=[x.filename for x in f.infolist() if Path(x.filename).name==name]
            if len(matches)!=1:raise ValueError('UNIQUE_PUBLISHED_PREFIX')
            selected.append(matches[0])
    destination=root/'media';destination.mkdir()
    entries=data.extract_selected(archive,selected,destination)
    for requested,entry in zip(names,entries):entry['requested']=requested
    save(root/'media-manifest.json',entries)
    print('MEDIA_CRC_CLOSED:102',flush=True)


def decode(root):
    root=Path(root);data=helper('question_temporal_data_056');cache=root/'frames';cache.mkdir()
    start=time.monotonic();deadline=start+1750;budget=[0];results={}
    for entry in json.loads((root/'media-manifest.json').read_text()):
        name=entry['requested']
        try:
            result=data.prepare_cache(root/'media'/entry['path'],cache,budget,deadline)
            import av
            with av.open(str(root/'media'/entry['path'])) as container:
                stream=container.streams.video[0]
                result['fps']=float(stream.average_rate);result['total_num_frames']=stream.frames
                result['duration']=float(stream.duration*stream.time_base)
                base=float(stream.start_time or 0)*float(stream.time_base)
                if max(abs(stamp-base-index/result['fps']) for stamp,index in zip(result['timestamps'],result['indices']))>1/result['fps']:
                    raise ValueError('FRAME_INDEX_CLOCK_NOT_CFR')
        except Exception as error:result=dict(status='FAILED',reason=str(error))
        results[name]=result
        print('CACHE_PROGRESS',len(results),'/102',result['status'],'frames',budget[0],flush=True)
        if time.monotonic()>deadline:break
    save(root/'cache-manifest.json',dict(records=results,decoded_frames=budget[0],outer_s=time.monotonic()-start,
                                       complete=sum(x['status']=='CLOSED' for x in results.values())))
    if len(results)!=102 or any(x['status']!='CLOSED' for x in results.values()):raise RuntimeError('REAL_INPUT_INCOMPLETE')
    print('REAL_INPUT_CLOSED:102',flush=True)


def training(root):
    """One CPU role; train labels only, no evaluation labels or B0 reads."""
    import torch
    root=Path(root);head=helper('question_temporal_056')
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized():raise RuntimeError('CPU_ROLE_CUDA')
    gpu_job=json.loads((root/'gpu-job.json').read_text())
    if gpu_job['active']!=0 or gpu_job['exit_code']!=0 or not (root/'gpu-success.json').exists():raise RuntimeError('GPU_NOT_CLOSED')
    index=json.loads((root/'feature-index.json').read_text()); observations={s:json.loads((root/(s+'-observations.json')).read_text()) for s in ['train','validation','development_test']}
    def v(name):return torch.load(root/'features'/index['video'][name]['path'],map_location='cpu',weights_only=True)
    def q(text):return torch.load(root/'features'/index['text'][text]['path'],map_location='cpu',weights_only=True)
    V=torch.stack([torch.stack([v(name) for name in row['videos']]) for row in observations['train']])
    Q=torch.stack([torch.stack([q(text) for text in row['questions']]) for row in observations['train']])
    labels=torch.tensor([x['labels'] for x in json.loads((root/'train-labels.json').read_text())],dtype=torch.float32)
    if len(V)!=25 or labels.shape!=(25,2,2):raise ValueError('TRAIN_SHAPE')
    directory=root/'training';directory.mkdir();deadline=time.monotonic()+1700;records=[];outputs=[]
    for seed in [19,73]:
        state,sequence=head.shared_plan(V.shape[-1],Q.shape[-1],25,seed)
        torch.save(dict(state=state,sequence=sequence),directory/('plan-'+str(seed)+'.pt'))
        for arm in ['A','V','S','I']:
            destination=directory/(arm+'-'+str(seed));start=time.monotonic()
            try:
                model=head.train(V,Q,labels,arm,seed,state,sequence,destination,deadline)
                change=sum(float((model.state_dict()[key]-state[key]).abs().sum()) for key in state)
                for split,rows in observations.items():
                    for row in rows:
                        for vi,name in enumerate(row['videos']):
                            for qi,text in enumerate(row['questions']):
                                if time.monotonic()>deadline:raise TimeoutError('CPU_EVAL_DEADLINE')
                                prediction=head.predict(model,v(name),q(text))
                                outputs.append(dict(arm=arm,seed=seed,split=split,index=row['index'],video=vi,question=qi,status='CLOSED',prediction=int(prediction)))
                records.append(dict(arm=arm,seed=seed,status='CLOSED',parameter_count=sum(p.numel() for p in model.parameters()),parameter_l1_change=change,outer_s=time.monotonic()-start))
                del model
            except Exception as error:records.append(dict(arm=arm,seed=seed,status='FAILED',reason=str(error),outer_s=time.monotonic()-start))
            print('TRAIN_CONFIG',arm,seed,records[-1]['status'],flush=True)
    save(root/'head-outputs-sealed.json',outputs);save(root/'training-summary.json',records)
    save(root/'all-outputs-seal.json',dict(outputs_sha256=hashlib.sha256((root/'head-outputs-sealed.json').read_bytes()).hexdigest(),
        b0_sha256=hashlib.sha256((root/'b0-sealed.json').read_bytes()).hexdigest(),research_steps_planned=2000,complete=all(x['status']=='CLOSED' for x in records)))
    print('TRAINING_ROLE_CLOSED',flush=True)


def scoring(root):
    """Explicit scoring role after all outputs sealed, or all-NOT_RUN closure."""
    import csv
    import random
    root=Path(root);plan=json.loads((root/'pilot-input-seal.json').read_text())
    executed=(root/'all-outputs-seal.json').exists()
    if executed:
        seal=json.loads((root/'all-outputs-seal.json').read_text())
        if hashlib.sha256((root/'head-outputs-sealed.json').read_bytes()).hexdigest()!=seal['outputs_sha256'] or hashlib.sha256((root/'b0-sealed.json').read_bytes()).hexdigest()!=seal['b0_sha256']:raise ValueError('OUTPUT_SEAL')
        predictions=json.loads((root/'head-outputs-sealed.json').read_text())
        b0=json.loads((root/'b0-sealed.json').read_text())
        labels={s:json.loads((root/(s+'-labels.json')).read_text()) for s in plan['selected']}
    else:
        predictions=[];b0=[];labels={}
    index={}
    for row in predictions:
        key=(row['split'],row['arm'],row['seed'],row['index'],row['video'],row['question'])
        if key in index:raise ValueError('DUPLICATE_OUTPUT')
        index[key]=row
    for row in b0:index[('development_test','B0','NA',row['index'],row['video'],row['question'])]=row
    conditions=[];integer=[];four={}
    for split,instances in plan['selected'].items():
        configurations=[(a,s) for s in [19,73] for a in ['A','V','S','I']]+([('B0','NA')] if split=='development_test' else [])
        for arm,seed in configurations:
            row=dict(dataset='DyBench_Breakfast_057',split=split,arm=arm,seed=seed,n_instances=len(instances),n_cells=4*len(instances),complete_cells=0,correct_cells=0,video_pair_correct=0,question_pair_correct=0,four_way_correct=0,failed_cells=0,invalid_cells=0,not_run_cells=0,status='COMPLETE')
            four[(split,arm,seed)]=[]
            for i,instance in enumerate(instances):
                cells=[];unknown=False
                for vi in range(2):
                    for qi in range(2):
                        output=index.get((split,arm,seed,i,vi,qi),dict(status='NOT_RUN',prediction=None))
                        status=output['status']
                        if status=='NOT_RUN':row['not_run_cells']+=1;unknown=True
                        elif status=='FAILED':row['failed_cells']+=1
                        elif status=='INVALID':row['invalid_cells']+=1;row['complete_cells']+=1
                        elif status=='CLOSED':row['complete_cells']+=1
                        else:raise ValueError('UNKNOWN_OUTPUT_STATUS')
                        correct=int(status=='CLOSED' and labels[split][i]['labels'][vi][qi]==output['prediction']) if executed else 0
                        row['correct_cells']+=correct;cells.append(correct)
                        integer.append(dict(split=split,arm=arm,seed=seed,index=i,video=vi,question=qi,status=status,correct=correct,group=instance['group_key']))
                row['video_pair_correct']+=cells[0]*cells[2]+cells[1]*cells[3]
                row['question_pair_correct']+=cells[0]*cells[1]+cells[2]*cells[3]
                success=int(all(cells));row['four_way_correct']+=success
                four[(split,arm,seed)].append(None if unknown else success)
            if row['not_run_cells'] or row['failed_cells']:row['status']='INCOMPLETE'
            conditions.append(row)
    paired=[];groups={}
    for i,row in enumerate(plan['selected']['development_test']):groups.setdefault(row['group_key'],[]).append(i)
    for seed in [19,73]:
        for comparator in ['A','V','S','B0']:
            left=four[('development_test','I',seed)];right=four[('development_test',comparator,'NA' if comparator=='B0' else seed)]
            row=dict(seed=seed,comparator=comparator,n_instances=24,i_only=0,comparator_only=0,both_correct=0,both_wrong=0,unknown=0,delta_four_way_pp='NA',bootstrap_low_pp='NA',bootstrap_high_pp='NA')
            for a,b in zip(left,right):
                if a is None or b is None:row['unknown']+=1
                else:row['i_only' if a and not b else 'comparator_only' if b and not a else 'both_correct' if a else 'both_wrong']+=1
            if not row['unknown']:
                row['delta_four_way_pp']=(row['i_only']-row['comparator_only'])*100/24
                generator=random.Random(55057);keys=sorted(groups);values=[]
                for _ in range(10000):
                    sampled=[i for group in generator.choices(keys,k=len(keys)) for i in groups[group]]
                    values.append(100*sum(left[i]-right[i] for i in sampled)/len(sampled))
                values.sort()
                def quantile(p):
                    position=(len(values)-1)*p;k=int(position)
                    return values[k]+(position-k)*(values[min(k+1,len(values)-1)]-values[k])
                row['bootstrap_low_pp']=quantile(.025);row['bootstrap_high_pp']=quantile(.975)
            paired.append(row)
    complete=all(x['status']=='COMPLETE' for x in conditions) and all(x['unknown']==0 for x in paired)
    gate=complete and all(next(x for x in paired if x['seed']==s and x['comparator']=='A')['i_only']-next(x for x in paired if x['seed']==s and x['comparator']=='A')['comparator_only']>=2 for s in [19,73]) and all(x['delta_four_way_pp']>0 for x in paired if x['comparator'] in ['V','S']) and sum(x['delta_four_way_pp'] for x in paired if x['comparator']=='B0')>0
    source_profile=[]
    for number,key in enumerate(sorted(groups)):
        for seed in [19,73]:
            for comparator in ['A','V','S','B0']:
                left=four[('development_test','I',seed)];right=four[('development_test',comparator,'NA' if comparator=='B0' else seed)];ids=groups[key]
                known=all(left[i] is not None and right[i] is not None for i in ids)
                source_profile.append(dict(source='S'+str(number+1).zfill(2),seed=seed,comparator=comparator,n=len(ids),net_correct=sum(left[i]-right[i] for i in ids) if known else None))
    for filename,rows in [('condition-summary.csv',conditions),('paired-summary.csv',paired)]:
        with open(root/filename,'x',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    save(root/'score-integers.json',integer)
    save(root/'scoring-summary.json',dict(status='PILOT_DEVELOPMENT_SIGNAL' if gate else 'NO_PILOT_SUPPORT_FOR_THIS_RECIPE' if complete else 'INCOMPLETE',complete=complete,gate=gate,source_profile=source_profile,external='NOT_RUN',conditions=conditions,paired=paired))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['seal','download','extract','decode','training','scoring']);parser.add_argument('--root',required=True);parser.add_argument('--prior')
    a=parser.parse_args()
    if a.phase=='seal':seal(a.root,a.prior)
    else:globals()[a.phase](a.root)
