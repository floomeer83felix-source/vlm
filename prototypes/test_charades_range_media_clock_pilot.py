"""Only synthetic HTTP, ZIP, identities and clocks; never connects to a server."""
import io
import json
import struct
import unittest
import zipfile
import zlib
import pathlib
import hashlib
import tempfile
import os
import ssl
import ast
import urllib.request
from unittest import mock
from charades_range_media_clock_pilot import (
    PilotError,Ledger,URL,NET_LIMIT,DISK_LIMIT,validate_range,read_response,eocd,
    central_directory,match_two,local_header,expand_member,select_cases,safe_name,
    validate_extra,ffprobe_command,classify_clock,public_receipt,NoRedirect,run_pilot)
from charades_range_media_clock_pilot import zip64_fields,authorize_parent,official_anchor,transfer_two
from charades_range_media_clock_pilot import PAGE,LICENSE,RangeClient,build_media_opener,fixed_request
from charades_range_media_clock_pilot import strong_etag,head_identity


class Response:
    def __init__(self,body,status=206,headers=None):
        self.body=io.BytesIO(body); self.status=status; self.calls=0
        self.headers=headers if headers is not None else {'Content-Range':'bytes 0-3/100','Content-Length':'4','ETag':'"toy-etag"','Content-Encoding':'identity'}
    def geturl(self): return URL
    def read(self,n): self.calls+=1; return self.body.read(n)
    def __enter__(self): return self
    def __exit__(self,*args): pass


def toy_zip(method=zipfile.ZIP_STORED):
    f=io.BytesIO()
    with zipfile.ZipFile(f,'w',compression=method) as z:
        z.writestr('bundle/SYNTHETIC-A.mp4',b'TOY BYTES A')
        z.writestr('bundle/SYNTHETIC-B.mp4',b'TOY BYTES B')
    return f.getvalue()


def records(data):
    off,size,n=eocd(data,len(data))
    return central_directory(data[off:off+size],n,off)


