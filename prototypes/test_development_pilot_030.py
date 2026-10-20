"""New030 connection witnesses. Fictional data only; never imports old tests."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

from development_pilot_030 import (Journal, ExclusiveRead, Job, run_child, require, digest,
                                   score_allowed, SnapshotRaw, restored_plan, GIB)
from development_media_030 import SendGate, match_headers, proven_transport, transfer, install_transport
from temporal_evidence_adapter_025 import (ContractError, TASK, QuestionKey, QuestionRecord,
    SourceRecord, Projection, build_plan, select_four)
from temporal_evidence_scorer_025 import OneShotScorer, FrozenLedger, TerminalAttempt, ChildExitReceipt

ROOT = None
RUN = '1'


class MemoryJournal:
    def __init__(self):
        self.rows = []
    def events(self, event):
        return [r for r in self.rows if r['event'] == event]
    def add(self,event,**values):
        self.rows.append(dict(event=event,**values))
    def once(self,event,key,**values):
        require(not any(r.get('key')==key for r in self.events(event)), 'CONSUMED_NO_RETRY')
        self.add(event,key=key,**values)


def plan_fixture():
    sources=tuple(SourceRecord('fixture_'+str(i),()) for i in range(4))
    questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening a box did closing a box?',('a','b','c','d','e')) for s in sources)
    return build_plan(Projection('inference',sources,questions))


class Body:
    def __init__(self,data,declared):
        self.data=io.BytesIO(data);self._amount_read=0;self._raw_stream=self
        self.length_remaining=declared;self.reads=[]
    def read(self,size):
        self.reads.append(size);data=self.data.read(size);self._amount_read+=len(data);self.length_remaining-=len(data);return data


class Witnesses(unittest.TestCase):
    def fixture_child(self, code, seconds=5):
        journal=Journal(ROOT)
        number=len(journal.events('FIXTURE'))
        self.assertLess(number,12)
        journal.add('FIXTURE',key=str(number),seconds=seconds);journal.close()
        return run_child([sys.executable,'-I','-S','-B','-c','import sys;sys.stdin.readline();'+code],seconds,job_memory=GIB)

    def test_01_fixed_16_rotation(self):
        plan=plan_fixture();self.assertEqual(plan.n_planned,4)
        self.assertEqual([''.join(c.arm for c in plan.calls[i:i+4]) for i in range(0,16,4)],['ABCD','BCDA','CDAB','DABC'])

    def test_02_media_unavailable_retains_four_slots(self):
        plan=plan_fixture();rows=FrozenLedger(tuple(TerminalAttempt(c,'NOT_RUN') for c in plan.calls),True)
        data={s.source:{'benchmark_dataset':[{'correct_answer_label':'A'}]} for s in plan.sources}
        report=OneShotScorer().score(lambda:io.StringIO(json.dumps(data)),plan,rows,ChildExitReceipt(('fixture',),('fixture',),True))
        self.assertEqual(report.n_planned,4);self.assertTrue(all(a.not_run==4 and a.accuracy==0 for a in report.arms))
        self.assertTrue(all(p.both_wrong==4 for p in report.paired))

    def test_03_gold_early_zero_opens(self):
        count=[];plan=plan_fixture()
        with self.assertRaises(ContractError):
            OneShotScorer().score(lambda:count.append(1),plan,FrozenLedger((),False),ChildExitReceipt((),(),False))
        self.assertEqual(count,[])
        with self.assertRaises(ContractError):score_allowed([])

    def test_04_profile_binding_refuses_before_open(self):
        count=[];plan=plan_fixture();ledger=FrozenLedger(tuple(TerminalAttempt(c,'NOT_RUN') for c in plan.calls),True)
        with self.assertRaises(ContractError):
            OneShotScorer().score(lambda:count.append(1),plan,ledger,ChildExitReceipt(('x',),('x',),True),profile='SKIP_NONFINITE_028',expected_binding=('wrong','wrong'))
        self.assertEqual(count,[])

    def test_05_partial_snapshot_not_complete(self):
        path=Path(ROOT)/('suite-'+RUN+'-short.bin');j=Journal(ROOT);j.reserve_output(path.name,2);j.close();path.write_bytes(b'xx')
        raw=SnapshotRaw(open(path,'rb'),3);self.assertEqual(raw.read(),b'xx');self.assertNotEqual(raw.count,3);raw.close()

    def test_06_exact_headers(self):
        expected=dict(ContentLength=3,ETag='"fixture"',VersionId='v1')
        match_headers({'Content-Length':'3','ETag':'"fixture"','x-amz-version-id':'v1'},expected)
        for key,value in [('Content-Length','4'),('ETag','"different"'),('x-amz-version-id','v2')]:
            headers={'Content-Length':'3','ETag':'"fixture"','x-amz-version-id':'v1'};headers[key]=value
            with self.assertRaises(ContractError):match_headers(headers,expected)

    def test_07_send_failure_consumes(self):
        j=MemoryJournal();g=SendGate(j,'GetObject:P1','GET','https://fixture.example/bucket/key')
        g.reserve('GET','https://fixture.example/bucket/key')
        with self.assertRaises(ContractError):g.reserve('GET','https://fixture.example/bucket/key')
        self.assertEqual(len(j.events('HTTPS')),1)

    def test_08_send_exact_method_host_key_version(self):
        for method,url in [('HEAD','https://fixture.example/b/k?versionId=v'),('GET','http://fixture.example/b/k?versionId=v'),
                           ('GET','https://other.example/b/k?versionId=v'),('GET','https://fixture.example/b/x?versionId=v'),
                           ('GET','https://fixture.example/b/k?versionId=other')]:
            j=MemoryJournal();g=SendGate(j,'GetObject:P1','GET','https://fixture.example/b/k','v')
            with self.assertRaises(ContractError):g.reserve(method,url)
            self.assertEqual(j.rows,[])

    def test_09_sdk_low_level_binding(self):
        self.assertTrue(proven_transport('x.urlopen(retries=Retry(False),preload_content=False)'))
        self.assertFalse(proven_transport('x.urlopen(retries=Retry(1),preload_content=False)'))
        self.assertFalse(proven_transport('x.urlopen(retries=Retry(False),preload_content=True)'))

    def test_10_stream_debit_before_read_and_no_extra_read(self):
        j=MemoryJournal();body=Body(b'abc',3)
        class Destination(io.BytesIO):
            def fileno(self):return -1
        # Real fsync/file length path, no BytesIO bypass of file verification.
        path=Path(ROOT)/('suite-'+RUN+'-transfer.bin');ledger=Journal(ROOT);ledger.reserve_output(path.name,3);ledger.close()
        with open(path,'xb') as target:
            sha,count=transfer(body,target,dict(ContentLength=3),j,'P1')
        self.assertEqual(count,3);self.assertEqual(body.reads,[3]);self.assertEqual(j.events('BODY_DEBIT')[0]['amount'],3)

    def test_11_truncated_stream_no_refund(self):
        j=MemoryJournal();body=Body(b'',3)
        with self.assertRaises(ContractError):transfer(body,io.BytesIO(),dict(ContentLength=3),j,'P1')
        self.assertEqual(j.events('BODY_DEBIT')[0]['amount'],3)

    def test_12_full_denominator_bad_gold_unknown(self):
        plan=plan_fixture();ledger=FrozenLedger(tuple(TerminalAttempt(c,'RETURNED','A') for c in plan.calls),True)
        report=OneShotScorer().score(lambda:io.StringIO('{}'),plan,ledger,ChildExitReceipt(('x',),('x',),True))
        self.assertEqual(report.n_planned,4);self.assertIsNone(report.paired);self.assertTrue(all(a.accuracy is None for a in report.arms))

    def test_13_oom_no_restart_or_answer_replay(self):
        j=MemoryJournal();j.once('MODEL_LAUNCH','gpu');j.once('STARTED','0');j.add('OOM')
        with self.assertRaises(ContractError):j.once('MODEL_LAUNCH','gpu')
        with self.assertRaises(ContractError):j.once('STARTED','0')

    def test_14_selectors_same_budget_different_order(self):
        pts=list(range(48));q=[0.0]*48;a=[0.0]*48;b=[0.0]*48;a[40]=1.;b[3]=1.
        arms=select_four(pts,q,a,b)
        self.assertTrue(all(len(s.indices)==12 and len(set(s.indices))==12 and list(s.indices)==sorted(s.indices) for s in arms))
        self.assertEqual(arms[2].event_pair,(40,3));self.assertLess(*arms[3].event_pair)

    def test_15_windows_canary_refusal_release_independent_score(self):
        plan=plan_fixture();data={s.source:{'benchmark_dataset':[{'correct_answer_label':'A','unretained':None}]} for s in plan.sources}
        path=Path(ROOT)/('suite-'+RUN+'-canary.json');j=Journal(ROOT);j.write(path.name,data);j.close()
        handle=ExclusiveRead(path)
        try:
            code='import json;\ntry:\n f=open('+repr(str(path))+',"rb");f.close();print("OPENED")\nexcept OSError as e:print(getattr(e,"winerror",None))'
            result=self.fixture_child(code);self.assertEqual(result['exit_code'],0);self.assertEqual(result['stdout'].strip(),'32')
        finally:handle.close()
        fake_model=self.fixture_child('import json;print(json.dumps(["A"]*16))')
        self.assertEqual(fake_model['exit_code'],0);self.assertEqual(fake_model['job_active'],0)
        self.assertEqual(len(json.loads(fake_model['stdout'])),16)
        # A distinct CPU PID performs the complete fictional four-arm score.
        code=('sys.path.insert(0,'+repr(str(Path(__file__).parent))+');'
              'from test_development_pilot_030 import plan_fixture;from temporal_evidence_scorer_025 import *;'
              'p=plan_fixture();l=FrozenLedger(tuple(TerminalAttempt(c,"RETURNED","A") for c in p.calls),True);'
              'r=OneShotScorer().score(lambda:open('+repr(str(path))+',encoding="utf-8"),p,l,ChildExitReceipt(('+repr(str(fake_model['pid']))+',),('+repr(str(fake_model['pid']))+',),True));'
              'assert r.n_planned==4 and all(a.correct_known==4 for a in r.arms);print("SCORED_N4_16")')
        result=self.fixture_child(code);self.assertEqual(result['exit_code'],0,result['stderr']);self.assertEqual(result['stdout'].strip(),'SCORED_N4_16')

    def test_16_job_timeout_healthy_peer(self):
        # Peer belongs to another Job and must survive termination of our timed Job.
        j=Journal(ROOT);number=len(j.events('FIXTURE'));self.assertLess(number,12);j.add('FIXTURE',key=str(number),seconds=5);j.close()
        peer_job=Job(GIB);peer=subprocess.Popen([sys.executable,'-I','-S','-B','-c','import sys,time;sys.stdin.readline();time.sleep(1);print("HEALTHY")'],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=0x08000000,close_fds=True)
        try:
            peer_job.assign(peer);peer.stdin.write(b'go\n');peer.stdin.flush();peer.stdin.close()
            result=self.fixture_child('import time;time.sleep(10)',seconds=.15)
            self.assertNotEqual(result['exit_code'],0);self.assertEqual(result['job_active'],0)
            peer.wait(timeout=4);self.assertEqual(peer.returncode,0);self.assertEqual(peer.stdout.read().strip(),b'HEALTHY')
            self.assertEqual(peer_job.active(),0)
        finally:
            if peer.poll() is None:peer_job.kill();peer.wait(timeout=2)
            peer_job.close()

    def test_17_persistent_chain_reopen_and_once(self):
        j=Journal(ROOT);j.once('SUITE_WITNESS','reopen-'+RUN);sig=j.rows[-1]['hash'];j.close()
        j=Journal(ROOT)
        try:
            self.assertEqual(j.events('SUITE_WITNESS')[-1]['hash'],sig)
            with self.assertRaises(ContractError):j.once('SUITE_WITNESS','reopen-'+RUN)
        finally:j.close()

    def test_18_head_unexpected_body_closed_without_read(self):
        from types import SimpleNamespace as NS
        class Raw:
            length_remaining=1;chunked=False;closed=False;reads=0
            def read(self,*a,**k):self.reads+=1;raise AssertionError('body read')
            def close(self):self.closed=True
        raw=Raw();response=NS(raw=raw,status_code=200,headers={})
        class Events:
            def register_first(self,event,handler,**kw):self.handler=handler
        events=Events();client=NS(meta=NS(events=events),_endpoint=NS(http_session=NS(send=lambda request:response)))
        j=MemoryJournal();gate=SendGate(j,'HeadObject:P1','HEAD','https://fixture.example/b/k')
        install_transport(client,gate,{},'x.urlopen(retries=Retry(False),preload_content=False)')
        request=NS(method='HEAD',url='https://fixture.example/b/k',headers={})
        events.handler(request)
        with self.assertRaises(ContractError):client._endpoint.http_session.send(request)
        self.assertTrue(raw.closed);self.assertEqual(raw.reads,0);self.assertEqual(len(j.events('HTTPS')),1)


if __name__=='__main__':
    sys.stdin.readline()
    ROOT=sys.argv[1];RUN=sys.argv[2] if len(sys.argv)>2 else '1';sys.argv=sys.argv[:1]
    unittest.main(verbosity=2)
