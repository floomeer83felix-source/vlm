"""078 metadata component; standard library only, no import-time I/O.

Derived from the unexecuted 077 producer/oracle; original source id is mapped
explicitly into internal annotation_id. Owner-tested on the fixed metadata
packet; this is not a Windows Job, RGB/model/training execution or 077 repair.

Perception Test annotations: CC-BY-4.0, DeepMind/Google DeepMind.
Modified representation: normalized unique-label action triples and symbolic orders.
No media, model, network, numerical library or training operations.
"""
import argparse,collections,hashlib,io,itertools,json,math,os,re,struct,time,zipfile
from fractions import Fraction
from pathlib import Path,PurePosixPath
DOMAIN=b'VLM077/pt-triple-v1/'
QUESTION='Does the event "{}" happen before the event "{}"? Answer Yes or No.'
REGEX=r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.'
BAD=r'\b(before|after|first|second|third|fourth|then|earlier|later|finally)\b'
NAMES={'DATA-LICENSE-NOTICE.txt','action_localisation_train_annotations.zip','archive-directory.json','archive-tail.bin','central-directory.bin','owner-preview-summary.json','owner-rule.json','owner-selection-frozen.json','package-manifest.json','source-README.md','source-receipt.json','source-registration.json'}
MIB=1024**2

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def write(p,x):
 with open(p,'xb') as f:f.write(canon(x)+b'\n');f.flush();os.fsync(f.fileno())
def check(ok,reason):
 if not ok:raise ValueError(reason)
def safe(n):return bool(n) and '\\' not in n and ':' not in n and not PurePosixPath(n).is_absolute() and all(x not in ('','..','.') for x in n.split('/'))
def unpack(b,maxsize,expected=None):
 z=zipfile.ZipFile(io.BytesIO(b));items=z.infolist();check(len({x.filename for x in items})==len(items),'DUPLICATE_ZIP');check(sum(x.file_size for x in items)<=maxsize,'ZIP_EXPANSION')
 if expected is not None:check({x.filename for x in items}==expected,'ZIP_ALLOWLIST')
 out={}
 for x in items:
  check(safe(x.filename) and not x.is_dir() and not x.flag_bits&1 and ((x.external_attr>>16)&0o170000)!=0o120000,'UNSAFE_ZIP');out[x.filename]=z.read(x)
 return out
class Reads:
 def __init__(self,root):self.root=Path(root);self.cache={};self.count=0;self.log=[]
 def charge(self,b,kind):
  self.count+=len(b);check(self.count<=32*MIB,'READ_LIMIT');self.log.append(dict(kind=kind,bytes=len(b)));return b
 def file(self,p):
  p=str(p)
  if p not in self.cache:self.cache[p]=self.charge(Path(p).read_bytes(),'file')
  return self.cache[p]
 def expand(self,b,limit,names=None):
  out=unpack(b,limit,names)
  for n,v in out.items():self.charge(v,'inflate:'+n)
  return out

def action_lists(row):
 check(isinstance(row.get('action_localisation'),list),'ACTION_CONTAINER_SCHEMA')
 actions=row['action_localisation']
 check(all(isinstance(a,dict) and 'id' in a and 'annotation_id' not in a for a in actions),'SOURCE_ID_SCHEMA')
 return actions

def metadata(row,key):
 m=row['metadata'];return m['frame_rate'],m['num_frames'],m['video_id'],m['split']

