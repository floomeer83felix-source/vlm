"""Only synthetic HTTP, ZIP, identities and clocks; never connects to a server."""
import io
import json
import struct
import unittest
import zipfile
import zlib
from unittest import mock
from charades_range_media_clock_pilot import (
    PilotError,Ledger,URL,NET_LIMIT,DISK_LIMIT,validate_range,read_response,eocd,
    central_directory,match_two,local_header,expand_member,select_cases,safe_name,
    validate_extra,ffprobe_command,classify_clock,public_receipt,NoRedirect,run_pilot)


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

    def test_missing_tool_stops_before_network_or_storage(self):
        with mock.patch('charades_range_media_clock_pilot.find_ffprobe',side_effect=PilotError('BLOCKED_EXISTING_FFPROBE_NOT_FOUND')), \
             mock.patch('charades_range_media_clock_pilot.urllib.request.build_opener') as network:
            with self.assertRaises(PilotError): run_pilot()
            network.assert_not_called()


if __name__=='__main__': unittest.main()
