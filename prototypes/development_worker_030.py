"""030 nongold four-arm worker with fixed035 binding; no defaults/heavy imports."""
import argparse
from dataclasses import asdict
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import time

from development_pilot_030 import Journal, require, require_ready, load, packed, digest, GIB, validate_queue_035, validate_start_035, resource_receipt_035
from temporal_evidence_adapter_025 import select_four


class StartupDiagnostic:
    def __init__(self):self.stage='ENTRY';self.stages=[];self.denials=[];self.denial_bytes=0
    def set(self,stage):
        self.stage=stage
        if len(self.stages)<128:self.stages.append(stage)
    def deny(self,event,reason,path=None,flags=0):
        item=dict(event=event,reason=reason,stage=self.stage,path=path[:1024] if path else None,flags=flags)
        size=len(packed(item))
        if len(self.denials)<16 and self.denial_bytes+size<=8192:self.denials.append(item);self.denial_bytes+=size
        raise PermissionError(reason)
    def error(self,error):
        frames=[];tb=error.__traceback__
        while tb is not None and len(frames)<32:
            frames.append(dict(filename=tb.tb_frame.f_code.co_filename,function=tb.tb_frame.f_code.co_name,lineno=tb.tb_lineno));tb=tb.tb_next
        return dict(stage=self.stage,stages=self.stages,exception_class=type(error).__name__,errno=getattr(error,'errno',None),
                    winerror=getattr(error,'winerror',None),message=str(error)[:512],frames=frames,denials=self.denials)


def install_policy(root,model_roots,diagnostic,exact_reads=(),install=True):
    norm=lambda p:os.path.normcase(os.path.abspath(os.fspath(p)))
    own=norm(root)
    allowed=[own,norm(Path(__file__).parent),norm(sys.prefix),norm(sys.base_prefix),norm(Path(os.__file__).parent)]+[norm(p) for p in model_roots]
    require(len(exact_reads)<=4,'035_EXACT_READ_LIMIT');exact={norm(p) for p in exact_reads}
    def audit(event,args):
        if event in ('socket.connect','socket.connect_ex','socket.getaddrinfo','subprocess.Popen','os.system'):
            diagnostic.deny(event,'035_NETWORK_OR_CHILD_DENIED')
        if event=='open' and not isinstance(args[0],int):
            name=norm(args[0]);flags=args[2] if len(args)>2 and type(args[2]) is int else 0
            if not any(name==p or name.startswith(p+os.sep) for p in allowed) and name not in exact:
                diagnostic.deny(event,'035_READ_ALLOWLIST',name,flags)
            if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND) and not name.startswith(own+os.sep):
                diagnostic.deny(event,'035_WRITE_ALLOWLIST',name,flags)
    if install:sys.addaudithook(audit)
    return audit


def startup(root,config,journal,diag,policy):
    diag.set('POLICY_INSTALL');rules=load(root,'startup-policy-%d.json'%policy)
    install_policy(root,config['models'],diag,rules['exact_reads'])
    diag.set('NUMPY_IMPORT');import numpy as np
    diag.set('TORCH_IMPORT');import torch
    diag.set('TRANSFORMERS_IMPORT');from transformers import AutoProcessor,SiglipModel,Qwen3VLForConditionalGeneration
    diag.set('VIDEO_METADATA_IMPORT');from transformers.video_utils import VideoMetadata
    torch.set_num_threads(2)
    diag.set('QWEN_CPU_PROCESSOR');qp=AutoProcessor.from_pretrained(config['models'][0],local_files_only=True,trust_remote_code=False)
    diag.set('SIGLIP_CPU_PROCESSOR');sp=AutoProcessor.from_pretrained(config['models'][1],local_files_only=True,trust_remote_code=False)
    diag.set('CPU_FACTORY');namespace={}
    source=(Path(root)/config['factory']).read_text(encoding='utf-8')
    exec(compile(source,'<035-private-original-factory>','exec'),namespace)
    return np,torch,AutoProcessor,SiglipModel,Qwen3VLForConditionalGeneration,VideoMetadata,qp,sp,namespace


