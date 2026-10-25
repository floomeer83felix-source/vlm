"""044 single registered source, real verified HTTPS and bounded CPU admission.

New transport/lifecycle, not a runtime replacement of043 fake types/constants.
Only explicit readonly040 platform /042 CPU-clock library functions are reused.
"""
import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import socket
import ssl
import sys
import time

CAP=4294967296
URL='https://data.bris.ac.uk/datasets/3h91syskeag572hl6tvuovwv4d/videos/test/P31/P31_10.MP4'
HOST='data.bris.ac.uk'
TARGET='/datasets/3h91syskeag572hl6tvuovwv4d/videos/test/P31/P31_10.MP4'
PUBLISHER_MD5='d400c28d06a4c4302312549a34008309'
MANIFEST_SHA='0f21ca3a765a5dd5ed264fca5147676d762b32f0dc4526db87b26153778b75c4'
clock=time.perf_counter

def require(x,reason):
    if not x:raise ValueError(reason)
def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def read(p):return json.loads(Path(p).read_bytes())
def exclusive(path,value):
    data=pack(value);require(len(data)<=65536,'CONTROL_FILE_CAP')
    with open(path,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def load_public(name):
    spec=importlib.util.spec_from_file_location('public_'+name,Path(__file__).with_name(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def offline_guard():
    def audit(event,args):
        if event.startswith('socket.'):raise PermissionError('OFFLINE_PRECHECK_044')
        if event=='import' and args[0].split('.')[0] in ('torch','transformers','numpy'):raise PermissionError('NO_MODEL_044')
    sys.addaudithook(audit);blocked=[]
    for name,fn in [('create',lambda:socket.socket()),('resolve',lambda:socket.getaddrinfo('localhost',80))]:
        try:fn()
        except PermissionError:blocked.append(name)
        else:raise AssertionError('GUARD_FAILED')
    return dict(installed=True,blocked=blocked,actual_sockets=0)

class Journal:
    def __init__(self,root,fail=None):self.path=Path(root)/'events.jsonl';self.seq=0;self.previous='0'*64;self.fail=fail
    def add(self,event,**data):
        require(self.seq<20000,'EVENT_CAP');body=dict(seq=self.seq+1,previous=self.previous,t=clock(),event=event,**data);h=hashlib.sha256(pack(body)).hexdigest();line=pack(dict(body=body,sha256=h))+b'\n';require(len(line)<=2048,'EVENT_LINE_CAP')
        with open(self.path,'ab') as f:
            f.write(line);f.flush()
            if event==self.fail:raise OSError('INJECTED_FSYNC_FAILURE')
            os.fsync(f.fileno())
        self.seq+=1;self.previous=h

def validated(status,headers):
    require(status==200,'HTTP_STATUS_'+str(status));fields={}
    critical={'content-length','etag','content-encoding','transfer-encoding','content-type','location'}
    for k,v in headers:
        k=k.lower()
        require(k not in critical or k not in fields,'DUPLICATE_CRITICAL_HEADER')
        fields[k]=v
    require('text/html' not in fields.get('content-type','').lower(),'HTML_OR_TERMS')
    require('location' not in fields,'REDIRECTION')
    value=fields.get('content-length','');require(value.isascii() and value.isdigit() and 0<int(value)<=CAP,'UNRELIABLE_OR_OVERSIZE_LENGTH')
    require(fields.get('content-encoding','identity').lower()=='identity' and 'transfer-encoding' not in fields,'ENCODING')
    etag=fields.get('etag')
    strong=bool(etag and len(etag)>=2 and etag.startswith('"') and etag.endswith('"') and all(0x21<=ord(ch)<=0x7e and ch!='"' for ch in etag[1:-1]))
    return dict(length=int(value),etag=etag,strong_etag=strong,encoding=fields.get('content-encoding','identity'))

class Transport:
    def __init__(self,url,journal,deadline,connection_factory=None):
        require(url==URL,'EXACT_URL_ALLOWLIST');self.journal=journal;self.deadline=deadline;self.sent=set();self.connections=[]
        self.factory=connection_factory or http.client.HTTPSConnection
        self.context=ssl.create_default_context();require(self.context.verify_mode==ssl.CERT_REQUIRED and self.context.check_hostname,'TLS_VALIDATION')
    def remaining(self,maximum):
        delta=self.deadline-clock();require(delta>0,'WORK_DEADLINE');return min(maximum,delta)
    def request(self,method,etag=None):
        require(method in ('HEAD','GET') and method not in self.sent,'ONE_SHOT_METHOD')
        self.sent.add(method)
        connection=self.factory(HOST,443,timeout=self.remaining(15),context=self.context);self.connections.append(connection)
        connection.connect()
        self.journal.add('CONNECTED',method=method)
        connection.sock.settimeout(self.remaining(30))
        headers={'Accept-Encoding':'identity','User-Agent':'VLM-044-noncommercial-research','Connection':'close'}
        if method=='GET' and etag is not None:headers['If-Match']=etag
        self.journal.add('SEND_STARTED',method=method,conditional=bool(etag))
        connection.request(method,TARGET,headers=headers)
        self.journal.add('SEND_RETURNED',method=method)
        # HTTPConnection may clear its .sock on Connection:close; retain the
        # response-owned socket so each body read receives a remaining-time cap.
        self.read_socket=connection.sock
        response=connection.getresponse();return response
    def read(self,response,size):
        self.read_socket.settimeout(self.remaining(30))
        return response.read(size)
    def close(self):
        for c in self.connections:c.close()

def store_headers(root,kind,response,journal):
    value=dict(status=response.status,headers=list(response.getheaders()))
    exclusive(Path(root)/(kind.lower()+'-headers.json'),value)
    journal.add(kind+'_RESULT',file=kind.lower()+'-headers.json',sha256=hashlib.sha256(pack(value)).hexdigest(),status=response.status)
    return value

def transfer(root,config,connection_factory=None,fail=None):
    """All tests and real execution use this exact adapter/lifecycle path."""
    root=Path(root);exclusive(root/'attempt.claim',config)
    j=Journal(root,fail);transport=Transport(config['url'],j,config['work_deadline'],connection_factory);returned=written=0;result=dict(state='FAILED',error=None)
    try:
        j.add('CLAIM',source_ref='C02_044',cap=CAP,manifest_sha256=MANIFEST_SHA,start=config['start'],work_deadline=config['work_deadline'])
        j.add('HEAD_INTENT',method='HEAD')
        head_response=transport.request('HEAD');raw=store_headers(root,'HEAD',head_response,j);head=validated(raw['status'],raw['headers'])
        j.add('HEAD_VALIDATED',**head);head_response.close()
        j.add('RESERVE',full_responsibility=head['length'],cap=CAP)
        j.add('GET_INTENT',method='GET',responsibility=head['length'],if_match=head['etag'] if head['strong_etag'] else None)
        response=transport.request('GET',head['etag'] if head['strong_etag'] else None);actual=store_headers(root,'GET',response,j);get=validated(actual['status'],actual['headers'])
        require(head['length']==get['length'] and (head['etag'] is None or head['etag']==get['etag']),'GET_METADATA_MISMATCH')
        j.add('GET_VALIDATED',**get)
        md5=hashlib.md5();sha=hashlib.sha256()
        with open(root/'media.partial','xb') as f:
            while returned<head['length']:
                require(clock()<config['work_deadline'],'WORK_DEADLINE')
                size=min(1024**2,head['length']-returned)
                j.add('READ_INTENT',requested=size,returned_before=returned,written_before=written)
                block=transport.read(response,size);require(bool(block),'SHORT_BODY');require(len(block)<=size,'READ_OVERFLOW')
                returned+=len(block);require(returned<=head['length'] and returned<=CAP,'BODY_CAP')
                j.add('READ_RETURN',returned_total=returned,size=len(block))
                f.write(block);f.flush();os.fsync(f.fileno());written+=len(block);md5.update(block);sha.update(block)
                j.add('PROGRESS',returned_total=returned,written_fsynced=written)
        require(written==head['length'] and md5.hexdigest()==config['publisher_md5'],'PUBLISHER_MD5_MISMATCH')
        j.add('BYTES_VERIFIED',bytes=written,md5=md5.hexdigest(),sha256=sha.hexdigest())
        target=root/('verified.fixture' if config.get('fixture') else 'media-02.MP4')
        os.rename(root/'media.partial',target);j.add('COMPLETE',bytes=written,md5=md5.hexdigest(),sha256=sha.hexdigest())
        result.update(state='COMPLETE',bytes=written,md5=md5.hexdigest(),sha256=sha.hexdigest())
    except Exception as e:
        result['error']=type(e).__name__+':'+str(e)[:200]
        # No request follows any failure. A persistence fault is not retried.
        if 'FSYNC_FAILURE' not in str(e):
            try:j.add('ABORT',reason=result['error'])
            except OSError:pass
    finally:transport.close()
    exclusive(root/'worker-result.json',result)

def replay(root):
    root=Path(root);events=[];unknown=False;prev='0'*64
    path=root/'events.jsonl'
    if path.exists():
        for line in path.read_bytes().splitlines(keepends=True):
            try:
                require(line.endswith(b'\n'),'HALF_LINE');r=json.loads(line);b=r['body'];require(b['seq']==len(events)+1 and b['previous']==prev and r['sha256']==hashlib.sha256(pack(b)).hexdigest(),'CHAIN')
                events.append(b);prev=r['sha256']
            except (ValueError,KeyError,TypeError):unknown=True;break
    def last(kind):return next((e for e in reversed(events) if e['event']==kind),None)
    metadata={}
    for kind in ('HEAD','GET'):
        ref=last(kind+'_RESULT')
        if ref:
            try:
                data=read(root/ref['file']);require(hashlib.sha256(pack(data)).hexdigest()==ref['sha256'],'HEADER_BINDING');metadata[kind]=data
            except (OSError,ValueError):unknown=True
    reserve=last('RESERVE');get_intent=last('GET_INTENT');complete=last('COMPLETE');verified=last('BYTES_VERIFIED')
    returned=max((e['returned_total'] for e in events if e['event']=='READ_RETURN'),default=0)
    written=max((e['written_fsynced'] for e in events if e['event']=='PROGRESS'),default=0)
    admitted=bool(complete and verified and not unknown and complete['sha256']==verified['sha256'] and complete['bytes']==written)
    file_exists=(root/'media-02.MP4').is_file() or (root/'verified.fixture').is_file()
    admitted=admitted and file_exists
    return dict(state='COMPLETE' if admitted else 'FAILED_OR_UNKNOWN',metadata=metadata,head=last('HEAD_VALIDATED'),responsibility=(reserve['full_responsibility'] if reserve else CAP if get_intent or unknown else 0),returned_lower=returned,written_lower=written,exactness='COMPLETE_APPLICATION_BODY' if admitted else 'UNKNOWN_PENDING_BODY' if get_intent or unknown else 'NO_GET_INTENT',journal_unknown=unknown,complete=complete,events=len(events),head_intents=sum(e['event']=='HEAD_INTENT' for e in events),get_intents=sum(e['event']=='GET_INTENT' for e in events),sends_started={m:sum(e['event']=='SEND_STARTED' and e['method']==m for e in events) for m in ('HEAD','GET')},sends_returned={m:sum(e['event']=='SEND_RETURNED' and e['method']==m for e in events) for m in ('HEAD','GET')},read_intents=sum(e['event']=='READ_INTENT' for e in events))

def supervise(root,role,args,limits,python=None):
    """Same supervisor for short blocked-adapter check and real840/870/900."""
    root=Path(root);t0=clock();work=t0+limits[0];drain=t0+limits[1];finish=t0+limits[2]
    p=load_public('auditable_runner_040');j=p.Job(memory=4*1024**3,active_limit=2);child=None;kill=None;active0=None;code=None;error=None;max_active=0
    config=dict(start=t0,work_deadline=work,active0_deadline=drain,finish_deadline=finish)
    exclusive(root/'supervisor-config.json',config)
    command=[python or sys.executable,'-I','-S','-B',str(Path(__file__).resolve()),role,str(root)]+list(args)
    try:
        child=p.Process(command,root/'worker.log',j)
        while True:
            active=j.active();now=clock();max_active=max(max_active,active)
            if not active:active0=now;break
            if now>=work-.1 and kill is None:kill=now;j.kill()
            if now>=drain:raise TimeoutError('ACTIVE0_DEADLINE')
            time.sleep(.005)
        code=child.poll()
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if active0 is None:
            if kill is None:kill=clock();j.kill()
            # No disk I/O in this ownership/drain wait either.
            while j.active() and clock()<drain:time.sleep(.005)
            if j.active()==0:active0=clock()
        snapshot=j.snapshot()
        if child:child.close()
        j.close()
    require(active0 is not None and snapshot['active']==0,'OWN_GROUP_EXIT_UNKNOWN')
    result=dict(**config,kill_requested=kill,active0=active0,exitcode=code,error=error,max_active=max_active,**snapshot)
    exclusive(root/'supervisor.json',result)
    result['finished']=clock();result['deadline_violation']=bool((kill is not None and kill>work) or active0>drain or result['finished']>finish)
    return result

def cpu_api(root,site):
    exclusive(Path(root)/'guard.json',offline_guard());sys.path.insert(0,site);import av
    require(all(hasattr(av.VideoFrame,k) for k in ('pts','duration','time_base')) and 'hwaccel' in av.open.__doc__,'CPU_FRAME_INTERFACE')
    binaries=[]
    for name in ('av._core','av.video.frame','av.video.codeccontext'):
        p=Path(sys.modules[name].__file__);binaries.append(dict(module=name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    require('torch' not in sys.modules,'TORCH_IMPORTED')
    exclusive(Path(root)/'api.json',dict(av=av.__version__,libraries={k:list(v) for k,v in av.library_versions.items()},binaries=binaries,torch_imported=False))

def real(root):
    root=Path(root);blob=(root.parent/'manifest.json').read_bytes();require(hashlib.sha256(blob).hexdigest()==MANIFEST_SHA,'MANIFEST_IDENTITY')
    item=json.loads(blob)['candidates'][0];require(item['candidate_rank']==2 and item['media_url']==URL and item['publisher_md5']==PUBLISHER_MD5,'REGISTERED_OBJECT')
    cfg=read(root/'supervisor-config.json');transfer(root,dict(cfg,url=URL,publisher_md5=PUBLISHER_MD5,fixture=False))

def cpu_scan(root,site):
    root=Path(root);exclusive(root/'scan-guard.json',offline_guard());sys.path.insert(0,site);import av
    av.logging.set_level(av.logging.PANIC)
    require(replay(root.parent/'fetch')['state']=='COMPLETE','FETCH_NOT_ADMITTED')
    # Readonly library call on this new044 root, never an old startup role/run.
    old=load_public('epic_clock_admission_042');old.scan(root.parent/'fetch',2,site)
    require('torch' not in sys.modules,'TORCH_IMPORTED')

def main():
    role,root,*args=sys.argv[1:]
    if role=='real':real(root)
    elif role=='api':cpu_api(root,args[0])
    elif role=='scan':cpu_scan(root,args[0])
    elif role=='blocked-precheck':
        sys.path.insert(0,str(Path(__file__).resolve().parent));from test_single_source_admission_044 import blocked
        blocked(root)
    elif role=='precheck':
        sys.path.insert(0,str(Path(__file__).resolve().parent));from test_single_source_admission_044 import suite
        suite(root)
    else:raise ValueError('ROLE')

if __name__=='__main__':main()
