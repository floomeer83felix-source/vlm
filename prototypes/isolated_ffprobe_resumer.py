"""BATCH-015 only: fixed-object append resume, read-only default, no media capability."""
import argparse
import hashlib
import json
import os
import pathlib
import platform
import re
import shutil
import stat
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile
from charades_metadata_audit import check_ancestors
from isolated_ffprobe_installer import (
    PACKAGE, PUBLISHER_SHA, NET_LIMIT, DISK_LIMIT, MIB, InstallError,
    direct_opener, header_value, file_digest, footprint, safe_tool_members,
    package_verified, exclusive_extract, version_result)

OFFSET = 13107200
OLD_BODY = 13186907
CHUNK = 65536
AUDIT_RESERVE = MIB
PART_NAME = 'incoming/ffmpeg-9.0.2.zip.part'
OLD_NAME = 'local-audit/tool-ledger.json'
NEW_NAME = 'local-audit/resume-015-ledger.json'


def fail(reason):
    raise InstallError(reason)


def parent_gate():
    docs = pathlib.Path(__file__).resolve().parent.parent
    results = (docs/'docs/codex-results.md').read_text(encoding='utf-8')
    board = (docs/'docs/next-steps.md').read_text(encoding='utf-8')
    ready = []
    for line in board.splitlines():
        c = [p.strip() for p in line.split('|')]
        if len(c)>4 and re.fullmatch(r'VLM-BATCH-\d{3}',c[1]) and c[3].startswith('**READY'):
            ready.append(c[1])
    if (ready != ['VLM-BATCH-015'] or
        not re.search(r'^### VLM-BATCH-014\s',results,re.M) or
        re.search(r'^### VLM-BATCH-015\s',results,re.M)):
        fail('PARENT_NOT_READY_OR_REPORTED')


def overlap(a, b):
    return a == b or a in b.parents or b in a.parents