def bootstrap(root,attempt,policy):
    from development_pilot_030 import code_version_035
    j=Journal(root);diag=StartupDiagnostic();result=dict(status='HOLD',attempt=attempt,policy=policy,code_hash=code_version_035())
    try:
        require_ready(j);calls=j.events('BOOTSTRAP');require(len(calls)==attempt and attempt in (1,2),'035_BOOTSTRAP_CAP')
        config=load(root,'worker-input.json');result['worker_hash']=digest(config)
        np,torch,_,_,_,VideoMetadata,qp,sp,namespace=startup(root,config,j,diag,policy)
        require(not torch.cuda.is_initialized(),'035_BOOTSTRAP_CUDA_INITIALIZED')
        diag.set('CPU_HELPER_INPUT');candidate=load(root,'P2-candidates.json');frames=np.load(Path(root)/candidate['frames'],mmap_mode='r',allow_pickle=False)
        source=next(v for v in config['sources'] if v['alias']=='P2');r={'grid':[6,12,18],'visual_tokens_per_call':324}
        helper=namespace['make_inputs']({'questions':[source]},VideoMetadata=VideoMetadata,duration=candidate['duration'],fps=candidate['fps'],
              frames=frames,need=require,np=np,prior=candidate['prior'],qc=config['qwen_config'],qp=qp,r=r,system=config['system'],times=candidate['times'])
        values=helper(0,tuple(round(47*k/11) for k in range(12)))
        require(values['video_grid_thw'][0].tolist()==[6,12,18] and int((values['input_ids']==config['qwen_config']['video_token_id']).sum())==324,'035_BOOTSTRAP_VISUAL_BUDGET')
        require(all(v.device.type=='cpu' for v in values.values()) and not torch.cuda.is_initialized(),'035_BOOTSTRAP_CPU_ONLY')
        diag.set('CPU_COMPLETE');result.update(status='PASS',stages=diag.stages,grid=[6,12,18],visual_tokens=324,input_tokens=int(values['input_ids'].shape[1]),cuda_initialized=False,
                    policy_hash=digest(load(root,'startup-policy-%d.json'%policy)))
    except Exception as error:result['diagnostic']=diag.error(error)
    finally:
        result['stage']=diag.stage;j.write('bootstrap-%d-result.json'%attempt,result);j.close()


def tensor_binding(values):
    sha = hashlib.sha256()
    for key in sorted(values):
        value = values[key].detach().cpu().contiguous()
        sha.update(key.encode()); sha.update(str(value.dtype).encode()); sha.update(str(tuple(value.shape)).encode())
        sha.update(value.view(__import__('torch').uint8).numpy().tobytes())
    return sha.hexdigest()


