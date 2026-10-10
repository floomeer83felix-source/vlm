"""Synthetic-only BATCH-015 tests. No network, supplier payload, real media or GPU."""
import io
import json
import os
import pathlib
import ssl
import stat
import subprocess
import tempfile
import unittest
import urllib.request
import zipfile
from unittest import mock
import isolated_ffprobe_resumer as r
from isolated_ffprobe_installer import NoRedirect


def old_state():
    return {'body_bytes':r.OLD_BODY,'get_attempts':4,'head_attempts':3,
            'successful_zip_gets':0,'version_runs':0,'status':'BLOCKED','reason':'timeout',
            'events':[{'kind':'TEXT','read':27484,'status':'COMPLETE'},
                      {'kind':'TEXT','read':52159,'status':'COMPLETE'},
                      {'kind':'TEXT','read':64,'status':'COMPLETE'},
                      {'kind':'PACKAGE','read':r.OFFSET,'status':'STOPPED'}]}


def snapshot():
    return {'old':old_state(),'part_sha':'SYNTHETIC','parent_sha':'SYNTHETIC',
            'part_identity':[1,2],'initial_disk_bytes':r.OFFSET+574}


def fixture(root):
    for d in ('incoming','local-audit','bin','licenses'): (root/d).mkdir()
    part=root/r.PART_NAME
    with part.open('wb') as f:
        f.write(b'PK\x03\x04'); f.seek(r.OFFSET-1); f.write(b'X')
    parent=root/r.OLD_NAME
    text=json.dumps(old_state()); assert len(text)<574
    parent.write_text(text+' '*(574-len(text)),encoding='ascii')
    return part,parent


class Response:
    def __init__(self,body=b'X',status=206,start=None,end=None,total=None,etag='"synthetic"'):
        start=r.OFFSET-1 if start is None else start
        end=start+len(body)-1 if end is None else end
        total=r.OFFSET+10 if total is None else total
        self.status=status; self.url=r.PACKAGE; self.body=io.BytesIO(body); self.read_calls=0
        self.headers={'Content-Length':str(len(body)),'Content-Range':f'bytes {start}-{end}/{total}',
                      'ETag':etag,'Content-Encoding':'identity'}
    def geturl(self): return self.url
    def read(self,n): self.read_calls+=1; return self.body.read(n)
    def __enter__(self): return self
    def __exit__(self,*args): pass


