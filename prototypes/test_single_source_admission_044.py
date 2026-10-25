"""044 integration precheck of the actual new adapter; no real socket/server."""
import hashlib
import json
from pathlib import Path
import ssl
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
import single_source_admission_044 as c

DATA=bytes((13+5*i)%256 for i in range(32768))

class Response:
    def __init__(self,method,mode,calls):self.method=method;self.mode=mode;self.calls=calls;self.cursor=0;self.status=302 if mode=='status' and method=='GET' else 200
    def getheaders(self):
        n=len(DATA)+(self.mode=='length' and self.method=='GET')
        etag='"different"' if self.mode=='etag' and self.method=='GET' else '"fixture044"'
        if self.mode=='weak':etag='W/"fixture044"'
        if self.mode=='malformed':etag='"'
        if self.mode=='missing':headers=[('Content-Length',str(n))]
        else:headers=[('Content-Length',str(n)),('ETag',etag)]
        headers += [('Content-Type','video/mp4'),('Content-Encoding','gzip' if self.mode=='encoding' and self.method=='GET' else 'identity')]
        if self.mode=='duplicate' and self.method=='GET':headers.append(('content-length',str(n)))
        return headers
    def read(self,size):
        self.calls.append(dict(event='READ',size=size))
        if self.mode=='blocked':time.sleep(60)
        if self.mode=='interrupted' and self.cursor:raise TimeoutError('OWNED_READ_INTERRUPTION')
        size=min(size,4096) if self.mode=='interrupted' else size
        data=DATA[self.cursor:self.cursor+size];self.cursor+=len(data);return data
    def close(self):pass

def factory(mode,calls):
    class Connection:
        def __init__(self,host,port,timeout,context):
            assert host==c.HOST and port==443 and 0<timeout<=15
            assert context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname
            calls.append(dict(event='CONNECTION',host=host,port=port,verified=True));self.sock=self
        def connect(self):calls.append(dict(event='CONNECT'))
        def settimeout(self,value):assert 0<value<=30
        def request(self,method,path,headers):
            assert path==c.TARGET and method in ('HEAD','GET') and 'Range' not in headers
            calls.append(dict(event='SEND',method=method,headers=headers));self.method=method
        def getresponse(self):return Response(self.method,mode,calls)
        def close(self):pass
    return Connection

def configuration(deadline=None,wrong_digest=False):
    return dict(start=c.clock(),work_deadline=deadline or c.clock()+30,url=c.URL,publisher_md5='0'*32 if wrong_digest else hashlib.md5(DATA).hexdigest(),fixture=True)

def blocked(root):
    root=Path(root);c.exclusive(root/'guard.json',c.offline_guard());calls=[]
    cfg=configuration(c.read(root/'supervisor-config.json')['work_deadline'])
    c.transfer(root,cfg,factory('blocked',calls))

def suite(root):
    root=Path(root);network_guard=c.offline_guard();checks=[];modes={}
    def check(name,ok):c.require(ok,name);checks.append(name)
    def run(name,mode='normal',wrong=False,fail=None):
        p=root/name;p.mkdir();calls=[];c.transfer(p,configuration(wrong_digest=wrong),factory(mode,calls),fail)
        modes[name]=dict(calls=calls,replay=c.replay(p));return p,calls,modes[name]['replay']
    p,calls,r=run('normal')
    check('normal_atomic_dual_digest',r['state']=='COMPLETE' and not (p/'media.partial').exists() and (p/'verified.fixture').read_bytes()==DATA and r['complete']['md5']==hashlib.md5(DATA).hexdigest() and r['complete']['sha256']==hashlib.sha256(DATA).hexdigest())
    check('single_HEAD_GET_no_range',[x['method'] for x in calls if x['event']=='SEND']==['HEAD','GET'])
    check('strong_if_match',next(x for x in calls if x.get('method')=='GET')['headers'].get('If-Match')=='"fixture044"')
    check('persisted_HEAD_before_GET',r['head']['length']==len(DATA) and r['metadata']['HEAD']['status']==200 and r['responsibility']==len(DATA))
    before=len(calls)
    try:c.transfer(p,configuration(),factory('normal',calls))
    except FileExistsError:pass
    else:raise AssertionError('DUPLICATE_CLAIM')
    check('consumed_attempt_no_resend',len(calls)==before)
    for mode in ('weak','missing','malformed'):
        _,calls,r=run(mode,mode);check(mode+'_conditional_absence_explicit',r['state']=='COMPLETE' and not r['head']['strong_etag'] and 'If-Match' not in next(x for x in calls if x.get('method')=='GET')['headers'])
    for stage in ('HEAD_VALIDATED','RESERVE'):
        _,calls,r=run('fail-'+stage,fail=stage);check(stage+'_fsync_failure_GET0',not any(x.get('method')=='GET' or x['event']=='READ' for x in calls) and r['state']!='COMPLETE' and r['metadata']['HEAD']['status']==200)
    for mode in ('length','etag','status','encoding','duplicate'):
        _,calls,r=run(mode,mode);check(mode+'_GET_rejected_before_read',r['state']!='COMPLETE' and not any(x['event']=='READ' for x in calls) and set(r['metadata'])=={'HEAD','GET'})
    p,calls,r=run('digest-fail',wrong=True);check('bad_digest_no_admission',r['state']!='COMPLETE' and not (p/'verified.fixture').exists() and (p/'media.partial').exists())
    _,calls,r=run('interrupted','interrupted');check('interruption_full_reservation',r['state']!='COMPLETE' and r['written_lower']==4096 and r['responsibility']==len(DATA) and r['exactness']=='UNKNOWN_PENDING_BODY')
    check('no_retry_after_failure',sum(x.get('method')=='GET' for x in calls)==1)
    p=root/'allowlist';p.mkdir();j=c.Journal(p);calls=[]
    for url in (c.URL+'?x=1',c.URL.replace('https:','http:'),c.URL.replace(c.HOST,'localhost')):
        try:c.Transport(url,j,c.clock()+2,factory('normal',calls))
        except ValueError:pass
        else:raise AssertionError('URL_REJECTION')
    check('exact_URL_no_connection',not calls)
    transport=c.Transport(c.URL,j,c.clock()+2,factory('normal',calls))
    try:transport.request('POST')
    except ValueError:pass
    else:raise AssertionError('METHOD_REJECTION')
    check('method_allowlist',not calls)
    c.exclusive(root/'precheck.json',dict(status='PASS',assertions=checks,guard=network_guard,cases=modes))

if __name__=='__main__':suite(sys.argv[1])
