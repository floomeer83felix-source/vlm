"""036 reference bytes, independent synthetic role, tested-policy recovery deltas."""
import argparse
import ast
import copy
from dataclasses import asdict
import hashlib
import inspect
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

import development_pilot_030 as p
import development_worker_030 as w
from temporal_evidence_adapter_025 import (TASK,Projection,SourceRecord,QuestionRecord,QuestionKey,build_plan)

ROOT=None
SUITE=None
MARKS={}


class MemoryJournal:
    def __init__(self,rows=None):self.rows=rows or [];self.saved={};self.opens=0
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**fields):
        row=dict(seq=len(self.rows),event=event,**fields);row['hash']=p.digest(row);self.rows.append(row)
    def once(self,event,key,**fields):
        p.require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY');self.add(event,key=key,**fields)
    def write(self,name,value):self.saved[name]=value
    def input(self,alias,path,category):
        self.opens+=1;self.add('INPUT',category=category)
        return self.body
    def close(self):pass


def chain(rows):
    out=[]
    for value in rows:
        row=dict(value,seq=len(out),prev=out[-1]['hash'] if out else '0'*64);row['hash']=p.digest(row);out.append(row)
    return b''.join(p.packed(r)+b'\n' for r in out)


def archive_fixture():
    rows=[dict(event='RUN',contract_id='035',root_name='integration_035',purpose='REAL_035',run_id='closed-fictional')]
    rows.append(dict(event='SUITE_RESULT',contract_id='035',run_id='closed-fictional',passed=True,expected=5,loaded=5,tests=5,failures=0,errors=0,skips=0))
    rows.extend([dict(event='FRAME_CACHE_VERIFIED',size=144,sha256='fake-frame',rgb_hashes=48),dict(event='INPUT_COMPLETE',alias='frame-cache',size=144,sha256='fake-frame'),dict(event='OUTPUT',key='P2-frames.npy',size=144),dict(event='PHASE_EXIT',name='prepare',code=1,job_active=0),dict(event='PHASE_EXIT',name='copy-frames',code=0,job_active=0),dict(event='NO_MODEL_QUEUE_CLOSED')])
    rows.extend(dict(event='TERMINAL',key=str(n),state='NOT_RUN') for n in range(16));rows.append(dict(event='RUN_STOPPED'))
    return rows


