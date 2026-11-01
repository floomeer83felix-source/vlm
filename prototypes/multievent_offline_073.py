"""073 offline metadata construction. Explicit CLI only; no network/model imports."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import time
import zipfile
import re
import itertools
from collections import Counter

REV = 'da3065053d958c38151304e33a42e138b1899eaf'
CAPS = {'api.json': 2*1024**2, 'README.md': 32*1024,
        'answer_final.json': 2*1024**2}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False)


def write_new(path, value):
    with open(path, 'xb') as f:
        f.write((canonical(value)+'\n').encode('utf-8'))
        f.flush()
        os.fsync(f.fileno())


def check(ok, reason):
    if not ok:
        raise ValueError(reason)


def input_gate(source):
    """One buffered read of three original members; no QA parsing or extraction."""
    start = time.monotonic()
    source = Path(source)
    physical_container_read = 0
    if source.is_file():
        check(source.suffix.lower() == '.zip', 'INPUT_NOT_ZIP_OR_DIRECTORY')
        check(source.stat().st_size <= 4*1024**2, 'ZIP_CONTAINER_OVER_4MIB')
        blob = source.read_bytes()
        physical_container_read = len(blob)
        z = zipfile.ZipFile(io.BytesIO(blob))
        names = z.infolist()
        check(len(names) <= 64, 'TOO_MANY_ZIP_ENTRIES')
        chosen = {}
        for name, cap in CAPS.items():
            matches = [x for x in names if not x.is_dir() and
                       x.filename.replace('\\', '/').split('/')[-1] == name]
            check(len(matches) == 1, 'MISSING_OR_AMBIGUOUS_'+name)
            item = matches[0]
            check(item.file_size <= cap, 'SIZE_CAP_'+name)
            check(not item.flag_bits & 1, 'ENCRYPTED_MEMBER')
            chosen[name] = item
        check(sum(x.file_size for x in chosen.values()) <= 4*1024**2, 'TOTAL_CAP')
        data = {k: z.read(v) for k, v in chosen.items()}
        z.close()
    else:
        check(source.is_dir(), 'INPUT_DIRECTORY_MISSING')
        for name, cap in CAPS.items():
            p = source/name
            check(p.is_file(), 'MISSING_'+name)
            check(p.stat().st_size <= cap, 'SIZE_CAP_'+name)
        check(sum((source/k).stat().st_size for k in CAPS) <= 4*1024**2, 'TOTAL_CAP')
        data = {k: (source/k).read_bytes() for k in CAPS}
    for name, b in data.items():
        check(len(b) <= CAPS[name], 'ACTUAL_SIZE_CAP_'+name)
        check(not b.lstrip().lower().startswith((b'<!doctype html', b'<html')), 'HTML_'+name)
    api = json.loads(data['api.json'].decode('utf-8'))
    check(api.get('sha') == REV, 'API_REVISION_MISMATCH')
    check(api.get('private') is False, 'API_PRIVATE_OR_UNKNOWN')
    check(api.get('gated') is False, 'API_GATED_OR_UNKNOWN')
    identities = {}
    for name in ('README.md', 'answer_final.json'):
        entries = [v for v in api.get('siblings', []) if v.get('rfilename') == name]
        check(len(entries) == 1, 'API_REGISTRATION_'+name)
        entry, b = entries[0], data[name]
        check(entry.get('size') == len(b), 'API_SIZE_MISMATCH_'+name)
        if entry.get('lfs'):
            expected = entry['lfs'].get('sha256')
            actual = hashlib.sha256(b).hexdigest()
            check(entry['lfs'].get('size') == len(b), 'LFS_SIZE_'+name)
            kind = 'LFS_SHA256'
        else:
            expected = entry.get('blobId')
            actual = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            kind = 'GIT_BLOB_SHA1'
        check(expected == actual, 'API_CONTENT_IDENTITY_MISMATCH_'+name)
        identities[name] = dict(kind=kind, identity=actual, size=len(b))
    elapsed = time.monotonic()-start
    check(elapsed <= 15, 'PREFLIGHT_TIME_OVER_15_SECONDS')
    return data, dict(status='PASS', revision=REV, seconds=elapsed,
                      source_logical_bytes=sum(map(len, data.values())),
                      zip_container_bytes=physical_container_read,
                      sizes={k: len(v) for k, v in data.items()}, identities=identities,
                      provenance='USER_SUPPLIED_FIXED_REVISION_COPY / OFFLINE_CROSS_FILE_IDENTITIES_MATCH',
                      source=str(source))


def observe(root):
    """Single shape-only observation. Never prints original QA or answer values."""
    from collections import Counter
    root = Path(root)
    write_new(root/'observation-started.json', {'state': 'STARTED'})
    b = (root/'answer_final.json').read_bytes()
    x = json.loads(b)
    candidates = []
    def visit(v, path):
        if isinstance(v, list):
            if v and all(isinstance(r, dict) and {'qa_id','video_id','format'} <= set(r) for r in v):
                candidates.append((path, v))
            else:
                for i, r in enumerate(v):
                    visit(r, path+[i])
        elif isinstance(v, dict):
            for k, r in v.items():
                visit(r, path+[k])
    visit(x, [])
    def shape(v, depth=0):
        if depth > 3:
            return type(v).__name__
        if isinstance(v, dict):
            return {k: shape(r, depth+1) for k,r in v.items()}
        if isinstance(v, list):
            return {'type': 'list', 'length': len(v), 'element_shapes':
                    list({canonical(shape(r, depth+1)) for r in v[:4]})}
        return type(v).__name__
    report = {'root_shape': shape(x, 3), 'collections': []}
    for path, rows in candidates:
        selected = [r for r in rows if r['format'] in ('ordering_3','ordering_4')]
        report['collections'].append({'path': path, 'n': len(rows),
            'formats': dict(Counter(r['format'] for r in rows)),
            'row_keys': sorted({k for r in rows for k in r}),
            'ordering_shapes': list({canonical(shape(r)) for r in selected})})
    api = json.loads((root/'api.json').read_bytes())
    report['api_keys'] = sorted(api)
    report['sibling_count'] = len(api['siblings'])
    report['sibling_schema'] = shape(api['siblings'][0])
    card = (root/'README.md').read_text(encoding='utf-8')
    report['card_evidence_lines'] = [s for s in card.splitlines() if
        any(k in s.lower() for k in ('license', 'rights', 'permission','non-overlap','timestamp','chronolog','temporal order','duration','source datasets','source:'))
        and not any(k in s.lower() for k in ('question', 'correct_order', 'events', 'qa_id'))]
    report['source_logical_bytes'] = len(b)+len((root/'api.json').read_bytes())+len(card.encode('utf-8'))
    # API is read twice above; both full-container reads count.
    report['source_logical_bytes'] += (root/'api.json').stat().st_size
    write_new(root/'schema-observation.json', report)
    print(canonical(report))


TEMPLATE = 'Does the event "{}" happen before the event "{}"? Answer Yes or No.'
PATTERN = r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.'
TEMPORAL = re.compile(r'\b(before|after|first|second|third|fourth|then|earlier|later|finally)\b', re.I)


def tau(q):
    # Byte-for-byte original062 regex and exchange, without importing torch code.
    m = re.fullmatch(PATTERN, q)
    if not m:
        raise ValueError('QUESTION_PARSE')
    return TEMPLATE.format(m[2], m[1])


def unresolved(value):
    if isinstance(value, dict):
        for k,v in value.items():
            if re.search(r'uncertain|unresolved|pending|ambiguous', k, re.I) and v not in (None,False,0,'',[],{}):
                return True
            if unresolved(v):
                return True
    elif isinstance(value, list):
        return any(unresolved(v) for v in value)
    elif isinstance(value, str):
        return bool(re.search(r'\b(uncertain|unresolved|pending|ambiguous)\b', value, re.I))
    return False


def locate(api, video_id):
    # Exact complete filename stem equality only; no fuzzy/substrings/extensions guessed.
    matches = [r for r in api['siblings'] if
               r['rfilename'].startswith('videos/') and
               Path(r['rfilename']).stem == video_id and
               Path(r['rfilename']).suffix.lower() in ('.mp4','.avi','.mov','.webm','.mkv')]
    if len(matches) != 1:
        return {'status': 'MEDIA_LOCATOR_UNKNOWN', 'exact_id_matches': len(matches),
                'source_namespace': 'SOURCE_UNKNOWN'}
    r = matches[0]
    identity = {'kind': 'LFS_SHA256', 'value': r['lfs'].get('sha256')} if r.get('lfs') else {'kind':'GIT_BLOB_SHA1','value':r.get('blobId')}
    return {'status': 'UNIQUE_EXACT_VIDEO_ID_TO_API_FILENAME_STEM',
            'path':r['rfilename'], 'size':r.get('size'), 'identity':identity,
            'source_namespace':str(Path(r['rfilename']).parent).replace('\\','/')}


def collection(bundle):
    found = []
    def walk(v, p):
        if isinstance(v,list):
            if v and all(isinstance(x,dict) and {'qa_id','video_id','format'} <= set(x) for x in v):
                found.append((p,v))
            else:
                for i,x in enumerate(v):walk(x,p+[i])
        elif isinstance(v,dict):
            for k,x in v.items():walk(x,p+[k])
    walk(bundle,[])
    check(len(found)==1,'NONUNIQUE_ENTRY_COLLECTION')
    return found[0]


def eligible(row, qa_counts, api):
    if row['format'] not in ('ordering_3','ordering_4'):
        return 'NOT_ORDERING', None
    if not isinstance(row['qa_id'],str) or not row['qa_id'] or qa_counts[row['qa_id']]!=1:
        return 'QA_ID_NOT_UNIQUE', None
    if not isinstance(row['video_id'],str) or not row['video_id']:
        return 'VIDEO_ID_UNKNOWN', None
    # Label/order and original question are deliberately absent from eligibility.
    if unresolved({k:v for k,v in row.items() if k not in ('correct_order','correct_answer','question','events')}):
        return 'PUBLISHER_UNRESOLVED_MARKER', None
    es = row.get('events')
    n = 3 if row['format']=='ordering_3' else 4
    if not isinstance(es,list) or len(es)!=n:
        return 'EVENT_CARDINALITY_OR_SCHEMA', None
    if any(not isinstance(e,dict) or set(e)!= {'label','event_text'} or
           not isinstance(e['label'],str) or not e['label'] or
           not isinstance(e['event_text'],str) for e in es):
        return 'EVENT_ID_TEXT_MAPPING_UNKNOWN', None
    events = {e['label']:' '.join(e['event_text'].split()) for e in es}
    if len(events)!=n or any(not t or re.fullmatch(r'event[ _-]*\d+',t,re.I) for t in events.values()) or len(set(events.values()))!=n:
        return 'EVENT_ID_TEXT_NONUNIQUE_OR_EMPTY', None
    if any(TEMPORAL.search(t) for t in events.values()):
        return 'EXPLICIT_TEMPORAL_WORD_IN_EVENT', None
    if unresolved(events):
        return 'PUBLISHER_UNRESOLVED_MARKER', None
    ids = sorted(events,key=lambda x:x.encode('utf-8'))[:3]
    selected = {i:events[i] for i in ids}
    for a,b in itertools.permutations(ids,2):
        q = TEMPLATE.format(selected[a],selected[b])
        m = re.fullmatch(PATTERN,q)
        if not m or m.groups()!=(selected[a],selected[b]) or tau(tau(q))!=q or tau(q)!=TEMPLATE.format(selected[b],selected[a]):
            return 'STRICT_TAU_BINDING_FAILED', None
    media = locate(api,row['video_id'])
    obs = {'source_namespace':media['source_namespace'], 'video_id':row['video_id'],
           'qa_id':row['qa_id'], 'media_path':media.get('path'), 'events':selected}
    return 'ELIGIBLE_OBSERVATION', {'observation':obs,'events':events,'media':media}


def fixture():
    # Text/integer only. Distinct synthetic strings have no experimental meaning.
    texts = ['alpha action','beta action','gamma action']
    qs = [TEMPLATE.format(a,b) for a,b in itertools.permutations(texts,2)]
    for q in qs:check(tau(tau(q))==q,'FIXTURE_TAU')
    orders = list(itertools.permutations(range(3)))
    labels = [[int(p.index(a)<p.index(b)) for a,b in itertools.permutations(range(3),2)] for p in orders]
    check(all(sum(x)==3 for x in labels),'FIXTURE_BALANCE')
    flips=holds=edges=0
    for p in orders:
        for i in (0,1):
            q=list(p);q[i],q[i+1]=q[i+1],q[i];q=tuple(q);edges+=1
            a,b=labels[orders.index(p)],labels[orders.index(q)]
            flips+=sum(x!=y for x,y in zip(a,b));holds+=sum(x==y for x,y in zip(a,b))
    check((edges,flips,holds)==(12,24,48),'FIXTURE_RELATIONS')
    return dict(questions=6,symbolic_cells=36,relations=72,flip=24,hold=48,model_calls=0)


def construct(root):
    root=Path(root)
    start=time.monotonic()
    seal=json.loads((root/'formal-code-seal.json').read_text(encoding='utf-8'))
    check(hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==seal['producer_lf_sha256'],'CODE_SEAL')
    write_new(root/'construction-started.json',{'state':'STARTED','selection_domain':'VLM072/select/','code':seal})
    raw={k:(root/k).read_bytes() for k in CAPS}
    api=json.loads(raw['api.json']);bundle=json.loads(raw['answer_final.json'])
    path,rows=collection(bundle)
    qa=Counter(r['qa_id'] for r in rows)
    excluded=Counter(); candidates=[]; exclusions=[]
    source_counts=Counter(locate(api,r['video_id'])['source_namespace'] for r in rows)
    for i,r in enumerate(rows):
        reason,record=eligible(r,qa,api)
        excluded[reason]+=1
        if record is None:
            exclusions.append({'index':i,'qa_id':r['qa_id'],'reason':reason})
            continue
        ob=canonical(record['observation']).encode('utf-8')
        record.update(row_index=i,sort_digest=hashlib.sha256(b'VLM072/select/'+ob).hexdigest())
        candidates.append(record)
    candidates.sort(key=lambda r:(r['sort_digest'],canonical(r['observation']).encode('utf-8')))
    best={}
    for r in candidates:best.setdefault(r['observation']['video_id'],r)
    selected=list(best.values())[:24]
    # Persist observation-only selection BEFORE accessing any selected correct_order.
    write_new(root/'selection-frozen.json',{'rule':'VLM072/select/','collection_path':path,
        'selected':[{'row_index':r['row_index'],'digest':r['sort_digest'],'observation':r['observation']} for r in selected],
        'exclusions':exclusions,'counts':dict(excluded),'per_video_candidates':len(best)})
    manifest=[];symbolic=[];relations=[]; statuses=Counter(); media_bytes=0;media_known=0
    all_questions=set(); all_videos=set(); all_qas=set()
    for number,r in enumerate(selected):
        row=rows[r['row_index']]; ids=list(r['observation']['events']); events=r['observation']['events']
        order=row.get('correct_order');full_ids=set(r['events'])
        status='VALID_PUBLISHER_ORDER' if isinstance(order,list) and all(isinstance(v,str) for v in order) and len(order)==len(full_ids) and len(set(order))==len(order) and set(order)==full_ids else 'INVALID_FULL_EVENT_ORDER'
        statuses[status]+=1
        filtered=[i for i in order if i in ids] if status=='VALID_PUBLISHER_ORDER' else None
        questions=[]
        for a,b in itertools.permutations(ids,2):
            q=TEMPLATE.format(events[a],events[b]);all_questions.add(q)
            questions.append({'event_a':a,'event_b':b,'question':q,'tau':tau(q),
                              'label':int(filtered.index(a)<filtered.index(b)) if filtered else None,
                              'status':status})
        all_videos.add(row['video_id']);all_qas.add(row['qa_id'])
        if r['media'].get('size') is not None and r['media']['identity'].get('value'):
            media_bytes+=r['media']['size'];media_known+=1
        manifest.append({'position':number,**r,'format':row['format'],'publisher_full_order':order,
                         'publisher_selected_order':filtered,'status':status,'questions':questions,
                         'label_level':'PUBLISHER_ORDER_DERIVED','formal_strict_temporal_scoring':'CONDITIONAL_NOT_CERTIFIED'})
        perms=list(itertools.permutations(ids))
        for pi,p in enumerate(perms):
            for qi,q in enumerate(questions):
                symbolic.append({'group':number,'permutation':pi,'order':list(p),'question_index':qi,
                    'question':q['question'],'label':int(p.index(q['event_a'])<p.index(q['event_b']))})
            for adjacent in (0,1):
                target=list(p);target[adjacent],target[adjacent+1]=target[adjacent+1],target[adjacent]
                pj=perms.index(tuple(target))
                for qi,q in enumerate(questions):
                    y=int(p.index(q['event_a'])<p.index(q['event_b']))
                    z=int(target.index(q['event_a'])<target.index(q['event_b']))
                    relations.append({'group':number,'from':pi,'to':pj,'question_index':qi,
                                      'from_label':y,'to_label':z,'relation':'FLIP' if y!=z else 'HOLD'})
    k=len(selected)
    write_new(root/'manifest.json',manifest)
    write_new(root/'symbolic-cells.json',symbolic)
    write_new(root/'symbolic-relations.json',relations)
    artifacts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
               [root/'selection-frozen.json',root/'manifest.json',root/'symbolic-cells.json',root/'symbolic-relations.json']}
    # Evidence inventory is scoped to supplied JSON/schema/card. No claim about unread media.
    card=raw['README.md'].decode('utf-8')
    all_keys=Counter()
    def keys(v):
        if isinstance(v,dict):
            for key,value in v.items():all_keys[key]+=1;keys(value)
        elif isinstance(v,list):
            for value in v:keys(value)
    keys(bundle)
    evidence_keys={key:count for key,count in all_keys.items() if re.search(r'start|end|time|bound|overlap|unique|clock|duration|path|source|uncertain|unresolved|pending',key,re.I)}
    ready=k==24 and statuses.get('VALID_PUBLISHER_ORDER',0)==k and media_known==k
    summary={'status':'OFFLINE_FIXED_MULTIQUERY_LABEL_PLAN_READY / USER_SUPPLIED_SOURCE_PROVENANCE / MEDIA_HOLD' if ready else 'PARTIAL_OR_NO_MULTIEVENT_ENTRY',
        'revision':REV,'provenance':'USER_SUPPLIED_FIXED_REVISION_COPY / OFFLINE_CROSS_FILE_IDENTITIES_MATCH',
        'collection_path':path,'rows':len(rows),'unique_qa_ids':len(qa),'duplicate_qa_id_excess':len(rows)-len(qa),
        'duplicate_exact_rows_excess':len(rows)-len({canonical(r) for r in rows}),
        'unique_video_ids':len({r['video_id'] for r in rows}),'format_counts':dict(Counter(r['format'] for r in rows)),
        'source_counts':dict(source_counts),'eligibility_partition':dict(excluded),'eligible_observations':len(candidates),
        'eligible_unique_videos':len(best),'same_video_candidates_removed':len(candidates)-len(best),
        'eligible_unique_videos_not_selected':max(0,len(best)-24),
        'selected_k':k,'selected_valid':statuses.get('VALID_PUBLISHER_ORDER',0),
        'selected_invalid':statuses.get('INVALID_FULL_EVENT_ORDER',0),'selected_unknown':0,
        'selection_domain':'VLM072/select/','selection_digest_tiebreak':'full digest, then canonical observation UTF8 bytes',
        'native_questions':6*k,'native_valid_labels':6*statuses.get('VALID_PUBLISHER_ORDER',0),
        'native_unknown_labels':6*statuses.get('INVALID_FULL_EVENT_ORDER',0),
        'unique_native_videos':len(all_videos),'unique_native_questions_including_tau':len(all_questions),
        'symbolic_cells':len(symbolic),'symbolic_relations':len(relations),
        'symbolic_flip':sum(x['relation']=='FLIP' for x in relations),'symbolic_hold':sum(x['relation']=='HOLD' for x in relations),
        'media_locators_with_size_identity':media_known,'selected_published_media_bytes_known':media_bytes,
        'media_bytes_complete':media_known==k,'media_locator_rule':'unique full video_id equality to API videos filename stem; no similar-name matching',
        'evidence_keys':evidence_keys,'event_boundaries':'NOT_PRESENT_IN_SUPPLIED_SCHEMA; ACTUAL_MEDIA_UNKNOWN',
        'strict_nonoverlap':'NOT_CERTIFIED','physical_unique_occurrence':'NOT_CERTIFIED','boundary_units':'UNKNOWN',
        'source_media_clock':'UNKNOWN','splice_permission':'NOT_GRANTED_BY_CARD; THIRD_PARTY_TERMS_REQUIRED',
        'controlled_media':'CONTROLLED_MEDIA_CONSTRUCTION_HOLD','label_semantics':'PUBLISHER_ORDER_DERIVED; EXACT_COMPLETE_ORDER; strict completion/nonoverlap unspecified',
        'physical_source_independence':'UNKNOWN','old_data_or_pretraining_overlap':'UNKNOWN',
        'card_license_other':bool(re.search(r'^license: other$',card,re.M)),
        'card_third_party_not_relicensed':'does not relicense third-party media' in card,
        'publisher_root_metadata':{key:value for key,value in bundle.items() if key!='items'},
        'source_logical_bytes':sum(map(len,raw.values())), 'fixture':fixture(),
        'artifact_sha256':artifacts,'code_lf_sha256':seal['producer_lf_sha256'],
        'future_native_feature_calls':len(all_videos)+len(all_questions),'future_36_head_cpu_cells':36*6*k,
        'future_media_512mib_size_gate':media_known==k and media_bytes<=512*1024**2,
        'model_accuracy':None,'model_calls':0,'training_updates':0,'metadata_network_requests':0,
        'seconds':time.monotonic()-start}
    write_new(root/'construction-aggregate-private.json',summary)
    print(canonical({key:value for key,value in summary.items() if key not in
                    ('artifact_sha256','publisher_root_metadata','source_counts','evidence_keys')}))


def independent_review(root):
    """Independent stdlib oracle; no producer imports/calls or network.

    Rebuilds selection, native questions/order and symbolic results directly from
    the three original copies. Does not call eligible/locate/tau/construct/fixture.
    """
    import json as J
    import hashlib as H
    import re as R
    import itertools as IT
    from pathlib import Path as P
    from collections import Counter as Cnt
    import time as T
    start=T.monotonic(); root=P(root); checks=0
    def verify(v,name):
        nonlocal checks
        checks+=1
        if not v:raise AssertionError(name)
    def canon(x):return J.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
    bs={n:(root/n).read_bytes() for n in ('api.json','README.md','answer_final.json')}
    api=J.loads(bs['api.json']);bundle=J.loads(bs['answer_final.json'])
    verify(api['sha']=='da3065053d958c38151304e33a42e138b1899eaf','revision')
    verify(api['private'] is False and api['gated'] is False,'public')
    for n in ('README.md','answer_final.json'):
        e=[v for v in api['siblings'] if v['rfilename']==n];verify(len(e)==1,'registration')
        e=e[0];b=bs[n];verify(e['size']==len(b),'size')
        if e.get('lfs'):verify(e['lfs']['sha256']==H.sha256(b).hexdigest() and e['lfs']['size']==len(b),'lfs')
        else:verify(e['blobId']==H.sha1(('blob %d\0'%len(b)).encode()+b).hexdigest(),'git_blob')
    coll=[]
    pending=[([],bundle)]
    while pending:
        p,v=pending.pop()
        if isinstance(v,list):
            if v and all(isinstance(x,dict) and all(k in x for k in ('qa_id','video_id','format')) for x in v):coll.append((p,v))
            else:pending.extend((p+[i],x) for i,x in enumerate(v))
        elif isinstance(v,dict):pending.extend((p+[k],x) for k,x in v.items())
    verify(len(coll)==1,'unique_collection');path,rows=coll[0]
    summary=J.loads((root/'construction-aggregate-private.json').read_bytes())
    frozen=J.loads((root/'selection-frozen.json').read_bytes())
    manifest=J.loads((root/'manifest.json').read_bytes())
    symbolic=J.loads((root/'symbolic-cells.json').read_bytes())
    relations=J.loads((root/'symbolic-relations.json').read_bytes())
    counts=Cnt(x['qa_id'] for x in rows); reasons=Cnt();candidates=[];excluded=[];sourcecounts=Cnt()
    def uncertain(v):
        stack=[v]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                for k,val in x.items():
                    if R.search('uncertain|unresolved|pending|ambiguous',k,R.I) and val not in (None,False,0,'',[],{}):return True
                    stack.append(val)
            elif isinstance(x,list):stack.extend(x)
            elif isinstance(x,str) and R.search(r'\b(uncertain|unresolved|pending|ambiguous)\b',x,R.I):return True
        return False
    for index,row in enumerate(rows):
        video=row['video_id']
        files=[]
        for f in api['siblings']:
            segments=f['rfilename'].split('/');basename=segments[-1];stem,_,extension=basename.rpartition('.')
            if segments[0]=='videos' and stem==video and extension.lower() in ('mp4','avi','mov','webm','mkv'):files.append(f)
        if len(files)==1:
            f=files[0];namespace=f['rfilename'].rsplit('/',1)[0]
            media={'status':'UNIQUE_EXACT_VIDEO_ID_TO_API_FILENAME_STEM','path':f['rfilename'],'size':f.get('size'),
                'identity':{'kind':'LFS_SHA256','value':f['lfs'].get('sha256')} if f.get('lfs') else {'kind':'GIT_BLOB_SHA1','value':f.get('blobId')},'source_namespace':namespace}
        else:
            namespace='SOURCE_UNKNOWN';media={'status':'MEDIA_LOCATOR_UNKNOWN','exact_id_matches':len(files),'source_namespace':namespace}
        sourcecounts[namespace]+=1
        reason=None;es=row.get('events');events={}
        if row['format'] not in ('ordering_3','ordering_4'):reason='NOT_ORDERING'
        elif not isinstance(row['qa_id'],str) or not row['qa_id'] or counts[row['qa_id']]!=1:reason='QA_ID_NOT_UNIQUE'
        elif not isinstance(video,str) or not video:reason='VIDEO_ID_UNKNOWN'
        elif uncertain({k:v for k,v in row.items() if k not in ['correct_order','correct_answer','question','events']}):reason='PUBLISHER_UNRESOLVED_MARKER'
        elif not isinstance(es,list) or len(es)!={'ordering_3':3,'ordering_4':4}[row['format']]:reason='EVENT_CARDINALITY_OR_SCHEMA'
        elif any(not isinstance(e,dict) or sorted(e)!=['event_text','label'] or not isinstance(e['label'],str) or not e['label'] or not isinstance(e['event_text'],str) for e in es):reason='EVENT_ID_TEXT_MAPPING_UNKNOWN'
        else:
            for e in es:events[e['label']]=R.sub(r'\s+',' ',e['event_text']).strip()
            if len(events)!=len(es) or any(not t or R.fullmatch(r'event[ _-]*\d+',t,R.I) for t in events.values()) or len(set(events.values()))!=len(es):reason='EVENT_ID_TEXT_NONUNIQUE_OR_EMPTY'
            elif any(R.search(r'\b(before|after|first|second|third|fourth|then|earlier|later|finally)\b',t,R.I) for t in events.values()):reason='EXPLICIT_TEMPORAL_WORD_IN_EVENT'
            elif uncertain(events):reason='PUBLISHER_UNRESOLVED_MARKER'
            else:
                ids=sorted(events,key=lambda s:s.encode())[:3]
                for a in ids:
                    for b in ids:
                        if a==b:continue
                        text='Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(events[a],events[b])
                        match=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',text)
                        if not match or match.groups()!=(events[a],events[b]):reason='STRICT_TAU_BINDING_FAILED';break
        if reason:
            reasons[reason]+=1;excluded.append({'index':index,'qa_id':row['qa_id'],'reason':reason});continue
        reasons['ELIGIBLE_OBSERVATION']+=1
        obs={'source_namespace':namespace,'video_id':video,'qa_id':row['qa_id'],'media_path':media.get('path'),'events':{i:events[i] for i in ids}}
        payload=canon(obs).encode();digest=H.sha256(b'VLM072/select/'+payload).hexdigest()
        candidates.append((digest,payload,index,obs,events,media))
    candidates.sort();seen=set();unique=[]
    for c in candidates:
        if c[3]['video_id'] not in seen:seen.add(c[3]['video_id']);unique.append(c)
    chosen=unique[:24]
    expected=[{'row_index':c[2],'digest':c[0],'observation':c[3]} for c in chosen]
    verify(frozen=={'rule':'VLM072/select/','collection_path':path,'selected':expected,'exclusions':excluded,'counts':dict(reasons),'per_video_candidates':len(unique)},'frozen_selection_and_exclusions')
    verify(len(manifest)==len(chosen),'fixed_denominator')
    valid=invalid=known=totalbytes=0;questions=set();s_expected=[];r_expected=[]
    for position,(c,m) in enumerate(zip(chosen,manifest)):
        digest,payload,index,obs,all_events,media=c;row=rows[index]
        ids=sorted(obs['events'],key=lambda s:s.encode());order=row.get('correct_order')
        ok=isinstance(order,list) and all(isinstance(e,str) for e in order) and len(order)==len(all_events) and len(set(order))==len(order) and set(order)==set(all_events)
        state='VALID_PUBLISHER_ORDER' if ok else 'INVALID_FULL_EVENT_ORDER'
        valid+=ok;invalid+=not ok;filtered=[e for e in order if e in ids] if ok else None
        pairs=[(a,b) for a in ids for b in ids if a!=b];qrows=[]
        for a,b in pairs:
            q='Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(all_events[a],all_events[b])
            t='Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(all_events[b],all_events[a])
            match=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q)
            verify(match is not None and match.groups()==(all_events[a],all_events[b]),'binding')
            match2=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',t)
            verify('Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(match2[2],match2[1])==q,'double_tau')
            questions.add(q);y=int(filtered.index(a)<filtered.index(b)) if ok else None
            qrows.append({'event_a':a,'event_b':b,'question':q,'tau':t,'label':y,'status':state})
        expected_m={'position':position,'observation':obs,'events':all_events,'media':media,'row_index':index,'sort_digest':digest,'format':row['format'],'publisher_full_order':order,'publisher_selected_order':filtered,'status':state,'questions':qrows,'label_level':'PUBLISHER_ORDER_DERIVED','formal_strict_temporal_scoring':'CONDITIONAL_NOT_CERTIFIED'}
        verify(m==expected_m,'entire_native_manifest_group')
        if ok:
            verify(sum(q['label'] for q in qrows)==3,'native_balance')
            for qi,(a,b) in enumerate(pairs):verify(qrows[qi]['label']+qrows[pairs.index((b,a))]['label']==1,'complements')
        if media.get('size') is not None and media['identity'].get('value'):known+=1;totalbytes+=media['size']
        a,b,cid=ids
        # Explicit six permutations, independent from producer's permutations call.
        permutations=[(a,b,cid),(a,cid,b),(b,a,cid),(b,cid,a),(cid,a,b),(cid,b,a)]
        for pi,p in enumerate(permutations):
            ys=[]
            for qi,(u,v) in enumerate(pairs):
                label=int(p.index(u)<p.index(v));ys.append(label)
                s_expected.append({'group':position,'permutation':pi,'order':list(p),'question_index':qi,'question':qrows[qi]['question'],'label':label})
            verify(sum(ys)==3,'symbolic_balance')
            for edge in ((1,0,2),(0,2,1)):
                target=tuple(p[i] for i in edge);pj=permutations.index(target);flip=0
                for qi,(u,v) in enumerate(pairs):
                    y=ys[qi];z=int(target.index(u)<target.index(v));flip+=y!=z
                    r_expected.append({'group':position,'from':pi,'to':pj,'question_index':qi,'from_label':y,'to_label':z,'relation':'FLIP' if y!=z else 'HOLD'})
                verify(flip==2,'exact_two_flip_four_hold')
    verify(symbolic==s_expected,'entire_symbolic_cells');verify(relations==r_expected,'entire_symbolic_relations')
    values={'rows':len(rows),'collection_path':path,'unique_qa_ids':len(counts),'duplicate_qa_id_excess':len(rows)-len(counts),'duplicate_exact_rows_excess':len(rows)-len({canon(r) for r in rows}),'unique_video_ids':len({r['video_id'] for r in rows}),'format_counts':dict(Cnt(r['format'] for r in rows)),'source_counts':dict(sourcecounts),'eligibility_partition':dict(reasons),'eligible_observations':len(candidates),'eligible_unique_videos':len(unique),'same_video_candidates_removed':len(candidates)-len(unique),'eligible_unique_videos_not_selected':max(0,len(unique)-24),'selected_k':len(chosen),'selected_valid':valid,'selected_invalid':invalid,'selected_unknown':0,'native_questions':6*len(chosen),'native_valid_labels':6*valid,'native_unknown_labels':6*invalid,'unique_native_videos':len({c[3]['video_id'] for c in chosen}),'unique_native_questions_including_tau':len(questions),'symbolic_cells':len(s_expected),'symbolic_relations':len(r_expected),'symbolic_flip':sum(e['relation']=='FLIP' for e in r_expected),'symbolic_hold':sum(e['relation']=='HOLD' for e in r_expected),'media_locators_with_size_identity':known,'selected_published_media_bytes_known':totalbytes,'media_bytes_complete':known==len(chosen),'future_native_feature_calls':len(chosen)+len(questions),'future_36_head_cpu_cells':36*6*len(chosen),'future_media_512mib_size_gate':known==len(chosen) and totalbytes<=512*1024**2}
    for key,value in values.items():verify(summary[key]==value,'aggregate_'+key)
    for filename,digest in summary['artifact_sha256'].items():verify(H.sha256((root/filename).read_bytes()).hexdigest()==digest,'artifact_seal')
    seal=J.loads((root/'formal-code-seal.json').read_bytes())
    verify(H.sha256(P(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==seal['producer_lf_sha256'],'code_unchanged')
    verify(summary['code_lf_sha256']==seal['producer_lf_sha256'],'summary_code')
    verify('does not relicense third-party media' in bs['README.md'].decode(),'rights_caveat')
    verify(summary['controlled_media']=='CONTROLLED_MEDIA_CONSTRUCTION_HOLD','media_hold')
    verify(summary['metadata_network_requests']==summary['model_calls']==summary['training_updates']==0,'no_execution')
    k=len(chosen);verify(len(s_expected)==36*k and len(r_expected)==72*k,'scale')
    # Independently inventory evidence and original bundle declarations without publishing values.
    keycounts=Cnt();stack=[bundle]
    while stack:
        value=stack.pop()
        if isinstance(value,dict):
            keycounts.update(value.keys());stack.extend(value.values())
        elif isinstance(value,list):stack.extend(value)
    observed_keys={key:n for key,n in keycounts.items() if R.search(r'start|end|time|bound|overlap|unique|clock|duration|path|source|uncertain|unresolved|pending',key,R.I)}
    verify(summary['evidence_keys']==observed_keys,'all_evidence_keys')
    verify(summary['publisher_root_metadata']=={key:value for key,value in bundle.items() if key!='items'},'root_declarations_retained')
    expected_status='OFFLINE_FIXED_MULTIQUERY_LABEL_PLAN_READY / USER_SUPPLIED_SOURCE_PROVENANCE / MEDIA_HOLD' if k==24 and valid==k and known==k else 'PARTIAL_OR_NO_MULTIEVENT_ENTRY'
    verify(summary['status']==expected_status,'qualification')
    result={'status':'PASS','checks':checks,'source_logical_bytes':sum(map(len,bs.values())),'seconds':T.monotonic()-start,'producer_imports':0,'native_groups':k,'symbolic_cells_checked':len(symbolic),'symbolic_relations_checked':len(relations)}
    with open(root/'independent-review.json','x',encoding='utf-8') as f:J.dump(result,f,sort_keys=True);f.flush();os.fsync(f.fileno())
    print(canon(result))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('role', choices=['gate', 'observe', 'fixture', 'construct', 'verify'])
    p.add_argument('--source')
    p.add_argument('--root', required=True)
    a = p.parse_args()
    if a.role == 'observe':
        return observe(a.root)
    if a.role == 'construct':
        return construct(a.root)
    if a.role == 'verify':
        return independent_review(a.root)
    if a.role == 'fixture':
        return print(canonical(fixture()))
    start = time.monotonic()
    code = Path(__file__).read_bytes().replace(b'\r\n', b'\n')
    seal = hashlib.sha256(code).hexdigest()
    try:
        data, receipt = input_gate(a.source)
    except Exception as e:
        print(canonical(dict(status='WAITING_USER_METADATA_FILES', reason=str(e),
                             seconds=time.monotonic()-start, gate_code_lf_sha256=seal)))
        return
    root = Path(a.root)
    check(not root.exists(), 'EXISTING_073_ROOT_DO_NOT_RESTART')
    import shutil
    check(shutil.disk_usage(root.parent).free >= 128*1024**2, 'FREE_SPACE')
    root.mkdir()
    for name, b in data.items():
        with open(root/name, 'xb') as f:
            f.write(b)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(root/name, 0o444)
    receipt['gate_code_lf_sha256'] = seal
    write_new(root/'input-gate.json', receipt)
    print(canonical({k: v for k, v in receipt.items() if k not in ('source', 'identities')}))


if __name__ == '__main__':
    main()
