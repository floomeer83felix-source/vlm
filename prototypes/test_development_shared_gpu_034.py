"""034 policy/archive/receipt delta witnesses; no historical tests or ML."""
import argparse
import ast
import copy
from dataclasses import asdict
import hashlib
import inspect
import json
from pathlib import Path
import struct
import sys
import time
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import development_pilot_030 as p
from temporal_evidence_adapter_025 import (TASK,Projection,SourceRecord,QuestionRecord,QuestionKey,build_plan)

ROOT=None
SUITE=None
MARKS={}
IDENTITY=dict(query_device=0,uuid='fictional-device',bus='fictional-bus')


def xml(free='22000 MiB',util='100 %',uid='fictional-device',bus='fictional-bus',minor='N/A'):
    return ('<nvidia_smi_log><gpu id="'+bus+'"><product_name>RTX 3090</product_name><uuid>'+uid+
            '</uuid><minor_number>'+minor+'</minor_number><fb_memory_usage><free>'+free+
            '</free></fb_memory_usage><utilization><gpu_util>'+util+'</gpu_util></utilization>'
            '<driver_model><current_dm>WDDM</current_dm></driver_model><processes>'
            '<process_info><type>C+G</type></process_info></processes></gpu></nvidia_smi_log>')


def plan_config():
    sources=tuple(SourceRecord('fictional_%d'%n,()) for n in range(4))
    questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening did closing?',tuple('abcde')) for s in sources)
    plan=build_plan(Projection('inference',sources,questions))
    config=dict(slots=[dict(slot=n,alias='P%d'%(n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)])
    return plan,config


class MemoryJournal:
    def __init__(self,root=None,rows=None):self.root=root;self.rows=rows or [];self.saved={}
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**fields):
        row=dict(event=event,**fields);row['hash']=p.digest(row);self.rows.append(row)
    def once(self,event,key,**fields):
        p.require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY');self.add(event,key=key,**fields)
    def reserve_output(self,name,size,category='metadata',files=1):
        p.require(not (self.root/name).exists(),'OUTPUT_EXISTS');self.add('OUTPUT',key=name,size=size)
    def write(self,name,value):self.saved[name]=value
    def close(self):pass


def chain(rows):
    out=[]
    for value in rows:
        row=dict(value,seq=len(out),prev=out[-1]['hash'] if out else '0'*64);row['hash']=p.digest(row);out.append(row)
    return b''.join(p.packed(r)+b'\n' for r in out)


