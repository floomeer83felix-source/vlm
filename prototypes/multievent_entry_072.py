"""072 bounded fixed-public-metadata acquisition and multievent manifest roles.

Import has no network, dataset, model or other research operations.
"""
import argparse,collections,hashlib,http.client,itertools,json,os,re,ssl,time,urllib.parse
from pathlib import Path
REV='da3065053d958c38151304e33a42e138b1899eaf'
REPO='anonymous-video-benchmark/toc_bench'
URLS=(('api',f'https://huggingface.co/api/datasets/{REPO}/revision/{REV}?blobs=true',2*1024**2),('readme',f'https://huggingface.co/datasets/{REPO}/resolve/{REV}/README.md',32*1024),('answers',f'https://huggingface.co/datasets/{REPO}/resolve/{REV}/answer_final.json',2*1024**2))
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def state(p,x):
 temp=Path(str(p)+'.writing')
 with open(temp,'w',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(temp,p)
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(json.dumps(dict(at_unix=time.time(),**x),ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def require(root,ok,code,actual,limit,stage):
 if not ok:event(root/'failures.jsonl',reason_code=code,actual=actual,limit=limit,stage=stage);raise RuntimeError(code)
def check_seal(root,name='download-code-seal.json'):
 for x in read(root/name)['files']:require(root,sha(Path(x['path']).read_bytes())==x['sha256'],'CODE_IDENTITY',Path(x['path']).name,'sealed digest','CODE')
def blobid(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def content_identity(entry,b):
 lfs=entry.get('lfs')
 if lfs:
  digest=lfs.get('sha256',lfs.get('oid',''));digest=digest.removeprefix('sha256:');return dict(kind='LFS_SHA256',expected=digest,actual=sha(b),size=entry.get('size',lfs.get('size')),matched=len(digest)==64 and digest==sha(b) and len(b)==entry.get('size',lfs.get('size')))
 digest=entry.get('blobId',entry.get('oid',''));return dict(kind='GIT_BLOB_SHA1',expected=digest,actual=blobid(b),size=entry.get('size'),matched=len(digest)==40 and digest==blobid(b) and len(b)==entry.get('size'))
def acquire(root):
 check_seal(root);start=read(root/'network-clock.json')['start_monotonic'];deadline=start+170;ledger=[];used=0;registered={};context=ssl.create_default_context();headers={'User-Agent':'VLM072-MetadataOnly','Accept-Encoding':'identity','Accept':'application/json,text/plain,text/markdown'}
 def persist():state(root/'network-progress.json',dict(requests=ledger,body_bytes=used,outer_s=time.monotonic()-start,limit_body_bytes=4*1024**2,limit_outer_s=180))
 for key,initial,cap in URLS:
  rec=dict(key=key,url=initial,status='STARTED',body_bytes=0,chain=[]);ledger.append(rec);persist();url=initial;final=b''
  try:
   if key!='api':
    target='README.md' if key=='readme' else 'answer_final.json';entry=registered[target];require(root,type(entry.get('size')) is int and 0<=entry['size']<=cap and used+entry['size']<=4*1024**2,'PUBLISHED_SIZE_CAP',{'file':target,'size':entry.get('size'),'used':used},{'item':cap,'total':4*1024**2},'PRE_GET')
   for hop in range(4):
    require(root,time.monotonic()<deadline,'NETWORK_DEADLINE',time.monotonic()-start,170,'CONNECT');u=urllib.parse.urlparse(url);host=u.hostname
    allowed=host=='huggingface.co' or (key!='api' and registered['README.md' if key=='readme' else 'answer_final.json'].get('lfs') and host in ('cdn-lfs.huggingface.co','cdn-lfs-us-1.hf.co','cas-bridge.xethub.hf.co'))
    require(root,u.scheme=='https' and allowed and u.username is None and u.password is None and u.port in (None,443),'REDIRECT_HOST',{'scheme':u.scheme,'host':host},'normal permitted HTTPS service','REDIRECT');response_rec=dict(url=url,hop=hop,state='STARTED',body_bytes=0);rec['chain'].append(response_rec);persist();conn=http.client.HTTPSConnection(host,timeout=min(15,max(.1,deadline-time.monotonic())),context=context)
    try:
     conn.connect();conn.sock.settimeout(min(30,max(.1,deadline-time.monotonic())));path=urllib.parse.urlunparse(('', '',u.path or '/',u.params,u.query,''));conn.request('GET',path,headers=headers);response=conn.getresponse();response_rec.update(http_status=response.status,content_type=response.getheader('Content-Type'),content_length=response.getheader('Content-Length'),content_encoding=response.getheader('Content-Encoding','identity'),location=response.getheader('Location'));persist();response_path=root/f'{key}-hop{hop}.body'
     require(root,response.getheader('Content-Encoding','identity')=='identity','UNEXPECTED_ENCODING',response.getheader('Content-Encoding'),'identity','READ')
     with open(response_path,'xb') as stream:
      while True:
       require(root,time.monotonic()<deadline,'NETWORK_DEADLINE',time.monotonic()-start,170,'READ');remaining=min(cap-rec['body_bytes'],4*1024**2-used)
       if remaining==0:
        require(root,response.length==0,'BODY_CAP_EXHAUSTED_AT_BOUNDARY',{'item':rec['body_bytes'],'total':used},{'item':cap,'total':4*1024**2},'READ');break
       require(root,remaining>0,'BODY_BUDGET',{'item':rec['body_bytes'],'total':used},{'item':cap,'total':4*1024**2},'READ');conn.sock.settimeout(min(30,max(.1,deadline-time.monotonic()))) if conn.sock else None;b=response.read(min(65536,remaining))
       if not b:break
       stream.write(b);stream.flush();os.fsync(stream.fileno());used+=len(b);rec['body_bytes']+=len(b);response_rec['body_bytes']+=len(b);persist()
     body=response_path.read_bytes();response_rec.update(state='CLOSED',sha256=sha(body));persist()
     if response.status in (301,302,303,307,308):require(root,hop<3 and bool(response.getheader('Location')),'REDIRECT_LIMIT',hop,3,'REDIRECT');url=urllib.parse.urljoin(url,response.getheader('Location'));continue
     require(root,response.status==200,'HTTP_FAILURE',response.status,200,'HTTP');require(root,not body.lstrip().lower().startswith((b'<!doctype html',b'<html')),'HTML_RESPONSE',response.getheader('Content-Type'),'metadata body','BODY');final=body;break
    finally:conn.close()
   require(root,bool(final),'EMPTY_FINAL_BODY',len(final),'>0','BODY')
   with open(root/(key+'.body'),'xb') as f:f.write(final);f.flush();os.fsync(f.fileno())
   if key=='api':
    api=json.loads(final);require(root,api.get('sha')==REV and not api.get('private') and api.get('gated') in (False,None),'REVISION_OR_GATE',{'sha':api.get('sha'),'private':api.get('private'),'gated':api.get('gated')},REV,'API_IDENTITY');siblings=api.get('siblings',[])
    for name in ('README.md','answer_final.json'):
     matches=[x for x in siblings if x.get('rfilename')==name];require(root,len(matches)==1,'FILE_REGISTRATION',{'file':name,'matches':len(matches)},1,'API_IDENTITY');registered[name]=matches[0]
    save(root/'registered-files.json',registered)
   else:
    identity=content_identity(registered['README.md' if key=='readme' else 'answer_final.json'],final);save(root/(key+'-identity.json'),identity);require(root,identity['matched'],'PUBLISHER_CONTENT_IDENTITY',identity,'registered fixed-revision Git blob or LFS content identity','IDENTITY')
    if key=='answers':require(root,final.lstrip()[:1] in (b'{',b'['),'JSON_ROOT',final[:16].hex(),'JSONobject/array','BODY');json.loads(final)
   rec.update(status='CLOSED',final_url=url,final_body_bytes=len(final),final_sha256=sha(final));persist()
  except Exception as e:
   rec.update(status='FAILED',reason_code=str(e) or type(e).__name__,error_type=type(e).__name__);persist();raise
 save(root/'acquisition-closed.json',dict(requests=ledger,body_bytes=used,outer_s=time.monotonic()-start,revision=REV,logical_requests=len(ledger),HTTP_responses=sum(len(x['chain']) for x in ledger),files=[dict(name=k+'.body',bytes=(root/(k+'.body')).stat().st_size,sha256=sha((root/(k+'.body')).read_bytes())) for k,_,_ in URLS]));print('THREE_METADATA_GETS_CLOSED',used,flush=True)
def collections_at(root):
 result=[]
 def visit(x,path):
  if isinstance(x,list):
   if x and any(isinstance(v,dict) and {'qa_id','video_id','format'}<=set(v) for v in x):result.append((path,x));return
   for i,v in enumerate(x):visit(v,path+[i])
  elif isinstance(x,dict):
   for k,v in x.items():visit(v,path+[k])
 visit(root,[]);return result
def observe(root):
 check_seal(root);require(root,not (root/'schema-observation.json').exists(),'SCHEMA_OBSERVATION_ALREADY_USED',True,False,'SCHEMA');bundle=read(root/'answers.body');found=collections_at(bundle);info=dict(root_type=type(bundle).__name__,root_keys=list(bundle) if isinstance(bundle,dict) else None,candidate_collections=[dict(path=p,count=len(rows),keys=sorted({k for x in rows if isinstance(x,dict) for k in x})) for p,rows in found],samples=[])
 if len(found)==1:
  for fmt in ('ordering_3','ordering_4'):
   x=next((x for x in found[0][1] if isinstance(x,dict) and x.get('format')==fmt),None)
   if x is not None:info['samples'].append(dict(format=fmt,schema={k:type(v).__name__ for k,v in x.items()},sample=x))
 save(root/'schema-observation.json',info);print(json.dumps(info,ensure_ascii=True),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('role',choices=('acquire','observe'));p.add_argument('--root',required=True);args=p.parse_args();root=Path(args.root)
 try:globals()[args.role](root)
 except Exception as e:event(root/'stops.jsonl',stage=args.role,reason_code=str(e) or type(e).__name__,actual='see persistent phase/network ledger',limit='sealed072limits');raise
