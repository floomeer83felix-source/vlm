"""Fail-closed two-member Range/clock pilot. Fixed sources/roots; no pixels or models."""
import csv
import hashlib
import html.parser
import io
import json
import os
import pathlib
import re
import shutil
import stat
import struct
import subprocess
import sys
import urllib.request
import zlib
from collections import Counter
from decimal import Decimal, InvalidOperation
from fractions import Fraction

MIB=1024*1024
NET_LIMIT=64*MIB
DISK_LIMIT=128*MIB
GET_LIMIT=12
HOST='ai2-public-datasets.s3-us-west-2.amazonaws.com'
URL='https://'+HOST+'/charades/Charades_v1_480.zip'
PAGE='https://prior.allenai.org/projects/charades'
LICENSE='https://prior.allenai.org/projects/data/charades/license.txt'
SOURCE_SHA={'zip':'c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866',
 'train':'59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc',
 'classes':'7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887'}


class PilotError(ValueError): pass


def number(x):
    try:
        d=Decimal(str(x))
        return d if d.is_finite() else None
    except (InvalidOperation,ValueError): return None


def find_ffprobe():
    candidates=[shutil.which('ffprobe')]
    candidates += ['C:/ffmpeg/bin/ffprobe.exe','C:/Program Files/ffmpeg/bin/ffprobe.exe',
                   'C:/ProgramData/chocolatey/bin/ffprobe.exe','C:/Tools/ffmpeg/bin/ffprobe.exe']
    if os.environ.get('LOCALAPPDATA'):
        candidates.append(str(pathlib.Path(os.environ['LOCALAPPDATA'])/'Microsoft/WinGet/Links/ffprobe.exe'))
    bundle=pathlib.Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies'
    candidates += [str(bundle/p) for p in ('bin/override/ffprobe.exe','bin/fallback/ffprobe.exe','native/ffmpeg/bin/ffprobe.exe')]
    for value in candidates:
        if not value: continue
        p=pathlib.Path(value)
        if any('conda' in part.lower() or part.lower()=='vlm' for part in p.parts): continue
        if p.is_file(): return p.resolve()
    raise PilotError('BLOCKED_EXISTING_FFPROBE_NOT_FOUND')


class Ledger:
    def __init__(self,path=None):
        self.path=path; self.state={'get_attempts':0,'body_bytes':0,'peak_local_bytes':0,'events':[]}
        if path is not None:
            if path.exists(): raise PilotError('LEDGER_ALREADY_EXISTS')
            self.save()
    def save(self):
        if self.path is None: return
        tmp=self.path.with_suffix('.next')
        with tmp.open('x',encoding='utf-8') as f: json.dump(self.state,f)
        os.replace(tmp,self.path)
    def begin(self,start,end):
        if not 0<=start<=end or self.state['get_attempts']>=GET_LIMIT or self.state['body_bytes']+end-start+1>NET_LIMIT:
            raise PilotError('NETWORK_PREFLIGHT_BUDGET')
        self.state['get_attempts']+=1
        self.state['events'].append({'requested_start':start,'requested_end':end,'read':0,'status':'STARTED'})
        self.save()
    def add(self,n):
        if n<0 or self.state['body_bytes']+n>NET_LIMIT: raise PilotError('NETWORK_BODY_BUDGET')
        self.state['body_bytes']+=n; self.state['events'][-1]['read']+=n; self.save()
    def finish(self,status):
        self.state['events'][-1]['status']=status; self.save()
    def disk(self,n):
        if n>DISK_LIMIT: raise PilotError('DISK_BUDGET')
        self.state['peak_local_bytes']=max(n,self.state['peak_local_bytes']); self.save()


def validate_range(status,headers,start,end,total,etag,final_url):
    if status!=206: raise PilotError('RANGE_REQUIRES_206_NO_BODY_READ')
    if final_url!=URL: raise PilotError('RANGE_SOURCE_CHANGED')
    if headers.get('Content-Encoding','identity').lower()!='identity': raise PilotError('RANGE_ENCODING')
    match=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',headers.get('Content-Range',''))
    if not match or tuple(map(int,match.groups()))!=(start,end,total): raise PilotError('RANGE_MISMATCH')
    if headers.get('Content-Length')!=str(end-start+1): raise PilotError('RANGE_LENGTH')
    if not etag or headers.get('ETag')!=etag: raise PilotError('RANGE_ETAG')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): raise PilotError('REDIRECT_FORBIDDEN')