def storage_root():
    import winreg
    if os.name!='nt' or platform.machine().lower() not in ('amd64','x86_64') or sys.getwindowsversion().major<10:
        fail('WINDOWS_X64_REQUIREMENT')
    base = pathlib.Path(os.environ['LOCALAPPDATA']).absolute()
    root = base/'VLM-Research-Isolated/CPU-Tools/ffprobe'
    original = os.environ.get('VLM_ORIGINAL_WORKSPACE')
    if not original: fail('ORIGINAL_EXCLUSION_UNKNOWN')
    forbidden = [pathlib.Path(original).absolute(), pathlib.Path(__file__).resolve().parent.parent,
                 base/'VLM-Research-Isolated/Charades-v1-Metadata',
                 base/'VLM-Research-Isolated/Charades-v1-MediaPilot']
    for k in ('OneDrive','OneDriveConsumer','OneDriveCommercial','Dropbox','BOX_SYNC'):
        if os.environ.get(k): forbidden.append(pathlib.Path(os.environ[k]).absolute())
    def subkeys(key):
        out=[]; j=0
        while True:
            try: out.append(winreg.EnumKey(key,j)); j+=1
            except OSError as e:
                if e.winerror==259: return out
                raise
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\OneDrive\Accounts') as key:
            for name in subkeys(key):
                with winreg.OpenKey(key,name) as item:
                    try: forbidden.append(pathlib.Path(winreg.QueryValueEx(item,'UserFolder')[0]).absolute())
                    except FileNotFoundError: pass
    except FileNotFoundError: pass
    for hive in (winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.OpenKey(hive,r'Software\Microsoft\Windows\CurrentVersion\Explorer\SyncRootManager') as key:
                for name in subkeys(key):
                    try:
                        with winreg.OpenKey(key,name+r'\UserSyncRoots') as item:
                            j=0
                            while True:
                                try:
                                    _,v,t=winreg.EnumValue(item,j); j+=1
                                    if t in (winreg.REG_SZ,winreg.REG_EXPAND_SZ):
                                        forbidden.append(pathlib.Path(os.path.expandvars(v)).absolute())
                                except OSError as e:
                                    if e.winerror==259: break
                                    raise
                    except FileNotFoundError: pass
        except FileNotFoundError: pass
    check_ancestors(root)
    if not root.is_dir() or base.resolve() not in root.resolve().parents: fail('STORAGE_IDENTITY')
    for a in (root.absolute(),root.resolve()):
        for p in forbidden:
            if any(overlap(a,b) for b in (p.absolute(),p.resolve())): fail('STORAGE_OVERLAP')
    if shutil.disk_usage(root).free < 1024*MIB: fail('STORAGE_FREE_SPACE')
    return root


def ordinary(path):
    check_ancestors(path)
    s=path.stat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1: fail('LOCAL_FILE_IDENTITY')
    return s


def old_contract(state):
    expected={'body_bytes':OLD_BODY,'get_attempts':4,'head_attempts':3,
              'successful_zip_gets':0,'version_runs':0,'status':'BLOCKED','reason':'timeout'}
    if any(type(state.get(k)) is not type(v) or state.get(k)!=v for k,v in expected.items()):
        fail('OLD_LEDGER_CONFLICT')
    events=state.get('events')
    if (not isinstance(events,list) or len(events)!=4 or
        any(type(e.get('read')) is not int or e['read']<0 for e in events) or
        sum(e['read'] for e in events)!=OLD_BODY or
        events[-1]!={'kind':'PACKAGE','read':OFFSET,'status':'STOPPED'} or
        [(e.get('kind'),e.get('status'),e['read']) for e in events[:-1]] !=
        [('TEXT','COMPLETE',27484),('TEXT','COMPLETE',52159),('TEXT','COMPLETE',64)]):
        fail('OLD_LEDGER_EVENTS')
    return state


def local_audit(root):
    part=root/PART_NAME; parent=root/OLD_NAME
    files=set()
    for p in root.rglob('*'):
        check_ancestors(p)
        if p.is_file(): files.add(p.relative_to(root).as_posix())
        elif not p.is_dir(): fail('LOCAL_SPECIAL_ASSET')
    if files != {PART_NAME,OLD_NAME}: fail('EXTRA_OR_RESUME_ASSET')
    ps=ordinary(part); ls=ordinary(parent)
    if ps.st_size!=OFFSET or ls.st_size!=574: fail('LOCAL_SIZE_CONFLICT')
    with part.open('rb') as f:
        if f.read(4)!=b'PK\x03\x04': fail('PART_SIGNATURE')
    old=old_contract(json.loads(parent.read_text(encoding='utf-8')))
    return {'part_sha':file_digest(part),'parent_sha':file_digest(parent),
            'part_identity':[ps.st_dev,ps.st_ino], 'old':old,
            'initial_disk_bytes':footprint(root)}


def unchanged(root, snapshot):
    ps=ordinary(root/PART_NAME)
    if ([ps.st_dev,ps.st_ino]!=snapshot['part_identity'] or ps.st_size!=OFFSET or
        file_digest(root/PART_NAME)!=snapshot['part_sha'] or
        file_digest(root/OLD_NAME)!=snapshot['parent_sha']): fail('LOCAL_CHANGED')


class ResumeLedger:
    def __init__(self,path,snapshot):
        self.path=path
        self.state={'parent_body_bytes':OLD_BODY,'body_bytes':OLD_BODY,'charged_bytes':OLD_BODY,
                    'new_body_bytes':0,'new_reserved_bytes':0,'new_get_attempts':0,'new_head_attempts':0,
                    'get_attempts':4,'head_attempts':3,'parent_events':snapshot['old']['events'],
                    'parent_sha':snapshot['parent_sha'],'initial_part_sha':snapshot['part_sha'],
                    'initial_part_bytes':OFFSET,'events':[],'status':'PREFLIGHT',
                    'range_support':'UNKNOWN','version_runs':0,'peak_local_bytes':snapshot['initial_disk_bytes']}
        if path is not None:
            check_ancestors(path)
            with path.open('x',encoding='utf-8') as f:
                json.dump(self.state,f,indent=2); f.flush(); os.fsync(f.fileno())
    def save(self):
        if self.path is None: return
        check_ancestors(self.path)
        tmp=self.path.with_suffix('.next'); check_ancestors(tmp)
        with tmp.open('x',encoding='utf-8') as f:
            json.dump(self.state,f,indent=2); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,self.path)
    def begin(self,kind,expected):
        if self.state['new_get_attempts']>=2 or self.state['charged_bytes']+expected>NET_LIMIT:
            fail('NETWORK_BUDGET_OR_GET_COUNT')
        if kind not in ('PROBE','SUFFIX') or expected<=0: fail('REQUEST_KIND')
        prior=[e['kind'] for e in self.state['events']]
        if prior != ([] if kind=='PROBE' else ['PROBE']): fail('REQUEST_SEQUENCE')
        if kind=='SUFFIX' and self.state['events'][-1]['status']!='COMPLETE': fail('PROBE_NOT_COMPLETE')
        self.state['new_get_attempts']+=1; self.state['get_attempts']+=1
        self.state['events'].append({'kind':kind,'expected':expected,'read':0,'reserved':0,'status':'STARTED'})
        self.save()  # Exclusive persistent attempt record before request.
    def reserve(self,n):
        event=self.state['events'][-1]
        if (not 0<n<=CHUNK or event['reserved']+n>event['expected'] or
            self.state['charged_bytes']+n>NET_LIMIT): fail('READ_RESERVATION_BUDGET')
        self.state['charged_bytes']+=n; self.state['new_reserved_bytes']+=n
        event['reserved']+=n; self.save()  # Crash charge durable BEFORE read; never decremented.
    def received(self,n):
        event=self.state['events'][-1]
        if not 0<n<=event['reserved']-event['read']: fail('READ_OVERRUN')
        event['read']+=n; self.state['new_body_bytes']+=n; self.state['body_bytes']+=n; self.save()
    def finish(self,status):
        self.state['events'][-1]['status']=status; self.save()
    def disk(self,n):
        if not 0<=n<=DISK_LIMIT: fail('DISK_BUDGET')
        self.state['peak_local_bytes']=max(n,self.state['peak_local_bytes']); self.save()