class PilotTests(unittest.TestCase):
    def setUp(self):
        # Any unmocked network or executable use fails, including legacy fixtures.
        for target in ('urllib.request.OpenerDirector.open','urllib.request.urlopen',
                       'socket.create_connection','subprocess.run'):
            patcher=mock.patch(target,side_effect=AssertionError('SYNTHETIC_ONLY_UNMOCKED_IO'))
            patcher.start(); self.addCleanup(patcher.stop)

    def test_good_206_exact_body_count(self):
        ledger=Ledger(); ledger.begin(0,3)
        self.assertEqual(read_response(Response(b'toy!'),0,3,100,'"toy-etag"',ledger),b'toy!')
        self.assertEqual(ledger.state['body_bytes'],4)

    def test_200_rejected_before_body(self):
        r=Response(b'SYNTHETIC WHOLE ARCHIVE',status=200); ledger=Ledger(); ledger.begin(0,3)
        with self.assertRaisesRegex(PilotError,'REQUIRES_206'): read_response(r,0,3,100,'"toy-etag"',ledger)
        self.assertEqual(r.calls,0); self.assertEqual(ledger.state['body_bytes'],0)

    def test_range_encoding_length_etag_and_domain_rejected(self):
        good=Response(b'toy!').headers
        for key,value in (('Content-Range','bytes 1-4/100'),('Content-Encoding','gzip'),('Content-Length','40'),('ETag','different')):
            bad=dict(good); bad[key]=value
            with self.assertRaises(PilotError): validate_range(206,bad,0,3,100,'"toy-etag"',URL)
        with self.assertRaises(PilotError): validate_range(206,good,0,3,100,'"toy-etag"','https://invalid.example/')
        with self.assertRaisesRegex(PilotError,'REDIRECT_FORBIDDEN'): NoRedirect().redirect_request(None)

    def test_cumulative_budget_and_failure_bytes_not_reset(self):
        ledger=Ledger(); ledger.state['body_bytes']=NET_LIMIT-3; ledger.state['charged_bytes']=NET_LIMIT-3
        with self.assertRaises(PilotError): ledger.begin(0,3)
        ledger.begin(0,2); ledger.reserve(2); ledger.add(2); ledger.finish('STOPPED')
        self.assertEqual(ledger.state['body_bytes'],NET_LIMIT-1)
        with self.assertRaises(PilotError): ledger.add(2)

    def test_request_count_and_disk_budget(self):
        ledger=Ledger(); ledger.state['get_attempts']=12
        with self.assertRaises(PilotError): ledger.begin(0,0)
        with self.assertRaises(PilotError): ledger.disk(DISK_LIMIT+1)
        ledger.disk(100); self.assertEqual(ledger.state['peak_local_bytes'],100)

    def test_truncated_response_keeps_read_account(self):
        ledger=Ledger(); ledger.begin(0,3)
        with self.assertRaisesRegex(PilotError,'TRUNCATED'): read_response(Response(b'to'),0,3,100,'"toy-etag"',ledger)
        self.assertEqual(ledger.state['body_bytes'],2)

    def test_eocd_and_directory_classic_valid(self):
        data=toy_zip(); r=records(data)
        self.assertEqual(len(r),2)
        self.assertEqual(len(match_two(r,['SYNTHETIC-A','SYNTHETIC-B'])),2)

    def test_zip64_multidisk_and_trailing_stop(self):
        for disk,count,size,offset in ((1,2,0,0),(0,65535,0,0),(0,2,0xffffffff,0)):
            tail=struct.pack('<4s4H2LH',b'PK\x05\x06',disk,0,count,count,size,offset,0)
            with self.assertRaises(PilotError): eocd(tail,len(tail))
        with self.assertRaises(PilotError): eocd(toy_zip()+b'trailing',len(toy_zip())+8)
        with self.assertRaises(PilotError): validate_extra(struct.pack('<HH',1,0))

    def test_zip64_eocd_64bit_offsets_supported(self):
        record_offset=5*1024*1024*1024
        central_offset=record_offset-512
        record=struct.pack('<4sQ2H2L4Q',b'PK\x06\x06',44,45,45,0,0,2,2,512,central_offset)
        locator=struct.pack('<4sLQL',b'PK\x06\x07',0,record_offset,1)
        end=struct.pack('<4s4H2LH',b'PK\x05\x06',0,0,2,2,512,0xffffffff,0)
        tail=record+locator+end
        self.assertEqual(eocd(tail,record_offset+len(tail)),(central_offset,512,2))
        changed=bytearray(tail); struct.pack_into('<L',changed,56+16,2)
        with self.assertRaises(PilotError): eocd(changed,record_offset+len(changed))

    def test_zip64_extra_strict_field_order_and_missing_values(self):
        body=struct.pack('<QQQ',100,80,5*1024*1024*1024)
        extra=struct.pack('<HH',1,len(body))+body
        self.assertEqual(zip64_fields(extra,0xffffffff,0xffffffff,0xffffffff,0),(100,80,5*1024*1024*1024,0))
        with self.assertRaises(PilotError): zip64_fields(extra,100,80,0,0)
        with self.assertRaises(PilotError): zip64_fields(b'',0xffffffff,80,0,0)

    def test_zip64_local_header_consistent_size(self):
        name=b'SYNTHETIC.mp4'; body=struct.pack('<QQ',100,80); extra=struct.pack('<HH',1,16)+body
        header=struct.pack('<4s5H3L2H',b'PK\x03\x04',45,0,8,0,0,123,0xffffffff,0xffffffff,len(name),len(extra))
        entry={'flags':0,'method':8,'crc':123,'compressed':80,'size':100,'name_bytes':name}
        self.assertEqual(local_header(header,name+extra,entry),len(name)+len(extra))

    def test_zip_paths_special_names_and_case_duplicates(self):
        for name in ('../bad.mp4','/bad.mp4','C:/bad.mp4','a\\b.mp4','NUL.txt','bad|name'):
            with self.assertRaises(PilotError): safe_name(name)
        f=io.BytesIO()
        with zipfile.ZipFile(f,'w') as z:
            z.writestr('toy.mp4',b'x'); z.writestr('TOY.mp4',b'x')
        with self.assertRaisesRegex(PilotError,'DUPLICATE'): records(f.getvalue())

    def test_symlink_encryption_and_descriptor_rejected(self):
        data=bytearray(toy_zip()); off,_,_=eocd(data,len(data))
        for flags in (1,8):
            changed=bytearray(data); struct.pack_into('<H',changed,off+8,flags)
            with self.assertRaises(PilotError): records(changed)
        changed=bytearray(data); struct.pack_into('<L',changed,off+38,0xa1ff<<16)
        with self.assertRaises(PilotError): records(changed)
        changed=bytearray(data); struct.pack_into('<H',changed,off+8,0x40)
        with self.assertRaises(PilotError): records(changed)

    def test_local_header_crc_size_and_name_match(self):
        data=toy_zip(); entry=records(data)[0]; pos=entry['offset']
        header=data[pos:pos+30]; n,e=struct.unpack_from('<HH',header,26)
        extra=data[pos+30:pos+30+n+e]
        self.assertEqual(local_header(header,extra,entry),n+e)
        with self.assertRaises(PilotError): local_header(header,b'WRONG',entry)
        modified=dict(entry); modified['crc']+=1
        with self.assertRaises(PilotError): local_header(header,extra,modified)

    def test_stored_and_deflate_bounded_crc(self):
        for method in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
            data=toy_zip(method); entry=records(data)[0]; p=entry['offset']
            n,e=struct.unpack_from('<HH',data,p+26); start=p+30+n+e
            body=data[start:start+entry['compressed']]
            self.assertEqual(expand_member(body,entry),b'TOY BYTES A')
            bad=dict(entry); bad['crc']^=1
            with self.assertRaises(PilotError): expand_member(body,bad)

    def test_zipbomb_bound_and_exact_two_matching(self):
        d=zlib.compressobj(wbits=-15); body=d.compress(b'X'*10000)+d.flush()
        entry={'compressed':len(body),'size':5,'method':8,'crc':0}
        with self.assertRaises(PilotError): expand_member(body,entry)
        r=records(toy_zip())
        for ids in (['SYNTHETIC-A'],['SYNTHETIC-A','SYNTHETIC-A'],['SYNTHETIC-A','MISSING']):
            with self.assertRaises(PilotError): match_two(r,ids)

    def test_selection_frozen_before_remote_and_duplicates_stop(self):
        rows=[{'id':'SYNTHETIC-A','subject':'PERSON-A','length':'10','actions':'toy-class 0 12'},
              {'id':'SYNTHETIC-B','subject':'PERSON-B','length':'10','actions':'toy-class 0 5'}]
        selected=select_cases(rows,{'toy-class'})
        self.assertEqual([x['id'] for x in selected],['SYNTHETIC-A','SYNTHETIC-B'])
        with self.assertRaises(PilotError): select_cases(rows+[rows[0]],{'toy-class'})

    def test_ffprobe_packet_only_and_private_clock_redacted(self):
        command=ffprobe_command('SYNTHETIC-TOOL','SYNTHETIC.mp4')
        self.assertIn('-show_packets',command); self.assertNotIn('-show_frames',command)
        self.assertIn('file',command)
        probe={'streams':[{'time_base':'1/10','avg_frame_rate':'10/1','r_frame_rate':'10/1','start_time':'0','duration':'1'}],
               'format':{'duration':'1'},'packets':[{'pts':'0','duration':'1'},{'pts':'9','duration':'1'}]}
        self.assertEqual(classify_clock(probe,'1'),'LENGTH_APPROX_MATCH')
        probe['streams'][0]['has_b_frames']=1
        self.assertEqual(classify_clock(probe,'1'),'CLOCK_UNKNOWN')
        text=json.dumps(public_receipt({'private_id':'SYNTHETIC-SECRET','duration':1}))
        self.assertNotIn('SYNTHETIC-SECRET',text); self.assertNotIn('duration',text)

    def test_nonfinite_clock_metadata_is_unknown_not_mismatch(self):
        from charades_range_media_clock_pilot import endpoint_relation
        probe={'streams':[{'time_base':'1/10','avg_frame_rate':'10/1','r_frame_rate':'10/1','start_time':'0','duration':'1'}],
               'format':{'duration':'Infinity'},'packets':[{'pts':'0','duration':'10'}]}
        self.assertEqual(classify_clock(probe,'1'),'CLOCK_UNKNOWN')
        self.assertEqual(endpoint_relation(probe,{'length':'1','ends':['2']}),'END_CLOCK_UNKNOWN')

    def test_missing_tool_stops_before_network_or_storage(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe',side_effect=PilotError('BLOCKED_EXISTING_FFPROBE_NOT_FOUND')), \
             mock.patch('charades_range_media_clock_pilot.urllib.request.build_opener') as network:
            with self.assertRaises(PilotError): run_pilot()
            network.assert_not_called()

    def test_canonical_tool_redirect_into_conda_still_rejected(self):
        from charades_range_media_clock_pilot import find_ffprobe
        with mock.patch('charades_metadata_audit.check_ancestors'), \
             mock.patch('charades_range_media_clock_pilot.shutil.which',return_value=None), \
             mock.patch('charades_range_media_clock_pilot.pathlib.Path.is_file',return_value=True), \
             mock.patch('charades_range_media_clock_pilot.pathlib.Path.resolve',return_value=pathlib.Path('SYNTHETIC/.conda/ffprobe.exe')):
            with self.assertRaisesRegex(PilotError,'FFPROBE_NOT_FOUND'): find_ffprobe()

    def test_preflight_only_never_creates_network_after_tool_success(self):
        with mock.patch('charades_range_media_clock_pilot.authorize_parent'), mock.patch('charades_range_media_clock_pilot.find_ffprobe',return_value=pathlib.Path('SYNTHETIC-TOOL')), \
             mock.patch('charades_range_media_clock_pilot.subprocess.run',return_value=mock.Mock(stdout=b'ffprobe version 9.0.2-SYNTHETIC')), \
             mock.patch('charades_range_media_clock_pilot.urllib.request.build_opener') as network:
            result=run_pilot()
            self.assertEqual(result['status'],'PREFLIGHT_ONLY')
            network.assert_not_called()

    def test_completed_parent_rejected_no_repeat(self):
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder); (root/'docs').mkdir()
            (root/'docs/next-steps.md').write_text('| VLM-BATCH-999 | P1 | **READY** | safe |',encoding='utf-8')
            (root/'docs/codex-results.md').write_text('### VLM-BATCH-999 completed',encoding='utf-8')
            with self.assertRaisesRegex(PilotError,'ALREADY_REPORTED'): authorize_parent('VLM-BATCH-999',root)

    def test_official_anchor_exact_unique_source(self):
        from charades_range_media_clock_pilot import URL
        good='<a href="'+URL+'">Data (scaled to 480p, 13 GB)</a>'
        official_anchor(good)
        with self.assertRaises(PilotError): official_anchor(good+good)
        with self.assertRaises(PilotError): official_anchor(good.replace(URL,'https://invalid.example/file.zip'))

    def test_persistent_ledger_atomic_restore_no_reset(self):
        with tempfile.TemporaryDirectory() as folder:
            file=pathlib.Path(folder)/'ledger.json'; ledger=Ledger(file)
            ledger.begin(0,3); ledger.reserve(2); ledger.add(2); ledger.finish('STOPPED')
            self.assertEqual(json.loads(file.read_text())['body_bytes'],2)
            with self.assertRaisesRegex(PilotError,'ALREADY_EXISTS'): Ledger(file)

    def test_coordinator_transfer_two_with_synthetic_range_client(self):
        data=toy_zip()
        ledger=Ledger()
        class Client:
            total=len(data)
            def __init__(self): self.ledger=ledger
            def get(self,start,end):
                ledger.begin(start,end); ledger.reserve(end-start+1); ledger.add(end-start+1); ledger.finish('COMPLETE')
                return data[start:end+1]
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            for name in ('incoming','media','local-audit'): (root/name).mkdir()
            saved=transfer_two(Client(),[{'id':'SYNTHETIC-A'},{'id':'SYNTHETIC-B'}],root)
            self.assertEqual(len(saved),2)
            self.assertEqual((root/'media/case-0.mp4').read_bytes(),b'TOY BYTES A')
            self.assertFalse(list((root/'incoming').iterdir()))
            self.assertEqual(ledger.state['saved_videos'],2)

    def test_execute_coordinator_complete_with_mocked_http_and_probe(self):
        from charades_range_media_clock_pilot import PAGE,URL
        data=toy_zip(); real_sha=hashlib.sha256
        def hash_only_synthetic_license(value=b''):
            if value==b'SYNTHETIC-LICENSE':
                return mock.Mock(hexdigest=lambda:'a734f9263490d2a0567da2e39f109f3cf535896e4efb91caaefa27644ac628f0')
            return real_sha(value)
        class Head:
            status=200; headers={'Content-Type':'application/zip','Content-Length':str(len(data)),'ETag':'"toy-etag"'}
            def geturl(self): return URL
            def __enter__(self): return self
            def __exit__(self,*args): pass
        class Client:
            def __init__(self,ledger,total,etag):
                self.ledger=ledger; self.total=total; self.etag=etag; self.opener=mock.Mock(open=lambda *a,**k:Head())
            def text(self,url,limit):
                value=('<a href="'+URL+'">Data (scaled to 480p, 13 GB)</a>').encode() if url==PAGE else b'SYNTHETIC-LICENSE'
                self.ledger.begin(0,limit-1); self.ledger.reserve(len(value)); self.ledger.add(len(value)); self.ledger.finish('COMPLETE'); return value
            def get(self,start,end):
                self.ledger.begin(start,end); self.ledger.reserve(end-start+1); self.ledger.add(end-start+1); self.ledger.finish('COMPLETE')
                return data[start:end+1]
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder); meta=base/'synthetic-metadata'; meta.mkdir()
            (meta/'classes.txt').write_text('toy-class Synthetic')
            (meta/'train.csv').write_text('id,subject,actions,length\nSYNTHETIC-A,PERSON-A,toy-class 0 12,10\nSYNTHETIC-B,PERSON-B,toy-class 0 5,10\n')
            probe={'streams':[{'time_base':'1/10','avg_frame_rate':'10/1','r_frame_rate':'10/1','start_time':'0','duration':'10'}],
                   'format':{'duration':'10'},'packets':[{'pts':'0','duration':'1'},{'pts':'99','duration':'1'}]}
            def fake_subprocess(command,**kwargs):
                return mock.Mock(stdout=b'ffprobe version 9.0.2-SYNTHETIC') if '-version' in command else mock.Mock(stdout=json.dumps(probe).encode())
            with mock.patch('charades_range_media_clock_pilot.find_ffprobe',return_value=pathlib.Path('SYNTHETIC-TOOL')), \
                 mock.patch('charades_range_media_clock_pilot.subprocess.run',fake_subprocess), \
                 mock.patch('charades_range_media_clock_pilot.authorize_parent'), \
                 mock.patch('charades_range_media_clock_pilot.fixed_preflight',return_value=(base/'synthetic-pilot',{'classes':meta/'classes.txt','train':meta/'train.csv'})), \
                 mock.patch('charades_range_media_clock_pilot.RangeClient',Client), \
                 mock.patch('charades_range_media_clock_pilot.hashlib.sha256',hash_only_synthetic_license), \
                 mock.patch('unittest.TextTestRunner.run',return_value=mock.Mock(testsRun=60,skipped=[],wasSuccessful=lambda:True)):
                out=run_pilot(True,'VLM-BATCH-999')
            self.assertEqual(out['status'],'CASE_LIMITED_COMPLETE')
            self.assertEqual(out['saved_videos'],2)
            self.assertNotIn('SYNTHETIC-A',json.dumps(out))
            self.assertEqual(out['CASE_CONTROL'],'LENGTH_APPROX_MATCH')

    def test_proxy_pollution_does_not_discover_or_install_proxy(self):
        with mock.patch.dict(os.environ,{'HTTPS_PROXY':'http://invalid.example:1',
             'HTTP_PROXY':'http://invalid.example:1','ALL_PROXY':'http://invalid.example:1',
             'https_proxy':'http://invalid.example:1','http_proxy':'http://invalid.example:1'}), \
             mock.patch('urllib.request.getproxies',side_effect=AssertionError('PROXY_DISCOVERY')) as discovery:
            opener=build_media_opener()
        discovery.assert_not_called()
        self.assertFalse(any(getattr(h,'proxies',{}) for h in opener.handlers))

    def test_windows_system_proxy_functions_never_queried(self):
        with mock.patch('urllib.request.getproxies',side_effect=AssertionError('SYSTEM_PROXY')) as combined, \
             mock.patch('urllib.request.getproxies_registry',create=True,side_effect=AssertionError('REGISTRY_PROXY')) as registry, \
             mock.patch('urllib.request.getproxies_environment',side_effect=AssertionError('ENV_PROXY')) as environment:
            RangeClient(Ledger(),100,'"toy-etag"')
        combined.assert_not_called(); registry.assert_not_called(); environment.assert_not_called()

    def test_default_tls_verified_and_insecure_context_refused(self):
        opener=build_media_opener()
        https=next(h for h in opener.handlers if isinstance(h,urllib.request.HTTPSHandler))
        self.assertTrue(https._context.check_hostname)
        self.assertEqual(https._context.verify_mode,ssl.CERT_REQUIRED)
        unsafe=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT); unsafe.check_hostname=False; unsafe.verify_mode=ssl.CERT_NONE
        with mock.patch('charades_range_media_clock_pilot.ssl.create_default_context',return_value=unsafe):
            with self.assertRaisesRegex(PilotError,'TLS_VERIFICATION_REQUIRED'): build_media_opener()

    def test_redirect_301_302_307_308_never_reads_body(self):
        request=fixed_request(PAGE,'GET',{'Accept-Encoding':'identity'})
        handler=NoRedirect()
        for code in (301,302,307,308):
            response=Response(b'SYNTHETIC REDIRECT')
            with self.assertRaisesRegex(PilotError,'REDIRECT_FORBIDDEN'):
                getattr(handler,'http_error_'+str(code))(request,response,code,'SYNTHETIC',{'location':URL})
            self.assertEqual(response.calls,0)

    def test_exact_https_url_and_method_allowlist(self):
        headers={'Accept-Encoding':'identity'}
        for source in (PAGE,LICENSE): self.assertEqual(fixed_request(source,'GET',headers).full_url,source)
        self.assertEqual(fixed_request(URL,'HEAD',headers).get_method(),'HEAD')
        for source,method in ((PAGE.replace('https:','http:'),'GET'),
              (URL.replace('https:','http:'),'HEAD'),(URL+'?override=1','HEAD'),
              ('https://invalid.example/media.zip','HEAD'),(PAGE,'HEAD'),(LICENSE,'POST'),(URL,'POST')):
            with self.assertRaisesRegex(PilotError,'SOURCE_OR_METHOD'): fixed_request(source,method,headers)

    def test_media_get_requires_bounded_range_and_identity(self):
        good={'Accept-Encoding':'identity','Range':'bytes=0-3','If-Range':'"toy-etag"'}
        self.assertEqual(fixed_request(URL,'GET',good).get_header('Range'),'bytes=0-3')
        for changes in ({'Range':''},{'Range':'bytes=0-'},{'Range':'bytes=3-0'},
                        {'If-Range':''},{'If-Range':'bad\r\nvalue'},{'Accept-Encoding':'gzip'}):
            with self.assertRaises(PilotError): fixed_request(URL,'GET',dict(good,**changes))

    def test_shared_opener_for_page_license_head_and_range(self):
        ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"'); seen=[]
        def respond(request,**kwargs):
            seen.append((request.full_url,request.get_method()))
            if request.get_method()=='HEAD':
                response=Response(b'',status=200,headers={'Content-Length':'100','Content-Type':'application/zip','ETag':'"toy-etag"'})
            elif request.full_url in (PAGE,LICENSE):
                response=Response(b'toy!',status=200,headers={'Content-Length':'4','Content-Encoding':'identity'})
                response.geturl=lambda:request.full_url
            else: response=Response(b'toy!')
            return response
        with mock.patch.object(client.opener,'open',side_effect=respond) as shared:
            self.assertEqual(client.text(PAGE,8),b'toy!')
            self.assertEqual(client.text(LICENSE,8),b'toy!')
            with client.opener.open(fixed_request(URL,'HEAD',{'Accept-Encoding':'identity'}),timeout=30) as head:
                self.assertEqual(head.status,200); self.assertEqual(head.calls,0)
            self.assertEqual(client.get(0,3),b'toy!')
            self.assertEqual(shared.call_count,4)
        self.assertEqual(seen,[(PAGE,'GET'),(LICENSE,'GET'),(URL,'HEAD'),(URL,'GET')])
        self.assertEqual(ledger.state['body_bytes'],12)

    def test_range_client_error_status_and_source_no_body(self):
        for status in (200,416,302):
            ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"'); response=Response(b'SYNTHETIC',status=status)
            with mock.patch.object(client.opener,'open',return_value=response):
                with self.assertRaises(PilotError): client.get(0,3)
            self.assertEqual(response.calls,0); self.assertEqual(ledger.state['body_bytes'],0)
            self.assertEqual(ledger.state['events'][-1]['status'],'STOPPED')
        ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"'); response=Response(b'toy!')
        response.geturl=lambda:'https://invalid.example/media.zip'
        with mock.patch.object(client.opener,'open',return_value=response):
            with self.assertRaises(PilotError): client.get(0,3)
        self.assertEqual(response.calls,0)

    def test_text_error_status_encoding_and_size_no_body(self):
        for status,headers in ((302,{'Content-Length':'4'}),(200,{'Content-Length':'4','Content-Encoding':'gzip'}),
                              (200,{}),(200,{'Content-Length':'40'})):
            ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"'); response=Response(b'toy!',status=status,headers=headers)
            response.geturl=lambda:PAGE
            with mock.patch.object(client.opener,'open',return_value=response):
                with self.assertRaises(PilotError): client.text(PAGE,8)
            self.assertEqual(response.calls,0); self.assertEqual(ledger.state['body_bytes'],0)
            self.assertEqual(ledger.state['events'][-1]['status'],'STOPPED')

    def test_text_unknown_source_stops_before_open_or_ledger(self):
        ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"')
        with mock.patch.object(client.opener,'open') as opener:
            with self.assertRaises(PilotError): client.text('https://invalid.example/license',8)
        opener.assert_not_called(); self.assertEqual(ledger.state['get_attempts'],0)

    def test_client_partial_failure_budget_not_reset(self):
        ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"'); response=Response(b'to')
        with mock.patch.object(client.opener,'open',return_value=response):
            with self.assertRaisesRegex(PilotError,'TRUNCATED'): client.get(0,3)
        self.assertEqual(ledger.state['body_bytes'],2); self.assertEqual(ledger.state['get_attempts'],1)
        good=Response(b'toy!')
        with mock.patch.object(client.opener,'open',return_value=good): self.assertEqual(client.get(0,3),b'toy!')
        self.assertEqual(ledger.state['body_bytes'],6); self.assertEqual(ledger.state['get_attempts'],2)

    def test_completed_013_protected_even_when_still_ready(self):
        with tempfile.TemporaryDirectory() as folder:
            docs=pathlib.Path(folder); (docs/'docs').mkdir()
            (docs/'docs/next-steps.md').write_text('| VLM-BATCH-013 | P1 | **READY** | synthetic |')
            (docs/'docs/codex-results.md').write_text('### VLM-BATCH-013 completed\n')
            with self.assertRaisesRegex(PilotError,'ALREADY_REPORTED'): authorize_parent('VLM-BATCH-013',docs)

    def test_static_network_entry_inventory_has_no_fallback(self):
        source=pathlib.Path(__file__).with_name('charades_range_media_clock_pilot.py').read_text(encoding='utf-8')
        tree=ast.parse(source)
        attrs=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertEqual(attrs.count('build_opener'),1)
        self.assertEqual(attrs.count('Request'),1)
        self.assertNotIn('urlopen',attrs)
        nodes={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        factory=ast.unparse(nodes['build_media_opener'])
        self.assertIn('ProxyHandler({})',factory); self.assertIn('create_default_context()',factory)
        for name in ('RangeClient','run_pilot'):
            text=ast.unparse(nodes[name]); self.assertIn('fixed_request(',text); self.assertIn('.opener.open(',text)

    def test_missing_parent_has_zero_tool_storage_network(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool, \
             mock.patch('charades_range_media_clock_pilot.fixed_preflight') as storage, \
             mock.patch('charades_range_media_clock_pilot.build_media_opener') as network, \
             mock.patch('charades_range_media_clock_pilot.subprocess.run') as process:
            with self.assertRaises(PilotError): run_pilot(True,None)
        tool.assert_not_called(); storage.assert_not_called(); network.assert_not_called(); process.assert_not_called()

    def test_old_completed_013_rejected_before_version(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool, \
             mock.patch('charades_range_media_clock_pilot.subprocess.run') as process:
            with self.assertRaisesRegex(PilotError,'ALREADY_REPORTED'): run_pilot(True,'VLM-BATCH-013')
        tool.assert_not_called(); process.assert_not_called()

    def test_keywords_cannot_spoof_frozen_017_authority(self):
        import charades_range_media_clock_pilot as pilot
        board='| VLM-BATCH-017 | P1 | **READY** | synthetic |'
        with mock.patch.object(pathlib.Path,'read_text',side_effect=[board,'','Charades_v1_480.zip 64 128 ffprobe']):
            with self.assertRaisesRegex(PilotError,'MEDIA_SCOPE'): authorize_parent('VLM-BATCH-017',pathlib.Path('SYNTHETIC'))
        with mock.patch.object(pathlib.Path,'read_text',side_effect=[board,'']):
            with self.assertRaises(PilotError): authorize_parent('VLM-BATCH-999',pathlib.Path('SYNTHETIC'))

    def test_frozen_contract_and_history_must_all_match(self):
        import charades_range_media_clock_pilot as pilot
        board='| VLM-BATCH-018 | P1 | **READY** | synthetic |'; contract='SYNTHETIC EXACT CONTRACT'
        sections={p:'### '+p+' synthetic complete' for p in pilot.HISTORY_SHA}
        results='\n\n'.join(sections.values())
        pins={p:hashlib.sha256(v.encode()).hexdigest() for p,v in sections.items()}
        with mock.patch.object(pilot,'CONTRACT_SHA',hashlib.sha256(contract.encode()).hexdigest()), \
             mock.patch.object(pilot,'HISTORY_SHA',pins):
            with mock.patch.object(pathlib.Path,'read_text',side_effect=[board,results,contract]):
                authorize_parent('VLM-BATCH-018',pathlib.Path('SYNTHETIC'))
            with mock.patch.object(pathlib.Path,'read_text',side_effect=[board,results+' CHANGED',contract]):
                with self.assertRaisesRegex(PilotError,'HISTORICAL'): authorize_parent('VLM-BATCH-018',pathlib.Path('SYNTHETIC'))

    def test_authorized_default_is_read_only_no_version(self):
        with mock.patch('charades_range_media_clock_pilot.authorize_parent'), \
             mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool, \
             mock.patch('charades_range_media_clock_pilot.fixed_preflight') as storage, \
             mock.patch('charades_range_media_clock_pilot.subprocess.run') as process:
            out=run_pilot(False,'VLM-BATCH-017')
        self.assertEqual(out['version_runs'],0); tool.assert_not_called(); storage.assert_not_called(); process.assert_not_called()

    def test_synthetic_gate_before_asset_or_tool_access(self):
        with mock.patch('charades_range_media_clock_pilot.authorize_parent'), \
             mock.patch('unittest.TextTestRunner.run',return_value=mock.Mock(testsRun=51,skipped=[],wasSuccessful=lambda:True)), \
             mock.patch('charades_range_media_clock_pilot.fixed_preflight') as storage, \
             mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool:
            with self.assertRaisesRegex(PilotError,'SYNTHETIC_GATE'): run_pilot(True,'VLM-BATCH-017')
        storage.assert_not_called(); tool.assert_not_called()

    def test_metadata_failure_before_version_or_http(self):
        with mock.patch('charades_range_media_clock_pilot.authorize_parent'), \
             mock.patch('unittest.TextTestRunner.run',return_value=mock.Mock(testsRun=60,skipped=[],wasSuccessful=lambda:True)), \
             mock.patch('charades_range_media_clock_pilot.fixed_preflight',side_effect=PilotError('SOURCE_SHA_MISMATCH')), \
             mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool, \
             mock.patch('charades_range_media_clock_pilot.build_media_opener') as network:
            out=run_pilot(True,'VLM-BATCH-017')
        self.assertEqual(out['version_runs'],0); self.assertEqual(out['get_attempts'],0)
        tool.assert_not_called(); network.assert_not_called()

    def test_fsync_reservation_persisted_before_read(self):
        with tempfile.TemporaryDirectory() as folder:
            path=pathlib.Path(folder)/'SYNTHETIC.json'; ledger=Ledger(path); ledger.begin(0,3)
            response=Response(b'toy!'); actual_read=response.read; real_fsync=os.fsync
            def read(n):
                saved=json.loads(path.read_text()); self.assertEqual(saved['charged_bytes'],4)
                self.assertEqual(saved['body_bytes'],0); self.assertGreater(sync.call_count,0)
                return actual_read(n)
            response.read=read
            with mock.patch('charades_range_media_clock_pilot.os.fsync',wraps=real_fsync) as sync:
                self.assertEqual(read_response(response,0,3,100,'"toy-etag"',ledger),b'toy!')

    def test_timeout_and_short_read_never_refund(self):
        for timeout in (True,False):
            ledger=Ledger(); ledger.begin(0,3); response=Response(b'to')
            if timeout: response.read=mock.Mock(side_effect=TimeoutError('SYNTHETIC'))
            with self.assertRaises((TimeoutError,PilotError)): read_response(response,0,3,100,'"toy-etag"',ledger)
            self.assertEqual(ledger.state['charged_bytes'],4)
            self.assertEqual(ledger.state['body_bytes'],0 if timeout else 2)
            ledger.finish('STOPPED'); ledger.begin(10,10); ledger.reserve(1); ledger.add(1)
            self.assertEqual(ledger.state['charged_bytes'],5)

    def test_pending_reservation_prevents_duplicate_read(self):
        ledger=Ledger(); ledger.begin(0,3); ledger.reserve(4)
        with self.assertRaises(PilotError): ledger.reserve(1)
        with self.assertRaises(PilotError): ledger.add(5)
        self.assertEqual(ledger.state['charged_bytes'],4)

    def test_ledger_write_failure_blocks_response_read(self):
        with tempfile.TemporaryDirectory() as folder:
            path=pathlib.Path(folder)/'SYNTHETIC.json'; ledger=Ledger(path); ledger.begin(0,3)
            response=Response(b'toy!')
            with mock.patch('charades_range_media_clock_pilot.os.fsync',side_effect=OSError('SYNTHETIC FSYNC')):
                with self.assertRaises(OSError): read_response(response,0,3,100,'"toy-etag"',ledger)
            self.assertEqual(response.calls,0); self.assertTrue(path.with_suffix('.next').exists())
            with self.assertRaises(PilotError): Ledger(path)

    def test_text_and_range_share_conservative_total_budget(self):
        ledger=Ledger(); ledger.state['charged_bytes']=NET_LIMIT-4
        client=RangeClient(ledger,100,'"toy-etag"')
        response=Response(b'to',status=200,headers={'Content-Length':'2'}); response.geturl=lambda:PAGE
        with mock.patch.object(client.opener,'open',return_value=response): self.assertEqual(client.text(PAGE,2),b'to')
        with mock.patch.object(client.opener,'open') as network:
            with self.assertRaises(PilotError): client.get(0,3)
        network.assert_not_called(); self.assertEqual(ledger.state['charged_bytes'],NET_LIMIT-2)

    def test_text_read_prepaid_not_recovered_on_truncation(self):
        ledger=Ledger(); client=RangeClient(ledger,100,'"toy-etag"')
        response=Response(b'to',status=200,headers={'Content-Length':'4'}); response.geturl=lambda:LICENSE
        with mock.patch.object(client.opener,'open',return_value=response):
            with self.assertRaisesRegex(PilotError,'TRUNCATED'): client.text(LICENSE,4)
        self.assertEqual(ledger.state['charged_bytes'],4); self.assertEqual(ledger.state['body_bytes'],2)

    def test_weak_etag_and_changed_source_total_rejected(self):
        for value in ('W/"weak"','unquoted',None):
            with self.assertRaises(PilotError): strong_etag(value)
        response=Response(b'',status=200,headers={'Content-Type':'application/zip','Content-Length':'13000000000','ETag':'"strong"'})
        self.assertEqual(head_identity(response),(13000000000,'"strong"'))
        for headers in ({'Content-Encoding':'gzip'},{'ETag':'W/"weak"'},{'Content-Length':'unknown'}):
            changed=Response(b'',status=200,headers=dict(response.headers,**headers))
            with self.assertRaises(PilotError): head_identity(changed)
        wrong=Response(b'toy!'); wrong.headers['Content-Range']='bytes 0-3/101'
        ledger=Ledger(); ledger.begin(0,3)
        with self.assertRaises(PilotError): read_response(wrong,0,3,100,'"toy-etag"',ledger)
        self.assertEqual(wrong.calls,0); self.assertEqual(ledger.state['charged_bytes'],0)

    def test_13gb_whole_get_and_range_over_budget_forbidden(self):
        with self.assertRaises(PilotError): fixed_request(URL,'GET',{'Accept-Encoding':'identity'})
        ledger=Ledger(); client=RangeClient(ledger,13000000000,'"strong"')
        with mock.patch.object(client.opener,'open') as network:
            with self.assertRaises(PilotError): client.get(0,13000000000-1)
        network.assert_not_called()

    def test_global_ffprobe_priority_conflict_cannot_switch_tools(self):
        from charades_range_media_clock_pilot import find_ffprobe
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder); tool=root/'VLM-Research-Isolated/CPU-Tools/ffprobe/bin/ffprobe.exe'
            tool.parent.mkdir(parents=True); tool.write_bytes(b'SYNTHETIC NOT EXECUTABLE')
            with mock.patch.dict(os.environ,{'LOCALAPPDATA':str(root),'VLM_ORIGINAL_WORKSPACE':str(root/'SYNTHETIC-RESEARCH')}), \
                 mock.patch('charades_range_media_clock_pilot.shutil.which',return_value=str(root/'OTHER.exe')):
                with self.assertRaisesRegex(PilotError,'PRIORITY_CONFLICT'): find_ffprobe()

    def test_closed_017_blocked_before_any_tool_or_asset(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe') as tool, \
             mock.patch('charades_range_media_clock_pilot.fixed_preflight') as assets, \
             mock.patch('charades_range_media_clock_pilot.subprocess.run') as process:
            with self.assertRaisesRegex(PilotError,'ALREADY_REPORTED'): run_pilot(True,'VLM-BATCH-017')
        tool.assert_not_called(); assets.assert_not_called(); process.assert_not_called()

    def test_018_exact_contract_and_017_receipt_pins(self):
        import charades_range_media_clock_pilot as pilot
        docs=pathlib.Path(__file__).resolve().parent.parent
        self.assertEqual(pilot.PARENT,'VLM-BATCH-018')
        contract=(docs/'docs/codex-artifacts/VLM-BATCH-018/README.md').read_text(encoding='utf-8')
        self.assertEqual(hashlib.sha256(contract.encode()).hexdigest(),pilot.CONTRACT_SHA)
        import re
        results=(docs/'docs/codex-results.md').read_text(encoding='utf-8')
        section=re.search(r'^### VLM-BATCH-017\s.*?(?=^### |\Z)',results,re.M|re.S).group().rstrip()
        self.assertEqual(hashlib.sha256(section.encode()).hexdigest(),pilot.HISTORY_SHA['VLM-BATCH-017'])

    def test_synthetic_original_context_ancestor_checks_are_mocked(self):
        from charades_range_media_clock_pilot import find_ffprobe
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)
            with mock.patch.dict(os.environ,{'LOCALAPPDATA':str(root),'VLM_ORIGINAL_WORKSPACE':'SYNTHETIC-RESEARCH'}), \
                 mock.patch('charades_metadata_audit.check_ancestors',side_effect=PilotError('SYNTHETIC_REPARSE')) as ancestors, \
                 mock.patch.object(pathlib.Path,'open',side_effect=AssertionError('NO_ASSET_READ')) as assets:
                with self.assertRaisesRegex(PilotError,'SYNTHETIC_REPARSE'): find_ffprobe()
            assets.assert_not_called()
            self.assertEqual(len(ancestors.call_args_list),1)
            self.assertIn(root,ancestors.call_args.args[0].parents)


if __name__=='__main__': unittest.main()
