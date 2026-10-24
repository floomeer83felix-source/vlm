"""Bounded 042 admission: immutable media list, CPU display-clock evidence only.

No labels, models, processor, hardware decoding, installation or retries.
Only the public040 Win32 Job/Process platform is reused, never its workloads.
"""
import csv
from fractions import Fraction as Q
import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import ssl
import struct
import sys
import time
from urllib.parse import urlsplit

GIB=1024**3
MANIFEST_SHA='24d2177a27a376da48bd6a3c9e7dfa12bf2396066d690056d3e743847d4b760c'

def require(ok,reason):
    if not ok:raise ValueError(reason)
def read(path):return json.loads(Path(path).read_bytes())
def write(path,value):
    with open(path,'x',encoding='utf-8') as f:json.dump(value,f,sort_keys=True,allow_nan=False);f.flush();os.fsync(f.fileno())
def event(root,value):
    with open(Path(root)/'http-events.jsonl','a',encoding='utf-8') as f:f.write(json.dumps(value,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def indices(count):return [round(Q(j*(count-1),47)) for j in range(48)]
def length(headers):
    value=headers.get('content-length','')
    require(value.isascii() and value.isdigit() and int(value)>0,'UNRELIABLE_LENGTH')
    require(headers.get('content-encoding','identity').lower() in ('identity',''),'ENCODING')
    require(not headers.get('transfer-encoding'),'TRANSFER_ENCODING')
    return int(value)
def limit_length(n,remaining):require(n<=4*GIB and n<=remaining,'SIZE_BUDGET')

def request(root,item,method,deadline):
    """Exactly one connection/request; no redirects, retry, Range or proxy fallback."""
    url=urlsplit(item['media_url']);require(url.scheme=='https' and url.hostname=='data.bris.ac.uk' and not url.query and not url.fragment,'URL_ALLOWLIST')
    conn=http.client.HTTPSConnection(url.hostname,timeout=min(15,max(.01,deadline-time.monotonic())),context=ssl.create_default_context())
    event(root,dict(rank=item['candidate_rank'],method=method,state='CONNECT_INTENT'))
    conn.connect()
    conn.sock.settimeout(min(60,max(.01,deadline-time.monotonic())))
    event(root,dict(rank=item['candidate_rank'],method=method,state='SEND_STARTED'))
    conn.request(method,url.path,headers={'Accept-Encoding':'identity','User-Agent':'VLM-042-noncommercial-research','Connection':'close'})
    response=conn.getresponse();headers={k.lower():v for k,v in response.getheaders()}
    event(root,dict(rank=item['candidate_rank'],method=method,state='RESPONSE',status=response.status))
    return conn,response,headers

def fetch(root,rank,remaining,seconds):
    root=Path(root);item=read(root/'manifest.json')[rank-1];start=time.monotonic();deadline=start+seconds
    result=dict(rank=rank,status='NOT_FETCHED',head_sent=False,get_sent=False,body_bytes=0,stop_network=False)
    conn=None
    try:
        conn,response,headers=request(root,item,'HEAD',deadline);result.update(head_sent=True,head_status=response.status)
        if response.status in (401,403,407,451) or 'text/html' in headers.get('content-type','').lower():result['stop_network']=True;raise ValueError('AUTH_OR_TERMS')
        require(response.status==200,'HEAD_STATUS_'+str(response.status));n=length(headers);limit_length(n,remaining)
        etag=headers.get('etag');result.update(expected_bytes=n,head_etag=etag);conn.close();conn=None
        require(time.monotonic()<deadline,'FETCH_DEADLINE')
        conn,response,actual=request(root,item,'GET',deadline);result.update(get_sent=True,get_status=response.status)
        if response.status in (401,403,407,451) or 'text/html' in actual.get('content-type','').lower():result['stop_network']=True;raise ValueError('AUTH_OR_TERMS')
        require(response.status==200,'GET_STATUS_'+str(response.status));require(length(actual)==n,'LENGTH_CHANGED')
        require(etag is None or actual.get('etag')==etag,'ETAG_CHANGED')
        md5=hashlib.md5();sha=hashlib.sha256();partial=root/f'media-{rank:02d}.partial'
        with open(partial,'xb') as f:
            while result['body_bytes']<n:
                require(time.monotonic()<deadline,'FETCH_DEADLINE')
                conn.sock.settimeout(min(60,max(.01,deadline-time.monotonic()))) if conn.sock is not None else None
                chunk=response.read(min(1024**2,n-result['body_bytes']))
                if not chunk:raise ValueError('SHORT_BODY')
                result['body_bytes']+=len(chunk);require(result['body_bytes']<=n and result['body_bytes']<=remaining,'BYTE_METER')
                md5.update(chunk);sha.update(chunk);f.write(chunk)
                # Persist byte accounting including failed/partial transfers.
                event(root,dict(rank=rank,state='BODY',bytes=result['body_bytes']))
            f.flush();os.fsync(f.fileno())
        result.update(md5=md5.hexdigest(),sha256=sha.hexdigest())
        require(md5.hexdigest()==item['publisher_md5'],'PUBLISHER_MD5_MISMATCH')
        os.rename(partial,root/f'media-{rank:02d}.MP4');result['status']='FETCH_VERIFIED'
    except Exception as e:result['error']=type(e).__name__+':'+str(e)[:240]
    finally:
        if conn:conn.close()
        result['wall_seconds']=time.monotonic()-start;write(root/f'fetch-{rank:02d}.json',result)

def mp4_clock(path):
    """Bounded atom metadata reads; no media sample read or assumed edit correction."""
    result=dict(edits=[],video_tracks=0)
    with open(path,'rb') as f:
        end=f.seek(0,2);seen=0;metadata_bytes=0
        def walk(start,stop,trail=(),track=None):
            nonlocal seen,metadata_bytes
            offset=start
            while offset<stop:
                seen+=1;require(seen<=20000,'ATOM_LIMIT');f.seek(offset);header=f.read(8);require(len(header)==8,'ATOM_HEADER');size,kind=struct.unpack('>I4s',header);h=8
                if size==1:size=struct.unpack('>Q',f.read(8))[0];h=16
                if size==0:size=stop-offset
                require(size>=h and offset+size<=stop,'ATOM_SIZE')
                if kind==b'trak':
                    current=dict(edits=[]);walk(offset+h,offset+size,trail+(kind,),current)
                    if current.get('handler')=='vide':
                        result['video_tracks']+=1;result['edits']=current['edits'];result['media']=current.get('media',{})
                elif kind in (b'moov',b'mdia',b'edts'):walk(offset+h,offset+size,trail+(kind,),track)
                elif kind in (b'mvhd',b'mdhd',b'elst',b'hdlr'):
                    require(size-h<=1024**2,'ATOM_METADATA_SIZE');data=f.read(size-h);metadata_bytes+=len(data);require(metadata_bytes<=4*1024**2,'ATOM_METADATA_TOTAL')
                    version=data[0]
                    if kind in (b'mvhd',b'mdhd'):
                        pos=20 if version==1 else 12;ts=struct.unpack_from('>I',data,pos)[0];duration=struct.unpack_from('>Q' if version==1 else '>I',data,pos+4)[0]
                        if kind==b'mvhd':result['movie']=dict(timescale=ts,duration=duration)
                        elif track is not None:track['media']=dict(timescale=ts,duration=duration)
                    elif kind==b'hdlr' and track is not None:track['handler']=data[8:12].decode('ascii')
                    elif kind==b'elst':
                        count=struct.unpack_from('>I',data,4)[0];require(count<=1024,'EDIT_COUNT');pos=8
                        for _ in range(count):
                            fmt='>Qqhh' if version==1 else '>Iihh';entry=struct.unpack_from(fmt,data,pos);pos+=struct.calcsize(fmt)
                            if track is not None:track['edits'].append(list(entry))
                offset+=size
        walk(0,end)
    return result

def qualify(points,rate,tb,origin_known,endpoint_ok):
    errors=[]
    if not origin_known:errors.append('ORIGIN_EDIT_UNKNOWN')
    if not endpoint_ok:errors.append('DURATION_BOUNDARY_UNKNOWN')
    if len(points)<48:errors.append('TOO_FEW_FRAMES')
    for i,(pts,duration) in enumerate(points):
        if pts is None or duration is None or duration<=0:errors.append('MISSING_PTS_OR_DURATION');break
        if i and pts<=points[i-1][0]:errors.append('DISPLAY_ORDER');break
        if i and points[i-1][0]+points[i-1][1]!=pts:errors.append('GAP_OR_OVERLAP');break
    if errors:return dict(clock_status='CLOCK_UNKNOWN',reasons=sorted(set(errors)))
    sample=indices(len(points));drift=max(abs(Q(i,1)/rate-points[i][0]*tb) for i in sample)
    intervals=[points[i][0]-points[i-1][0] for i in range(1,len(points))];span=max(intervals)-min(intervals)
    layer='HIGH_OFFSET' if span>1 and drift>=Q(1,4) else ('CFR' if span<=1 and drift<=Q(1,50) else 'OTHER')
    return dict(clock_status='CLOCK_CERTIFIED',layer=layer,d_num=drift.numerator,d_den=drift.denominator,d_seconds=float(drift),interval_tick_span=span,sample_indices=sample,sample_pts=[points[i][0] for i in sample])

def scan(root,rank,site):
    root=Path(root);sys.path.insert(0,site);import av
    start=time.monotonic();result=dict(rank=rank,clock_status='CLOCK_UNKNOWN');points=[];frame_tb=None
    try:
        atoms=mp4_clock(root/f'media-{rank:02d}.MP4');result['atoms']=atoms
        with av.open(str(root/f'media-{rank:02d}.MP4'),mode='r',format='mov',hwaccel=None,container_options={'ignore_editlist':'0','protocol_whitelist':'file'}) as container:
            require(len(container.streams.video)==1,'VIDEO_TRACK_COUNT')
            stream=container.streams.video[0];stream.thread_count=4;stream.thread_type='SLICE';tb=Q(stream.time_base);rate=Q(stream.average_rate)
            result.update(time_base=str(tb),source_avg_frame_rate=str(rate),stream_start_time=stream.start_time,stream_duration=stream.duration,container_start_time=container.start_time,container_duration=container.duration,has_b_frames=stream.codec_context.has_b_frames,codec=stream.codec_context.name,hwaccel=False,threads=stream.thread_count)
            with open(root/f'frames-{rank:02d}.bin','xb') as table:
                for frame in container.decode(video=0):
                    require(time.monotonic()-start<895,'SCAN_DEADLINE');require(len(points)<1000000,'FRAME_LIMIT')
                    frame_tb=Q(frame.time_base);require(frame_tb==tb,'FRAME_TIME_BASE_CHANGED')
                    pts=frame.pts;duration=frame.duration
                    points.append((pts,duration));table.write(struct.pack('<qq',pts if pts is not None else -(2**63),duration or 0))
                    del frame
            result.update(frame_count=len(points),display_order='decoder-output-not-packet-order')
            no_edits=not atoms['edits'];identity_edit=len(atoms['edits'])==1 and atoms['edits'][0][1:]==[0,1,0]
            origin=atoms['video_tracks']==1 and (no_edits or identity_edit) and stream.start_time==0 and container.start_time==0 and bool(points) and points[0][0]==0
            # Track-aware atoms exclude the audio mdhd/edits from video certification.
            origin=origin and atoms.get('media',{}).get('timescale')==tb.denominator and tb.numerator==1
            end=Q(points[-1][0]+points[-1][1])*tb if points and points[-1][0] is not None and points[-1][1] else None
            endpoint=end is not None and stream.duration is not None and abs(end-stream.duration*tb)<=tb and container.duration is not None and abs(end-Q(container.duration,1000000))<=tb
            result.update(qualify(points,rate,tb,origin,endpoint));result['first_pts']=points[0][0] if points else None;result['last_end']=str(end)
    except Exception as e:result['error']=type(e).__name__+':'+str(e)[:240]
    result['wall_seconds']=time.monotonic()-start;result['torch_imported']='torch' in sys.modules
    write(root/f'scan-{rank:02d}.json',result)

def api_receipt(root,site):
    sys.path.insert(0,site);import av
    require(all(hasattr(av.VideoFrame,n) for n in ('pts','duration','time_base')),'FRAME_INTERFACE')
    require('hwaccel' in av.open.__doc__,'NO_EXPLICIT_CPU_API')
    binaries=[]
    for name in ('av._core','av.video.frame','av.video.codeccontext'):
        module=sys.modules[name];p=Path(module.__file__);binaries.append(dict(module=name,size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    require('torch' not in sys.modules,'TORCH_IMPORTED')
    write(Path(root)/'selected-api.json',dict(av=av.__version__,binaries=binaries,libraries={k:list(v) for k,v in av.library_versions.items()},cpu_command='av.open(local,format=mov,hwaccel=None,ignore_editlist=0,protocol_whitelist=file); video.thread_count=4; video.thread_type=SLICE; container.decode(video=0)',torch_imported=False))

def quota(root):
    media=other=files=0
    for p in Path(root).iterdir():
        st=p.lstat();require(not st.st_file_attributes & 1024,'ROOT_REPARSE')
        require(p.is_file(),'UNEXPECTED_DIRECTORY');files+=1
        if p.suffix in ('.MP4','.partial'):media+=st.st_size
        else:other+=st.st_size
    require(media<=32*GIB and other<=256*1024**2 and files<=2048,'OUTPUT_QUOTA')
    return dict(media_bytes=media,other_bytes=other,files=files)

def supervise(root,role,args,seconds):
    root=Path(root);pf=read(root/'preflight.json');require(time.time()+seconds<pf['deadline'],'PARENT_DEADLINE')
    spec=importlib.util.spec_from_file_location('platform040',Path(__file__).with_name('auditable_runner_040.py'));platform=importlib.util.module_from_spec(spec);spec.loader.exec_module(platform)
    job=platform.Job(memory=4*GIB);child=None;start=time.monotonic();error=None;code=None;peak=quota(root)
    tag=str(args[0]) if str(args[0]).isdigit() else hashlib.sha256(str(args[0]).encode()).hexdigest()[:12]
    bootstrap="import os,sys,runpy;os.environ.update(CUDA_VISIBLE_DEVICES='',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4');sys.argv="+repr([str(Path(__file__).resolve()),role,str(root)]+[str(a) for a in args])+";runpy.run_path(sys.argv[0],run_name='__main__')"
    try:
        child=platform.Process([pf['python'],'-I','-S','-B','-c',bootstrap],root/(role+'-'+tag+'.log'),job)
        while child.poll() is None:
            require(time.monotonic()-start<seconds-2,'WORKER_TIMEOUT');q=quota(root)
            peak={k:max(peak[k],v) for k,v in q.items()};time.sleep(.1)
        code=child.poll()
    except Exception as e:error=type(e).__name__+':'+str(e)
    finally:
        if not job.empty(time.monotonic()+.2):job.kill()
        require(job.empty(time.monotonic()+1),'OWN_JOB_NOT_EMPTY');snapshot=job.snapshot();job.close()
        if child:child.close()
    result=dict(exitcode=code,error=error,wall_seconds=time.monotonic()-start,peak_output=peak,**snapshot);write(root/(role+'-'+tag+'-job.json'),result)
    return result

def main():
    role,root,*args=sys.argv[1:]
    if role=='fetch':fetch(root,int(args[0]),int(args[1]),float(args[2]))
    elif role=='scan':scan(root,int(args[0]),args[1])
    elif role=='api':api_receipt(root,args[0])
    elif role=='suite':
        sys.path.insert(0,str(Path(__file__).parent));from test_epic_clock_admission_042 import suite
        suite(root)
    elif role=='supervise':print(json.dumps(supervise(root,args[0],args[2:],float(args[1]))))
    else:raise ValueError('ROLE')

if __name__=='__main__':main()
