"""Standalone stdlib reference runner040; Windows process faults, not inference.

The worker/oracle writer is controlled, not a malicious-code attestation. No
historical research modules are imported. Claims cannot provide exactly-once.
"""
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time

MIB=1024**2
PROFILES=('B0','B1','F','F-NOBIND','F-NOCONSUME','F-NOEXIT')
POLICIES={name:dict(consume=name not in ('B0','F-NOCONSUME'),
                   bind=name not in ('B0','F-NOBIND'),group_exit=name not in ('B0','F-NOEXIT'),
                   sqlite=name=='B1') for name in PROFILES}
WORK_CONFIG=dict(version='VLM-040/v1',iterations=64,operation='sha256-original-bytes')


def require(ok,reason):
    if not ok:raise ValueError(reason)


def packed(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(value):return hashlib.sha256(packed(value)).hexdigest()
def read(path):return json.loads(Path(path).read_bytes())
def source_hash():return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def atomic(path,value):
    path=Path(path);temporary=path.with_name(path.name+'.writing')
    with open(temporary,'xb') as f:f.write(packed(value)+b'\n');f.flush();os.fsync(f.fileno())
    os.replace(temporary,path)


def signal(path):
    with open(path,'xb') as f:f.write(b'1');f.flush();os.fsync(f.fileno())


def wait_file(path,deadline):
    while not Path(path).exists():
        if time.monotonic()>=deadline:raise TimeoutError('BARRIER_TIMEOUT')
        time.sleep(.001)


class Basic(C.Structure):
    _fields_=[('process_time',C.c_int64),('job_time',C.c_int64),('flags',W.DWORD),
              ('min_ws',C.c_size_t),('max_ws',C.c_size_t),('active_limit',W.DWORD),
              ('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]
class IO(C.Structure):
    _fields_=[(n,C.c_uint64) for n in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]
class Extended(C.Structure):
    _fields_=[('basic',Basic),('io',IO),('process_memory',C.c_size_t),('job_memory',C.c_size_t),
              ('peak_process',C.c_size_t),('peak_job',C.c_size_t)]
class Accounting(C.Structure):
    _fields_=[('user',C.c_int64),('kernel',C.c_int64),('period_user',C.c_int64),('period_kernel',C.c_int64),
              ('faults',W.DWORD),('total',W.DWORD),('active',W.DWORD),('terminated',W.DWORD)]
class Startup(C.Structure):
    _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
              ('x',W.DWORD),('y',W.DWORD),('xsize',W.DWORD),('ysize',W.DWORD),('xchars',W.DWORD),
              ('ychars',W.DWORD),('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('reserved_size',W.WORD),
              ('reserved_ptr',C.POINTER(C.c_byte)),('stdin',W.HANDLE),('stdout',W.HANDLE),('stderr',W.HANDLE)]
class ProcessInfo(C.Structure):
    _fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]


def kernel():
    require(os.name=='nt','WINDOWS_ONLY')
    api=C.WinDLL('kernel32',use_last_error=True)
    signatures={
      'CreateJobObjectW':([W.LPVOID,W.LPCWSTR],W.HANDLE),
      'SetInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD],W.BOOL),
      'QueryInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD,W.LPVOID],W.BOOL),
      'AssignProcessToJobObject':([W.HANDLE,W.HANDLE],W.BOOL),
      'TerminateJobObject':([W.HANDLE,W.UINT],W.BOOL),
      'CloseHandle':([W.HANDLE],W.BOOL),
      'CreateProcessW':([W.LPCWSTR,W.LPWSTR,W.LPVOID,W.LPVOID,W.BOOL,W.DWORD,W.LPVOID,W.LPCWSTR,C.POINTER(Startup),C.POINTER(ProcessInfo)],W.BOOL),
      'ResumeThread':([W.HANDLE],W.DWORD),
      'GetExitCodeProcess':([W.HANDLE,C.POINTER(W.DWORD)],W.BOOL),
      'TerminateProcess':([W.HANDLE,W.UINT],W.BOOL),
      'OpenProcess':([W.DWORD,W.BOOL,W.DWORD],W.HANDLE),
      'IsProcessInJob':([W.HANDLE,W.HANDLE,C.POINTER(W.BOOL)],W.BOOL)}
    for name,(args,ret) in signatures.items():getattr(api,name).argtypes=args;getattr(api,name).restype=ret
    return api


class Job:
    def __init__(self,memory=512*MIB,active_limit=0):
        self.api=kernel();self.handle=self.api.CreateJobObjectW(None,None);require(self.handle,'JOB_CREATE')
        limits=Extended();limits.basic.flags=0x2000|0x100|0x200
        if active_limit:limits.basic.flags|=0x8;limits.basic.active_limit=active_limit
        limits.process_memory=limits.job_memory=memory
        require(self.api.SetInformationJobObject(self.handle,9,C.byref(limits),C.sizeof(limits)),'JOB_LIMITS')
        self.killed=False
    def assign(self,process):require(self.api.AssignProcessToJobObject(self.handle,process.handle),'JOB_ASSIGN')
    def snapshot(self):
        a=Accounting();e=Extended()
        require(self.api.QueryInformationJobObject(self.handle,1,C.byref(a),C.sizeof(a),None),'JOB_ACCOUNT')
        require(self.api.QueryInformationJobObject(self.handle,9,C.byref(e),C.sizeof(e),None),'JOB_MEMORY')
        return dict(active=a.active,total_processes=a.total,user_seconds=a.user/1e7,kernel_seconds=a.kernel/1e7,
                    peak_commit=e.peak_job,killed=self.killed)
    def active(self):return self.snapshot()['active']
    def empty(self,deadline):
        while self.active():
            if time.monotonic()>=deadline:return False
            time.sleep(.001)
        return True
    def kill(self):
        require(self.api.TerminateJobObject(self.handle,99),'OWN_JOB_TERMINATION');self.killed=True
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None


class Process:
    """CREATE_SUSPENDED -> assign Job -> ResumeThread, before Python user code."""
    def __init__(self,args,log,job=None):
        import msvcrt
        self.api=kernel();self.handle=None;self.pid=None
        si=Startup();si.cb=C.sizeof(si);si.flags=0x100
        pi=ProcessInfo();env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
        block=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
        command=C.create_unicode_buffer(subprocess.list2cmdline([str(x) for x in args]))
        with open(log,'xb') as output,open(os.devnull,'rb') as incoming:
            out=msvcrt.get_osfhandle(output.fileno());inp=msvcrt.get_osfhandle(incoming.fileno())
            os.set_handle_inheritable(out,True);os.set_handle_inheritable(inp,True)
            si.stdout=si.stderr=out;si.stdin=inp
            ok=self.api.CreateProcessW(None,command,None,None,True,0x08000000|0x4|0x400,block,None,C.byref(si),C.byref(pi))
            os.set_handle_inheritable(out,False);os.set_handle_inheritable(inp,False)
            require(ok,'CREATE_PROCESS_'+str(C.get_last_error()))
        self.handle,self.pid=pi.process,pi.pid
        try:
            if job is not None:job.assign(self)
            require(self.api.ResumeThread(pi.thread)!=0xffffffff,'RESUME_THREAD')
        except Exception:
            self.api.TerminateProcess(self.handle,98);raise
        finally:self.api.CloseHandle(pi.thread)
    @classmethod
    def registered(cls,pid,job):
        obj=cls.__new__(cls);obj.api=kernel();obj.pid=pid
        obj.handle=obj.api.OpenProcess(0x1000|0x100000,False,pid)
        require(obj.handle,'REGISTERED_PROCESS_OPEN')
        inside=W.BOOL();require(obj.api.IsProcessInJob(obj.handle,job.handle,C.byref(inside)) and inside.value,'REGISTERED_PROCESS_NOT_OWNED')
        return obj
    def poll(self):
        code=W.DWORD();require(self.api.GetExitCodeProcess(self.handle,C.byref(code)),'PROCESS_QUERY')
        return None if code.value==259 else code.value
    def wait(self,deadline):
        while self.poll() is None:
            if time.monotonic()>=deadline:raise TimeoutError('PROCESS_TIMEOUT')
            time.sleep(.001)
        return self.poll()
    def kill(self):require(self.api.TerminateProcess(self.handle,99),'OWN_PROCESS_TERMINATION')
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None


def command(role,*args):return [sys.executable,'-I','-S','-B',str(Path(__file__).resolve()),role]+[str(x) for x in args]


def connect(store):
    db=sqlite3.connect(str(Path(store)/'state.sqlite'),timeout=.5,isolation_level=None)
    db.execute('PRAGMA journal_mode=DELETE');db.execute('PRAGMA synchronous=FULL');db.execute('PRAGMA temp_store=MEMORY')
    return db


def initialize_store(store,profile):
    t=time.perf_counter();store=Path(store);store.mkdir()
    if profile=='B1':
        with connect(store) as db:
            db.execute('CREATE TABLE claims(key TEXT PRIMARY KEY,state TEXT NOT NULL,receipt TEXT)')
            db.execute('CREATE TABLE scores(key TEXT PRIMARY KEY)')
    return time.perf_counter()-t


def cache_path(store,key):return Path(store)/(hashlib.sha256(key.encode()).hexdigest()+'.result.json')


def claim(store,plan,profile):
    policy=POLICIES[profile];key=plan['key'];cached=cache_path(store,key)
    if cached.exists():
        try:prior=read(cached)
        except (ValueError,OSError):return 'UNKNOWN_CACHE'
        return 'CACHED' if validate_receipt(plan,prior,profile) is None else 'CACHE_MISMATCH'
    if not policy['consume']:return 'DISPATCH'
    if policy['sqlite']:
        db=connect(store)
        try:
            db.execute('BEGIN IMMEDIATE')
            db.execute('INSERT INTO claims VALUES(?,?,?)',(key,'STARTED',None));db.execute('COMMIT')
            return 'DISPATCH'
        except sqlite3.IntegrityError:
            db.execute('ROLLBACK');return 'CONSUMED'
        except sqlite3.OperationalError:
            if db.in_transaction:db.execute('ROLLBACK')
            return 'SQLITE_BUSY'
        finally:db.close()
    path=Path(store)/(hashlib.sha256(key.encode()).hexdigest()+'.claim')
    try:
        with open(path,'xb') as f:
            f.write(packed(dict(state='STARTED',key=key,code=plan['code'],config=plan['config'],manifest=plan['manifest']))+b'\n')
            f.flush();os.fsync(f.fileno())
        return 'DISPATCH'
    except FileExistsError:
        try:existing=read(path)
        except (ValueError,OSError):return 'UNKNOWN_CLAIM'
        return 'CONSUMED' if existing.get('state')=='STARTED' and existing.get('key')==key else 'UNKNOWN_CLAIM'


def dispatch(plan_path,store,profile,output):
    plan=read(plan_path)
    state=claim(store,plan,profile)
    atomic(output,dict(state=state,request_process=os.getpid(),at=time.perf_counter()))


def validate_receipt(plan,receipt,profile):
    if not isinstance(receipt,dict):return 'NO_RECEIPT'
    for key in ('key','code','config','manifest'):
        if receipt.get(key)!=plan[key]:return 'RECEIPT_'+key.upper()
    # All policies check consistency of the returned computation. Checking the
    # original expected digest here would duplicate the ablated payload check
    # because this workload's final result is SHA256(actual original bytes).
    if receipt.get('result')!=receipt.get('payload_hash'):return 'RESULT_INCONSISTENT'
    if POLICIES[profile]['bind'] and receipt.get('payload_hash')!=plan['payload_hash']:return 'PAYLOAD_MISMATCH'
    return None


def admit(plan,receipt,profile,store,direct,job):
    error=validate_receipt(plan,receipt,profile)
    if error:return dict(admitted=False,reason=error)
    code=direct.poll()
    if code not in (None,0):return dict(admitted=False,reason='DIRECT_FAILURE')
    if profile=='B0' and code is None:return dict(admitted=False,reason='DIRECT_NOT_EXITED')
    if POLICIES[profile]['group_exit'] and job.active()!=0:return dict(admitted=False,reason='GROUP_NOT_EXITED')
    if profile=='B1':
        db=connect(store)
        try:
            db.execute('BEGIN IMMEDIATE');db.execute('INSERT INTO scores VALUES(?)',(plan['key'],));db.execute('COMMIT')
        except sqlite3.IntegrityError:
            db.execute('ROLLBACK');return dict(admitted=False,reason='ALREADY_SCORED')
        except sqlite3.OperationalError:
            if db.in_transaction:db.execute('ROLLBACK')
            return dict(admitted=False,reason='SQLITE_BUSY')
        finally:db.close()
    else:
        path=Path(store)/(hashlib.sha256(plan['key'].encode()).hexdigest()+'.scored')
        try:
            with open(path,'xb') as f:f.write(b'1');f.flush();os.fsync(f.fileno())
        except FileExistsError:return dict(admitted=False,reason='ALREADY_SCORED')
    return dict(admitted=True,reason='ADMITTED')


def commit_success(store,plan,receipt,profile):
    atomic(cache_path(store,plan['key']),receipt)
    if profile=='B1':
        with connect(store) as db:
            db.execute('BEGIN IMMEDIATE');db.execute('UPDATE claims SET state=?,receipt=? WHERE key=?',
                      ('COMPLETE',json.dumps(receipt),plan['key']));db.execute('COMMIT')


def trace(store,plan,profile,event,**fields):
    """Per-key file evidence, rooted in the durable claim, one observer writer.

    No observer oracle payload is read here; only supplied receipt/lifecycle
    observations. This trace is not another pre-dispatch deduplication gate.
    """
    if not profile.startswith('F'):return
    stem=hashlib.sha256(plan['key'].encode()).hexdigest();path=Path(store)/(stem+'.jsonl')
    previous='0'*64;seq=0;claim_path=Path(store)/(stem+'.claim')
    if path.exists():
        lines=path.read_bytes().splitlines();last=json.loads(lines[-1]);previous=last['hash'];seq=len(lines)
    elif claim_path.exists():previous=hashlib.sha256(claim_path.read_bytes()).hexdigest()
    row=dict(seq=seq,prev=previous,key=plan['key'],code=plan['code'],config=plan['config'],event=event,**fields)
    row['hash']=digest(row)
    with open(path,'ab') as f:f.write(packed(row)+b'\n');f.flush();os.fsync(f.fileno())


def descendant(case,invocation):
    case=Path(case);begin=time.monotonic()
    atomic(case/('desc-%d.json'%invocation),dict(pid=os.getpid(),entered=time.perf_counter()))
    while not (case/'release-desc').exists() and time.monotonic()-begin<2:time.sleep(.001)


def worker(plan_path,case,invocation):
    case=Path(case);plan=read(plan_path);begin=time.perf_counter();deadline=time.monotonic()+4.5
    atomic(case/('oracle-entry-%d.json'%invocation),dict(pid=os.getpid(),entered=begin,invocation=invocation))
    if plan['family'] in ('INPUT_DRIFT','DUP_ACTIVE'):
        wait_file(case/'release-work',deadline)
    raw=(case/'payload.bin').read_bytes();actual=hashlib.sha256(raw).hexdigest()
    t=time.perf_counter()
    for _ in range(64):result=hashlib.sha256(raw).hexdigest()
    elapsed=time.perf_counter()-t
    atomic(case/('oracle-complete-%d.json'%invocation),dict(pid=os.getpid(),completed=time.perf_counter(),
           payload_hash=actual,result=result,iterations=64,compute_seconds=elapsed,worker_wall=time.perf_counter()-begin))
    if plan['family']=='CRASH_AFTER_WORK' and invocation==1:os._exit(17)
    if plan['family']=='DESCENDANT_ALIVE':
        child=Process(command('desc',case,invocation),case/('desc-%d.log'%invocation))
        wait_file(case/('desc-%d.json'%invocation),deadline);child.close()
    receipt=dict(key=plan['key'],code=source_hash(),config=digest(WORK_CONFIG),manifest=plan['manifest'],
                 payload_hash=actual,result=result,format='RETURNED',invocation=invocation)
    atomic(case/('receipt-%d.json'%invocation),receipt)
    if plan['family']=='EARLY_SCORE':wait_file(case/'release-work',deadline)


def main():
    parser=argparse.ArgumentParser(description='040 standalone Windows auditable CPU runner; not exactly-once.')
    subs=parser.add_subparsers(dest='role',required=True)
    for role in ('worker','desc','dispatch'):
        s=subs.add_parser(role)
        if role=='worker':s.add_argument('plan');s.add_argument('case');s.add_argument('invocation',type=int)
        elif role=='desc':s.add_argument('case');s.add_argument('invocation',type=int)
        else:s.add_argument('plan');s.add_argument('store');s.add_argument('profile',choices=PROFILES);s.add_argument('output')
    s=subs.add_parser('demo');s.add_argument('--root',required=True);s.add_argument('--profile',choices=PROFILES,default='F')
    args=parser.parse_args()
    if args.role=='worker':worker(args.plan,args.case,args.invocation)
    elif args.role=='desc':descendant(args.case,args.invocation)
    elif args.role=='dispatch':dispatch(args.plan,args.store,args.profile,args.output)
    else:
        import importlib.util
        path=Path(__file__).with_name('benchmark_auditable_runner_040.py')
        spec=importlib.util.spec_from_file_location('benchmark040_demo',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        root=Path(args.root);root.mkdir();store=root/'store';initialize_store(store,args.profile)
        result=module.run_case(root/'normal',store,'N1K',0,args.profile,'DEMO')
        print(json.dumps(result))


if __name__=='__main__':main()
