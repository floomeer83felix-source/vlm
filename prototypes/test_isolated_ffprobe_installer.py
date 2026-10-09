"""Synthetic-only supply-chain, HTTP, ZIP and version tests; never downloads binaries."""
import hashlib
import io
import pathlib
import ssl
import stat
import subprocess
import tempfile
import unittest
import urllib.request
import zipfile
from unittest import mock
from isolated_ffprobe_installer import (
    VERSION,PUBLISHER_SHA,FFMPEG,GYAN,PACKAGE,CHECKSUM,ALIAS,ALIAS_SHA,NET_LIMIT,DISK_LIMIT,
    InstallError,Ledger,NoRedirect,direct_opener,source_url,response_policy,stream_body,
    checksum_text,publisher_pages,alias_head,safe_tool_members,package_verified,version_result,exclusive_extract,create_new_root)


ROOT='ffmpeg-9.0.2-essentials_build'


def infos(extra=()):
    exe=zipfile.ZipInfo(ROOT+'/bin/ffprobe.exe'); exe.file_size=100
    license=zipfile.ZipInfo(ROOT+'/LICENSE'); license.file_size=10
    return [exe,license]+list(extra)


class Response:
    status=200
    def __init__(self,body,length='4'):
        self.body=io.BytesIO(body); self.headers={} if length is None else {'Content-Length':length}
        self.requested=PACKAGE; self.calls=0
    def geturl(self): return self.requested
    def read(self,n): self.calls+=1; return self.body.read(n)


