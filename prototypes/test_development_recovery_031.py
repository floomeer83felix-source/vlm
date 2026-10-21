"""031 new combined witnesses: actual Windows gates, fictional research data.

Explicit loader only. Never imports/replays030 or any historical test module.
"""
import ast
from dataclasses import asdict
import hashlib
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace as NS
import sys
import time
import unittest

from development_pilot_030 import (Journal, ExclusiveRead, zero_body_observation, run_child,
    python_command, packed, digest, archive_rows, recover_pretty_input, restored_plan,
    make_queue, close_model_queue, score_allowed, load, require, GIB)
from development_media_030 import SendGate, install_transport, transfer
from temporal_evidence_adapter_025 import (ContractError, TASK, QuestionKey, QuestionRecord,
    SourceRecord, Projection, build_plan)

ROOT=None
SUITE=None
MARKS={}
EXPECTED=7


class MemoryJournal:
    def __init__(self):self.rows=[]
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**values):self.rows.append(dict(event=event,**values))
    def once(self,event,key,**values):
        require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY')
        self.add(event,key=key,**values)


class Recovery(unittest.TestCase):
    def child(self,command,descendants=0,work=None):
        j=Journal(ROOT)
        for _ in range(1+descendants):
            number=len(j.events('FIXTURE_PID'));self.assertLess(number,24)
            j.add('FIXTURE_PID',key=str(number),seconds=3)
        j.close()
        result=run_child(command,3,job_memory=GIB,work_seconds=work)
        self.assertLessEqual(result['seconds'],3)
        self.assertEqual(result['job_active'],0)
        return result

    def code_child(self,code,**kw):
        return self.child([sys.executable,'-I','-S','-B','-c','import sys;sys.stdin.readline();'+code],**kw)

    def tree(self,label):
        name='witness-'+SUITE+'-'+label
        j=Journal(ROOT);j.reserve_output(name+'-tree-budget',192*1024,files=24);j.close()
        parent=Path(ROOT)/name;parent.mkdir()
        return parent/'integration_031'

    def score_tree(self,label,broken=False):
        root=self.tree(label);j=Journal(root,create=True,fixture=True)
        sources=tuple(SourceRecord('fixture_'+str(i),()) for i in range(4))
        questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,
            'How long after opening a box did closing a box?',('one','two','three','four','five')) for s in sources)
        projection=Projection('inference',sources,questions);plan=build_plan(projection)
        slots=[dict(slot=n,alias='P%d' % (n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)]
        config=dict(slots=slots,sources=[dict(alias='P%d' % (i+1)) for i in range(4)],fixture=True)
        j.write('nongold.json',dict(binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1'],projection=asdict(projection)))
        j.write('worker-input.json',config)
        j.add('FROZEN',n=4,options=20,slots=16,plan_hash=digest(asdict(plan)),worker_hash=digest(config))
        queue=make_queue(root,j,{s['alias']:True for s in slots})
        data={s.source:{'benchmark_dataset':[dict(correct_answer_label='A')]} for s in sources}
        full=packed(data);raw=full[:-2] if broken else full
        canary=root/'fictional-canary.json';j.reserve_output(canary.name,len(raw))
        with open(canary,'xb') as f:f.write(raw)
        stat=canary.stat()
        j.write('annotation-reference.json',dict(path=str(canary),identity=[stat.st_dev,stat.st_ino],size=stat.st_size,mtime_ns=stat.st_mtime_ns))
        j.write('expected-snapshot.json',dict(binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1'],size=len(raw),sha256=hashlib.sha256(full).hexdigest()))
        j.once('MODEL_LAUNCH','gpu',run_id=j.rows[0]['run_id'],queue_hash=digest(queue));j.close()
        fake=self.code_child('import json;print(json.dumps(["A"]*16))')
        self.assertEqual(fake['exit_code'],0)
        predictions=json.loads(fake['stdout']);self.assertEqual(len(predictions),16)
        j=Journal(root)
        for slot,prediction in zip(slots,predictions):
            j.once('STARTED',str(slot['slot']),alias=slot['alias'],arm=slot['arm'])
            j.once('TERMINAL',str(slot['slot']),alias=slot['alias'],arm=slot['arm'],state='RETURNED',prediction=prediction)
        close_model_queue(root,j,fake);j.close()
        return root

    def test_01_native_and_python_share_refusal_then_release(self):
        name='witness-'+SUITE+'-canary.json';j=Journal(ROOT);j.write(name,dict(fictional=True));j.close()
        path=Path(ROOT)/name;handle=ExclusiveRead(path)
        try:
            result=self.child(python_command(sys.executable,'development_pilot_030','probe',str(path)))
            self.assertEqual(result['exit_code'],0);observed=json.loads(result['stdout'])
            self.assertEqual(observed['native']['winerror'],32);self.assertFalse(observed['native']['opened'])
            self.assertFalse(observed['python']['opened']);self.assertTrue(observed['denied'])
            self.assertEqual(observed['native']['body_bytes']+observed['python']['body_bytes'],0)
            MARKS['win32_sharing']=True
        finally:handle.close()
        released=self.child(python_command(sys.executable,'development_pilot_030','probe',str(path)))
        observed=json.loads(released['stdout']);self.assertEqual(released['exit_code'],0)
        self.assertTrue(observed['native']['opened'] and observed['python']['opened']);self.assertFalse(observed['denied'])
        self.assertEqual(observed['native']['body_bytes']+observed['python']['body_bytes'],0)
        missing=zero_body_observation(Path(ROOT)/('witness-'+SUITE+'-nonexistent'))
        self.assertFalse(missing['denied']);self.assertEqual(missing['native']['winerror'],2)
        MARKS['release_open']=True

    def test_02_bounded_natural_peer_and_owned_descendant(self):
        peer=self.code_child('import time;time.sleep(.02);print("HEALTHY")')
        self.assertEqual(peer['exit_code'],0);self.assertEqual(peer['stdout'].strip(),'HEALTHY');self.assertFalse(peer['killed'])
        MARKS['healthy_job_empty']=True
        # Parent returns while a real descendant remains in its inherited Job.
        code='import subprocess;p=subprocess.Popen([sys.executable,"-I","-S","-B","-c","import time;time.sleep(10)"]);print(p.pid)'
        child=self.code_child(code,descendants=1,work=.5)
        self.assertTrue(child['stdout'].strip().isdigit());self.assertTrue(child['killed']);self.assertEqual(child['job_active'],0)
        MARKS['descendant_empty']=True

    def test_03_production_score_exit_binding_and_truncation(self):
        root=self.score_tree('score-ok');j=Journal(root);score_allowed(j.rows,root)
        rows=[dict(r) for r in j.rows];j.close()
        for field in ('job_active','run_id','launch_hash'):
            modified=[dict(r) for r in rows]
            next(r for r in modified if r['event']=='MODEL_EXIT')[field]=1 if field=='job_active' else 'wrong'
            with self.assertRaises(ContractError):score_allowed(modified,root)
        duplicated=rows+[dict(next(r for r in rows if r['event']=='TERMINAL'))]
        with self.assertRaises(ContractError):score_allowed(duplicated,root)
        no_exit=[r for r in rows if r['event']!='MODEL_EXIT']
        with self.assertRaises(ContractError):score_allowed(no_exit,root)
        result=self.child(python_command(sys.executable,'development_pilot_030','score',str(root)))
        self.assertEqual(result['exit_code'],0,result['stderr'])
        report=load(root,'score-anonymous.json');self.assertEqual(report['status'],'PASS');self.assertEqual(report['n_planned'],4)
        self.assertTrue(all(a['correct_known']==4 for a in report['arms']))
        j=Journal(root);self.assertEqual(len(j.events('SCORE_CONSUMED')),1);self.assertEqual(len(j.events('SCORED')),1)
        self.assertTrue(j.events('SCORED')[0]['raw_binding']);j.close();MARKS['independent_score']=True
        broken=self.score_tree('score-truncated',broken=True)
        result=self.child(python_command(sys.executable,'development_pilot_030','score',str(broken)))
        self.assertEqual(result['exit_code'],0);self.assertFalse((broken/'score-anonymous.json').exists())
        j=Journal(broken);self.assertEqual(len(j.events('SCORE_CONSUMED')),1);self.assertEqual(len(j.events('SCORED')),0)
        self.assertEqual(sum(r['category']=='gold' for r in j.events('INPUT')),1);j.close()

    def test_04_expired_archive_cache_bytes_not_resumed(self):
        rows=[]
        def add(event,**fields):
            r=dict(seq=len(rows),prev=rows[-1]['hash'] if rows else '0'*64,event=event,**fields);r['hash']=digest(r);rows.append(r)
        add('RUN',epoch=0,run_id='fictional-old')
        add('RUN_STOPPED',key='030')
        for n in range(16):add('TERMINAL',key=str(n),state='NOT_RUN')
        raw=b''.join(packed(r)+b'\n' for r in rows)
        self.assertEqual(archive_rows(raw)[0]['epoch'],0)
        with self.assertRaises(ContractError):archive_rows(raw[:-1])
        with self.assertRaises(ContractError):archive_rows(raw.replace(b'fictional-old',b'changed-runxx'))
        with self.assertRaises(ContractError):Journal(Path(ROOT).parent/'integration_030')
        data=dict(binding=['SKIP_NONFINITE_028','PROJECTOR_028_V1'],keys=[dict(source='fixture_source',index=0)])
        old=json.dumps(data,ensure_ascii=True,indent=2,allow_nan=False).encode();cache=packed(data)
        candidates=list(recover_pretty_input('keys',json.loads(cache),{}))
        self.assertIn(old,candidates);self.assertNotEqual(hashlib.sha256(old).hexdigest(),hashlib.sha256(cache).hexdigest())
        self.assertTrue(any(hashlib.sha256(c).hexdigest()==hashlib.sha256(old).hexdigest() and packed(json.loads(c))==cache for c in candidates))

    def test_05_head_conditional_get_stream_and_alias_dedup(self):
        j=MemoryJournal();headers={'content-length':'3','etag':'"fixture"','x-amz-version-id':'v1'}
        expected=dict(ContentLength=3,ETag='"fixture"',VersionId='v1')
        class Events:
            def register_first(self,event,handler,**kw):self.handler=handler
        class Raw:
            chunked=False
            def __init__(self,data,size):self.data=io.BytesIO(data);self.length_remaining=size;self._amount_read=0;self._raw_stream=self;self.closed=False;self.reads=0
            def close(self):self.closed=True
            def read(self,size):
                assert j.events('BODY_DEBIT') and j.events('BODY_DEBIT')[-1]['amount']==size
                self.reads+=1;data=self.data.read(size);self.length_remaining-=len(data);self._amount_read+=len(data);return data
        source='pool.urlopen(retries=Retry(False),preload_content=False)'
        raw_head=Raw(b'',0);events=Events();response=NS(raw=raw_head,status_code=200,headers=headers)
        client=NS(meta=NS(events=events),_endpoint=NS(http_session=NS(send=lambda req:response)))
        gate=SendGate(j,'HeadObject:P1','HEAD','https://fixture.example/b/k')
        install_transport(client,gate,{},source);request=NS(method='HEAD',url='https://fixture.example/b/k',headers={})
        events.handler(request);client._endpoint.http_session.send(request)
        self.assertTrue(raw_head.closed);self.assertEqual(raw_head.reads,0)
        raw=Raw(b'abc',3);events=Events();response=NS(raw=raw,status_code=200,headers=headers)
        client=NS(meta=NS(events=events),_endpoint=NS(http_session=NS(send=lambda req:response)))
        gate=SendGate(j,'GetObject:P1','GET','https://fixture.example/b/k','v1')
        install_transport(client,gate,{},source,expected);request=NS(method='GET',url='https://fixture.example/b/k?versionId=v1',headers={'If-Match':'"fixture"'})
        events.handler(request);client._endpoint.http_session.send(request);self.assertEqual(raw.reads,0)
        path=Path(ROOT)/('witness-'+SUITE+'-transport.bin');budget=Journal(ROOT);budget.reserve_output(path.name,3);budget.close()
        with open(path,'xb') as target:sha,count=transfer(raw,target,expected,j,'P1')
        self.assertEqual(count,3);self.assertEqual(raw.reads,1);self.assertEqual(len(j.events('TRANSPORT_SEND')),2)
        with self.assertRaises(ContractError):SendGate(j,'GetObject:P2','GET','https://fixture.example/b/k','v1').reserve('GET',request.url)
        self.assertEqual(len(j.events('HTTPS')),2)
        events=Events();bad=Raw(b'bad',3);response=NS(raw=bad,status_code=200,headers=dict(headers,etag='"different"'))
        client=NS(meta=NS(events=events),_endpoint=NS(http_session=NS(send=lambda req:response)))
        g=SendGate(MemoryJournal(),'GetObject:P3','GET','https://fixture.example/b/other','v1')
        install_transport(client,g,{},source,expected);request=NS(method='GET',url='https://fixture.example/b/other?versionId=v1',headers={'If-Match':'"fixture"'})
        events.handler(request)
        with self.assertRaises(ContractError):client._endpoint.http_session.send(request)
        self.assertTrue(bad.closed);self.assertEqual(bad.reads,0)

    def test_06_original_factory_fake_processor_connection(self):
        class Sum:
            def sum(self):return 324
        class IDs:
            shape=(1,100)
            def __eq__(self,other):return Sum()
        class Grid:
            def __getitem__(self,index):return 6 if isinstance(index,tuple) else self
            def tolist(self):return [6,12,18]
        class Processor:
            def apply_chat_template(self,msg,**kwargs):self.msg=msg;return 'fictional rendered template'
            def __call__(self,**kwargs):self.kwargs=kwargs;return dict(input_ids=IDs(),video_grid_thw=Grid())
        namespace={};source=(Path(ROOT)/'factory_1.py').read_text(encoding='utf-8')
        original=(Path(ROOT)/'runner_1.py').read_text(encoding='utf-8')
        select=lambda text:[n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.FunctionDef) and n.name=='inputs'][0]
        self.assertEqual(ast.dump(select(source)),ast.dump(select(original)))
        exec(compile(source,'<031-fictional-factory>','exec'),namespace)
        processor=Processor();frames=list(range(48));times=[float(i) for i in range(48)]
        fn=namespace['make_inputs']({'questions':[dict(question='fictional question',options=['one','two','three','four','five'])]},
            VideoMetadata=lambda **kw:NS(**kw),duration=100.,fps=30.,frames=frames,need=require,np=NS(stack=lambda v:NS(shape=(len(v),2,4,3))),
            prior={'video_packets':3000},qc={'video_token_id':1},qp=processor,r={'grid':[6,12,18],'visual_tokens_per_call':324},
            system='fictional system',times=times)
        out=fn(0,list(range(12)));self.assertEqual(out['video_grid_thw'][0].tolist(),[6,12,18])
        self.assertFalse(processor.kwargs['do_sample_frames']);self.assertEqual(processor.kwargs['size'],{'shortest_edge':4096,'longest_edge':786432})
        self.assertEqual(processor.msg[0]['content'],'fictional system');self.assertIn('E. five',processor.msg[1]['content'][1]['text'])

    def test_07_fresh_fixed_journal_and_full_queue(self):
        root=self.tree('journal');j=Journal(root,create=True,fixture=True)
        run=j.rows[0];self.assertEqual(run['contract_id'],'031');self.assertEqual(run['root_name'],'integration_031')
        self.assertGreater(run['epoch'],0);j.once('ONCE','slot')
        with self.assertRaises(ContractError):j.once('ONCE','slot')
        j.close();j=Journal(root);self.assertEqual(j.rows[0]['run_id'],run['run_id']);j.close()
        with self.assertRaises(FileExistsError):Journal(root,create=True,fixture=True)


def main():
    global ROOT,SUITE
    sys.stdin.readline();ROOT=sys.argv[1];SUITE=sys.argv[2]
    loader=unittest.TestLoader();tests=loader.loadTestsFromTestCase(Recovery)
    actual=tests.countTestCases()
    result=unittest.TextTestRunner(verbosity=2).run(tests)
    j=Journal(ROOT)
    try:
        receipt=dict(contract_id='031',run_id=j.rows[0]['run_id'],expected=EXPECTED,tests=result.testsRun,
            loaded=actual,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS)
        j.write('suite-'+SUITE+'-result.json',receipt)
    finally:j.close()
    sys.exit(0 if actual==EXPECTED and result.testsRun==EXPECTED and result.wasSuccessful() and not result.skipped else 1)


if __name__=='__main__':main()
