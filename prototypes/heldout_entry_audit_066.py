"""066 metadata-only, stdlib roles. No science-module import or media/model access.

Reader projects observations immediately; admission reads projections only.
Publisher answers are read solely after the admission seal, by structure role.
"""
import argparse,ast,csv,hashlib,json,os,re,time,urllib.request,urllib.error,urllib.parse
from collections import Counter,defaultdict
from pathlib import Path
DY='fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405'
TB='bafceda3a2bd0e5128c390ec25fdc54e470a743d'
GH='03129551918c0830f3ee727485eb9cfb437e21e5'
SOURCES=[('dy','https://huggingface.co/datasets/ddz16/DyBench/resolve/'+DY+'/json/event_sequence.json'),('dy-card','https://huggingface.co/datasets/ddz16/DyBench/resolve/'+DY+'/README.md'),('tb','https://huggingface.co/datasets/BaiqiL/TimeBlind/resolve/'+TB+'/data.jsonl'),('tb-card','https://huggingface.co/datasets/BaiqiL/TimeBlind/resolve/'+TB+'/README.md')]+[(k,'https://raw.githubusercontent.com/Baiqi-Li/TimeBlind/'+GH+'/'+p) for k,p in [('tb-code-card','README.md'),('tb-tags','tags.json'),('tb-utils','utils.py')]]+[(k,'https://huggingface.co/api/datasets/'+d+'/tree/'+rev+'?recursive=true&expand=false') for k,d,rev in [('dy-tree','ddz16/DyBench',DY),('tb-tree','BaiqiL/TimeBlind',TB)]]
OBS_KEYS={'video','video_path','video_id','question','question_type','type','index','idx','id','source_category','source_subcategory','question_id','pair_id','source','source_id','original_video','original_video_id','recording_id','url','video_url','action1','action2','Action1','Action2','event1','event2','events'}
BLOCKED=re.compile('answer|label|gold|predict|correct|score|candidate|option|ground.?truth',re.I)
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tau(q):
 m=re.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
 if not m:raise ValueError('QUESTION_PARSE')
 return f'Does the event "{m[2]}" happen before the event "{m[1]}"? Answer Yes or No.'
def project(x):
 if isinstance(x,dict):return {k:project(v) for k,v in x.items() if not BLOCKED.search(k)}
 if isinstance(x,list):return [project(v) for v in x]
 return x
def acquire(root):
 root=Path(root);start=time.monotonic();used=0;ledger=[];redirects=[]
 class Redirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,req,fp,code,msg,headers,newurl):
   u=urllib.parse.urlparse(newurl)
   if u.scheme!='https' or u.hostname not in ('huggingface.co','raw.githubusercontent.com'):raise RuntimeError('REDIRECT_HOST_REJECTED')
   if u.hostname=='huggingface.co' and not (u.path.startswith('/api/resolve-cache/datasets/') and any(r in u.path for r in (DY,TB))):raise RuntimeError('REDIRECT_PATH_REJECTED')
   redirects.append(dict(source=req.full_url,target=newurl,status=code));return super().redirect_request(req,fp,code,msg,headers,newurl)
 opener=urllib.request.build_opener(Redirect())
 for key,url in SOURCES:
  if len(ledger)>=12 or time.monotonic()-start>=110:break
  rec=dict(key=key,url=url,state='STARTED',body_bytes=0);ledger.append(rec);Path(root/'network-started.json').write_text(json.dumps(ledger),encoding='utf-8');body=b'';t=time.monotonic()
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'VLM066-MetadataAudit','Accept-Encoding':'identity'})
   with opener.open(req,timeout=min(12,max(1,110-(time.monotonic()-start)))) as response:
    rec.update(status=response.status,final_url=response.url,content_encoding=response.headers.get('Content-Encoding','identity'),link=response.headers.get('Link'),revision_header=response.headers.get('X-Repo-Commit'))
    declared=response.headers.get('Content-Length')
    if declared and int(declared)>2*1024**2:raise RuntimeError('SINGLE_BODY_CAP_DECLARED')
    while True:
     if time.monotonic()-start>=110:raise RuntimeError('NETWORK_DEADLINE')
     chunk=response.read(min(65536,2*1024**2-len(body)+1,10*1024**2-used+1))
     if not chunk:break
     body+=chunk;used+=len(chunk)
     if len(body)>2*1024**2 or used>10*1024**2:raise RuntimeError('BODY_CAP')
   (root/(key+'.body')).write_bytes(body);rec.update(state='CLOSED',body_bytes=len(body),sha256=sha(root/(key+'.body')))
   if key in ('dy','tb'):
    rows=json.loads(body) if key=='dy' else [json.loads(line) for line in body.decode('utf-8-sig').splitlines() if line.strip()]
    observations=[dict(position=i,fields=project({k:v for k,v in row.items() if k in OBS_KEYS})) for i,row in enumerate(rows)]
    save(root/(key+'-observations.json'),observations);rec['raw_schema_keys']=sorted({k for row in rows for k in row});rec['projection_sha256']=sha(root/(key+'-observations.json'))
  except Exception as e:rec.update(state='FAILED',reason=type(e).__name__+':'+str(e),body_bytes=len(body))
  rec['outer_s']=time.monotonic()-t
  Path(root/'network.json').write_text(json.dumps(dict(requests=ledger,body_bytes=used,redirects_observed=redirects,outer_s=time.monotonic()-start),indent=2),encoding='utf-8')
 save(root/'acquisition-closed.json',dict(requests=len(ledger),body_bytes=used,outer_s=time.monotonic()-start,files=[dict(name=p.name,sha256=sha(p),bytes=p.stat().st_size) for p in root.glob('*.body')],projection_files=[dict(name=p.name,sha256=sha(p)) for p in root.glob('*-observations.json')]))
 print('ACQUIRED',len(ledger),'BODIES',used,'FAILURES',sum(x['state']!='CLOSED' for x in ledger),flush=True)

