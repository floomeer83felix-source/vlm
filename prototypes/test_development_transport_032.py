"""032 new transport/archive/binding combinations; fictional data, no network/ML.

No old test imports, OS demonstration replay, or fictional child is needed.
"""
import copy
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace as NS, ModuleType
import unittest
from unittest.mock import patch
from urllib.parse import quote

from development_pilot_030 import (Journal,load,packed,digest,require,archive_rows,archive_031_rows,
    validate_031_metadata,make_queue,close_model_queue,score_allowed,score,require_ready)
from development_media_030 import (client_for,current_get_kwargs,install_transport,SendGate,transfer,network_failure)
from temporal_evidence_adapter_025 import (ContractError,TASK,QuestionKey,QuestionRecord,SourceRecord,Projection,build_plan)

ROOT=None
SUITE=None
MARKS={}
EXPECTED=6
SOURCE='pool.urlopen(retries=Retry(False),preload_content=False)'
PIN=dict(ContentLength=3,ETag='"fictional-etag"',VersionId='fictional-version')
TARGET=dict(bucket='fixture-bucket',key='opaque')


class MemoryJournal:
    def __init__(self):self.rows=[]
    def events(self,event):return [r for r in self.rows if r['event']==event]
    def add(self,event,**values):self.rows.append(dict(event=event,**values))
    def once(self,event,key,**values):
        require(not any(r.get('key')==key for r in self.events(event)),'CONSUMED_NO_RETRY')
        self.add(event,key=key,**values)


class Raw:
    def __init__(self,j,data=b'abc',length=3,chunked=False):
        self.j=j;self.data=io.BytesIO(data);self.length_remaining=length;self.chunked=chunked
        self._amount_read=0;self._raw_stream=self;self.reads=self.streams=self.drains=0;self.closed=False
    def read(self,size):
        self.reads+=1
        assert self.j.events('BODY_DEBIT') and self.j.events('BODY_DEBIT')[-1]['amount']==size
        data=self.data.read(size);self._amount_read+=len(data);self.length_remaining-=len(data);return data
    def stream(self,*a,**kw):self.streams+=1;raise AssertionError('raw stream not permitted')
    def drain_conn(self):self.drains+=1;raise AssertionError('raw drain not permitted')
    def close(self):self.closed=True


class Events:
    def register_first(self,event,handler,**kw):self.handler=handler


class FakeHTTP:
    def __init__(self,response=None,error=None):self.response=response;self.error=error;self.sends=0
    def send(self,request):
        self.sends+=1
        if self.error:raise self.error
        return self.response


class FakeConfig:
    def __init__(self,**kw):self.kwargs=kw


def client_fixture(j,status=200,headers=None,data=b'abc',length=3,chunked=False,error=None,slot='GetObject:P1'):
    raw=Raw(j,data,length,chunked)
    response=NS(raw=raw,status_code=status,headers=headers if headers is not None else
        {'content-length':'3','etag':PIN['ETag'],'x-amz-version-id':PIN['VersionId']})
    http=FakeHTTP(response,error);events=Events();client=NS(meta=NS(events=events),_endpoint=NS(http_session=http))
    session=NS(calls=[])
    def create(name,**kw):session.calls.append((name,kw));return client
    session.create_client=create
    config_module=ModuleType('botocore.config');config_module.Config=FakeConfig
    http_module=ModuleType('botocore.httpsession');http_module.URLLib3Session=FakeHTTP
    with patch.dict(sys.modules,{'botocore':ModuleType('botocore'),'botocore.config':config_module,'botocore.httpsession':http_module}):
        client,context=client_for(session,j,SOURCE,'us-east-1',slot,TARGET['bucket'],TARGET['key'],PIN)
    request=NS(method='GET',url='https://s3.us-east-1.amazonaws.com/fixture-bucket/opaque',headers={'If-Match':PIN['ETag']})
    return client,context,raw,http,request,session


