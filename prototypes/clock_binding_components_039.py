"""039 owned component contrast; fresh run only. ML is confined to children.

No original research-data, historical execution, or training entry point.
The inherited helpers are pure serialization/policy/OS supervision utilities.
"""
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time

import clock_binding_probe_038 as base

need,sha,digest,packed,load,write,chain = base.need,base.sha,base.digest,base.packed,base.load,base.write,base.chain
MIB,GIB=1024**2,1024**3
SYSTEM='You are a helpful assistant.'
POSITIONS=((0,2),(0,4),(1,5),(3,5))
CLOCKS=((0,1,4,5,8,9,12,13,16,17,20,21),(0,1,2,3,6,7,14,15,18,19,20,21),
        (60,61,64,65,68,69,72,73,76,77,80,81))
TASKS=('NG','NR','SG','SR','OG')
PROMPTS={
 'NG':'Using the timestamps attached to the red square and the blue square in the provided video, what is their absolute time difference in seconds? Output only a non-negative integer.',
 'NR':'Read the timestamp attached to the red square and the timestamp attached to the blue square in the provided video. Output only the red timestamp first and the blue timestamp second, each in seconds with one decimal place, separated by a comma and no spaces.',
 'SG':'The image contains six panels, each with a square and a printed timestamp in seconds. What is the absolute time difference between the printed timestamp for the red square and the printed timestamp for the blue square? Output only a non-negative integer.',
 'SR':'The image contains six panels, each with a square and a printed timestamp in seconds. Read the printed timestamp for the red square and the printed timestamp for the blue square. Output only the red timestamp first and the blue timestamp second, each in seconds with one decimal place, separated by a comma and no spaces.',
 'OG':'The red square has timestamp {red:.1f} seconds. The blue square has timestamp {blue:.1f} seconds. What is their absolute time difference in seconds? Output only a non-negative integer.'}
FONT={
 '0':'01110/10001/10011/10101/11001/10001/01110',
 '1':'00100/01100/00100/00100/00100/00100/01110',
 '2':'01110/10001/00001/00010/00100/01000/11111',
 '3':'11110/00001/00001/01110/00001/00001/11110',
 '4':'00010/00110/01010/10010/11111/00010/00010',
 '5':'11111/10000/10000/11110/00001/00001/11110',
 '6':'01110/10000/10000/11110/10001/10001/01110',
 '7':'11111/00001/00010/00100/01000/01000/01000',
 '8':'01110/10001/10001/01110/10001/10001/01110',
 '9':'01110/10001/10001/01111/00001/00001/01110',
 '.':'00000/00000/00000/00000/00000/00100/00100'}
VISUAL_KEYS=('pixel_values','image_grid_thw','pixel_values_videos','video_grid_thw')


def spec():
    return dict(id='039_COMPONENTS_1',positions=POSITIONS,clocks=CLOCKS,totals=(22,22,82),fps=1,
                shape=(12,192,288,3),colors=((16,16,16),(96,96,96),(240,32,32),(32,64,240)),
                square=(96,192,48,144),image_shape=(384,864,3),font=FONT,font_origin=(16,8),scale=4,advance=24,
                prompts=PROMPTS,system=SYSTEM,tasks=TASKS,seed=19,max_new_tokens=16,dtype='bfloat16',attention='sdpa')


def queue():
    output=[]
    for w in range(8):
        original=[(task,g) for task in TASKS for g in range(3)];k=(7*w)%15
        for task,g in original[k:]+original[:k]:output.append(dict(slot=len(output),world=w,clock=g,task=task))
    return output


def ticks(g):
    return [(CLOCKS[g][k]+CLOCKS[g][k+1])*5 for k in range(0,12,2)]


