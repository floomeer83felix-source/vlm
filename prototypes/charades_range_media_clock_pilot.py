"""Fail-closed two-member Range/clock pilot. Fixed sources/roots; no pixels or models."""
import csv
import argparse
import hashlib
import html.parser
import math
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
AUDIT_RESERVE=64*1024
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
    if os.environ.get('LOCALAPPDATA'):
        candidates.insert(0,str(pathlib.Path(os.environ['LOCALAPPDATA'])/'VLM-Research-Isolated/CPU-Tools/ffprobe/bin/ffprobe.exe'))
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
        if p.is_file():
            resolved=p.resolve()
            if any('conda' in part.lower() or part.lower()=='vlm' for part in resolved.parts): continue
            original=os.environ.get('VLM_ORIGINAL_WORKSPACE')
            if original:
                blocked=pathlib.Path(original).resolve()
                if resolved==blocked or blocked in resolved.parents: continue
            return resolved
    raise PilotError('BLOCKED_EXISTING_FFPROBE_NOT_FOUND')


class Ledger:
    def __init__(self,path=None):
        self.path=path; self.state={'get_attempts':0,'body_bytes':0,'peak_local_bytes':0,'events':[]}
        if path is not None:
            if path.exists(): raise PilotError('LEDGER_ALREADY_EXISTS')
            self.save()
    def save(self):
        if self.path is None: return
        from charades_metadata_audit import check_ancestors
        tmp=self.path.with_suffix('.next')
        check_ancestors(self.path); check_ancestors(tmp)
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
        if not 0<=start<=end<self.total: raise PilotError('RANGE_OBJECT_BOUNDS')
        self.ledger.begin(start,end)
        request=urllib.request.Request(URL,headers={'Range':'bytes='+str(start)+'-'+str(end),
                                      'Accept-Encoding':'identity','If-Range':self.etag})
        try:
            with self.opener.open(request,timeout=30) as r:
                return read_response(r,start,end,self.total,self.etag,self.ledger)
        except Exception:
            self.ledger.finish('STOPPED'); raise

    def text(self,url,limit):
        if url not in (PAGE,LICENSE): raise PilotError('TEXT_SOURCE_FORBIDDEN')
        self.ledger.begin(0,limit-1)
        try:
            with self.opener.open(urllib.request.Request(url,headers={'Accept-Encoding':'identity'}),timeout=30) as r:
                if r.status!=200 or r.geturl()!=url or r.headers.get('Content-Encoding','identity').lower()!='identity':
                    raise PilotError('TEXT_RESPONSE_CHANGED')
                length=r.headers.get('Content-Length')
                if length is None or not 0<int(length)<=limit: raise PilotError('TEXT_SIZE_UNKNOWN')
                remaining=int(length); body=[]
                while remaining:
                    amount=min(65536,remaining); part=r.read(amount)
                    if not part: raise PilotError('TEXT_TRUNCATED')
                    if len(part)>amount: raise PilotError('TEXT_READER_OVERRUN')
                    self.ledger.add(len(part)); body.append(part); remaining-=len(part)
                self.ledger.finish('COMPLETE'); return b''.join(body)
        except Exception:
            self.ledger.finish('STOPPED'); raise


