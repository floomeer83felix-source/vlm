"""033 fictional resource/cache/queue witnesses; no old tests, ML or network."""
import argparse
import copy
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import time
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

import development_pilot_030 as p
from temporal_evidence_adapter_025 import (TASK,Projection,SourceRecord,QuestionRecord,QuestionKey,build_plan)

ROOT=None
SUITE=None
EXPECTED=6
MARKS={}


def xml(free='22000 MiB',util='5 %',uid='fictional-device',minor='0'):
    return ('<nvidia_smi_log><gpu id="fictional-bus"><product_name>RTX 3090</product_name>'
            '<minor_number>'+minor+'</minor_number><uuid>'+uid+'</uuid>'
            '<fb_memory_usage><free>'+free+'</free></fb_memory_usage><utilization><gpu_util>'+util+
            '</gpu_util></utilization><driver_model><current_dm>WDDM</current_dm></driver_model>'
            '<processes><process_info><type>C+G</type></process_info></processes></gpu></nvidia_smi_log>')


def plan_config():
    sources=tuple(SourceRecord('fixture_%d'%n,()) for n in range(4))
    questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening did closing?',tuple('abcde')) for s in sources)
    plan=build_plan(Projection('inference',sources,questions))
    slots=[dict(slot=n,alias='P%d'%(n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)]
    return plan,dict(slots=slots)


class MemoryJournal:
    def __init__(self,root=None,rows=None):self.root=root;self.rows=rows or [];self.saved={}
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**fields):
        row=dict(event=event,**fields);row['hash']=p.digest(row);self.rows.append(row)
    def once(self,event,key,**fields):
        p.require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY')
        self.add(event,key=key,**fields)
    def reserve_output(self,name,size,category='metadata',files=1):
        p.require(not (self.root/name).exists(),'OUTPUT_EXISTS')
        self.add('OUTPUT',key=name,size=size,category=category)
    def write(self,name,value):self.saved[name]=value
    def close(self):pass


def chain(rows):
    out=[]
    for value in rows:
        row=dict(value,seq=len(out),prev=out[-1]['hash'] if out else '0'*64)
        row['hash']=p.digest(row);out.append(row)
    return b''.join(p.packed(r)+b'\n' for r in out)


