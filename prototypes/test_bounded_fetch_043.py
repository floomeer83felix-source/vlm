"""043 logic checks, frozen fault driver, independent post-exit verifier.

The independent oracle reads raw fixture calls and journal bytes. It never uses
worker-return.json or the component's replay state as its expected truth.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bounded_fetch_043 as c

def logic(root):
    root=Path(root);passed=[];network_guard=c.guard()
    def check(name,x):c.require(x,name);passed.append(name)
    def rejects(name,fn):
        try:fn()
        except ValueError:passed.append(name);return
        raise AssertionError(name)
    check('normal_length',c.validated([('Content-Length','32768')])['length']==32768)
    for name,headers in [('missing',[]),('negative',[('Content-Length','-1')]),('encoding',[('Content-Length','1'),('Content-Encoding','gzip')]),('duplicate',[('Content-Length','1'),('content-length','1')]),('transfer',[('Content-Length','1'),('Transfer-Encoding','chunked')]),('large',[('Content-Length','65537')])]:rejects(name,lambda h=headers:c.validated(h))
    trace=c.Trace(root);j=c.Journal(root/'logic.jsonl','LOGIC',trace);j.append('HEAD_VALIDATED',length=32768,etag='owned',encoding='identity')
    with open(root/'logic.jsonl','ab') as f:f.write(b'{"half":')
    replay=c.replay(root/'logic.jsonl');check('half_prefix_preserves_head',replay['journal_unknown'] and replay['head']['length']==32768)
    with open(root/'logic-sequence.jsonl','wb') as f:f.write(c.encoded(dict(body=dict(seq=2,event='HEAD_VALIDATED',previous='0'*64),sha256='x'))+b'\n')
    check('missing_sequence_unknown',c.replay(root/'logic-sequence.jsonl')['journal_unknown'])
    config=dict(work_deadline=123.0,remaining=1,prior_reserved=0)
    check('claim_once',c.claim(root,'logical',config,trace) is not None and c.claim(root,'logical',config,trace) is None)
    c.stop_run(root,'TEST_UNKNOWN');check('stop_prevents_next',c.claim(root,'new',config,trace) is None)
    check('fixed_absolute_deadline',config['work_deadline']==123.0)
    # Real lifecycle with too-small shared budget: fake HEAD only, never GET/read.
    budget=root/'budget';budget.mkdir();t=c.Trace(budget)
    c.execute(budget,'first',c.FakeTransport('LOGIC',t),dict(config,work_deadline=time.monotonic()+5))
    events=[json.loads(x)['event'] for x in t.path.read_bytes().splitlines()]
    check('shared_budget_no_get',events.count('HEAD_SEND')==1 and 'GET_SEND' not in events and 'READ_ENTER' not in events)
    c.exclusive(root/'logic-result.json',dict(status='PASS',assertions=passed,guard=network_guard))

def raw_prefix(path):
    """Independent decoder, intentionally not c.replay or a cached status."""
    records=[];prev='0'*64;damaged=False
    if not path.exists():return records,True
    for line in path.read_bytes().splitlines(keepends=True):
        if not line.endswith(b'\n'):damaged=True;break
        try:
            item=json.loads(line);b=item['body'];canonical=json.dumps(b,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
            if b['seq']!=len(records)+1 or b['previous']!=prev or hashlib.sha256(canonical).hexdigest()!=item['sha256']:raise ValueError('CHAIN')
        except (ValueError,TypeError,KeyError):damaged=True;break
        records.append(b);prev=item['sha256']
    return records,damaged

def verify(root,target):
    root=Path(root);rows=[];network_guard=c.guard();timings=c.read(root/'matrix-times.json')
    for case in c.CASES:
        directory=root/case
        if not (directory/'supervisor.json').exists():rows.append(dict(case=case,run_id='initial',status='NOT_RUN'));continue
        s=c.read(directory/'supervisor.json');z=c.read(directory/'closure-observed.json');assert s['active']==0
        z['finished_write_returned']=timings[case]['controlled_finished'];z['deadline_violation']=timings[case]['deadline_violation']
        events,bad=raw_prefix(directory/'first.jsonl');trace=[json.loads(x) for x in (directory/'fixture-trace.jsonl').read_bytes().splitlines()]
        core=c.replay(directory/'first.jsonl');guard=c.read(directory/'guard.json');names=[e['event'] for e in trace]
        head=next((e for e in events if e['event']=='HEAD_VALIDATED'),None)
        rawhead=next((e for e in events if e['event']=='HEAD_RESULT'),None);rawget=next((e for e in events if e['event']=='GET_RESULT'),None)
        reservations=[e['single_reserved'] for e in events if e['event']=='RESERVE'];upper=max(reservations,default=0)
        lower=max((e['written_fsynced'] for e in events if e['event']=='PROGRESS'),default=0)
        received=sum(e['size'] for e in trace if e['event']=='READ_RETURN');returns=names.count('READ_RETURN');heads=names.count('HEAD_SEND');gets=names.count('GET_SEND');reads=names.count('READ_ENTER')
        failures=[]
        def check(name,ok):
            if not ok:failures.append(name)
        check('replay_prefix',core['lower']==lower and core['upper']==upper and core['journal_unknown']==bad)
        check('actual_guard',guard['installed'] and guard['actual_sockets']==0 and len(guard['blocked_negative_attempts'])==3)
        check('timing',not z['deadline_violation'] and s['active0']<=s['active0_deadline'] and z['finished_write_returned']<=s['finish_deadline'])
        check('memory_members',s['peak_commit']<=512*1024**2 and s['max_active']<=3)
        if case!='F02':check('head_recovered',head is not None and head['length']==32768 and head['etag']=='"owned-043-v1"')
        if case in ('F01','F11'):
            complete=next((e for e in events if e['event']=='COMPLETE'),None)
            check('normal_complete',received==lower==upper==32768 and complete is not None and complete['sha256']==hashlib.sha256(c.PAYLOAD).hexdigest())
            check('body_digest',hashlib.sha256((directory/'first.body').read_bytes()).hexdigest()==hashlib.sha256(c.PAYLOAD).hexdigest())
        elif case in ('F02','F03','F04','F05','F10'):
            check('real_timeout',s['killed'] and s['kill_requested'] is not None and s['work_deadline']-.1<=s['kill_requested']<=s['work_deadline'])
            check('not_complete',not any(e['event']=='COMPLETE' for e in events))
        if case=='F02':check('connect_block',names.count('CONNECT')==1 and heads==gets==reads==0)
        if case=='F03':check('before_get',heads==1 and gets==reads==0 and 'BEFORE_GET_BLOCK' in names)
        if case=='F04':check('blocked_first_read',gets==reads==1 and received==lower==0 and upper==32768 and core['exactness']=='UNKNOWN_PENDING_BODY')
        if case=='F05':check('progress_no_extension',received>0 and lower<=received<=upper==32768 and s['last_activity']>s['start']+1)
        if case=='F06':check('no_finally',s['exitcode']==17 and received==4096 and lower==0 and upper==32768)
        if case=='F07':check('half_line',s['exitcode']==19 and bad and received==4096 and lower==0 and upper==32768)
        if case=='F08':check('fsync_stop',names.count('FSYNC_FAILED')==1 and gets==reads==0 and upper==32768)
        if case=='F09':
            check('mismatch_no_read',heads==gets==1 and reads==0 and rawhead is not None and rawget is not None and dict(rawhead['headers'])['Content-Length']=='32768' and dict(rawget['headers'])['Content-Length']=='32769')
            check('mismatch_stops',(directory/'run.stop').exists())
        if case=='F10':check('logging_block','FSYNC_BLOCK' in names and gets==reads==0)
        if case=='F11':check('duplicate_no_send',names.count('DUPLICATE_REJECTED')==1 and heads==gets==1)
        if case=='F12':check('unknown_then_next_block',names.count('READ_ERROR')==1 and names.count('NEXT_OBJECT_REJECTED')==1 and not any(e.get('object')=='SECOND' and e['event'] in ('CONNECT','HEAD_SEND','GET_SEND','READ_ENTER') for e in trace) and upper==32768 and (directory/'run.stop').exists())
        if case not in ('F01','F11'):check('run_stopped',(directory/'run.stop').exists())
        rows.append(dict(case=case,run_id='initial',status='PASS' if not failures else 'FAIL',failed_assertions=';'.join(failures),start=s['start'],work_deadline=s['work_deadline'],last_activity=s['last_activity'],kill_requested=s['kill_requested'],active0=s['active0'],finished=z['finished_write_returned'],exitcode=s['exitcode'],wall=z['finished_write_returned']-s['start'],job_user=s['user_seconds'],job_kernel=s['kernel_seconds'],peak_commit=s['peak_commit'],max_active=s['max_active'],active=s['active'],killed=s['killed'],head_recovered=bool(head),head_length=head['length'] if head else '',head_etag=head['etag'] if head else '',get_declared_length=dict(rawget['headers']).get('Content-Length') if rawget else '',fake_heads=heads,fake_gets=gets,fake_read_calls=reads,fake_read_returns=returns,fixture_received=received,persisted_lower=lower,responsibility_upper=upper,exactness=core['exactness'],journal_unknown=bad,replay_state=core['state'],run_stopped=(directory/'run.stop').exists(),duplicate_rejected=names.count('DUPLICATE_REJECTED'),next_rejected=names.count('NEXT_OBJECT_REJECTED'),guard_blocked=len(guard['blocked_negative_attempts']),real_network=0))
    fields=list(dict.fromkeys(key for row in rows for key in row))
    with open(target,'x',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    c.exclusive(root/'verification.json',dict(rows=len(rows),passed=sum(x['status']=='PASS' for x in rows),failed=[x for x in rows if x['status']=='FAIL'],not_run=sum(x['status']=='NOT_RUN' for x in rows),guard=network_guard))

def matrix(root):
    root=Path(root);timings={};c.exclusive(root/'matrix-guard.json',c.guard())
    for case in c.CASES:
        receipt=c.run_case(root/case,case)
        timings[case]=dict(controlled_finished=receipt['controlled_finished'],deadline_violation=receipt['deadline_violation'])
        if receipt['active'] or receipt['deadline_violation']:
            c.exclusive(root/'matrix.stop',dict(case=case,reason='SUPERVISION_FAILURE'));break
    c.exclusive(root/'matrix-times.json',timings)

if __name__=='__main__':
    role,root,*args=sys.argv[1:]
    if role=='logic':logic(root)
    elif role=='matrix':matrix(root)
    elif role=='verify':verify(root,args[0])
    else:raise ValueError('ROLE')
