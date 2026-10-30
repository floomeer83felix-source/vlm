"""Explicit local Qwen057 runtime. Import performs no model/network actions."""
import hashlib
import json
import os
from pathlib import Path
import re
import time


def write(path,value):
    with open(path,'x',encoding='utf-8') as f:
        json.dump(value,f,sort_keys=True,indent=2);f.flush();os.fsync(f.fileno())


def event(path,**value):
    with open(path,'a',encoding='utf-8') as f:
        f.write(json.dumps(value,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())


def device_check():
    import subprocess
    result=subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.free,uuid','--format=csv,noheader,nounits'],text=True,timeout=15).strip().splitlines()
    if len(result)!=1:raise RuntimeError('GPU_BUSY_OR_NOT_SINGLE')
    name,free,identity=[x.strip() for x in result[0].split(',')]
    if '3090' not in name or int(free)<18*1024:raise RuntimeError('GPU_BUSY')
    return dict(name=name,free_mib=int(free),uuid=identity)


def cpu_prepare(root,model_root):
    import numpy as np
    import torch
    from transformers import AutoProcessor
    from transformers.video_utils import VideoMetadata
    root=Path(root);manifest=json.loads((root/'cache-manifest.json').read_text())
    if manifest['complete']!=102:raise RuntimeError('REAL_INPUT_INCOMPLETE')
    processor=AutoProcessor.from_pretrained(model_root,local_files_only=True,trust_remote_code=False)
    input_seal=json.loads((root/'pilot-input-seal.json').read_text()); questions=sorted({q for rows in input_seal['selected'].values() for row in rows for q in row['questions']})
    tokens={q:processor.tokenizer(q,return_tensors='pt') for q in questions}
    if any(x['input_ids'].shape[1]>128 for x in tokens.values()):raise ValueError('QUESTION_TOKEN_LIMIT')
    records={};directory=root/'prepared';directory.mkdir()
    for i,(name,row) in enumerate(manifest['records'].items()):
        array=np.load(root/'frames'/row['array'],allow_pickle=False)
        if array.shape!=(12,224,224,3) or array.dtype!=np.uint8:raise ValueError('RGB_ARRAY')
        meta=VideoMetadata(total_num_frames=row['total_num_frames'],fps=row['fps'],duration=row['duration'],width=224,height=224,frames_indices=row['indices'])
        processed=processor.video_processor(videos=[array],video_metadata=[meta],do_sample_frames=False,do_resize=False,return_tensors='pt')
        grid=processed['video_grid_thw']
        if grid.tolist()!=[[6,14,14]] or processed['pixel_values_videos'].shape!=(1176,1536):raise ValueError('PROCESSOR_TUBELET_MAP')
        data=dict(pixel_values_videos=processed['pixel_values_videos'].to(torch.bfloat16),video_grid_thw=grid)
        target=directory/(str(i)+'.pt');torch.save(data,target)
        records[name]=dict(path=target.name,rgb_sha256=row['sha256'],grid=grid.tolist(),metadata=row)
    tokenizer_root=Path(model_root)
    hashes={}
    for file in sorted(tokenizer_root.iterdir()):
        if file.is_file() and (file.suffix in ['.json','.safetensors'] or file.name in ['merges.txt','vocab.json']):
            h=hashlib.sha256()
            with open(file,'rb') as f:
                for block in iter(lambda:f.read(1024**2),b''):h.update(block)
            hashes[file.name]=h.hexdigest()
    identity=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    write(root/'runtime-input-seal.json',dict(records=records,questions=questions,model_config_sha256=identity,
        model_file_sha256=hashes,code_sha256={p.name:hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in [Path(__file__),Path(__file__).with_name('question_temporal_train_057.py')]},
        processor_grid=[6,14,14],tubelet_frames=2,spatial_tokens_per_time=49,visual_input_order='time,row-merge,column-merge,spatial-inner',
        feature_source='main visual merger output before LLM; deepstack omitted',text_source='pure text final decoder last effective token',
        question_token_limit=128,max_new_tokens=8,b0_parser='complete Yes/No optional period; case insensitive',
        actual_runtime_verified=False))
    write(root/'cpu-runtime-check.json',dict(status='PASS',videos=102,distinct_questions=len(questions),cuda_initialized=torch.cuda.is_initialized()))
    print('CPU_RUNTIME_PREPARED',len(questions),flush=True)


def gpu(root,model_root):
    import gc
    import numpy as np
    import torch
    from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
    from transformers.video_utils import VideoMetadata
    root=Path(root);start=time.monotonic();deadline=start+3420
    check=device_check();write(root/'gpu-worker-device.json',check)
    if check['uuid']!=json.loads((root/'gpu-supervisor-device.json').read_text())['uuid']:raise RuntimeError('GPU_IDENTITY_CHANGED')
    inputs=json.loads((root/'runtime-input-seal.json').read_text());plan=json.loads((root/'pilot-input-seal.json').read_text())
    counts=dict(video_feature=0,text_feature=0,b0_generate=0,root_forward=0,decoder_forward=0,visual_encoder=0)
    features=root/'features';features.mkdir();calls=root/'model-calls';calls.mkdir();b0=[];maps=dict(video={},text={})
    model=None
    def increment(name):
        def hook(*args,**kwargs):counts[name]+=1
        return hook
    def call(mode,identity,function):
        key=hashlib.sha256(json.dumps([mode,identity,inputs['model_config_sha256']],sort_keys=True).encode()).hexdigest()
        claim=calls/(key+'.started');closed=calls/(key+'.closed')
        if closed.exists():return json.loads(closed.read_text())['result']
        if claim.exists():raise RuntimeError('CONSUMED_MODEL_INPUT')
        if sum(counts[x] for x in ['video_feature','text_feature','b0_generate'])>=300 or time.monotonic()>deadline:raise TimeoutError('GPU_OR_CALL_BUDGET')
        write(claim,dict(status='STARTED',mode=mode,input_identity=identity))
        counts[mode]+=1
        try:
            result=function()
            torch.cuda.synchronize()
            if torch.cuda.max_memory_allocated()>18*1024**3:raise RuntimeError('ALLOCATED_LIMIT')
            write(closed,dict(status='CLOSED',result=result))
            return result
        except Exception as e:
            write(calls/(key+'.failed'),dict(status='FAILED',reason=str(e)));raise
    try:
        write(root/'weight-load-started.json',dict(status='STARTED',time=time.time()))
        model=Qwen3VLForConditionalGeneration.from_pretrained(model_root,local_files_only=True,trust_remote_code=False,torch_dtype=torch.bfloat16,attn_implementation='sdpa').to('cuda')
        model.eval();model.requires_grad_(False)
        model.register_forward_pre_hook(increment('root_forward'))
        model.model.language_model.register_forward_pre_hook(increment('decoder_forward'))
        model.model.visual.register_forward_pre_hook(increment('visual_encoder'))
        processor=AutoProcessor.from_pretrained(model_root,local_files_only=True,trust_remote_code=False)
        with torch.no_grad():
            for i,(name,row) in enumerate(inputs['records'].items()):
                def get_video(row=row,i=i):
                    data=torch.load(root/'prepared'/row['path'],map_location='cpu',weights_only=True)
                    kwargs={k:v.to('cuda') for k,v in data.items()}
                    result=model.get_video_features(**kwargs)
                    main=result[0]
                    if not isinstance(main,(tuple,list)) or len(main)!=1:raise ValueError('VISUAL_RETURN_CONTRACT')
                    tensor=main[0];grid=data['video_grid_thw'][0].tolist();t,h,w=grid
                    if tensor.ndim!=2 or tensor.shape[0]!=t*(h//2)*(w//2) or t!=6:raise ValueError('VISUAL_TIME_MAP')
                    pooled=tensor.reshape(t,(h//2)*(w//2),tensor.shape[-1]).mean(1).float().cpu()
                    if not torch.isfinite(pooled).all():raise ValueError('NAN_FEATURE')
                    target=features/('v'+str(i)+'.pt');torch.save(pooled,target)
                    return dict(path=target.name,shape=list(pooled.shape))
                maps['video'][name]=call('video_feature',row['rgb_sha256'],get_video)
            for i,text in enumerate(inputs['questions']):
                def get_text(text=text,i=i):
                    batch=processor.tokenizer(text,return_tensors='pt').to('cuda')
                    output=model.model(**batch,use_cache=False,return_dict=True)
                    tensor=output.last_hidden_state[0,int(batch['attention_mask'].sum())-1].float().cpu()
                    if tensor.ndim!=1 or not torch.isfinite(tensor).all():raise ValueError('TEXT_FEATURE')
                    target=features/('q'+str(i)+'.pt');torch.save(tensor,target)
                    return dict(path=target.name,shape=list(tensor.shape))
                maps['text'][text]=call('text_feature',text,get_text)
            write(root/'feature-index.json',maps)
            for index,row in enumerate(plan['selected']['development_test']):
                for vi,name in enumerate(row['videos']):
                    record=inputs['records'][name];meta=record['metadata']
                    array=np.load(root/'frames'/meta['array'],allow_pickle=False)
                    for qi,question in enumerate(row['questions']):
                        def generate(question=question,array=array,meta=meta):
                            messages=[{'role':'user','content':[{'type':'video'},{'type':'text','text':question}]}]
                            prompt=processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
                            metadata=VideoMetadata(total_num_frames=meta['total_num_frames'],fps=meta['fps'],duration=meta['duration'],frames_indices=meta['indices'],width=224,height=224)
                            data=processor(text=[prompt],videos=[array],video_metadata=[metadata],do_sample_frames=False,do_resize=False,return_tensors='pt').to('cuda')
                            data.pop('video_metadata',None)
                            output=model.generate(**data,do_sample=False,max_new_tokens=8)
                            text=processor.tokenizer.decode(output[0,data['input_ids'].shape[1]:],skip_special_tokens=True).strip()
                            valid=re.fullmatch(r'(Yes|No)\.?',text,re.I)
                            return dict(status='CLOSED' if valid else 'INVALID',prediction=int(valid[1].lower()=='yes') if valid else None,text=text)
                        result=call('b0_generate',[record['rgb_sha256'],question,{k:meta[k] for k in ['fps','indices','duration','total_num_frames']}],generate)
                        b0.append(dict(index=index,video=vi,question=qi,**result))
            write(root/'b0-sealed.json',b0)
            if any(p.grad is not None or p.requires_grad for p in model.parameters()):raise RuntimeError('MAIN_MODEL_NOT_FROZEN')
        write(root/'gpu-success.json',dict(status='CLOSED',counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),elapsed_s=time.monotonic()-start))
    finally:
        write(root/'gpu-counts-final.json',dict(counts=counts,peak_allocated_bytes=torch.cuda.max_memory_allocated(),elapsed_s=time.monotonic()-start))
        del model;gc.collect();torch.cuda.empty_cache();torch.cuda.synchronize()


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['cpu_prepare','gpu']);p.add_argument('--root',required=True);p.add_argument('--model',required=True)
    a=p.parse_args();globals()[a.phase](a.root,a.model)
