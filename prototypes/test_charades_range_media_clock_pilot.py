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
from unittest import mock
from charades_range_media_clock_pilot import (
    PilotError,Ledger,URL,NET_LIMIT,DISK_LIMIT,validate_range,read_response,eocd,
    central_directory,match_two,local_header,expand_member,select_cases,safe_name,
    validate_extra,ffprobe_command,classify_clock,public_receipt,NoRedirect,run_pilot)
from charades_range_media_clock_pilot import zip64_fields,authorize_parent,official_anchor,transfer_two


class Response:
    def __init__(self,body,status=206,headers=None):
        self.body=io.BytesIO(body); self.status=status; self.calls=0
        self.headers=headers or {'Content-Range':'bytes 0-3/100','Content-Length':'4','ETag':'toy-etag','Content-Encoding':'identity'}
    def geturl(self): return URL
    def read(self,n): self.calls+=1; return self.body.read(n)


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
    def test_good_206_exact_body_count(self):
        ledger=Ledger(); ledger.begin(0,3)
        self.assertEqual(read_response(Response(b'toy!'),0,3,100,'toy-etag',ledger),b'toy!')
        self.assertEqual(ledger.state['body_bytes'],4)

    def test_200_rejected_before_body(self):
        r=Response(b'SYNTHETIC WHOLE ARCHIVE',status=200); ledger=Ledger(); ledger.begin(0,3)
        with self.assertRaisesRegex(PilotError,'REQUIRES_206'): read_response(r,0,3,100,'toy-etag',ledger)
        self.assertEqual(r.calls,0); self.assertEqual(ledger.state['body_bytes'],0)

    def test_range_encoding_length_etag_and_domain_rejected(self):
        good=Response(b'toy!').headers
        for key,value in (('Content-Range','bytes 1-4/100'),('Content-Encoding','gzip'),('Content-Length','40'),('ETag','different')):
            bad=dict(good); bad[key]=value
            with self.assertRaises(PilotError): validate_range(206,bad,0,3,100,'toy-etag',URL)
        with self.assertRaises(PilotError): validate_range(206,good,0,3,100,'toy-etag','https://invalid.example/')
        with self.assertRaisesRegex(PilotError,'REDIRECT_FORBIDDEN'): NoRedirect().redirect_request(None)

    def test_cumulative_budget_and_failure_bytes_not_reset(self):
        ledger=Ledger(); ledger.state['body_bytes']=NET_LIMIT-3
        with self.assertRaises(PilotError): ledger.begin(0,3)
        ledger.begin(0,2); ledger.add(2); ledger.finish('STOPPED')
        self.assertEqual(ledger.state['body_bytes'],NET_LIMIT-1)
        with self.assertRaises(PilotError): ledger.add(2)

    def test_request_count_and_disk_budget(self):
        ledger=Ledger(); ledger.state['get_attempts']=12
        with self.assertRaises(PilotError): ledger.begin(0,0)
        with self.assertRaises(PilotError): ledger.disk(DISK_LIMIT+1)
        ledger.disk(100); self.assertEqual(ledger.state['peak_local_bytes'],100)

    def test_truncated_response_keeps_read_account(self):
        ledger=Ledger(); ledger.begin(0,3)
        with self.assertRaisesRegex(PilotError,'TRUNCATED'): read_response(Response(b'to'),0,3,100,'toy-etag',ledger)
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
        with mock.patch('charades_range_media_clock_pilot.shutil.which',return_value=None), \
             mock.patch('charades_range_media_clock_pilot.pathlib.Path.is_file',return_value=True), \
             mock.patch('charades_range_media_clock_pilot.pathlib.Path.resolve',return_value=pathlib.Path('SYNTHETIC/.conda/ffprobe.exe')):
            with self.assertRaisesRegex(PilotError,'FFPROBE_NOT_FOUND'): find_ffprobe()

    def test_preflight_only_never_creates_network_after_tool_success(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe',return_value=pathlib.Path('SYNTHETIC-TOOL')), \
             mock.patch('charades_range_media_clock_pilot.subprocess.run',return_value=mock.Mock(stdout=b'ffprobe version SYNTHETIC')), \
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
            ledger.begin(0,3); ledger.add(2); ledger.finish('STOPPED')
            self.assertEqual(json.loads(file.read_text())['body_bytes'],2)
            with self.assertRaisesRegex(PilotError,'ALREADY_EXISTS'): Ledger(file)

    def test_coordinator_transfer_two_with_synthetic_range_client(self):
        data=toy_zip()
        ledger=Ledger()
        class Client:
            total=len(data)
            def __init__(self): self.ledger=ledger
            def get(self,start,end):
                ledger.begin(start,end); ledger.add(end-start+1); ledger.finish('COMPLETE')
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
            status=200; headers={'Content-Type':'application/zip','Content-Length':str(len(data)),'ETag':'toy-etag'}
            def geturl(self): return URL
            def __enter__(self): return self
            def __exit__(self,*args): pass
        class Client:
            def __init__(self,ledger,total,etag):
                self.ledger=ledger; self.total=total; self.etag=etag; self.opener=mock.Mock(open=lambda *a,**k:Head())
            def text(self,url,limit):
                value=('<a href="'+URL+'">Data (scaled to 480p, 13 GB)</a>').encode() if url==PAGE else b'SYNTHETIC-LICENSE'
                self.ledger.begin(0,limit-1); self.ledger.add(len(value)); self.ledger.finish('COMPLETE'); return value
            def get(self,start,end):
                self.ledger.begin(start,end); self.ledger.add(end-start+1); self.ledger.finish('COMPLETE')
                return data[start:end+1]
        with tempfile.TemporaryDirectory() as folder:
            base=pathlib.Path(folder); meta=base/'synthetic-metadata'; meta.mkdir()
            (meta/'classes.txt').write_text('toy-class Synthetic')
            (meta/'train.csv').write_text('id,subject,actions,length\nSYNTHETIC-A,PERSON-A,toy-class 0 12,10\nSYNTHETIC-B,PERSON-B,toy-class 0 5,10\n')
            probe={'streams':[{'time_base':'1/10','avg_frame_rate':'10/1','r_frame_rate':'10/1','start_time':'0','duration':'10'}],
                   'format':{'duration':'10'},'packets':[{'pts':'0','duration':'1'},{'pts':'99','duration':'1'}]}
            def fake_subprocess(command,**kwargs):
                return mock.Mock(stdout=b'ffprobe version SYNTHETIC') if '-version' in command else mock.Mock(stdout=json.dumps(probe).encode())
            with mock.patch('charades_range_media_clock_pilot.find_ffprobe',return_value=pathlib.Path('SYNTHETIC-TOOL')), \
                 mock.patch('charades_range_media_clock_pilot.subprocess.run',fake_subprocess), \
                 mock.patch('charades_range_media_clock_pilot.authorize_parent'), \
                 mock.patch('charades_range_media_clock_pilot.fixed_preflight',return_value=(base/'synthetic-pilot',{'classes':meta/'classes.txt','train':meta/'train.csv'})), \
                 mock.patch('charades_range_media_clock_pilot.RangeClient',Client), \
                 mock.patch('charades_range_media_clock_pilot.hashlib.sha256',hash_only_synthetic_license), \
                 mock.patch('unittest.TextTestRunner.run',return_value=mock.Mock(testsRun=24,wasSuccessful=lambda:True)):
                out=run_pilot(True,'VLM-BATCH-999')
            self.assertEqual(out['status'],'CASE_LIMITED_COMPLETE')
            self.assertEqual(out['saved_videos'],2)
            self.assertNotIn('SYNTHETIC-A',json.dumps(out))
            self.assertEqual(out['CASE_CONTROL'],'LENGTH_APPROX_MATCH')


if __name__=='__main__': unittest.main()