def read_response(response,start,end,total,etag,ledger):
    validate_range(response.status,response.headers,start,end,total,etag,response.geturl())
    remaining=end-start+1; parts=[]
    while remaining:
        amount=min(65536,remaining,NET_LIMIT-ledger.state['body_bytes'])
        if amount<=0: raise PilotError('NETWORK_BODY_BUDGET')
        block=response.read(amount)
        if not block: raise PilotError('RANGE_TRUNCATED')
        if len(block)>amount: raise PilotError('READER_EXCEEDED_REQUEST')
        ledger.add(len(block)); parts.append(block); remaining-=len(block)
    ledger.finish('COMPLETE')
    return b''.join(parts)


class RangeClient:
    def __init__(self,ledger,total,etag):
        self.ledger=ledger; self.total=total; self.etag=etag
        self.opener=urllib.request.build_opener(NoRedirect())
    def get(self,start,end):
        self.ledger.begin(start,end)
        request=urllib.request.Request(URL,headers={'Range':'bytes='+str(start)+'-'+str(end),
                                      'Accept-Encoding':'identity','If-Range':self.etag})
        try:
            with self.opener.open(request,timeout=30) as r:
                return read_response(r,start,end,self.total,self.etag,self.ledger)
        except Exception:
            self.ledger.finish('STOPPED'); raise


def eocd(tail,total):
    position=tail.rfind(b'PK\x05\x06')
    if position<0 or position+22>len(tail): raise PilotError('EOCD_UNKNOWN')
    sig,disk,cd_disk,on_disk,count,size,offset,comment=struct.unpack_from('<4s4H2LH',tail,position)
    if position+22+comment!=len(tail): raise PilotError('EOCD_COMMENT_OR_TRAILING')
    if disk or cd_disk or on_disk!=count: raise PilotError('MULTI_DISK_UNSUPPORTED')
    if count==65535 or size==0xffffffff or offset==0xffffffff or b'PK\x06\x07' in tail[max(0,position-20):position]:
        raise PilotError('ZIP64_UNSUPPORTED_STOP')
    absolute=total-len(tail)+position
    if not 0<count<=20000 or size>8*MIB or offset+size!=absolute: raise PilotError('CENTRAL_BOUNDS')
    return offset,size,count


def safe_name(name):
    if not name or name.startswith(('/', '\\')) or '\\' in name or ':' in name: raise PilotError('ZIP_PATH')
    parts=name.rstrip('/').split('/')
    if len(parts)>4 or any(p in ('','.','..') or p.endswith((' ','.')) or
       re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?',p,re.I) or
       any(ord(c)<32 or c in '<>"|?*' for c in p) for p in parts): raise PilotError('ZIP_NAME')


def central_directory(data,expected,cd_offset):
    records=[]; seen=set(); cursor=0
    while cursor<len(data):
        if cursor+46>len(data): raise PilotError('CENTRAL_TRUNCATED')
        v=struct.unpack_from('<4s6H3L5H2L',data,cursor)
        if v[0]!=b'PK\x01\x02': raise PilotError('CENTRAL_SIGNATURE')
        _,made,version,flags,method,mt,md,crc,compressed,size,nlen,elen,clen,disk,internal,external,offset=v
        end=cursor+46+nlen+elen+clen
        if end>len(data): raise PilotError('CENTRAL_TRUNCATED')
        name_bytes=data[cursor+46:cursor+46+nlen]
        validate_extra(data[cursor+46+nlen:cursor+46+nlen+elen])
        name=name_bytes.decode('utf-8' if flags&0x800 else 'cp437'); safe_name(name)
        key=name.rstrip('/').casefold()
        if key in seen: raise PilotError('CENTRAL_DUPLICATE')
        seen.add(key)
        kind=stat.S_IFMT(external>>16)
        if kind not in (0,stat.S_IFREG,stat.S_IFDIR) or flags&1: raise PilotError('ZIP_SPECIAL_OR_ENCRYPTED')
        if flags&8: raise PilotError('DATA_DESCRIPTOR_UNSUPPORTED_STOP')
        if disk or version>=45 or compressed==0xffffffff or size==0xffffffff or offset==0xffffffff:
            raise PilotError('ZIP64_OR_DISK_UNSUPPORTED_STOP')
        if method not in (0,8): raise PilotError('COMPRESSION_UNSUPPORTED')
        if offset+30+nlen+compressed>cd_offset: raise PilotError('MEMBER_BOUNDS')
        records.append({'name':name,'name_bytes':name_bytes,'flags':flags,'method':method,'crc':crc,
                        'compressed':compressed,'size':size,'offset':offset})
        cursor=end
    if len(records)!=expected: raise PilotError('CENTRAL_COUNT')
    ordered=sorted(records,key=lambda r:r['offset'])
    for a,b in zip(ordered,ordered[1:]):
        if a['offset']+30+len(a['name_bytes'])+a['compressed']>b['offset']: raise PilotError('MEMBER_OVERLAP')
    return records