def coverage(indices, times):
    return dict(span_seconds=round(times[indices[-1]] - times[indices[0]]),
                candidate_bins=len({i // 4 for i in indices}),
                time_bins=len({min(11, int(12 * (times[i]-times[0]) / (times[-1]-times[0]))) for i in indices}))


def worker(root,attempt,policy):
    start = time.monotonic(); journal = Journal(root); torch = None; result = dict(status='HOLD', stage='ENTRY',attempt=attempt);diag=StartupDiagnostic()
    try:
        require_ready(journal)
        journal.once('WORKER_ENTERED', str(attempt),attempt=attempt)
        config = load(root, 'worker-input.json'); queue = load(root, 'queue.json')
        frozen=journal.events('FROZEN');launches=journal.events('MODEL_LAUNCH')
        require(digest(config) == queue['worker_hash'] and len(queue['slots']) == 16
                and queue['contract_id']=='035' and queue['run_id']==journal.rows[0]['run_id']
                and len(frozen)==1 and 1<=len(launches)<=2 and frozen[0]['worker_hash']==queue['worker_hash']
                and frozen[0]['plan_hash']==queue['plan_hash'] and launches[-1]['queue_hash']==digest(queue)
                and queue['slots']==config['slots'], 'WORKER_FREEZE_BINDING')
        validate_queue_035(queue,config)
        resource=resource_receipt_035(journal.rows,root)
        require(launches[-1].get('resource_hash')==resource['hash'],'035_WORKER_RESOURCE_BINDING')
        from development_pilot_030 import validate_attempt_035
        validate_attempt_035(journal.rows,root,attempt)
        require(launches[-1]['policy']==policy,'035_WORKER_POLICY')
        np,torch,_,SiglipModel,Qwen3VLForConditionalGeneration,VideoMetadata,qp,sp,namespace=startup(root,config,journal,diag,policy)
        diag.set('CUDA_AVAILABILITY')
        require(torch.cuda.is_available(), 'CUDA_UNAVAILABLE')
        diag.set('CUDA_DEVICE');properties=torch.cuda.get_device_properties(0)
        require('3090' in properties.name,'035_WORKER_DEVICE')
        diag.set('CUDA_FREE');free,total=torch.cuda.mem_get_info(0)
        journal.add('WORKER_FREE_RECHECK',attempt=attempt,device=0,free_bytes=free,total_bytes=total,resource_hash=resource['hash'])
        require(free>=20*GIB,'035_WORKER_FREE_MEMORY')
        require(23 * GIB <= total <= 25 * GIB, 'DEVICE_MEMORY')
        diag.set('ALLOCATOR');torch.cuda.set_per_process_memory_fraction(18 * GIB / total, 0)
        torch.cuda.reset_peak_memory_stats(0)
        torch.manual_seed(19)
        def guard():
            require(time.time()<journal.events('GPU_ENVELOPE')[0]['deadline']-5 and time.monotonic() - start < 895 and torch.cuda.max_memory_allocated(0) <= 18 * GIB, 'GPU_RESOURCE_CAP')
            journal.check_time()
        model_inputs = {}; selections = {}; features = {}; costs = {}; frames_by_source = {}; bindings = {}
        diag.set('SIGLIP_LOAD');result['stage'] = 'SIGLIP_LOAD'; guard(); t = time.monotonic()
        sm = SiglipModel.from_pretrained(config['models'][1], local_files_only=True, trust_remote_code=False,
                use_safetensors=True, attn_implementation='sdpa').eval().to(device='cuda:0', dtype=torch.float32)
        torch.cuda.synchronize(); result['siglip_load_seconds'] = time.monotonic()-t
        for source in config['sources']:
            alias = source['alias']
            if not queue['available'][alias]:
                continue
            guard(); candidate = load(root, alias + '-candidates.json')
            frames = np.load(Path(root) / candidate['frames'], mmap_mode='r', allow_pickle=False)
            require(len(frames) == 48 and all(hashlib.sha256(frames[i].tobytes()).hexdigest() == candidate['rgb_hashes'][i] for i in range(48)), 'FRAME_BINDING')
            frames_by_source[alias] = frames
            diag.set('SIGLIP_IMAGE_ENCODE');image = []; t = time.monotonic()
            with torch.inference_mode():
                for offset in range(0, 48, 8):
                    guard(); pixels = sp(images=[f for f in frames[offset:offset+8]], return_tensors='pt')['pixel_values'].to('cuda:0')
                    encoded = sm.get_image_features(pixel_values=pixels)
                    require(bool(torch.isfinite(encoded).all().item()), 'SIGLIP_NONFINITE')
                    image.append(torch.nn.functional.normalize(encoded, dim=-1).cpu()); del pixels, encoded
                torch.cuda.synchronize(); image_seconds = time.monotonic()-t
                # Same original padding/truncation rule, three separately measured queries.
                diag.set('SIGLIP_TEXT_ENCODE');texts = [source['question'], source['event_a'], source['event_b']]
                text_features = []; text_metrics = []
                for text in texts:
                    guard(); t = time.monotonic()
                    uncut = sp.tokenizer(text, truncation=False, add_special_tokens=True)['input_ids']
                    values = sp(text=[text], padding='max_length', truncation=True, return_tensors='pt')
                    actual = int(values['input_ids'].shape[-1])
                    real = int(values['attention_mask'].sum()) if 'attention_mask' in values else min(len(uncut), actual)
                    values = {k: v.to('cuda:0') for k, v in values.items()}
                    encoded = sm.get_text_features(**values)
                    require(bool(torch.isfinite(encoded).all().item()), 'SIGLIP_NONFINITE')
                    text_features.append(torch.nn.functional.normalize(encoded, dim=-1).cpu())
                    torch.cuda.synchronize()
                    text_metrics.append(dict(seconds=time.monotonic()-t, untruncated_length=len(uncut), actual_length=actual,
                                             content_length=real, truncated=len(uncut)>actual)); del values, encoded
            t = time.monotonic()
            diag.set('SELECT');scores = (torch.cat(text_features) @ torch.cat(image).T).numpy().tolist()
            arms = select_four(candidate['times'], *scores)
            selections[alias] = {s.arm: s for s in arms}
            metrics = {s.arm: coverage(s.indices, candidate['times']) for s in arms}
            costs[alias] = dict(image_seconds=image_seconds, texts=text_metrics, selection_seconds=time.monotonic()-t,
                                cd_same=arms[2].indices == arms[3].indices, coverage=metrics,
                                c_pair_forward=arms[2].event_pair[0] < arms[2].event_pair[1],
                                c_objective=scores[1][arms[2].event_pair[0]]+scores[2][arms[2].event_pair[1]],
                                d_objective=scores[1][arms[3].event_pair[0]]+scores[2][arms[3].event_pair[1]])
            journal.write(alias + '-selection-%d-private.json'%attempt, dict(arms=[asdict(s) for s in arms], scores=scores, metrics=costs[alias]))
            r = {'grid': [6, 12, 18], 'visual_tokens_per_call': 324}
            model_inputs[alias] = namespace['make_inputs']({'questions': [source]}, VideoMetadata=VideoMetadata,
                duration=candidate['duration'], fps=candidate['fps'], frames=frames, need=require, np=np,
                prior=candidate['prior'], qc=config['qwen_config'], qp=qp, r=r, system=config['system'], times=candidate['times'])
            del image, text_features
        del sm; gc.collect(); torch.cuda.empty_cache(); guard()
        diag.set('QWEN_LOAD');result['stage'] = 'QWEN_LOAD'; t = time.monotonic()
        model = Qwen3VLForConditionalGeneration.from_pretrained(config['models'][0], local_files_only=True, trust_remote_code=False,
                    use_safetensors=True, torch_dtype=torch.bfloat16, attn_implementation='sdpa').eval().to('cuda:0')
        torch.cuda.synchronize(); result['qwen_load_seconds'] = time.monotonic()-t
        eos = model.generation_config.eos_token_id; eos = set(eos if isinstance(eos, list) else [eos])
        diag.set('GENERATE');result['stage'] = 'GENERATE'
        for slot in queue['slots']:
            alias, arm, number = slot['alias'], slot['arm'], slot['slot']
            if not queue['available'][alias]:
                continue
            guard(); t = time.monotonic()
            diag.set('QWEN_PROCESSOR');values = model_inputs[alias](0, selections[alias][arm].indices)
            require(values['video_grid_thw'][0].tolist() == [6, 12, 18]
                    and int((values['input_ids'] == config['qwen_config']['video_token_id']).sum()) == 324, 'REALIZED_VISUAL_BUDGET')
            token_count = int(values['input_ids'].shape[1]); input_hash = tensor_binding(values)
            bindings[(alias, arm)] = input_hash
            values = {k: (v.to('cuda:0', dtype=torch.bfloat16) if v.is_floating_point() else v.to('cuda:0')) for k, v in values.items()}
            prep_seconds = time.monotonic()-t; guard()
            validate_start_035(journal.rows,queue,config,dict(key=str(number),alias=alias,arm=arm,attempt=attempt))
            journal.once('STARTED', str(number),attempt=attempt, alias=alias, arm=arm, input_hash=input_hash, input_tokens=token_count,
                         grid=[6,12,18], visual_tokens=324, processor_seconds=prep_seconds)
            # This line is the actual new call, never reused or retried.
            t = time.monotonic()
            diag.set('QWEN_GENERATE')
            with torch.inference_mode():
                output = model.generate(**values, max_new_tokens=64, do_sample=False)
            torch.cuda.synchronize()
            generated = output[0, token_count:].detach().cpu().tolist()
            raw = qp.tokenizer.decode(generated, skip_special_tokens=True)
            require(len(raw.encode()) <= 8192, 'REPLY_BYTES')
            prediction = raw.strip() if raw.strip() in ('A','B','C','D','E') else None
            journal.write('reply-%02d-private.json' % number, dict(raw=raw, prediction=prediction))
            journal.once('TERMINAL', str(number),attempt=attempt, alias=alias, arm=arm, state='RETURNED' if prediction else 'INVALID',
                         prediction=prediction, tokens=len(generated), eos=bool(generated and generated[-1] in eos),
                         truncated=len(generated)>=64 and (not generated or generated[-1] not in eos), generate_seconds=time.monotonic()-t)
            guard(); del values, output, generated, raw
        result.update(status='COMPLETE', stage='COMPLETE', costs=costs,
                      cd_tensor_equal={a: bindings.get((a,'C')) == bindings.get((a,'D')) for a in selections})
    except Exception as error:
        result['diagnostic']=diag.error(error)
        result['stage']=diag.stage
        result.update(reason=str(error) if isinstance(error, ValueError) and str(error).isupper() else type(error).__name__)
        journal.add('WORKER_FAILURE',attempt=attempt,stage=result['stage'],reason=result['reason'])
    finally:
        result['gpu_worker_seconds'] = time.monotonic()-start
        if torch is not None:
            try:
                result['peak_allocated'] = torch.cuda.max_memory_allocated(0)
                result['peak_reserved'] = torch.cuda.max_memory_reserved(0)
            except Exception:
                pass
        journal.write('worker-%d-result.json'%attempt, result)
        journal.close()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('root');parser.add_argument('mode',choices=['bootstrap','gpu']);parser.add_argument('attempt',type=int);parser.add_argument('policy',type=int);args = parser.parse_args()
    sys.stdin.readline()  # Own parent Job assigned, original annotation locked.
    if args.mode=='bootstrap':bootstrap(args.root,args.attempt,args.policy)
    else:worker(args.root,args.attempt,args.policy)


if __name__ == '__main__':
    main()