def roles(w,g):
    i,j=POSITIONS[w//2];a,b=ticks(g)[i],ticks(g)[j]
    return (a,b) if w%2==0 else (b,a)


def truth(w,g,task):
    a,b=roles(w,g)
    return [a,b] if task in ('NR','SR') else abs(a-b)//10


def frames(w):
    i,j=POSITIONS[w//2];raw=bytearray();bg=bytes((16,16,16))
    for n in range(12):
        k=n//2;color=(96,96,96)
        if k==i:color=(240,32,32) if w%2==0 else (32,64,240)
        if k==j:color=(32,64,240) if w%2==0 else (240,32,32)
        fg=bytes(color)
        for y in range(192):raw.extend(bg*96+fg*96+bg*96 if 48<=y<144 else bg*288)
    return bytes(raw)


def montage(w,g,label=True):
    raw=frames(w);image=bytearray(384*864*3);stride=288*3;unit=192*stride
    for k in range(6):
        top,left=(k//3)*192,(k%3)*288
        for y in range(192):
            begin=((top+y)*864+left)*3
            image[begin:begin+stride]=raw[2*k*unit+y*stride:2*k*unit+(y+1)*stride]
        if label:
            text='%.1f'%(ticks(g)[k]/10)
            for n,ch in enumerate(text):
                for gy,line in enumerate(FONT[ch].split('/')):
                    for gx,bit in enumerate(line):
                        if bit=='1':
                            for dy in range(4):
                                yy=top+8+gy*4+dy;xx=left+16+n*24+gx*4
                                begin=(yy*864+xx)*3;image[begin:begin+12]=bytes((240,240,240))*4
    return bytes(image)


def erase_label_boxes(raw):
    image=bytearray(raw)
    for k in range(6):
        top,left=(k//3)*192,(k%3)*288
        for y in range(top+8,top+36):
            a=(y*864+left+16)*3;image[a:a+96*3]=bytes((16,16,16))*96
    return bytes(image)


def parse(task,raw):
    raw=raw.strip()
    if task not in ('NR','SR'):return int(raw) if re.fullmatch(r'[0-9]{1,3}',raw) else None
    match=re.fullmatch(r'([0-9]{1,3}\.[0-9]),([0-9]{1,3}\.[0-9])',raw)
    return [int(s.replace('.','')) for s in match.groups()] if match else None


def code_hash():
    folder=Path(__file__).parent
    return digest({name:sha((folder/name).read_bytes()) for name in
                   ('clock_binding_components_039.py','test_clock_binding_components_039.py',
                    'clock_binding_probe_038.py','development_pilot_030.py')})


def append(root,event,**fields):
    path=Path(root)/'039-ledger.jsonl';rows=chain(path.read_bytes()) if path.exists() else []
    row=dict(seq=len(rows),prev=rows[-1]['hash'] if rows else '0'*64,event=event,at=time.time(),**fields)
    row['hash']=digest(row)
    with open(path,'ab') as f:f.write(packed(row)+b'\n');f.flush();os.fsync(f.fileno())


def exact_read(path,cap,purpose):
    before=path.stat();need(before.st_size<=cap and not before.st_file_attributes & 0x400,'EXTERNAL_METADATA')
    with open(path,'rb') as f:raw=f.read(cap+1);after=os.fstat(f.fileno())
    need(len(raw)==before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns,'EXTERNAL_CHANGED')
    return raw,dict(purpose=purpose,size=len(raw),sha256=sha(raw),stat=[before.st_dev,before.st_ino,before.st_mtime_ns])


def initialize(root,old,start):
    root=Path(root);old=Path(old)
    need(root.name=='integration_039' and old.name=='integration_038' and root.parent==old.parent,'EXACT_ROOT')
    need(not root.exists() and time.time()<start+1800,'OLD_ROOT_OR_DEADLINE')
    free=shutil.disk_usage(root.parent).free;checked=time.time();required=64*MIB+2*GIB
    need(free>=required,'DISK_HEADROOM')  # Before the FIRST new private output.
    root.mkdir()
    with open(root/'run.lock','xb') as f:f.write(b'039-single-run-no-resume\n')
    append(root,'RUN',purpose='REAL_039',start=start,deadline=start+1800,disk_free=free,disk_required=required,disk_checked_at=checked)
    for folder in ('runtime','inputs','gpu','score','cache','cache/temp','cache/hf','cache/torch','cache/xdg'):(root/folder).mkdir()
    payload={};reads=[]
    for name,cap in (('runtime/config.json',MIB),('runtime/external-reads.json',MIB),('038-ledger.jsonl',2*MIB),('runtime/final-summary.json',MIB)):
        raw,record=exact_read(old/name,cap,'038/'+name);reads.append(record);payload[name]=raw
    oldrows=chain(payload['038-ledger.jsonl']);summary=json.loads(payload['runtime/final-summary.json'])
    need(oldrows[0].get('purpose')=='REAL_038' and oldrows[-1]['event']=='RUN_STOPPED','OLD_RUN_OPEN')
    begun=[r for r in oldrows if r['event']=='STARTED'];ended=[r for r in oldrows if r['event']=='TERMINAL']
    need(len(begun)==len(ended)==48 and {r['slot'] for r in begun}=={r['slot'] for r in ended}==set(range(48)), 'OLD_QUEUE')
    need(len([r for r in oldrows if r['event']=='MODEL_EXIT' and r['job_active']==0])==1
         and any(r['event']=='QUEUE_CLOSED' for r in oldrows)
         and all(r['job_active']==0 and r['exit_code']==0 for r in summary['phases']), 'OLD_EXIT')
    cfg=json.loads(payload['runtime/config.json']);prior=json.loads(payload['runtime/external-reads.json'])
    cfg={k:cfg[k] for k in ('model','runtime','device','video_token_id')}
    for name in ('config.json','preprocessor_config.json'):
        raw,record=exact_read(Path(cfg['model'])/name,MIB,'Qwen/'+name)
        evidence=[r for r in prior if r['name']=='qwen-'+name]
        need(len(evidence)==1 and evidence[0]['size']==len(raw) and evidence[0]['sha256']==sha(raw),'MODEL_CONFIG_CHANGED')
        reads.append(record)
        if name=='config.json':
            value=json.loads(raw);need(value['model_type']=='qwen3_vl','MODEL_TYPE')
            cfg['image_token_id']=value['image_token_id'];need(cfg['video_token_id']==value['video_token_id'],'VIDEO_TOKEN_CHANGED')
    for name,rel in (('processing_qwen3_vl.py','transformers/models/qwen3_vl/processing_qwen3_vl.py'),
                     ('video_processing_qwen3_vl.py','transformers/models/qwen3_vl/video_processing_qwen3_vl.py'),
                     ('video_utils.py','transformers/video_utils.py')):
        raw,record=exact_read(Path(cfg['runtime']['site'])/rel,MIB,'runtime/'+name);reads.append(record)
        with open(root/'runtime'/name,'xb') as f:f.write(raw)
    cfg['model_configs']=reads[4:6]
    write(root,'runtime/config.json',cfg);write(root,'runtime/external-reads.json',reads)
    write(root,'inputs/spec.json',spec());write(root,'inputs/queue.json',queue())
    write(root,'score/truth.json',[dict(slot=s['slot'],truth=truth(s['world'],s['clock'],s['task'])) for s in queue()])
    append(root,'INITIALIZED',research_bytes=sum(r['size'] for r in reads),old_stop=oldrows[-1]['hash'],
           spec_hash=digest(spec()),queue_hash=digest(queue()),config_hash=digest(cfg))
    print(json.dumps(dict(status='INITIALIZED',research_opens=len(reads),research_bytes=sum(r['size'] for r in reads),
                          disk_free=free,disk_required=required,disk_checked_at=checked,start=start)))


def tensor_binding(values,torch):
    parts={key:base.tensor_signature(value,torch,True) for key,value in sorted(values.items())}
    return dict(full=digest(parts),parts=parts,visual=digest({k:v for k,v in parts.items() if k in VISUAL_KEYS}),
                text=digest({k:v for k,v in parts.items() if k not in VISUAL_KEYS}))


def make_input(slot,processor,np,VideoMetadata):
    w,g,task=slot['world'],slot['clock'],slot['task'];question=PROMPTS[task]
    if task=='OG':
        a,b=roles(w,g);question=question.format(red=a/10,blue=b/10)
    content=[]
    if task in ('NG','NR'):content.append(dict(type='video',video='owned-memory-only'))
    if task in ('SG','SR'):content.append(dict(type='image',image='owned-memory-only'))
    content.append(dict(type='text',text=question))
    text=processor.apply_chat_template([dict(role='system',content=SYSTEM),dict(role='user',content=content)],
                                       tokenize=False,add_generation_prompt=True)
    raw=None
    if task in ('NG','NR'):
        raw=frames(w);array=np.frombuffer(raw,dtype=np.uint8).reshape(12,192,288,3).copy()
        meta=VideoMetadata(total_num_frames=(22,22,82)[g],fps=1.,width=288,height=192,
                           duration=float((22,22,82)[g]),frames_indices=list(CLOCKS[g]))
        values=processor(text=[text],videos=[array],video_metadata=[meta],do_sample_frames=False,do_resize=False,return_tensors='pt')
    elif task in ('SG','SR'):
        raw=montage(w,g);array=np.frombuffer(raw,dtype=np.uint8).reshape(384,864,3).copy()
        values=processor(text=[text],images=[array],do_resize=False,return_tensors='pt')
    else:values=processor(text=[text],return_tensors='pt')
    return values,raw,question


def check_input(slot,values,raw,question,processor,torch,cfg):
    task,g=slot['task'],slot['clock'];ids=values['input_ids']
    nv=int((ids==cfg['video_token_id']).sum());ni=int((ids==cfg['image_token_id']).sum())
    n=int(ids.shape[-1]);need(n<=2048,'INPUT_LENGTH')
    decoded=processor.tokenizer.decode(ids[0],skip_special_tokens=False)
    need(decoded.count(question)==1,'PROMPT_MISMATCH')
    found=[int(x.replace('.','')) for x in re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded)]
    if task in ('NG','NR'):
        need(nv==324 and ni==0 and values['video_grid_thw'].tolist()==[[6,12,18]],'VIDEO_GRID_TOKENS')
        need(found==ticks(g),'NATIVE_TIMECODES')
    elif task in ('SG','SR'):
        need(ni==324 and nv==0 and values['image_grid_thw'].tolist()==[[1,24,54]],'IMAGE_GRID_TOKENS')
        need(not found and question==PROMPTS[task],'IMAGE_TEXT_LEAK')
        need(erase_label_boxes(raw)==erase_label_boxes(montage(slot['world'],g,False)),'OUTSIDE_GLYPH_CHANGED')
    else:need(nv==ni==0 and not any(k in values for k in VISUAL_KEYS),'OG_VISUAL_LEAK')
    normalized=re.sub(r'<[0-9]+\.[0-9] seconds>','<CLOCK>',decoded)
    return dict(**tensor_binding(values,torch),tokens=n,video_tokens=nv,image_tokens=ni,
                native_ticks=found,raw_rgb=sha(raw) if raw else None,normalized_text=sha(normalized.encode()),
                image_outside_labels=sha(erase_label_boxes(raw)) if task in ('SG','SR') else None)


def snapshots(root,cfg):
    return dict(code_hash=code_hash(),spec_hash=digest(load(root,'inputs/spec.json')),
                queue_hash=digest(load(root,'inputs/queue.json')),config_hash=digest(cfg))


def exposure(root,attempt):
    cfg=load(root,'runtime/config.json');base.child_policy(root,cfg['model'],'exposure')
    result=dict(status='HOLD_INPUT',**snapshots(root,cfg));start=time.monotonic();stage='IMPORT'
    try:
        import numpy as np
        import torch
        import transformers
        from transformers import AutoProcessor
        from transformers.video_utils import VideoMetadata
        torch.set_num_threads(2);need(not torch.cuda.is_initialized(),'CPU_CUDA')
        stage='PROCESSOR';processor=AutoProcessor.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False)
        source_path=Path(sys.modules[type(processor.image_processor).__module__].__file__)
        if attempt==1:
            raw,record=exact_read(source_path,MIB,'runtime/actual-image-processor-class')
            reads=load(root,'runtime/external-reads.json');need(sum(r['size'] for r in reads)+len(raw)<=12*MIB,'RESEARCH_BUDGET')
            with open(Path(root)/'runtime/image-processor-source.py','xb') as f:f.write(raw)
            write(root,'runtime/research-reads-complete.json',reads+[record])
        stage='INPUTS';bindings={};native={};native_text={};images={};outside={}
        for slot in queue():
            values,raw,question=make_input(slot,processor,np,VideoMetadata)
            item=check_input(slot,values,raw,question,processor,torch,cfg);w,g,task=slot['world'],slot['clock'],slot['task']
            if task in ('NG','NR'):
                prior=native.setdefault(w,[])
                need(all(x['visual']==item['visual'] and x['raw_rgb']==item['raw_rgb'] for x in prior),'NATIVE_VISUAL_CHANGED')
                prior.append(item);text_prior=native_text.setdefault((w,task),[])
                need(all(x['normalized_text']==item['normalized_text'] and x['text']!=item['text'] for x in text_prior),'NATIVE_TEXT_CLOCK')
                text_prior.append(item)
            if task in ('SG','SR'):
                prior=images.setdefault((w,g),[])
                need(all(x['visual']==item['visual'] and x['raw_rgb']==item['raw_rgb'] for x in prior),'SG_SR_IMAGE_CHANGED')
                prior.append(item);prior_out=outside.setdefault(w,item['image_outside_labels'])
                need(prior_out==item['image_outside_labels'],'NONLABEL_CLOCK_PIXELS')
            bindings[str(slot['slot'])]=item;del values,raw
        need(len(bindings)==120 and all(len(x)==6 for x in native.values()) and len(native)==8
             and len(images)==24 and all(len(x)==2 for x in images.values()),'INPUTS_INCOMPLETE')
        need(not torch.cuda.is_initialized(),'CPU_CUDA')
        result.update(status='PASS',bindings=bindings,cuda_initialized=False,
                      versions=dict(torch=torch.__version__,numpy=np.__version__,transformers=transformers.__version__),
                      processor_class=type(processor).__name__,image_processor_class=type(processor.image_processor).__name__)
    except Exception as error:
        import traceback
        result.update(stage=stage,error=type(error).__name__,message=str(error)[:1500],stack=traceback.format_exc()[-7000:])
    result['seconds']=time.monotonic()-start;write(root,'inputs/exposure-%d.json'%attempt,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','message','stack')}))


def resource(root):
    import subprocess
    from development_pilot_030 import parse_resource_sample_036
    cfg=load(root,'runtime/config.json')
    raw=subprocess.run(['nvidia-smi','-q','-x','-i','0'],capture_output=True,timeout=8,creationflags=0x08000000)
    need(raw.returncode==0,'QUERY_FAILED')
    sample=parse_resource_sample_036(raw.stdout.decode(),cfg['device'])
    write(root,'runtime/resource.json',sample)
    print(json.dumps(dict(status='PASS',free_MiB=sample['free_MiB'],utilization=sample['utilization_percent'])))


def gpu(root,attempt):
    cfg=load(root,'runtime/config.json');base.child_policy(root,cfg['model'],'gpu')
    expected=load(root,'inputs/exposure-%d.json'%attempt);bound=snapshots(root,cfg)
    need(expected['status']=='PASS' and all(expected[k]==v for k,v in bound.items()),'INPUT_SNAPSHOT_CHANGED')
    result=dict(status='FAILED',stage='IMPORT',**bound);begin=time.monotonic();torch=None
    try:
        import numpy as np
        import torch
        from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
        from transformers.video_utils import VideoMetadata
        torch.set_num_threads(2);torch.manual_seed(19);torch.cuda.set_device(0)
        need('3090' in torch.cuda.get_device_properties(0).name,'LOAD_DEVICE')
        free,total=torch.cuda.mem_get_info();need(free>=20*GIB,'LOAD_FREE')
        result['preload_free_bytes']=free
        torch.cuda.set_per_process_memory_fraction(18*GIB/total,0);torch.cuda.reset_peak_memory_stats()
        processor=AutoProcessor.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False)
        result['stage']='LOAD'
        model=Qwen3VLForConditionalGeneration.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False,
                    use_safetensors=True,torch_dtype=torch.bfloat16,attn_implementation='sdpa').eval().to('cuda:0')
        torch.cuda.synchronize();result['load_stage_seconds']=time.monotonic()-begin
        eos=model.generation_config.eos_token_id;eos=set(eos if isinstance(eos,list) else [eos])
        deadline=load(root,'runtime/model-envelope.json')['deadline']
        for slot in queue():
            need(time.time()<deadline-3,'MODEL_DEADLINE');result['stage']='INPUT'
            values,raw,question=make_input(slot,processor,np,VideoMetadata)
            item=check_input(slot,values,raw,question,processor,torch,cfg)
            need(item==expected['bindings'][str(slot['slot'])],'WORKER_INPUT_CHANGED')
            values={k:(v.to('cuda:0',dtype=torch.bfloat16) if v.is_floating_point() else v.to('cuda:0')) for k,v in values.items()}
            need(tensor_binding(values,torch)=={k:item[k] for k in ('full','parts','visual','text')},'DEVICE_BINDING')
            append(root,'STARTED',slot=slot['slot'],binding=item['full']);result['stage']='GENERATE';t=time.monotonic()
            with torch.inference_mode():output=model.generate(**values,max_new_tokens=16,do_sample=False)
            torch.cuda.synchronize();tokens=output[0,values['input_ids'].shape[-1]:].detach().cpu().tolist()
            answer=processor.tokenizer.decode(tokens,skip_special_tokens=True);need(len(answer.encode())<=8192,'ANSWER_LIMIT')
            pred=parse(slot['task'],answer)
            append(root,'TERMINAL',slot=slot['slot'],state='RETURNED' if pred is not None else 'INVALID',prediction=pred,
                   raw=answer,tokens=len(tokens),eos=bool(tokens and tokens[-1] in eos),
                   truncated=len(tokens)>=16 and (not tokens or tokens[-1] not in eos),seconds=time.monotonic()-t)
            need(torch.cuda.max_memory_allocated()<=18*GIB,'ALLOCATED_LIMIT')
            del values,raw,output,tokens
        result['status']='COMPLETE'
    except Exception as error:
        import traceback
        result.update(error=type(error).__name__,message=str(error)[:1500],stack=traceback.format_exc()[-7000:])
    finally:
        if torch is not None and torch.cuda.is_initialized():
            result.update(peak_allocated=torch.cuda.max_memory_allocated(),peak_reserved=torch.cuda.max_memory_reserved())
        result['seconds']=time.monotonic()-begin;write(root,'gpu/result.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('message','stack')}))


def validate_closed(rows,exit_record,bindings):
    started=[r for r in rows if r['event']=='STARTED'];terminal=[r for r in rows if r['event']=='TERMINAL']
    need(len(started)<=120 and len({r['slot'] for r in started})==len(started),'DUPLICATE_STARTED')
    need(len(terminal)==120 and {r['slot'] for r in terminal}==set(range(120)),'TERMINAL_CLOSURE')
    need(exit_record.get('pid') and exit_record.get('job_active')==0 and exit_record.get('exit_code') is not None,'MODEL_EXIT')
    begun={r['slot'] for r in started}
    need(all(r['state'] in ('RETURNED','INVALID','FAILED','NOT_RUN') and
             (r['slot'] in begun or r['state']=='NOT_RUN') for r in terminal),'STATE_CAUSALITY')
    need(all(r['binding']==bindings[str(r['slot'])]['full'] for r in started),'START_INPUT_BINDING')
    return {r['slot']:r for r in terminal}


def score(root,attempt):
    with open(Path(root)/'score/consumed.lock','xb') as f:f.write(b'039-once')
    rows=chain((Path(root)/'039-ledger.jsonl').read_bytes());cfg=load(root,'runtime/config.json')
    need(any(r['event']=='MODEL_EXIT' for r in rows) and any(r['event']=='QUEUE_CLOSED' for r in rows),'SCORE_ORDER')
    expected=load(root,'inputs/exposure-%d.json'%attempt);bound=snapshots(root,cfg)
    model=load(root,'gpu/result.json')
    need(all(expected[k]==model[k]==v for k,v in bound.items()),'SCORE_SNAPSHOT')
    terminal=validate_closed(rows,load(root,'gpu/exit.json'),expected['bindings'])
    frozen=load(root,'score/truth.json')
    need(frozen==[dict(slot=s['slot'],truth=truth(s['world'],s['clock'],s['task'])) for s in queue()],'FROZEN_TRUTH')
    result=[]
    for slot in queue():
        end=terminal[slot['slot']];pred=end.get('prediction');want=truth(slot['world'],slot['clock'],slot['task'])
        observed=end['state'] in ('RETURNED','INVALID')
        item=dict(**slot,state=end['state'],prediction=pred,truth=want,correct=(pred==want) if observed else None,
                  eos=end.get('eos'),truncated=end.get('truncated'),tokens=end.get('tokens'))
        if slot['task'] in ('NR','SR'):
            valid=pred is not None;grid=ticks(slot['clock'])
            item.update(red_correct=valid and pred[0]==want[0],blue_correct=valid and pred[1]==want[1],
                        swapped=valid and pred==list(reversed(want)),
                        ongrid_wrong_roles=valid and all(x in grid for x in pred) and pred!=want,
                        offgrid=valid and any(x not in grid for x in pred),
                        derived_gap_correct=valid and abs(pred[0]-pred[1])==abs(want[0]-want[1]))
        result.append(item)
    write(root,'score/results.json',dict(status='SCORED',slots=result,**bound));print(json.dumps(dict(status='SCORED',slots=120)))


def file_totals(root):
    return base.file_totals(root)


def coordinator(root):
    from development_pilot_030 import run_child,python_command,ExclusiveRead
    root=Path(root);cfg=load(root,'runtime/config.json');initial=chain((root/'039-ledger.jsonl').read_bytes())[0]
    need(not any(r['event']=='COORDINATOR' for r in chain((root/'039-ledger.jsonl').read_bytes())),'NO_COORDINATOR_RESTART')
    lock=ExclusiveRead(root/'run.lock');deadline=initial['deadline'];cpu=90;phases=[];attempt=1;model_exit=None
    env={k:v for k,v in os.environ.items() if not k.upper().startswith(('AWS_','AZURE_','GOOGLE_','HF_TOKEN'))}
    env.update(PATH=cfg['runtime']['path'],TEMP=str(root/'cache/temp'),TMP=str(root/'cache/temp'),
               HF_HOME=str(root/'cache/hf'),HF_HUB_CACHE=str(root/'cache/hf'),TORCH_HOME=str(root/'cache/torch'),
               XDG_CACHE_HOME=str(root/'cache/xdg'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
               HF_HUB_DISABLE_TELEMETRY='1',TOKENIZERS_PARALLELISM='false',PYTHONDONTWRITEBYTECODE='1')
    def phase(name,mode,limit,ml=False):
        nonlocal cpu
        need(time.time()+limit+30<deadline,'PARENT_DEADLINE')
        if mode!='gpu':need(cpu+limit<=480,'CPU_BUDGET');cpu+=limit
        append(root,'RESERVE',phase=name,seconds=limit,cpu_reserved=cpu,resource='gpu' if mode=='gpu' else 'cpu')
        command=python_command(cfg['runtime']['python'] if ml else sys.executable,'clock_binding_components_039',mode,str(root),str(attempt),
                               site=cfg['runtime']['site'] if ml else None)
        value=run_child(command,limit,environment=env)
        write(root,'runtime/'+name+'-exit.json',value)
        phases.append(dict(phase=name,**{k:v for k,v in value.items() if k not in ('stdout','stderr')}))
        append(root,'PHASE_EXIT',phase=name,exit_hash=digest(value),job_active=value['job_active'],seconds=value['seconds'])
        file_totals(root);return value
    reason='UNKNOWN'
    try:
        append(root,'COORDINATOR',pid=os.getpid(),**snapshots(root,cfg))
        passed=False
        for attempt in (1,2):
            suite=phase('suite-%d'%attempt,'suite',60)
            need(suite['exit_code']==0 and not suite['killed'] and not suite['overflow'],'NEW_SUITE_FAILED')
            actual=phase('exposure-%d'%attempt,'exposure',90,True)
            receipt=load(root,'inputs/exposure-%d.json'%attempt) if (root/('inputs/exposure-%d.json'%attempt)).exists() else {}
            if actual['exit_code']==0 and receipt.get('status')=='PASS':passed=True;break
            need(attempt==1 and receipt.get('error') in ('TypeError','AttributeError'),'HOLD_INPUT')
            before=code_hash();append(root,'API_REPAIR_REQUEST',code_hash=before,diagnostic_hash=digest(receipt))
            print('API_REPAIR_WAIT',flush=True);wait_end=min(deadline-720,time.time()+180)
            while time.time()<wait_end and not (root/'runtime/repair-approved.json').exists():time.sleep(.2)
            repair=load(root,'runtime/repair-approved.json')
            need(repair['prior_code']==before and repair['new_code']==code_hash() and before!=code_hash()
                 and repair.get('source_basis'),'REPAIR_NOT_BOUND')
        need(passed,'HOLD_INPUT')
        value=phase('resource','resource',10)
        need(value['exit_code']==0 and not value['killed'] and not value['overflow'],'RESOURCE_HOLD')
        write(root,'runtime/model-envelope.json',dict(deadline=time.time()+595,**snapshots(root,cfg)))
        append(root,'MODEL_LAUNCH',**snapshots(root,cfg))
        model_exit=phase('model','gpu',600,True);write(root,'gpu/exit.json',model_exit)
        append(root,'MODEL_EXIT',pid=model_exit['pid'],exit_code=model_exit['exit_code'],job_active=model_exit['job_active'],exit_hash=digest(model_exit))
        reason='MODEL_PHASE_FINISHED'
    except Exception as error:
        reason=str(error) if isinstance(error,ValueError) else type(error).__name__;append(root,'HOLD',reason=reason)
    finally:
        rows=chain((root/'039-ledger.jsonl').read_bytes());begun={r['slot'] for r in rows if r['event']=='STARTED'}
        ended={r['slot'] for r in rows if r['event']=='TERMINAL'}
        for slot in range(120):
            if slot not in ended:append(root,'TERMINAL',slot=slot,state='FAILED' if slot in begun else 'NOT_RUN',reason=reason)
        append(root,'QUEUE_CLOSED',slots=120)
        if model_exit is not None and any(r['event']=='TERMINAL' and r['state'] in ('RETURNED','INVALID') for r in rows):
            try:
                actual=phase('scorer','score',30)
                if actual['exit_code']!=0:append(root,'SCORE_HOLD',reason='SCORER_FAILED_NO_REOPEN')
            except Exception as error:append(root,'SCORE_HOLD',reason=type(error).__name__)
        append(root,'RUN_STOPPED',reason=reason,cpu_reserved=cpu,parent_seconds=time.time()-initial['start'])
        summary=dict(reason=reason,cpu_reserved=cpu,phases=phases,output=file_totals(root),parent_seconds=time.time()-initial['start'])
        write(root,'runtime/final-summary.json',summary);lock.close();print(json.dumps(summary),flush=True)


def main():
    if sys.argv[1]=='coordinate':return coordinator(sys.argv[2])
    need(sys.stdin.readline().strip()=='','PARENT_HANDSHAKE')
    mode,root,attempt=sys.argv[1],Path(sys.argv[2]),int(sys.argv[3])
    if mode=='suite':
        import unittest
        import test_clock_binding_components_039
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_clock_binding_components_039))
        need(result.testsRun>=16 and result.wasSuccessful(),'SUITE_FAILED')
    elif mode=='exposure':exposure(root,attempt)
    elif mode=='resource':resource(root)
    elif mode=='gpu':gpu(root,attempt)
    elif mode=='score':score(root,attempt)
    else:raise ValueError('MODE')


if __name__=='__main__':main()