def strong_etag(value):
    if not isinstance(value,str) or not re.fullmatch(r'"[\x21\x23-\x7e]+"',value):
        fail('REMOTE_STRONG_ETAG_REQUIRED')
    return value


def head_identity(status,headers,url):
    if status!=200 or url!=PACKAGE: fail('REMOTE_HEAD_STATUS_OR_URL')
    if header_value(headers,'Content-Encoding','identity').lower()!='identity': fail('REMOTE_ENCODING')
    raw=header_value(headers,'Content-Length','')
    if not re.fullmatch(r'[0-9]+',raw): fail('REMOTE_LENGTH')
    n=int(raw)
    if not OFFSET<n<=NET_LIMIT or n-OFFSET+1>NET_LIMIT-OLD_BODY: fail('REMOTE_LENGTH_BUDGET')
    if 'zip' not in header_value(headers,'Content-Type','').lower(): fail('REMOTE_TYPE')
    return n,strong_etag(header_value(headers,'ETag'))


def range_identity(response,start,end,total,etag):
    if response.status!=206 or response.geturl()!=PACKAGE: fail('RANGE_STATUS_OR_URL')
    h=response.headers
    if header_value(h,'Content-Range')!=f'bytes {start}-{end}/{total}': fail('RANGE_OFFSET_TOTAL')
    if header_value(h,'Content-Length')!=str(end-start+1): fail('RANGE_LENGTH')
    if header_value(h,'Content-Encoding','identity').lower()!='identity': fail('RANGE_ENCODING')
    if strong_etag(header_value(h,'ETag'))!=etag: fail('RANGE_ETAG_CHANGE')


def range_request(start,end,etag):
    if not 0<=start<=end or not (start==end==OFFSET-1 or start==OFFSET): fail('RANGE_REQUEST_OFFSET')
    strong_etag(etag)
    return urllib.request.Request(PACKAGE,headers={'Range':f'bytes={start}-{end}',
        'If-Range':etag,'Accept-Encoding':'identity'},method='GET')


def transfer(response,ledger,length,writer=None,root=None,initial_size=None):
    received=0; data=[]
    while received<length:
        n=min(CHUNK,length-received)
        ledger.reserve(n)
        if root is not None: ledger.disk(footprint(root))
        chunk=response.read(n)
        if len(chunk)!=n:  # Short reads/EOF are fail closed; no hidden read retry.
            if chunk: ledger.received(len(chunk))
            fail('RANGE_SHORT_READ')
        ledger.received(n)
        if writer is not None:
            if os.fstat(writer.fileno()).st_size != initial_size+received: fail('APPEND_SIZE_CHANGED')
            writer.write(chunk); writer.flush(); os.fsync(writer.fileno())
        else: data.append(chunk)
        received+=n
        if root is not None: ledger.disk(footprint(root))
    ledger.finish('COMPLETE')
    return b''.join(data) if writer is None else received


class Client:
    def __init__(self,ledger): self.ledger=ledger; self.opener=direct_opener()
    def head(self):
        if self.ledger.state['new_head_attempts']>=2: fail('HEAD_COUNT')
        self.ledger.state['new_head_attempts']+=1; self.ledger.state['head_attempts']+=1; self.ledger.save()
        req=urllib.request.Request(PACKAGE,method='HEAD',headers={'Accept-Encoding':'identity'})
        with self.opener.open(req,timeout=30) as r:
            identity=head_identity(r.status,r.headers,r.geturl())
        self.ledger.state.setdefault('heads',[]).append({'length':identity[0],'etag':identity[1]})
        self.ledger.save()
        return identity
    def get(self,start,end,total,etag,kind,writer=None,root=None):
        self.ledger.begin(kind,end-start+1)
        try:
            with self.opener.open(range_request(start,end,etag),timeout=30) as r:
                range_identity(r,start,end,total,etag)  # 200/416/redirect: no body read.
                return transfer(r,self.ledger,end-start+1,writer,root,OFFSET if writer else None)
        except Exception:
            self.ledger.finish('STOPPED'); raise