class ResumeTests(unittest.TestCase):
    def test_no_proxy_under_polluted_environment(self):
        with mock.patch.dict(os.environ,{'HTTPS_PROXY':'http://invalid.example:1','HTTP_PROXY':'http://invalid.example:1'}), \
             mock.patch('urllib.request.getproxies',side_effect=AssertionError('system/env proxy read')):
            opener=r.direct_opener()
        self.assertFalse(any(getattr(h,'proxies',{}) for h in opener.handlers))

    def test_tls_verified_no_redirect(self):
        context=ssl.create_default_context()
        self.assertTrue(context.check_hostname); self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)
        self.assertIsNone(NoRedirect().redirect_request(None))
        https=next(h for h in r.direct_opener().handlers if isinstance(h,urllib.request.HTTPSHandler))
        self.assertTrue(https._context.check_hostname)

    def test_weak_missing_invalid_etags_refused(self):
        for v in (None,'W/"weak"','unquoted','""','"bad\nvalue"'):
            with self.assertRaises(r.InstallError): r.strong_etag(v)
        self.assertEqual(r.strong_etag('"strong"'),'"strong"')

    def test_head_identity_and_fixed_source(self):
        h={'Content-Length':str(r.OFFSET+10),'Content-Type':'application/zip','ETag':'"strong"'}
        self.assertEqual(r.head_identity(200,h,r.PACKAGE),(r.OFFSET+10,'"strong"'))
        for status,url in ((302,r.PACKAGE),(200,'https://invalid.example/charades.zip')):
            with self.assertRaises(r.InstallError): r.head_identity(status,h,url)

    def test_head_lengths_encoding_type_budget(self):
        baseline={'Content-Length':str(r.OFFSET+10),'Content-Type':'application/zip','ETag':'"strong"'}
        for changes in ({'Content-Length':'unknown'},{'Content-Length':str(r.OFFSET)},
                        {'Content-Length':str(r.NET_LIMIT+1)},{'Content-Type':'text/html'},
                        {'Content-Encoding':'gzip'},{'ETag':'W/"weak"'}):
            with self.assertRaises(r.InstallError): r.head_identity(200,dict(baseline,**changes),r.PACKAGE)

    def test_206_precise_headers(self):
        response=Response()
        r.range_identity(response,r.OFFSET-1,r.OFFSET-1,r.OFFSET+10,'"synthetic"')

    def test_200_416_no_body_read(self):
        for status in (200,416,302):
            response=Response(status=status)
            with self.assertRaises(r.InstallError): r.range_identity(response,r.OFFSET-1,r.OFFSET-1,r.OFFSET+10,'"synthetic"')
            self.assertEqual(response.read_calls,0)

    def test_range_bad_offsets_length_encoding_etag(self):
        for h in ({'Content-Range':'bytes 0-0/1'},{'Content-Length':'2'},
                  {'Content-Encoding':'gzip'},{'ETag':'"changed"'},{'ETag':'W/"weak"'}):
            response=Response(); response.headers.update(h)
            with self.assertRaises(r.InstallError): r.range_identity(response,r.OFFSET-1,r.OFFSET-1,r.OFFSET+10,'"synthetic"')

    def test_request_if_range_and_no_arbitrary_url(self):
        req=r.range_request(r.OFFSET,r.OFFSET+9,'"strong"')
        self.assertEqual(req.full_url,r.PACKAGE)
        self.assertEqual(req.get_header('Range'),f'bytes={r.OFFSET}-{r.OFFSET+9}')
        self.assertEqual(req.get_header('If-range'),'"strong"')
        self.assertEqual(req.get_header('Accept-encoding'),'identity')
        with self.assertRaises(r.InstallError): r.range_request(0,9,'"strong"')

    def test_old_ledger_exact_events_and_no_reset(self):
        r.old_contract(old_state())
        for field,value in (('body_bytes',0),('get_attempts',3),('successful_zip_gets',1),('version_runs',1)):
            state=old_state(); state[field]=value
            with self.assertRaises(r.InstallError): r.old_contract(state)
        state=old_state(); state['events'][-1]['read']-=1
        with self.assertRaises(r.InstallError): r.old_contract(state)

    def test_local_part_size_magic_and_unexpected_asset(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); part,parent=fixture(root)
            r.local_audit(root)
            extra=root/'local-audit/prior-resume.json'; extra.write_text('SYNTHETIC')
            with self.assertRaises(r.InstallError): r.local_audit(root)
            extra.unlink()
            with part.open('r+b') as f: f.write(b'BAD!')
            with self.assertRaises(r.InstallError): r.local_audit(root)

    def test_local_prefix_mutation_caught(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); part,parent=fixture(root); snap=r.local_audit(root)
            r.unchanged(root,snap)
            with part.open('r+b') as f: f.seek(10); f.write(b'X')
            with self.assertRaises(r.InstallError): r.unchanged(root,snap)

    def test_inherited_budget_persistent_old_not_rewritten(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); part,parent=fixture(root); original=parent.read_bytes()
            ledger=r.ResumeLedger(root/r.NEW_NAME,r.local_audit(root))
            self.assertEqual(ledger.state['body_bytes'],r.OLD_BODY)
            ledger.begin('PROBE',1); ledger.reserve(1); ledger.received(1); ledger.finish('COMPLETE')
            saved=json.loads((root/r.NEW_NAME).read_text())
            self.assertEqual(saved['body_bytes'],r.OLD_BODY+1); self.assertEqual(saved['get_attempts'],5)
            self.assertEqual(parent.read_bytes(),original)
            with self.assertRaises(FileExistsError): r.ResumeLedger(root/r.NEW_NAME,snapshot())

    def test_crash_reservation_durable_before_read(self):
        with tempfile.TemporaryDirectory() as d:
            path=pathlib.Path(d)/'SYNTHETIC.json'; ledger=r.ResumeLedger(path,snapshot()); ledger.begin('PROBE',1)
            response=Response()
            def timeout_read(n):
                saved=json.loads(path.read_text()); self.assertEqual(saved['charged_bytes'],r.OLD_BODY+1)
                self.assertEqual(saved['new_body_bytes'],0)
                raise TimeoutError('SYNTHETIC')
            response.read=timeout_read
            with self.assertRaises(TimeoutError): r.transfer(response,ledger,1)
            self.assertEqual(ledger.state['charged_bytes'],r.OLD_BODY+1)

    def test_chunk_global_and_event_budget_rejection(self):
        ledger=r.ResumeLedger(None,snapshot()); ledger.begin('PROBE',1)
        for n in (r.CHUNK+1,0,2):
            with self.assertRaises(r.InstallError): ledger.reserve(n)
        ledger.state['charged_bytes']=r.NET_LIMIT
        with self.assertRaises(r.InstallError): ledger.reserve(1)

    def test_only_two_gets_probe_then_suffix_no_retry(self):
        ledger=r.ResumeLedger(None,snapshot())
        with self.assertRaises(r.InstallError): ledger.begin('SUFFIX',1)
        ledger.begin('PROBE',1); ledger.reserve(1); ledger.received(1); ledger.finish('COMPLETE')
        ledger.begin('SUFFIX',10)
        with self.assertRaises(r.InstallError): ledger.begin('SUFFIX',10)

    def test_failed_probe_never_unlocks_suffix(self):
        ledger=r.ResumeLedger(None,snapshot()); ledger.begin('PROBE',1); ledger.finish('STOPPED')
        with self.assertRaises(r.InstallError): ledger.begin('SUFFIX',10)

    def test_short_body_stops_without_second_read(self):
        ledger=r.ResumeLedger(None,snapshot()); ledger.begin('PROBE',4); response=Response(b'X')
        with self.assertRaises(r.InstallError): r.transfer(response,ledger,4)
        self.assertEqual(response.read_calls,1); self.assertEqual(ledger.state['new_body_bytes'],1)
        self.assertEqual(ledger.state['new_reserved_bytes'],4)

    def test_reader_overrun_cannot_be_counted_or_written(self):
        ledger=r.ResumeLedger(None,snapshot()); ledger.begin('PROBE',1); response=Response()
        response.read=lambda n:b'XX'
        with self.assertRaises(r.InstallError): r.transfer(response,ledger,1)
        self.assertEqual(ledger.state['new_body_bytes'],0)

    def test_successful_synthetic_append_retains_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); part,parent=fixture(root); snap=r.local_audit(root)
            ledger=r.ResumeLedger(root/r.NEW_NAME,snap); ledger.begin('PROBE',1)
            r.transfer(Response(),ledger,1); ledger.begin('SUFFIX',3)
            with part.open('ab') as writer:
                r.transfer(Response(b'XYZ'),ledger,3,writer,root,r.OFFSET)
            self.assertEqual(part.stat().st_size,r.OFFSET+3)
            with part.open('rb') as f: self.assertEqual(f.read(4),b'PK\x03\x04'); f.seek(r.OFFSET); self.assertEqual(f.read(),b'XYZ')
            self.assertEqual(r.file_digest(parent),snap['parent_sha'])

    def test_full_sha_mismatch_no_extract_or_process(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); part=root/'SYNTHETIC.part'; part.write_bytes(b'PK\x03\x04FAKE')
            ledger=r.ResumeLedger(None,snapshot())
            with mock.patch.object(r,'exclusive_extract') as extract, mock.patch.object(r.subprocess,'run') as process:
                with self.assertRaises(r.InstallError): r.deploy_archive(root,part,ledger,part.stat().st_size)
                extract.assert_not_called(); process.assert_not_called()

    def test_zip64_crc_license_and_whitelist(self):
        data=io.BytesIO(); prefix='ffmpeg-9.0.2-essentials_build'
        with zipfile.ZipFile(data,'w') as z:
            with z.open(prefix+'/bin/ffprobe.exe','w',force_zip64=True) as f: f.write(b'SYNTHETIC')
            z.writestr(prefix+'/LICENSE',b'SYNTHETIC')
        with zipfile.ZipFile(io.BytesIO(data.getvalue())) as z:
            self.assertEqual(len(r.safe_tool_members(z.infolist(),len(data.getvalue()))),2)
            self.assertIsNone(z.testzip())
            with self.assertRaises(r.InstallError): r.safe_tool_members(z.infolist()[:1],100)
        damaged=bytearray(data.getvalue()); damaged[damaged.find(b'SYNTHETIC')]^=1
        with zipfile.ZipFile(io.BytesIO(damaged)) as z: self.assertIsNotNone(z.testzip())

    def test_zip_dangerous_duplicate_dll_symlink(self):
        prefix='ffmpeg-9.0.2-essentials_build'
        base=[zipfile.ZipInfo(prefix+'/bin/ffprobe.exe'),zipfile.ZipInfo(prefix+'/LICENSE')]
        base[0].file_size=10; base[1].file_size=10
        link=zipfile.ZipInfo('link'); link.external_attr=(stat.S_IFLNK|0o777)<<16
        for info in (zipfile.ZipInfo('../escape'),zipfile.ZipInfo(prefix+'/bin/FFPROBE.exe'),zipfile.ZipInfo('extra.dll'),link):
            with self.assertRaises(r.InstallError): r.safe_tool_members(base+[info],100)

    def test_exe_existing_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d); target=root/'ffprobe.exe'; target.write_bytes(b'EXISTING')
            data=io.BytesIO()
            with zipfile.ZipFile(data,'w') as z: z.writestr('toy',b'SYNTHETIC')
            with zipfile.ZipFile(io.BytesIO(data.getvalue())) as z:
                with self.assertRaises(r.InstallError): r.exclusive_extract(z,z.getinfo('toy'),target,root,r.ResumeLedger(None,snapshot()))
            self.assertEqual(target.read_bytes(),b'EXISTING')

    def test_version_failure_wrong_version_timeout_scope(self):
        for p in (mock.Mock(returncode=1,stdout=b''),mock.Mock(returncode=0,stdout=b'ffprobe version 8.0.1')):
            with self.assertRaises(r.InstallError): r.version_result(p)
        with mock.patch.object(r.subprocess,'run',side_effect=subprocess.TimeoutExpired('SYNTHETIC',10)):
            with self.assertRaises(subprocess.TimeoutExpired): r.subprocess.run(['SYNTHETIC','-version'],timeout=10)

    def test_public_receipt_redacts_identity_and_private_hash(self):
        ledger=r.ResumeLedger(None,snapshot()); ledger.state['heads']=[{'etag':'"PRIVATE"'}]
        receipt=r.public_receipt(ledger.state)
        self.assertNotIn('heads',receipt); self.assertNotIn('parent_sha',receipt)
        self.assertNotIn('initial_part_sha',receipt); self.assertNotIn('executable_sha',receipt)

    def test_parent_completed_or_other_ready_refused(self):
        text='### VLM-BATCH-014 history\n### VLM-BATCH-015 completed\n'
        board='| VLM-BATCH-015 | P1 | **READY** | Codex | task |'
        with mock.patch.object(pathlib.Path,'read_text',side_effect=[text,board]):
            with self.assertRaises(r.InstallError): r.parent_gate()


if __name__=='__main__': unittest.main()
