"""043 offline request lifecycle core and independent Win32 deadline supervision.

Transport is explicitly injected; this delivery admits owned FakeTransport only.
No HTTP implementation, automatic retries, media scanner or model code.
Journal fsync covers the process-exit fault model, not power-loss durability.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import sys
import time

LIMIT=65536
TOTAL=98304
PAYLOAD=bytes((19+7*i)%256 for i in range(32768))
BLOCK=4096
CASES=tuple('F%02d'%i for i in range(1,13))

def require(ok,reason):
    if not ok:raise ValueError(reason)
def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(encoded(value)).hexdigest()
def read(path):return json.loads(Path(path).read_bytes())
def exclusive(path,value):
    data=encoded(value);require(len(data)<=16384,'CONTROL_FILE_CAP')
    with open(path,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def guard():
    def audit(event,args):
        if event.startswith('socket.') or event in ('os.system','subprocess.Popen','os.posix_spawn'):raise PermissionError('OFFLINE_043')
        if event=='import' and args[0].split('.')[0] in ('torch','av','transformers','numpy'):raise PermissionError('NO_ML_043')
    sys.addaudithook(audit)
    blocked=[]
    for name,fn in [('socket',lambda:socket.socket()),('resolve',lambda:socket.getaddrinfo('localhost',80)),('hostname',lambda:socket.gethostbyname('localhost'))]:
        try:fn()
        except PermissionError:blocked.append(name)
        else:raise AssertionError('GUARD_MISSED_'+name)
    return dict(installed=True,blocked_negative_attempts=blocked,actual_sockets=0)

def validated(headers):
    """Preserve multiplicity; duplicate critical headers are rejected, not collapsed."""
    fields={}
    for key,value in headers:
        key=key.lower();require(key not in fields,'DUPLICATE_HEADER');fields[key]=value
    length=fields.get('content-length','')
    require(length.isascii() and length.isdigit() and 0<int(length)<=LIMIT,'UNRELIABLE_LENGTH')
    require(fields.get('content-encoding','identity').lower()=='identity','CONTENT_ENCODING')
    require('transfer-encoding' not in fields,'TRANSFER_ENCODING')
    return dict(length=int(length),etag=fields.get('etag'),encoding=fields.get('content-encoding','identity'))

class Trace:
    def __init__(self,directory):self.path=Path(directory)/'fixture-trace.jsonl';self.count=0
    def event(self,event,**kw):
        self.count+=1;require(self.count<=200,'TRACE_CAP')
        data=encoded(dict(event=event,t=time.monotonic(),**kw))+b'\n';require(len(data)<=1024,'TRACE_LINE_CAP')
        with open(self.path,'ab') as f:f.write(data);f.flush();os.fsync(f.fileno())

class Journal:
    def __init__(self,path,case,trace):self.path=Path(path);self.case=case;self.trace=trace;self.seq=0;self.previous='0'*64
    def append(self,event,**data):
        self.seq+=1;require(self.seq<=256,'JOURNAL_EVENT_CAP')
        body=dict(seq=self.seq,event=event,t=time.monotonic(),previous=self.previous,**data);h=digest(body);line=encoded(dict(body=body,sha256=h))+b'\n';require(len(line)<=4096,'JOURNAL_LINE_CAP')
        with open(self.path,'ab') as f:
            if self.case=='F07' and event=='PROGRESS':
                f.write(line[:len(line)//2]);f.flush();os.fsync(f.fileno());self.trace.event('HALF_LOG_EXIT');os._exit(19)
            f.write(line);f.flush()
            if self.case=='F08' and event=='RESERVE':self.trace.event('FSYNC_FAILED',stage=event);raise OSError('INJECTED_FSYNC_FAILURE')
            if self.case=='F10' and event=='HEAD_VALIDATED':self.trace.event('FSYNC_BLOCK',stage=event);time.sleep(60)
            os.fsync(f.fileno())
        self.previous=h

class FakeTransport:
    """Owned, bounded bytes and observable calls; no real network anywhere."""
    def __init__(self,case,trace,name='FIRST'):self.case=case;self.trace=trace;self.name=name;self.cursor=0
    def connect(self):
        self.trace.event('CONNECT',object=self.name)
        if self.case=='F02':time.sleep(60)
    def head(self):
        self.trace.event('HEAD_SEND',object=self.name)
        return 200,[('Content-Length',str(len(PAYLOAD))),('ETag','"owned-043-v1"'),('Content-Encoding','identity')]
    def get(self):
        self.trace.event('GET_SEND',object=self.name)
        return 200,[('Content-Length',str(len(PAYLOAD)+(self.case=='F09'))),('ETag','"owned-043-v1"'),('Content-Encoding','identity')]
    def read(self,size):
        self.trace.event('READ_ENTER',object=self.name)
        if self.case=='F04':time.sleep(60)
        if self.case=='F12':self.trace.event('READ_ERROR',object=self.name);raise OSError('INJECTED_READ_INTERRUPTION')
        if self.case=='F05':time.sleep(.6);size=min(size,512)
        data=PAYLOAD[self.cursor:self.cursor+size];self.cursor+=len(data)
        self.trace.event('READ_RETURN',object=self.name,size=len(data),sha256=hashlib.sha256(data).hexdigest())
        return data

def stop_run(directory,reason):
    path=Path(directory)/'run.stop'
    if not path.exists():exclusive(path,dict(reason=reason))

def claim(directory,attempt,config,trace):
    directory=Path(directory)
    if (directory/'run.stop').exists():trace.event('NEXT_OBJECT_REJECTED',attempt=attempt);return None
    path=directory/(attempt+'.claim')
    try:exclusive(path,config)
    except FileExistsError:trace.event('DUPLICATE_REJECTED',attempt=attempt);return None
    return directory/(attempt+'.jsonl')

def execute(directory,attempt,transport,config):
    """Actual tested lifecycle; durable writes precede each transport side effect."""
    require(type(transport) is FakeTransport,'ONLY_FAKE_TRANSPORT_AUTHORIZED')
    directory=Path(directory);trace=transport.trace
    journal_path=claim(directory,attempt,config,trace)
    if journal_path is None:return 'REJECTED'
    journal=Journal(journal_path,transport.case,trace);written=0
    try:
        journal.append('CLAIM',attempt=attempt,source_ref='OWNED_FIXTURE_043',config=config)
        journal.append('HEAD_INTENT',method='HEAD',source_ref='OWNED_FIXTURE_043')
        transport.connect();status,headers=transport.head()
        journal.append('HEAD_RESULT',status=status,headers=headers)
        require(status==200,'HEAD_STATUS');head=validated(headers)
        require(head['length']<=config['remaining'],'SHARED_BUDGET')
        journal.append('HEAD_VALIDATED',**head)
        if transport.case=='F03':trace.event('BEFORE_GET_BLOCK');time.sleep(60)
        journal.append('RESERVE',single_reserved=head['length'],cumulative_reserved=config['prior_reserved']+head['length'],single_limit=LIMIT,total_limit=TOTAL)
        journal.append('GET_INTENT',method='GET',source_ref='OWNED_FIXTURE_043',reserved=head['length'])
        status,headers=transport.get();journal.append('GET_RESULT',status=status,headers=headers)
        actual=validated(headers);require(status==200 and head==actual,'GET_METADATA_MISMATCH')
        journal.append('GET_VALIDATED',**actual)
        sha=hashlib.sha256()
        with open(directory/(attempt+'.body'),'xb') as f:
            while written<head['length']:
                require(time.monotonic()<config['work_deadline'],'WORK_DEADLINE')
                block=transport.read(min(BLOCK,head['length']-written));require(bool(block),'SHORT_BODY')
                if transport.case=='F06':trace.event('READ_WITHOUT_PROGRESS_EXIT',size=len(block));os._exit(17)
                require(written+len(block)<=head['length'],'BODY_CAP')
                f.write(block);f.flush();os.fsync(f.fileno());written+=len(block);sha.update(block)
                journal.append('PROGRESS',read_returned=written,written_fsynced=written)
        journal.append('COMPLETE',bytes=written,sha256=sha.hexdigest());return 'COMPLETE'
    except OSError as e:
        stop_run(directory,'UNKNOWN_IO')
        # Persistence failure never allows a GET or a memory-only continuation.
        if 'FSYNC_FAILURE' not in str(e):journal.append('ABORT',reason='UNKNOWN_IO')
        return 'UNKNOWN'
    except ValueError as e:
        stop_run(directory,str(e));journal.append('ABORT',reason=str(e));return 'FAILED'

def replay(path):
    """Trusted prefix retained on half-line/hash/sequence error; no worker object."""
    path=Path(path);events=[];bad=False;previous='0'*64
    if path.exists():
        for line in path.read_bytes().splitlines(keepends=True):
            try:
                require(line.endswith(b'\n'),'HALF_LINE');record=json.loads(line);body=record['body']
                require(body['seq']==len(events)+1 and body['previous']==previous and record['sha256']==digest(body),'SEQUENCE_OR_HASH')
                events.append(body);previous=record['sha256']
            except (ValueError,KeyError,TypeError):bad=True;break
    head=next((x for x in events if x['event']=='HEAD_VALIDATED'),None)
    head_raw=next((x for x in events if x['event']=='HEAD_RESULT'),None)
    get_raw=next((x for x in events if x['event']=='GET_RESULT'),None)
    reserved=max((x['single_reserved'] for x in events if x['event']=='RESERVE'),default=0)
    lower=max((x['written_fsynced'] for x in events if x['event']=='PROGRESS'),default=0)
    get_intent=any(x['event']=='GET_INTENT' for x in events)
    complete=next((x for x in events if x['event']=='COMPLETE'),None)
    exact=bool(complete and not bad and complete['bytes']==lower)
    return dict(state='COMPLETE' if exact else 'UNKNOWN',journal_unknown=bad,head=head,head_raw=head_raw,get_raw=get_raw,lower=lower,upper=reserved,exactness='COMPLETE_APPLICATION_BODY' if exact else ('UNKNOWN_PENDING_BODY' if get_intent or bad else 'NO_GET_INTENT'),get_intent=get_intent,events=len(events),complete=complete)

def worker(directory,case,config):
    directory=Path(directory);exclusive(directory/'guard.json',guard());trace=Trace(directory)
    transport=FakeTransport(case,trace);result=execute(directory,'first',transport,read(config))
    if case=='F11':execute(directory,'first',FakeTransport(case,trace),read(config))
    if case=='F12':execute(directory,'second',FakeTransport(case,trace,'SECOND'),read(config))
    # Not consumed by independent verifier as truth; useful raw terminal evidence only.
    exclusive(directory/'worker-return.json',dict(result=result))

def platform():
    spec=importlib.util.spec_from_file_location('platform040',Path(__file__).with_name('auditable_runner_040.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def run_case(directory,case):
    """Critical wait has only monotonic/kernel Job queries/sleep; no disk I/O."""
    directory=Path(directory);require(not directory.exists(),'CASE_CONSUMED');directory.mkdir()
    t0=time.monotonic();work=t0+8;zero=t0+12;finish_limit=t0+15
    config=dict(start=t0,work_deadline=work,active0_deadline=zero,finish_deadline=finish_limit,remaining=TOTAL,prior_reserved=0,block=BLOCK,payload_size=len(PAYLOAD))
    exclusive(directory/'config.json',config)
    p=platform();job=p.Job(memory=512*1024**2,active_limit=2);child=None;kill=None;active0=None;error=None;max_active=0;exitcode=None
    try:
        child=p.Process([sys.executable,'-I','-S','-B',str(Path(__file__).resolve()),'worker',str(directory),case,str(directory/'config.json')],directory/'worker.log',job)
        while True:
            # Only owned kernel queries here: no quota scan/log/fsync/finally dependency.
            active=job.active();now=time.monotonic();max_active=max(max_active,active)
            if active==0:active0=now;break
            # Schedule the call 100ms before the hard8s ceiling, not after it.
            if now>=work-.1 and kill is None:kill=now;job.kill()
            if now>=zero:raise TimeoutError('ACTIVE0_DEADLINE')
            time.sleep(.002)
        exitcode=child.poll()
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if active0 is None:
            if kill is None:kill=time.monotonic();job.kill()
            if job.empty(zero):active0=time.monotonic()
        snapshot=job.snapshot()
        if child:child.close()
        job.close()
    require(active0 is not None and snapshot['active']==0,'OWNERSHIP_OR_DRAIN_UNKNOWN')
    current=replay(directory/'first.jsonl')
    if error or current['state']!='COMPLETE':stop_run(directory,'SUPERVISOR_INCOMPLETE')
    trace=[json.loads(x) for x in (directory/'fixture-trace.jsonl').read_bytes().splitlines()] if (directory/'fixture-trace.jsonl').exists() else []
    last=max((x['t'] for x in trace),default=None)
    receipt=dict(case=case,start=t0,work_deadline=work,active0_deadline=zero,finish_deadline=finish_limit,last_activity=last,kill_requested=kill,active0=active0,exitcode=exitcode,error=error,max_active=max_active,**snapshot)
    exclusive(directory/'supervisor.json',receipt)
    finished=time.monotonic();exclusive(directory/'closed.json',dict(finished=finished))
    after_close=time.monotonic()
    exclusive(directory/'closure-observed.json',dict(finished_write_returned=after_close,deadline_violation=bool((kill is not None and kill>work) or active0>zero or after_close>finish_limit)))
    receipt['controlled_finished']=time.monotonic()
    receipt['deadline_violation']=bool((kill is not None and kill>work) or active0>zero or receipt['controlled_finished']>finish_limit)
    return receipt

def main():
    role,*args=sys.argv[1:]
    if role=='worker':worker(args[0],args[1],args[2])
    else:raise ValueError('ROLE')

if __name__=='__main__':main()
