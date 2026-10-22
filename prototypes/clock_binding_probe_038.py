"""038 owned synthetic clock probe. No historical experiment/data entry point.

ML imports occur only in supervised exposure/model children. Pure supervision
helpers are imported read-only; no historical Journal or execution is used.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

MIB = 1024 ** 2
GIB = 1024 ** 3
SYSTEM = 'You are a helpful assistant.'
VIDEO_QUESTION = ('Using the timestamps attached to the red square and the blue square in the provided video, '
                  'what is their absolute time difference in seconds? Output only a non-negative integer.')
TEXT_QUESTION = ('The red square has timestamp {red:.1f} seconds. The blue square has timestamp {blue:.1f} seconds. '
                 'What is their absolute time difference in seconds? Output only a non-negative integer.')
POSITIONS = ((1, 3), (1, 4), (2, 3), (2, 4))
CLOCKS = ((0,1,4,5,8,9,12,13,16,17,20,21),
          (0,1,2,3,6,7,14,15,18,19,20,21),
          (60,61,64,65,68,69,72,73,76,77,80,81))
COLORS = ((16,16,16), (96,96,96), (240,32,32), (32,64,240))
TERMINALS = ('RETURNED', 'INVALID', 'FAILED', 'NOT_RUN')


def need(value, reason):
    if not value:
        raise ValueError(reason)


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(packed(value))


def load(root, name):
    return json.loads((Path(root)/name).read_bytes())


def write(root, name, value):
    target = Path(root)/name
    need(target.parent.is_dir(), 'OUTPUT_PARENT')
    raw = packed(value)+b'\n'
    need(len(raw) <= 4*MIB, 'OUTPUT_SIZE')
    with open(target, 'xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def append(root, event, **fields):
    path = Path(root)/'038-ledger.jsonl'
    rows = chain(path.read_bytes()) if path.exists() else []
    row = dict(seq=len(rows), prev=rows[-1]['hash'] if rows else '0'*64,
               event=event, at=time.time(), **fields)
    row['hash'] = digest(row)
    with open(path, 'ab') as stream:
        stream.write(packed(row)+b'\n'); stream.flush(); os.fsync(stream.fileno())


def chain(raw):
    need(raw.endswith(b'\n'), 'CHAIN_TRUNCATED')
    rows = []
    for line in raw.splitlines():
        row = json.loads(line); signature = row.pop('hash')
        need(row['seq']==len(rows) and row['prev']==(rows[-1]['hash'] if rows else '0'*64)
             and digest(row)==signature, 'CHAIN_INVALID')
        rows.append(dict(row, hash=signature))
    return rows


def spec():
    return dict(version='038_FROZEN_1', positions=POSITIONS, clocks=CLOCKS,
                colors=COLORS, shape=[12,192,288,3], fps=1, totals=[22,22,82],
                system=SYSTEM, video=VIDEO_QUESTION, text=TEXT_QUESTION,
                max_new_tokens=16, seed=19, dtype='bfloat16', attention='sdpa')


def queue():
    slots=[]
    for world in range(8):
        base=[(ch,g) for ch in ('V','O') for g in range(3)]
        shift=world%6; rotated=base[shift:]+base[:shift]
        for ch,g in rotated:
            slots.append(dict(slot=len(slots),world=world,clock=g,channel=ch))
    return slots


def times(clock):
    indices=CLOCKS[clock]
    return [(indices[k]+indices[k+1])/2 for k in range(0,12,2)]


def operands(world, clock):
    early,late=POSITIONS[world//2]
    red,blue=(early,late) if world%2==0 else (late,early)
    ts=times(clock)
    return ts[red],ts[blue]


def truth(world, clock):
    red,blue=operands(world,clock)
    return int(abs(red-blue))


def frame_bytes(world):
    early,late=POSITIONS[world//2]
    result=bytearray()
    for frame in range(12):
        k=frame//2; color=COLORS[1]
        if k==early: color=COLORS[2+world%2]
        if k==late: color=COLORS[3-world%2]
        bg=bytes(COLORS[0]); fg=bytes(color)
        for y in range(192):
            result.extend(bg*96+fg*96+bg*96 if 48<=y<144 else bg*288)
    return bytes(result)


def parse(raw):
    value=raw.strip()
    return int(value) if re.fullmatch(r'[0-9]{1,3}',value) else None


def validate_closed(rows, model_exit, expected_bindings):
    started=[r for r in rows if r['event']=='STARTED']
    ended=[r for r in rows if r['event']=='TERMINAL']
    need(len(started)<=48 and len({r['slot'] for r in started})==len(started), 'DUPLICATE_STARTED')
    need(len(ended)==48 and {r['slot'] for r in ended}==set(range(48)), 'INCOMPLETE_TERMINALS')
    need(all(r['state'] in TERMINALS for r in ended), 'INVALID_TERMINAL')
    need(model_exit.get('job_active')==0 and model_exit.get('pid') and model_exit.get('exit_code') is not None,
         'MODEL_EXIT_UNPROVEN')
    need(all(r['binding']==expected_bindings[str(r['slot'])]['full'] for r in started), 'INPUT_BINDING')
    return ended


def init(root, old):
    root=Path(root); old=Path(old)
    need(root.name=='integration_038' and old.name=='integration_036' and root.parent==old.parent, 'FIXED_ROOTS')
    need(not root.exists(), 'ROOT_ALREADY_EXISTS')
    root.mkdir()
    with open(root/'run.lock','xb') as stream: stream.write(b'038-single-run-do-not-remove\n')
    append(root,'RUN',purpose='REAL_038',deadline=time.time()+1680,started_monotonic=time.monotonic())
    for folder in ('runtime','inputs','gpu','score','cache','cache/temp','cache/hf','cache/torch','cache/xdg'):
        (root/folder).mkdir()
    evidence=[]; objects={}
    for name,cap in (('synthetic-startup-config.json',MIB),('runtime.json',MIB),
                     ('device-identity-reference.json',MIB),('startup-policy-3.json',MIB),('036-ledger.jsonl',2*MIB)):
        path=old/name; before=path.stat()
        need(not (before.st_file_attributes & 0x400) and before.st_size<=cap,'HANDOFF_METADATA')
        with open(path,'rb') as stream:
            raw=stream.read(cap+1); after=os.fstat(stream.fileno())
        need(len(raw)==before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns,'HANDOFF_CHANGED')
        evidence.append(dict(name=name,size=len(raw),sha256=sha(raw),mtime_ns=before.st_mtime_ns))
        objects[name]=raw
    oldrows=chain(objects.pop('036-ledger.jsonl'))
    need(oldrows[0].get('purpose')=='REAL_036' and oldrows[-1]['event']=='RUN_STOPPED','OLD_NOT_CLOSED')
    need(not any(r['event'] in ('MODEL_LAUNCH','STARTED','SCORE_CONSUMED','GPU_QUERY') for r in oldrows),'OLD_REAL_ACTION')
    need(len([r for r in oldrows if r['event']=='BOOTSTRAP'])==3 and any(r['event']=='SYNTHETIC_PASS' for r in oldrows),'OLD_STARTUP')
    cfg=json.loads(objects['synthetic-startup-config.json']); runtime=json.loads(objects['runtime.json'])
    identity=json.loads(objects['device-identity-reference.json']); policy=json.loads(objects['startup-policy-3.json'])
    need(policy.get('allow_null_device') is True,'NULL_COMPATIBILITY')
    model=cfg['models'][0]
    filtered=dict(model=model,runtime={k:runtime[k] for k in ('python','site','path')},device=identity)
    for name in ('config.json','preprocessor_config.json'):
        path=Path(model)/name; st=path.stat();need(st.st_size<=MIB,'CONFIG_SIZE')
        with open(path,'rb') as stream:raw=stream.read(MIB+1)
        need(len(raw)==st.st_size,'CONFIG_SHORT')
        value=json.loads(raw);evidence.append(dict(name='qwen-'+name,size=len(raw),sha256=sha(raw)))
        if name=='config.json':
            need(value.get('model_type')=='qwen3_vl','QWEN_TYPE')
            filtered['video_token_id']=value['video_token_id']
    write(root,'runtime/config.json',filtered)
    write(root,'runtime/external-reads.json',evidence)
    write(root,'inputs/spec.json',spec());write(root,'inputs/queue.json',queue())
    write(root,'score/truth.json',[dict(slot=s['slot'],truth=truth(s['world'],s['clock'])) for s in queue()])
    append(root,'INITIALIZED',input_bytes=sum(x['size'] for x in evidence),old_closed_hash=oldrows[-1]['hash'],
           spec_hash=digest(spec()),queue_hash=digest(queue()),cpu_reserved=0)
    print(json.dumps(dict(status='INITIALIZED',read_count=len(evidence),input_bytes=sum(x['size'] for x in evidence),
                          runtime_keys=list(filtered['runtime']),model=model,python=runtime['python'],site=runtime['site'])))


def code_hash():
    return sha(Path(__file__).read_bytes())


def child_policy(root, model, role):
    """Local-process read/write allowlist, not a whole-machine security claim."""
    norm=lambda p:os.path.normcase(os.path.abspath(os.fsdecode(os.fspath(p))))
    own=norm(root); weights=norm(model); score=norm(Path(root)/'score')
    readonly=[norm(sys.prefix),norm(sys.base_prefix),norm(Path(__file__).parent),weights]
    null=norm(os.devnull)
    def below(name,prefix):return name==prefix or name.startswith(prefix+os.sep)
    def audit(event,args):
        if event in ('socket.connect','socket.connect_ex','socket.getaddrinfo','subprocess.Popen','os.system'):
            raise PermissionError('038_NETWORK_OR_CHILD_DENIED')
        if event=='open' and not isinstance(args[0],int):
            name=norm(args[0]);flags=args[2] if len(args)>2 and type(args[2]) is int else 0
            if name==null:return
            if below(name,score):raise PermissionError('038_SCORE_DENIED')
            if not below(name,own) and not any(below(name,p) for p in readonly):
                raise PermissionError('038_READ_DENIED')
            if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_TRUNC) and not below(name,own):
                raise PermissionError('038_WRITE_DENIED')
            if role=='exposure' and below(name,weights) and name.endswith(('.safetensors','.bin','.pt','.pth')):
                raise PermissionError('038_CPU_WEIGHTS_DENIED')
    sys.addaudithook(audit)


def tensor_signature(value, torch, final=False):
    val=value.detach().cpu().contiguous()
    if final and val.is_floating_point():val=val.to(torch.bfloat16)
    return dict(dtype=str(val.dtype),shape=list(val.shape),sha256=sha(val.view(torch.uint8).numpy().tobytes()))


def binding(values, torch):
    parts={key:tensor_signature(value,torch,True) for key,value in sorted(values.items())}
    return dict(full=digest(parts),parts=parts,
                visual=digest({k:v for k,v in parts.items() if k in ('pixel_values_videos','video_grid_thw')}),
                text=digest({k:v for k,v in parts.items() if k not in ('pixel_values_videos','video_grid_thw')}))


def inputs(slot, processor, np, VideoMetadata):
    w,g,ch=slot['world'],slot['clock'],slot['channel']
    question=VIDEO_QUESTION if ch=='V' else TEXT_QUESTION.format(red=operands(w,g)[0],blue=operands(w,g)[1])
    content=([dict(type='video',video='owned-memory-only')] if ch=='V' else [])+[dict(type='text',text=question)]
    messages=[dict(role='system',content=SYSTEM),dict(role='user',content=content)]
    prompt=processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    if ch=='V':
        frames=np.frombuffer(frame_bytes(w),dtype=np.uint8).reshape(12,192,288,3).copy()
        metadata=VideoMetadata(total_num_frames=(22,22,82)[g],fps=1.,width=288,height=192,
                               duration=float((22,22,82)[g]),frames_indices=list(CLOCKS[g]))
        values=processor(text=[prompt],videos=[frames],video_metadata=[metadata],
                         do_sample_frames=False,do_resize=False,return_tensors='pt')
    else:
        values=processor(text=[prompt],return_tensors='pt')
    return values,question


def check_input(slot,values,question,processor,torch,video_id):
    count=int((values['input_ids']==video_id).sum())
    need(int(values['input_ids'].shape[-1])<=2048,'INPUT_TOKEN_LIMIT')
    decoded=processor.tokenizer.decode(values['input_ids'][0],skip_special_tokens=False)
    if slot['channel']=='V':
        need(values['video_grid_thw'].tolist()==[[6,12,18]] and count==324,'GRID_OR_TOKEN_BUDGET')
        got=[float(x) for x in re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded)]
        need(got==times(slot['clock']),'NATIVE_TIMECODES')
        need(decoded.count(VIDEO_QUESTION)==1 and question==VIDEO_QUESTION,'QUESTION_CHANGED')
    else:
        need(count==0 and 'pixel_values_videos' not in values,'TEXT_VISUAL_LEAK')
        need(question in decoded,'TEXT_OPERANDS_CHANGED')
        got=[]
    normalized=re.sub(r'<[0-9]+\.[0-9] seconds>','<CLOCK>',decoded) if slot['channel']=='V' else decoded
    return dict(**binding(values,torch),tokens=int(values['input_ids'].shape[-1]),visual_tokens=count,
                timecodes=got,normalized_text=sha(normalized.encode()),
                rgb=sha(frame_bytes(slot['world'])) if slot['channel']=='V' else None)


def exposure(root, attempt):
    cfg=load(root,'runtime/config.json');child_policy(root,cfg['model'],'exposure')
    stage='IMPORT';start=time.monotonic()
    result=dict(status='HOLD_INPUT',attempt=attempt,code_hash=code_hash(),spec_hash=digest(spec()),queue_hash=digest(queue()))
    try:
        import numpy as np
        import torch
        import transformers
        from transformers import AutoProcessor
        from transformers.video_utils import VideoMetadata
        torch.set_num_threads(2);need(not torch.cuda.is_initialized(),'CPU_CUDA_INITIALIZED')
        stage='PROCESSOR';processor=AutoProcessor.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False)
        bindings={};seen={};stage='INPUTS'
        for slot in queue():
            values,question=inputs(slot,processor,np,VideoMetadata)
            item=check_input(slot,values,question,processor,torch,cfg['video_token_id'])
            if slot['channel']=='V':
                w=slot['world'];previous=seen.setdefault(w,[])
                need(all(x['visual']==item['visual'] and x['rgb']==item['rgb'] for x in previous),'CLOCK_VISUAL_CHANGED')
                need(all(x['normalized_text']==item['normalized_text'] for x in previous),'NONCLOCK_TEXT_CHANGED')
                need(all(x['text']!=item['text'] and x['full']!=item['full'] for x in previous),'CLOCK_NOT_EXPOSED')
                previous.append(item)
            bindings[str(slot['slot'])]=item
            del values
        need(len(bindings)==48 and len(seen)==8 and all(len(x)==3 for x in seen.values()),'EXPOSURE_COMPLETE')
        need(not torch.cuda.is_initialized(),'CPU_CUDA_INITIALIZED')
        result.update(status='PASS',bindings=bindings,versions=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=np.__version__),
                      cuda_initialized=False,processor_class=type(processor).__name__)
    except Exception as error:
        import traceback
        result.update(stage=stage,error=type(error).__name__,message=str(error)[:1500],stack=traceback.format_exc()[-7000:])
    result['seconds']=time.monotonic()-start
    write(root,'inputs/exposure-%d.json'%attempt,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('bindings','stack','message')},default=str))


def resource(root):
    from development_pilot_030 import parse_resource_sample_036
    import subprocess
    cfg=load(root,'runtime/config.json')
    # Exactly one external query; subprocess has its own short timeout.
    raw=subprocess.run(['nvidia-smi','-q','-x','-i','0'],capture_output=True,timeout=8,creationflags=0x08000000)
    need(raw.returncode==0,'RESOURCE_QUERY_FAILED')
    sample=parse_resource_sample_036(raw.stdout.decode(),cfg['device'])
    write(root,'runtime/resource.json',sample)
    print(json.dumps(dict(status='PASS',free_MiB=sample['free_MiB'],utilization=sample['utilization_percent'])))


def gpu(root,attempt):
    cfg=load(root,'runtime/config.json');child_policy(root,cfg['model'],'gpu')
    expected=load(root,'inputs/exposure-%d.json'%attempt)
    need(expected['status']=='PASS' and expected['code_hash']==code_hash(),'EXPOSURE_CODE_STALE')
    result=dict(status='FAILED',code_hash=code_hash(),spec_hash=digest(spec()),queue_hash=digest(queue()),stage='IMPORT')
    begin=time.monotonic();torch=None
    try:
        import numpy as np
        import torch
        from transformers import AutoProcessor,Qwen3VLForConditionalGeneration
        from transformers.video_utils import VideoMetadata
        torch.set_num_threads(2);torch.manual_seed(19)
        torch.cuda.set_device(0)
        props=torch.cuda.get_device_properties(0)
        need('3090' in props.name,'LOAD_DEVICE')
        free,total=torch.cuda.mem_get_info();need(free>=20*GIB,'LOAD_FREE_THRESHOLD')
        torch.cuda.set_per_process_memory_fraction(18*GIB/total,0);torch.cuda.reset_peak_memory_stats()
        processor=AutoProcessor.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False)
        result['stage']='LOAD'
        model=Qwen3VLForConditionalGeneration.from_pretrained(cfg['model'],local_files_only=True,trust_remote_code=False,
                    use_safetensors=True,torch_dtype=torch.bfloat16,attn_implementation='sdpa').eval().to('cuda:0')
        torch.cuda.synchronize();result['load_seconds']=time.monotonic()-begin
        eos=model.generation_config.eos_token_id;eos=set(eos if isinstance(eos,list) else [eos])
        for slot in queue():
            need(time.time()<load(root,'runtime/worker-envelope.json')['deadline']-3,'GPU_DEADLINE')
            result['stage']='INPUT';values,question=inputs(slot,processor,np,VideoMetadata)
            item=check_input(slot,values,question,processor,torch,cfg['video_token_id'])
            need(item==expected['bindings'][str(slot['slot'])],'WORKER_INPUT_CHANGED')
            values={k:(v.to('cuda:0',dtype=torch.bfloat16) if v.is_floating_point() else v.to('cuda:0')) for k,v in values.items()}
            # Verify the exact final device representation without another forward.
            need(binding(values,torch)=={k:item[k] for k in ('full','parts','visual','text')},'DEVICE_INPUT_CHANGED')
            append(root,'STARTED',slot=slot['slot'],binding=item['full'])
            result['stage']='GENERATE';t=time.monotonic()
            with torch.inference_mode():
                output=model.generate(**values,max_new_tokens=16,do_sample=False)
            torch.cuda.synchronize()
            tokens=output[0,values['input_ids'].shape[-1]:].detach().cpu().tolist()
            raw=processor.tokenizer.decode(tokens,skip_special_tokens=True)
            prediction=parse(raw);need(len(raw.encode())<=8192,'RAW_LIMIT')
            append(root,'TERMINAL',slot=slot['slot'],state='RETURNED' if prediction is not None else 'INVALID',
                   raw=raw,prediction=prediction,tokens=len(tokens),eos=bool(tokens and tokens[-1] in eos),
                   truncated=len(tokens)>=16 and (not tokens or tokens[-1] not in eos),seconds=time.monotonic()-t)
            need(torch.cuda.max_memory_allocated()<=18*GIB,'ALLOCATED_LIMIT')
            del values,output,tokens
        result['status']='COMPLETE'
    except Exception as error:
        import traceback
        result.update(error=type(error).__name__,message=str(error)[:1500],stack=traceback.format_exc()[-7000:])
    finally:
        if torch is not None and torch.cuda.is_initialized():
            result.update(peak_allocated=torch.cuda.max_memory_allocated(),peak_reserved=torch.cuda.max_memory_reserved())
        result['seconds']=time.monotonic()-begin
        write(root,'gpu/result.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('stack','message')}))


def score(root,attempt):
    with open(Path(root)/'score/consumed.lock','xb') as stream:stream.write(b'once')
    rows=chain((Path(root)/'038-ledger.jsonl').read_bytes())
    need(any(r['event']=='MODEL_EXIT' for r in rows) and any(r['event']=='QUEUE_CLOSED' for r in rows),'SCORE_GATE')
    exposure_record=load(root,'inputs/exposure-%d.json'%attempt)
    need(exposure_record['code_hash']==code_hash() and exposure_record['spec_hash']==digest(load(root,'inputs/spec.json'))
         and exposure_record['queue_hash']==digest(load(root,'inputs/queue.json')),'SCORE_SNAPSHOT')
    ended=validate_closed(rows,load(root,'gpu/exit.json'),exposure_record['bindings'])
    frozen=load(root,'score/truth.json')
    need(frozen==[dict(slot=s['slot'],truth=truth(s['world'],s['clock'])) for s in queue()],'TRUTH_BINDING')
    output=[]
    for slot in queue():
        end=next(x for x in ended if x['slot']==slot['slot'])
        pred=end.get('prediction');observed=end['state'] in ('RETURNED','INVALID')
        output.append(dict(**slot,state=end['state'],prediction=pred,truth=truth(slot['world'],slot['clock']),
                           correct=(pred==truth(slot['world'],slot['clock'])) if observed else None))
    write(root,'score/results.json',dict(status='SCORED',slots=output))
    print(json.dumps(dict(status='SCORED',slots=len(output))))


def file_totals(root):
    files=[]
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs+names:
            st=(Path(folder)/name).lstat();need(not st.st_file_attributes & 0x400,'OUTPUT_REPARSE')
        files.extend(Path(folder)/n for n in names)
    total=sum(p.stat().st_size for p in files)
    need(len(files)<=96 and total<=64*MIB,'OUTPUT_QUOTA')
    return dict(files=len(files),bytes=total)


def coordinator(root):
    """One live parent holds the run lock through suite/exposure and GPU/score."""
    from development_pilot_030 import run_child,python_command,ExclusiveRead
    root=Path(root);lock=ExclusiveRead(root/'run.lock');cfg=load(root,'runtime/config.json')
    initial=chain((root/'038-ledger.jsonl').read_bytes())[0]
    window=load(root,'runtime/parent-window.json')
    deadline=min(initial['deadline'],window['deadline']);cpu=60;phase_results=[]
    env={k:v for k,v in os.environ.items() if not k.upper().startswith(('AWS_','AZURE_','GOOGLE_','HF_TOKEN'))}
    env.update(PATH=cfg['runtime']['path'],TEMP=str(root/'cache/temp'),TMP=str(root/'cache/temp'),
               HF_HOME=str(root/'cache/hf'),HF_HUB_CACHE=str(root/'cache/hf'),TORCH_HOME=str(root/'cache/torch'),
               XDG_CACHE_HOME=str(root/'cache/xdg'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
               HF_HUB_DISABLE_TELEMETRY='1',TOKENIZERS_PARALLELISM='false',PYTHONDONTWRITEBYTECODE='1')
    def phase(name,mode,limit,ml=False):
        nonlocal cpu
        need(time.time()+limit+30<deadline,'PARENT_DEADLINE')
        isgpu=mode=='gpu'
        if not isgpu:need(cpu+limit<=480,'CPU_BUDGET');cpu+=limit
        append(root,'RESERVE',phase=name,seconds=limit,resource='gpu' if isgpu else 'cpu',cpu_reserved=cpu)
        command=python_command(cfg['runtime']['python'] if ml else sys.executable,'clock_binding_probe_038',mode,str(root),str(attempt),
                               site=cfg['runtime']['site'] if ml else None)
        value=run_child(command,limit,environment=env)
        write(root,'runtime/'+name+'-exit.json',value);phase_results.append(dict(phase=name,**{k:v for k,v in value.items() if k not in ('stdout','stderr')}))
        append(root,'PHASE_EXIT',phase=name,exit_hash=digest(value),job_active=value['job_active'],seconds=value['seconds'])
        return value
    reason='UNKNOWN';attempt=1;gpu_exit=None
    try:
        append(root,'COORDINATOR',pid=os.getpid(),deadline=deadline)
        passed=False
        for attempt in (1,2):
            suite=phase('suite-%d'%attempt,'suite',60)
            need(suite['exit_code']==0 and not suite['killed'] and not suite['overflow'],'NEW_SUITE_FAILED')
            actual=phase('exposure-%d'%attempt,'exposure',90,True)
            receipt=load(root,'inputs/exposure-%d.json'%attempt) if (root/('inputs/exposure-%d.json'%attempt)).exists() else {}
            if actual['exit_code']==0 and receipt.get('status')=='PASS':passed=True;break
            # An optional second attempt requires a human-visible, exact-source
            # API diagnosis and a changed implementation, not an automatic retry.
            need(attempt==1 and receipt.get('error') in ('TypeError','AttributeError'),'HOLD_INPUT')
            append(root,'API_REPAIR_REQUEST',code_hash=code_hash(),diagnostic_hash=digest(receipt))
            print('API_REPAIR_WAIT',flush=True)
            prior=code_hash();wait_end=min(deadline-300,time.time()+180)
            while time.time()<wait_end and not (root/'runtime/repair-approved.json').exists():time.sleep(.2)
            repair=load(root,'runtime/repair-approved.json')
            need(repair['prior_code']==prior and repair['new_code']==code_hash() and prior!=code_hash()
                 and repair.get('source_basis'),'REPAIR_NOT_BOUND')
        need(passed,'HOLD_INPUT')
        phase_results_before=list(phase_results)
        query=phase('resource','resource',10)
        need(query['exit_code']==0 and not query['killed'] and not query['overflow'],'RESOURCE_HOLD')
        write(root,'runtime/worker-envelope.json',dict(deadline=time.time()+595,code_hash=code_hash(),attempt=attempt))
        append(root,'MODEL_LAUNCH',code_hash=code_hash(),attempt=attempt)
        gpu_exit=phase('model','gpu',600,True);write(root,'gpu/exit.json',gpu_exit)
        append(root,'MODEL_EXIT',pid=gpu_exit['pid'],job_active=gpu_exit['job_active'],exit_code=gpu_exit['exit_code'],exit_hash=digest(gpu_exit))
        reason='MODEL_PHASE_FINISHED'
    except Exception as error:
        reason=str(error) if isinstance(error,ValueError) else type(error).__name__
        append(root,'HOLD',reason=reason)
    finally:
        rows=chain((root/'038-ledger.jsonl').read_bytes());started={r['slot'] for r in rows if r['event']=='STARTED'}
        ended={r['slot'] for r in rows if r['event']=='TERMINAL'}
        for slot in range(48):
            if slot not in ended:append(root,'TERMINAL',slot=slot,state='FAILED' if slot in started else 'NOT_RUN',reason=reason)
        append(root,'QUEUE_CLOSED',slots=48)
        if gpu_exit is not None and any(r['event']=='TERMINAL' and r['state'] in ('RETURNED','INVALID') for r in rows):
            try:phase('scorer','score',30)
            except Exception as error:append(root,'SCORE_HOLD',reason=type(error).__name__)
        append(root,'RUN_STOPPED',reason=reason,cpu_reserved=cpu,parent_seconds=time.time()-window['start'])
        summary=dict(reason=reason,cpu_reserved=cpu,phases=phase_results,output=file_totals(root),
                     parent_seconds=time.time()-window['start'])
        write(root,'runtime/final-summary.json',summary);lock.close()
        print(json.dumps(summary),flush=True)


def main():
    mode=sys.argv[1]
    if mode=='init':return init(sys.argv[2],sys.argv[3])
    if mode=='coordinate':return coordinator(sys.argv[2])
    need(sys.stdin.readline().strip()=='','PARENT_HANDSHAKE')
    root=Path(sys.argv[2]);attempt=int(sys.argv[3])
    if mode=='suite':
        import unittest
        import test_clock_binding_probe_038
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_clock_binding_probe_038))
        need(result.testsRun>=12 and result.wasSuccessful(),'SUITE_FAILED')
    elif mode=='exposure':exposure(root,attempt)
    elif mode=='resource':resource(root)
    elif mode=='gpu':gpu(root,attempt)
    elif mode=='score':score(root,attempt)
    else:raise ValueError('MODE')


if __name__=='__main__':main()