def eocd(tail,total,fetch=None):
    position=tail.rfind(b'PK\x05\x06')
    if position<0 or position+22>len(tail): raise PilotError('EOCD_UNKNOWN')
    sig,disk,cd_disk,on_disk,count,size,offset,comment=struct.unpack_from('<4s4H2LH',tail,position)
    if position+22+comment!=len(tail): raise PilotError('EOCD_COMMENT_OR_TRAILING')
    if disk or cd_disk or on_disk!=count: raise PilotError('MULTI_DISK_UNSUPPORTED')
    absolute=total-len(tail)+position
    locator=position>=20 and tail[position-20:position-16]==b'PK\x06\x07'
    if count==65535 or size==0xffffffff or offset==0xffffffff or locator:
        if not locator: raise PilotError('ZIP64_LOCATOR_MISSING')
        _,record_disk,record_offset,disks=struct.unpack_from('<4sLQL',tail,position-20)
        if record_disk or disks!=1: raise PilotError('ZIP64_MULTI_DISK')
        locator_offset=absolute-20
        if not 0<=record_offset or record_offset+56!=locator_offset: raise PilotError('ZIP64_RECORD_BOUNDS')
        relative=record_offset-(total-len(tail))
        if relative>=0: record=tail[relative:relative+56]
        elif fetch is not None: record=fetch(record_offset,record_offset+55)
        else: raise PilotError('ZIP64_RECORD_NOT_AVAILABLE')
        if len(record)!=56: raise PilotError('ZIP64_RECORD_SIZE')
        values=struct.unpack('<4sQ2H2L4Q',record)
        sig,length,made,needed,disk64,cd_disk64,on_disk64,count64,size64,offset64=values
        if sig!=b'PK\x06\x06' or length!=44 or needed>45 or disk64 or cd_disk64 or on_disk64!=count64:
            raise PilotError('ZIP64_RECORD_UNSUPPORTED')
        if count!=65535 and count!=count64 or size!=0xffffffff and size!=size64 or offset!=0xffffffff and offset!=offset64:
            raise PilotError('ZIP64_CLASSIC_DISAGREEMENT')
        count,size,offset=count64,size64,offset64
        absolute=record_offset
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
        extra=data[cursor+46+nlen:cursor+46+nlen+elen]
        name=name_bytes.decode('utf-8' if flags&0x800 else 'cp437'); safe_name(name)
        key=name.rstrip('/').casefold()
        if key in seen: raise PilotError('CENTRAL_DUPLICATE')
        seen.add(key)
        kind=stat.S_IFMT(external>>16)
        if kind not in (0,stat.S_IFREG,stat.S_IFDIR) or flags&1: raise PilotError('ZIP_SPECIAL_OR_ENCRYPTED')
        if flags&8: raise PilotError('DATA_DESCRIPTOR_UNSUPPORTED_STOP')
        if flags&~0x806 or method==0 and flags&6: raise PilotError('ZIP_FLAGS_UNSUPPORTED')
        size,compressed,offset,disk=zip64_fields(extra,size,compressed,offset,disk)
        if disk or version>45: raise PilotError('ZIP_VERSION_OR_DISK_UNSUPPORTED_STOP')
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


def extra_fields(data):
    result={}
    cursor=0
    while cursor<len(data):
        if cursor+4>len(data): raise PilotError('ZIP_EXTRA_TRUNCATED')
        tag,size=struct.unpack_from('<HH',data,cursor); cursor+=4
        if cursor+size>len(data): raise PilotError('ZIP_EXTRA_TRUNCATED')
        if tag in result: raise PilotError('ZIP_EXTRA_DUPLICATE')
        if tag not in (1,0x5455,0x000a,0x7875): raise PilotError('ZIP_EXTRA_UNSUPPORTED_STOP')
        result[tag]=data[cursor:cursor+size]
        cursor+=size
    return result


def validate_extra(data):
    if 1 in extra_fields(data): raise PilotError('ZIP64_EXTRA_NEEDS_CONTEXT')


