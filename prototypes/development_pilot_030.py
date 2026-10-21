"""030 production helpers routed to fixed034; old runs stay closed.

Windows sharing/Job gates are OS gates, not a hostile-code sandbox. Every child
waits for a parent handshake before dependency imports or research work.
"""
import argparse
import ctypes
from ctypes import wintypes as W
from dataclasses import asdict
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import uuid

from temporal_evidence_adapter_025 import ContractError
from temporal_pilot_prepare_026 import checked_path

MIB = 1024 ** 2
GIB = 1024 ** 3


def require(condition, reason):
    if not condition:
        raise ContractError(reason)


def packed(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(packed(value)).hexdigest()


class Journal:
    """OS-locked, append/fsync hash chain; a consumed attempt never refunds."""
    def __init__(self, root, create=False, fixture=False):
        self.root = Path(root)
        require(self.root.name == 'integration_034', 'FIXED_034_ROOT_REQUIRED')
        if create:
            checked_path(self.root.parent, directory=True)
            self.root.mkdir()  # Existing root is terminal, never resume/relabel.
        checked_path(self.root, directory=True)
        self.lock = open(self.root / '034.lock', 'a+b')
        import msvcrt
        self.lock.seek(0)
        if self.lock.read(1) == b'':
            self.lock.write(b'0'); self.lock.flush(); os.fsync(self.lock.fileno())
        self.lock.seek(0)
        msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
        self.path = self.root / '034-ledger.jsonl'
        self.rows = []
        self.byte_length = 0
        if self.path.exists():
            raw = self.path.read_bytes()
            self.byte_length = len(raw)
            require(len(raw) <= 8 * MIB and raw.endswith(b'\n'), 'LEDGER_TRUNCATED')
            for line in raw.splitlines():
                row = json.loads(line)
                sig = row.pop('hash')
                require(row['seq'] == len(self.rows) and row['prev'] == (self.rows[-1]['hash'] if self.rows else '0' * 64)
                        and sig == digest(row), 'LEDGER_CHAIN')
                self.rows.append(dict(row, hash=sig))
        if create:
            if fixture:
                require(self.root.parent.name.startswith('witness-') and self.root.parent.parent.name=='integration_034','FIXTURE_ANCESTRY')
            self.add('RUN', contract_id='034', root_name='integration_034', purpose='FICTIONAL_034_WITNESS' if fixture else 'REAL_034',
                     run_id=uuid.uuid4().hex, epoch=time.time(), parent_cap=2400)
        require(self.rows and self.rows[0]['event'] == 'RUN' and self.rows[0].get('contract_id') == '034'
                and self.rows[0].get('root_name') == self.root.name, 'RUN_REQUIRED')
        self.check_time()

    def close(self):
        self.lock.close()

    def check_time(self):
        if self.rows:
            require(0 <= time.time() - self.rows[0]['epoch'] < 2400, 'PARENT_DEADLINE')

    def add(self, event, **fields):
        self.check_time()
        require(event not in ('HTTPS','TRANSPORT_SEND','BODY_DEBIT','MEDIA_COMPLETE'), '034_NETWORK_MEDIA_FORBIDDEN')
        if event=='GPU_QUERY':
            require(fields.get('key')=='0' and not self.events('GPU_QUERY'),'034_ONE_QUERY_ONLY')
        if event=='STARTED':
            validate_start_034(self.rows,load(self.root,'queue.json'),load(self.root,'worker-input.json'),fields)
            resource_receipt_034(self.rows,self.root)
        if event=='MODEL_LAUNCH':
            receipt=resource_receipt_034(self.rows,self.root)
            require(fields.get('resource_hash')==receipt['hash'],'034_LAUNCH_RESOURCE_BINDING')
        row = dict(seq=len(self.rows), prev=self.rows[-1]['hash'] if self.rows else '0' * 64,
                   event=event, **fields)
        row['hash'] = digest(row)
        raw = packed(row) + b'\n'
        require(self.byte_length + len(raw) <= 8 * MIB, 'LEDGER_BYTES')
        with open(self.path, 'ab') as target:
            target.write(raw); target.flush(); os.fsync(target.fileno())
        self.rows.append(row)
        self.byte_length += len(raw)

    def events(self, event):
        return [r for r in self.rows if r['event'] == event]

    def once(self, event, key, **fields):
        require(not any(r.get('key') == key for r in self.events(event)), 'CONSUMED_NO_RETRY')
        self.add(event, key=key, **fields)

    def reserve_time(self, stage, seconds, key):
        caps = dict(cpu=600, gpu=900)
        require(stage in caps and seconds > 0 and
                sum(r['seconds'] for r in self.events('WINDOW') if r['stage'] == stage) + seconds <= caps[stage], 'STAGE_TIME')
        self.once('WINDOW', key, stage=stage, seconds=seconds)

    def reserve_output(self, name, size, category='metadata', files=1):
        require(Path(name).name == name and name not in ('034.lock', '034-ledger.jsonl') and size >= 0, 'OUTPUT_NAME')
        used = self.events('OUTPUT')
        limits = dict(metadata=32 * MIB - 9 * MIB, frames=256 * MIB)
        require(category in limits and type(files) is int and 1<=files<=32 and sum(r.get('files',1) for r in used) + files + 2 <= 128 and
                sum(r['size'] for r in used) + size + 9 * MIB <= 512 * MIB and
                sum(r['size'] for r in used if r['category'] == category) + size <= limits[category], 'OUTPUT_CAP')
        require(not (self.root / name).exists(), 'OUTPUT_EXISTS')
        self.once('OUTPUT', name, size=size, category=category, files=files)

    def write(self, name, value):
        raw = packed(value)
        self.reserve_output(name, len(raw))
        with open(self.root / name, 'xb') as target:
            target.write(raw); target.flush(); os.fsync(target.fileno())

    def input(self, alias, path, category='handoff'):
        path, before = checked_path(path)
        caps = dict(handoff=22, source=4, config=4, gold=1)
        cap = 4*MIB if category=='gold' else 2*MIB if alias=='archive_033' else MIB
        used = self.events('INPUT')
        require(category in caps and sum(r['category'] == category for r in used) < caps[category]
                and 0 < before.st_size <= cap and
                sum(r['size'] for r in used if r['category']!='frame-cache') + before.st_size <= 40 * MIB, 'INPUT_CAP')
        ident = [before.st_dev, before.st_ino]
        require(before.st_ino > 0 and not any(r['identity'] == ident or r['path'].casefold() == str(path).casefold() for r in used), 'INPUT_ALIAS')
        self.once('INPUT', alias, path=str(path), identity=ident, size=before.st_size, category=category)
        with open(path, 'rb') as source:
            opened = os.fstat(source.fileno())
            require(os.path.samestat(before, opened), 'INPUT_IDENTITY')
            raw = source.read(cap + 1)
            after_fd = os.fstat(source.fileno())
        after = path.stat()
        # Compare each API to itself: Windows path/fd ctime may differ.
        stable = lambda a, b: (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns) == (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
        require(stable(before, after) and stable(opened, after_fd) and len(raw) == before.st_size, 'INPUT_CHANGED_OR_PARTIAL')
        self.add('INPUT_COMPLETE', alias=alias, size=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        return raw


def load(root, name):
    return json.loads((Path(root) / name).read_bytes())


def archive_rows(raw):
    """Read-only historical validation. No old Journal, lock, epoch check or writes."""
    require(0 < len(raw) <= MIB and raw.endswith(b'\n'), 'ARCHIVE_INCOMPLETE')
    rows=[]
    for line in raw.splitlines():
        row=json.loads(line); signature=row.pop('hash')
        require(row['seq']==len(rows) and row['prev']==(rows[-1]['hash'] if rows else '0'*64)
                and digest(row)==signature,'ARCHIVE_CHAIN')
        rows.append(dict(row,hash=signature))
    require(rows and rows[0]['event']=='RUN' and any(r['event']=='RUN_STOPPED' for r in rows),'ARCHIVE_NOT_STOPPED')
    terminal=[r for r in rows if r['event']=='TERMINAL']
    require(len(terminal)==16 and {r['key'] for r in terminal}=={str(n) for n in range(16)}
            and all(r['state']=='NOT_RUN' for r in terminal)
            and not any(r['event'] in ('HTTPS','STARTED','MODEL_LAUNCH','SCORE_CONSUMED')
                        or r['event']=='INPUT' and r.get('category')=='gold' for r in rows),'ARCHIVE_REAL_ACTION_OR_QUEUE')
    return rows


def archive_031_rows(raw):
    """031 is a closed metadata/network archive, NOT a zero-action030 run."""
    require(0<len(raw)<=MIB and raw.endswith(b'\n'),'ARCHIVE_031_INCOMPLETE')
    rows=[]
    for line in raw.splitlines():
        row=json.loads(line);signature=row.pop('hash')
        require(row['seq']==len(rows) and row['prev']==(rows[-1]['hash'] if rows else '0'*64)
                and digest(row)==signature,'ARCHIVE_031_CHAIN')
        rows.append(dict(row,hash=signature))
    require(rows and rows[0].get('contract_id')=='031' and rows[0].get('root_name')=='integration_031'
            and rows[0].get('purpose')=='REAL_031' and rows[-1]['event']=='RUN_STOPPED','ARCHIVE_031_IDENTITY_OR_OPEN')
    terminals=[r for r in rows if r['event']=='TERMINAL'];suite=[r for r in rows if r['event']=='SUITE_RESULT']
    require(len(terminals)==16 and {r['key'] for r in terminals}=={str(i) for i in range(16)}
            and all(r['state']=='NOT_RUN' for r in terminals),'ARCHIVE_031_TERMINALS')
    require(len(suite)==1 and suite[0]['passed'] is True and suite[0]['tests']==7
            and suite[0].get('contract_id')=='031' and suite[0].get('run_id')==rows[0]['run_id']
            and suite[0].get('failures')==suite[0].get('errors')==suite[0].get('skips')==0,'ARCHIVE_031_SUITE')
    require(not any(r['event'] in ('BODY_DEBIT','MEDIA_COMPLETE','STARTED','MODEL_LAUNCH','SCORE_CONSUMED')
                        or r['event']=='INPUT' and r.get('category')=='gold' for r in rows),'ARCHIVE_031_HAS_MEDIA_MODEL_OR_GOLD')
    http=[r for r in rows if r['event']=='HTTPS'];sent=[r for r in rows if r['event']=='TRANSPORT_SEND']
    require(len(http)==len(sent)==11 and len({r['key'] for r in http})==11
            and sorted((r['key'],r['method'],r['url']) for r in http)==sorted((r['slot'],r['method'],r['url']) for r in sent)
            and [sum(r['api']==api for r in http) for api in ('HeadBucket','HeadObject','GetObject')]==[3,4,4],'ARCHIVE_031_NETWORK')
    heads=[r for r in rows if r['event']=='OBJECT_HEAD_TERMINAL']
    require(len(heads)==4 and {r['alias'] for r in heads}=={'P1','P2','P3','P4'}
            and all(r['observed_status']==200 for r in heads),'ARCHIVE_031_HEAD_TERMINALS')
    return rows


def validate_031_metadata(rows, payload):
    from urllib.parse import urlsplit,parse_qsl,quote
    from source_provenance_029 import canonical_object
    completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'}
    outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
    for name in ('keys','cohort','nongold','plan','receipts','targets','heads029','official'):
        raw=payload[name][0];expected=completed['cache_'+name]
        require(len(raw)==expected['size']==outputs[name+'.json']['size'] and hashlib.sha256(raw).hexdigest()==expected['sha256'],
                'ARCHIVE_031_CACHE_BYTES_'+name.upper())
    for name in ('annotation-reference','execution-config','runtime','metadata-summary'):
        require(len(payload[name][0])==outputs[name+'.json']['size'],'ARCHIVE_031_RETAINED_OUTPUT_SIZE')
    targets=payload['targets'][1]['targets'];summary=payload['metadata-summary'][1]['results']
    require(len(targets)==len(summary)==4 and [t['alias'] for t in targets]==['P1','P2','P3','P4'],'ARCHIVE_031_FOUR')
    heads=[]
    for target,record in zip(targets,summary):
        alias=target['alias'];raw,head=payload[alias+'-head']
        require(head==record and len(raw)==outputs[alias+'-head.json']['size'] and head['alias']==alias
                and head['status']==200 and head['eligible'] is True and type(head['ContentLength']) is int
                and 0<head['ContentLength']<=4*GIB and type(head.get('VersionId')) is str and bool(head['VersionId'])
                and type(head.get('ETag')) is str and head['ETag'].startswith('"') and head['ETag'].endswith('"')
                and not head['ETag'].startswith('W/') and type(head.get('region')) is str,'ARCHIVE_031_HEAD_PIN')
        require(canonical_object(target['uri'])==(target['bucket'],target['key']) and outputs[alias+'.partial']['size']==head['ContentLength'],
                'ARCHIVE_031_MEDIA_RESERVATION')
        attempts=[r for r in rows if r['event']=='TRANSPORT_SEND' and r['slot']=='GetObject:'+alias]
        require(len(attempts)==1,'ARCHIVE_031_UNIQUE_GET')
        request=attempts[0];url=urlsplit(request['url'])
        require(request['method']=='GET' and url.scheme=='https' and url.netloc=='s3.'+head['region']+'.amazonaws.com'
                and url.path=='/'+target['bucket']+'/'+quote(target['key'],safe='/~')
                and parse_qsl(url.query)==[('versionId',head['VersionId'])] and not url.fragment,'ARCHIVE_031_WIRE_VERSION_BINDING')
        heads.append(head)
    require(sum(h['ContentLength'] for h in heads)==6002290187,'ARCHIVE_031_EXACT_LENGTH_TOTAL')
    old=next(h for h in payload['heads029'][1]['results'] if h['alias']=='P1')
    require(heads[0]['ContentLength']<=890*MIB and all(heads[0][k]==old.get(k) for k in ('ContentLength','ETag','VersionId')),'ARCHIVE_031_P1_029_BINDING')
    return heads


def transfer_cache_032(root, old_root):
    raise ContractError('OLD_032_TRANSFER_CLOSED')
    journal=Journal(root,create=True)
    try:
        journal.reserve_time('cpu',45,'cache-initialize')
        old=Path(old_root);require(old.name=='integration_031','EXACT_031_ARCHIVE_ROOT')
        rows=archive_031_rows(journal.input('archive_031',old/'031-ledger.jsonl'))
        names=['keys','cohort','nongold','plan','receipts','targets','heads029','official',
               'annotation-reference','execution-config','runtime','P1-head','P2-head','P3-head','P4-head','metadata-summary']
        payload={}
        for name in names:
            raw=journal.input('cache_'+name,old/(name+'.json'));payload[name]=(raw,json.loads(raw))
        validate_031_metadata(rows,payload)
        for name in names:
            if name not in ('runtime','execution-config'):
                journal.write(name+'.json',payload[name][1])
        completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'}
        outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
        for alias in ('factory_0','factory_1','runner_0','runner_1'):
            raw=journal.input('cache_'+alias,old/(alias+'.py'),'source');expected=completed['cache_'+alias]
            require(len(raw)==expected['size']==outputs[alias+'.py']['size'] and hashlib.sha256(raw).hexdigest()==expected['sha256'],'ARCHIVE_031_SOURCE_BYTES')
            journal.reserve_output(alias+'.py',len(raw))
            with open(journal.root/(alias+'.py'),'xb') as target:target.write(raw);target.flush();os.fsync(target.fileno())
        execution=dict(payload['execution-config'][1],runtime=payload['runtime'][1])
        journal.write('execution-config.json',execution)
        journal.write('runtime-handoff.json',payload['runtime'][1])
        journal.write('032-handoff-private.json',dict(archive_hash=rows[-1]['hash'],archive_run_id=rows[0]['run_id'],
            source='READONLY_031_ARCHIVE',metadata_binding='RETAINED_RECEIPT_AND_WIRE_VERSION_NOT_HISTORICAL_HEAD_SHA',
            exact_media_total=6002290187,objects=4,profile='CURRENT_IFMATCH_PINNED_RESPONSE_032'))
        journal.add('CACHE_BOUND',inputs=21,archive_hash=rows[-1]['hash'],retained_heads=4,new_heads=0)
    finally:journal.close()


AVAILABLE_034 = dict(P1=False,P2=True,P3=False,P4=False)
RESOURCE_PROFILE_034 = 'MEMORY_BOUNDED_SHARED_GPU_034'


def validate_queue_034(queue, config):
    slots=[dict(slot=n,alias='P%d' % (n//4+1),arm='ABCD'[(n%4+n//4)%4]) for n in range(16)]
    require(queue.get('available')==AVAILABLE_034 and queue.get('slots')==config.get('slots')==slots,
            '034_FIXED_FULL_QUEUE')


def validate_start_034(rows, queue, config, item):
    validate_queue_034(queue,config)
    started=[r for r in rows if r.get('event')=='STARTED']
    expected=[s for s in queue['slots'] if s['alias']=='P2']
    require(len(started)<4 and str(item.get('key'))==str(expected[len(started)]['slot'])
            and item.get('alias')=='P2' and item.get('arm')==expected[len(started)]['arm']
            and not any(r['key']==str(item.get('key')) for r in started),'034_ONLY_P2_FOUR_STARTS')


def parse_resource_sample_034(raw, expected, query_device=0):
    import math,re
    import xml.etree.ElementTree as ET
    require(type(query_device) is int and query_device==0,'034_QUERY_DEVICE_REQUIRED')
    require(type(raw) is str and len(raw.encode())<=65536,'034_XML_BOUND')
    tree=ET.fromstring(raw);gpus=tree.findall('gpu');require(len(gpus)==1,'034_ONE_DEVICE')
    gpu=gpus[0];uid=gpu.findtext('uuid');bus=gpu.get('id')
    require('3090' in gpu.findtext('product_name','') and bool(uid) and bool(bus)
            and expected.get('query_device')==0 and uid==expected.get('uuid') and bus==expected.get('bus'),'034_DEVICE_IDENTITY')
    free_text=gpu.findtext('fb_memory_usage/free','')
    match=re.fullmatch(r'([0-9]+(?:\.[0-9]+)?) MiB',free_text)
    require(match is not None,'034_FREE_UNITS');free=float(match[1])
    require(math.isfinite(free) and free>=20*1024,'034_FREE_THRESHOLD')
    util=None;match=re.fullmatch(r'([0-9]+(?:\.[0-9]+)?) %',gpu.findtext('utilization/gpu_util',''))
    if match:
        value=float(match[1])
        if math.isfinite(value) and 0<=value<=100:util=value
    types=[p.findtext('type','UNKNOWN') for p in gpu.findall('processes/process_info')]
    return dict(uuid=uid,bus=bus,device='0',reported_minor=gpu.findtext('minor_number','UNKNOWN'),
                free_MiB=free,utilization_percent=util,driver_model=gpu.findtext('driver_model/current_dm','UNKNOWN'),
                process_types={t:types.count(t) for t in sorted(set(types))})


def resource_receipt_034(rows, root):
    found=[r for r in rows if r.get('event')=='RESOURCE_ADMITTED']
    require(len(found)==1,'034_RESOURCE_RECEIPT_REQUIRED')
    require(len([r for r in rows if r.get('event')=='GPU_QUERY' and r.get('key')=='0'])==1
            and len([r for r in rows if r.get('event')=='GPU_QUERY'])==1,'034_QUERY_RECEIPT_REQUIRED')
    receipt=found[0];queue=load(root,'queue.json');config=load(root,'worker-input.json')
    validate_queue_034(queue,config)
    require(rows[0].get('contract_id')=='034' and queue.get('contract_id')=='034'
            and receipt.get('run_id')==queue.get('run_id')==rows[0].get('run_id')
            and receipt.get('profile')==RESOURCE_PROFILE_034 and receipt.get('queue_hash')==digest(queue),
            '034_RESOURCE_BINDING')
    observations=load(root,'gpu-samples-private.json')
    require(len(observations['xml'])==len(observations['starts'])==1,'034_ONE_CURRENT_SAMPLE')
    sample=parse_resource_sample_034(observations['xml'][0],load(root,'device-identity-reference.json'),observations.get('query_device'))
    require(receipt.get('sample_hash')==digest(sample) and receipt.get('device_uuid')==sample['uuid'],
            '034_RESOURCE_SAMPLES_BINDING')
    return receipt


def query_resource_034(root):
    """One bounded child, one current observation, utilization is descriptive only."""
    journal=Journal(root)
    try:
        require_ready(journal);queue=load(root,'queue.json');validate_queue_034(queue,load(root,'worker-input.json'))
        xmls=[];starts=[]
        for number in range(1):
            journal.once('GPU_QUERY',str(number))
            starts.append(time.monotonic())
            child=subprocess.Popen(['nvidia-smi','-q','-x','-i','0'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                   creationflags=0x08000000,close_fds=True)
            buffers=[bytearray(),bytearray()];overflow=threading.Event();threads=[]
            def capture(stream,buffer):
                while True:
                    chunk=stream.read(4096)
                    if not chunk:break
                    if len(buffer)+len(chunk)>65536:overflow.set()
                    buffer.extend(chunk[:max(0,65536-len(buffer))])
            for stream,buffer in zip((child.stdout,child.stderr),buffers):
                thread=threading.Thread(target=capture,args=(stream,buffer),daemon=True);thread.start();threads.append(thread)
            try:
                child.wait(timeout=6)
            finally:
                if child.poll() is None:child.kill();child.wait(timeout=1)
                for thread in threads:thread.join(1)
                child.stdout.close();child.stderr.close()
            require(child.returncode==0 and not overflow.is_set() and not any(t.is_alive() for t in threads),'034_QUERY_CAPTURE')
            xmls.append(bytes(buffers[0]).decode('utf-8',errors='strict'))
        journal.write('gpu-samples-private.json',dict(xml=xmls,starts=starts,query_device=0))
        sample=parse_resource_sample_034(xmls[0],load(root,'device-identity-reference.json'))
        journal.once('RESOURCE_ADMITTED','gpu',run_id=journal.rows[0]['run_id'],profile=RESOURCE_PROFILE_034,
                     queue_hash=digest(queue),sample_hash=digest(sample),device_uuid=sample['uuid'])
    finally:journal.close()



validate_queue_033 = validate_queue_034  # Same frozen slot/availability rule for old cache validation.

def archive_032_rows(raw):
    """Closed partial-media032 archive; never instantiate its Journal."""
    require(0<len(raw)<=2*MIB and raw.endswith(b'\n'),'ARCHIVE_032_INCOMPLETE')
    rows=[]
    for line in raw.splitlines():
        row=json.loads(line);signature=row.pop('hash')
        require(row['seq']==len(rows) and row['prev']==(rows[-1]['hash'] if rows else '0'*64)
                and digest(row)==signature,'ARCHIVE_032_CHAIN');rows.append(dict(row,hash=signature))
    require(rows[0].get('contract_id')=='032' and rows[0].get('root_name')=='integration_032'
            and rows[0].get('purpose')=='REAL_032' and rows[-1]['event']=='RUN_STOPPED','ARCHIVE_032_IDENTITY_STOP')
    events=lambda name:[r for r in rows if r['event']==name]
    require(not any(r['event'] in ('STARTED','MODEL_LAUNCH','SCORE_CONSUMED') or
                    r['event']=='INPUT' and r.get('category')=='gold' for r in rows),'ARCHIVE_032_MODEL_GOLD')
    terminal=events('TERMINAL');suites=events('SUITE_RESULT')
    require(len(terminal)==16 and {r['key'] for r in terminal}=={str(n) for n in range(16)}
            and all(r['state']=='NOT_RUN' for r in terminal),'ARCHIVE_032_TERMINALS')
    require(len(suites)==1 and suites[0].get('contract_id')=='032' and suites[0].get('run_id')==rows[0]['run_id']
            and suites[0].get('passed') is True and suites[0].get('tests')==6
            and suites[0].get('failures')==suites[0].get('errors')==suites[0].get('skips')==0,'ARCHIVE_032_SUITE')
    http=events('HTTPS');sent=events('TRANSPORT_SEND');response=events('TRANSPORT_RESPONSE')
    wanted={'GetObject:P%d'%n for n in range(1,5)}
    require(len(http)==len(sent)==len(response)==4 and {r['key'] for r in http}==wanted
            and {r['slot'] for r in sent}=={r['slot'] for r in response}==wanted
            and all(r['api']=='GetObject' and r['method']=='GET' for r in http)
            and all(r['status']==200 and r.get('profile')=='CURRENT_IFMATCH_PINNED_RESPONSE_032' for r in response)
            and sorted((r['key'],r['url']) for r in http)==sorted((r['slot'],r['url']) for r in sent),'ARCHIVE_032_HTTP')
    require(len(events('MEDIA_COMPLETE'))==1 and events('MEDIA_COMPLETE')[0]['alias']=='P2','ARCHIVE_032_P2_MEDIA')
    exits={r['name']:r for r in events('PHASE_EXIT')}
    require(all(exits[n]['code']==0 and exits[n]['job_active']==0 for n in ('get-P2','candidates-P2'))
            and all(exits['get-'+a]['code']==99 and exits['get-'+a]['job_active']==0 for a in ('P1','P3','P4')),
            'ARCHIVE_032_EXIT')
    return rows


def validate_cache_032(rows, payload):
    completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'}
    output={r['key']:r for r in rows if r['event']=='OUTPUT'}
    for name in ('keys','cohort','nongold','plan','receipts','targets','heads029','official','P2-head'):
        raw=payload[name][0];prior=completed['cache_'+name]
        require(len(raw)==prior['size']==output[name+'.json']['size'] and hashlib.sha256(raw).hexdigest()==prior['sha256'],
                '033_CACHE_BYTES')
    for name,(raw,value) in payload.items():
        require(name+'.json' in output and len(raw)==output[name+'.json']['size'],'033_RETAINED_OUTPUT_SIZE')
    head=payload['P2-head'][1];media=payload['P2-media-binding'][1];candidate=payload['P2-candidates'][1]
    target=next(t for t in payload['targets'][1]['targets'] if t['alias']=='P2')
    from urllib.parse import urlsplit,quote
    require([t['alias'] for t in payload['targets'][1]['targets']]==['P1','P2','P3','P4'],'033_TARGETS')
    for t in payload['targets'][1]['targets']:
        sent=next(r for r in rows if r['event']=='TRANSPORT_SEND' and r['slot']=='GetObject:'+t['alias'])
        wire=urlsplit(sent['url'])
        require(wire.scheme=='https' and wire.path=='/'+t['bucket']+'/'+quote(t['key'],safe='/~')
                and not wire.query and not wire.fragment,'033_FOUR_FIXED_OBJECTS')
    request=next(r for r in rows if r['event']=='TRANSPORT_SEND' and r['slot']=='GetObject:P2');url=urlsplit(request['url'])
    require(url.scheme=='https' and url.netloc=='s3.'+head['region']+'.amazonaws.com' and
            url.path=='/'+target['bucket']+'/'+quote(target['key'],safe='/~') and not url.query and not url.fragment,'033_EXACT_P2_WIRE')
    require(head['eligible'] is True and head['status']==200 and media['alias']=='P2' and media['uri']==target['uri']
            and all(media[k]==head[k] for k in ('ETag','VersionId','ContentLength'))
            and media['size']==media['received']==head['ContentLength'],'033_MEDIA_BINDING')
    complete=next(r for r in rows if r['event']=='MEDIA_COMPLETE')
    require(complete['size']==media['size'],'033_MEDIA_COMPLETE_BINDING')
    frozen=[r for r in rows if r['event']=='FROZEN'];config=payload['worker-input'][1];queue=payload['queue'][1]
    require(len(frozen)==1 and frozen[0]['worker_hash']==digest(config)==queue['worker_hash']
            and frozen[0]['plan_hash']==digest(payload['plan'][1]['plan'])==queue['plan_hash']
            and queue['contract_id']=='032' and queue['run_id']==rows[0]['run_id'],'033_OLD_FROZEN_QUEUE')
    validate_queue_033(queue,config)
    reference=payload['annotation-reference'][1];snapshot=payload['expected-snapshot'][1]
    receipts=[r for r in payload['receipts'][1]['receipts'] if r['alias']=='annotation']
    require(len(receipts)==3 and all(r['complete'] and r['byte_count']==snapshot['size']==reference['size']
            and r['digest']==snapshot['sha256'] and r['before'][:2]==reference['identity']
            and r['before'][3]==reference['mtime_ns'] for r in receipts)
            and snapshot['binding']==['SKIP_NONFINITE_028','PROJECTOR_028_V1'],'033_RAW_SNAPSHOT')
    require(candidate['alias']=='P2' and candidate['frames']=='P2-frames.npy' and candidate['demux_eof'] is True
            and candidate['corrupt']==candidate['missing']==0,'033_CANDIDATE_METADATA')


def transfer_cache_033(root, old_root):
    raise ContractError('OLD_033_TRANSFER_CLOSED')
    journal=Journal(root,create=True)
    try:
        journal.reserve_time('cpu',45,'cache-initialize');old=Path(old_root)
        require(old.name=='integration_032','033_EXACT_032_ARCHIVE')
        rows=archive_032_rows(journal.input('archive_032',old/'032-ledger.jsonl'))
        names=['keys','cohort','nongold','plan','receipts','targets','heads029','official',
               'annotation-reference','execution-config','runtime','worker-input','queue','expected-snapshot',
               'P2-head','P2-media-binding','P2-candidates','032-final-summary-private','gpu-resource-exit-private']
        payload={}
        for name in names:
            raw=journal.input('cache_'+name,old/(name+'.json'));payload[name]=(raw,json.loads(raw))
        validate_cache_032(rows,payload)
        for name in ('keys','cohort','nongold','plan','receipts','targets','heads029','official',
                     'annotation-reference','P2-head','P2-media-binding','P2-candidates'):
            journal.write(name+'.json',payload[name][1])
        completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'};outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
        for name in ('factory_0','factory_1','runner_0','runner_1'):
            raw=journal.input('cache_'+name,old/(name+'.py'),'source');prior=completed['cache_'+name]
            require(len(raw)==prior['size']==outputs[name+'.py']['size'] and hashlib.sha256(raw).hexdigest()==prior['sha256'],'033_SOURCE_BYTES')
            journal.reserve_output(name+'.py',len(raw))
            with open(Path(root)/(name+'.py'),'xb') as target:target.write(raw);target.flush();os.fsync(target.fileno())
        journal.write('execution-config.json',dict(payload['execution-config'][1],runtime=payload['runtime'][1]))
        journal.write('frozen-worker-032.json',payload['worker-input'][1])
        journal.write('frozen-snapshot-032.json',payload['expected-snapshot'][1])
        journal.write('frame-source-reference-private.json',dict(path=str(old/'P2-frames.npy'),
                     reserved_size=outputs['P2-frames.npy']['size']))
        journal.add('CACHE_BOUND',inputs=24,archive_hash=rows[-1]['hash'],frame_copy_required=True)
    finally:journal.close()


def verify_npy_033(path, candidate):
    """Bounded stdlib NPY validation, no NumPy import or media decoder."""
    import ast,math,struct
    require(candidate['frames']=='P2-frames.npy' and len(candidate['times'])==len(candidate['rgb_hashes'])==48
            and all(type(x) in (int,float) and math.isfinite(x) for x in candidate['times'])
            and all(b>a for a,b in zip(candidate['times'],candidate['times'][1:])),'033_FRAME_TIMES')
    with open(path,'rb') as source:
        prefix=source.read(8);require(prefix[:6]==b'\x93NUMPY' and prefix[6:] in (b'\x01\x00',b'\x02\x00',b'\x03\x00'),'033_NPY_MAGIC')
        width=2 if prefix[6]==1 else 4;raw=source.read(width)
        require(len(raw)==width,'033_NPY_LENGTH');length=int.from_bytes(raw,'little');require(0<length<=4096,'033_NPY_HEADER')
        header=source.read(length);require(len(header)==length,'033_NPY_HEADER')
        info=ast.literal_eval(header.decode('utf-8' if prefix[6]==3 else 'latin1'))
        shape=info.get('shape');require(info.get('descr')=='|u1' and info.get('fortran_order') is False
            and type(shape) is tuple and len(shape)==4 and shape[0]==48 and shape[-1]==3
            and all(type(x) is int and x>0 for x in shape),'033_NPY_SHAPE_DTYPE')
        require(math.prod(shape)==candidate['frame_bytes'] and path.stat().st_size==8+width+length+math.prod(shape),'033_NPY_SIZE')
        size=math.prod(shape[1:])
        for expected in candidate['rgb_hashes']:
            raw=source.read(size);require(len(raw)==size and hashlib.sha256(raw).hexdigest()==expected,'033_RGB_BINDING')
        require(source.read(1)==b'','033_NPY_TRAILING')
    return list(shape)


def copy_frames_034(root):
    import shutil
    journal=Journal(root)
    try:
        require_ready(journal);journal.once('PHASE','copy-frames')
        reference=load(root,'frame-source-reference-private.json');path,before=checked_path(reference['path'])
        require(path.name=='P2-frames.npy' and path.parent.name=='integration_033' and 0<before.st_size<=256*MIB
                and before.st_size==reference['size'],'034_FRAME_SIZE')
        require(shutil.disk_usage(root).free>=before.st_size+2*GIB,'034_FRAME_DISK')
        require(not any(r.get('category')=='frame-cache' for r in journal.events('INPUT')),'034_FRAME_ALREADY_OPENED')
        journal.once('INPUT','frame-cache',path=str(path),identity=[before.st_dev,before.st_ino],size=before.st_size,category='frame-cache')
        journal.reserve_output('P2-frames.npy',before.st_size,'frames');sha=hashlib.sha256();count=0
        with open(path,'rb') as source,open(Path(root)/'P2-frames.npy','xb') as target:
            opened=os.fstat(source.fileno());require(os.path.samestat(before,opened),'034_FRAME_IDENTITY')
            while count<before.st_size:
                raw=source.read(min(MIB,before.st_size-count));require(bool(raw),'034_FRAME_PARTIAL')
                target.write(raw);sha.update(raw);count+=len(raw)
            require(not source.read(1),'034_FRAME_OVERSIZE');after_fd=os.fstat(source.fileno());target.flush();os.fsync(target.fileno())
        stable=lambda a,b:(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns)
        require(stable(before,path.stat()) and stable(opened,after_fd) and count==before.st_size,'034_FRAME_CHANGED')
        require(sha.hexdigest()==reference['sha256'],'034_HISTORICAL_FRAME_SHA')
        journal.add('INPUT_COMPLETE',alias='frame-cache',size=count,sha256=sha.hexdigest())
        destination=Path(root)/'P2-frames.npy';shape=verify_npy_033(destination,load(root,'P2-candidates.json'))
        copied=hashlib.sha256()
        with open(destination,'rb') as source:
            for raw in iter(lambda:source.read(MIB),b''):copied.update(raw)
        require(copied.hexdigest()==sha.hexdigest(),'034_FRAME_COPY_HASH')
        journal.add('FRAME_CACHE_VERIFIED',size=count,shape=shape,sha256=sha.hexdigest(),rgb_hashes=48,
                    evidence='DIRECT_033_FILE_SHA_AND_RGB_HASHES')
    finally:journal.close()


def archive_033_rows(raw):
    """Closed033 has frame-copy/resource observations, not real model actions."""
    require(0<len(raw)<=2*MIB and raw.endswith(b'\n'),'ARCHIVE_033_INCOMPLETE')
    rows=[]
    for line in raw.splitlines():
        row=json.loads(line);signature=row.pop('hash')
        require(row['seq']==len(rows) and row['prev']==(rows[-1]['hash'] if rows else '0'*64)
                and digest(row)==signature,'ARCHIVE_033_CHAIN');rows.append(dict(row,hash=signature))
    require(rows[0].get('contract_id')=='033' and rows[0].get('root_name')=='integration_033'
            and rows[0].get('purpose')=='REAL_033' and rows[-1]['event']=='RUN_STOPPED','ARCHIVE_033_IDENTITY_STOP')
    events=lambda name:[r for r in rows if r['event']==name]
    forbidden=('HTTPS','TRANSPORT_SEND','BODY_DEBIT','MEDIA_COMPLETE','STARTED','MODEL_LAUNCH',
               'WORKER_FREE_RECHECK','RESOURCE_ADMITTED','SCORE_CONSUMED','SCORED')
    require(not any(r['event'] in forbidden or r['event']=='INPUT' and r.get('category')=='gold' for r in rows),'ARCHIVE_033_REAL_ACTION')
    suites=events('SUITE_RESULT');terminal=events('TERMINAL')
    require(len(suites)==2 and {r['name'] for r in suites}=={'suite-1','suite-2'}
            and all(r.get('contract_id')=='033' and r.get('run_id')==rows[0]['run_id'] and r.get('passed') is True
                    and r.get('expected')==r.get('loaded')==r.get('tests')==6
                    and r.get('failures')==r.get('errors')==r.get('skips')==0 for r in suites),'ARCHIVE_033_SUITES')
    require(len(terminal)==16 and {r['key'] for r in terminal}=={str(n) for n in range(16)}
            and all(r['state']=='NOT_RUN' for r in terminal),'ARCHIVE_033_TERMINALS')
    verified=events('FRAME_CACHE_VERIFIED');completed=[r for r in events('INPUT_COMPLETE') if r['alias']=='frame-cache']
    inputs=[r for r in events('INPUT') if r.get('category')=='frame-cache'];outputs=[r for r in events('OUTPUT') if r['key']=='P2-frames.npy']
    require(len(verified)==len(completed)==len(inputs)==len(outputs)==1 and verified[0]['rgb_hashes']==48
            and verified[0]['size']==completed[0]['size']==inputs[0]['size']==outputs[0]['size']
            and verified[0]['sha256']==completed[0]['sha256'],'ARCHIVE_033_FRAME_CHAIN')
    queries=events('GPU_QUERY');require(len(queries)==2 and {r['key'] for r in queries}=={'0','1'},'ARCHIVE_033_QUERIES')
    exits={r['name']:r for r in events('PHASE_EXIT')}
    require(exits['gpu-resource']['code']==1 and all(r['job_active']==0 for r in exits.values())
            and all(exits[name]['code']==0 for name in ('copy-frames','prepare','refusal-0','refusal-1')),'ARCHIVE_033_EXITS')
    return rows


def identity_from_033(observations):
    """Identity evidence only; never retroactively admit the old resource run."""
    import xml.etree.ElementTree as ET
    require(len(observations['xml'])==len(observations['starts'])==2 and
            observations['starts'][1]-observations['starts'][0]>=1,'034_OLD_TWO_IDENTITIES')
    identities=[]
    for raw in observations['xml']:
        require(type(raw) is str and len(raw.encode())<=65536,'034_OLD_XML_BOUND')
        gpus=ET.fromstring(raw).findall('gpu');require(len(gpus)==1,'034_OLD_ONE_DEVICE')
        gpu=gpus[0];require('3090' in gpu.findtext('product_name','') and gpu.findtext('uuid') and gpu.get('id'),'034_OLD_IDENTITY')
        identities.append(dict(query_device=0,uuid=gpu.findtext('uuid'),bus=gpu.get('id')))
    require(identities[0]==identities[1],'034_OLD_DEVICE_CHANGED')
    return identities[0]


def validate_cache_033(rows,payload):
    completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'}
    outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
    direct={name:'cache_'+name for name in ('keys','cohort','nongold','plan','receipts','targets','heads029','official',
            'annotation-reference','P2-head','P2-media-binding','P2-candidates')}
    direct.update({'frozen-worker-032':'cache_worker-input','frozen-snapshot-032':'cache_expected-snapshot'})
    for name,alias in direct.items():
        raw=payload[name][0];old=completed[alias]
        require(len(raw)==old['size']==outputs[name+'.json']['size'] and hashlib.sha256(raw).hexdigest()==old['sha256'],'034_CACHE_DIRECT_BYTES')
    for name,(raw,value) in payload.items():
        require(len(raw)==outputs[name+'.json']['size'],'034_RETAINED_OUTPUT_SIZE')
    plan=payload['plan'][1]['plan'];config=payload['worker-input'][1];queue=payload['queue'][1]
    frozen=[r for r in rows if r['event']=='FROZEN']
    require(len(frozen)==1 and frozen[0]['plan_hash']==queue['plan_hash']==digest(plan)
            and frozen[0]['worker_hash']==queue['worker_hash']==digest(config)
            and config==payload['frozen-worker-032'][1] and queue['contract_id']=='033' and queue['run_id']==rows[0]['run_id'],
            '034_FROZEN_SCIENCE_QUEUE')
    validate_queue_034(queue,config)
    snapshot=payload['expected-snapshot'][1];reference=payload['annotation-reference'][1]
    require(snapshot==payload['frozen-snapshot-032'][1] and snapshot['binding']==['SKIP_NONFINITE_028','PROJECTOR_028_V1'],'034_SNAPSHOT_PROFILE')
    receipts=[r for r in payload['receipts'][1]['receipts'] if r['alias']=='annotation']
    require(len(receipts)==3 and all(r['complete'] and r['byte_count']==snapshot['size']==reference['size']
            and r['digest']==snapshot['sha256'] and r['before'][:2]==reference['identity'] and r['before'][3]==reference['mtime_ns']
            for r in receipts),'034_FULL_RAW_RECEIPTS')
    targets=payload['targets'][1]['targets'];require([t['alias'] for t in targets]==['P1','P2','P3','P4'],'034_TARGET_ORDER')
    head=payload['P2-head'][1];media=payload['P2-media-binding'][1];candidate=payload['P2-candidates'][1]
    require(head['alias']==media['alias']==candidate['alias']=='P2' and head['eligible'] is True and head['status']==200
            and media['uri']==targets[1]['uri'] and media['size']==media['received']==head['ContentLength']
            and all(media[k]==head[k] for k in ('ETag','VersionId','ContentLength'))
            and candidate['demux_eof'] is True and candidate['corrupt']==candidate['missing']==0
            and candidate['frames']=='P2-frames.npy','034_P2_BINDING')
    return identity_from_033(payload['gpu-samples-private'][1])


def transfer_cache_034(root,old_root):
    journal=Journal(root,create=True)
    try:
        journal.reserve_time('cpu',45,'cache-initialize');old=Path(old_root)
        require(old.name=='integration_033','034_EXACT_033_ARCHIVE')
        rows=archive_033_rows(journal.input('archive_033',old/'033-ledger.jsonl'))
        names=['keys','cohort','nongold','plan','receipts','targets','heads029','official','annotation-reference',
               'execution-config','runtime','worker-input','queue','expected-snapshot','P2-head','P2-media-binding','P2-candidates',
               '033-final-summary-private','gpu-samples-private','frozen-worker-032','frozen-snapshot-032']
        payload={}
        for name in names:
            raw=journal.input('cache_'+name,old/(name+'.json'));payload[name]=(raw,json.loads(raw))
        identity=validate_cache_033(rows,payload)
        for name in ('keys','cohort','nongold','plan','receipts','targets','heads029','official','annotation-reference',
                     'P2-head','P2-media-binding','P2-candidates','frozen-worker-032','frozen-snapshot-032'):
            journal.write(name+'.json',payload[name][1])
        completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'};outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
        for name in ('factory_0','factory_1','runner_0','runner_1'):
            raw=journal.input('cache_'+name,old/(name+'.py'),'source');prior=completed['cache_'+name]
            require(len(raw)==prior['size']==outputs[name+'.py']['size'] and hashlib.sha256(raw).hexdigest()==prior['sha256'],'034_SOURCE_BYTES')
            journal.reserve_output(name+'.py',len(raw))
            with open(Path(root)/(name+'.py'),'xb') as destination:destination.write(raw);destination.flush();os.fsync(destination.fileno())
        journal.write('execution-config.json',dict(payload['execution-config'][1],runtime=payload['runtime'][1]))
        journal.write('device-identity-reference.json',identity)
        frame=completed['frame-cache']
        journal.write('frame-source-reference-private.json',dict(path=str(old/'P2-frames.npy'),size=frame['size'],sha256=frame['sha256']))
        journal.add('CACHE_BOUND',inputs=26,archive_hash=rows[-1]['hash'],frame_copy_required=True)
    finally:journal.close()


def recover_pretty_input(alias, data, context):
    """Reverse only the published028/029 pretty-JSON writer ordering.

    030 reserialized JSON into sorted compact form. Acceptance still requires
    EXACT original INPUT_COMPLETE SHA256 and size, then the known030 transform
    must reproduce every cache byte. Canonical equivalence alone never passes.
    No original source is reopened; no semantic field/array order is changed.
    """
    import itertools
    headers=context.get('official',{}).get('joined',{}).get('summary',{}).get('headers',[])
    roots=dict(keys=['binding','keys'],cohort=['binding','cohort','exclusions','source_conflicts'],
               nongold=['binding','projection'],plan=['binding','plan'],receipts=['binding','receipts','diagnostics'],
               targets=['targets','evidence','errors'],heads029=['results'],official=['binding','joined','qualification'])
    diagnostic_order=['old_%d' % i for i in range(6)]+['handoff_0','index','screen','inference']
    metadata_order={s['source']:[pair[0] for pair in s['metadata']] for s in context.get('nongold',{}).get('projection',{}).get('sources',[])}
    def reorder(value,path=()):
        if isinstance(value,list):return [reorder(v,path+(i,)) for i,v in enumerate(value)]
        if not isinstance(value,dict):return value
        order=[]
        keys=set(value)
        if not path:order=roots.get(alias,[])
        elif path==('diagnostics',):order=diagnostic_order
        elif 'byte_count' in keys and 'digest' in keys:order=['alias','byte_count','digest','before','after','complete']
        elif 'skipped_nonfinite' in keys:order=['binding','complete','skipped_nonfinite','decoded_values','character_position']
        elif keys=={'source','index'}:order=['source','index']
        elif keys=={'key','arm'}:order=['key','arm']
        elif 'decomposition' in keys:order=['key','task','question','decomposition']
        elif 'event_a' in keys and 'key' in keys:order=['key','task','question','event_a','event_b','metadata','limits']
        elif 'event_a' in keys:order=['status','reason','event_a','event_b']
        elif 'options' in keys:order=['key','task','question','options']
        elif keys=={'source','metadata'}:order=['source','metadata']
        elif 'calls' in keys:order=['sources','questions','exclusions','calls']
        elif 'view' in keys:order=['view','sources','questions']
        elif keys=={'key','reason'}:order=['key','reason']
        elif path==('joined',):order=['rows','group_matches','summary','duplicates']
        elif path==('joined','summary'):order=['row_count','headers','requested_uids','matched_uids','missing_uids','duplicate_uids','requested_groups','matched_groups']
        elif len(path)==3 and path[:2]==('joined','rows'):order=headers
        elif len(path)==3 and path[0]=='cohort' and path[-1]=='metadata':
            uid=data['cohort'][path[1]]['key']['source'];order=metadata_order.get(uid,[])+[h for h in headers if h not in metadata_order.get(uid,[])]
        elif 'current_rights' in keys and 'source_status' in keys:order=['alias','source_status','reasons','current_rights','physical_independence']
        elif path and path[0]=='targets':order=['alias','uri','bucket','key']
        elif path and path[0]=='results':order=['alias','status','ContentLength','ETag','VersionId','LastModified','region','reason','exception_kind']
        ordered=list(dict.fromkeys([k for k in order if k in value]+list(value)))
        return {k:reorder(value[k],path+(k,)) for k in ordered}
    ordered=reorder(data)
    variants=[ordered]
    if alias=='official':
        # Manifest row order was preserved by the original writer, but sorted by
        # 030's transform. Four fixed rows permit a bounded24 serialization proof.
        rows=ordered['joined']['rows']
        require(len(rows)==4,'ARCHIVE_OFFICIAL_FOUR')
        variants=[]
        for order in itertools.permutations(rows):
            variant=dict(ordered);variant['joined']=dict(ordered['joined'],rows={k:rows[k] for k in order});variants.append(variant)
    for value in variants:
        yield json.dumps(value,ensure_ascii=True,indent=2,allow_nan=False).encode()


def transfer_cache_031(root, old_root, sdk_python, conda_entry=None, runtime=None):
    """Fresh031 budget, exact read-only030 cache with byte-level provenance."""
    raise ContractError('OLD_031_TRANSFER_CLOSED')
    journal=Journal(root,create=True)
    try:
        journal.reserve_time('cpu',45,'cache-initialize')
        old=Path(old_root);require(old.name=='integration_030','EXACT_ARCHIVE_ROOT')
        rows=archive_rows(journal.input('archive_030',old/'030-ledger.jsonl'))
        completed={r['alias']:r for r in rows if r['event']=='INPUT_COMPLETE'}
        outputs={r['key']:r for r in rows if r['event']=='OUTPUT'}
        names=['keys','cohort','nongold','plan','receipts','targets','heads029','official']
        payload={};raws={};checks=[]
        for alias in names:
            raw=journal.input('cache_'+alias,old/(alias+'.json'));raws[alias]=raw;payload[alias]=json.loads(raw)
        for alias in names:
            raw=raws[alias];expected=completed[alias]
            require(alias+'.json' in outputs and len(raw)==outputs[alias+'.json']['size'],'CACHE_OUTPUT_SIZE')
            exact=hashlib.sha256(raw).hexdigest()==expected['sha256'] and len(raw)==expected['size']
            restored=None
            if not exact:
                require(packed(payload[alias])==raw,'CACHE_NOT_PUBLISHED_CANONICAL_FORM')
                for candidate in recover_pretty_input(alias,payload[alias],payload):
                    if len(candidate)==expected['size'] and hashlib.sha256(candidate).hexdigest()==expected['sha256']:
                        restored=candidate;break
            checks.append(dict(alias=alias,bound=exact or restored is not None,
                               mode='EXACT_CACHE_BYTES' if exact else 'EXACT_ORIGINAL_BYTES_RECOVERED' if restored is not None else 'UNBOUND_CANONICAL_REWRITE'))
            if exact or restored is not None:
                journal.write(alias+'.json',payload[alias])
        for alias in ('factory_0','factory_1','runner_0','runner_1'):
            raw=journal.input('cache_'+alias,old/(alias+'.py'),'source');expected=completed[alias]
            good=len(raw)==expected['size'] and hashlib.sha256(raw).hexdigest()==expected['sha256']
            checks.append(dict(alias=alias,bound=good,mode='EXACT_CACHE_BYTES' if good else 'SOURCE_HASH_HOLD'))
            if good:
                journal.reserve_output(alias+'.py',len(raw))
                with open(journal.root/(alias+'.py'),'xb') as target:
                    target.write(raw);target.flush();os.fsync(target.fileno())
        reference=json.loads(journal.input('cache_annotation_reference',old/'annotation-reference.json'))
        # This file was created inside030; bind its identity to three exact028
        # full receipts, rather than pretending it was an original INPUT_COMPLETE.
        receipts=[r for r in payload['receipts']['receipts'] if r['alias']=='annotation']
        require(len(receipts)==3 and all(r['complete'] for r in receipts)
                and len({(r['byte_count'],r['digest'],tuple(r['before'])) for r in receipts})==1
                and reference['identity']==receipts[0]['before'][:2] and reference['size']==receipts[0]['byte_count']
                and reference['mtime_ns']==receipts[0]['before'][3],'CACHE_ANNOTATION_REFERENCE')
        journal.write('annotation-reference.json',reference)
        journal.write('cache-verification-private.json',dict(checks=checks,archive_stopped=True,old_actions_zero=True,old_run_id=rows[0]['run_id']))
        journal.write('execution-config.json',dict(sdk_python=str(sdk_python),conda_entry=str(conda_entry) if conda_entry else None,runtime=runtime))
        if all(r['bound'] for r in checks):
            journal.add('CACHE_BOUND',inputs=12,archive_hash=rows[-1]['hash'])
        else:
            journal.add('CACHE_HOLD',reason='ORIGINAL_INPUT_DIGEST_NOT_RECOVERED',aliases=[r['alias'] for r in checks if not r['bound']])
    finally:
        journal.close()


def win32_file_api():
    require(os.name == 'nt', 'WINDOWS_REQUIRED')
    api = ctypes.WinDLL('kernel32', use_last_error=True)
    api.CreateFileW.argtypes = [W.LPCWSTR, W.DWORD, W.DWORD, W.LPVOID, W.DWORD, W.DWORD, W.HANDLE]
    api.CreateFileW.restype = W.HANDLE
    api.CloseHandle.argtypes = [W.HANDLE]; api.CloseHandle.restype = W.BOOL
    api.GetHandleInformation.argtypes = [W.HANDLE, ctypes.POINTER(W.DWORD)]
    api.GetHandleInformation.restype = W.BOOL
    return api


class ExclusiveRead:
    def __init__(self, path):
        self.api = win32_file_api(); self.handle = None
        handle = self.api.CreateFileW(str(path), 0x80000000, 0, None, 3, 0x80, None)
        error = ctypes.get_last_error()  # Immediate raw Win32 observation.
        require(handle != ctypes.c_void_p(-1).value, 'EXCLUSIVE_HANDLE_FAILED_%d' % error)
        self.handle = handle
        try:
            flags = W.DWORD()
            require(self.api.GetHandleInformation(W.HANDLE(handle), ctypes.byref(flags)) and not flags.value & 1, 'HANDLE_INHERITANCE')
        except BaseException:
            self.close(); raise

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle); self.handle = None


def zero_body_observation(path):
    """Same production and witness probe: one native + one Python open, no read."""
    api = win32_file_api()
    ctypes.set_last_error(0)
    handle = api.CreateFileW(str(path), 0x80000000, 7, None, 3, 0x80, None)
    error = ctypes.get_last_error()
    opened = handle != ctypes.c_void_p(-1).value
    if opened:
        api.CloseHandle(handle)
    native = dict(opened=opened, winerror=None if opened else error, body_bytes=0)
    try:
        source = open(path, 'rb'); source.close()
        python = dict(opened=True, exception_kind=None, errno=None, winerror=None, body_bytes=0)
    except OSError as failure:
        python = dict(opened=False, exception_kind=type(failure).__name__, errno=failure.errno,
                      winerror=getattr(failure, 'winerror', None), body_bytes=0)
    return dict(native=native, python=python,
                denied=not opened and error == 32 and python['opened'] is False)


class _Basic(ctypes.Structure):
    _fields_ = [('per_process_time', ctypes.c_int64), ('per_job_time', ctypes.c_int64),
                ('flags', W.DWORD), ('min_ws', ctypes.c_size_t), ('max_ws', ctypes.c_size_t),
                ('active_limit', W.DWORD), ('affinity', ctypes.c_size_t), ('priority', W.DWORD), ('scheduling', W.DWORD)]


class _IO(ctypes.Structure):
    _fields_ = [(n, ctypes.c_uint64) for n in ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]


class _Extended(ctypes.Structure):
    _fields_ = [('basic', _Basic), ('io', _IO), ('process_memory', ctypes.c_size_t),
                ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t), ('peak_job', ctypes.c_size_t)]


class _Accounting(ctypes.Structure):
    _fields_ = [('user', ctypes.c_int64), ('kernel', ctypes.c_int64), ('period_user', ctypes.c_int64),
                ('period_kernel', ctypes.c_int64), ('faults', W.DWORD), ('total', W.DWORD), ('active', W.DWORD), ('terminated', W.DWORD)]


class Job:
    def __init__(self, memory=24 * GIB):
        require(os.name == 'nt', 'WINDOWS_REQUIRED')
        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [W.LPVOID, W.LPCWSTR]; self.api.CreateJobObjectW.restype = W.HANDLE
        for name, args in (('SetInformationJobObject', [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD]),
                           ('QueryInformationJobObject', [W.HANDLE, ctypes.c_int, W.LPVOID, W.DWORD, W.LPVOID]),
                           ('AssignProcessToJobObject', [W.HANDLE, W.HANDLE]),
                           ('TerminateJobObject', [W.HANDLE, W.UINT]), ('CloseHandle', [W.HANDLE])):
            getattr(self.api, name).argtypes = args
        self.handle = self.api.CreateJobObjectW(None, None)
        require(bool(self.handle), 'JOB_CREATE')
        limits = _Extended()
        limits.basic.flags = 0x2000 | 0x100 | 0x200  # kill-on-close, process and Job memory.
        limits.process_memory = limits.job_memory = memory
        require(self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)), 'JOB_MEMORY_LIMIT')

    def assign(self, child):
        require(self.api.AssignProcessToJobObject(self.handle, W.HANDLE(int(child._handle))), 'JOB_ASSIGN')

    def active(self):
        record = _Accounting()
        require(self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(record), ctypes.sizeof(record), None), 'JOB_ACCOUNTING')
        return record.active

    def wait_empty(self, deadline):
        """Only an actual observed zero certifies exit; never kills a healthy peer."""
        while True:
            active = self.active()
            if active == 0:
                return True
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return False
            time.sleep(min(.01, remaining))

    def peak(self):
        record = _Extended()
        require(self.api.QueryInformationJobObject(self.handle, 9, ctypes.byref(record), ctypes.sizeof(record), None), 'JOB_PEAK')
        return record.peak_job

    def kill(self):
        self.api.TerminateJobObject(self.handle, 99)

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle); self.handle = None


def run_child(command, seconds, *, job_memory=24 * GIB, payload='', environment=None, work_seconds=None):
    """Child MUST read one stdin line before work. Job assignment precedes it."""
    job = Job(job_memory)
    child = None
    buffers = [bytearray(), bytearray()]
    overflow = threading.Event()
    threads = []
    start = time.monotonic()
    deadline = start + seconds
    cleanup = min(5., seconds * .45)
    work_deadline = min(start + work_seconds, deadline-cleanup) if work_seconds is not None else deadline-cleanup
    killed = False
    try:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 env=environment, creationflags=0x08000000, close_fds=True)
        job.assign(child)
        def capture(stream, buffer):
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                if len(buffer) + len(chunk) > 65536:
                    overflow.set()
                buffer.extend(chunk[:max(0, 65536 - len(buffer))])
        for stream, buffer in zip((child.stdout, child.stderr), buffers):
            thread = threading.Thread(target=capture, args=(stream, buffer), daemon=True)
            thread.start(); threads.append(thread)
        child.stdin.write((payload + '\n').encode()); child.stdin.flush(); child.stdin.close()
        while child.poll() is None:
            if time.monotonic() >= work_deadline or overflow.is_set():
                job.kill(); killed = True; break
            time.sleep(min(.02, max(0, work_deadline-time.monotonic())))
        child.wait(timeout=max(.001, deadline-time.monotonic()))
        # Includes descendants. Never search for or kill a peer process.
        # First allow natural accounting drain; if a descendant remains, only
        # our Job is terminated and its zero must still be observed in-window.
        natural_deadline = min(deadline-.2, time.monotonic()+min(.4, cleanup/3))
        empty = job.wait_empty(natural_deadline)
        if not empty:
            job.kill(); killed = True
            empty = job.wait_empty(deadline-.1)
        require(empty, 'JOB_STILL_ACTIVE')
        for thread in threads:
            thread.join(max(0,deadline-time.monotonic()))
        require(not any(t.is_alive() for t in threads), 'PIPE_NOT_CLOSED')
        require(time.monotonic() <= deadline, 'FULL_CHILD_WINDOW_EXCEEDED')
        return dict(pid=child.pid, exit_code=child.returncode, job_active=0, peak_commit=job.peak(),
                    seconds=time.monotonic() - start, overflow=overflow.is_set(), killed=killed,
                    stdout=bytes(buffers[0]).decode(errors='replace'), stderr=bytes(buffers[1]).decode(errors='replace'))
    finally:
        if child is not None and child.poll() is None:
            job.kill(); child.kill()
            try:
                child.wait(timeout=max(.001, deadline-time.monotonic()))
            except subprocess.TimeoutExpired:
                pass  # No exit receipt; the retained Job is killed on close.
        if child is not None:
            for stream in (child.stdin, child.stdout, child.stderr):
                if stream is not None and not stream.closed:
                    stream.close()
        job.close()


