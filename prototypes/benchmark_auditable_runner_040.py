"""040 fixed Windows fault harness and independent external observer.

No F validator is called to judge oracle correctness. This is CPU SHA work,
not model inference. All generated faults concern only the new supplied root.
"""
import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time


def sibling(name):
    path=Path(__file__).with_name(name+'.py');spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module


r=sibling('auditable_runner_040')
FAMILIES=('N1K','N64K','N1M','INPUT_DRIFT','DUP_ACTIVE','CRASH_AFTER_WORK','RECEIPT_MISMATCH','EARLY_SCORE','DESCENDANT_ALIVE')
SIZES={f:(65536 if f=='N64K' else 1048576 if f=='N1M' else 1024) for f in FAMILIES}
FILES=('auditable_runner_040.py','benchmark_auditable_runner_040.py','test_auditable_runner_040.py')
FIELDS=('case','family','rep','profile','phase','attempted','planned_requests','actual_requests','work_dispatched','work_entered','work_completed',
        'terminal','injection','violation_count','violation_types','duplicate_extra','legal_completion','work_without_terminal',
        'consumed_unrecoverable','consumed_zero_work','group_zero','outer_fallback','outer_kill','wall_seconds','work_wall_seconds',
        'job_user_seconds','job_kernel_seconds','scheduler_cpu_seconds','peak_commit_bytes','output_bytes','requests_json',
        'score_requests_json','worker_exits_json','evidence_json','error','plan_hash')


class SafetyStop(RuntimeError):pass


def payload(family,rep):return hashlib.shake_256(('VLM-040/v1/%s/%d'%(family,rep)).encode()).digest(SIZES[family])
def expected_sha(raw):return hashlib.sha256(raw).hexdigest()


def fixed_queue():
    result=[]
    for rep in range(10):
        for j,family in enumerate(FAMILIES):
            k=(rep+j)%6;profiles=r.PROFILES[k:]+r.PROFILES[:k]
            for profile in profiles:result.append(dict(case=len(result),family=family,rep=rep,profile=profile))
    return result