def zip64_fields(extra,size,compressed,offset=None,disk=None):
    fields=extra_fields(extra); body=fields.get(1,b''); cursor=0
    values=[size,compressed,offset,disk]
    for index,value in enumerate(values):
        sentinel=65535 if index==3 else 0xffffffff
        if value==sentinel:
            width=4 if index==3 else 8
            if cursor+width>len(body): raise PilotError('ZIP64_EXTRA_MISSING_VALUE')
            values[index]=struct.unpack_from('<L' if width==4 else '<Q',body,cursor)[0]
            cursor+=width
    if cursor!=len(body): raise PilotError('ZIP64_EXTRA_UNEXPECTED_VALUES')
    return tuple(values)


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
    if len(variable)!=nlen+elen or variable[:nlen]!=entry['name_bytes']: raise PilotError('LOCAL_NAME')
    size,compressed,_,_=zip64_fields(variable[nlen:],size,compressed)
    if sig!=b'PK\x03\x04' or flags!=entry['flags'] or method!=entry['method'] or crc!=entry['crc'] or compressed!=entry['compressed'] or size!=entry['size']:
        raise PilotError('LOCAL_CENTRAL_MISMATCH')
    if version>45 or flags&8: raise PilotError('LOCAL_UNSUPPORTED')
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
        start=float(stream['start_time']); expected=float(csv_length)
        if not math.isfinite(start) or not math.isfinite(expected) or expected<=0: return 'CLOCK_UNKNOWN'
        pts=[int(p['pts'])*float(tb) for p in packets]
        ends=[(int(p['pts'])+int(p['duration']))*float(tb) for p in packets]
        if not pts or abs(min(pts)-start)>tolerance: return 'CLOCK_UNKNOWN'
        targets=(float(probe['format']['duration']),float(stream['duration']),max(ends)-start)
        if any(not math.isfinite(x) or not (x>0) for x in targets): return 'CLOCK_UNKNOWN'
        return 'LENGTH_APPROX_MATCH' if all(abs(x-expected)<=tolerance for x in targets) else 'LENGTH_DIFFERS'
    except (KeyError,ValueError,IndexError,ZeroDivisionError,TypeError,OverflowError): return 'CLOCK_UNKNOWN'


def endpoint_relation(probe,chosen):
    if classify_clock(probe,chosen['length'])=='CLOCK_UNKNOWN' or not chosen.get('ends'): return 'END_CLOCK_UNKNOWN'
    try:
        stream=probe['streams'][0]; tb=Fraction(stream['time_base'])
        fps=Fraction(stream['avg_frame_rate']); tolerance=max(float(tb),float(1/fps),0.001)
        boundary=max((int(p['pts'])+int(p['duration']))*float(tb) for p in probe['packets'])-float(stream['start_time'])
        target=max(float(e) for e in chosen['ends'])  # Pre-frozen deterministic endpoint among qualifying records.
        return 'END_AFTER_PACKET_BOUNDARY' if target>boundary+tolerance else 'END_WITHIN_PACKET_BOUNDARY'
    except (KeyError,ValueError,IndexError,ZeroDivisionError,TypeError,OverflowError): return 'END_CLOCK_UNKNOWN'


def public_receipt(state,clock=None):
    return {'get_attempts':state.get('get_attempts',0),'response_body_bytes':state.get('body_bytes',0),
            'peak_local_bytes':state.get('peak_local_bytes',0),'saved_videos':state.get('saved_videos',0),
            'CASE_OVERFLOW':(clock or {}).get('CASE_OVERFLOW','CLOCK_UNKNOWN'),
            'CASE_CONTROL':(clock or {}).get('CASE_CONTROL','CLOCK_UNKNOWN')}


def authorize_parent(parent,docs):
    if not re.fullmatch(r'VLM-BATCH-\d{3}',parent): raise PilotError('PARENT_TASK_INVALID')
    board=(docs/'docs/next-steps.md').read_text(encoding='utf-8')
    results=(docs/'docs/codex-results.md').read_text(encoding='utf-8')
    active=[]
    for line in board.splitlines():
        columns=[c.strip() for c in line.split('|')]
        if len(columns)>4 and re.fullmatch(r'VLM-BATCH-\d{3}',columns[1]) and columns[3].startswith('**READY'):
            active.append(columns[1])
    if active!=[parent]: raise PilotError('PARENT_NOT_UNIQUE_READY')
    if re.search(r'^### '+re.escape(parent)+r'\s',results,re.M): raise PilotError('PARENT_ALREADY_REPORTED')
    readme=(docs/'docs/codex-artifacts'/parent/'README.md').read_text(encoding='utf-8')
    if not all(x in readme for x in ('Charades_v1_480.zip','64','128','ffprobe')):
        raise PilotError('PARENT_MEDIA_SCOPE_UNVERIFIED')