def python_command(interpreter, module, *arguments, site=None):
    # Explicit source insertion is needed because -I ignores PYTHONPATH.
    code = 'import sys;sys.path.insert(0,sys.argv.pop(1));'
    if site:
        code += 'sys.path.insert(0,sys.argv.pop(1));'
    code += 'import runpy;runpy.run_module(sys.argv.pop(1),run_name="__main__",alter_sys=True)'
    return [str(interpreter), '-I', '-S', '-B', '-c', code, str(Path(__file__).parent)] + ([str(site)] if site else []) + [module] + list(arguments)


def initialize(root, entries, annotation):
    raise ContractError('LEGACY_INITIALIZE_CLOSED_USE_031_ARCHIVE_TRANSFER')
    # Historical implementation retained for code provenance, never executed.
    journal = Journal(root, create=True)
    try:
        journal.reserve_time('cpu', 120, 'initialize')
        # Exact entries supplied by trusted local handoff, not discovered.
        for alias, record in entries.items():
            raw = journal.input(alias, record['path'], record['category'])
            if record['category'] == 'source':
                journal.reserve_output(alias + '.py', len(raw))
                with open(journal.root / (alias + '.py'), 'xb') as target:
                    target.write(raw); target.flush(); os.fsync(target.fileno())
            else:
                journal.write(alias + '.json', json.loads(raw))
        _, stat = checked_path(annotation)
        journal.write('annotation-reference.json', dict(path=str(annotation), identity=[stat.st_dev, stat.st_ino],
                                                        size=stat.st_size, mtime_ns=stat.st_mtime_ns))
        journal.add('INITIALIZED', handoffs=len(entries), annotation_body=0)
    finally:
        journal.close()


