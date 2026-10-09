"""Fixed 9.0.2 publisher-hash deployment. Default preflight only; no media capability."""
import argparse
import hashlib
import html.parser
import json
import os
import pathlib
import platform
import re
import shutil
import ssl
import stat
import struct
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

VERSION='9.0.2'
PUBLISHER_SHA='60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba'
FFMPEG='https://ffmpeg.org/download.html'
GYAN='https://www.gyan.dev/ffmpeg/builds/'
PACKAGE=GYAN+'packages/ffmpeg-9.0.2-essentials_build.zip'
CHECKSUM=PACKAGE+'.sha256'
ALIAS=GYAN+'ffmpeg-release-essentials.zip'
ALIAS_SHA=ALIAS+'.sha256'
MIB=1024*1024
NET_LIMIT=150*MIB
DISK_LIMIT=512*MIB
TEXT_CAP=512*1024
GET_ALLOWED=frozenset((FFMPEG,GYAN,PACKAGE,CHECKSUM))
HEAD_ALLOWED=GET_ALLOWED|frozenset((ALIAS,ALIAS_SHA))


class InstallError(ValueError): pass


def header_value(headers,name,default=None):
    return next((v for k,v in headers.items() if k.lower()==name.lower()),default)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None


def direct_opener():
    context=ssl.create_default_context()
    if not context.check_hostname or context.verify_mode!=ssl.CERT_REQUIRED: raise InstallError('TLS_POLICY')
    return urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=context))


def source_url(url,method):
    allowed=GET_ALLOWED if method=='GET' else HEAD_ALLOWED
    if method not in ('GET','HEAD') or url not in allowed or urllib.parse.urlsplit(url).scheme!='https':
        raise InstallError('SOURCE_URL_FORBIDDEN')


class Ledger:
    def __init__(self,path=None):
        self.path=path; self.state={'get_attempts':0,'head_attempts':0,'body_bytes':0,'successful_zip_gets':0,
                                   'peak_local_bytes':0,'version_runs':0,'events':[],'status':'PREFLIGHT'}
        if path is not None:
            if path.exists(): raise InstallError('LEDGER_EXISTS')
            self.save()
    def save(self):
        if self.path is None: return
        from charades_metadata_audit import check_ancestors
        tmp=self.path.with_suffix('.next'); check_ancestors(self.path); check_ancestors(tmp)
        with tmp.open('x',encoding='utf-8') as f: json.dump(self.state,f,indent=2)
        os.replace(tmp,self.path)
    def begin(self,label,limit):
        if limit<=0 or self.state['body_bytes']>=NET_LIMIT: raise InstallError('NETWORK_BUDGET')
        self.state['get_attempts']+=1; self.state['events'].append({'kind':label,'read':0,'status':'STARTED'})
        self.save()
    def reserve_read(self,n):
        if n<0 or self.state['body_bytes']+n>NET_LIMIT: raise InstallError('NETWORK_BUDGET')
    def received(self,n):
        self.reserve_read(n); self.state['body_bytes']+=n; self.state['events'][-1]['read']+=n; self.save()
    def finish(self,status):
        self.state['events'][-1]['status']=status; self.save()
    def disk(self,n):
        if n<0 or n>DISK_LIMIT: raise InstallError('DISK_BUDGET')
        self.state['peak_local_bytes']=max(self.state['peak_local_bytes'],n); self.save()


def response_policy(status,headers,final_url,requested,cap):
    if status!=200 or final_url!=requested: raise InstallError('HTTP_STATUS_OR_REDIRECT')
    if header_value(headers,'Content-Encoding','identity').lower()!='identity': raise InstallError('CONTENT_ENCODING')
    raw=header_value(headers,'Content-Length')
    try: length=None if raw is None else int(raw)
    except ValueError: raise InstallError('CONTENT_LENGTH_INVALID') from None
    if length is not None and not 0<length<=cap: raise InstallError('CONTENT_LENGTH_LIMIT')
    return length


