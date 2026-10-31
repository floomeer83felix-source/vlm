"""060 explicit offline media/CPU processor and single frozen GPU roles.

Import does not load weights, initialize CUDA, access task files or network.
"""
import argparse
from collections import Counter, defaultdict
import gc
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import time
import zipfile


def core():
    spec=importlib.util.spec_from_file_location('pool060',Path(__file__).with_name('temporal_pool_transfer_060.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def media(root):
    c=core();root=Path(root);prior=Path(c.read(root/'prior-assets.json')['prior057'])
    plan=c.read(root/'data-bindings.json');names=[n for rows in plan['pools'].values() for r in rows for n in r['videos']]
    if len(names)!=366 or len(set(names))!=366:raise ValueError('MEMBERS366')
    oldmedia={r['requested']:r for r in c.read(prior/'media-manifest.json')};oldcache=c.read(prior/'cache-manifest.json')['records']
    oldruntime=c.read(prior/'runtime-input-seal.json')['records']
    if set(oldmedia)!=set(oldcache) or set(oldcache)!=set(oldruntime):raise ValueError('OLD102_BINDING')
    for name,row in oldcache.items():
        if row!=oldruntime[name]['metadata'] or row['input_sha256']!=oldmedia[name]['sha256'] or row['sha256']!=oldruntime[name]['rgb_sha256'] or row['status']!='CLOSED':raise ValueError('OLD_RGB_MEDIA_BINDING')
        if c.digest(prior/'frames'/row['array'])!=row['sha256']:raise ValueError('OLD_RGB_FILE_IDENTITY')
    archive=prior/'event_sequence_zip.body';expected=c.read(prior/'media-plan.json')
    c.save(root/'zip-sha-started.json',dict(status='STARTED',bytes=archive.stat().st_size))
    if archive.stat().st_size!=2783546023 or c.digest(archive)!=expected['publisher_content_sha256']:raise ValueError('OLD_ZIP_CONTENT_SHA')
    c.save(root/'zip-sha-closed.json',dict(status='CLOSED',sha256=expected['publisher_content_sha256'],bytes=archive.stat().st_size))
    newnames=[n for n in names if n not in oldmedia]
    if len(newnames)!=264:raise ValueError('NEW264')
    helper=c.module('question_temporal_data_056');destination=root/'media';destination.mkdir()
    with zipfile.ZipFile(archive) as f:
        infos=f.infolist();bybase=defaultdict(list)
        for x in infos:bybase[Path(x.filename).name].append(x.filename)
        if any(len(bybase[n])!=1 for n in names):raise ValueError('MEMBER_MAP366')
        selected=[bybase[n][0] for n in newnames]
    # Existing056 routine validates the entire directory and CRC/sizes, once.
    entries=helper.extract_selected(archive,selected,destination)
    for name,r in zip(newnames,entries):r['requested']=name
    c.save(root/'media-manifest.json',entries)
    print('MEDIA_CRC_CLOSED',len(entries),sum(r['bytes'] for r in entries),flush=True)


def decode(root):
    import av
    c=core();root=Path(root);prior=Path(c.read(root/'prior-assets.json')['prior057'])
    helper=c.module('question_temporal_data_056');directory=root/'frames';directory.mkdir()
    records={};known={};old=c.read(prior/'cache-manifest.json')['records']
    for name,r in old.items():
        item=dict(r,array_path=str(prior/'frames'/r['array']),origin='OLD_RGB');records[name]=item;known[r['input_sha256']]=item
    budget=[0];start=time.monotonic();deadline=start+1740;newdecoded=0;aliases=0
    for entry in c.read(root/'media-manifest.json'):
        name=entry['requested']
        if entry['sha256'] in known:
            records[name]=dict(known[entry['sha256']],origin='MEDIA_ALIAS');aliases+=1;continue
        c.event(root/'decode-ledger.jsonl',event='STARTED',member=name,input_sha256=entry['sha256'])
        try:
            r=helper.prepare_cache(root/'media'/entry['path'],directory,budget,deadline)
            with av.open(str(root/'media'/entry['path'])) as f:
                stream=f.streams.video[0];r['fps']=float(stream.average_rate);r['total_num_frames']=stream.frames;r['duration']=float(stream.duration*stream.time_base)
                base=float(stream.start_time or 0)*float(stream.time_base)
                if max(abs(stamp-base-index/r['fps']) for stamp,index in zip(r['timestamps'],r['indices']))>1/r['fps']:raise ValueError('FRAME_INDEX_CLOCK_NOT_CFR')
            r.update(array_path=str(directory/r['array']),origin='NEW_RGB');records[name]=r;known[entry['sha256']]=r;newdecoded+=1
            c.event(root/'decode-ledger.jsonl',event='CLOSED',member=name,frames_total=budget[0])
        except Exception as e:
            c.event(root/'decode-ledger.jsonl',event='FAILED',member=name,reason=str(e));raise
        if newdecoded%32==0:print('DECODE',newdecoded,'frames',budget[0],flush=True)
    if len(records)!=366 or any(r['status']!='CLOSED' for r in records.values()):raise ValueError('RGB_INPUT_INCOMPLETE')
    sources={n:row['source'] for rows in c.read(root/'data-bindings.json')['pools'].values() for row in rows for n in row['videos']}
    mediahash={r['requested']:r['sha256'] for r in c.read(prior/'media-manifest.json')+c.read(root/'media-manifest.json')}
    collision=[];duplicates={}
    for kind,identities in [('media',mediahash),('rgb',{n:r['sha256'] for n,r in records.items()})]:
        groups=defaultdict(list)
        for name,identity in identities.items():groups[identity].append(name)
        collision.extend(dict(kind=kind,members=members) for members in groups.values() if len({sources[n] for n in members})>1)
        duplicates[kind]=dict(duplicate_groups=sum(len(v)>1 for v in groups.values()),duplicate_slots=sum(len(v)-1 for v in groups.values()))
    degeneracy={}
    for source in ('Breakfast','50Salads'):
        rows=[r for entries in c.read(root/'data-bindings.json')['pools'].values() for r in entries if r['source']==source]
        degeneracy[source]=dict(n=len(rows),same_media_pair=sum(mediahash[r['videos'][0]]==mediahash[r['videos'][1]] for r in rows),same_rgb_pair=sum(records[r['videos'][0]]['sha256']==records[r['videos'][1]]['sha256'] for r in rows))
    c.save(root/'cache-manifest.json',dict(records=records,complete=366,new_decoded=newdecoded,media_aliases=aliases,decoded_frames=budget[0],outer_s=time.monotonic()-start))
    c.save(root/'collision-check.json',dict(status='SOURCE_INPUT_COLLISION/UNKNOWN' if collision else 'NO_EXACT_CROSS_SOURCE_COLLISION',collisions=collision,duplicates=duplicates,degeneracy=degeneracy,not_proven='No transcode/crop/physical-source independence guarantee'))
    if collision:raise RuntimeError('SOURCE_INPUT_COLLISION/UNKNOWN')
    print('RGB_CLOSED',newdecoded,budget[0],'NO_EXACT_CROSS_SOURCE_COLLISION',flush=True)


def processor(root,model_root):
    import numpy as np
    import torch
    from transformers import AutoProcessor
    from transformers.video_utils import VideoMetadata
    c=core();root=Path(root);prior=Path(c.read(root/'prior-assets.json')['prior057'])
    if torch.cuda.is_initialized():raise ValueError('CPU_PROCESSOR_CUDA')
    old=c.read(prior/'runtime-input-seal.json');oldindex=c.read(prior/'feature-index.json')
    hashes={}
    for p in sorted(Path(model_root).iterdir()):
        if p.is_file() and (p.suffix in ('.json','.safetensors') or p.name in ('merges.txt','vocab.json')):hashes[p.name]=c.digest(p)
    if hashes!=old['model_file_sha256']:raise ValueError('MODEL_PROCESSOR_TOKENIZER_IDENTITY')
    identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    if identity!=old['model_config_sha256']:raise ValueError('MODEL_IDENTITY')
    proc=AutoProcessor.from_pretrained(model_root,local_files_only=True,trust_remote_code=False)
    cache=c.read(root/'cache-manifest.json')['records'];questions=sorted({q for rows in c.read(root/'data-bindings.json')['pools'].values() for r in rows for q in r['questions']})
    if not set(oldindex['text'])<=set(questions):raise ValueError('OLD_TEXT_SET_NOT_SUBSET')
    newquestions=[q for q in questions if q not in oldindex['text']]
    if len(newquestions)>312:raise ValueError('NEW_TEXT_CAP')
    for q in questions:
        batch=proc.tokenizer(q,return_tensors='pt')
        if int(batch['attention_mask'].sum())>128:raise ValueError('TEXT_TOKEN_CAP')
    maps={k:{key:dict(path=str(prior/'features'/r['path']),shape=r['shape'],origin='OLD') for key,r in oldindex[k].items()} for k in ('video','text')}
    byrgb={cache[n]['sha256']:n for n in oldindex['video']};records={};prepared=root/'prepared';prepared.mkdir();aliases={}
    for name,row in cache.items():
        if name in oldindex['video']:continue
        rgb=row['sha256']
        if rgb in byrgb:
            aliases[name]=byrgb[rgb];continue
        array=np.load(row['array_path'],allow_pickle=False)
        if array.shape!=(12,224,224,3) or array.dtype!=np.uint8:raise ValueError('RGB_ARRAY')
        meta=VideoMetadata(total_num_frames=row['total_num_frames'],fps=row['fps'],duration=row['duration'],width=224,height=224,frames_indices=row['indices'])
        processed=proc.video_processor(videos=[array],video_metadata=[meta],do_sample_frames=False,do_resize=False,return_tensors='pt')
        if processed['video_grid_thw'].tolist()!=[[6,14,14]] or processed['pixel_values_videos'].shape!=(1176,1536):raise ValueError('PROCESSOR_TUBELET_MAP')
        path=prepared/(str(len(records))+'.pt')
        with open(path,'xb') as f:torch.save(dict(pixel_values_videos=processed['pixel_values_videos'].to(torch.bfloat16),video_grid_thw=processed['video_grid_thw']),f)
        records[name]=dict(path=str(path),rgb_sha256=rgb,metadata=row);byrgb[rgb]=name
    # The original057 installed-source ordering was validated; local code hashes
    # are bound with the unchanged weights/config/tokenizer and processor grid.
    import inspect
    from transformers.models.qwen3_vl import modeling_qwen3_vl
    runtime_sources={str(Path(inspect.getfile(obj)).name):c.digest(inspect.getfile(obj)) for obj in (modeling_qwen3_vl, type(proc.video_processor))}
    c.save(root/'runtime-input-seal.json',dict(records=records,video_aliases=aliases,questions=newquestions,all_questions=questions,old_feature_index=maps,model_root=str(model_root),model_config_sha256=identity,model_file_sha256=hashes,installed_sources=runtime_sources,feature_source=old['feature_source'],text_source=old['text_source'],processor_grid=[6,14,14],pixels_shape=[1176,1536],tubelet_frames=2,spatial_tokens_per_time=49,visual_input_order=old['visual_input_order'],text_token_limit=128,b0_max_new_tokens=8))
    c.save(root/'cpu-runtime-check.json',dict(status='PASS',new_unique_video=len(records),video_aliases=len(aliases),new_questions=len(newquestions),all_questions=len(questions),old_videos=102,old_questions=54,weights_loaded=False,cuda_initialized=torch.cuda.is_initialized()))
    print('PROCESSOR_PASS',len(records),len(newquestions),'grid6x14x14 pixels1176x1536',flush=True)


def device_check():
    import subprocess
    result=subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.free,uuid','--format=csv,noheader,nounits'],text=True,timeout=15).strip().splitlines()
    if len(result)!=1:raise RuntimeError('GPU_BUSY_OR_NOT_SINGLE')
    name,free,identity=[x.strip() for x in result[0].split(',')]
    if '3090' not in name or int(free)<18*1024:raise RuntimeError('GPU_BUSY')
    return dict(name=name,free_mib=int(free),uuid=identity)


def gpu(root,model_root):
    import numpy as np
    import torch
    from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
    from transformers.video_utils import VideoMetadata
    c=core();root=Path(root);c.check_frozen(root);start=time.monotonic();deadline=start+1630
    check=device_check();c.save(root/'gpu-worker-device.json',check)
    if check['uuid']!=c.read(root/'gpu-supervisor-device.json')['uuid']:raise RuntimeError('GPU_CHANGED')
    inputs=c.read(root/'runtime-input-seal.json');cache=c.read(root/'cache-manifest.json')['records']
    observations=c.read(root/'source_holdout50-observations.json');features=root/'features';features.mkdir();calls=root/'model-calls';calls.mkdir()
    maps=inputs['old_feature_index'];counts=dict(video_feature=0,text_feature=0,b0_generate=0,root_forward=0,decoder_forward=0,decoder_layer_forward=0,visual_encoder=0)
    model=None;limits=dict(video_feature=264,text_feature=312,b0_generate=200);b0=[]
    def hook(name):
        def increment(*args,**kwargs):counts[name]+=1
        return increment
    def call(mode,identity,function):
        key=hashlib.sha256(json.dumps([mode,identity,inputs['model_config_sha256']],sort_keys=True).encode()).hexdigest();claim=calls/(key+'.started');closed=calls/(key+'.closed')
        if closed.exists():return c.read(closed)['result']
        if claim.exists():raise RuntimeError('CONSUMED_INPUT_NO_RETRY')
        if counts[mode]>=limits[mode] or sum(counts[k] for k in limits)>=776 or time.monotonic()>deadline:raise TimeoutError('GPU_CALL_OR_TIME_LIMIT')
        c.save(claim,dict(status='STARTED',mode=mode,input_identity=identity,at_unix=time.time()));counts[mode]+=1
        try:
            result=function();torch.cuda.synchronize()
            if torch.cuda.max_memory_allocated()>18*1024**3:raise RuntimeError('ALLOCATED_LIMIT')
            c.save(closed,dict(status='CLOSED',result=result));return result
        except Exception as e:
            c.save(calls/(key+'.failed'),dict(status='FAILED',reason=str(e)));raise
    try:
        c.save(root/'weight-load-started.json',dict(status='STARTED',at_unix=time.time()))
        model=Qwen3VLForConditionalGeneration.from_pretrained(model_root,local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to('cuda')
        model.eval();model.requires_grad_(False)
        model.register_forward_pre_hook(hook('root_forward'));model.model.language_model.register_forward_pre_hook(hook('decoder_forward'));model.model.visual.register_forward_pre_hook(hook('visual_encoder'))
        for layer in model.model.language_model.layers:layer.register_forward_pre_hook(hook('decoder_layer_forward'))
        proc=AutoProcessor.from_pretrained(model_root,local_files_only=True,trust_remote_code=False)
        with torch.no_grad():
            for i,(name,row) in enumerate(inputs['records'].items()):
                def video(row=row,i=i):
                    data=torch.load(row['path'],map_location='cpu',weights_only=True);out=model.get_video_features(**{k:v.to('cuda') for k,v in data.items()})
                    main=out[0]
                    if not isinstance(main,(tuple,list)) or len(main)!=1:raise ValueError('VISUAL_RETURN')
                    tensor=main[0];t,h,w=data['video_grid_thw'][0].tolist()
                    if (t,h,w)!=(6,14,14) or tensor.shape!=(294,2560):raise ValueError('VISUAL_TIME_AXIS')
                    pooled=tensor.reshape(6,49,2560).mean(1).float().cpu()
                    if not torch.isfinite(pooled).all():raise ValueError('NONFINITE_V')
                    path=features/f'v{i}.pt'
                    with open(path,'xb') as f:torch.save(pooled,f)
                    return dict(path=str(path),shape=[6,2560],origin='NEW')
                maps['video'][name]=call('video_feature',row['rgb_sha256'],video)
                if (i+1)%32==0:print('V_FEATURE',i+1,flush=True)
            for name,source in inputs['video_aliases'].items():maps['video'][name]=dict(maps['video'][source],origin='ALIAS')
            for i,q in enumerate(inputs['questions']):
                def text(q=q,i=i):
                    batch=proc.tokenizer(q,return_tensors='pt').to('cuda');out=model.model(**batch,use_cache=False,return_dict=True)
                    tensor=out.last_hidden_state[0,int(batch['attention_mask'].sum())-1].float().cpu()
                    if tensor.shape!=(2560,) or not torch.isfinite(tensor).all():raise ValueError('NONFINITE_Q')
                    path=features/f'q{i}.pt'
                    with open(path,'xb') as f:torch.save(tensor,f)
                    return dict(path=str(path),shape=[2560],origin='NEW')
                maps['text'][q]=call('text_feature',q,text)
                if (i+1)%48==0:print('Q_FEATURE',i+1,flush=True)
            if len(maps['video'])!=366 or set(maps['text'])!=set(inputs['all_questions']):raise ValueError('COMPLETE_FEATURE_SLOTS')
            c.save(root/'feature-index.json',maps)
            for row in observations:
                for vi,name in enumerate(row['videos']):
                    meta=cache[name];array=np.load(meta['array_path'],allow_pickle=False)
                    for qi,q in enumerate(row['questions']):
                        def generate(q=q,meta=meta,array=array):
                            messages=[dict(role='user',content=[dict(type='video'),dict(type='text',text=q)])]
                            prompt=proc.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
                            metadata=VideoMetadata(total_num_frames=meta['total_num_frames'],fps=meta['fps'],duration=meta['duration'],frames_indices=meta['indices'],width=224,height=224)
                            data=proc(text=[prompt],videos=[array],video_metadata=[metadata],do_sample_frames=False,do_resize=False,return_tensors='pt').to('cuda');data.pop('video_metadata',None)
                            out=model.generate(**data,do_sample=False,max_new_tokens=8)
                            text=proc.tokenizer.decode(out[0,data['input_ids'].shape[1]:],skip_special_tokens=True).strip();valid=re.fullmatch(r'(Yes|No)\.?',text,re.I)
                            return dict(status='CLOSED' if valid else 'INVALID',prediction=int(valid[1].lower()=='yes') if valid else None,text=text)
                        identity=[meta['sha256'],q,{k:meta[k] for k in ('fps','indices','duration','total_num_frames')}]
                        result=call('b0_generate',identity,generate)
                        b0.append(dict(method='B0',seed='NA',split='source_holdout50',index=row['index'],video=vi,question=qi,origin='NEW_B0',**result))
                if (row['index']+1)%10==0:print('B0_INSTANCES',row['index']+1,flush=True)
            if len(b0)!=200 or any(p.requires_grad or p.grad is not None for p in model.parameters()):raise ValueError('FROZEN_MODEL_OR_B0_COUNT')
            c.save(root/'b0-sealed.json',b0)
        c.save(root/'gpu-success.json',dict(status='CLOSED',counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),elapsed_s=time.monotonic()-start,loads=1,main_backward=0,main_optimizer=0))
    finally:
        c.save(root/'gpu-counts-final.json',dict(counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),elapsed_s=time.monotonic()-start))
        del model;gc.collect()
        if torch.cuda.is_initialized():torch.cuda.empty_cache();torch.cuda.synchronize()


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=('media','decode','processor','gpu'));p.add_argument('--root',required=True);p.add_argument('--model')
    a=p.parse_args()
    if a.phase in ('processor','gpu'):globals()[a.phase](a.root,a.model)
    else:globals()[a.phase](a.root)