def probe(path):
    # This process never calls read(), even on an unexpected successful open.
    sys.stdin.readline()
    print(json.dumps(zero_body_observation(path)))


def restored_plan(root):
    from temporal_evidence_adapter_025 import Projection, SourceRecord, QuestionRecord, QuestionKey, build_plan
    raw = load(root, 'nongold.json')['projection']
    projection = Projection(raw['view'], tuple(SourceRecord(s['source'], tuple(tuple(v) for v in s['metadata'])) for s in raw['sources']),
                            tuple(QuestionRecord(QuestionKey(**q['key']), q['task'], q['question'], tuple(q['options'])) for q in raw['questions']))
    return build_plan(projection)


def prepare(root):
    import ast
    import shutil
    journal = Journal(root)
    try:
        require_ready(journal)
        require(journal.events('CACHE_BOUND'),'CACHE_BINDING_REQUIRED')
        journal.once('PHASE', 'prepare')
        binding = ['SKIP_NONFINITE_028', 'PROJECTOR_028_V1']
        for name in ('keys', 'cohort', 'nongold', 'plan', 'receipts', 'official'):
            require(load(root, name + '.json')['binding'] == binding, 'PROFILE_BINDING')
        plan = restored_plan(root)
        require(len(plan.questions) == 4 and len(plan.calls) == 16 and packed(asdict(plan)) == packed(load(root, 'plan.json')['plan']), 'FROZEN_PLAN_CHANGED')
        # asdict retains tuples, JSON has lists: canonical bytes normalize both.
        keys = [asdict(q.key) for q in plan.questions]
        require(keys == load(root, 'keys.json')['keys'], 'FOUR_KEYS_CHANGED')
        cohort = load(root, 'cohort.json')['cohort']
        nongold = load(root, 'nongold.json')['projection']['questions']
        require([q['key'] for q in cohort] == keys and [q['key'] for q in nongold] == keys
                and all(len(q['options']) == 5 and all(type(v) is str and v.strip() for v in q['options']) for q in nongold), 'COHORT_OPTIONS')
        receipts = [r for r in load(root, 'receipts.json')['receipts'] if r['alias'] == 'annotation']
        require(len(receipts) == 3 and all(r['complete'] for r in receipts)
                and len({(r['byte_count'], r['digest'], tuple(r['before'])) for r in receipts}) == 1, '028_FULL_SNAPSHOT')
        reference = load(root, 'annotation-reference.json'); _, stat = checked_path(reference['path'])
        old = receipts[0]
        require([stat.st_dev, stat.st_ino] == old['before'][:2] == reference['identity']
                and stat.st_size == old['byte_count'] == reference['size']
                and stat.st_mtime_ns == old['before'][3] == reference['mtime_ns'], 'ANNOTATION_SNAPSHOT_STAT')
        journal.write('expected-snapshot.json', dict(binding=binding, size=old['byte_count'], sha256=old['digest']))
        targets = load(root, 'targets.json')['targets']; official = load(root, 'official.json')['joined']['rows']
        require([x['alias'] for x in targets] == ['P1', 'P2', 'P3', 'P4'], 'TARGET_ALIASES')
        sources = []
        for i, (question, item, target) in enumerate(zip(plan.questions, nongold, targets)):
            row = official[question.key.source]
            metadata = dict(plan.sources[i].metadata)
            require(row['video_uid'] == question.key.source and row['canonical_s3_location'] == target['uri']
                    and row['release_1'] in ('True', True, 'true') and row['canonical_is_validated'] in ('True', True, 'true'), 'OFFICIAL_FIXED_SOURCE')
            duration = float(row['canonical_mp4_duration_sec'])
            require(abs(duration - float(metadata['duration_in_seconds'])) <= .01
                    and item['question'] == cohort[i]['question'] == question.question
                    and question.decomposition.event_a == cohort[i]['event_a']
                    and question.decomposition.event_b == cohort[i]['event_b'], 'SOURCE_OR_EVENT_BINDING')
            sources.append(dict(alias=target['alias'], question=item['question'], options=item['options'],
                                event_a=cohort[i]['event_a'], event_b=cohort[i]['event_b'], declared_duration=duration))
        systems = []; model_roots = []
        for number in range(2):
            source = (Path(root) / ('runner_%d.py' % number)).read_text(encoding='utf-8')
            tree = ast.parse(source)
            system = [node.value.value for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == 'system' for t in node.targets)
                      and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)]
            require(len(system) == 1, 'ORIGINAL_SYSTEM_PROMPT')
            systems.append(system[0])
            constants = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and type(node.value) is str}
            roots = []
            for class_name in ('Qwen3VLForConditionalGeneration', 'SiglipModel'):
                calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                         and n.func.attr == 'from_pretrained' and isinstance(n.func.value, ast.Name) and n.func.value.id == class_name]
                require(len(calls) == 1 and isinstance(calls[0].args[0], ast.Constant), 'ORIGINAL_MODEL_REFERENCE')
                roots.append(calls[0].args[0].value)
            model_roots.append(roots)
        require(systems[0] == systems[1] and model_roots[0] == model_roots[1], 'BACKEND_CONFIG_CONFLICT')
        for number in range(2):
            factory = ast.parse((Path(root) / ('factory_%d.py' % number)).read_text(encoding='utf-8'))
            helper = [n for n in ast.walk(factory) if isinstance(n, ast.FunctionDef) and n.name == 'inputs']
            runner = ast.parse((Path(root) / ('runner_%d.py' % number)).read_text(encoding='utf-8'))
            original = [n for n in ast.walk(runner) if isinstance(n, ast.FunctionDef) and n.name == 'inputs']
            require(len(helper) == len(original) == 1 and ast.dump(helper[0]) == ast.dump(original[0]), 'EXACT_HELPER_AST')
        configs = []
        for name, model in zip(('qwen_config', 'siglip_config'), model_roots[0]):
            configs.append(json.loads(journal.input(name, Path(model) / 'config.json', 'config')))
        require(configs[0]['model_type'] == 'qwen3_vl' and configs[1]['model_type'] == 'siglip', 'MODEL_CONFIG')
        slots = [dict(slot=n, alias='P%d' % (n // 4 + 1), arm=call.arm) for n, call in enumerate(plan.calls)]
        journal.write('worker-input.json', dict(binding=binding, sources=sources, slots=slots, system=systems[0],
                      models=model_roots[0], qwen_config=configs[0], seed=19, max_new_tokens=64, factory='factory_1.py'))
        require(load(root,'worker-input.json')==load(root,'frozen-worker-032.json'),'033_SCIENTIFIC_CONFIG_CHANGED')
        require(load(root,'expected-snapshot.json')==load(root,'frozen-snapshot-032.json'),'033_SNAPSHOT_CHANGED')
        journal.add('FROZEN', n=4, options=20, slots=16, plan_hash=digest(asdict(plan)), worker_hash=digest(load(root, 'worker-input.json')))
        # Resolve the explicitly existing named conda runtime, no inventory/import.
        execution=load(root,'execution-config.json')
        runtime=execution.get('runtime')
        resolution_pid=None
        if runtime is None:
            conda=Path(execution['conda_entry'])
            checked_path(conda)
            journal.reserve_time('cpu',20,'runtime-resolution')
            code = 'import sys,os,json;sys.stdin.readline();print(json.dumps(dict(python=sys.executable,path=os.environ.get("PATH",""))))'
            result = run_child([str(conda), 'run', '--no-capture-output', '-n', 'pytorch', 'python', '-I', '-S', '-B', '-c', code],20)
            require(result['exit_code'] == 0 and not result['overflow'], 'EXISTING_RUNTIME_RESOLUTION')
            runtime = json.loads(result['stdout'].strip());resolution_pid=result['pid']
        runtime['site'] = str(Path(runtime['python']).parent / 'Lib' / 'site-packages')
        journal.write('runtime.json', runtime)
        journal.add('PREPARED', helper_ast_matches=2, original_annotation_body=0, resolution_pid=resolution_pid)
    finally:
        journal.close()


def phase(root, name, stage, seconds, command, environment=None):
    journal = Journal(root)
    try:
        if name.startswith('suite-'):
            require(name in ('suite-1', 'suite-2') and seconds<=60 and not journal.events('RUN_STOPPED'), 'SUITE_CAP_OR_STOP')
        journal.reserve_time(stage, seconds, name)
    finally:
        journal.close()
    result = run_child(command, seconds, environment=environment)
    journal = Journal(root)
    try:
        journal.write(name + '-exit-private.json', result)
        journal.add('PHASE_EXIT', name=name, pid=result['pid'], code=result['exit_code'], job_active=result['job_active'], seconds=result['seconds'])
        if name.startswith('suite-'):
            receipt=load(root,name+'-result.json') if (Path(root)/(name+'-result.json')).exists() else {}
            marks=receipt.get('os_marks',{})
            passed=(result['exit_code']==0 and not result['overflow'] and receipt.get('contract_id')=='034'
                    and receipt.get('run_id')==journal.rows[0]['run_id'] and receipt.get('expected')==receipt.get('loaded')==receipt.get('tests')==4
                    and receipt.get('failures')==receipt.get('errors')==receipt.get('skips')==0
                    and all(marks.get(k) is True for k in ('shared_resource','archive_033','bindings_034','no_network')))
            journal.add('SUITE_RESULT', name=name, contract_id='034',run_id=journal.rows[0]['run_id'],passed=passed,
                        expected=receipt.get('expected'),loaded=receipt.get('loaded'),tests=receipt.get('tests',0),failures=receipt.get('failures'),errors=receipt.get('errors'),skips=receipt.get('skips'),os_marks=marks)
    finally:
        journal.close()
    return result


def require_ready(journal):
    results = journal.events('SUITE_RESULT')
    require(journal.rows[0].get('purpose')=='REAL_034' and not journal.events('RUN_STOPPED') and results and results[-1]['passed'] is True
            and results[-1].get('contract_id')=='034' and results[-1].get('run_id')==journal.rows[0]['run_id']
            and 0 < results[-1]['tests'] and len(results) <= 2, 'NEW_SUITE_NOT_PASSED')


def make_queue(root, journal, available):
    config=load(root,'worker-input.json'); plan=restored_plan(root)
    validate_queue_034(dict(slots=config['slots'],available=available),config)
    require(len(config['slots'])==16 and len(plan.calls)==16,'FULL_QUEUE_REQUIRED')
    queue=dict(contract_id='034',run_id=journal.rows[0]['run_id'],plan_hash=digest(asdict(plan)),
               worker_hash=digest(config),slots=config['slots'],available=available)
    journal.write('queue.json',queue)
    return queue


def close_model_queue(root, journal, child_exit):
    require(child_exit['job_active']==0 and type(child_exit['pid']) is int and child_exit['pid']>0,'REAL_JOB_EXIT_REQUIRED')
    launches=journal.events('MODEL_LAUNCH');require(len(launches)==1,'UNIQUE_MODEL_LAUNCH')
    launch=launches[0];queue=load(root,'queue.json')
    journal.add('MODEL_EXIT',pid=child_exit['pid'],job_active=child_exit['job_active'],code=child_exit['exit_code'],
                run_id=journal.rows[0]['run_id'],launch_hash=launch['hash'],queue_hash=digest(queue),
                exit_binding=digest(child_exit),seconds=child_exit['seconds'])
    journal.add('QUEUE_CLOSED',pid=child_exit['pid'],run_id=journal.rows[0]['run_id'],
                model_exit_hash=journal.events('MODEL_EXIT')[0]['hash'],terminal_hash=digest(journal.events('TERMINAL')),
                queue_hash=digest(queue),plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash'])


def score_allowed(rows, root):
    closes = [r for r in rows if r['event'] == 'QUEUE_CLOSED']
    exits = [r for r in rows if r['event'] == 'MODEL_EXIT']
    require(len(closes) == len(exits) == 1 and exits[0]['job_active'] == 0
            and exits[0]['pid'] == closes[0]['pid'] and closes[0]['model_exit_hash'] == exits[0]['hash']
            and len([r for r in rows if r['event'] == 'TERMINAL']) == 16
            and any(r['event'] == 'TERMINAL' and r['state'] in ('RETURNED', 'INVALID') for r in rows), 'GOLD_GATE_CLOSED')
    queue=load(root,'queue.json');config=load(root,'worker-input.json');plan=restored_plan(root)
    run=rows[0];launches=[r for r in rows if r['event']=='MODEL_LAUNCH'];frozen=[r for r in rows if r['event']=='FROZEN']
    require(run.get('contract_id')=='034' and len(launches)==len(frozen)==1,'SCORE_RUN_BINDING')
    launch=launches[0];close=closes[0];exit_row=exits[0]
    require(queue['contract_id']=='034' and queue['run_id']==run['run_id']==close['run_id']==exit_row['run_id']==launch['run_id']
            and frozen[0]['plan_hash']==queue['plan_hash']==close['plan_hash']==digest(asdict(plan))
            and frozen[0]['worker_hash']==queue['worker_hash']==close['worker_hash']==digest(config)
            and digest(queue)==launch['queue_hash']==exit_row['queue_hash']==close['queue_hash']
            and exit_row['launch_hash']==launch['hash'],'SCORE_HASH_BINDING')
    resource=resource_receipt_034(rows,root)
    require(launch.get('resource_hash')==resource['hash'] and exit_row['exit_binding']==digest(load(root,'gpu-worker-exit-private.json')),'034_SCORE_RESOURCE_EXIT')
    validate_queue_034(queue,config)
    slots=config['slots'];terminal=[r for r in rows if r['event']=='TERMINAL']
    require(queue['slots']==slots and len(slots)==16 and {r['slot'] for r in slots}==set(range(16))
            and len({r['key'] for r in terminal})==16 and {r['key'] for r in terminal}=={str(n) for n in range(16)}
            and close['terminal_hash']==digest(terminal),'SCORE_QUEUE_TERMINAL_BINDING')
    attempts=[r for r in rows if r['event']=='STARTED']
    for n,item in enumerate(attempts):validate_start_034(attempts[:n],queue,config,item)
    started={r['key'] for r in attempts}
    mapping={str(s['slot']):s for s in slots}
    for item in terminal:
        expected=mapping[item['key']]
        require(item['alias']==expected['alias'] and item['arm']==expected['arm']
                and item['state'] in ('RETURNED','INVALID','FAILED','NOT_RUN')
                and (item['state'] not in ('RETURNED','INVALID') or item['key'] in started),'SCORE_SLOT_BINDING')


class SnapshotRaw(io.RawIOBase):
    def __init__(self, file, expected):
        super().__init__(); self.file = file; self.expected = expected; self.count = 0
        self.sha = hashlib.sha256(); self.eof = False
    def readable(self):
        return True
    def readinto(self, buffer):
        require(self.count <= self.expected, 'SCORE_BYTE_CAP')
        chunk = self.file.read(min(len(buffer), self.expected - self.count + 1))
        self.count += len(chunk); require(self.count <= self.expected, 'SCORE_OVERSIZE')
        self.sha.update(chunk); self.eof = not chunk
        buffer[:len(chunk)] = chunk; return len(chunk)
    def close(self):
        if not self.closed:
            self.after = os.fstat(self.file.fileno()); self.file.close()
        super().close()


def score(root):
    from temporal_evidence_scorer_025 import OneShotScorer, FrozenLedger, TerminalAttempt, ChildExitReceipt
    journal = Journal(root)
    try:
        journal.once('SCORE_CONSUMED', 'original')
        score_allowed(journal.rows,root)
        snapshot = load(root, 'expected-snapshot.json'); reference = load(root, 'annotation-reference.json')
        plan = restored_plan(root); terminal = {int(r['key']): r for r in journal.events('TERMINAL')}
        if journal.rows[0].get('purpose')=='FICTIONAL_034_WITNESS':
            require(Path(reference['path']).parent==Path(root) and all(q.key.source.startswith('fixture_') for q in plan.questions), 'FICTIONAL_SCORE_SCOPE')
        ledger = FrozenLedger(tuple(TerminalAttempt(call, terminal[n]['state'], terminal[n].get('prediction')) for n, call in enumerate(plan.calls)), True)
        exit_row = journal.events('MODEL_EXIT')[0]
        receipt = ChildExitReceipt((str(exit_row['pid']),), (str(exit_row['pid']),), True)
        holders = []; diagnostic = {}
        def opener():
            path, before = checked_path(reference['path'])
            require([before.st_dev,before.st_ino] == reference['identity'] and before.st_size == snapshot['size']
                    and before.st_mtime_ns == reference['mtime_ns'] and before.st_size <= 4 * MIB, 'SCORE_FILE_CHANGED')
            require(not journal.events('INPUT') or not any(r['category'] == 'gold' for r in journal.events('INPUT')), 'GOLD_ALREADY_OPENED')
            used = journal.events('INPUT')
            require(sum(r['size'] for r in used if r['category']!='frame-cache') + before.st_size <= 40 * MIB, 'INPUT_CAP')
            journal.once('INPUT', 'gold', category='gold', path=str(path), identity=reference['identity'], size=before.st_size)
            file = open(path, 'rb'); opened = os.fstat(file.fileno())
            if not os.path.samestat(before, opened):
                file.close(); raise ContractError('SCORE_IDENTITY')
            raw = SnapshotRaw(file, before.st_size); holders.append((raw, before, opened, path))
            return io.TextIOWrapper(io.BufferedReader(raw), encoding='utf-8')
        report = OneShotScorer().score(opener, plan, ledger, receipt, profile=snapshot['binding'][0],
                                     expected_binding=tuple(snapshot['binding']), diagnostic=diagnostic)
        require(len(holders) == 1, 'SCORE_OPEN_FAILED')
        raw, before, opened, path = holders[0]; after = path.stat()
        stable = lambda a,b: (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns) == (b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns)
        require(diagnostic.get('complete') is True and raw.eof and raw.count == snapshot['size']
                and raw.sha.hexdigest() == snapshot['sha256'] and stable(before,after) and stable(opened,raw.after), 'FULL_SNAPSHOT_BINDING')
        journal.write('score-private.json', asdict(report))
        # Publish only after the complete stream/OS/snapshot gate.
        safe = asdict(report)
        for index, source in enumerate(safe['by_source']):
            source['source'] = 'P%d' % (index+1)
        journal.write('score-anonymous.json', safe)
        journal.add('SCORED', status=report.status, n=4, raw_bytes=raw.count, decoded_labels=4,
                    run_id=journal.rows[0]['run_id'],queue_hash=digest(load(root,'queue.json')),raw_binding=True)
    except Exception as error:
        journal.write('score-hold.json', dict(status='UNKNOWN', reason=str(error) if isinstance(error,ContractError) else type(error).__name__))
    finally:
        journal.close()


def execute(root):
    import xml.etree.ElementTree as ET
    gate = Journal(root)
    try:
        require_ready(gate)
        require(gate.events('PREPARED') and not gate.events('MODEL_LAUNCH'), 'PREPARED_ONCE_REQUIRED')
    finally:
        gate.close()
    runtime = load(root, 'runtime.json'); own_python = sys.executable
    reference = load(root, 'annotation-reference.json'); handle = None
    model_exit = None
    try:
        handle = ExclusiveRead(reference['path'])
        journal = Journal(root); journal.once('ORIGINAL_LOCK', 'annotation', body=0); journal.close()
        for n in range(2):
            probe_result = phase(root, 'refusal-%d' % n, 'cpu', 5,
                                 python_command(own_python,'development_pilot_030','probe',reference['path']))
            require(probe_result['exit_code'] == 0 and json.loads(probe_result['stdout'])['denied'] is True, 'ORIGINAL_REFUSAL_PROBE')
        journal=Journal(root)
        try:
            require(journal.events('FRAME_CACHE_VERIFIED'),'034_FRAME_CACHE_REQUIRED')
            config=load(root,'worker-input.json')
            queue=make_queue(root,journal,AVAILABLE_034)
            for item in config['slots']:
                if item['alias']!='P2':
                    journal.once('TERMINAL',str(item['slot']),alias=item['alias'],arm=item['arm'],state='NOT_RUN',reason='NOT_AVAILABLE_FROM_CLOSED_CACHE')
        finally:journal.close()
        telemetry=phase(root,'gpu-resource','cpu',10,python_command(own_python,'development_pilot_030','resource-034',str(root)))
        require(telemetry['exit_code']==0 and not telemetry['overflow'] and telemetry['job_active']==0,'034_RESOURCE_CHILD_HOLD')
        journal=Journal(root)
        try:resource=resource_receipt_034(journal.rows,root)
        finally:journal.close()
        # No credential values/profile overrides are passed to the model child.
        environment = {k:v for k,v in os.environ.items() if not k.upper().startswith(('AWS_','AZURE_','GOOGLE_','HF_TOKEN'))}
        environment.update(PATH=runtime['path'],HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',
                           TEMP=str(root),TMP=str(root),TOKENIZERS_PARALLELISM='false',PYTHONDONTWRITEBYTECODE='1')
        journal=Journal(root);journal.once('MODEL_LAUNCH','gpu',run_id=journal.rows[0]['run_id'],queue_hash=digest(load(root,'queue.json')),resource_hash=resource['hash']);journal.close()
        model_exit = phase(root,'gpu-worker','gpu',900,
                           python_command(runtime['python'],'development_worker_030',str(root),site=runtime['site']),environment)
    except Exception as error:
        journal=Journal(root)
        journal.write('execution-hold.json',dict(reason=str(error) if isinstance(error,ContractError) else type(error).__name__))
        journal.close()
    finally:
        journal=Journal(root)
        config=load(root,'worker-input.json')
        ended={r['key'] for r in journal.events('TERMINAL')}; started={r['key'] for r in journal.events('STARTED')}
        for item in config['slots']:
            key=str(item['slot'])
            if key not in ended:
                journal.once('TERMINAL',key,alias=item['alias'],arm=item['arm'],state='FAILED' if key in started else 'NOT_RUN',reason='WORKER_STOPPED')
        if model_exit:
            close_model_queue(root,journal,model_exit)
        else:
            journal.add('NO_MODEL_QUEUE_CLOSED',slots=16)
        can_score=bool(model_exit and any(r['state'] in ('RETURNED','INVALID') for r in journal.events('TERMINAL')))
        journal.close()
        if handle is not None:
            handle.close()
        if can_score:
            scored=phase(root,'score','cpu',60,python_command(own_python,'development_pilot_030','score',str(root)))
            journal=Journal(root)
            try:
                rows=journal.events('SCORED')
                okay=scored['exit_code']==0 and len(rows)==1 and rows[0]['status']=='PASS' and rows[0].get('raw_binding') is True
                journal.add('SCORE_PUBLICATION',status='BOUND_SCORE_AVAILABLE' if okay else 'UNKNOWN_NO_BOUND_SCORE')
            finally:journal.close()


def finish_stopped(root):
    raise ContractError('OLD_030_FINALIZER_CLOSED')
    """Close this failed030 without original input, credentials, media or model IO."""
    import ast
    journal = Journal(root)
    try:
        journal.reserve_time('cpu', 60, 'finalize-stopped')
        # Recover the already persisted two suite exits, not another execution.
        for number in (1,2):
            name='suite-%d' % number
            result=load(root,name+'-exit-private.json')
            if not any(r['name']==name for r in journal.events('SUITE_RESULT')):
                journal.add('SUITE_RESULT',name=name,passed=False,tests=0 if number==1 else 18,
                            failures=0 if number==1 else 2,exit_code=result['exit_code'])
        require(len(journal.events('SUITE'))==2 and not any(r['passed'] for r in journal.events('SUITE_RESULT')), 'STOP_REASON_BINDING')
        journal.once('RUN_STOPPED','030',reason='SECOND_SUITE_FAILED_NO_THIRD_ATTEMPT')
        cached=dict(status='HOLD')
        try:
            plan=restored_plan(root)
            require(len(plan.questions)==4 and len(plan.calls)==16
                    and packed(asdict(plan))==packed(load(root,'plan.json')['plan']), 'CACHED_PLAN_BINDING')
            require([asdict(q.key) for q in plan.questions]==load(root,'keys.json')['keys'],'CACHED_KEYS')
            binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1']
            for name in ('keys','cohort','nongold','plan','receipts','official'):
                require(load(root,name+'.json')['binding']==binding,'CACHED_PROFILE')
            options=load(root,'nongold.json')['projection']['questions']
            require(len(options)==4 and all(len(q['options'])==5 and all(v.strip() for v in q['options']) for q in options),'CACHED_OPTIONS')
            receipt=[r for r in load(root,'receipts.json')['receipts'] if r['alias']=='annotation']
            require(len(receipt)==3 and all(r['complete'] for r in receipt)
                    and len({(r['byte_count'],r['digest'],tuple(r['before'])) for r in receipt})==1,'CACHED_FULL_RECEIPT')
            reference=load(root,'annotation-reference.json')
            require(reference['identity']==receipt[0]['before'][:2] and reference['size']==receipt[0]['byte_count']
                    and reference['mtime_ns']==receipt[0]['before'][3],'INITIAL_STAT_TO_028_BINDING')
            helper_matches=0
            for number in (0,1):
                factory=ast.parse((Path(root)/('factory_%d.py' % number)).read_text(encoding='utf-8'))
                source=ast.parse((Path(root)/('runner_%d.py' % number)).read_text(encoding='utf-8'))
                left=[n for n in ast.walk(factory) if isinstance(n,ast.FunctionDef) and n.name=='inputs']
                right=[n for n in ast.walk(source) if isinstance(n,ast.FunctionDef) and n.name=='inputs']
                require(len(left)==len(right)==1 and ast.dump(left[0])==ast.dump(right[0]),'CACHED_HELPER_AST')
                helper_matches+=1
            official=load(root,'official.json')['joined']['rows'];targets=load(root,'targets.json')['targets']
            require(len(targets)==4,'CACHED_TARGET_COUNT')
            for n,q in enumerate(plan.questions):
                row=official[q.key.source]
                require(row['video_uid']==q.key.source and row['canonical_s3_location']==targets[n]['uri']
                        and targets[n]['alias']=='P%d' % (n+1) and row['release_1']=='True'
                        and row['canonical_is_validated']=='True','CACHED_OFFICIAL_JOIN')
            cached=dict(status='PASS_CACHED_NONGOLD_ONLY',n=4,options=20,slots=16,helpers_ast_equal=helper_matches,
                        full028_receipts=3,profile=binding,source_overlap_allowed=True,prior_exposure_possible=True)
        except Exception as error:
            cached['reason']=str(error) if isinstance(error,ContractError) else type(error).__name__
        slots=[dict(slot=n,alias='P%d' % (n//4+1),arm='ABCD'[(n%4+n//4)%4],state='NOT_RUN',reason='SECOND_SUITE_FAILED') for n in range(16)]
        require(not journal.events('STARTED') and not journal.events('HTTPS') and not journal.events('MODEL_LAUNCH'),'NO_REAL_ACTIONS_FOR_STOP')
        for item in slots:
            journal.once('TERMINAL',str(item['slot']),alias=item['alias'],arm=item['arm'],state='NOT_RUN',reason=item['reason'])
        journal.write('stopped-queue.json',dict(n=4,slots=slots,queue_closed=True,model_launched=False,gold_opens=0))
        journal.add('NO_MODEL_QUEUE_CLOSED',slots=16,reason='SUITE_FAILURE',gold_allowed=False)
        journal.write('cached-handoff-verification.json',cached)
        inputs=journal.events('INPUT');windows=journal.events('WINDOW');exits=journal.events('PHASE_EXIT')
        summary=dict(status='IMPLEMENTATION_WITNESS_HOLD_REAL_QA_NOT_RUN',cached=cached,n=4,slots=16,
            suite_starts=2,first_suite_tests=0,second_suite_tests=18,second_suite_passed=16,second_suite_failures=2,
            fixture_children=len(journal.events('FIXTURE')),source_opens=len(inputs),source_bytes=sum(r['size'] for r in inputs),
            input_categories={k:sum(r['category']==k for r in inputs) for k in ('handoff','source','config','gold')},
            cpu_reserved_seconds=sum(r['seconds'] for r in windows if r['stage']=='cpu'),
            observed_suite_windows_seconds=sum(r['seconds'] for r in exits),parent_elapsed_seconds=time.time()-journal.rows[0]['epoch'],
            actual_https=0,head_bucket=0,head_object=0,get_object=0,media_bytes=0,original_annotation_body=0,gold_opens=0,
            model_launches=0,generate=0,gpu_seconds=0,nvidia_queries=0,training_updates=0)
        journal.write('final-summary.json',summary)
        print(json.dumps(summary))
    finally:
        journal.close()


def finalize_034(root, reason=None):
    journal=Journal(root)
    try:
        journal.reserve_time('cpu',30,'finalize-034')
        config=load(root,'worker-input.json') if (Path(root)/'worker-input.json').exists() else None
        slots=config['slots'] if config else [dict(slot=n,alias='P%d' % (n//4+1),arm='ABCD'[(n%4+n//4)%4]) for n in range(16)]
        ended={r['key'] for r in journal.events('TERMINAL')};started={r['key'] for r in journal.events('STARTED')}
        for slot in slots:
            key=str(slot['slot'])
            if key not in ended:
                journal.once('TERMINAL',key,alias=slot['alias'],arm=slot['arm'],state='FAILED' if key in started else 'NOT_RUN',
                             reason=reason or 'NOT_STARTED_OR_WORKER_STOPPED')
        if not journal.events('QUEUE_CLOSED') and not journal.events('NO_MODEL_QUEUE_CLOSED'):
            journal.add('NO_MODEL_QUEUE_CLOSED',slots=16,gold_allowed=False)
        windows=journal.events('WINDOW');inputs=journal.events('INPUT');complete=journal.events('INPUT_COMPLETE')
        transport=journal.events('TRANSPORT_SEND');results=journal.events('SUITE_RESULT')
        summary=dict(contract_id='034',run_id=journal.rows[0]['run_id'],reason=reason,n=4,slots=16,
            suites=[{k:r.get(k) for k in ('name','tests','passed','failures','errors','skips','os_marks')} for r in results],
            cache_bound=bool(journal.events('CACHE_BOUND')),cache_holds=[r.get('aliases') for r in journal.events('CACHE_HOLD')],
            input_opens=len(inputs),complete_inputs=len(complete),reserved_input_bytes=sum(r['size'] for r in inputs),
            actual_input_bytes=sum(r['size'] for r in complete),
            input_categories={k:sum(r['category']==k for r in inputs) for k in ('handoff','source','config','gold')},
            reserved_windows={s:sum(r['seconds'] for r in windows if r['stage']==s) for s in ('cpu','media','acquisition','gpu')},
            observed_windows=sum(r['seconds'] for r in journal.events('PHASE_EXIT')),
            actual_https_attempts=len(transport),http_reserved=len(journal.events('HTTPS')),
            api_attempts={api:sum(r['slot'].startswith(api+':') for r in transport) for api in ('HeadBucket','HeadObject','GetObject')},
            body_debited=sum(r['amount'] for r in journal.events('BODY_DEBIT')),model_launches=len(journal.events('MODEL_LAUNCH')),
            generate_attempts=len(journal.events('STARTED')),terminal=[{k:r.get(k) for k in ('key','alias','arm','state','reason')} for r in journal.events('TERMINAL')],
            fixture_pid_reservations=len(journal.events('FIXTURE_PID')),gold_opens=sum(r['category']=='gold' for r in inputs),
            scored=[{k:r.get(k) for k in ('status','n','raw_bytes','raw_binding')} for r in journal.events('SCORED')],
            parent_seconds=time.time()-journal.rows[0]['epoch'])
        if (Path(root)/'worker-result.json').exists():
            summary['worker']=load(root,'worker-result.json')
        journal.write('034-final-summary-private.json',summary)
        journal.once('RUN_STOPPED','034',reason=reason or 'ROUND_DELIVERED_NO_CONTINUATION')
        print(json.dumps({k:v for k,v in summary.items() if k not in ('run_id','worker','terminal')}))
    finally:journal.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['initialize', 'probe', 'prepare', 'execute', 'score', 'finalize-stopped','finalize-034', 'copy-034', 'resource-034'])
    parser.add_argument('root')
    args = parser.parse_args()
    if args.mode == 'probe':
        probe(args.root); return
    payload = sys.stdin.readline()
    if args.mode == 'initialize':
        config = json.loads(payload); initialize(args.root, config['entries'], config['annotation']); return
    if args.mode == 'copy-034':
        copy_frames_034(args.root)
    elif args.mode == 'resource-034':
        query_resource_034(args.root)
    elif args.mode == 'prepare':
        prepare(args.root)
    elif args.mode == 'execute':
        execute(args.root)
    elif args.mode == 'score':
        score(args.root)
    elif args.mode == 'finalize-stopped':
        finish_stopped(args.root)
    elif args.mode == 'finalize-034':
        finalize_034(args.root)


if __name__ == '__main__':
    main()