class InstallerTests(unittest.TestCase):
    def test_new_nested_root_parent_creation_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            root=pathlib.Path(folder)/'SYNTHETIC-TOOLS'/'ffprobe'
            create_new_root(root)
            self.assertTrue(root.is_dir())
            with self.assertRaisesRegex(InstallError,'ALREADY_EXISTS'): create_new_root(root)
    def test_no_proxy_inherited_and_tls_verification(self):
        with mock.patch('urllib.request.getproxies',side_effect=AssertionError('must not query proxies')):
            opener=direct_opener()
        self.assertFalse(any(getattr(h,'proxies',{}) for h in opener.handlers))
        context=ssl.create_default_context(); self.assertTrue(context.check_hostname)
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)

    def test_fixed_https_sources_only_and_redirect_not_followed(self):
        source_url(PACKAGE,'GET'); source_url(ALIAS,'HEAD')
        for url in ('http://www.gyan.dev/file','https://invalid.example/file',ALIAS):
            with self.assertRaises(InstallError): source_url(url,'GET')
        self.assertIsNone(NoRedirect().redirect_request(None))

    def test_response_status_encoding_length_and_final_url(self):
        self.assertEqual(response_policy(200,{'content-length':'4'},PACKAGE,PACKAGE,4),4)
        self.assertIsNone(response_policy(200,{},PACKAGE,PACKAGE,4))
        for status,headers,url in ((302,{},PACKAGE),(200,{'Content-Encoding':'gzip'},PACKAGE),
                                  (200,{'Content-Length':'5'},PACKAGE),(200,{},'https://invalid.example/')):
            with self.assertRaises(InstallError): response_policy(status,headers,url,PACKAGE,4)

    def test_stream_known_size_and_sha(self):
        ledger=Ledger(); ledger.begin('PACKAGE',10)
        n,sha,data=stream_body(Response(b'toy!'),ledger,10)
        self.assertEqual((n,data),(4,b'toy!'))
        self.assertEqual(sha,hashlib.sha256(b'toy!').hexdigest())
        self.assertEqual(ledger.state['body_bytes'],4)

    def test_unknown_size_bounded_and_truncation_counted(self):
        ledger=Ledger(); ledger.begin('TEXT',10)
        self.assertEqual(stream_body(Response(b'toy!',None),ledger,10)[0],4)
        ledger=Ledger(); ledger.begin('TEXT',10)
        with self.assertRaisesRegex(InstallError,'TRUNCATED'): stream_body(Response(b'to'),ledger,10)
        self.assertEqual(ledger.state['body_bytes'],2)

    def test_budget_across_failure_requests_and_read_reservation(self):
        ledger=Ledger(); ledger.state['body_bytes']=NET_LIMIT-2; ledger.begin('PACKAGE',10)
        with self.assertRaisesRegex(InstallError,'BUDGET'): stream_body(Response(b'toy!'),ledger,10)
        self.assertEqual(ledger.state['body_bytes'],NET_LIMIT-2)
        ledger.received(2); ledger.finish('STOPPED')
        with self.assertRaises(InstallError): ledger.begin('PACKAGE',10)
        with self.assertRaises(InstallError): ledger.disk(DISK_LIMIT+1)

    def test_ledger_persists_before_reads_and_no_reset(self):
        with tempfile.TemporaryDirectory() as folder:
            p=pathlib.Path(folder)/'ledger.json'; ledger=Ledger(p); ledger.begin('TEXT',10)
            import json
            self.assertEqual(json.loads(p.read_text())['events'][0]['status'],'STARTED')
            ledger.received(2); ledger.finish('STOPPED')
            self.assertEqual(json.loads(p.read_text())['body_bytes'],2)
            with self.assertRaises(InstallError): Ledger(p)

    def test_publisher_checksum_exact_version(self):
        self.assertEqual(checksum_text((PUBLISHER_SHA+'\n').encode()),PUBLISHER_SHA)
        self.assertEqual(checksum_text((PUBLISHER_SHA+'  ffmpeg-9.0.2-essentials_build.zip').encode()),PUBLISHER_SHA)
        for value in ('0'*64,PUBLISHER_SHA+'  wrong.zip',PUBLISHER_SHA+'\n'+'0'*64):
            with self.assertRaises(InstallError): checksum_text(value.encode())
        with self.assertRaises(InstallError): package_verified('0'*64)

    def test_vendor_chain_and_alias_pin(self):
        f=('<a href="'+GYAN+'">Windows build</a>').encode()
        g=('<p>9.0.2 release essentials GPLv3</p><a href="'+ALIAS+'">zip</a><a href="'+ALIAS_SHA+'">hash</a>').encode()
        publisher_pages(f,g)
        with self.assertRaises(InstallError): publisher_pages(f,g.replace(b'9.0.2',b'8.0.1'))
        alias_head(302,{'location':PACKAGE},ALIAS,PACKAGE)
        with self.assertRaises(InstallError): alias_head(302,{'Location':'https://invalid.example/'},ALIAS,PACKAGE)
        with self.assertRaises(InstallError): alias_head(200,{},ALIAS,PACKAGE)

    def test_zip_whitelist_one_exe_and_license(self):
        other=zipfile.ZipInfo(ROOT+'/bin/ffmpeg.exe'); other.file_size=100
        selected=safe_tool_members(infos([other]),100)
        self.assertEqual({target for target,_ in selected.values()},{'bin/ffprobe.exe','licenses/LICENSE'})
        with self.assertRaises(InstallError): safe_tool_members([infos()[0]],100)
        duplicate=zipfile.ZipInfo('other/bin/ffprobe.exe'); duplicate.file_size=100
        with self.assertRaises(InstallError): safe_tool_members(infos([duplicate]),100)

    def test_zip_paths_null_case_collision_and_special(self):
        for name in ('../escape.exe','/escape.exe','C:/escape.exe','a\\b.exe','CON.txt','bad\x00name'):
            with self.assertRaises(InstallError): safe_tool_members(infos([zipfile.ZipInfo(name)]),100)
        with self.assertRaises(InstallError): safe_tool_members(infos([zipfile.ZipInfo(ROOT+'/license')]),100)
        link=zipfile.ZipInfo('link'); link.external_attr=(stat.S_IFLNK|0o777)<<16
        with self.assertRaises(InstallError): safe_tool_members(infos([link]),100)

    def test_zip_encrypted_zipbomb_dll_nested_and_limits(self):
        encrypted=zipfile.ZipInfo('secret'); encrypted.flag_bits=1
        huge=zipfile.ZipInfo('huge'); huge.file_size=DISK_LIMIT+1
        for item in (encrypted,huge,zipfile.ZipInfo('extra.dll'),zipfile.ZipInfo('inner.zip')):
            with self.assertRaises(InstallError): safe_tool_members(infos([item]),100)
        with self.assertRaises(InstallError): safe_tool_members(infos([zipfile.ZipInfo('x'+str(i)) for i in range(199)]),100)

    def test_zip64_stdlib_small_fixture_and_crc(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:
            with z.open(ROOT+'/bin/ffprobe.exe','w',force_zip64=True) as f: f.write(b'SYNTHETIC-EXE')
            z.writestr(ROOT+'/LICENSE',b'SYNTHETIC-LICENSE')
        with zipfile.ZipFile(io.BytesIO(data.getvalue())) as z:
            self.assertEqual(len(safe_tool_members(z.infolist(),len(data.getvalue()))),2)
            self.assertIsNone(z.testzip())
        broken=bytearray(data.getvalue()); p=broken.find(b'SYNTHETIC-EXE'); broken[p]^=1
        with zipfile.ZipFile(io.BytesIO(broken)) as z: self.assertIsNotNone(z.testzip())

    def test_extract_exclusive_no_overwrite(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z: z.writestr('toy',b'SYNTHETIC')
        with tempfile.TemporaryDirectory() as folder,zipfile.ZipFile(io.BytesIO(data.getvalue())) as z:
            root=pathlib.Path(folder); target=root/'ffprobe.exe'; ledger=Ledger()
            exclusive_extract(z,z.getinfo('toy'),target,root,ledger)
            self.assertEqual(target.read_bytes(),b'SYNTHETIC')
            with self.assertRaises(InstallError): exclusive_extract(z,z.getinfo('toy'),target,root,ledger)
            self.assertEqual(target.read_bytes(),b'SYNTHETIC')

    def test_version_health_scope_and_failure(self):
        process=mock.Mock(returncode=0,stdout=b'ffprobe version 9.0.2-SYNTHETIC\n')
        self.assertIn(VERSION,version_result(process))
        for p in (mock.Mock(returncode=1,stdout=b''),mock.Mock(returncode=0,stdout=b'ffprobe version 8.0.1')):
            with self.assertRaises(InstallError): version_result(p)
        with mock.patch('isolated_ffprobe_installer.subprocess.run',side_effect=subprocess.TimeoutExpired('SYNTHETIC',10)):
            with self.assertRaises(subprocess.TimeoutExpired): subprocess.run(['SYNTHETIC','-version'],timeout=10)


if __name__=='__main__': unittest.main()