def fixed_preflight():
    from charades_metadata_audit import check_ancestors
    import winreg
    base=pathlib.Path(os.environ['LOCALAPPDATA']).absolute()
    meta=base/'VLM-Research-Isolated/Charades-v1-Metadata'
    pilot=base/'VLM-Research-Isolated/Charades-v1-MediaPilot'
    original_value=os.environ.get('VLM_ORIGINAL_WORKSPACE')
    if not original_value: raise PilotError('ORIGINAL_WORKSPACE_EXCLUSION_UNKNOWN')
    docs=pathlib.Path(__file__).resolve().parent.parent
    forbidden=[meta,docs,pathlib.Path(original_value).absolute()]
    for key in ('OneDrive','OneDriveConsumer','OneDriveCommercial','Dropbox','BOX_SYNC'):
        if os.environ.get(key): forbidden.append(pathlib.Path(os.environ[key]).absolute())
    def names(key):
        result=[]; index=0
        while True:
            try: result.append(winreg.EnumKey(key,index)); index+=1
            except OSError as e:
                if e.winerror==259: return result
                raise
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\OneDrive\Accounts') as accounts:
            for name in names(accounts):
                with winreg.OpenKey(accounts,name) as account:
                    try: forbidden.append(pathlib.Path(winreg.QueryValueEx(account,'UserFolder')[0]).absolute())
                    except FileNotFoundError: pass
    except FileNotFoundError: pass
    for hive in (winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.OpenKey(hive,r'Software\Microsoft\Windows\CurrentVersion\Explorer\SyncRootManager') as providers:
                for name in names(providers):
                    try:
                        with winreg.OpenKey(providers,name+r'\UserSyncRoots') as key:
                            i=0
                            while True:
                                try:
                                    _,value,kind=winreg.EnumValue(key,i); i+=1
                                    if kind in (winreg.REG_SZ,winreg.REG_EXPAND_SZ): forbidden.append(pathlib.Path(os.path.expandvars(value)).absolute())
                                except OSError as e:
                                    if e.winerror==259: break
                                    raise
                    except FileNotFoundError: pass
        except FileNotFoundError: pass
    check_ancestors(pilot); check_ancestors(meta)
    if pilot.exists(): raise PilotError('PILOT_ROOT_ALREADY_EXISTS')
    if base.resolve(strict=True) not in pilot.resolve().parents: raise PilotError('PILOT_CONTAINMENT')
    for target in (pilot,pilot.resolve()):
        for p in forbidden:
            for b in (p.absolute(),p.resolve()):
                if target==b or b in target.parents or target in b.parents: raise PilotError('PILOT_FORBIDDEN_OVERLAP')
    if shutil.disk_usage(base).free<512*MIB: raise PilotError('PILOT_DISK_SPACE')
    sources={'zip':meta/'incoming/Charades.zip','train':meta/'extracted/Charades_v1_train.csv','classes':meta/'extracted/Charades_v1_classes.txt'}
    for role,p in sources.items():
        check_ancestors(p); digest=hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda:f.read(65536),b''): digest.update(chunk)
        if digest.hexdigest()!=SOURCE_SHA[role]: raise PilotError('SOURCE_SHA_MISMATCH')
    return pilot,sources


def official_anchor(text):
    class Links(html.parser.HTMLParser):
        def __init__(self): super().__init__(); self.href=None; self.parts=[]; self.found=[]
        def handle_starttag(self,tag,attrs):
            if tag=='a': self.href=dict(attrs).get('href'); self.parts=[]
        def handle_data(self,data):
            if self.href is not None: self.parts.append(data)
        def handle_endtag(self,tag):
            if tag=='a' and self.href is not None:
                if ' '.join(''.join(self.parts).split())=='Data (scaled to 480p, 13 GB)': self.found.append(self.href)
                self.href=None
    parser=Links(); parser.feed(text)
    if parser.found!=[URL]: raise PilotError('OFFICIAL_ANCHOR_CHANGED')