def validate_extra(data):
    cursor=0
    while cursor<len(data):
        if cursor+4>len(data): raise PilotError('ZIP_EXTRA_TRUNCATED')
        tag,size=struct.unpack_from('<HH',data,cursor); cursor+=4
        if cursor+size>len(data): raise PilotError('ZIP_EXTRA_TRUNCATED')
        if tag==1: raise PilotError('ZIP64_EXTRA_UNSUPPORTED_STOP')
        if tag not in (0x5455,0x000a,0x7875): raise PilotError('ZIP_EXTRA_UNSUPPORTED_STOP')
        cursor+=size


def match_two(records,ids):
    if len(ids)!=2 or len(set(ids))!=2: raise PilotError('EXACTLY_TWO_UNIQUE_SELECTIONS')
    chosen=[]
    for identity in ids:
        found=[r for r in records if pathlib.PurePosixPath(r['name']).name==identity+'.mp4']
        if len(found)!=1: raise PilotError('MEMBER_UNIQUE_MATCH_FAILED')
        chosen.append(found[0])
    if sum(r['compressed'] for r in chosen)>NET_LIMIT or sum(r['size'] for r in chosen)>DISK_LIMIT:
        raise PilotError('SELECTED_SIZE_BUDGET')
    return chosen


def local_header(header,variable,entry):
    if len(header)!=30: raise PilotError('LOCAL_HEADER_SIZE')
    sig,version,flags,method,mt,md,crc,compressed,size,nlen,elen=struct.unpack('<4s5H3L2H',header)
    if sig!=b'PK\x03\x04' or flags!=entry['flags'] or method!=entry['method'] or crc!=entry['crc'] or compressed!=entry['compressed'] or size!=entry['size']:
        raise PilotError('LOCAL_CENTRAL_MISMATCH')
    if len(variable)!=nlen+elen or variable[:nlen]!=entry['name_bytes']: raise PilotError('LOCAL_NAME')
    validate_extra(variable[nlen:])
    if version>=45 or flags&8: raise PilotError('LOCAL_UNSUPPORTED')
    return nlen+elen


def expand_member(body,entry):
    if len(body)!=entry['compressed'] or entry['size']>DISK_LIMIT: raise PilotError('MEMBER_INPUT_SIZE')
    if entry['method']==0: output=body
    elif entry['method']==8:
        d=zlib.decompressobj(-15); output=d.decompress(body,entry['size']+1)
        if len(output)>entry['size'] or d.unconsumed_tail or not d.eof or d.unused_data:
            raise PilotError('DEFLATE_BOUND_OR_TRAILING')
    else: raise PilotError('COMPRESSION_UNSUPPORTED')
    if len(output)!=entry['size'] or zlib.crc32(output)&0xffffffff!=entry['crc']: raise PilotError('MEMBER_CRC_OR_SIZE')
    return output