def archive_fixture(extra=None):
    rows=[];payload={}
    def add(event,**fields):
        r=dict(seq=len(rows),prev=rows[-1]['hash'] if rows else '0'*64,event=event,**fields);r['hash']=digest(r);rows.append(r)
    add('RUN',contract_id='031',root_name='integration_031',purpose='REAL_031',run_id='fictional-old',epoch=0)
    add('SUITE_RESULT',contract_id='031',run_id='fictional-old',passed=True,tests=7,failures=0,errors=0,skips=0)
    lengths=[900000000,2100000000,2500000000,502290187];targets=[];heads=[]
    for i,size in enumerate(lengths):
        alias='P%d'%(i+1);key='opaque_'+str(i);uri='s3'+':/'+'/fixture-bucket/'+key
        target=dict(alias=alias,bucket='fixture-bucket',key=key,uri=uri);targets.append(target)
        head=dict(alias=alias,status=200,eligible=True,ContentLength=size,ETag='"fixture%d"'%i,VersionId='fixture-v%d'%i,region='us-east-1');heads.append(head)
        payload[alias+'-head']=(packed(head),head)
        add('OUTPUT',key=alias+'-head.json',size=len(packed(head)))
        add('OUTPUT',key=alias+'.partial',size=size)
        add('OBJECT_HEAD_TERMINAL',alias=alias,observed_status=200)
    values={name:dict(fictional=name) for name in ('keys','cohort','nongold','plan','receipts','official')}
    values.update(targets=dict(targets=targets),heads029=dict(results=[dict(heads[0])]),
        **{'metadata-summary':dict(results=heads),'annotation-reference':dict(fictional=True),
           'execution-config':dict(fictional=True),'runtime':dict(fictional=True)})
    for name,value in values.items():
        raw=packed(value);payload[name]=(raw,value);add('OUTPUT',key=name+'.json',size=len(raw))
        if name in ('keys','cohort','nongold','plan','receipts','official','targets','heads029'):
            add('INPUT_COMPLETE',alias='cache_'+name,size=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    for i in range(3):
        slot='HeadBucket:fixture-'+str(i);url='https://s3.amazonaws.com/fixture-'+str(i)
        add('HTTPS',key=slot,api='HeadBucket',method='HEAD',url=url);add('TRANSPORT_SEND',slot=slot,method='HEAD',url=url)
    for target,head in zip(targets,heads):
        base='https://s3.us-east-1.amazonaws.com/'+target['bucket']+'/'+quote(target['key'],safe='/~')
        for api,method,url in [('HeadObject','HEAD',base),('GetObject','GET',base+'?versionId='+head['VersionId'])]:
            slot=api+':'+target['alias'];add('HTTPS',key=slot,api=api,method=method,url=url);add('TRANSPORT_SEND',slot=slot,method=method,url=url)
    for n in range(16):add('TERMINAL',key=str(n),state='NOT_RUN')
    if extra:add(extra,category='gold')
    add('RUN_STOPPED',key='031')
    return b''.join(packed(r)+b'\n' for r in rows),payload


class Transport032(unittest.TestCase):
    def test_01_production_current_request_and_complete_pinned_stream(self):
        j=MemoryJournal();client,context,raw,http,request,session=client_fixture(j)
        kwargs=current_get_kwargs(TARGET,PIN);self.assertEqual(set(kwargs),{'Bucket','Key','IfMatch'})
        self.assertEqual(kwargs['IfMatch'],PIN['ETag']);self.assertEqual(PIN['VersionId'],'fictional-version')
        self.assertEqual(session.calls[0][1]['endpoint_url'],'https://s3.us-east-1.amazonaws.com')
        cfg=session.calls[0][1]['config'].kwargs;self.assertEqual(cfg['retries']['total_max_attempts'],1);self.assertEqual(cfg['proxies'],{})
        client.meta.events.handler(request);response=client._endpoint.http_session.send(request)
        self.assertEqual(raw.reads,0);self.assertEqual(context['status'],200)
        self.assertEqual(j.events('TRANSPORT_RESPONSE')[0]['profile'],'CURRENT_IFMATCH_PINNED_RESPONSE_032')
        name='witness-'+SUITE+'-complete.bin';budget=Journal(ROOT);budget.reserve_output(name,3);budget.close()
        with open(Path(ROOT)/name,'xb') as target:sha,count=transfer(response.raw,target,PIN,j,'P1')
        self.assertEqual(count,3);self.assertEqual(raw.reads,1);self.assertEqual(sum(r['amount'] for r in j.events('BODY_DEBIT')),3)
        self.assertEqual(http.sends,1);MARKS['current_request']=MARKS['response_pin']=True

    def test_02_three_header_pin_and_no_read_on_any_mismatch(self):
        base={'content-length':'3','etag':PIN['ETag'],'x-amz-version-id':PIN['VersionId']}
        variants=[dict(base,**{'x-amz-version-id':'new-version'}),{k:v for k,v in base.items() if k!='x-amz-version-id'},
                  dict(base,etag='"other"'),dict(base,**{'content-length':'4'}),dict(base,extra='x'*65537)]
        for headers in variants:
            j=MemoryJournal();client,context,raw,http,request,_=client_fixture(j,headers=headers)
            client.meta.events.handler(request)
            with self.assertRaises(ContractError):client._endpoint.http_session.send(request)
            self.assertTrue(raw.closed);self.assertEqual(raw.reads+raw.streams+raw.drains,0);self.assertEqual(j.events('TRANSPORT_RESPONSE')[0]['status'],200)
        for length,chunked in [(4,False),(3,True)]:
            j=MemoryJournal();client,context,raw,http,request,_=client_fixture(j,length=length,chunked=chunked);client.meta.events.handler(request)
            with self.assertRaises(ContractError):client._endpoint.http_session.send(request)
            self.assertTrue(raw.closed);self.assertEqual(raw.reads,0)
        class FailedLedger(MemoryJournal):
            def add(self,event,**fields):
                if event=='TRANSPORT_RESPONSE':raise OSError('fictional persistence failure')
                super().add(event,**fields)
        j=FailedLedger();client,context,raw,http,request,_=client_fixture(j);client.meta.events.handler(request)
        with self.assertRaises(OSError):client._endpoint.http_session.send(request)
        self.assertTrue(raw.closed);self.assertEqual(raw.reads,0)

    def test_03_http_failures_unknown_response_and_nonrefund(self):
        for status in [403,404,412,500,503]:
            j=MemoryJournal();client,context,raw,http,request,_=client_fixture(j,status=status);client.meta.events.handler(request)
            response=client._endpoint.http_session.send(request)
            self.assertEqual(j.events('TRANSPORT_RESPONSE')[0]['status'],status);self.assertTrue(raw.closed)
            self.assertEqual(raw.reads+raw.streams+raw.drains,0);self.assertEqual(response.raw.read(),b'')
            error=Exception('not retained');error.response={'ResponseMetadata':{'HTTPStatusCode':status},'Error':{'Message':'not retained'}}
            failure=network_failure(error,context);self.assertEqual(failure['observed_status'],status);self.assertIsNone(failure['service_code']);self.assertNotIn('Message',failure)
        j=MemoryJournal();client,context,raw,http,request,_=client_fixture(j,error=TimeoutError('not retained'));client.meta.events.handler(request)
        with self.assertRaises(TimeoutError):client._endpoint.http_session.send(request)
        self.assertEqual(len(j.events('TRANSPORT_SEND')),1);self.assertEqual(j.events('TRANSPORT_RESPONSE'),[])
        self.assertIsNone(network_failure(TimeoutError(),context)['observed_status'])
        j=MemoryJournal();raw=Raw(j,b'ab',3);name='witness-'+SUITE+'-truncated.partial';budget=Journal(ROOT);budget.reserve_output(name,3);budget.close()
        with open(Path(ROOT)/name,'xb') as target:
            with self.assertRaises(ContractError):transfer(raw,target,PIN,j,'P1')
        self.assertEqual(sum(r['amount'] for r in j.events('BODY_DEBIT')),3);self.assertEqual(j.events('MEDIA_COMPLETE'),[])
        MARKS['error_no_body']=True

    def test_04_query_range_head_redirect_duplicate_are_presend_denials(self):
        for change in ('version','range','host','method'):
            j=MemoryJournal();client,context,raw,http,request,_=client_fixture(j)
            if change=='version':request.url+='?versionId=fictional-version'
            elif change=='range':request.headers['Range']='bytes=0-1'
            elif change=='host':request.url=request.url.replace('s3.us-east-1.amazonaws.com','other.example')
            else:request.method='HEAD'
            with self.assertRaises(ContractError):client.meta.events.handler(request)
            self.assertEqual(http.sends,0);self.assertEqual(j.events('TRANSPORT_SEND'),[])
        j=MemoryJournal();g=SendGate(j,'GetObject:P1','GET','https://fixture.example/b/k');g.reserve('GET','https://fixture.example/b/k')
        with self.assertRaises(ContractError):g.reserve('GET','https://fixture.example/b/k')
        with self.assertRaises(ContractError):SendGate(j,'GetObject:P2','GET','https://fixture.example/b/k').reserve('GET','https://fixture.example/b/k')
        with self.assertRaises(ContractError):SendGate(j,'HeadObject:P1','HEAD','https://fixture.example/b/k').reserve('HEAD','https://fixture.example/b/k')
        self.assertEqual(len(j.events('HTTPS')),1)

    def test_05_031_real_action_archive_and_direct_bytes_metadata_binding(self):
        raw,payload=archive_fixture();rows=archive_031_rows(raw);self.assertEqual(len(validate_031_metadata(rows,payload)),4)
        with self.assertRaises(ContractError):archive_rows(raw)
        for event in ('BODY_DEBIT','MEDIA_COMPLETE','MODEL_LAUNCH','STARTED','SCORE_CONSUMED','INPUT'):
            changed,_=archive_fixture(event)
            with self.assertRaises(ContractError):archive_031_rows(changed)
        with self.assertRaises(ContractError):archive_031_rows(raw[:-1])
        with self.assertRaises(ContractError):archive_031_rows(raw.replace(b'fictional-old',b'tampered-runx'))
        changed=copy.deepcopy(payload);value=changed['keys'][1];changed['keys']=(json.dumps(value,indent=2).encode(),value)
        with self.assertRaises(ContractError):validate_031_metadata(rows,changed)
        for key,value in [('VersionId','different-version'),('ContentLength',1),('ETag','"other"')]:
            changed=copy.deepcopy(payload);head=dict(changed['P2-head'][1]);head[key]=value;changed['P2-head']=(packed(head),head)
            with self.assertRaises(ContractError):validate_031_metadata(rows,changed)
        MARKS['archive_031']=True

    def test_06_fixed032_suite_queue_score_and_zero_opener_on_wrong_binding(self):
        name='witness-'+SUITE+'-bindings';j=Journal(ROOT);j.reserve_output(name+'-budget',96*1024,files=24);j.close()
        parent=Path(ROOT)/name;parent.mkdir();root=parent/'integration_032';j=Journal(root,create=True,fixture=True)
        self.assertEqual(j.rows[0]['contract_id'],'032')
        sources=tuple(SourceRecord('fixture_'+str(i),()) for i in range(4))
        questions=tuple(QuestionRecord(QuestionKey(s.source,0),TASK,'How long after opening a box did closing a box?',('one','two','three','four','five')) for s in sources)
        projection=Projection('inference',sources,questions);plan=build_plan(projection)
        config=dict(slots=[dict(slot=n,alias='P%d'%(n//4+1),arm=c.arm) for n,c in enumerate(plan.calls)])
        j.write('nongold.json',dict(projection=asdict(projection)));j.write('worker-input.json',config)
        j.add('FROZEN',plan_hash=digest(asdict(plan)),worker_hash=digest(config));queue=make_queue(root,j,{a:True for a in ['P1','P2','P3','P4']})
        self.assertEqual(queue['contract_id'],'032');self.assertEqual(queue['run_id'],j.rows[0]['run_id'])
        with self.assertRaises(ContractError):require_ready(j)
        j.add('SUITE_RESULT',contract_id='031',run_id=j.rows[0]['run_id'],passed=True,tests=7)
        with self.assertRaises(ContractError):require_ready(j)
        # Fictional trace only, not an OS exit certificate; malformed launch is
        # rejected by the production scorer before any annotation opener exists.
        j.once('MODEL_LAUNCH','gpu',run_id=j.rows[0]['run_id'],queue_hash='wrong-binding')
        for slot in config['slots']:
            j.once('STARTED',str(slot['slot']));j.once('TERMINAL',str(slot['slot']),alias=slot['alias'],arm=slot['arm'],state='RETURNED',prediction='A')
        close_model_queue(root,j,dict(job_active=0,pid=1,exit_code=0,seconds=.01))
        with self.assertRaises(ContractError):score_allowed(j.rows,root)
        j.close();score(root);j=Journal(root)
        self.assertEqual(len(j.events('SCORE_CONSUMED')),1);self.assertEqual(j.events('INPUT'),[]);self.assertEqual(j.events('SCORED'),[])
        j.once('RUN_STOPPED','032')
        with self.assertRaises(ContractError):require_ready(j)
        j.close()
        with self.assertRaises(ContractError):Journal(Path(ROOT).parent/'integration_031')
        MARKS['bindings_032']=True


def main():
    global ROOT,SUITE
    sys.stdin.readline();ROOT=sys.argv[1];SUITE=sys.argv[2]
    tests=unittest.TestLoader().loadTestsFromTestCase(Transport032);loaded=tests.countTestCases()
    result=unittest.TextTestRunner(verbosity=2).run(tests)
    j=Journal(ROOT)
    try:j.write('suite-'+SUITE+'-result.json',dict(contract_id='032',run_id=j.rows[0]['run_id'],expected=EXPECTED,loaded=loaded,
        tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),os_marks=MARKS))
    finally:j.close()
    sys.exit(0 if loaded==EXPECTED==result.testsRun and result.wasSuccessful() and not result.skipped else 1)


if __name__=='__main__':main()
