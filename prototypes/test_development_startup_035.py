"""035 startup diagnostics, limited recovery/all-exit delta; no old tests/ML."""
import argparse
import ast
import copy
from dataclasses import asdict
import inspect
import json
import os
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

import development_pilot_030 as p
import development_worker_030 as w
from temporal_evidence_adapter_025 import (TASK,Projection,SourceRecord,QuestionRecord,QuestionKey,build_plan)

ROOT=None
SUITE=None
MARKS={}


class MemoryJournal:
    def __init__(self,rows=None):self.rows=rows or [];self.saved={}
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**fields):
        row=dict(event=event,**fields);row['hash']=p.digest(row);self.rows.append(row)
    def once(self,event,key,**fields):
        p.require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY');self.add(event,key=key,**fields)
    def write(self,name,value):self.saved[name]=value
    def close(self):pass


def chained(rows):
    out=[]
    for value in rows:
        row=dict(value,seq=len(out),prev=out[-1]['hash'] if out else '0'*64);row['hash']=p.digest(row);out.append(row)
    return b''.join(p.packed(r)+b'\n' for r in out)


def closed034():
    rows=[dict(event='RUN',contract_id='034',root_name='integration_034',purpose='REAL_034',run_id='old-fixture')]
    rows.append(dict(event='SUITE_RESULT',passed=True,contract_id='034',run_id='old-fixture',expected=4,loaded=4,tests=4,failures=0,errors=0,skips=0))
    for event in ('GPU_QUERY','RESOURCE_ADMITTED','MODEL_LAUNCH','WORKER_ENTERED','QUEUE_CLOSED'):rows.append(dict(event=event))
    rows.extend([dict(event='FRAME_CACHE_VERIFIED',size=144,sha256='fixture-sha',rgb_hashes=48),
                 dict(event='INPUT_COMPLETE',alias='frame-cache',size=144,sha256='fixture-sha'),dict(event='OUTPUT',key='P2-frames.npy',size=144),
                 dict(event='WORKER_FAILURE',stage='SETUP',reason='PermissionError'),dict(event='MODEL_EXIT',job_active=0)])
    rows.extend(dict(event='TERMINAL',key=str(n),state='NOT_RUN') for n in range(16));rows.append(dict(event='RUN_STOPPED'))
    return rows


