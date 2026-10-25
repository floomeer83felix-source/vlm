"""One046 integration precheck; no actual socket, media or old task tests."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import ssl
import sys
import time
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent))
import holoassist_real_input_046 as c

DATA=bytes((17+3*i)%256 for i in range(32768))
def fixture_manifest():
    m=c.read(Path(__file__).resolve().parents[1]/'docs/codex-artifacts/VLM-HOLOASSIST-REAL-INPUT-046/manifest.json')
    m['candidates'][0]['expected_bytes']=len(DATA);m['candidates'][0]['publisher_lfs_sha256']=hashlib.sha256(DATA).hexdigest();return m
def factory(mode,calls,m):
    class Response:
        def __init__(self,method,path):self.method=method;self.path=path;self.cursor=0;self.status=302 if method=='HEAD' or path.startswith('/datasets/') else 200
        def getheaders(self):
            h=[('Content-Type','application/octet-stream')]
            if self.status==302:
                h.extend([('X-Linked-Size',str(len(DATA))),('X-Linked-ETag','"'+m['candidates'][0]['publisher_lfs_sha256']+'"'),('Location','https://cas-bridge.xethub.hf.co/owned?owned=1')])
                if mode=='badhost' and self.method=='GET':h[-1]=('Location','https://outside.invalid/owned')
                if mode=='duplicate' and self.method=='GET':h.append(('Location','https://cas-bridge.xethub.hf.co/other'))
                if mode=='headsha' and self.method=='HEAD':h[2]=('X-Linked-ETag','"wrong"')
            else:
                h.append(('Content-Length',str(len(DATA)+(mode=='length'))))
                if mode=='encoding':h.append(('Content-Encoding','gzip'))
            return h
        def read(self,n):
            calls.append(dict(event='READ'))
            if mode=='blocked':time.sleep(60)
            size=min(n,4096) if mode=='short' else n
            if mode=='short' and self.cursor:return b''
            b=DATA[self.cursor:self.cursor+size];self.cursor+=len(b)
            if mode=='digest':return bytes(255-x for x in b)
            return b
        def close(self):pass
    class Connection:
        def __init__(self,host,port,timeout,context):assert host in m['redirect_host_allowlist'] and port==443 and 0<timeout<=15;assert context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname;self.host=host;self.sock=self
        def connect(self):pass
        def settimeout(self,t):assert 0<t<=30
        def request(self,method,path,headers):
            assert method in ('HEAD','GET') and not any(k.lower() in ('range','authorization','cookie') for k in headers);self.method=method;self.path=path;calls.append(dict(event='SEND',method=method,host=self.host,path=path))
        def getresponse(self):return Response(self.method,self.path)
        def close(self):pass
    return Connection

def blocked(root):
    c.offline_guard();root=Path(root);m=fixture_manifest();calls=[];cfg=c.read(root/'blocked-config.json');c.fetch(root,m,cfg,factory('blocked',calls,m))

def suite(root):
    root=Path(root);c.offline_guard();checks=[];records={}
    def check(n,x):c.require(x,n);checks.append(n)
    def rejects(n,fn):
        try:fn()
        except (ValueError,TypeError):checks.append(n);return
        raise AssertionError(n)
    m=fixture_manifest();url=m['candidates'][0]['media_url']
    for name,bad in [('host','https://elsewhere.invalid/a'),('userinfo','https://user@huggingface.co/a'),('fragment','https://huggingface.co/a#x'),('port','https://huggingface.co:444/a'),('http','http://huggingface.co/a'),('login','https://huggingface.co/login')]:rejects('URL_'+name,lambda u=bad:c.checked_url(u,m))
    rejects('initial_binding',lambda:c.checked_url('https://huggingface.co/other',m,True))
    def run(name,mode='normal',fail=None):
        p=root/name;p.mkdir();calls=[];c.fetch(p,m,dict(start=c.clock(),work_deadline=c.clock()+30),factory(mode,calls,m),fail);r=c.replay(p);records[name]=r;return p,calls,r
    p,calls,r=run('complete');check('exact_full_digest',r['state']=='COMPLETE' and (p/'copy.mp4').read_bytes()==DATA)
    check('HEAD_not_followed_GET_starts_resolve',[(x['method'],x['host']) for x in calls if x['event']=='SEND']==[('HEAD','huggingface.co'),('GET','huggingface.co'),('GET','cas-bridge.xethub.hf.co')])
    check('identity_and_reservation',r['responsibility']==len(DATA) and r['complete']['sha256']==m['candidates'][0]['publisher_lfs_sha256'])
    for mode in ('headsha','badhost','duplicate','length','encoding','short','digest'):
        p,calls,r=run(mode,mode);check(mode+'_reject',r['state']!='COMPLETE' and not (p/'copy.mp4').exists())
        if mode=='headsha':check('bad_HEAD_GET0',not any(x.get('method')=='GET' for x in calls))
        if mode in ('badhost','duplicate','length','encoding'):check(mode+'_body0',not any(x['event']=='READ' for x in calls))
    p,calls,r=run('fsync',fail='HEAD_VALIDATED');check('HEAD_fsync_GET0',not any(x.get('method')=='GET' for x in calls) and r['metadata'])
    rejects('duplicate_head',lambda:c.validate_head(200,[('Content-Length','32768'),('content-length','32768')],m['candidates'][0]))
    points=[(4*i,4) for i in range(60)];tb=Q(1);T=Q(240);result=c.qualify(points,tb,Q(1,4),True,True)
    check('dynamic_F_T_CFR',result['F']==60 and result['T']=='240' and result['layer']=='CFR')
    check('N_left_closed_right_open',c.assign_uniform(points,tb,T)[0]==0 and c.assign_uniform(points,tb,T)[-1]==58)
    check('duration_gate',c.qualify(points,Q(1,10),Q(5,2),True,True)['gate']=='DURATION_OR_FRAME_GATE_FAILED')
    check('origin_hold',c.qualify(points,tb,Q(1,4),False,True)['clock_status']=='CLOCK_UNKNOWN')
    broken=points.copy();broken[3]=(broken[3][0]+1,4);check('gap_hold',c.qualify(broken,tb,Q(1,4),True,True)['clock_status']=='CLOCK_UNKNOWN')
    ix=c.sample_indices(60);mapping=c.PTSMap(ix,points,tb,Q(1,4),T);check('dynamic_map48',len(mapping.times(ix,.25,2))==24)
    rejects('request_wrong_order',lambda:mapping.times(list(reversed(ix)),.25,2));rejects('request_wrong_fps',lambda:mapping.times(ix,.5,2))
    class Base:
        def __init__(self,image_processor=None,tokenizer=None,video_processor=None,chat_template=None):self.image_processor=image_processor;self.tokenizer=tokenizer;self.video_processor=video_processor or SimpleNamespace(merge_size=2);self.chat_template=chat_template
        def __call__(self,**kw):m=kw['video_metadata'][0];return self._calculate_timestamps(m.frames_indices,m.fps,2)
        def _calculate_timestamps(self,indices,video_fps,merge_size=2):return [(indices[i]+indices[i+1])/(2*video_fps) for i in range(0,48,2)]
    base=Base();p=c.bind(base,mapping);kw=dict(videos=[SimpleNamespace(shape=(48,192,288,3))],text=['owned'],video_metadata=[SimpleNamespace(total_num_frames=60,duration=240.,width=288,height=192,frames_indices=ix,fps=.25)])
    check('same_binding_path',p(**kw)==[float(x) for x in mapping.times(ix,.25,2)] and '_calculate_timestamps' not in base.__dict__)
    rejects('single_request_reuse',lambda:p(**kw))
    trace=[dict(indices=ix,fps=.25,merge=2,returned=[0]*24)];c.validate_callback(trace,ix,.25);check('actual_callback_binding',True)
    rejects('callback_changed_indices',lambda:c.validate_callback(trace,list(reversed(ix)),.25));rejects('callback_changed_fps',lambda:c.validate_callback(trace,ix,.5))
    f=root/'meter.fixture';f.write_bytes(b'12345');meter=c.Meter(f,root,'fixture');check('meter_read',meter.read(3)==b'123');meter.seek(0);check('meter_seek_not_refund',meter.read(2)==b'12' and meter.total==5);meter.close()
    write=c.write;write(root/'suite.json',dict(status='PASS',assertions=checks,actual_network=0,actual_media_decode=0,actual_processor_calls=0,fixtures=records))