def directory(b):
 out=[];pos=0
 while pos<len(b):
  check(b[pos:pos+4]==b'PK\x01\x02','CENTRAL_SIGNATURE');v=struct.unpack_from('<4s6H3I5H2I',b,pos);nl,el,cl=v[10:13];name=b[pos+46:pos+46+nl].decode('utf-8' if v[3]&2048 else 'cp437');extra=b[pos+46+nl:pos+46+nl+el];u,c,o=v[9],v[8],v[16];disk=v[13];at=0;z64=None
  while at<len(extra):
   tag,n=struct.unpack_from('<HH',extra,at);at+=4;check(at+n<=len(extra),'EXTRA_BOUNDS')
   if tag==1:check(z64 is None,'DUPLICATE_ZIP64');z64=extra[at:at+n]
   at+=n
  cur=0;vals=[]
  for x in (u,c,o):
   if x==0xffffffff:check(z64 is not None and cur+8<=len(z64),'ZIP64_MISSING');x=struct.unpack_from('<Q',z64,cur)[0];cur+=8
   vals.append(x)
  u,c,o=vals
  if disk==65535:check(z64 is not None and cur+4<=len(z64),'ZIP64_DISK');disk=struct.unpack_from('<I',z64,cur)[0]
  check(disk==0 and safe(name.rstrip('/')) and not v[3]&1 and ((v[15]>>16)&0o170000)!=0o120000,'UNSAFE_MEDIA_DIRECTORY')
  out.append(dict(name=name,compressed=c,uncompressed=u,offset=o,crc=v[7],method=v[4],flags=v[3]));pos+=46+nl+el+cl
 check(pos==len(b) and len({x['name'] for x in out})==len(out),'DIRECTORY_SIZE_OR_DUPLICATE');return out

def produce(raw,cd):
 entries=directory(cd);by=collections.defaultdict(list)
 for e in entries:
  if not e['name'].endswith('/'):by[PurePosixPath(e['name']).stem].append(e)
 counts=collections.Counter(videos=len(raw));rejections=collections.Counter();best=[];allrows=[]
 for key,row in raw.items():
  actions=action_lists(row);counts['actions']+=len(actions);fps,n,vid,split=metadata(row,key)
  goodmeta=isinstance(fps,(int,float)) and not isinstance(fps,bool) and math.isfinite(fps) and fps>0 and isinstance(n,int) and n>0 and vid==key and split=='train'
  ids=[a['id'] for a in actions];goodmeta=goodmeta and len(set(ids))==len(ids)
  if not goodmeta:rejections['video_identity_fps_split_or_duplicate_id']+=1;allrows.append(dict(video_id=key,status='INVALID_METADATA',actions=len(actions)));continue
  texts=[' '.join(a['label'].split()) for a in actions];freq=collections.Counter(texts);segments=[];reject=collections.Counter()
  for a,text in zip(actions,texts):
   reason=None;t=a.get('timestamps');f=a.get('frame_ids')
   if not text or freq[text]!=1:reason='empty_or_repeated_label'
   elif re.search(BAD,text,re.I):reason='temporal_word'
   elif not isinstance(a['id'],(int,float)) or isinstance(a['id'],bool) or not math.isfinite(a['id']):reason='annotation_id'
   elif not isinstance(t,list) or not isinstance(f,list) or len(t)!=2 or len(f)!=2 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in t+f):reason='boundary_schema'
   elif not (0<=t[0]<t[1] and 500000<=t[1]-t[0]<=8000000 and t[1]/1e6<=(n+1)/fps and 0<=f[0]<f[1]<n):reason='boundary_duration'
   elif any(abs(ti/1e6-fi/fps)>1/fps+1e-6 for ti,fi in zip(t,f)):reason='clock_error'
   if reason:reject[reason]+=1;continue
   points=[(t[0]+(j+.5)*(t[1]-t[0])/12)/1e6 for j in range(12)];indices=[math.floor(x*fps+.5) for x in points]
   if len(set(indices))!=12 or any(not f[0]<=x<=f[1] for x in indices):reject['planned_frame_indices']+=1;continue
   segments.append(dict(annotation_id=a['id'],label_id=a['label_id'],text=text,timestamps_us=t,frame_ids=f))
  counts['eligible_segments']+=len(segments);rejections.update(reject);candidates=[];segments.sort(key=lambda e:(e['timestamps_us'][0],e['annotation_id']))
  for tri in itertools.combinations(segments,3):
   if any(tri[i+1]['timestamps_us'][0]-tri[i]['timestamps_us'][1]<100000 for i in (0,1)):continue
   slots=sorted(tri,key=lambda e:e['annotation_id']);qs=[QUESTION.format(slots[i]['text'],slots[j]['text']) for i,j in itertools.permutations(range(3),2)]
   if any(not (m:=re.fullmatch(REGEX,q)) or m.groups()!=(slots[i]['text'],slots[j]['text']) for q,(i,j) in zip(qs,itertools.permutations(range(3),2))):rejections['ambiguous_question_triple']+=1;continue
   obs=dict(source='PerceptionTest/action_localisation/train',video_id=key,events=slots);b=canon(obs);candidates.append((hashlib.sha256(DOMAIN+b).hexdigest(),b,obs))
  counts['candidate_triples']+=len(candidates)
  loc=by[key];eligible=bool(candidates) and len(loc)==1
  if candidates and len(loc)!=1:rejections['nonunique_or_missing_media']+=1
  allrows.append(dict(video_id=key,status='ELIGIBLE' if eligible else 'NO_ELIGIBLE_TRIPLE',actions=len(actions),eligible_segments=len(segments),candidates=len(candidates),segment_rejections=reject,media_matches=len(loc)))
  if eligible:
   candidate=min(candidates,key=lambda x:(x[0],x[1]));best.append((*candidate,loc[0]));counts['eligible_videos']+=1
 best.sort(key=lambda x:(x[0],x[1]));check(len(best)>=32,'INSUFFICIENT_GROUPS')
 selected=[]
 for rank,(digest,b,obs,media) in enumerate(best[:32]):
  row=raw[obs['video_id']];fps=row['metadata']['frame_rate'];sample=[]
  for e in obs['events']:
   s,t=e['timestamps_us'];pts=[(s+(j+.5)*(t-s)/12)/1e6 for j in range(12)];sample.append(dict(seconds=pts,indices=[math.floor(x*fps+.5) for x in pts]))
  selected.append(dict(rank=rank,split='train' if rank<20 else 'development' if rank<24 else 'test',digest=digest,observation=obs,media=media,sampling=sample,questions=[QUESTION.format(obs['events'][i]['text'],obs['events'][j]['text']) for i,j in itertools.permutations(range(3),2)],rgb_block_plans=[list(x) for x in itertools.permutations(range(3))],runtime=dict(fps=12,frames=36,duration_seconds=3)))
 return selected,dict(counts),dict(rejections),allrows,entries