def qualify(root):
 root=Path(root);result={};eligible=[];observed=[]
 if (root/'dy-observations.json').exists():
  rows=read(root/'dy-observations.json');groups=defaultdict(list);videos=Counter(r['fields'].get('video') for r in rows)
  for row in rows:
   f=row['fields'];groups[(f.get('source_subcategory','UNKNOWN'),re.sub(r'_reversed(?=\.mp4$)','',f.get('video','')))].append(row)
  overall=dict(rows=len(rows),nominal_pairs=len(groups),category_rows=dict(Counter(x['fields'].get('source_subcategory','UNKNOWN') for x in rows)),excluded_old_categories={'Breakfast','50Salads'}.__len__())
  for cat in ('VIDHALLUC','TempCompass'):
   counts=Counter();pool=[]
   for (category,base),members in sorted(groups.items()):
    if category!=cat:continue
    counts['nominal_pairs']+=1;reason=None;events=None;qs=None
    if len(members)!=2 or len({x['fields'].get('video') for x in members})!=2:reason='PAIR_ROW_MEMBERSHIP'
    elif {x['fields']['video'] for x in members}!={base,base[:-4]+'_reversed.mp4'} or not base.endswith('.mp4'):reason='ORIGINAL_REVERSED_MEMBERSHIP'
    else:
     counts['complete_pairs']+=1
     if any(x['fields'].get('source_category')!='event_sequence' for x in members):reason='CATEGORY_FIELD'
     elif any(videos[x['fields']['video']]!=1 for x in members):reason='DUPLICATE_MEMBER'
     elif members[0]['fields'].get('question')!=members[1]['fields'].get('question'):reason='QUESTION_PAIR_MISMATCH'
     else:
      match=re.fullmatch(r'.*\nAction 1\. (.+)\nAction 2\. (.+)\nPlease output their order\.',members[0]['fields'].get('question',''),re.S)
      if not match:reason='EVENT_PARSE'
      else:
       counts['parsed_pairs']+=1;a,b=match.groups();normalize=lambda x:' '.join(x.replace('_',' ').split())
       if normalize(a)==normalize(b):reason='SAME_NORMALIZED_EVENT'
       else:
        counts['distinct_event_pairs']+=1;events=[a,b];qs=[f'Does the event "{a}" happen before the event "{b}"? Answer Yes or No.',f'Does the event "{b}" happen before the event "{a}"? Answer Yes or No.']
        try:
         if tau(qs[0])!=qs[1] or tau(qs[1])!=qs[0] or any(tau(tau(q))!=q for q in qs):reason='TAU_CLOSURE'
        except ValueError:reason='TAU_FORMAT'
    if reason:counts['excluded_'+reason]+=1
    else:
     counts['direct_format_pairs']+=1
     # No recording/participant key is fabricated from arbitrary filename pieces.
     shared={k:members[0]['fields'][k] for k in ('original_video_id','recording_id','source_id') if members[0]['fields'].get(k) and all(x['fields'].get(k)==members[0]['fields'][k] for x in members)}
     group_key=cat+'/'+(next(iter(shared))+':'+str(next(iter(shared.values()))) if shared else base)
     record=dict(category=cat,base=base,positions=[x['position'] for x in members],videos=[base,base[:-4]+'_reversed.mp4'],events=events,questions=qs,group_key=group_key,group_level='EXPLICIT_METADATA_ID' if shared else 'TWO_VIDEO_INSTANCE_ONLY',available_origin_fields=sorted(shared));pool.append(record);eligible.append(record)
    observed.append(dict(category=cat,base=base,positions=[x['position'] for x in members],reason=reason or 'ELIGIBLE_OBSERVATION'))
   counts['candidate_groups']=len({x['group_key'] for x in pool});counts['repeated_group_clusters']=sum(n>1 for n in Counter(x['group_key'] for x in pool).values());counts['raw_rows']=sum(x['fields'].get('source_subcategory')==cat for x in rows);result[cat]=dict(counts=counts,source_key_levels=dict(Counter(x['group_level'] for x in pool)))
  result['DyBench']=overall
  groupmap=defaultdict(list)
  for item in eligible:groupmap[item['group_key']].append(item)
  ordered=sorted(groupmap,key=lambda k:(hashlib.sha256(('VLM066/heldout/'+k).encode()).digest(),k.encode()));selected=[];skipped=[]
  for k in ordered:
   if len(selected)+len(groupmap[k])<=50:selected.extend(groupmap[k])
   else:skipped.append(k)
  result['selection']=dict(N=len(selected),groups=len({x['group_key'] for x in selected}),by_category=dict(Counter(x['category'] for x in selected)),unique_V=len({v for x in selected for v in x['videos']}),unique_q=len({q for x in selected for q in x['questions']}),tau_closure_union=len({tau(q) for x in selected for q in x['questions']}|{q for x in selected for q in x['questions']}),maximum=50,skipped_whole_groups=len(skipped))
  # Literal coverage is descriptive only, never a selection input.
  old_events=set();old_questions=set()
  for (cat,base),members in groups.items():
   if cat in ('Breakfast','50Salads'):
    m=re.fullmatch(r'.*\nAction 1\. (.+)\nAction 2\. (.+)\nPlease output their order\.',members[0]['fields'].get('question',''),re.S)
    if m:
     a,b=m.groups();old_events.update((a,b));old_questions.update((f'Does the event "{a}" happen before the event "{b}"? Answer Yes or No.',f'Does the event "{b}" happen before the event "{a}"? Answer Yes or No.'))
  result['literal_overlap_with_all_excluded_old_categories']=dict(selected_instances_any_event_seen=sum(any(e in old_events for e in x['events']) for x in selected),selected_instances_any_question_seen=sum(any(q in old_questions for q in x['questions']) for x in selected),not_a_train_only_coverage_claim=True)
 else:selected=[];result['DyBench']=dict(status='UNKNOWN_METADATA_NOT_ACQUIRED')
 if (root/'tb-observations.json').exists() and (root/'tb-tags.body').exists():
  rows=read(root/'tb-observations.json');tags=read(root/'tb-tags.body');indices=tags.get('Temporal_Relation',[]);look={x['fields'].get('index',x['fields'].get('idx',x['position'])):x for x in rows};tagset=set(indices);blocks=sorted({i//4 for i in tagset if type(i) is int});compatible=[];counts=Counter()
  for i in indices:
   if i not in look:counts['tag_index_missing']+=1;continue
   row=look[i];q=row['fields'].get('question','')
   try:
    derived=tau(q);assert tau(derived)==q;compatible.append(i)
   except (ValueError,AssertionError,TypeError):counts['original_question_format_incompatible']+=1
  counts.update(total_rows=len(rows),temporal_tag_rows=len(indices),unique_temporal_indices=len(tagset),nominal_four_index_blocks=len(blocks),full_tag_blocks=sum(all(4*b+j in tagset for j in range(4)) for b in blocks),direct_tau_rows=len(compatible),direct_tau_complete_blocks=sum(all(4*b+j in compatible for j in range(4)) for b in blocks),explicit_event_field_rows=sum(any(k in x['fields'] for k in ('Action1','Action2','action1','action2','event1','event2','events')) for x in rows))
  result['TimeBlind']=dict(counts=counts,observed_question_types=dict(Counter(str(x['fields'].get('question_type',x['fields'].get('type','UNKNOWN'))) for x in rows)),official_block_semantics='STATIC_SOURCE_REVIEW_REQUIRED',physical_source_independence='UNKNOWN',status='NO_DIRECT_ENTRY' if not compatible else 'DIRECT_ROWS_REQUIRE_BLOCK_AND_RELATION_EVIDENCE')
 else:result['TimeBlind']=dict(status='UNKNOWN_METADATA_NOT_ACQUIRED')
 save(root/'admission-private.json',dict(eligible=eligible,observed=observed,selected=selected,result=result));save(root/'admission-seal.json',dict(code_lf_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),observation_inputs=[dict(name=p.name,sha256=sha(p)) for p in root.glob('*-observations.json')],admission_sha256=sha(root/'admission-private.json'),answer_used_for_membership=False,at_unix=time.time()));save(root/'admission-aggregate.json',result);print('ADMISSION_SEALED','N',len(selected),'TB_DIRECT',result.get('TimeBlind',{}).get('counts',{}).get('direct_tau_rows','UNKNOWN'),flush=True)

def structure(root):
 root=Path(root);seal=read(root/'admission-seal.json');assert sha(root/'admission-private.json')==seal['admission_sha256'];a=read(root/'admission-private.json');result={}
 if (root/'dy.body').exists():
  rows=read(root/'dy.body');options=['First action 1, then action 2','First action 2, then action 1'];counts=defaultdict(Counter);selected={x['base'] for x in a['selected']}
  for x in a['eligible']:
   members=[rows[i] for i in x['positions']];valid=all(r.get('candidates')==options for r in members) and {r.get('answer') for r in members}==set(options)
   counts[x['category']]['publisher_four_cell_consistent' if valid else 'publisher_structure_failed']+=1
   if x['base'] in selected:counts['selected']['publisher_four_cell_consistent' if valid else 'publisher_structure_failed']+=1
  result['DyBench']={k:dict(v) for k,v in counts.items()}
 if (root/'tb.body').exists() and (root/'tb-tags.body').exists():
  rows=[json.loads(x) for x in (root/'tb.body').read_text(encoding='utf-8-sig').splitlines() if x.strip()];tags=read(root/'tb-tags.body').get('Temporal_Relation',[]);look={r.get('index',r.get('idx',i)):r for i,r in enumerate(rows)};counts=Counter()
  for b in sorted({i//4 for i in tags}):
   if not all(4*b+j in look for j in range(4)):counts['missing_block']+=1;continue
   answers=[str(look[4*b+j].get('answer','')).strip().rstrip('.').casefold() for j in range(4)]
   if not all(x in ('yes','no') for x in answers):counts['answer_structure_unknown']+=1
   elif answers[0]==answers[3] and answers[1]==answers[2] and answers[0]!=answers[1]:counts['diagonal_complement_pattern']+=1
   else:counts['other_answer_pattern']+=1
  result['TimeBlind']=dict(counts)
 save(root/'publisher-structure.json',dict(results=result,admission_unchanged=sha(root/'admission-private.json')==seal['admission_sha256'],qualification_not_reselected=True,only_publisher_metadata_no_model_scores=True));print('PUBLISHER_STRUCTURE_CLOSED',flush=True)

def metadata_details(root):
 """Static official index semantics and type-specific publisher structure; no admission change."""
 root=Path(root);out={};seal=read(root/'admission-seal.json');assert sha(root/'admission-private.json')==seal['admission_sha256']
 if (root/'tb-observations.json').exists() and (root/'tb-utils.body').exists():
  obs=read(root/'tb-observations.json');rows=[x['fields'] for x in obs];indices=[x.get('index') for x in rows];look={x['index']:x for x in rows};src=(root/'tb-utils.body').read_text(encoding='utf-8');tree=ast.parse(src)
  functions={x.name:ast.get_source_segment(src,x) for x in tree.body if isinstance(x,ast.FunctionDef)}
  proof=all(s in functions.get('build_answers','') for s in ('sample_id = idx // 4','role = idx % 4','pred_q0_i0 = group[0]','pred_q0_i1 = group[1]','pred_q1_i0 = group[2]','pred_q1_i1 = group[3]')) and all(s in functions.get('get_tag_scores','') for s in ('range(0, len(indices), 4)','chunk = indices[s:s + 4]','"q0_i0": vals[0]','"q1_i1": vals[3]'))
  tags=read(root/'tb-tags.body')['Temporal_Relation'];blocks=[sorted(tags)[i:i+4] for i in range(0,len(tags),4)];counts=Counter();pairs=[]
  for chunk in blocks:
   if len(chunk)!=4 or not all(i in look for i in chunk):counts['block_missing']+=1;continue
   rs=[look[i] for i in chunk];counts['blocks_'+str(rs[0].get('type','UNKNOWN'))]+=1
   counts['qmajor_video_question_binding_pass']+=int(rs[0]['video_path']==rs[2]['video_path'] and rs[1]['video_path']==rs[3]['video_path'] and rs[0]['video_path']!=rs[1]['video_path'] and rs[0]['question']==rs[1]['question'] and rs[2]['question']==rs[3]['question'] and rs[0]['question']!=rs[2]['question'])
   pairs.append(tuple(sorted({x['video_path'] for x in rs})))
   counts['block_aligns_global_index_div4']+=int(chunk==list(range(chunk[0],chunk[0]+4)) and chunk[0]%4==0)
  direct=Counter()
  for row in rows:
   try:derived=tau(row['question']);assert tau(derived)==row['question'];direct[str(row.get('type'))]+=1
   except (ValueError,AssertionError,TypeError):pass
  raw=[json.loads(x) for x in (root/'tb.body').read_text(encoding='utf-8-sig').splitlines() if x.strip()];pub=Counter()
  for chunk in blocks:
   rs=[raw[i] for i in chunk];typ=rs[0]['type'];v=[str(x.get('answer','')).strip().rstrip('.').casefold() for x in rs];mapping={'yes':1,'no':0} if typ=='yes_no' else {'a':1,'b':0} if typ=='multiple_choice' else {}
   if not all(x in mapping for x in v):pub[typ+'_unknown']+=1;continue
   labels=[mapping[x] for x in v];pub[typ+('_diagonal_complement' if labels[0]==labels[3] and labels[1]==labels[2] and labels[0]!=labels[1] else '_other_pattern')]+=1
  out['TimeBlind']=dict(unique_index_count=len(set(indices)),row_index_equals_position=indices==list(range(len(rows))),index_collision_rows=len(indices)-len(set(indices)),official_group_semantics_verified_static=proof,official_role_order=['q0_i0','q0_i1','q1_i0','q1_i1'],group_checks=dict(counts),temporal_unique_exact_video_pair_keys=len(set(pairs)),temporal_repeated_exact_video_pair_clusters=sum(n>1 for n in Counter(pairs).values()),all_dataset_direct_tau_by_type=dict(direct),publisher_structure_by_native_type=dict(pub),not_strict_before_or_physical_independence_certification=True)
 for key,media in [('dy-tree','video/event_sequence.zip'),('tb-tree',None)]:
  if (root/(key+'.body')).exists():
   files=read(root/(key+'.body'));out[key]=dict(entries=len(files),file_entries=sum(x.get('type')=='file' for x in files),known_media_bytes=sum(x.get('size',0) for x in files if x.get('type')=='file' and x.get('path','').lower().endswith(('.mp4','.zip'))),event_archive_bytes=next((x.get('size') for x in files if x.get('path')==media),None),listed_direct_mp4_objects=sum(x.get('type')=='file' and x.get('path','').endswith('.mp4') for x in files))
 save(root/'metadata-details.json',dict(results=out,admission_unchanged=sha(root/'admission-private.json')==seal['admission_sha256'],type_specific_structure_extension='Native yes/no and A/B interpreted only after frozen observation selection;initial yes/no-only54unknown retained separately;no re-selection'));print('STATIC_INDEX_AND_TYPE_DETAILS_CLOSED',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('role',choices=('acquire','qualify','structure','metadata_details'));p.add_argument('--root',required=True);a=p.parse_args();globals()[a.role](a.root)