def score_fixture(count=2):
    sources=tuple(SourceRecord('fixture_%d'%n,()) for n in range(4))
    questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening did closing?',tuple('abcde')) for s in sources)
    plan=build_plan(Projection('inference',sources,questions));config=dict(slots=[dict(slot=n,alias='P%d'%(n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)])
    queue=dict(contract_id='035',run_id='fresh-fixture',plan_hash=p.digest(asdict(plan)),worker_hash=p.digest(config),slots=config['slots'],available=p.AVAILABLE_035)
    j=MemoryJournal([dict(event='RUN',contract_id='035',run_id='fresh-fixture')]);j.add('FROZEN',plan_hash=queue['plan_hash'],worker_hash=queue['worker_hash'])
    j.add('GPU_ENVELOPE',deadline=time.time()+900);resource=dict(hash='fixture-resource')
    data={'queue.json':queue,'worker-input.json':config}
    for attempt in range(1,count+1):
        j.add('MODEL_LAUNCH',attempt=attempt,run_id='fresh-fixture',queue_hash=p.digest(queue),resource_hash=resource['hash'],code_hash='fixture-code')
        actual=dict(pid=120+attempt,job_active=0,exit_code=0,seconds=.1);data['gpu-worker-%d-exit-private.json'%attempt]=actual
        with patch.object(p,'load',side_effect=lambda root,name:data[name]):p.record_model_exit_035(ROOT,j,attempt,actual)
    for slot in config['slots']:
        if slot['alias']=='P2':j.add('STARTED',key=str(slot['slot']),alias='P2',arm=slot['arm'],attempt=count)
        j.add('TERMINAL',key=str(slot['slot']),alias=slot['alias'],arm=slot['arm'],state='RETURNED' if slot['alias']=='P2' else 'NOT_RUN')
    with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_035',return_value=resource):p.close_model_queue(ROOT,j)
    return j,plan,data,resource


class Startup035(unittest.TestCase):
    def test_diagnostic_policy_no_recursion(self):
        diag=w.StartupDiagnostic();diag.set('TORCH_IMPORT')
        exact=str(ROOT/'runtime-single.txt');audit=w.install_policy(ROOT,[],diag,[exact],install=False)
        with patch('builtins.open',side_effect=AssertionError('recursive IO')),patch.object(Path,'resolve',side_effect=AssertionError('resolve')):
            for event,args in [('socket.connect',('secret-not-retained',)),('subprocess.Popen',('secret-not-retained',)),('open',(str(ROOT.parent/'blocked'),'r',0))]:
                with self.assertRaises(PermissionError):audit(event,args)
            audit('open',(exact,'r',0));audit('open',(str(ROOT/'owned'),'w',os.O_WRONLY|os.O_CREAT))
        self.assertNotIn('secret-not-retained',json.dumps(diag.denials));self.assertEqual(diag.denials[-1]['stage'],'TORCH_IMPORT')
        for n in range(25):
            with self.assertRaises(PermissionError):diag.deny('open','DENY','x'*1000)
        self.assertLessEqual(len(diag.denials),16);self.assertLessEqual(diag.denial_bytes,8192)
        try:raise OSError(13,'fictional')
        except OSError as error:receipt=diag.error(error)
        self.assertEqual(receipt['errno'],13);self.assertLessEqual(len(receipt['frames']),32)
        self.assertNotIn('locals',json.dumps(receipt))
        MARKS['startup_policy']=True

    def test_cpu_bootstrap_same_policy(self):
        source=inspect.getsource(w.bootstrap);startup=inspect.getsource(w.startup)
        self.assertIn('startup(root,config',source);self.assertIn('install_policy(root',startup)
        for forbidden in ('cuda.is_available','cuda.mem_get_info','generate(','SiglipModel.from_pretrained','Qwen3VLForConditionalGeneration.from_pretrained'):
            self.assertNotIn(forbidden,source+startup)
        self.assertIn('CPU_COMPLETE',source);self.assertIn('324',source);self.assertIn('is_initialized',source)

    def test_archive_with_real_failed_launch(self):
        rows=closed034();raw=chained(rows);self.assertEqual(len(p.archive_034_rows(raw)),len(rows))
        for bad in (raw[:-1],raw.replace(b'old-fixture',b'bad-fixture',1),chained(rows[:-1])):
            with self.assertRaises(ValueError):p.archive_034_rows(bad)
        for extra in (dict(event='STARTED'),dict(event='INPUT',category='gold')):
            with self.assertRaises(ValueError):p.archive_034_rows(chained(rows[:-1]+[extra,rows[-1]]))
        MARKS['archive_034']=True

    def test_two_attempt_all_exit_and_restart(self):
        j,plan,data,resource=score_fixture()
        with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_035',return_value=resource),patch.object(p,'restored_plan',return_value=plan):
            p.score_allowed(j.rows,ROOT)
            noexit=[r for r in j.rows if not(r['event']=='MODEL_EXIT' and r['attempt']==1)]
            with self.assertRaises(ValueError):p.score_allowed(noexit,ROOT)
        # Before any QA/closure a validated first exit plus repair can authorize only attempt2.
        j.rows=[r for r in j.rows if r['event'] not in ('STARTED','TERMINAL','QUEUE_CLOSED') and not(r['event'] in ('MODEL_LAUNCH','MODEL_EXIT') and r['attempt']==2)]
        j.add('REPAIR_ACCEPTED',key='GPU-1',code_hash='fixture-code')
        with patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'code_version_035',return_value='fixture-code'):
            p.validate_launch_035(j.rows,ROOT,dict(attempt=2,code_hash='fixture-code'))
            j.add('STARTED',key='4')
            with self.assertRaises(ValueError):p.validate_launch_035(j.rows,ROOT,dict(attempt=2,code_hash='fixture-code'))
            with self.assertRaises(ValueError):p.validate_launch_035(j.rows,ROOT,dict(attempt=3,code_hash='fixture-code'))
        MARKS['recovery']=True

    def test_score_mismatch_opener_zero_and_no_network(self):
        for fault in ('exit','queue','attempt'):
            j,plan,data,resource=score_fixture()
            if fault=='exit':data['gpu-worker-1-exit-private.json']['pid']=999
            elif fault=='queue':data['queue.json']['available']['P1']=True
            else:j.events('STARTED')[0]['attempt']=3
            with patch.object(p,'Journal',return_value=j),patch.object(p,'load',side_effect=lambda root,name:data[name]),patch.object(p,'resource_receipt_035',return_value=resource),patch.object(p,'restored_plan',return_value=plan),patch('builtins.open') as opener:
                p.score(ROOT);self.assertEqual(opener.call_count,0)
            self.assertEqual(len(j.events('SCORE_CONSUMED')),1)
        folder=ROOT/('witness-gate-'+SUITE);folder.mkdir();j=p.Journal(folder/'integration_035',create=True,fixture=True)
        try:
            for event in ('HTTPS','BODY_DEBIT','TRANSPORT_SEND','MEDIA_COMPLETE'):
                with self.assertRaises(ValueError):j.add(event)
        finally:j.close()
        tree=ast.dump(ast.parse(inspect.getsource(p.wait_repair_035)));self.assertNotIn('eval',tree);self.assertNotIn('subprocess',tree)
        MARKS['bindings_035']=True;MARKS['no_network']=True


def main():
    global ROOT,SUITE
    parser=argparse.ArgumentParser();parser.add_argument('root');parser.add_argument('suite');args=parser.parse_args()
    sys.stdin.readline();ROOT=Path(args.root);SUITE=args.suite
    j=p.Journal(ROOT);run=j.rows[0]['run_id'];j.reserve_output('witness-'+SUITE,16384,files=8);j.close()
    names=('test_diagnostic_policy_no_recursion','test_cpu_bootstrap_same_policy','test_archive_with_real_failed_launch','test_two_attempt_all_exit_and_restart','test_score_mismatch_opener_zero_and_no_network')
    suite=unittest.TestSuite(Startup035(n) for n in names);loaded=suite.countTestCases();start=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
    receipt=dict(contract_id='035',run_id=run,expected=5,loaded=loaded,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS,seconds=time.monotonic()-start)
    j=p.Journal(ROOT);j.write(SUITE+'-result.json',receipt);j.close();print(json.dumps(receipt));sys.exit(0 if result.wasSuccessful() and result.testsRun==5 else 1)


if __name__=='__main__':main()
