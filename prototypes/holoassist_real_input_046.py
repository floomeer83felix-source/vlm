"""046 one fixed HoloAssist distribution copy: bounded HTTPS and CPU inputs.

No SDK/retry/Range, credentials, labels, models or GPU. Only040 Job/Process
platform is imported as a library; old task entrypoints are never called.
"""
from collections import Counter
from fractions import Fraction as Q
import bisect
import ctypes as C
import hashlib
import http.client
import importlib.util
import json
import math
import os
from pathlib import Path
import ssl
import struct
import sys
import time
from types import MappingProxyType
from urllib.parse import urlsplit

MANIFEST_SHA='d79a7eeb7ec57e95c4c1c60418db12b794f14736891ed3046fd58712fed63ef9'
EXPECTED=114523050
LFS_SHA='8ee70b404c996a1c823b65744debc9763564ac6bb5e57835f15be8c07d3bac98'
CAP=128*1024**2
READ_CAP=512*1024**2
clock=time.perf_counter

def require(x,why):
    if not x:raise ValueError(why)
def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def digest(x):return sha(pack(x))
def read(p):return json.loads(Path(p).read_bytes())
def write(p,x):
    data=pack(x);require(len(data)<=8*1024**2,'RECEIPT_CAP')
    with open(p,'xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
def append(p,x):
    with open(p,'ab') as f:f.write(pack(x)+b'\n');f.flush();os.fsync(f.fileno())
def platform():
    spec=importlib.util.spec_from_file_location('platform040',Path(__file__).with_name('auditable_runner_040.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def offline_guard():
    def audit(event,args):
        if event.startswith('socket.') or event in ('subprocess.Popen','os.system'):raise PermissionError('OFFLINE_046')
    sys.addaudithook(audit)

class Ledger:
    def __init__(self,root,fail=None):self.path=Path(root)/'events.jsonl';self.seq=0;self.previous='0'*64;self.fail=fail
    def add(self,event,**kw):
        require(self.seq<20000,'EVENT_CAP');b=dict(seq=self.seq+1,previous=self.previous,event=event,t=clock(),**kw);h=digest(b);line=pack(dict(body=b,sha256=h))+b'\n';require(len(line)<=2048,'LINE_CAP')
        with open(self.path,'ab') as f:
            f.write(line);f.flush()
            if event==self.fail:raise OSError('INJECTED_FSYNC_FAILURE')
            os.fsync(f.fileno())
        self.seq+=1;self.previous=h

def headers(raw):
    out={};critical={'content-length','content-encoding','transfer-encoding','etag','x-linked-size','x-linked-etag','location','content-type'}
    for k,v in raw:
        k=k.lower();require(k not in critical or k not in out,'DUPLICATE_CRITICAL_HEADER');out[k]=v
    require(out.get('content-encoding','identity').lower()=='identity','ENCODING')
    require('text/html' not in out.get('content-type','').lower(),'HTML_OR_TERMS')
    return out
def positive(value):require(isinstance(value,str) and value.isascii() and value.isdigit() and int(value)>0,'MISSING_LENGTH');return int(value)
def linked(h,item,required=False):
    if required or 'x-linked-size' in h:require(positive(h.get('x-linked-size'))==item['expected_bytes'],'LINKED_SIZE')
    if required or 'x-linked-etag' in h:require(h.get('x-linked-etag','').strip('"')==item['publisher_lfs_sha256'],'LINKED_DIGEST')
def validate_head(status,raw,item):
    h=headers(raw);require(status in (200,302,307),'HEAD_STATUS')
    if status==200:require(positive(h.get('content-length'))==item['expected_bytes'],'HEAD_SIZE');linked(h,item)
    else:linked(h,item,True)
    require(item['expected_bytes']<=CAP,'BODY_CAP');return h
def validate_final(status,raw,item):
    h=headers(raw);require(status==200,'GET_STATUS');require('transfer-encoding' not in h,'TRANSFER_ENCODING')
    require(positive(h.get('content-length'))==item['expected_bytes'],'GET_SIZE');linked(h,item);return h
def checked_url(url,manifest,initial=False):
    require(isinstance(url,str) and url.startswith('https://'),'HTTPS_ABSOLUTE_ONLY');u=urlsplit(url)
    require(u.scheme=='https' and u.hostname in manifest['redirect_host_allowlist'] and u.port in (None,443) and not u.username and not u.password and not u.fragment,'URL_SCOPE')
    require(not any(x in u.path.lower().split('/') for x in ('login','auth','oauth','authorize','signin')),'AUTH_PATH')
    if initial:require(url==manifest['candidates'][0]['media_url'],'EXACT_INITIAL_URL')
    return u

def fetch(root,manifest,config,factory=None,fail=None):
    root=Path(root);item=manifest['candidates'][0];write(root/'attempt.claim',dict(candidate='H01',expected_bytes=item['expected_bytes'],expected_sha256=item['publisher_lfs_sha256'],start=config['start'],cap=CAP))
    j=Ledger(root,fail);connections=[];counter=0
    def request(url,method,hop):
        nonlocal counter
        u=checked_url(url,manifest,initial=method=='HEAD' or hop==0);counter+=1;require(counter<=4,'SEND_CAP')
        j.add('SEND_INTENT',method=method,hop=hop,host=u.hostname,url_sha256=sha(url.encode()))
        left=config['work_deadline']-clock();require(left>0,'WORK_DEADLINE')
        context=ssl.create_default_context();require(context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname,'TLS_VERIFY')
        conn=(factory or http.client.HTTPSConnection)(u.hostname,443,timeout=min(15,left),context=context);connections.append(conn);conn.connect()
        sock=conn.sock;sock.settimeout(min(30,max(.001,config['work_deadline']-clock())))
        path=u.path+('?' +u.query if u.query else '')
        conn.request(method,path,headers={'Accept-Encoding':'identity','Connection':'close','User-Agent':'VLM-046-research'})
        j.add('SENT',method=method,hop=hop,host=u.hostname,url_sha256=sha(url.encode()))
        response=conn.getresponse();value=dict(url=url,status=response.status,headers=list(response.getheaders()));require(len(pack(value))<=65536,'HEADER_FILE_CAP')
        name=f'headers-{counter:02d}.json';write(root/name,value);j.add('RESPONSE',method=method,hop=hop,host=u.hostname,url_sha256=sha(url.encode()),status=response.status,file=name,file_sha256=digest(value))
        return response,sock,value,conn
    result=dict(state='FAILED',error=None);returned=written=0
    try:
        url=item['media_url'];j.add('HEAD_INTENT');response,_,raw,conn=request(url,'HEAD',0)
        h=validate_head(raw['status'],raw['headers'],item);j.add('HEAD_VALIDATED',bytes=item['expected_bytes'],linked_sha256=h.get('x-linked-etag'),etag=h.get('etag'),host=urlsplit(url).hostname)
        response.close();conn.close();j.add('RESERVE',bytes=item['expected_bytes'],cap=CAP);j.add('GET_INTENT',responsibility=item['expected_bytes'])
        seen=set()
        for hop in range(3):
            require(url not in seen,'REDIRECT_LOOP');seen.add(url)
            response,sock,raw,conn=request(url,'GET',hop)
            if raw['status'] in (302,307):
                h=headers(raw['headers']);linked(h,item);require(hop<2,'REDIRECT_CAP');require('location' in h,'MISSING_LOCATION');target=h['location'];checked_url(target,manifest)
                j.add('REDIRECT',hop=hop,status=raw['status'],next_host=urlsplit(target).hostname,next_url_sha256=sha(target.encode()));response.close();conn.close();url=target;continue
            final=validate_final(raw['status'],raw['headers'],item);j.add('GET_VALIDATED',bytes=item['expected_bytes'],host=urlsplit(url).hostname,etag=final.get('etag'),etag_equals_lfs=final.get('etag','').strip('"')==item['publisher_lfs_sha256'])
            checksum=hashlib.sha256()
            with open(root/'media.partial','xb') as f:
                while returned<item['expected_bytes']:
                    left=config['work_deadline']-clock();require(left>0,'WORK_DEADLINE');sock.settimeout(min(30,left));n=min(1024**2,item['expected_bytes']-returned)
                    j.add('READ_INTENT',requested=n,returned_before=returned,written_before=written)
                    block=response.read(n);require(block and len(block)<=n,'SHORT_OR_OVERSIZE_READ');returned+=len(block);require(returned<=CAP,'BODY_CAP');j.add('READ_RETURN',total=returned,size=len(block))
                    f.write(block);f.flush();os.fsync(f.fileno());checksum.update(block);written+=len(block);j.add('PROGRESS',returned=returned,written=written)
            require(written==item['expected_bytes'] and checksum.hexdigest()==item['publisher_lfs_sha256'],'LFS_SHA256_MISMATCH')
            j.add('VERIFIED',bytes=written,sha256=checksum.hexdigest());os.rename(root/'media.partial',root/'copy.mp4');j.add('COMPLETE',bytes=written,sha256=checksum.hexdigest());result=dict(state='COMPLETE');break
    except Exception as e:
        result['error']=type(e).__name__+':'+str(e)[:160]
        if 'FSYNC_FAILURE' not in str(e):
            try:j.add('ABORT',reason=result['error'])
            except OSError:pass
    finally:
        for conn in connections:conn.close()
    write(root/'worker-result.json',result)

def replay(root):
    root=Path(root);events=[];prev='0'*64;bad=False
    if (root/'events.jsonl').exists():
        for line in (root/'events.jsonl').read_bytes().splitlines(keepends=True):
            try:
                require(line.endswith(b'\n'),'HALF_LINE');x=json.loads(line);b=x['body'];require(b['seq']==len(events)+1 and b['previous']==prev and x['sha256']==digest(b),'CHAIN');events.append(b);prev=x['sha256']
            except (ValueError,KeyError,TypeError):bad=True;break
    metadata=[]
    for e in events:
        if e['event']=='RESPONSE':
            try:
                value=read(root/e['file']);require(digest(value)==e['file_sha256'],'HEADER_BINDING');metadata.append(dict(method=e['method'],hop=e['hop'],host=e['host'],url_sha256=e['url_sha256'],status=e['status'],headers=value['headers']))
            except (OSError,ValueError):bad=True
    complete=next((e for e in events if e['event']=='COMPLETE'),None);reserve=next((e for e in events if e['event']=='RESERVE'),None);intent=any(e['event']=='GET_INTENT' for e in events)
    return dict(state='COMPLETE' if complete and not bad and (root/'copy.mp4').is_file() else 'FAILED_OR_UNKNOWN',complete=complete,metadata=metadata,journal_unknown=bad,intents=[e for e in events if e['event']=='SEND_INTENT'],sent=[e for e in events if e['event']=='SENT'],redirects=[e for e in events if e['event']=='REDIRECT'],returned_lower=max((e['total'] for e in events if e['event']=='READ_RETURN'),default=0),written_lower=max((e['written'] for e in events if e['event']=='PROGRESS'),default=0),responsibility=reserve['bytes'] if reserve else CAP if intent or bad else 0,exactness='COMPLETE_APPLICATION_BODY' if complete and not bad else 'UNKNOWN_PENDING_BODY' if intent or bad else 'NO_GET_INTENT',events=len(events))

class Meter:
    """Actual Python file-read returns, shared across both decode stages."""
    def __init__(self,path,root,phase):
        self.f=open(path,'rb');self.root=Path(root);self.phase=phase;self.path=self.root/'cpu-reads.jsonl';self.total=0;self.seeks=0
        if self.path.exists():
            for line in self.path.read_bytes().splitlines():self.total=json.loads(line)['total']
    def read(self,n=-1):
        if n<0:n=os.fstat(self.f.fileno()).st_size-self.f.tell()
        require(self.total+n<=READ_CAP,'CPU_READ_CAP');b=self.f.read(n);self.total+=len(b);append(self.path,dict(phase=self.phase,returned=len(b),total=self.total));return b
    def readinto(self,b):data=self.read(len(b));b[:len(data)]=data;return len(data)
    def seek(self,offset,whence=0):self.seeks+=1;return self.f.seek(offset,whence)
    def tell(self):return self.f.tell()
    def readable(self):return True
    def seekable(self):return True
    def writable(self):return False
    def close(self):self.f.close()

def atoms(meter):
    size=meter.seek(0,2);result=dict(videos=[],movie=None);count=0
    def walk(start,end,track=None):
        nonlocal count
        at=start
        while at<end:
            count+=1;require(count<=20000,'ATOM_CAP');meter.seek(at);b=meter.read(8);require(len(b)==8,'ATOM_HEADER');n,kind=struct.unpack('>I4s',b);h=8
            if n==1:n=struct.unpack('>Q',meter.read(8))[0];h=16
            if n==0:n=end-at
            require(n>=h and at+n<=end,'ATOM_SIZE')
            if kind==b'trak':
                t=dict(edits=[]);walk(at+h,at+n,t)
                if t.get('handler')=='vide':result['videos'].append(t)
            elif kind in (b'moov',b'mdia',b'edts'):walk(at+h,at+n,track)
            elif kind in (b'mvhd',b'mdhd',b'tkhd',b'hdlr',b'elst'):
                require(n-h<=65536,'ATOM_METADATA_CAP');d=meter.read(n-h);v=d[0]
                if kind in (b'mvhd',b'mdhd'):
                    pos=20 if v==1 else 12;scale=struct.unpack_from('>I',d,pos)[0];duration=struct.unpack_from('>Q' if v==1 else '>I',d,pos+4)[0];x=dict(timescale=scale,duration=duration)
                    if kind==b'mvhd':result['movie']=x
                    elif track is not None:track['media']=x
                elif track is not None and kind==b'tkhd':track['id']=struct.unpack_from('>I',d,20 if v==1 else 12)[0]
                elif track is not None and kind==b'hdlr':track['handler']=d[8:12].decode('ascii')
                elif track is not None and kind==b'elst':
                    entries=struct.unpack_from('>I',d,4)[0];require(entries<=1024,'EDIT_CAP');p=8
                    for _ in range(entries):fmt='>Qqhh' if v==1 else '>Iihh';track['edits'].append(list(struct.unpack_from(fmt,d,p)));p+=struct.calcsize(fmt)
            at+=n
    walk(0,size);return result

def sample_indices(F):return [round(Q(j*(F-1),47)) for j in range(48)]
def assign_uniform(points,tb,T):
    starts=[Q(p)*tb for p,d in points];out=[]
    for j in range(48):
        u=Q(j)*T/48;i=bisect.bisect_right(starts,u)-1
        require(i>=0 and starts[i]<=u<Q(points[i][0]+points[i][1])*tb,'N_UNCOVERED');out.append(i)
    return out
def qualify(points,tb,rate,origin,endpoint,provenance=True):
    reasons=[]
    if not origin:reasons.append('ORIGIN_EDIT_UNKNOWN')
    if not endpoint:reasons.append('VIDEO_BOUNDARY_UNKNOWN')
    if not provenance:reasons.append('ENCODED_PTS_OR_DURATION_UNPROVEN')
    if not points:reasons.append('NO_FRAMES')
    for i,(p,d) in enumerate(points):
        if p is None or d is None or d<=0:reasons.append('MISSING_PTS_DURATION');break
        if i and (p<=points[i-1][0] or p!=points[i-1][0]+points[i-1][1]):reasons.append('GAP_OVERLAP_ORDER');break
    if reasons:return dict(clock_status='CLOCK_UNKNOWN',reasons=sorted(set(reasons)))
    T=Q(points[-1][0]+points[-1][1])*tb;F=len(points)
    if not 180<=T<=900 or F<48:return dict(clock_status='CLOCK_CERTIFIED',gate='DURATION_OR_FRAME_GATE_FAILED',T=str(T),F=F)
    ix=sample_indices(F);d=max(abs(Q(i)/rate-Q(points[i][0])*tb) for i in ix);intervals=[points[i][0]-points[i-1][0] for i in range(1,F)];span=max(intervals)-min(intervals)
    layer='HIGH_OFFSET' if span>1 and d>=Q(1,4) else 'CFR' if span<=1 and d<=Q(1,50) else 'OTHER'
    return dict(clock_status='CLOCK_CERTIFIED',gate='PASS',T=str(T),F=F,layer=layer,d=str(d),d_seconds=float(d),interval_tick_span=span,indices=ix,sampled_pts=[points[i][0] for i in ix],n_indices=assign_uniform(points,tb,T))

def open_video(av,meter):return av.open(meter,mode='r',format='mov',hwaccel=None,container_options={'ignore_editlist':'0','enable_drefs':'0','protocol_whitelist':'file'},buffer_size=32768)
def scan(root,config):
    root=Path(root);sys.path.insert(0,config['site']);import av
    av.logging.set_level(av.logging.PANIC);m=Meter(root/'copy.mp4',root,'scan');start=clock();result=dict(clock_status='CLOCK_UNKNOWN');points=[];packet_info={};missing=0;mismatch=0
    try:
        a=atoms(m);require(len(a['videos'])==1,'ONE_VIDEO_TRACK');video=a['videos'][0];m.seek(0)
        with open_video(av,m) as container:
            require(len(container.streams.video)==1,'ONE_VIDEO_STREAM');s=container.streams.video[0];s.thread_count=4;s.thread_type='SLICE';tb=Q(s.time_base);rate=Q(s.average_rate)
            with open(root/'frame-clock.bin','xb') as f:
                for packet in container.demux(video=0):
                    if packet.size:
                        if packet.pts is None:missing+=1
                        else:packet_info[packet.pts]=packet.duration
                    for frame in packet.decode():
                        require(clock()-start<590 and len(points)<1000000,'SCAN_RESOURCE_CAP');require(Q(frame.time_base)==tb,'TIMEBASE_CHANGED')
                        p,d=frame.pts,frame.duration;points.append((p,d))
                        if p not in packet_info or d!=packet_info[p]:mismatch+=1
                        f.write(struct.pack('<qq',p if p is not None else -(2**63),d or 0));del frame
            require(bool(points),'NO_DECODED_FRAMES');last=points[-1];T=Q(last[0]+last[1])*tb if last[0] is not None and last[1] else None
            edits=video['edits'];identity=not edits or len(edits)==1 and edits[0][1:]==[0,1,0] and T is not None and abs(Q(edits[0][0],a['movie']['timescale'])-T)<=Q(1,a['movie']['timescale'])
            origin=identity and video.get('id')==s.id and points[0][0]==0 and s.start_time==0 and tb==Q(1,video['media']['timescale'])
            endpoint=T is not None and s.duration is not None and abs(T-s.duration*tb)<=tb and abs(T-Q(video['media']['duration'],video['media']['timescale']))<=tb
            result.update(qualify(points,tb,rate,origin,endpoint,missing==mismatch==0));result.update(time_base=str(tb),average_rate=str(rate),source_width=s.codec_context.width,source_height=s.codec_context.height,stream_duration=s.duration,stream_start=s.start_time,container_duration=container.duration,container_start=container.start_time,video_metadata=video,movie=a['movie'],packet_missing_pts=missing,frame_provenance_mismatch=mismatch,decoded_frames=len(points),video_end=str(T),container_minus_video=str(Q(container.duration,1000000)-T) if container.duration is not None and T is not None else None,movie_minus_video=str(Q(a['movie']['duration'],a['movie']['timescale'])-T) if a['movie'] and T is not None else None)
    except Exception as e:result['error']=type(e).__name__+':'+str(e)[:180]
    finally:m.close()
    result.update(wall=clock()-start,read_return_total=m.total,seek_calls=m.seeks);write(root/'clock.json',result)

class PTSMap:
    def __init__(self,indices,points,tb,fps,T):
        self.indices=tuple(indices);self.F=len(points);self.fps=float(fps);self.T=Q(T)
        require(self.F>=48 and len(self.indices)==48 and all(type(i) is int and 0<=i<self.F for i in self.indices) and all(a<b for a,b in zip(self.indices,self.indices[1:])),'DYNAMIC_INDICES')
        require(math.isfinite(self.fps) and self.fps>0 and self.T>0,'DYNAMIC_CLOCK')
        values=[Q(p)*tb for p,d in points];require(values[0]>=0 and all(a<b for a,b in zip(values,values[1:])),'PTS_ORDER')
        self.mapping=MappingProxyType(dict(enumerate(values)));self.identity=digest(dict(F=self.F,T=str(self.T),fps=self.fps,indices=self.indices,pts=[str(x) for x in values]))
    def times(self,indices,fps,merge):
        ix=indices.tolist() if hasattr(indices,'tolist') else list(indices)
        require(all(type(i) is int for i in ix) and tuple(ix)==self.indices,'CALLBACK_INDICES')
        require(type(merge) is int and merge==2 and fps is not None and math.isfinite(float(fps)) and float(fps)==self.fps,'CALLBACK_CLOCK')
        return [(self.mapping[ix[j]]+self.mapping[ix[j+1]])/2 for j in range(0,48,2)]

def bind(base,mapping):
    class ScopedPTSProcessor(type(base)):
        def __call__(self,**kwargs):
            require(not self._used,'SINGLE_REQUEST');self._used=True
            require(len(kwargs['videos'])==len(kwargs['video_metadata'])==len(kwargs['text'])==1 and tuple(kwargs['videos'][0].shape)==(48,192,288,3),'SINGLE48_PAYLOAD')
            m=kwargs['video_metadata'][0];require(m.total_num_frames==self._mapping.F and m.duration==float(self._mapping.T) and m.width==288 and m.height==192,'REAL_F_T_BINDING')
            self._mapping.times(m.frames_indices,m.fps,self.video_processor.merge_size)
            return super().__call__(**kwargs)
        def _calculate_timestamps(self,indices,video_fps,merge_size=2):
            raw=self._mapping.times(indices,video_fps,merge_size);self._trace.append(dict(indices=list(indices),fps=float(video_fps),merge=merge_size,raw=[str(x) for x in raw],map=self._mapping.identity));return [float(x) for x in raw]
    p=ScopedPTSProcessor(image_processor=base.image_processor,tokenizer=base.tokenizer,video_processor=base.video_processor,chat_template=base.chat_template);p._mapping=mapping;p._trace=[];p._used=False;return p

def asset_config_identity(base,versions):return digest(dict(model='Qwen3-VL-4B',versions=versions,image=base.image_processor.to_dict(),video=base.video_processor.to_dict(),tokenizer=sha(base.tokenizer.backend_tokenizer.to_str().encode()),template=base.chat_template))
def boundary(batch,torch,common):
    state={k:v.to(torch.bfloat16) if k in ('pixel_values','pixel_values_videos') and torch.is_tensor(v) and v.is_floating_point() else v for k,v in batch.items()};parts={}
    for k,v in state.items():
        if torch.is_tensor(v):require(v.device.type=='cpu','CPU_ONLY');parts[k]=dict(shape=list(v.shape),dtype=str(v.dtype),device=str(v.device),sha256=sha(v.contiguous().view(torch.uint8).numpy().tobytes()))
        else:parts[k]=dict(value=v)
    return state,dict(kwargs=parts,full_hash=digest(dict(kwargs=parts,common=common)),visual_hash=digest({k:v for k,v in parts.items() if k in ('pixel_values_videos','video_grid_thw')}))
def tensor_equal(a,b,torch,keys):
    for k in keys:
        if k not in a or k not in b:return False
        x,y=a[k],b[k]
        if torch.is_tensor(x):
            if x.dtype!=y.dtype or x.shape!=y.shape or x.device!=y.device or not torch.equal(x,y):return False
        elif x!=y:return False
    return True
def validate_callback(trace,indices,fps):
    require(len(trace)==1 and trace[0]['indices']==list(indices) and trace[0]['fps']==float(fps) and trace[0]['merge']==2 and len(trace[0].get('returned',[]))==24,'ACTUAL_CALLBACK_BINDING')

def cpu_policy(root,config):
    root=Path(root).resolve();allowed=[root,Path(config['site']).resolve(),Path(config['model']).resolve(),Path(sys.base_prefix).resolve(),Path(__file__).resolve().parent]
    def inside(p,rs):return any(p==r or r in p.parents for r in rs)
    def audit(event,args):
        if event.startswith('socket.') or event in ('subprocess.Popen','os.system'):raise PermissionError('CPU_OFFLINE_046')
        if event=='open' and not isinstance(args[0],int):
            raw=os.fsdecode(args[0])
            if os.path.normcase(raw)==os.path.normcase(os.devnull):return
            p=Path(raw).resolve();mode=args[1];flags=args[2];writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_CREAT|os.O_WRONLY|os.O_RDWR))
            if writing:require(inside(p,[root]),'WRITE_SCOPE')
            else:require(inside(p,allowed) and (p.suffix.lower() not in ('.safetensors','.bin','.pt','.pth','.gguf','.onnx') or p==root/'frame-clock.bin'),'READ_OR_WEIGHT_SCOPE')
    sys.addaudithook(audit)

def api(root,config):
    offline_guard();sys.path.insert(0,config['site']);import av
    from PIL import Image
    from importlib import metadata
    require(all(hasattr(av.VideoFrame,n) for n in ('pts','duration','time_base')) and 'hwaccel' in av.open.__doc__,'CPU_API')
    binaries=[]
    for name in ('av._core','av.video.frame','av.video.codeccontext'):
        p=Path(sys.modules[name].__file__);binaries.append(dict(module=name,size=p.stat().st_size,sha256=sha(p.read_bytes())))
    p=Path(config['site'])/'transformers/models/qwen3_vl/processing_qwen3_vl.py';data=p.read_bytes()
    versions={name:metadata.version(name) for name in ('torch','transformers','numpy','Pillow')}
    input_ready=versions['torch']=='2.5.1' and versions['transformers']=='4.57.6' and versions['numpy']=='1.26.4' and sha(data)=='efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9' and Path(config['model']).is_dir()
    write(Path(root)/'api.json',dict(av=av.__version__,versions=versions,binaries=binaries,processor_source=dict(bytes=len(data),sha256=sha(data)),input_ready=input_ready,bilinear=bool(Image.Resampling.BILINEAR),torch_imported='torch' in sys.modules))

def inputs(root,config,event_name):
    root=Path(root);cpu_policy(root,config);sys.path.insert(0,config['site']);import av,numpy as np
    from PIL import Image
    av.logging.set_level(av.logging.PANIC);info=read(root/'clock.json');require(info.get('layer')=='HIGH_OFFSET' and info.get('gate')=='PASS','CLOCK_GATE')
    F=info['F'];T=Q(info['T']);tb=Q(info['time_base']);rate=Q(info['average_rate']);raw=(root/'frame-clock.bin').read_bytes();require(len(raw)==16*F,'CLOCK_TABLE_BINDING');points=[struct.unpack_from('<qq',raw,16*i) for i in range(F)]
    ix=info['indices'];nx=info['n_indices'];wanted=set(ix+nx);require(len(wanted)<=96,'FRAME_BUFFER_CAP');buffers={};m=Meter(root/'copy.mp4',root,'selection');decode_start=clock();convert_seconds=0.;letterbox_seconds=0.;native_decode_seconds=0.;count=0
    with open_video(av,m) as container:
        require(len(container.streams.video)==1,'ONE_VIDEO_TRACK');s=container.streams.video[0];s.thread_count=4;s.thread_type='SLICE'
        iterator=iter(container.decode(video=0))
        while True:
            tick=clock()
            try:frame=next(iterator)
            except StopIteration:native_decode_seconds+=clock()-tick;break
            native_decode_seconds+=clock()-tick
            require(clock()-decode_start<590 and count<F,'SELECTION_RESOURCE');require((frame.pts,frame.duration)==points[count] and Q(frame.time_base)==tb,'SECOND_PASS_CLOCK_MISMATCH')
            if count in wanted:
                t=clock();rgb=frame.to_ndarray(format='rgb24');convert_seconds+=clock()-t;t=clock();image=Image.fromarray(rgb);w,h=image.size;scale=min(288/w,192/h);resized=image.resize((max(1,round(w*scale)),max(1,round(h*scale))),Image.Resampling.BILINEAR);canvas=Image.new('RGB',(288,192),(0,0,0));canvas.paste(resized,((288-resized.width)//2,(192-resized.height)//2));buffers[count]=np.array(canvas,dtype=np.uint8);letterbox_seconds+=clock()-t
            count+=1;del frame
    m.close();require(count==F and len(buffers)==len(wanted),'SECOND_PASS_COMPLETE')
    shared_start=clock();b0=np.stack([buffers[i] for i in ix]);nframes=np.stack([buffers[i] for i in nx]);mapping=PTSMap(ix,points,tb,rate,T)
    plan=dict(F=F,T=str(T),source_fps=str(rate),indices=ix,n_indices=nx,n_targets=[str(Q(j)*T/48) for j in range(48)],n_duplicate_count=48-len(set(nx)),n_different_indices=sum(a!=b for a,b in zip(ix,nx)),n_index_displacements=[b-a for a,b in zip(ix,nx)],rgb_sha256=dict(B0=sha(b0.tobytes()),N=sha(nframes.tobytes())),asset_sha256=read(root/'fetch-replay.json')['complete']['sha256'],selection_inclusive_seconds=clock()-decode_start,native_decode_seconds=native_decode_seconds,convert_seconds=convert_seconds,letterbox_seconds=letterbox_seconds,shared_stack_map_seconds=clock()-shared_start,media_read_return_total=m.total,seek_calls=m.seeks,map_identity=mapping.identity)
    write(root/'input-plan.json',plan);signal_event(event_name)
    import torch,transformers
    require(torch.__version__=='2.5.1' and transformers.__version__=='4.57.6' and np.__version__=='1.26.4','CPU_VERSION_HOLD')
    from transformers import AutoProcessor
    from transformers.video_utils import VideoMetadata
    torch.set_num_threads(4);torch.set_num_interop_threads(1);require(not torch.cuda.is_initialized(),'CUDA_INITIALIZED')
    base=AutoProcessor.from_pretrained(config['model'],local_files_only=True,trust_remote_code=False);versions=dict(torch=torch.__version__,transformers=transformers.__version__,numpy=np.__version__);common=asset_config_identity(base,versions);original=type(base)._calculate_timestamps;calls=0;states={};records=[]
    def prepare(arm,phase):
        nonlocal calls
        require(calls<5,'PROCESSOR_CAP');calls+=1;append(root/'processor-calls.jsonl',dict(ordinal=calls,arm=arm,phase=phase))
        nf=48 if arm=='N' else F;declared=Q(48)/T if arm=='N' else rate;indices=list(range(48)) if arm=='N' else ix;array=nframes if arm=='N' else b0
        metadata=VideoMetadata(total_num_frames=nf,fps=float(declared),duration=float(T),width=288,height=192,frames_indices=indices.copy());processor=bind(base,mapping) if arm=='P' else base
        text=base.apply_chat_template([dict(role='system',content='You are a helpful assistant.'),dict(role='user',content=[dict(type='video'),dict(type='text',text='Describe the video.')])],tokenize=False,add_generation_prompt=True)
        traces=[]
        def profile(frame,event,arg):
            if frame.f_code.co_name!='_calculate_timestamps':return
            if event=='call':
                x=frame.f_locals;i=x['indices'];traces.append(dict(indices=i.tolist() if hasattr(i,'tolist') else list(i),fps=float(x['video_fps']),merge=x['merge_size']))
            elif event=='return' and traces:traces[-1]['returned']=list(arg) if arg is not None else None
        sys.setprofile(profile);start=clock()
        try:batch=processor(text=[text],videos=[array.copy()],video_metadata=[metadata],do_sample_frames=False,do_resize=False,return_tensors='pt')
        finally:sys.setprofile(None)
        state,r=boundary(batch,torch,common);decoded=base.tokenizer.decode(state['input_ids'][0].tolist(),skip_special_tokens=False,clean_up_tokenization_spaces=False)
        import re
        times=re.findall(r'<([0-9]+\.[0-9]) seconds>',decoded);stripped=re.sub(r'<[0-9]+\.[0-9] seconds>','<TIME>',decoded)
        expected=mapping.times(ix,float(rate),2) if arm=='P' else [(Q(indices[j])+Q(indices[j+1]))/(2*declared) for j in range(0,48,2)]
        r.update(arm=arm,phase=phase,callback=traces,pts_trace=processor._trace if arm=='P' else [],source_frame_count=F,source_fps_rational=str(rate),declared_total_frames=nf,declared_indices=indices,declared_fps_rational=str(declared),declared_fps=float(declared),duration=str(T),raw_rational=[str(x) for x in expected],timecodes=times,timecode_error=[float(a)-float(b) for a,b in zip(times,expected)],grid=state['video_grid_thw'].tolist(),visual_tokens=int(state['video_grid_thw'].prod())//4,input_ids=state['input_ids'].tolist(),attention_mask=state['attention_mask'].tolist(),roundtrip=base.tokenizer.encode(decoded,add_special_tokens=False)==state['input_ids'][0].tolist(),stripped=stripped,base_identity_before=common,base_identity_after=asset_config_identity(base,versions),base_method_unchanged=type(base)._calculate_timestamps is original,wall=clock()-start)
        require(not torch.cuda.is_initialized(),'CUDA_INITIALIZED');return state,r
    try:
        _,probe=prepare('B0','probe');require(len(probe['callback'])==1 and len(probe['timecodes'])==24,'PROBE_API');write(root/'input-probe.json',probe)
    except Exception as e:write(root/'input-error.json',dict(stage='probe',error=type(e).__name__+':'+str(e)[:180]));return
    write(root/'input-seal.json',dict(code_sha256=sha(Path(__file__).read_bytes()),plan_sha256=digest(plan),base_identity=common,prompt='Describe the video.',order=['B0','P','N']))
    for arm in ('B0','P','N'):
        try:
            state,r=prepare(arm,'formal');states[arm]=state;r['status']='PASS'
            require(r['grid']==[[24,12,18]] and r['visual_tokens']==1296 and r['base_identity_before']==r['base_identity_after'] and r['base_method_unchanged'] and r['roundtrip'],'INPUT_BOUNDARY_GATE')
            validate_callback(r['callback'],r['declared_indices'],r['declared_fps']);require(len(r['timecodes'])==24 and r['timecodes']==[f'{float(t):.1f}' for t in r['callback'][0]['returned']],'NATIVE_TIMECODE_FORMAT')
            if arm=='P':
                r['visual_equal_B0']=tensor_equal(state,states['B0'],torch,('pixel_values_videos','video_grid_thw'));r['text_only_difference']=r['stripped']==records[0]['stripped'] and set(state)=={'input_ids','attention_mask','pixel_values_videos','video_grid_thw'} and state['input_ids'].shape==state['attention_mask'].shape and bool(torch.all(state['attention_mask']==1));require(r['visual_equal_B0'] and r['text_only_difference'] and len(r['pts_trace'])==1,'PAIRED_GATE')
            r['equivalent_to']=[a for a,b in states.items() if set(state)==set(b) and tensor_equal(state,b,torch,state.keys())]
            r['classification']='INPUT_EQUIVALENT_AFTER_NATIVE_QUANTIZATION' if arm=='P' and 'B0' in r['equivalent_to'] else 'MEASURED'
            records.append(r);append(root/'input-records.jsonl',r)
        except Exception as e:
            append(root/'input-records.jsonl',dict(arm=arm,status='FAIL',error=type(e).__name__+':'+str(e)[:180]));break
    write(root/'input-complete.json',dict(calls=calls,rows=len(records),cuda_initialized=torch.cuda.is_initialized(),base_identity_before=common,base_identity_after=asset_config_identity(base,versions),versions=versions))

def event_api():
    from ctypes import wintypes as W
    k=C.WinDLL('kernel32',use_last_error=True)
    for n,args,ret in [('CreateEventW',[W.LPVOID,W.BOOL,W.BOOL,W.LPCWSTR],W.HANDLE),('OpenEventW',[W.DWORD,W.BOOL,W.LPCWSTR],W.HANDLE),('SetEvent',[W.HANDLE],W.BOOL),('WaitForSingleObject',[W.HANDLE,W.DWORD],W.DWORD),('CloseHandle',[W.HANDLE],W.BOOL)]:getattr(k,n).argtypes=args;getattr(k,n).restype=ret
    return k
def signal_event(name):
    k=event_api();h=k.OpenEventW(2,False,name);require(h,'STAGE_EVENT_OPEN')
    try:require(k.SetEvent(h),'STAGE_EVENT_SET')
    finally:k.CloseHandle(h)

def supervise(root,phase,limits,python=None,event_name=None):
    root=Path(root);cfg=read(root/'config.json');require(time.time()+limits[-1]<cfg['deadline'],'PARENT_DEADLINE');start=clock();work=start+limits[0];drain=start+limits[1];finish=start+limits[2]
    write(root/(phase+'-config.json'),dict(start=start,work_deadline=work,active0_deadline=drain,finish_deadline=finish))
    p=platform();job=p.Job(memory=4*1024**3,active_limit=2);child=None;kill=zero=code=None;error=None;stage2=None;event=None;k=None
    if event_name:k=event_api();event=k.CreateEventW(None,True,False,event_name);require(event,'STAGE_EVENT_CREATE')
    bootstrap="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES='',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',HF_HOME="+repr(str(root/'hf'))+",TEMP="+repr(str(root))+",TMP="+repr(str(root))+");sys.path.insert(0,"+repr(cfg['site'])+");sys.path.insert(0,"+repr(str(Path(__file__).parent))+");sys.argv="+repr([str(Path(__file__).resolve()),phase,str(root)]+([event_name] if event_name else []))+";runpy.run_path(sys.argv[0],run_name='__main__')"
    try:
        child=p.Process([python or cfg['python'],'-I','-S','-B','-c',bootstrap],root/(phase+'.log'),job)
        while job.active():
            now=clock()
            if event and stage2 is None and k.WaitForSingleObject(event,0)==0:stage2=now;work=now+285;drain=now+295;finish=now+300
            if now>=work-.1 and kill is None:kill=now;job.kill()
            if now>=drain:raise TimeoutError('DRAIN_DEADLINE')
            time.sleep(.005)
        zero=clock();code=child.poll()
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if zero is None:
            if kill is None:kill=clock();job.kill()
            while job.active() and clock()<drain:time.sleep(.005)
            if not job.active():zero=clock()
        snap=job.snapshot()
        if child:child.close()
        job.close()
        if event:k.CloseHandle(event)
    require(zero is not None and snap['active']==0,'OWN_GROUP_EXIT_UNKNOWN');result=dict(start=start,work_deadline=work,active0_deadline=drain,finish_deadline=finish,kill=kill,active0=zero,exitcode=code,error=error,stage2_start=stage2,**snap);write(root/(phase+'-supervisor.json'),result);result['finished']=clock();result['wall']=result['finished']-start;result['deadline_violation']=bool((kill is not None and kill>work) or zero>drain or result['finished']>finish);return result

if __name__=='__main__':
    phase,root,*args=sys.argv[1:];root=Path(root);cfg=read(root/'config.json')
    if phase=='fetch':
        blob=(root/'manifest.json').read_bytes();require(sha(blob)==MANIFEST_SHA,'MANIFEST_IDENTITY');m=json.loads(blob);require(m['candidates'][0]['expected_bytes']==EXPECTED and m['candidates'][0]['publisher_lfs_sha256']==LFS_SHA,'FIXED_OBJECT');fetch(root,m,read(root/'fetch-config.json'))
    elif phase=='api':api(root,cfg)
    elif phase=='scan':offline_guard();scan(root,cfg)
    elif phase=='inputs':inputs(root,cfg,args[0])
    elif phase in ('suite','blocked'):
        sys.path.insert(0,str(Path(__file__).resolve().parent));from test_holoassist_real_input_046 import suite,blocked
        (suite if phase=='suite' else blocked)(root)
    else:raise ValueError('PHASE')