def archive_fixture():
    plan,config=plan_config();snapshot=dict(binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1'],size=3,sha256='fictional-raw')
    reference=dict(identity=[1,2],size=3,mtime_ns=4,path='fictional-annotation')
    receipt=dict(alias='annotation',complete=True,byte_count=3,digest=snapshot['sha256'],before=[1,2,3,4,5])
    head=dict(alias='P2',eligible=True,status=200,ContentLength=3,ETag='fake-etag',VersionId='fake-version')
    targets=[dict(alias='P%d'%n,uri='fictional-object-%d'%n) for n in range(1,5)]
    media=dict(alias='P2',uri=targets[1]['uri'],size=3,received=3,**{k:head[k] for k in ('ETag','VersionId','ContentLength')})
    queue=dict(contract_id='033',run_id='closed-fictional',plan_hash=p.digest(asdict(plan)),worker_hash=p.digest(config),slots=config['slots'],available=p.AVAILABLE_034)
    values={n:{} for n in ('keys','cohort','nongold','heads029','official','execution-config','runtime','033-final-summary-private')}
    values.update(plan=dict(plan=asdict(plan)),receipts=dict(receipts=[receipt]*3),targets=dict(targets=targets),
                  **{'annotation-reference':reference,'worker-input':config,'queue':queue,'expected-snapshot':snapshot,
                     'P2-head':head,'P2-media-binding':media,'P2-candidates':dict(alias='P2',frames='P2-frames.npy',demux_eof=True,corrupt=0,missing=0),
                     'frozen-worker-032':config,'frozen-snapshot-032':snapshot,'gpu-samples-private':dict(xml=[xml(util='16 %'),xml(util='22 %')],starts=[0,1.2])})
    payload={n:(p.packed(v),v) for n,v in values.items()}
    rows=[dict(event='RUN',contract_id='033',root_name='integration_033',purpose='REAL_033',run_id='closed-fictional')]
    for n,(raw,v) in payload.items():
        rows.append(dict(event='OUTPUT',key=n+'.json',size=len(raw)))
        if n in ('keys','cohort','nongold','plan','receipts','targets','heads029','official','annotation-reference','P2-head','P2-media-binding','P2-candidates'):
            rows.append(dict(event='INPUT_COMPLETE',alias='cache_'+n,size=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    for n,alias in [('frozen-worker-032','cache_worker-input'),('frozen-snapshot-032','cache_expected-snapshot')]:
        rows.append(dict(event='INPUT_COMPLETE',alias=alias,size=len(payload[n][0]),sha256=hashlib.sha256(payload[n][0]).hexdigest()))
    for name in ('suite-1','suite-2'):
        rows.append(dict(event='SUITE_RESULT',name=name,contract_id='033',run_id='closed-fictional',passed=True,expected=6,loaded=6,tests=6,failures=0,errors=0,skips=0))
    rows.extend([dict(event='FROZEN',plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash']),
                 dict(event='INPUT',key='frame-cache',category='frame-cache',size=144),
                 dict(event='INPUT_COMPLETE',alias='frame-cache',size=144,sha256='fictional-full-frame'),
                 dict(event='OUTPUT',key='P2-frames.npy',size=144),
                 dict(event='FRAME_CACHE_VERIFIED',size=144,sha256='fictional-full-frame',rgb_hashes=48),
                 dict(event='GPU_QUERY',key='0'),dict(event='GPU_QUERY',key='1')])
    rows.extend(dict(event='PHASE_EXIT',name=n,code=1 if n=='gpu-resource' else 0,job_active=0) for n in ('prepare','copy-frames','refusal-0','refusal-1','gpu-resource'))
    rows.extend(dict(event='TERMINAL',key=str(n),state='NOT_RUN') for n in range(16));rows.append(dict(event='RUN_STOPPED'))
    return rows,payload


def bound_score_fixture():
    plan,config=plan_config();j=MemoryJournal(rows=[dict(event='RUN',contract_id='034',run_id='new-fictional')])
    queue=dict(contract_id='034',run_id='new-fictional',plan_hash=p.digest(asdict(plan)),worker_hash=p.digest(config),slots=config['slots'],available=p.AVAILABLE_034)
    sample=p.parse_resource_sample_034(xml(),IDENTITY)
    j.add('GPU_QUERY',key='0');j.add('FROZEN',plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash'])
    j.add('RESOURCE_ADMITTED',run_id='new-fictional',queue_hash=p.digest(queue),profile=p.RESOURCE_PROFILE_034,sample_hash=p.digest(sample),device_uuid=sample['uuid'])
    j.add('MODEL_LAUNCH',run_id='new-fictional',queue_hash=p.digest(queue),resource_hash=j.events('RESOURCE_ADMITTED')[0]['hash'])
    for item in config['slots']:
        if item['alias']=='P2':j.add('STARTED',key=str(item['slot']),alias='P2',arm=item['arm'])
        j.add('TERMINAL',key=str(item['slot']),alias=item['alias'],arm=item['arm'],state='RETURNED' if item['alias']=='P2' else 'NOT_RUN')
    exited=dict(pid=123,job_active=0,exit_code=0,seconds=.01)
    data={'worker-input.json':config,'queue.json':queue,'device-identity-reference.json':IDENTITY,
          'gpu-samples-private.json':dict(xml=[xml()],starts=[0],query_device=0),'gpu-worker-exit-private.json':exited}
    with patch.object(p,'load',side_effect=lambda root,name:data[name]):p.close_model_queue(ROOT,j,exited)
    return j,plan,data


class SharedGPU034(unittest.TestCase):
    def test_shared_policy(self):
        for utilization in ('22 %','100 %','N/A','NaN %','101 %'):
            sample=p.parse_resource_sample_034(xml(util=utilization,minor='N/A'),IDENTITY)
            self.assertEqual(sample['utilization_percent'],float(utilization.split()[0]) if utilization in ('22 %','100 %') else None)
        for bad in [xml(free='20479 MiB'),xml(free='NaN MiB'),xml(free='22 GiB'),xml(uid='other'),xml(bus='other'),xml()[:-4],xml().replace('</nvidia_smi_log>','<gpu id="other"></gpu></nvidia_smi_log>')]:
            with self.assertRaises((ValueError,ET.ParseError)):p.parse_resource_sample_034(bad,IDENTITY)
        with self.assertRaises(ValueError):p.parse_resource_sample_034(xml(),IDENTITY,query_device=1)
        MARKS['shared_resource']=True

    def test_closed_archive_and_direct_sha(self):
        rows,payload=archive_fixture();raw=chain(rows);parsed=p.archive_033_rows(raw)
        self.assertEqual(p.validate_cache_033(parsed,payload),IDENTITY)
        for bad in (raw[:-1],raw.replace(b'closed-fictional',b'bad-fictional',1),chain(rows[:-1])):
            with self.assertRaises(ValueError):p.archive_033_rows(bad)
        for extra in (dict(event='MODEL_LAUNCH'),dict(event='INPUT',category='gold')):
            with self.assertRaises(ValueError):p.archive_033_rows(chain(rows[:-1]+[extra,rows[-1]]))
        bad=copy.deepcopy(rows);next(r for r in bad if r['event']=='FRAME_CACHE_VERIFIED')['sha256']='changed'
        with self.assertRaises(ValueError):p.archive_033_rows(chain(bad))
        bad=copy.deepcopy(payload);bad['keys']=(b'[]',{})
        with self.assertRaises(ValueError):p.validate_cache_033(parsed,bad)
        folder=ROOT/('witness-cache-'+SUITE);folder.mkdir();old=folder/'integration_033';new=folder/'integration_034';old.mkdir();new.mkdir()
        pixels=bytes(range(144));header=repr(dict(descr='|u1',fortran_order=False,shape=(48,1,1,3))).encode()+b'\n'
        encoded=b'\x93NUMPY\x01\x00'+struct.pack('<H',len(header))+header+pixels;(old/'P2-frames.npy').write_bytes(encoded)
        candidate=dict(frames='P2-frames.npy',frame_bytes=144,times=list(range(48)),rgb_hashes=[hashlib.sha256(pixels[n:n+3]).hexdigest() for n in range(0,144,3)])
        data={'frame-source-reference-private.json':dict(path=str(old/'P2-frames.npy'),size=len(encoded),sha256=hashlib.sha256(encoded).hexdigest()),'P2-candidates.json':candidate};j=MemoryJournal(new)
        with patch.object(p,'Journal',return_value=j),patch.object(p,'require_ready'),patch.object(p,'load',side_effect=lambda root,name:data[name]):
            p.copy_frames_034(new);self.assertEqual((new/'P2-frames.npy').read_bytes(),encoded)
            with self.assertRaises(ValueError):p.copy_frames_034(new)
        altered=copy.deepcopy(candidate);altered['rgb_hashes'][0]='bad'
        with self.assertRaises(ValueError):p.verify_npy_033(new/'P2-frames.npy',altered)
        # A second fresh fixture has the correct bytes but a wrong historical SHA.
        other=folder/'bad-copy';other.mkdir();data['frame-source-reference-private.json']['sha256']='wrong'
        with patch.object(p,'Journal',return_value=MemoryJournal(other)),patch.object(p,'require_ready'),patch.object(p,'load',side_effect=lambda root,name:data[name]):
            with self.assertRaises(ValueError):p.copy_frames_034(other)
        MARKS['archive_033']=True

    def test_resource_queue_score_binding(self):
        j,plan,data=bound_score_fixture()
        with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'restored_plan',return_value=plan):p.score_allowed(j.rows,ROOT)
        for fault in ('old_profile','run','queue','exit','science'):
            j,plan,data=bound_score_fixture()
            if fault=='old_profile':j.events('RESOURCE_ADMITTED')[0]['profile']='WINDOWS_SHARED_LOW_LOAD_033'
            elif fault=='run':j.rows[0]['contract_id']='033'
            elif fault=='queue':data['queue.json']['available']['P1']=True
            elif fault=='exit':data['gpu-worker-exit-private.json']['pid']=124
            else:data['worker-input.json']['changed_prompt']='fictional'
            with patch.object(p,'Journal',return_value=j),patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'restored_plan',return_value=plan),patch('builtins.open') as opener:
                p.score(ROOT);self.assertEqual(opener.call_count,0)
            self.assertEqual(len(j.events('SCORE_CONSUMED')),1)
            with self.assertRaises(ValueError):j.once('SCORE_CONSUMED','original')
        j,plan,data=bound_score_fixture();starts=j.events('STARTED')
        for n,item in enumerate(starts):p.validate_start_034(starts[:n],data['queue.json'],data['worker-input.json'],item)
        with self.assertRaises(ValueError):p.validate_start_034(starts,data['queue.json'],data['worker-input.json'],starts[0])
        MARKS['bindings_034']=True

    def test_single_query_and_zero_media_gate(self):
        tree=ast.dump(ast.parse(inspect.getsource(p.execute)))
        for forbidden in ('development_media_030','get_object','demux','decode'):self.assertNotIn(forbidden,tree)
        folder=ROOT/('witness-gate-'+SUITE);folder.mkdir();j=p.Journal(folder/'integration_034',create=True,fixture=True)
        try:
            for event in ('HTTPS','TRANSPORT_SEND','BODY_DEBIT','MEDIA_COMPLETE'):
                with self.assertRaises(ValueError):j.add(event)
            j.once('GPU_QUERY','0')
            for key in ('0','1'):
                with self.assertRaises(ValueError):j.once('GPU_QUERY',key)
            with self.assertRaises(ValueError):p.require_ready(j)
            self.assertEqual(len(j.events('GPU_QUERY')),1)
        finally:j.close()
        MARKS['no_network']=True


def main():
    global ROOT,SUITE
    parser=argparse.ArgumentParser();parser.add_argument('root');parser.add_argument('suite');args=parser.parse_args()
    sys.stdin.readline();ROOT=Path(args.root);SUITE=args.suite
    j=p.Journal(ROOT);run=j.rows[0]['run_id'];j.reserve_output('witness-'+SUITE,32768,files=16);j.close()
    names=('test_shared_policy','test_closed_archive_and_direct_sha','test_resource_queue_score_binding','test_single_query_and_zero_media_gate')
    suite=unittest.TestSuite(SharedGPU034(n) for n in names);loaded=suite.countTestCases();started=time.monotonic()
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt=dict(contract_id='034',run_id=run,expected=4,loaded=loaded,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS,seconds=time.monotonic()-started)
    j=p.Journal(ROOT);j.write(SUITE+'-result.json',receipt);j.close();print(json.dumps(receipt))
    sys.exit(0 if result.wasSuccessful() and result.testsRun==4 else 1)


if __name__=='__main__':main()