def stream_body(response,ledger,cap,writer=None):
    length=response_policy(response.status,response.headers,response.geturl(),response.requested,cap)
    if length is not None: ledger.reserve_read(length)
    n=0; digest=hashlib.sha256(); chunks=[]
    while length is None or n<length:
        available=min(cap-n,NET_LIMIT-ledger.state['body_bytes'])
        if available<=0: raise InstallError('BODY_BUDGET_NO_EOF_ROOM')
        amount=min(65536,available,available if length is None else length-n)
        ledger.reserve_read(amount)
        chunk=response.read(amount)
        if not chunk: break
        if len(chunk)>amount: raise InstallError('HTTP_READER_OVERRUN')
        ledger.received(len(chunk)); n+=len(chunk); digest.update(chunk)
        if writer is not None: writer.write(chunk)
        else: chunks.append(chunk)
    if length is not None and n!=length: raise InstallError('BODY_TRUNCATED')
    if n==0: raise InstallError('BODY_EMPTY')
    ledger.finish('COMPLETE')
    return n,digest.hexdigest(),None if writer is not None else b''.join(chunks)


class Client:
    def __init__(self,ledger): self.ledger=ledger; self.opener=direct_opener()
    def head(self,url):
        source_url(url,'HEAD'); self.ledger.state['head_attempts']+=1; self.ledger.save()
        request=urllib.request.Request(url,method='HEAD',headers={'Accept-Encoding':'identity'})
        try:
            with self.opener.open(request,timeout=30) as r: return r.status,dict(r.headers),r.geturl()
        except urllib.error.HTTPError as e:
            try: return e.code,dict(e.headers),url
            finally: e.close()  # Never read a redirect/error body on HEAD.
    def get(self,url,cap,writer=None):
        source_url(url,'GET'); self.ledger.begin('PACKAGE' if url==PACKAGE else 'TEXT',cap)
        try:
            with self.opener.open(urllib.request.Request(url,headers={'Accept-Encoding':'identity'}),timeout=30) as r:
                r.requested=url
                return stream_body(r,self.ledger,cap,writer)
        except Exception:
            self.ledger.finish('STOPPED'); raise


def checksum_text(body):
    if len(body)>4096: raise InstallError('CHECKSUM_TEXT_LIMIT')
    text=body.decode('ascii').strip()
    m=re.fullmatch(r'([a-fA-F0-9]{64})(?:\s+\*?(ffmpeg-9\.0\.2-essentials_build\.zip))?',text)
    if not m or m.group(1).lower()!=PUBLISHER_SHA: raise InstallError('PUBLISHER_SHA_CHANGED')
    return m.group(1).lower()