def select_cases(rows,classes):
    overflow=[]; control=[]
    ids=Counter((r.get('id') or '').strip() for r in rows)
    if any(not key or count!=1 for key,count in ids.items()): raise PilotError('CSV_ID_NOT_UNIQUE')
    for r in rows:
        length=number(r.get('length')); identity=(r.get('id') or '').strip(); subject=(r.get('subject') or '').strip()
        if not identity or not subject or length is None or length<=0: continue
        events=[]; valid=True; structurally_valid=True; targets=[]
        for token in (r.get('actions') or '').split(';'):
            p=token.split()
            if len(p)!=3 or p[0] not in classes: valid=False; structurally_valid=False; continue
            a,b=number(p[1]),number(p[2])
            if a is None or b is None or a<0 or a>=b: valid=False; structurally_valid=False; continue
            events.append((a,b))
            if a<length<b and Decimal(1)<b-length<=5: targets.append(b)
            if b>length: valid=False
        item={'id':identity,'subject':subject,'length':length,'ends':targets}
        if targets and structurally_valid: overflow.append(item)
        if events and valid: control.append(item)
    if not overflow or not control: raise PilotError('CASE_SELECTION_UNAVAILABLE')
    key=lambda x:hashlib.sha256(('VLM-BATCH-013|'+x['id']).encode()).hexdigest()
    a=min(overflow,key=key)
    candidates=[x for x in control if x['subject']!=a['subject'] and abs(x['length']-a['length'])<=5]
    if not candidates: raise PilotError('MATCHED_CONTROL_UNAVAILABLE')
    b=min(candidates,key=key)
    if a['id']==b['id']: raise PilotError('CASE_NOT_DISTINCT')
    return [a,b]


def ffprobe_command(executable,media):
    return [str(executable),'-v','error','-protocol_whitelist','file','-select_streams','v:0',
            '-show_entries','format=duration,start_time:stream=time_base,avg_frame_rate,r_frame_rate,start_time,duration,has_b_frames:packet=pts,dts,duration',
            '-show_format','-show_streams','-show_packets','-of','json',str(media)]


def classify_clock(probe,csv_length):
    try:
        stream=probe['streams'][0]; packets=probe['packets']
        tb=Fraction(stream['time_base']); fps=Fraction(stream['avg_frame_rate'])
        if tb<=0 or fps<=0 or stream.get('has_b_frames',0)>0 or stream['avg_frame_rate']!=stream['r_frame_rate']:
            return 'CLOCK_UNKNOWN'
        tolerance=max(float(tb),float(1/fps),0.001)
        start=float(stream['start_time']); pts=[int(p['pts'])*float(tb) for p in packets]
        ends=[(int(p['pts'])+int(p['duration']))*float(tb) for p in packets]
        if not pts or abs(min(pts)-start)>tolerance: return 'CLOCK_UNKNOWN'
        targets=(float(probe['format']['duration']),float(stream['duration']),max(ends)-start)
        if any(not (x>0) for x in targets): return 'CLOCK_UNKNOWN'
        return 'LENGTH_APPROX_MATCH' if all(abs(x-float(csv_length))<=tolerance for x in targets) else 'LENGTH_DIFFERS'
    except (KeyError,ValueError,IndexError,ZeroDivisionError,TypeError): return 'CLOCK_UNKNOWN'


def public_receipt(state,clock=None):
    return {'get_attempts':state.get('get_attempts',0),'response_body_bytes':state.get('body_bytes',0),
            'peak_local_bytes':state.get('peak_local_bytes',0),'saved_videos':state.get('saved_videos',0),
            'CASE_OVERFLOW':(clock or {}).get('CASE_OVERFLOW','CLOCK_UNKNOWN'),
            'CASE_CONTROL':(clock or {}).get('CASE_CONTROL','CLOCK_UNKNOWN')}


def run_pilot():
    # No network or new directory before the mandatory existing-tool gate.
    executable=find_ffprobe()
    version=subprocess.run([str(executable),'-version'],capture_output=True,timeout=10,check=True)
    if not version.stdout.startswith(b'ffprobe version'): raise PilotError('FFPROBE_VERSION_UNVERIFIED')
    # Supported transport helpers are intentionally not an authorization token.
    # This task stopped at the real tool gate. Never silently run an unexercised
    # source/disk/provenance preflight or substitute a different package here.
    raise PilotError('COORDINATOR_NOT_RELEASED_BEYOND_TESTED_PREFLIGHT')


if __name__=='__main__':
    try:
        if len(sys.argv)!=1: raise PilotError('NO_CUSTOM_URL_PATH_ARGUMENTS')
        run_pilot()
    except PilotError as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e),'response_body_bytes':0,'saved_videos':0}))
        raise SystemExit(1) from None
    except Exception:
        print(json.dumps({'status':'BLOCKED','reason':'UNVERIFIED_ENVIRONMENT','response_body_bytes':0,'saved_videos':0}))
        raise SystemExit(1) from None