def owned_disk_bytes(root):
    from charades_metadata_audit import check_ancestors
    total=0
    for p in root.rglob('*'):
        check_ancestors(p)
        if p.is_file(): total+=p.stat().st_size
    return total


def transfer_two(client,selection,root):
    from charades_metadata_audit import check_ancestors
    tail=client.get(max(0,client.total-128*1024),client.total-1)
    offset,size,count=eocd(tail,client.total,client.get)
    if client.ledger.state['body_bytes']+size>NET_LIMIT: raise PilotError('CENTRAL_NETWORK_BUDGET')
    directory=client.get(offset,offset+size-1)
    all_entries=central_directory(directory,count,offset)
    entries=match_two(all_entries,[x['id'] for x in selection])
    windows=[]
    for entry in entries:
        pos=entry['offset']; header=client.get(pos,pos+29)
        n,e=struct.unpack_from('<HH',header,26)
        if n+e==0 or pos+30+n+e+entry['compressed']>offset: raise PilotError('LOCAL_RANGE_BOUNDS')
        variable=client.get(pos+30,pos+29+n+e)
        local_header(header,variable,entry)
        next_offset=min((x['offset'] for x in all_entries if x['offset']>pos),default=offset)
        if pos+30+n+e+entry['compressed']>next_offset: raise PilotError('LOCAL_MEMBER_OVERLAP')
        windows.append((pos+30+n+e,entry))
    if client.ledger.state['body_bytes']+sum(e['compressed'] for _,e in windows)>NET_LIMIT:
        raise PilotError('MEDIA_NETWORK_BUDGET')
    if owned_disk_bytes(root)+2*sum(e['size'] for _,e in windows)+AUDIT_RESERVE>DISK_LIMIT:
        raise PilotError('MEDIA_STORAGE_PREFLIGHT')
    saved=[]
    for index,(start,entry) in enumerate(windows):
        if entry['compressed']<=0 or entry['size']<=0: raise PilotError('EMPTY_MEDIA_MEMBER')
        body=client.get(start,start+entry['compressed']-1)
        output=expand_member(body,entry)
        part=root/'incoming'/('case-'+str(index)+'.part'); final=root/'media'/('case-'+str(index)+'.mp4')
        check_ancestors(part); check_ancestors(final)
        if part.exists() or final.exists(): raise PilotError('MEDIA_DESTINATION_EXISTS')
        if owned_disk_bytes(root)+2*len(output)+AUDIT_RESERVE>DISK_LIMIT: raise PilotError('MEDIA_STORAGE_BUDGET')
        with part.open('xb') as f: f.write(output)
        client.ledger.disk(owned_disk_bytes(root))
        os.link(part,final)  # Atomic exclusive final publication; never overwrites.
        client.ledger.disk(owned_disk_bytes(root)); part.unlink()
        client.ledger.state['saved_videos']=len(saved)+1; client.ledger.save()
        saved.append({'file':final,'sha256':hashlib.sha256(output).hexdigest(),'case_index':index})
    return saved