class PageParser(html.parser.HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.words=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a' and dict(attrs).get('href'): self.links.append(dict(attrs)['href'])
    def handle_data(self,data): self.words.append(data)


def publisher_pages(ffmpeg_body,gyan_body):
    f=PageParser(); f.feed(ffmpeg_body.decode('utf-8')); g=PageParser(); g.feed(gyan_body.decode('utf-8'))
    if not any(urllib.parse.urljoin(FFMPEG,l).rstrip('/')==GYAN.rstrip('/') for l in f.links):
        raise InstallError('FFMPEG_VENDOR_REFERENCE_UNKNOWN')
    links={urllib.parse.urljoin(GYAN,l) for l in g.links}; text=' '.join(g.words).lower()
    if not {ALIAS,ALIAS_SHA}<=links or VERSION not in text or 'essentials' not in text or not ('gplv3' in text or 'gpl v3' in text or 'gpl version 3' in text):
        raise InstallError('GYAN_VERSION_LICENSE_UNKNOWN')


def alias_head(status,headers,alias,fixed):
    location=urllib.parse.urljoin(alias,header_value(headers,'Location',''))
    if status not in (301,302,303,307,308) or location!=fixed: raise InstallError('ALIAS_VERSION_NOT_PINNED')


def safe_tool_members(infos,package_bytes):
    if len(infos)>200 or sum(i.file_size for i in infos)>DISK_LIMIT or package_bytes>NET_LIMIT:
        raise InstallError('ZIP_DECLARED_LIMIT')
    seen=set(); names={}; probe=[]; directories={}
    for i in infos:
        name=i.orig_filename
        if name!=i.filename or not name or name.startswith(('/','\\')) or '\\' in name or ':' in name: raise InstallError('ZIP_PATH')
        parts=name.rstrip('/').split('/')
        if len(parts)>6 or any(p in ('','.','..') or p.endswith((' ','.')) or
           re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?',p,re.I) or
           any(ord(ch)<32 or ch in '<>"|?*' for ch in p) for p in parts): raise InstallError('ZIP_COMPONENT')
        key='/'.join(parts).casefold()
        if key in seen: raise InstallError('ZIP_CASE_COLLISION')
        seen.add(key); directories[key]=i.is_dir(); names[name]=i
        kind=stat.S_IFMT(i.external_attr>>16)
        if i.flag_bits&1 or kind not in (0,stat.S_IFREG,stat.S_IFDIR) or i.volume:
            raise InstallError('ZIP_ENCRYPTED_SPECIAL_OR_DISK')
        if i.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED): raise InstallError('ZIP_COMPRESSION')
        if i.file_size<0 or i.file_size>DISK_LIMIT or (i.is_dir() and i.file_size): raise InstallError('ZIP_MEMBER_LIMIT')
        if parts[-1].lower().endswith(('.zip','.7z','.rar','.tar','.gz')): raise InstallError('ZIP_NESTED_ARCHIVE')
        if parts[-1].lower().endswith('.dll'): raise InstallError('PACKAGED_DLL_NOT_AUTHORIZED')
        if '/'.join(parts[-2:]).casefold()=='bin/ffprobe.exe': probe.append(i)
    for key in directories:
        p=key.split('/')
        if any(directories.get('/'.join(p[:j])) is False for j in range(1,len(p))): raise InstallError('ZIP_PARENT_COLLISION')
    if len(probe)!=1: raise InstallError('FFPROBE_NOT_UNIQUE')
    item=probe[0]; prefix='/'.join(item.filename.split('/')[:-2])
    if prefix!='ffmpeg-9.0.2-essentials_build' or item.file_size<=0: raise InstallError('PACKAGE_ROOT_VERSION')
    selected={item.filename:('bin/ffprobe.exe',item)}
    license_found=False
    for name,entry in names.items():
        p=name.split('/')
        if len(p)==2 and p[0]==prefix and p[1].casefold() in ('license','license.txt','notice','notice.txt','readme.txt','readme.md'):
            selected[name]=('licenses/'+p[1],entry)
            if p[1].casefold().startswith(('license','notice')): license_found=True
    if not license_found: raise InstallError('PACKAGE_LICENSE_MISSING')
    if package_bytes+sum(i.file_size for _,i in selected.values())+1024*1024>DISK_LIMIT:
        raise InstallError('EXTRACTION_DISK_PREFLIGHT')
    return selected


def package_verified(actual_sha):
    if actual_sha!=PUBLISHER_SHA: raise InstallError('PACKAGE_SHA_MISMATCH')


def version_result(process):
    if process.returncode!=0: raise InstallError('VERSION_NONZERO_OR_DEPENDENCY')
    text=process.stdout.decode('utf-8',errors='replace'); first=text.splitlines()[0] if text.splitlines() else ''
    if not re.match(r'^ffprobe version 9\.0\.2(?:[-\s]|$)',first): raise InstallError('VERSION_MISMATCH')
    return first[:160]


def file_digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(65536),b''): h.update(chunk)
    return h.hexdigest()


def footprint(root):
    from charades_metadata_audit import check_ancestors
    n=0
    for p in root.rglob('*'):
        check_ancestors(p)
        if p.is_file(): n+=p.stat().st_size
    return n


def exclusive_extract(z,info,target,root,ledger):
    from charades_metadata_audit import check_ancestors
    part=target.with_suffix(target.suffix+'.part'); check_ancestors(target); check_ancestors(part)
    if target.exists() or part.exists(): raise InstallError('TARGET_EXISTS_NO_OVERWRITE')
    if footprint(root)+2*info.file_size+1024*1024>DISK_LIMIT: raise InstallError('EXTRACT_TEMP_DISK_BUDGET')
    n=0
    with z.open(info) as f,part.open('xb') as out:
        for chunk in iter(lambda:f.read(65536),b''):
            n+=len(chunk)
            if n>info.file_size: raise InstallError('EXTRACT_SIZE')
            out.write(chunk)
    if n!=info.file_size: raise InstallError('EXTRACT_TRUNCATED')
    ledger.disk(footprint(root)); os.link(part,target); ledger.disk(footprint(root)); part.unlink()