def deploy_archive(root,part,ledger,total):
    if part.stat().st_size!=total: fail('FULL_SIZE_MISMATCH')
    package_verified(file_digest(part))  # No extraction before frozen publisher SHA.
    ledger.state['full_sha_verified']=True; ledger.save()
    with zipfile.ZipFile(part) as z:
        selected=safe_tool_members(z.infolist(),total)
        if z.testzip() is not None: fail('FULL_CRC')
        ledger.state['archive_crc_verified']=True; ledger.state['selected_count']=len(selected); ledger.save()
        for _,(relative,info) in selected.items(): exclusive_extract(z,info,root/relative,root,ledger)
    exe=root/'bin/ffprobe.exe'
    ledger.state['executable_sha']=file_digest(exe); ledger.state['version_runs']=1; ledger.save()
    process=subprocess.run([str(exe),'-version'],capture_output=True,timeout=10)
    ledger.state['version']=version_result(process); ledger.state['authenticode']='UNKNOWN_NOT_CHECKED'
    ledger.state['status']='AVAILABLE_PUBLISHER_HASH_VERIFIED'; ledger.disk(footprint(root)); ledger.save()


def public_receipt(state):
    keys=('status','reason','range_support','parent_body_bytes','new_body_bytes','body_bytes','charged_bytes',
          'new_reserved_bytes','new_get_attempts','new_head_attempts','get_attempts','head_attempts',
          'peak_local_bytes','full_sha_verified','archive_crc_verified','selected_count','version_runs','version')
    return {k:state.get(k) for k in keys}


def resume():
    parent_gate(); root=storage_root(); snapshot=local_audit(root)
    ledger=ResumeLedger(root/NEW_NAME,snapshot)
    try:
        ledger.disk(footprint(root)); client=Client(ledger)
        first=client.head(); second=client.head()
        if first!=second: fail('REMOTE_HEAD_CHANGED')
        total,etag=first
        if footprint(root)+(total-OFFSET)+AUDIT_RESERVE>DISK_LIMIT: fail('DISK_SUFFIX_PREFLIGHT')
        unchanged(root,snapshot)
        with (root/PART_NAME).open('rb') as f: f.seek(OFFSET-1); boundary=f.read(1)
        observed=client.get(OFFSET-1,OFFSET-1,total,etag,'PROBE',root=root)
        if observed!=boundary: fail('PROBE_PART_MISMATCH')
        ledger.state['range_support']='VERIFIED_206'; ledger.save()
        if ledger.state['charged_bytes']+(total-OFFSET)>NET_LIMIT: fail('SUFFIX_GLOBAL_BUDGET')
        unchanged(root,snapshot)
        with (root/PART_NAME).open('ab') as writer:
            s=os.fstat(writer.fileno())
            if [s.st_dev,s.st_ino]!=snapshot['part_identity'] or s.st_size!=OFFSET: fail('APPEND_IDENTITY')
            client.get(OFFSET,total-1,total,etag,'SUFFIX',writer,root)
        if file_digest(root/OLD_NAME)!=snapshot['parent_sha']: fail('PARENT_LEDGER_CHANGED')
        deploy_archive(root,root/PART_NAME,ledger,total)
    except Exception as e:
        ledger.state['status']='BLOCKED'
        ledger.state['reason']=str(e) if isinstance(e,InstallError) else type(e).__name__
        if ledger.state['reason'].startswith('REMOTE'): ledger.state['range_support']='BLOCKED'
        ledger.disk(footprint(root)); ledger.save()
    return public_receipt(ledger.state)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(); group.add_argument('--resume',action='store_true')
    group.add_argument('--preflight',action='store_true'); args=parser.parse_args()
    try:
        if args.resume: result=resume()
        else:
            parent_gate(); snapshot=local_audit(storage_root())
            result={'status':'PREFLIGHT_PASS','old_body_bytes':OLD_BODY,'part_bytes':OFFSET,'http_requests':0,'local_writes':0}
        print(json.dumps(result,ensure_ascii=True,indent=2))
        if result['status']=='BLOCKED': raise SystemExit(1)
    except Exception as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e) if isinstance(e,InstallError) else type(e).__name__}))
        raise SystemExit(1) from None