def score_fixture():
    sources=tuple(SourceRecord('fixture_%d'%n,()) for n in range(4));questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening did closing?',tuple('abcde')) for s in sources)
    plan=build_plan(Projection('inference',sources,questions));config=dict(slots=[dict(slot=n,alias='P%d'%(n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)])
    queue=dict(contract_id='036',run_id='fresh-fictional',plan_hash=p.digest(asdict(plan)),worker_hash=p.digest(config),slots=config['slots'],available=p.AVAILABLE_036)
    j=MemoryJournal([dict(event='RUN',contract_id='036',run_id='fresh-fictional')]);j.add('FROZEN',plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash'])
    data={'queue.json':queue,'worker-input.json':config,'current-annotation-reference.json':dict(identity=[2,3])};resource=dict(hash='resource-fixture')
    for attempt in (1,2):
        j.add('SUITE_RESULT',passed=True,code_hash='fixture-code-%d'%attempt,policy_id=attempt,policy_hash='fixture-policy-%d'%attempt)
        j.add('MODEL_LAUNCH',attempt=attempt,run_id='fresh-fictional',queue_hash=p.digest(queue),resource_hash=resource['hash'],code_hash='fixture-code-%d'%attempt,policy=attempt,policy_hash='fixture-policy-%d'%attempt)
        actual=dict(pid=120+attempt,job_active=0,exit_code=0,seconds=.1);data['gpu-worker-%d-exit-private.json'%attempt]=actual
        with patch.object(p,'load',side_effect=lambda root,name:data[name]):p.record_model_exit_036(ROOT,j,attempt,actual)
    for item in config['slots']:
        if item['alias']=='P2':j.add('STARTED',key=str(item['slot']),alias='P2',arm=item['arm'],attempt=2)
        j.add('TERMINAL',key=str(item['slot']),alias=item['alias'],arm=item['arm'],state='RETURNED' if item['alias']=='P2' else 'NOT_RUN')
    with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_036',return_value=resource):p.close_model_queue(ROOT,j)
    return j,plan,data,resource


class ReferenceStartup036(unittest.TestCase):
    def test_bounded_metadata_and_pure_bytes(self):
        info=NS(st_dev=1,st_ino=2)
        self.assertEqual(p.unique_reference_036([('first',info),('alias',info)])[1],info)
        with self.assertRaises(ValueError):p.unique_reference_036([])
        with self.assertRaises(ValueError):p.unique_reference_036([('a',info)],True)
        with self.assertRaises(ValueError):p.unique_reference_036([('a',info),('b',NS(st_dev=1,st_ino=3))])
        j=MemoryJournal();probe=p.ReferenceMetadata036(j)
        with patch.object(Path,'lstat',side_effect=FileNotFoundError(2,'fake')):
            for n in range(32):self.assertIsNone(probe.stat(ROOT/str(n)))
            with self.assertRaises(ValueError):probe.stat(ROOT/'33')
        # Invalid UTF8/non-JSON bytes are hashed without decoding or gold extraction.
        raw=b'fictional invalid JSON \xff';snapshot=dict(size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1'])
        candidate=dict(path=str(ROOT/'fictional-input'),size=len(raw),identity=[5,6],mtime_ns=7)
        meta=NS(st_dev=5,st_ino=6,st_size=len(raw),st_mtime_ns=7)
        for correct in (True,False):
            j=MemoryJournal();j.body=raw if correct else raw[:-1];data={'reference-candidate-private.json':candidate,'frozen-snapshot-032.json':snapshot}
            with patch.object(p,'Journal',return_value=j),patch.object(p,'require_ready'),patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'checked_path',return_value=(Path(candidate['path']),meta)):
                p.reference_hash_036(ROOT);self.assertEqual(j.opens,1)
                with self.assertRaises(ValueError):j.once('ANNOTATION_HASH_CONSUMED','one')
            self.assertEqual(bool(j.events('ANNOTATION_REFERENCE_BOUND')),correct)
            if correct:self.assertEqual(j.saved['current-annotation-reference.json']['identity'],[5,6])
        MARKS['reference_bytes']=True

    def test_synthetic_independent_and_no_real_gate(self):
        source=inspect.getsource(w.bootstrap)
        self.assertIn('synthetic-startup-config.json',source);self.assertIn('np.zeros',source);self.assertNotIn("load(root,'P2-candidates.json')",source)
        for forbidden in ('mem_get_info','is_available','model.generate','SiglipModel.from_pretrained','Qwen3VLForConditionalGeneration.from_pretrained'):self.assertNotIn(forbidden,source)
        with self.assertRaises(ValueError):p.require_synthetic_036(ROOT,[],1)
        with self.assertRaises(ValueError):p.current_reference_036(ROOT,[])
        diag=w.StartupDiagnostic()
        before=w.install_policy(ROOT,[],diag,install=False)
        with self.assertRaises(PermissionError):before('open',(os.devnull,'r',0))
        fixed=w.install_policy(ROOT,[],diag,install=False,allow_null_device=True)
        fixed('open',(os.devnull,'r',0));fixed('open',(os.devnull,'wb',os.O_WRONLY))
        fixed('open',(os.fsencode(str(ROOT/'temporary-owned')),'wb',os.O_WRONLY))
        with self.assertRaises(PermissionError):fixed('open',(os.fsencode(str(ROOT.parent/'outside-bytes')),'r',0))
        with self.assertRaises(PermissionError):fixed('open',(str(ROOT.parent/'not-allowed'),'r',0))
        with self.assertRaises(PermissionError):fixed('subprocess.Popen',('not-retained',))
        MARKS['synthetic_role']=True

    def test_missing_prepare_archive(self):
        rows=archive_fixture();raw=chain(rows);self.assertEqual(len(p.archive_035_rows(raw)),len(rows))
        for bad in (raw[:-1],raw.replace(b'closed-fictional',b'bad-fictional',1),chain(rows[:-1])):
            with self.assertRaises(ValueError):p.archive_035_rows(bad)
        for extra in (dict(event='MODEL_LAUNCH'),dict(event='INPUT',category='gold')):
            with self.assertRaises(ValueError):p.archive_035_rows(chain(rows[:-1]+[extra,rows[-1]]))
        MARKS['archive_035']=True

    def test_post_request_tested_policy_and_replay(self):
        binding=dict(code_hash='current-code',policy_id=2,policy_hash='new-policy',science_hash='frozen-science')
        request=dict(seq=10,request_hash='request-fixture');suite=dict(event='SUITE_RESULT',seq=11,hash='suite-fixture',passed=True,**binding)
        response=dict(action='CONTINUE',request_hash=request['request_hash'],suite_hash=suite['hash'],suite_seq=11,**binding)
        self.assertEqual(p.accept_repair_036([suite],request,response,binding),2)
        for change in ({'seq':9},{'code_hash':'old-code'},{'policy_id':1},{'passed':False}):
            altered=dict(suite,**change)
            with self.assertRaises(ValueError):p.accept_repair_036([altered],request,response,binding)
        with self.assertRaises(ValueError):p.accept_repair_036([suite,dict(event='REPAIR_ACCEPTED',request_hash=request['request_hash'])],request,response,binding)
        tree=ast.dump(ast.parse(inspect.getsource(p.execute)));self.assertIn('policy',tree);self.assertIn('wait_repair_036',tree)
        MARKS['repair_binding']=True

    def test_all_exit_current_binding_and_no_network(self):
        j,plan,data,resource=score_fixture()
        with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_036',return_value=resource),patch.object(p,'restored_plan',return_value=plan),patch.object(p,'current_reference_036',return_value=data['current-annotation-reference.json']):
            p.score_allowed(j.rows,ROOT)
            missing=[r for r in j.rows if not(r['event']=='MODEL_EXIT' and r['attempt']==1)]
            with self.assertRaises(ValueError):p.score_allowed(missing,ROOT)
        j.events('STARTED')[0]['attempt']=3
        with patch.object(p,'Journal',return_value=j),patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_036',return_value=resource),patch.object(p,'restored_plan',return_value=plan),patch.object(p,'current_reference_036',return_value=data['current-annotation-reference.json']),patch('builtins.open') as opener:
            p.score(ROOT);self.assertEqual(opener.call_count,0)
        folder=ROOT/('witness-'+SUITE);folder.mkdir();actual=p.Journal(folder/'integration_036',create=True,fixture=True)
        try:
            with self.assertRaises(ValueError):actual.add('HTTPS')
            with self.assertRaises(ValueError):p.require_ready(actual)
        finally:actual.close()
        MARKS['all_exit']=True


def main():
    global ROOT,SUITE
    parser=argparse.ArgumentParser();parser.add_argument('root');parser.add_argument('suite');args=parser.parse_args();sys.stdin.readline()
    ROOT=Path(args.root);SUITE=args.suite;j=p.Journal(ROOT);run=j.rows[0]['run_id'];j.reserve_output('witness-'+SUITE,16384,files=8);j.close()
    binding=p.tested_binding_036(ROOT);names=('test_bounded_metadata_and_pure_bytes','test_synthetic_independent_and_no_real_gate','test_missing_prepare_archive','test_post_request_tested_policy_and_replay','test_all_exit_current_binding_and_no_network')
    suite=unittest.TestSuite(ReferenceStartup036(n) for n in names);loaded=suite.countTestCases();start=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt=dict(contract_id='036',run_id=run,expected=5,loaded=loaded,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS,seconds=time.monotonic()-start,**binding)
    j=p.Journal(ROOT);j.write(SUITE+'-result.json',receipt);j.close();print(json.dumps({k:v for k,v in receipt.items() if k not in binding}));sys.exit(0 if result.wasSuccessful() and result.testsRun==5 else 1)


if __name__=='__main__':main()