def supervise(selected):
 answers=[];relations=[];perms=list(itertools.permutations(range(3)));qp=list(itertools.permutations(range(3),2))
 for g in selected:
  for pi,p in enumerate(perms):
   for qi,(a,b) in enumerate(qp):answers.append(dict(group=g['rank'],split=g['split'],permutation=pi,question=qi,yes=int(p.index(a)<p.index(b))))
   for swap in (0,1):
    target=list(p);target[swap],target[swap+1]=target[swap+1],target[swap];pj=perms.index(tuple(target))
    for qi,(a,b) in enumerate(qp):
     left=int(p.index(a)<p.index(b));right=int(target.index(a)<target.index(b));relations.append(dict(group=g['rank'],split=g['split'],left=pi,right=pj,question=qi,difference=right-left,relation='FLIP' if right!=left else 'HOLD'))
 return answers,relations

def independent(raw,cd,selected,answers,relations):
 """Separate rational selection, byte-level directory and relation oracle.

 Does not call producer metadata, selection, ranking, directory or label helpers.
 """
 checks=0
 def demand(ok):
  nonlocal checks;checks+=1
  if not ok:raise ValueError('INDEPENDENT_CHECK_'+str(checks))
 def enc(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
 # Parse each central field separately rather than reuse producer unpack/layout.
 directory2=[];at=0
 def u(start,n):return int.from_bytes(cd[start:start+n],'little')
 while at<len(cd):
  demand(cd[at:at+4]==b'PK\x01\x02');nl,el,cl=[u(at+x,2) for x in (28,30,32)];flags=u(at+8,2);name=cd[at+46:at+46+nl].decode('utf-8' if flags&2048 else 'cp437');ext=cd[at+46+nl:at+46+nl+el];fields={};cursor=0
  while cursor<len(ext):
   tag=int.from_bytes(ext[cursor:cursor+2],'little');length=int.from_bytes(ext[cursor+2:cursor+4],'little');demand(cursor+4+length<=len(ext));fields[tag]=ext[cursor+4:cursor+4+length];cursor+=4+length
  vals=[u(at+24,4),u(at+20,4),u(at+42,4)];cursor=0
  for i,x in enumerate(vals):
   if x==2**32-1:demand(1 in fields and cursor+8<=len(fields[1]));vals[i]=int.from_bytes(fields[1][cursor:cursor+8],'little');cursor+=8
  demand(not name.startswith('/') and '..' not in name.split('/') and '\\' not in name and ':' not in name and not flags&1)
  directory2.append(dict(name=name,compressed=vals[1],uncompressed=vals[0],offset=vals[2],crc=u(at+16,4),method=u(at+10,2),flags=flags));at+=46+nl+el+cl
 demand(at==len(cd) and len(directory2)==2184);candidates=[];candidate_count=0;eligible=0;action_count=0;validsegments=0
 for vid,row in raw.items():
  m=row['metadata'];rate=Fraction(str(m['frame_rate']));nf=m['num_frames'];demand(m['video_id']==vid and m['split']=='train' and rate>0 and nf>0)
  actions=row['action_localisation'];demand(isinstance(actions,list));action_count+=len(actions);demand(all('id' in e and 'annotation_id' not in e for e in actions));demand(len({e['id'] for e in actions})==len(actions));norm=collections.Counter(' '.join(e['label'].split()) for e in actions);segments=[]
  for e in actions:
   text=' '.join(e['label'].split())
   if not text or norm[text]!=1 or re.search(r'\b(?:before|after|first|second|third|fourth|then|earlier|later|finally)\b',text,re.I):continue
   ts=e['timestamps'];fr=e['frame_ids']
   if len(ts)!=2 or len(fr)!=2 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in ts+fr):continue
   t0,t1=[Fraction(str(v)) for v in ts];f0,f1=[Fraction(str(v)) for v in fr]
   if not (0<=t0<t1 and 500000<=t1-t0<=8000000 and t1*rate<=1000000*(nf+1) and 0<=f0<f1<nf):continue
   if any(abs(t*rate-f*1000000)>1000000+rate for t,f in zip((t0,t1),(f0,f1))):continue
   times=[(t0+Fraction(2*j+1,24)*(t1-t0))/1000000 for j in range(12)];idx=[(x*rate+Fraction(1,2)).numerator//(x*rate+Fraction(1,2)).denominator for x in times]
   if len(set(idx))!=12 or not all(f0<=x<=f1 for x in idx):continue
   segments.append(dict(annotation_id=e['id'],label_id=e['label_id'],text=text,timestamps_us=ts,frame_ids=fr))
  validsegments+=len(segments);local=[]
  for slots in itertools.combinations(sorted(segments,key=lambda e:e['annotation_id']),3):
   chron=sorted(slots,key=lambda e:e['timestamps_us'][0])
   if any(Fraction(str(chron[i+1]['timestamps_us'][0]))-Fraction(str(chron[i]['timestamps_us'][1]))<100000 for i in (0,1)):continue
   bad=False
   for a in range(3):
    for b in range(3):
     if a==b:continue
     q='Does the event "'+slots[a]['text']+'" happen before the event "'+slots[b]['text']+'"? Answer Yes or No.';mt=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
     if not mt or mt.groups()!=(slots[a]['text'],slots[b]['text']):bad=True
   if bad:continue
   ob={'source':'PerceptionTest/action_localisation/train','video_id':vid,'events':list(slots)};payload=enc(ob);local.append((hashlib.sha256(b'VLM077/pt-triple-v1/'+payload).hexdigest(),payload,ob))
  candidate_count+=len(local);matches=[e for e in directory2 if not e['name'].endswith('/') and PurePosixPath(e['name']).stem==vid]
  if local and len(matches)==1:eligible+=1;best=sorted(local,key=lambda v:(v[0],v[1]))[0];candidates.append((*best,matches[0]))
 candidates.sort(key=lambda v:(v[0],v[1]));demand(len(selected)==32 and len({g['observation']['video_id'] for g in selected})==32)
 for i,g in enumerate(selected):
  v=candidates[i];demand(g['digest']==v[0] and enc(g['observation'])==v[1] and g['media']==v[3]);demand(g['rank']==i and g['split']==('train' if i<20 else 'development' if i<24 else 'test'))
  for e,sample in zip(g['observation']['events'],g['sampling']):
   rate=Fraction(str(raw[g['observation']['video_id']]['metadata']['frame_rate']));start,end=map(lambda x:Fraction(str(x)),e['timestamps_us']);points=[(start+(end-start)*Fraction(2*j+1,24))/1000000 for j in range(12)];demand(all(abs(float(x)-y)<1e-12 for x,y in zip(points,sample['seconds'])));demand(sample['indices']==[math.floor(x*rate+Fraction(1,2)) for x in points])
 perms=list(itertools.permutations([0,1,2]));questions=[(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)];truth={};rel={}
 for g in range(32):
  for pi,p in enumerate(perms):
   position={slot:loc for loc,slot in enumerate(p)}
   for qi,(a,b) in enumerate(questions):truth[(g,pi,qi)]=int(position[a]<position[b])
   for pi2,p2 in enumerate(perms):
    changed=[j for j in range(3) if p[j]!=p2[j]]
    if len(changed)!=2 or changed[1]-changed[0]!=1:continue
    for qi,(a,b) in enumerate(questions):
     delta=int(p2.index(a)<p2.index(b))-int(position[a]<position[b]);rel[(g,pi,pi2,qi)]=(delta,'HOLD' if delta==0 else 'FLIP')
 demand(len(answers)==len(truth)==1152 and len(relations)==len(rel)==2304)
 seen=set()
 for a in answers:
  k=(a['group'],a['permutation'],a['question']);demand(k not in seen and a['yes']==truth[k] and a['split']==selected[k[0]]['split']);seen.add(k)
 seen=set()
 for a in relations:
  k=(a['group'],a['left'],a['right'],a['question']);demand(k not in seen and (a['difference'],a['relation'])==rel[k] and a['split']==selected[k[0]]['split']);seen.add(k)
 for g in range(32):
  for q in range(6):demand(sum(truth[g,p,q] for p in range(6))==3)
  # Every fixed text-only six-answer vector necessarily misses at least one variant.
  for bits in itertools.product((0,1),repeat=6):demand(sum(all(bits[q]==truth[g,p,q] for p in range(6) for q in range(6)) for _ in [0])==0)
 demand(sum(v[1]=='FLIP' for v in rel.values())==768);demand(sum(v[1]=='HOLD' for v in rel.values())==1536)
 return dict(status='PASS',checks=checks,counts=dict(videos=len(raw),actions=action_count,candidate_triples=candidate_count,eligible_videos=eligible,eligible_segments=validsegments),directory=directory2)

def owner_compare(preview,selection,selected,counts):
 # Exact ordered reference binding, opened after both independent reconstructions.
 check(isinstance(selection,list) and len(selection)==len(selected)==32,'OWNER_SELECTION_SIZE')
 check(all(g['rank']==i and g['digest']==ref['digest'] and canon(g['observation'])==canon(ref['observation']) for i,(g,ref) in enumerate(zip(selected,selection))),'OWNER_ORDERED_SELECTION_MISMATCH')
 check(preview['source_videos']==counts['videos'] and preview['source_actions']==counts['actions'] and preview['qualifying_candidate_triples']==counts['candidate_triples'] and preview['eligible_videos_with_exact_archive_member']==counts['eligible_videos'],'OWNER_SOURCE_COUNTS_MISMATCH')
 check(preview['selected_source_videos']==32 and preview['selected_distinct_action_texts']==len({e['text'] for g in selected for e in g['observation']['events']}),'OWNER_SELECTED_COUNTS_MISMATCH')
 check(preview['media_compressed_bytes']==sum(g['media']['compressed'] for g in selected) and preview['media_uncompressed_bytes']==sum(g['media']['uncompressed'] for g in selected) and preview['media_uncompressed_max_bytes']==max(g['media']['uncompressed'] for g in selected),'OWNER_MEDIA_SIZE_MISMATCH')
 return dict(status='PASS',all_32_observations=True,all_32_ordered_digests=True,independently_computed_before_reference=True)

def fixture():
 # Symbolic semantics only, with no input/source data and no training updates.
 x=[dict(rank=0,split='train')];a,r=supervise(x);check(len(a)==36 and len(r)==72,'FIXTURE_SIZE');check(sum(z['relation']=='FLIP' for z in r)==24,'FIXTURE_FLIP');return dict(status='PASS',answers=36,relations=72)

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--zip',required=True);args=p.parse_args();root=Path(args.root);reads=Reads(root);start=time.monotonic()
 try:
  seal=json.loads(reads.file(root/'code-seal.json'));check(hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==seal['science_lf_sha256'],'CODE_SEAL');write(root/'fixture.json',fixture())
  blob=reads.file(args.zip);check(len(blob)==390919 and hashlib.sha256(blob).hexdigest()=='950ae2f6766179743f27e512948730682e444eb1c235393d034e508081224cd2','PACKET_IDENTITY');packet=reads.expand(blob,1104895,NAMES);manifest=json.loads(packet['package-manifest.json']);check(len(manifest['members'])==11 and {m['name'] for m in manifest['members']}==NAMES-{'package-manifest.json'},'MANIFEST_COUNT_AND_ALLOWLIST')
  for m in manifest['members']:check(len(packet[m['name']])==m['bytes'] and hashlib.sha256(packet[m['name']]).hexdigest()==m['sha256'],'MEMBER_IDENTITY')
  for n,b in packet.items():
   with (root/n).open('xb') as f:f.write(b)
  original=packet['action_localisation_train_annotations.zip'];check(len(original)==222956 and hashlib.sha256(original).hexdigest()=='5b27beaa97df0a1ea258437b179ed17092981a93501a22a572d64dd46fb12575','ANNOTATION_IDENTITY');zi=zipfile.ZipFile(io.BytesIO(original));names={x.filename for x in zi.infolist()};check(names=={'action_localisation_train.json'},'ANNOTATION_MEMBER_ALLOWLIST');annotation=reads.expand(original,2692679,names);ab=next(iter(annotation.values()));check(len(ab)==2692679,'ANNOTATION_JSON_SIZE');raw=json.loads(ab);check(isinstance(raw,dict) and len(raw)==2135,'SOURCE_SCHEMA')
  cd=packet['central-directory.bin'];check(len(cd)==171100 and hashlib.sha256(cd).hexdigest()=='505019446df7a796909c8f00a63bd55a2e214d3ba533de00104001f0a30aac82','CENTRAL_IDENTITY');write(root/'construct-started.json',dict(epoch=time.time(),code_sha256=seal['science_lf_sha256']))
  selected,counts,rejected,allrows,entries=produce(raw,cd);answers,relations=supervise(selected);write(root/'source-rows.json',allrows);write(root/'selected.json',selected);write(root/'answers.json',answers);write(root/'relations.json',relations);write(root/'counts.json',dict(counts=counts,rejections=rejected));review=independent(raw,cd,selected,answers,relations);check(review['counts']==counts,'INDEPENDENT_COUNTS');check(review.pop('directory')==entries,'INDEPENDENT_DIRECTORY');write(root/'independent.json',review)
  # Validate sparse ZIP archive metadata without reading any media payload.
  tail=packet['archive-tail.bin'];at=tail.rfind(b'PK\x05\x06');check(at>=0 and at+22+int.from_bytes(tail[at+20:at+22],'little')==len(tail),'EOCD');eocd=struct.unpack_from('<4s4H2IH',tail,at);check(eocd[4] in (2184,65535) and eocd[5]==len(cd),'EOCD_DIRECTORY');offset=eocd[6]
  if offset==0xffffffff:
   za=tail.rfind(b'PK\x06\x06',0,at);locator=tail.rfind(b'PK\x06\x07',0,at);check(za>=0 and locator>=0,'ZIP64_TAIL');check(int.from_bytes(tail[za+32:za+40],'little')==2184 and int.from_bytes(tail[za+40:za+48],'little')==len(cd),'ZIP64_DIRECTORY');offset=int.from_bytes(tail[za+48:za+56],'little');check(offset+len(cd)+len(tail)-za==28404087974,'ARCHIVE_TOTAL_ZIP64')
  else:check(offset+len(cd)+len(tail)-at==28404087974,'ARCHIVE_TOTAL')
  readme=packet['source-README.md'];check(hashlib.sha1(b'blob '+str(len(readme)).encode()+b'\0'+readme).hexdigest()=='505cd675d6759962202747c2fd4970074a027df4','README_BLOB');registration=json.loads(packet['source-registration.json']);check(registration['revision']=='3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf' and registration['data_license']=='CC-BY-4.0','REGISTRATION')
  comparison=owner_compare(json.loads(packet['owner-preview-summary.json']),json.loads(packet['owner-selection-frozen.json']),selected,counts);write(root/'owner-comparison.json',comparison)
  stats=[]
  for split in ('train','development','test','total'):
   groups=[g for g in selected if split=='total' or g['split']==split];n=len(groups);stats.append(dict(split=split,planned_groups={'train':20,'development':4,'test':8,'total':32}[split],actual_groups=n,variants=6*n,questions_answers=36*n,FLIP=24*n,HOLD=48*n,compressed_bytes=sum(g['media']['compressed'] for g in groups),uncompressed_bytes=sum(g['media']['uncompressed'] for g in groups),status='QUALIFIED_METADATA_ONLY',unknown_groups=0))
  summary=dict(status='TIMESTAMPED_TRIPLE_SUPERVISION_READY / RGB_NOT_CONSTRUCTED / TRAINING_NOT_RUN',counts=counts,rejections=rejected,splits=stats,unique_selected_texts=len({e['text'] for g in selected for e in g['observation']['events']}),max_compressed_member=max(g['media']['compressed'] for g in selected),max_uncompressed_member=max(g['media']['uncompressed'] for g in selected),distinct_questions=len({q for g in selected for q in g['questions']}),source_frame_count_metadata=sum(raw[g['observation']['video_id']]['metadata']['num_frames'] for g in selected),methods=sorted({g['media']['method'] for g in selected}),independent=review,owner_comparison=comparison,q_only=dict(each_question_yes=3,each_question_no=3,item_accuracy_pct=50,all36_upper_bound=0,scope='CONSTRUCTION_IDENTITY_NOT_MODEL_SCORE'),model_scores='NA',research_network=0,media_reads=0,decodes=0,model_forwards=0,GPU=0,training_updates=0,source_overlap='POSSIBLE_SHARED_ORIGINAL_SOURCE / OLD_PHYSICAL_OVERLAP_UNKNOWN',worker_seconds=time.monotonic()-start)
  check(summary['unique_selected_texts']==29 and stats[-1]['compressed_bytes']==581426975 and stats[-1]['uncompressed_bytes']==579702574 and summary['max_compressed_member']==71166131 and summary['max_uncompressed_member']==70872100 and summary['distinct_questions']==138 and summary['source_frame_count_metadata']==28139 and summary['methods']==[12],'ACTUAL_AGGREGATES');write(root/'summary.json',summary)
 except Exception as e:write(root/'failure.json',dict(status='FAILED_ONCE_NO_RETRY',stage='CONSTRUCTION_OR_REVIEW',exception=type(e).__name__,reason=str(e),elapsed_seconds=time.monotonic()-start));raise
 finally:write(root/'logical-reads.json',dict(bytes=reads.count,limit=32*MIB,reads=reads.log,scope='shared in-process buffers counted once; archive inflation counted; not OS physical IO'))
if __name__=='__main__':main()