def archive_fixture():
    plan,config=plan_config();binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1']
    reference=dict(identity=[1,2],size=3,mtime_ns=4,path='fictional-annotation')
    snapshot=dict(binding=binding,size=3,sha256='fictional-raw-hash')
    receipt=dict(alias='annotation',complete=True,byte_count=3,digest=snapshot['sha256'],before=[1,2,3,4,5])
    targets=[dict(alias='P%d'%n,bucket='fixture',key='opaque%d'%n,uri='s3'+':/'+'/fixture/opaque%d'%n) for n in range(1,5)]
    head=dict(alias='P2',region='fictional-region',eligible=True,status=200,ContentLength=3,ETag='"fake"',VersionId='fake-version')
    media=dict(alias='P2',uri=targets[1]['uri'],size=3,received=3,sha256='fake-media',**{k:head[k] for k in ('ContentLength','ETag','VersionId')})
    queue=dict(contract_id='032',run_id='old-fictional',worker_hash=p.digest(config),plan_hash=p.digest(asdict(plan)),slots=config['slots'],available=p.AVAILABLE_033)
    values={name:{} for name in ('keys','cohort','nongold','heads029','official','execution-config','runtime','032-final-summary-private','gpu-resource-exit-private')}
    values.update(plan=dict(plan=asdict(plan)),receipts=dict(receipts=[receipt]*3),targets=dict(targets=targets),
                  **{'P2-head':head,'P2-media-binding':media,'P2-candidates':dict(alias='P2',frames='P2-frames.npy',demux_eof=True,corrupt=0,missing=0),
                     'worker-input':config,'queue':queue,'annotation-reference':reference,'expected-snapshot':snapshot})
    payload={n:(p.packed(v),v) for n,v in values.items()}
    rows=[dict(event='RUN',contract_id='032',root_name='integration_032',purpose='REAL_032',run_id='old-fictional')]
    rows+=[dict(event='OUTPUT',key=n+'.json',size=len(raw)) for n,(raw,v) in payload.items()]
    rows+=[dict(event='INPUT_COMPLETE',alias='cache_'+n,size=len(payload[n][0]),sha256=hashlib.sha256(payload[n][0]).hexdigest()) for n in ('keys','cohort','nongold','plan','receipts','targets','heads029','official','P2-head')]
    rows.append(dict(event='SUITE_RESULT',contract_id='032',run_id='old-fictional',passed=True,tests=6,failures=0,errors=0,skips=0))
    rows.append(dict(event='FROZEN',plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash']))
    for n in range(1,5):
        alias='P%d'%n;slot='GetObject:'+alias;url='https://s3.fictional-region.amazonaws.com/fixture/opaque%d'%n
        rows.extend([dict(event='HTTPS',key=slot,api='GetObject',method='GET',url=url),
                     dict(event='TRANSPORT_SEND',slot=slot,method='GET',url=url),
                     dict(event='TRANSPORT_RESPONSE',slot=slot,status=200,profile='CURRENT_IFMATCH_PINNED_RESPONSE_032'),
                     dict(event='PHASE_EXIT',name='get-'+alias,code=0 if n==2 else 99,job_active=0)])
    rows.extend([dict(event='BODY_DEBIT',alias='P2',amount=3),dict(event='MEDIA_COMPLETE',alias='P2',size=3),
                 dict(event='PHASE_EXIT',name='candidates-P2',code=0,job_active=0)])
    rows+=[dict(event='TERMINAL',key=str(n),state='NOT_RUN') for n in range(16)]
    rows.append(dict(event='RUN_STOPPED'))
    return rows,payload


def scoring_fixture():
    plan,config=plan_config();j=MemoryJournal(rows=[dict(event='RUN',contract_id='033',run_id='new-fictional')])
    queue=dict(contract_id='033',run_id='new-fictional',worker_hash=p.digest(config),plan_hash=p.digest(asdict(plan)),slots=config['slots'],available=p.AVAILABLE_033)
    observations=dict(xml=[xml(),xml()],starts=[0,1.1],query_device=0);samples=p.parse_resource_samples_033(observations['xml'])
    j.add('FROZEN',worker_hash=queue['worker_hash'],plan_hash=queue['plan_hash'])
    j.add('RESOURCE_ADMITTED',run_id='new-fictional',profile=p.RESOURCE_PROFILE_033,queue_hash=p.digest(queue),samples_hash=p.digest(samples),device_uuid=samples[0]['uuid'])
    j.add('MODEL_LAUNCH',run_id='new-fictional',queue_hash=p.digest(queue),resource_hash=j.events('RESOURCE_ADMITTED')[0]['hash'])
    for s in config['slots']:
        if s['alias']=='P2':j.add('STARTED',key=str(s['slot']),alias=s['alias'],arm=s['arm'])
        j.add('TERMINAL',key=str(s['slot']),alias=s['alias'],arm=s['arm'],state='RETURNED' if s['alias']=='P2' else 'NOT_RUN')
    exited=dict(pid=123,job_active=0,exit_code=0,seconds=.01)
    data={'queue.json':queue,'worker-input.json':config,'gpu-samples-private.json':observations,'gpu-worker-exit-private.json':exited}
    with patch.object(p,'load',side_effect=lambda root,name:data[name]):p.close_model_queue(ROOT,j,exited)
    return j,plan,data


class CachedGPU033(unittest.TestCase):
    def test_01_resource_windows(self):
        good=p.parse_resource_samples_033([xml(),xml()]);self.assertEqual(good[0]['process_types'],{'C+G':1})
        self.assertEqual(p.parse_resource_samples_033([xml(minor='N/A'),xml(minor='N/A')])[0]['device'],'0')
        with self.assertRaises(ValueError):p.parse_resource_samples_033([xml(),xml()],query_device=1)
        for bad in [xml(free='20479 MiB'),xml(util='21 %'),xml(util='N/A'),xml(util='NaN %'),xml(free='22 GiB'),xml(uid='other'),xml(minor='1'),xml()[:-5]]:
            with self.subTest(bad=bad):
                with self.assertRaises((ValueError,ET.ParseError)):p.parse_resource_samples_033([xml(),bad])
        with self.assertRaises(ValueError):p.parse_resource_samples_033([xml()])
        MARKS['resource_windows']=True

    def test_02_archive_and_metadata(self):
        rows,payload=archive_fixture();raw=chain(rows)
        parsed=p.archive_032_rows(raw);p.validate_cache_032(parsed,payload)
        for bad in [raw[:-1],raw.replace(b'old-fictional',b'bad-fictional',1),chain(rows[:-1])]:
            with self.assertRaises(ValueError):p.archive_032_rows(bad)
        for extra in [dict(event='MODEL_LAUNCH'),dict(event='INPUT',category='gold')]:
            with self.assertRaises(ValueError):p.archive_032_rows(chain(rows[:-1]+[extra,rows[-1]]))
        for name,field,value in [('P2-head','VersionId','changed'),('P2-media-binding','size',4),('P2-candidates','frames','other.npy')]:
            bad=copy.deepcopy(payload);bad[name][1][field]=value
            with self.assertRaises(ValueError):p.validate_cache_032(parsed,bad)
        bad=copy.deepcopy(payload);bad['keys']=(b'[]',{})
        with self.assertRaises(ValueError):p.validate_cache_032(parsed,bad)
        MARKS['archive_032']=True

    def test_03_frame_copy_and_hashes(self):
        parent=ROOT/('witness-copy-'+SUITE);parent.mkdir();old=parent/'integration_032';old.mkdir();new=parent/'integration_033';new.mkdir()
        raw=bytes(range(144));header=repr(dict(descr='|u1',fortran_order=False,shape=(48,1,1,3))).encode()+b'\n'
        encoded=b'\x93NUMPY\x01\x00'+struct.pack('<H',len(header))+header+raw
        (old/'P2-frames.npy').write_bytes(encoded)
        candidate=dict(frames='P2-frames.npy',times=list(range(48)),frame_bytes=144,rgb_hashes=[hashlib.sha256(raw[n:n+3]).hexdigest() for n in range(0,144,3)])
        data={'frame-source-reference-private.json':dict(path=str(old/'P2-frames.npy'),reserved_size=len(encoded)),'P2-candidates.json':candidate}
        j=MemoryJournal(new)
        with patch.object(p,'Journal',return_value=j),patch.object(p,'require_ready'),patch.object(p,'load',side_effect=lambda root,name:data[name]):
            p.copy_frames_033(new)
            self.assertEqual((new/'P2-frames.npy').read_bytes(),encoded)
            self.assertEqual(len(j.events('FRAME_CACHE_VERIFIED')),1)
            with self.assertRaises(ValueError):p.copy_frames_033(new)
        bad=copy.deepcopy(candidate);bad['rgb_hashes'][0]='bad'
        with self.assertRaises(ValueError):p.verify_npy_033(new/'P2-frames.npy',bad)
        bad=copy.deepcopy(candidate);bad['frame_bytes']+=1
        with self.assertRaises(ValueError):p.verify_npy_033(new/'P2-frames.npy',bad)
        MARKS['frame_copy']=True

    def test_04_only_p2_and_binding(self):
        j,plan,data=scoring_fixture();q=data['queue.json'];config=data['worker-input.json']
        p.validate_queue_033(q,config)
        attempts=j.events('STARTED')
        for n,item in enumerate(attempts):p.validate_start_033(attempts[:n],q,config,item)
        with self.assertRaises(ValueError):p.validate_start_033(attempts,q,config,attempts[0])
        bad=copy.deepcopy(q);bad['available']['P1']=True
        with self.assertRaises(ValueError):p.validate_queue_033(bad,config)
        with self.assertRaises(ValueError):p.validate_start_033([],q,config,dict(key='0',alias='P1',arm='A'))
        with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'restored_plan',return_value=plan):
            p.score_allowed(j.rows,ROOT)
            j.events('MODEL_LAUNCH')[0]['resource_hash']='wrong'
            with self.assertRaises(ValueError):p.score_allowed(j.rows,ROOT)
        MARKS['bindings_033']=True

    def test_05_score_refusal_opener_zero(self):
        for fault in ('exit','resource','queue','run'):
            j,plan,data=scoring_fixture()
            if fault=='exit':j.rows=[r for r in j.rows if r['event']!='MODEL_EXIT']
            elif fault=='resource':j.events('RESOURCE_ADMITTED')[0]['profile']='old032'
            elif fault=='queue':data['queue.json']['available']['P4']=True
            else:j.rows[0]['contract_id']='032'
            with patch.object(p,'Journal',return_value=j),patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'restored_plan',return_value=plan),patch('builtins.open') as opener:
                p.score(ROOT);self.assertEqual(opener.call_count,0)
            self.assertEqual(len(j.events('SCORE_CONSUMED')),1);self.assertIn('score-hold.json',j.saved)

    def test_06_no_network_and_fixed_gate(self):
        import ast,inspect
        tree=ast.parse(inspect.getsource(p.execute));text=ast.dump(tree)
        for word in ('development_media_030','get_object','candidates','sdk_python'):self.assertNotIn(word,text)
        # Actual production Journal refuses even an accidentally invoked old SendGate.
        from development_media_030 import SendGate
        outer=p.Journal(ROOT);outer.reserve_output('witness-gate-'+SUITE,4096,files=5);outer.close()
        folder=ROOT/('witness-gate-'+SUITE);folder.mkdir();child=folder/'integration_033'
        j=p.Journal(child,create=True,fixture=True)
        try:
            with self.assertRaises(ValueError):SendGate(j,'GetObject:P2','GET','https://fictional/object').reserve('GET','https://fictional/object')
            self.assertFalse(j.events('HTTPS'))
            with self.assertRaises(ValueError):p.require_ready(j)
        finally:j.close()
        MARKS['no_network']=True


def main():
    global ROOT,SUITE
    parser=argparse.ArgumentParser();parser.add_argument('root');parser.add_argument('suite');args=parser.parse_args()
    sys.stdin.readline();ROOT=Path(args.root);SUITE=args.suite
    j=p.Journal(ROOT);run_id=j.rows[0]['run_id'];j.reserve_output('witness-copy-'+SUITE,16384,files=8);j.close()
    names=['test_%02d_%s'%(n,s) for n,s in enumerate(('resource_windows','archive_and_metadata','frame_copy_and_hashes','only_p2_and_binding','score_refusal_opener_zero','no_network_and_fixed_gate'),1)]
    suite=unittest.TestSuite(CachedGPU033(n) for n in names)
    started=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt=dict(contract_id='033',run_id=run_id,expected=EXPECTED,loaded=suite.countTestCases(),tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS,seconds=time.monotonic()-started)
    j=p.Journal(ROOT);j.write(args.suite+'-result.json',receipt);j.close()
    print(json.dumps(receipt));sys.exit(0 if result.wasSuccessful() and result.testsRun==EXPECTED else 1)


if __name__=='__main__':main()