def run_pilot(execute=False,parent='VLM-BATCH-013'):
    # Repair/preflight mode never accesses the network or media store.
    executable=find_ffprobe()
    version=subprocess.run([str(executable),'-version'],capture_output=True,timeout=10,check=True)
    if not version.stdout.startswith(b'ffprobe version'): raise PilotError('FFPROBE_VERSION_UNVERIFIED')
    if not execute: return {'status':'PREFLIGHT_ONLY','ffprobe':'AVAILABLE','response_body_bytes':0,'saved_videos':0}
    docs=pathlib.Path(__file__).resolve().parent.parent; authorize_parent(parent,docs)
    # Same fixed synthetic suite is mandatory even for a later approved executor.
    import unittest
    suite=unittest.defaultTestLoader.loadTestsFromName('test_charades_range_media_clock_pilot')
    checked=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    if not checked.wasSuccessful() or checked.testsRun<12: raise PilotError('SYNTHETIC_GATE_FAILED')
    root,sources=fixed_preflight()
    classes={line.split()[0] for line in sources['classes'].read_text(encoding='utf-8-sig').splitlines() if line.strip()}
    with sources['train'].open('r',encoding='utf-8-sig',newline='') as f:
        rows=[{k:r.get(k) for k in ('id','subject','actions','length')} for r in csv.DictReader(f)]
    selection=select_cases(rows,classes)
    root.mkdir(exist_ok=False)
    for name in ('incoming','media','local-audit'): (root/name).mkdir(exist_ok=False)
    with (root/'local-audit/selection.json').open('x',encoding='utf-8') as f: json.dump(selection,f,default=str)
    ledger=Ledger(root/'local-audit/network-ledger.json')
    client=RangeClient(ledger,0,'')
    clock={}
    try:
        official_anchor(client.text(PAGE,512*1024).decode('utf-8'))
        license_body=client.text(LICENSE,16*1024)
        if hashlib.sha256(license_body).hexdigest()!='a734f9263490d2a0567da2e39f109f3cf535896e4efb91caaefa27644ac628f0':
            raise PilotError('OFFICIAL_LICENSE_CHANGED')
        with client.opener.open(urllib.request.Request(URL,method='HEAD',headers={'Accept-Encoding':'identity'}),timeout=30) as head:
            if head.status!=200 or head.geturl()!=URL or 'zip' not in head.headers.get('Content-Type','').lower(): raise PilotError('HEAD_SOURCE_UNVERIFIED')
            total=int(head.headers['Content-Length']); etag=head.headers.get('ETag')
            if total<=0 or not etag: raise PilotError('HEAD_SIZE_ETAG_UNKNOWN')
        client.total=total; client.etag=etag
        ledger.state['source']={'total':total,'etag':etag}; ledger.save()
        saved=transfer_two(client,selection,root)
        for item,chosen,case in zip(saved,selection,('CASE_OVERFLOW','CASE_CONTROL')):
            command=ffprobe_command(executable,item['file'])
            process=subprocess.run(command,capture_output=True,timeout=60,check=True)
            probe=json.loads(process.stdout)
            clock[case]=classify_clock(probe,chosen['length'])
            payload=json.dumps({'probe':probe,'media_sha256':item['sha256'],'category':clock[case],
                                'selected_end_relation':endpoint_relation(probe,chosen)}).encode('utf-8')
            if owned_disk_bytes(root)+len(payload)+AUDIT_RESERVE>DISK_LIMIT: raise PilotError('CLOCK_AUDIT_STORAGE_BUDGET')
            with (root/'local-audit'/('clock-'+str(item['case_index'])+'.json')).open('xb') as f: f.write(payload)
            ledger.disk(owned_disk_bytes(root))
        result=public_receipt(ledger.state,clock); result['status']='CASE_LIMITED_COMPLETE'
        return result
    except Exception as e:
        ledger.state['stopped']=str(e) if isinstance(e,PilotError) else type(e).__name__; ledger.save()
        result=public_receipt(ledger.state,clock); result['status']='BLOCKED'; result['reason']=ledger.state['stopped']
        return result


if __name__=='__main__':
    try:
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--execute',action='store_true')
        parser.add_argument('--parent-task',default='VLM-BATCH-013')
        args=parser.parse_args()
        result=run_pilot(args.execute,args.parent_task)
        print(json.dumps(result))
        if result.get('status')=='BLOCKED': raise SystemExit(1)
    except PilotError as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e),'response_body_bytes':0,'saved_videos':0}))
        raise SystemExit(1) from None
    except Exception:
        print(json.dumps({'status':'BLOCKED','reason':'UNVERIFIED_ENVIRONMENT','response_body_bytes':0,'saved_videos':0}))
        raise SystemExit(1) from None