def preflight():
    from charades_metadata_audit import check_ancestors
    import winreg
    if os.name!='nt' or platform.machine().lower() not in ('amd64','x86_64') or sys.getwindowsversion().major<10:
        raise InstallError('WINDOWS_X64_REQUIREMENT')
    base=pathlib.Path(os.environ['LOCALAPPDATA']).absolute(); root=base/'VLM-Research-Isolated/CPU-Tools/ffprobe'
    check_ancestors(root)
    original=os.environ.get('VLM_ORIGINAL_WORKSPACE')
    if not original: raise InstallError('ORIGINAL_WORKSPACE_EXCLUSION_UNKNOWN')
    forbidden=[pathlib.Path(original).absolute(),pathlib.Path(__file__).resolve().parent.parent,
               base/'VLM-Research-Isolated/Charades-v1-Metadata',base/'VLM-Research-Isolated/Charades-v1-MediaPilot']
    for k in ('OneDrive','OneDriveConsumer','OneDriveCommercial','Dropbox','BOX_SYNC'):
        if os.environ.get(k): forbidden.append(pathlib.Path(os.environ[k]).absolute())
    def subkeys(key):
        items=[]; j=0
        while True:
            try: items.append(winreg.EnumKey(key,j)); j+=1
            except OSError as e:
                if e.winerror==259: return items
                raise
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\OneDrive\Accounts') as key:
            for name in subkeys(key):
                with winreg.OpenKey(key,name) as item:
                    try: forbidden.append(pathlib.Path(winreg.QueryValueEx(item,'UserFolder')[0]).absolute())
                    except FileNotFoundError: pass
    except FileNotFoundError: pass
    for hive in (winreg.HKEY_CURRENT_USER,winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.OpenKey(hive,r'Software\Microsoft\Windows\CurrentVersion\Explorer\SyncRootManager') as key:
                for name in subkeys(key):
                    try:
                        with winreg.OpenKey(key,name+r'\UserSyncRoots') as item:
                            j=0
                            while True:
                                try:
                                    _,v,t=winreg.EnumValue(item,j); j+=1
                                    if t in (winreg.REG_SZ,winreg.REG_EXPAND_SZ): forbidden.append(pathlib.Path(os.path.expandvars(v)).absolute())
                                except OSError as e:
                                    if e.winerror==259: break
                                    raise
                    except FileNotFoundError: pass
        except FileNotFoundError: pass
    for target in (root,root.resolve()):
        for p in forbidden:
            for other in (p.absolute(),p.resolve()):
                if target==other or other in target.parents or target in other.parents: raise InstallError('STORAGE_FORBIDDEN_OVERLAP')
    if root.exists(): raise InstallError('TOOL_ROOT_ALREADY_EXISTS')
    if base.resolve() not in root.resolve().parents or shutil.disk_usage(base).free<1024*MIB:
        raise InstallError('STORAGE_SPACE_OR_CONTAINMENT')
    existing=shutil.which('ffprobe')
    if existing and 'conda' not in existing.lower(): raise InstallError('STANDALONE_ASSET_ALREADY_EXISTS')
    return root


def parent_gate():
    docs=pathlib.Path(__file__).resolve().parent.parent
    results=(docs/'docs/codex-results.md').read_text(encoding='utf-8')
    board=(docs/'docs/next-steps.md').read_text(encoding='utf-8'); active=[]
    for line in board.splitlines():
        c=[p.strip() for p in line.split('|')]
        if len(c)>4 and re.fullmatch(r'VLM-BATCH-\d{3}',c[1]) and c[3].startswith('**READY'): active.append(c[1])
    if active!=['VLM-BATCH-014'] or re.search(r'^### VLM-BATCH-014\s',results,re.M): raise InstallError('PARENT_NOT_READY_OR_REPORTED')


def create_new_root(root):
    from charades_metadata_audit import check_ancestors
    check_ancestors(root)
    if root.exists(): raise InstallError('TOOL_ROOT_ALREADY_EXISTS')
    root.parent.mkdir(parents=True,exist_ok=True)
    check_ancestors(root.parent)
    root.mkdir(exist_ok=False)


def deploy():
    parent_gate(); root=preflight()
    create_new_root(root)
    for d in ('incoming','bin','licenses','local-audit'): (root/d).mkdir(exist_ok=False)
    probe=root/'local-audit/write-check'
    with probe.open('xb'): pass
    probe.unlink()
    ledger=Ledger(root/'local-audit/tool-ledger.json'); client=Client(ledger)
    try:
        _,_,f=client.get(FFMPEG,TEXT_CAP); _,_,g=client.get(GYAN,TEXT_CAP); publisher_pages(f,g)
        for a,fixed in ((ALIAS,PACKAGE),(ALIAS_SHA,CHECKSUM)):
            status,headers,final=client.head(a); alias_head(status,headers,a,fixed)
        _,_,body=client.get(CHECKSUM,4096); checksum_text(body)
        status,headers,final=client.head(PACKAGE)
        head_size=response_policy(status,headers,final,PACKAGE,NET_LIMIT)
        if 'zip' not in header_value(headers,'Content-Type','').lower(): raise InstallError('PACKAGE_CONTENT_TYPE')
        if head_size is not None and head_size+ledger.state['body_bytes']>NET_LIMIT: raise InstallError('PACKAGE_GLOBAL_PREFLIGHT')
        part=root/'incoming/ffmpeg-9.0.2.zip.part'; package=root/'incoming/ffmpeg-9.0.2.zip'
        with part.open('xb') as writer: size,sha,_=client.get(PACKAGE,NET_LIMIT,writer)
        ledger.disk(footprint(root)); package_verified(sha)
        if head_size is not None and size!=head_size: raise InstallError('PACKAGE_HEAD_GET_SIZE')
        with part.open('rb') as f:
            if f.read(4)!=b'PK\x03\x04': raise InstallError('PACKAGE_SIGNATURE')
        os.link(part,package); ledger.disk(footprint(root)); part.unlink()
        ledger.state['successful_zip_gets']=1; ledger.state['package_bytes']=size; ledger.state['package_sha256']=sha; ledger.save()
        with zipfile.ZipFile(package) as z:
            selected=safe_tool_members(z.infolist(),size)
            if z.testzip() is not None: raise InstallError('PACKAGE_CRC')
            ledger.state['member_count']=len(z.infolist()); ledger.state['selected_count']=len(selected); ledger.save()
            for _,(relative,info) in selected.items(): exclusive_extract(z,info,root/relative,root,ledger)
        exe=root/'bin/ffprobe.exe'; binary_sha=file_digest(exe)
        ledger.state['version_runs']=1; ledger.state['executable_sha256']=binary_sha; ledger.save()
        process=subprocess.run([str(exe),'-version'],capture_output=True,timeout=10)
        version=version_result(process)
        ledger.state['status']='AVAILABLE_VERIFIED_WITHIN_PUBLISHER_HASH_SCOPE'; ledger.state['version']=version
        ledger.state['authenticode']='UNKNOWN_NOT_CHECKED'; ledger.disk(footprint(root)); ledger.save()
    except Exception as e:
        ledger.state['status']='BLOCKED'; ledger.state['reason']=str(e) if isinstance(e,InstallError) else type(e).__name__; ledger.save()
    return {k:ledger.state.get(k) for k in ('status','reason','body_bytes','get_attempts','head_attempts','successful_zip_gets',
            'package_bytes','package_sha256','peak_local_bytes','version_runs','version','executable_sha256','authenticode','member_count','selected_count')}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--install',action='store_true'); args=parser.parse_args()
    try:
        result=deploy() if args.install else {'status':'PREFLIGHT_ONLY','storage':'PASS' if preflight() else 'UNKNOWN','network_requests':0}
        print(json.dumps(result,ensure_ascii=True,indent=2))
        if result['status']=='BLOCKED': raise SystemExit(1)
    except InstallError as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)})); raise SystemExit(1) from None
    except Exception:
        print(json.dumps({'status':'BLOCKED','reason':'ENVIRONMENT_OR_SOURCE_UNVERIFIED'})); raise SystemExit(1) from None