def run_case(case,store,family,rep,profile,phase='FORMAL',watchdog=5):
    """Actual fault orchestration. Oracle checks never invoke r.validate_receipt."""
    begin=time.perf_counter();deadline=time.monotonic()+watchdog;case=Path(case);store=Path(store)
    case.mkdir();raw=payload(family,rep);original=expected_sha(raw)
    with open(case/'payload.bin','xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    plan=dict(key='%s/%d'%(family,rep),family=family,rep=rep,code=expected_sha(Path(r.__file__).read_bytes()),
              config=hashlib.sha256(json.dumps(r.WORK_CONFIG,sort_keys=True,separators=(',',':')).encode()).hexdigest(),payload_hash=original)
    plan['manifest']=hashlib.sha256(json.dumps(plan,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    r.atomic(case/'plan.json',plan)
    job=r.Job(active_limit=3);workers=[];schedulers=[];scheduler_jobs=[];requests=[];scores=[];exits=[]
    evidence={};receipt=None;fault_delivered=family.startswith('N');fallback=False;error='';group_stats=None;claimed=False
    def request(number):
        nonlocal claimed
        sj=r.Job(active_limit=1);scheduler_jobs.append(sj)
        output=case/('request-%d.json'%number)
        process=r.Process(r.command('dispatch',case/'plan.json',store,profile,output),case/('scheduler-%d.log'%number),sj)
        schedulers.append(process);code=process.wait(deadline-.2)
        r.require(sj.empty(deadline-.1),'SCHEDULER_NOT_EMPTY')
        value=r.read(output) if output.exists() else dict(state='NO_RESPONSE')
        item=dict(request=number,state=value['state'],exit=code,at=time.perf_counter()-begin)
        requests.append(item);claimed=claimed or (value['state']=='DISPATCH' and r.POLICIES[profile]['consume'])
        return value['state']
    def launch(number):
        process=r.Process(r.command('worker',case/'plan.json',case,number),case/('worker-%d.log'%number),job)
        workers.append(process)
        r.wait_file(case/('oracle-entry-%d.json'%number),deadline-.2)
        return process
    def entries():
        return [r.read(case/('oracle-entry-%d.json'%n)) for n in range(1,len(workers)+1) if (case/('oracle-entry-%d.json'%n)).exists()]
    def offer(label,delivered,direct):
        # Independent OS snapshot and expected digest, not the scheme validator.
        active=job.active();running=direct.poll() is None;entered=len(entries())
        before=time.perf_counter()-begin
        outcome=r.admit(plan,delivered,profile,store,direct,job)
        violations=[]
        if outcome['admitted']:
            if delivered.get('payload_hash')!=original:violations.append('INPUT_BINDING')
            if delivered.get('result')!=original:violations.append('RESULT_INCORRECT')
            if any(delivered.get(k)!=plan[k] for k in ('key','code','config','manifest')):violations.append('RECEIPT_BINDING')
            if entered>1:violations.append('DUPLICATE_EXECUTION')
            if active>0 or running:violations.append('PROCESS_STILL_ALIVE')
        record=dict(request=label,admitted=outcome['admitted'],reason=outcome['reason'],group_active=active,
                    direct_running=running,work_entered=entered,at=before,violations=violations)
        scores.append(record)
        r.trace(store,plan,profile,'SCORE_DECISION',decision=record,
                actual_payload=delivered.get('payload_hash') if delivered else None)
        return outcome['admitted']
    try:
        state=request(1)
        if state!='DISPATCH':error='INITIAL_'+state
        else:
            first=launch(1)
            if family=='INPUT_DRIFT':
                prior_live=first.poll() is None
                changed=raw[:-1]+bytes([raw[-1]^1]);after=expected_sha(changed)
                with open(case/'payload.bin','r+b') as f:f.seek(-1,os.SEEK_END);f.write(changed[-1:]);f.flush();os.fsync(f.fileno())
                evidence.update(before_hash=original,after_hash=after,last_before=raw[-1],last_after=changed[-1],held_before_change=prior_live)
                r.signal(case/'release-work')
            elif family=='DUP_ACTIVE':
                held=first.poll() is None;entry=r.read(case/'oracle-entry-1.json')
                state2=request(2);second=None
                if state2=='DISPATCH':second=launch(2)
                fault_delivered=held and first.poll() is None and requests[1]['at']>entry['entered']-begin
                evidence.update(first_entered_before_second_request=fault_delivered,first_alive_before_release=first.poll() is None,
                                second_request_state=state2)
                r.signal(case/'release-work')
            elif family=='CRASH_AFTER_WORK':
                code=first.wait(deadline-.3);complete=case/'oracle-complete-1.json'
                fault_delivered=code==17 and complete.exists() and not (case/'receipt-1.json').exists()
                evidence.update(first_exit=code,work_complete_before_recovery=complete.exists(),first_receipt_absent=not (case/'receipt-1.json').exists())
                state2=request(2);evidence['recovery_state']=state2
                if state2=='DISPATCH':launch(2)
            if family=='EARLY_SCORE':
                r.wait_file(case/'receipt-1.json',deadline-.2);receipt=r.read(case/'receipt-1.json')
                before=first.poll() is None;admitted=offer('EARLY',receipt,first)
                fault_delivered=before and first.poll() is None
                evidence.update(early_direct_alive=before,still_alive_after_decision=first.poll() is None,
                                decision_before_release=True)
                r.signal(case/'release-work')
            elif family=='DESCENDANT_ALIVE':
                first.wait(deadline-.3);r.wait_file(case/'desc-1.json',deadline-.2)
                registration=r.read(case/'desc-1.json');desc=r.Process.registered(registration['pid'],job)
                try:
                    before=first.poll()==0 and desc.poll() is None and job.active()>0
                    receipt=r.read(case/'receipt-1.json');offer('EARLY_DESCENDANT',receipt,first)
                    fault_delivered=before and desc.poll() is None
                    evidence.update(parent_exited=first.poll()==0,descendant_owned_job=True,descendant_alive_at_request=before,
                                    descendant_alive_after_decision=desc.poll() is None,decision_before_release=True)
                    fallback=not r.POLICIES[profile]['group_exit'] and before
                    r.signal(case/'release-desc')
                finally:desc.close()
            for index,process in enumerate(workers,1):
                code=process.wait(deadline-.15);exits.append(code)
                location=case/('receipt-%d.json'%index)
                if location.exists():receipt=r.read(location)
                r.trace(store,plan,profile,'WORKER_TERMINAL',invocation=index,exit_code=code,
                        state='RETURNED' if code==0 and location.exists() else 'UNKNOWN',
                        receipt=receipt if location.exists() else None)
            if not job.empty(deadline-.1):
                fallback=True;job.kill();r.require(job.empty(deadline),'WORK_GROUP_CLEANUP_FAILED')
            if family=='INPUT_DRIFT':
                complete=r.read(case/'oracle-complete-1.json')
                fault_delivered=bool(evidence['held_before_change'] and complete['payload_hash']==evidence['after_hash']!=original)
                evidence['actual_read_hash']=complete['payload_hash']
            if family=='RECEIPT_MISMATCH' and receipt is not None:
                before=receipt['code'];receipt=dict(receipt,code=('0' if before[0]!='0' else '1')+before[1:])
                r.atomic(case/'delivered-receipt.json',receipt)
                fault_delivered=receipt['code']!=before and len(receipt['code'])==64 and receipt['result']==original
                evidence.update(original_code=before,delivered_code=receipt['code'],numerical_result_unchanged=receipt['result']==original)
            if not any(x['admitted'] for x in scores):offer('FINAL',receipt,workers[-1])
            if any(x['admitted'] for x in scores) and receipt is not None and exits and exits[-1]==0:
                r.commit_success(store,plan,receipt,profile)
    except Exception as exc:
        error=type(exc).__name__+(':'+str(exc) if isinstance(exc,ValueError) and str(exc).isupper() else '')
    finally:
        if job.active():fallback=True;job.kill()
        # A failure to observe owned groups empty is fatal to all later cells.
        if not job.empty(time.monotonic()+min(.1,max(0,deadline-time.monotonic()))):
            job.close();raise SafetyStop('OWN_GROUP_EXIT_UNPROVEN')
        group_stats=job.snapshot();job.close()
        scheduler_stats=[]
        for sj in scheduler_jobs:
            if sj.active():sj.kill();fallback=True
            if not sj.empty(time.monotonic()+.05):sj.close();raise SafetyStop('SCHEDULER_EXIT_UNPROVEN')
            scheduler_stats.append(sj.snapshot());sj.close()
        for process in workers+schedulers:process.close()
    actual_entries=entries();complete=[]
    for n in range(1,len(workers)+1):
        path=case/('oracle-complete-%d.json'%n)
        if path.exists():complete.append(r.read(path))
    violations=[v for x in scores for v in x['violations']]
    accepted=any(x['admitted'] for x in scores)
    legal=accepted and not violations and len(actual_entries)==1 and not error
    if error:terminal='FAILED'
    elif violations:terminal='VIOLATION'
    elif legal:terminal='RETURNED'
    elif family=='CRASH_AFTER_WORK' and complete and receipt is None:terminal='UNKNOWN'
    else:terminal='REJECTED'
    summary=dict(case=plan['key'],family=family,rep=rep,profile=profile,phase=phase,attempted=True,
                 planned_requests=2 if family in ('DUP_ACTIVE','CRASH_AFTER_WORK') else 1,
                 actual_requests=len(requests),work_dispatched=len(workers),work_entered=len(actual_entries),work_completed=len(complete),
                 terminal=terminal,injection='NOT_APPLICABLE' if family.startswith('N') else 'DELIVERED' if fault_delivered else 'INJECTION_NOT_DELIVERED',
                 violation_count=sum(bool(x['violations']) for x in scores),violation_types=sorted(set(violations)),
                 duplicate_extra=max(0,len(actual_entries)-1),legal_completion=legal,
                 work_without_terminal=sum(1 for n in range(1,len(workers)+1) if (case/('oracle-complete-%d.json'%n)).exists() and not (case/('receipt-%d.json'%n)).exists()),
                 consumed_unrecoverable=bool(complete and receipt is None and evidence.get('recovery_state') in ('CONSUMED','UNKNOWN_CLAIM')),
                 consumed_zero_work=bool(claimed and not actual_entries),group_zero=True,outer_fallback=fallback,outer_kill=group_stats['killed'],
                 wall_seconds=time.perf_counter()-begin,work_wall_seconds=sum(x['worker_wall'] for x in complete),
                 job_user_seconds=group_stats['user_seconds'],job_kernel_seconds=group_stats['kernel_seconds'],
                 scheduler_cpu_seconds=sum(x['user_seconds']+x['kernel_seconds'] for x in scheduler_stats),peak_commit_bytes=group_stats['peak_commit'],
                 output_bytes=sum(p.stat().st_size for p in case.iterdir() if p.is_file()),requests_json=requests,score_requests_json=scores,
                 worker_exits_json=exits,evidence_json=evidence,error=error,plan_hash=plan['manifest'])
    r.atomic(case/'case-summary.json',summary)
    require_wall=time.perf_counter()-begin
    if require_wall>watchdog:summary['error']='CELL_WATCHDOG_EXCEEDED';summary['terminal']='FAILED'
    return summary


def csv_row(value):
    return {k:json.dumps(value[k],sort_keys=True,separators=(',',':')) if isinstance(value.get(k),(list,dict)) else value.get(k,'') for k in FIELDS}


def output_totals(roots):
    files=0;size=0
    for root in roots:
        for directory,dirs,names in os.walk(root,followlinks=False):
            for name in dirs+names:
                st=(Path(directory)/name).lstat();r.require(not st.st_file_attributes&0x400,'OUTPUT_REPARSE')
            for name in names:files+=1;size+=(Path(directory)/name).stat().st_size
    r.require(files<=10000 and size<=128*r.MIB,'OUTPUT_QUOTA')
    return dict(files=files,bytes=size)


def planned_not_run(item,reason):
    row={k:0 for k in FIELDS};row.update(item,case='%s/%d'%(item['family'],item['rep']),phase='FORMAL',
        terminal='NOT_RUN',injection='NOT_RUN',violation_types=[],requests_json=[],score_requests_json=[],worker_exits_json=[],
        evidence_json={},error=reason,group_zero='UNKNOWN',plan_hash='',planned_requests=2 if item['family'] in ('DUP_ACTIVE','CRASH_AFTER_WORK') else 1)
    return row


def frozen_run(root,mode='formal'):
    root=Path(root);root.mkdir();stores=root/'stores';stores.mkdir();initialization={}
    for profile in r.PROFILES:initialization[profile]=r.initialize_store(stores/profile,profile)
    if mode=='formal':items=fixed_queue();limit=885
    else:items=[dict(family=f,rep=0,profile=p) for f in ('N1K','CRASH_AFTER_WORK') for p in r.PROFILES];limit=100
    hashes={name:expected_sha(Path(__file__).with_name(name).read_bytes()) for name in FILES}
    r.atomic(root/'planned.json',items);r.atomic(root/'seal.json',dict(source_hashes=hashes,queue_hash=r.digest(items),
        workload=r.WORK_CONFIG,profiles=r.POLICIES,watchdog=5,case_loop_seconds=limit,formal_work_entry_cap=720,phase=mode))
    with open(root/'once.lock','xb') as f:f.write(b'ONE_FORMAL_RUN' if mode=='formal' else b'ONE_CLEAN_REPRO')
    rows=[];begin=time.monotonic();stop=None
    with open(root/'rows.csv','x',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS);writer.writeheader()
        for i,item in enumerate(items):
            if not stop and (time.monotonic()-begin+5>limit):stop='BENCHMARK_WINDOW'
            if not stop and any(expected_sha(Path(__file__).with_name(name).read_bytes())!=h for name,h in hashes.items()):stop='SEALED_SOURCE_CHANGED'
            if stop:row=planned_not_run(item,stop)
            else:
                try:row=run_case(root/('case-%03d'%i),stores/item['profile'],item['family'],item['rep'],item['profile'],'FORMAL' if mode=='formal' else 'CLEAN')
                except SafetyStop as error:
                    stop=str(error);row=planned_not_run(item,'SAFETY_STOP_DURING_CASE')
                    row.update(attempted=True,terminal='UNKNOWN',injection='UNKNOWN',work_entered=None,work_completed=None,work_dispatched=None)
            rows.append(row);writer.writerow(csv_row(row));f.flush();os.fsync(f.fileno())
            if sum(x['work_entered'] or 0 for x in rows)>720:stop='WORK_ENTRY_CAP'
            if i%30==0:print(json.dumps(dict(progress=i+1,planned=len(items),phase=mode)),flush=True)
    summary=dict(mode=mode,planned=len(items),seconds=time.monotonic()-begin,initialization_seconds=initialization,
                 stop_reason=stop,work_entered=sum(x['work_entered'] or 0 for x in rows),source_hashes=hashes,
                 queue_hash=r.digest(items),forbidden_imports=[x for x in sys.modules if x.split('.')[0] in ('torch','numpy','transformers','development_pilot_030','clock_binding_probe_038')])
    r.atomic(root/'summary.json',summary);print(json.dumps(summary),flush=True)


def clean_run(root):
    root=Path(root);begin=time.monotonic();children=[]
    for name in FILES:
        group=r.Job(active_limit=1)
        process=r.Process([sys.executable,'-I','-S','-B',str(root/name),'--help'],root/(name+'.help.log'),group)
        try:
            code=process.wait(time.monotonic()+5);r.require(group.empty(time.monotonic()+.1),'CLEAN_HELP_EXIT')
            children.append(dict(action='help',module=name,exit=code,job=group.snapshot()))
        finally:process.close();group.close()
    group=r.Job()
    process=r.Process([sys.executable,'-I','-S','-B',str(root/'auditable_runner_040.py'),'demo','--root',str(root/'demo')],root/'demo.log',group)
    try:
        code=process.wait(time.monotonic()+6);r.require(group.empty(time.monotonic()+.1),'CLEAN_DEMO_EXIT')
        children.append(dict(action='demo',exit=code,job=group.snapshot()))
    finally:process.close();group.close()
    demo=json.loads((root/'demo.log').read_text());frozen_run(root/'matrix','reproduce')
    r.atomic(root/'clean-summary.json',dict(seconds=time.monotonic()-begin,children=children,demo=demo,
        source_hashes={name:expected_sha((root/name).read_bytes()) for name in FILES},
        forbidden_imports=[x for x in sys.modules if x.split('.')[0] in ('torch','numpy','transformers','development_pilot_030','clock_binding_probe_038')]))


def main():
    parser=argparse.ArgumentParser(description='Fixed040 CPU SHA fault benchmark, never model inference.')
    parser.add_argument('mode',choices=('formal','reproduce','clean'));parser.add_argument('--root',required=True)
    args=parser.parse_args()
    if args.mode=='clean':clean_run(args.root)
    else:frozen_run(args.root,args.mode)


if __name__=='__main__':main()
