"""052: stdlib-only, sealed nongold classification before derived-score analysis.

The independent review is emitted as a separate stdlib program. No model,
processor, array or image entry point is provided. All dataset text is data.
"""
import ctypes as C
import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import threading
import time

MIB=1024**2
FAMILIES=('summarization','perception','reasoning','navigation')
CLASSES=('TASK_UNKNOWN','AUXILIARY_IMAGE_REQUIRED','PREDICTIVE_PREFIX_REQUIRED','OUTSIDE_049_TIME_SCOPE','TEXT_SCOPE_CONFLICT','NO_LISTED_SPECIAL_BRANCH')
IMAGES={'navigation/room_to_room_image','navigation/object_retrieval_image','reasoning/spatial/layout'}
TIME_WORDS=('temporal','ordering','duration','timestamp','timecode','chronolog')
ARMS=('SO','F48','P0','P1','P2','P3','V4')
COUNTS=('SO_correct','F48_correct','V4_correct','F48_correction','F48_harm','F48_both_correct','F48_both_wrong','V4_correction','V4_harm','V4_both_correct','V4_both_wrong','all_five_wrong','full_only','split_only','split_recovered','vote_missed')
HELPERS={'selection_channel_049.py':'407cbbd77daa2d4d2d9d6c5fad8fec8b83b49991','hourvideo_mcq_schema_051.py':'1e1e306de3d76c476701ba68a5a6f638d5f631cc','auditable_runner_040.py':'3e56faf30afea1bed850c085bceb2afcc4fb257c'}


def need(ok,reason):
    if not ok:raise ValueError(reason)


def sha(b):return hashlib.sha256(b).hexdigest()
def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def read(p):return json.loads(Path(p).read_bytes())


def write(p,x,replace=False):
    p=Path(p);b=pack(x);need(len(b)<=8*MIB,'OUTPUT_FILE_CAP');tmp=p.with_name(p.name+'.writing') if replace else p
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    if replace:os.replace(tmp,p)


def regular(p,cap):
    p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=cap,'INPUT_TYPE_SIZE')
    for item in [p,*p.parents]:
        a=item.lstat();need(not stat.S_ISLNK(a.st_mode) and not getattr(a,'st_file_attributes',0)&1024,'INPUT_REPARSE')
    return s


def load_helper(repo,name):
    p=Path(repo)/'prototypes'/name;b=p.read_bytes();normalized=b.replace(b'\r\n',b'\n')
    need(hashlib.sha1(b'blob '+str(len(normalized)).encode()+b'\0'+normalized).hexdigest()==HELPERS[name],'HELPER_NORMALIZED_GIT_IDENTITY')
    spec=importlib.util.spec_from_file_location('helper052_'+p.stem,p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module,dict(actual_byte_sha256=sha(b),canonical_LF_git_blob=HELPERS[name],newline_normalization='CRLF_TO_LF_FOR_GIT_BLOB_ONLY')


class Meter:
    def __init__(self,root,role):self.root=Path(root);self.role=role;self.rows=[]
    def get(self,path,bucket='old_metadata'):
        path=Path(path);limit=4*MIB if bucket=='original' else 2*MIB if bucket=='old_metadata' else 8*MIB
        st=regular(path,limit);budget=read(self.root/'read-budget.json')
        if bucket=='original':
            need(budget['original_opens']==0,'ORIGINAL_REOPEN_FORBIDDEN');budget['original_opens']=1
        elif bucket=='old_metadata':need(budget['old_metadata_returned']+st.st_size<=8*MIB,'METADATA_TOTAL_CAP')
        write(self.root/'read-budget.json',budget,True)
        with path.open('rb') as f:
            b=f.read(st.st_size);after=os.fstat(f.fileno())
        if bucket=='original':budget['original_returned']+=len(b)
        elif bucket=='old_metadata':
            budget['old_metadata_returned']+=len(b);budget['old_opens'].append(dict(name=path.name,bytes=len(b),phase=self.role))
        write(self.root/'read-budget.json',budget,True)
        self.rows.append(dict(name=path.name,bucket=bucket,returned=len(b),byte_sha256=sha(b)))
        need(len(b)==st.st_size and (after.st_ino,after.st_size,after.st_mtime_ns)==(st.st_ino,st.st_size,st.st_mtime_ns),'FILE_CHANGED_OR_SHORT_READ')
        return b
    def json(self,path,bucket='old_metadata'):return json.loads(self.get(path,bucket))
    def close(self):write(self.root/(self.role+'-reads.json'),dict(reads=self.rows,returned=sum(x['returned'] for x in self.rows)))


def valid_task(task):
    return type(task) is str and 0<len(task)<=160 and re.fullmatch(r'[a-z0-9_]+(/[a-z0-9_]+)*',task) is not None and task.split('/')[0] in FAMILIES


def classify(task,qualification):
    valid=valid_task(task);image=valid and task in IMAGES;predictive=valid and task=='reasoning/predictive';outside=valid and any(w in task for w in TIME_WORDS)
    kind='TASK_UNKNOWN' if not valid else 'AUXILIARY_IMAGE_REQUIRED' if image else 'PREDICTIVE_PREFIX_REQUIRED' if predictive else 'OUTSIDE_049_TIME_SCOPE' if outside else 'TEXT_SCOPE_CONFLICT' if qualification!='ELIGIBLE_NONGOLD' else 'NO_LISTED_SPECIAL_BRANCH'
    return dict(protocol_class=kind,family=task.split('/')[0] if valid else 'F_UNKNOWN',image_required=image,predictive_prefix_required=predictive,time_scope_flag=outside,qualification=qualification)


def validate_cells(rows):
    cells={}
    for row in rows:
        i,c=row['question'],row['condition']
        need(type(i) is int and 0<=i<24 and c in ARMS and (i,c) not in cells,'DUPLICATE_OR_UNEXPECTED_JOIN')
        v=row['correct'];s=row['state'];need(type(v) is int and v in (0,1) and s==('VALID_CORRECT' if v else 'VALID_WRONG'),'DERIVED_STATE_OR_VALUE')
        cells[i,c]=v
    need(set(cells)=={(i,c) for i in range(24) for c in ARMS},'MISSING_JOIN')
    return cells


def classify_stage(root):
    root=Path(root);cfg=read(root/'classification-config.json');meter=Meter(root,'classify');api,api_id=load_helper(cfg['repo'],'selection_channel_049.py');schema,schema_id=load_helper(cfg['repo'],'hourvideo_mcq_schema_051.py')
    try:
        data={name:meter.json(path) for name,path in cfg['inputs'].items()};questions=data['nongold'];selection=data['selection'];mapping=data['mapping'];binding=data['binding'];queue=data['queue'];phase=data['phase'];done=data['done'];review=data['review']
        need(len(questions)==24 and len(selection['aliases'])==4 and len(set(selection['aliases']))==4,'COHORT')
        need([q['id'] for q in questions]==['Q'+str(i+1).zfill(2) for i in range(24)],'QUESTION_ORDER')
        need(all(type(q['ordinal']) is int and q['source'] in selection['aliases'] for q in questions) and all(sum(q['source']==s for q in questions)==6 for s in selection['aliases']),'SOURCE_ORDINAL')
        wanted={k:set(v) for k,v in mapping['wanted'].items()};reconstructed={}
        for q in questions:reconstructed.setdefault(mapping['uids'][q['source']],set()).add(q['ordinal'])
        need(reconstructed==wanted and sum(map(len,wanted.values()))==24,'SOURCE_MAP_JOIN')
        nongold_read=next(row for row in meter.rows if row['name']=='nongold.json');nongold_bytes=nongold_read['returned'];nongold_sha=nongold_read['byte_sha256']
        need(nongold_sha==queue['nongold_sha']==binding['nongold_sha'],'NONGOLD_BYTE_BINDING')
        need(binding['original_file_hash']==cfg['annotation_sha256'] and binding['status']=='PASS','ORIGINAL_BINDING')
        need(phase['active']==0 and phase['exitcode']==0 and not phase['killed'] and done['new_attempts']==done['new_returns']==120 and review['status']=='PASS','UNCLOSED_MODEL')
        need(len(queue['logical'])==len(queue['info'])==120,'QUEUE_DENOMINATOR')
        need(all(queue['logical'][5*i+j]['question']==i and queue['logical'][5*i+j]['source']==questions[i]['source'] for i in range(24) for j in range(5)),'QUEUE_SOURCE_ORDER')
        raw=meter.get(cfg['annotation'],'original');need(sha(raw)==cfg['annotation_sha256'],'ORIGINAL_SHA')
        projected,gold_decoded=api.projected_json(raw,wanted,{'question','mcq_test','task'});need(gold_decoded==0,'PROTECTED_VALUE_DECODE');del raw
        rows=[];modes={};normalizations=0
        for i,q in enumerate(questions):
            row=projected[mapping['uids'][q['source']]][q['ordinal']];bound=schema.bind_original_nongold(row,q['question'],q['options']);task=row.get('task');qualification=api.qualify(q)
            rows.append(dict(question_index=i,id=q['id'],source=q['source'],ordinal=q['ordinal'],task=task,**classify(task,qualification)))
            modes[bound['parse_mode']]=modes.get(bound['parse_mode'],0)+1;normalizations+=bound['frozen_option_boundary_normalization_count']
        tasks=sorted({row['task'] for row in rows if valid_task(row['task'])});aliases={task:'T'+str(i+1).zfill(2) for i,task in enumerate(tasks)}
        for row in rows:row['task_alias']=aliases[row['task']] if valid_task(row['task']) else 'T_UNKNOWN'
        write(root/'nongold-projection-private.json',dict(projection=projected))
        write(root/'classification-private.json',dict(rows=rows,task_aliases=aliases,source_aliases={s:'S'+str(i+1).zfill(2) for i,s in enumerate(selection['aliases'])}))
        field_sets=[set(x['fields']) for x in queue['info']];video_only=all(x=={'input_ids','attention_mask','pixel_values_videos','video_grid_thw'} for x in field_sets)
        write(root/'classification-seal.json',dict(status='PASS',N=24,at=time.time(),classification_sha=sha((root/'classification-private.json').read_bytes()),projection_sha=sha((root/'nongold-projection-private.json').read_bytes()),code_sha=sha(Path(__file__).read_bytes()),helpers={'projector_qualify':api_id,'display_binder':schema_id},nongold_sha=nongold_sha,nongold_bytes=nongold_bytes,original_snapshot_match=True,gold_values_decoded=0,original_opens=1,display_modes=modes,frozen_option_normalizations=normalizations,all_120_inputs_video_only_no_image_fields=video_only,score_entry_in_classification_config=False))
        print('CLASSIFICATION_SEALED',len(rows),'gold_decoded',gold_decoded)
    finally:meter.close()


def contributions(cells,i):
    so,f,v=(cells[i,c] for c in ('SO','F48','V4'));parts=[cells[i,'P'+str(j)] for j in range(4)];any_p=any(parts)
    return dict(SO_correct=so,F48_correct=f,V4_correct=v,F48_correction=int(f and not so),F48_harm=int(so and not f),F48_both_correct=f*so,F48_both_wrong=int(not(f or so)),V4_correction=int(v and not so),V4_harm=int(so and not v),V4_both_correct=v*so,V4_both_wrong=int(not(v or so)),all_five_wrong=int(not(f or any_p)),full_only=int(f and not any_p),split_only=int(not f and any_p),split_recovered=int(not f and any_p and v),vote_missed=int(any_p and not v))


def aggregate(rows,cells):
    sources=['S01','S02','S03','S04'];groups=[('overall','ALL')]+[('family',f) for f in FAMILIES+('F_UNKNOWN',)]+[('task',t) for t in sorted({x['task_alias'] for x in rows}|{'T_UNKNOWN'})]+[('protocol',c) for c in CLASSES];output=[]
    for kind,group in groups:
        ids=[i for i,x in enumerate(rows) if kind=='overall' or x[{'family':'family','task':'task_alias','protocol':'protocol_class'}[kind]]==group]
        for source in ['ALL']+sources:
            selected=[i for i in ids if source=='ALL' or rows[i]['source_alias']==source];ns={s:sum(rows[i]['source_alias']==s for i in selected) for s in sources}
            output.append(dict(group_kind=kind,group_id=group,source=source,n=len(selected),source_count=sum(v>0 for v in ns.values()),**{'n_'+s:ns[s] for s in sources},**{k:sum(contributions(cells,i)[k] for i in selected) for k in COUNTS}))
    return output


def analyze_stage(root):
    root=Path(root);cfg=read(root/'analysis-config.json');meter=Meter(root,'analyze')
    try:
        phase=read(root/'classify-phase.json');seal=read(root/'classification-seal.json');need(phase['active']==0 and phase['exitcode']==0 and not phase['killed'],'CLASSIFICATION_NOT_EXITED')
        b=meter.get(root/'classification-private.json','new');need(sha(b)==seal['classification_sha'] and sha(Path(__file__).read_bytes())==seal['code_sha'],'CLASSIFICATION_SEAL_CHANGED');classified=json.loads(b);rows=classified['rows'];source_aliases=classified['source_aliases']
        for row in rows:row['source_alias']=source_aliases[row['source']]
        # Only this role receives the score path, after classification exits.
        text=meter.get(cfg['score_path']).decode('utf-8');view=Selective(text);chosen=[];mismatch=None
        for key,a,b in view.members(0):
            if key=='slots':
                for x,y in view.elements(a):
                    attrs=view.fields(x,{'question','condition'})
                    if attrs['condition'] in ARMS:chosen.append(view.fields(x,{'question','condition','correct','state'}))
            elif key=='result':mismatch=view.fields(a,{'baseline_mismatch_count'})['baseline_mismatch_count']
        need(mismatch==0,'BASELINE_MISMATCH');cells=validate_cells(chosen);public=json.loads(Path(cfg['public_summary']).read_bytes())
        totals={c:sum(cells[i,c] for i in range(24)) for c in ARMS};need(totals=={'SO':9,'F48':9,'P0':8,'P1':8,'P2':8,'P3':8,'V4':10},'OVERALL_RECOUNT')
        for s in source_aliases.values():
            ids=[i for i,x in enumerate(rows) if x['source_alias']==s];need(len(ids)==6,'SOURCE_DENOMINATOR')
            for c in ARMS:need(sum(cells[i,c] for i in ids)==public['per_source'][s]['arms'][c]['correct'],'PUBLIC_SOURCE_RECOUNT')
        table=aggregate(rows,cells);overall=next(x for x in table if x['group_kind']=='overall' and x['source']=='ALL');need([overall[k] for k in ('all_five_wrong','full_only','split_only','split_recovered','vote_missed')]==[12,1,3,3,1],'DIAGNOSTIC_RECOUNT')
        joined=[dict(question_index=i,source_alias=rows[i]['source_alias'],correct={c:cells[i,c] for c in ARMS}) for i in range(24)]
        write(root/'derived-join-private.json',joined);write(root/'group-table.json',table)
        with (root/'protocol-and-error-profile.csv').open('x',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
        distribution={c:sum(x['protocol_class']==c for x in rows) for c in CLASSES};conflict_ids=[i for i,x in enumerate(rows) if x['protocol_class'] not in ('TASK_UNKNOWN','NO_LISTED_SPECIAL_BRANCH')]
        state='TASK_PROTOCOL_REVIEW_REQUIRED' if conflict_ids else 'TASK_METADATA_INCOMPLETE' if distribution['TASK_UNKNOWN'] else 'NO_LISTED_PROTOCOL_GAP_FOUND'
        write(root/'analysis-receipt.json',dict(status=state,N=24,totals=totals,protocol_counts=distribution,known_conflicts=len(conflict_ids),known_conflict_all_five_wrong=sum(contributions(cells,i)['all_five_wrong'] for i in conflict_ids),unknown_task_all_five_wrong=sum(contributions(cells,i)['all_five_wrong'] for i,x in enumerate(rows) if x['protocol_class']=='TASK_UNKNOWN'),baseline_mismatch_count=mismatch,cells_selected=len(chosen),classification_sha=seal['classification_sha'],classification_sealed_before_score_open=True,derived_sha=sha((root/'derived-join-private.json').read_bytes()),table_sha=sha((root/'group-table.json').read_bytes()),score_file_physical_opens=1,original_opens=0))
        print('DERIVED_RECOUNT_PASS',state,'selected_cells',len(chosen))
    finally:meter.close()


class Selective:
    """Value skipping without deserializing unselected score fields."""
    def __init__(self,s):self.s=s;self.n=len(s)
    def ws(self,p):
        while p<self.n and self.s[p] in ' \r\n\t':p+=1
        return p
    def string(self,p):
        need(self.s[p]=='"','JSON_STRING');p+=1
        while p<self.n:
            if self.s[p]=='\\':p+=2
            elif self.s[p]=='"':return p+1
            else:p+=1
        raise ValueError('JSON_EOF')
    def skip(self,p):
        p=self.ws(p);s=self.s
        if s[p]=='"':return self.string(p)
        if s[p] in '{[':
            opening=s[p];closing='}' if opening=='{' else ']';p=self.ws(p+1)
            if s[p]==closing:return p+1
            while True:
                if opening=='{':p=self.ws(self.string(p));need(s[p]==':','JSON_COLON');p=self.ws(p+1)
                p=self.ws(self.skip(p))
                if s[p]==closing:return p+1
                need(s[p]==',','JSON_COMMA');p=self.ws(p+1)
        end=p
        while end<self.n and s[end] not in ',]} \t\r\n':end+=1
        need(end>p,'JSON_ATOM');return end
    def members(self,p):
        p=self.ws(p);need(self.s[p]=='{','JSON_OBJECT');p=self.ws(p+1);seen=set()
        if self.s[p]=='}':return
        while True:
            e=self.string(p);key=json.loads(self.s[p:e]);need(key not in seen,'JSON_DUPLICATE');seen.add(key);p=self.ws(e);need(self.s[p]==':','JSON_COLON');a=self.ws(p+1);b=self.skip(a);yield key,a,b;p=self.ws(b)
            if self.s[p]=='}':return
            need(self.s[p]==',','JSON_COMMA');p=self.ws(p+1)
    def elements(self,p):
        p=self.ws(p);need(self.s[p]=='[','JSON_ARRAY');p=self.ws(p+1)
        if self.s[p]==']':return
        while True:
            e=self.skip(p);yield p,e;p=self.ws(e)
            if self.s[p]==']':return
            need(self.s[p]==',','JSON_COMMA');p=self.ws(p+1)
    def fields(self,p,names):return {k:json.loads(self.s[a:b]) for k,a,b in self.members(p) if k in names}


def suite(root):
    cfg=read(Path(root)/'coordinator-config.json');api,_=load_helper(cfg['repo'],'selection_channel_049.py');binder,_=load_helper(cfg['repo'],'hourvideo_mcq_schema_051.py');count=0
    def check(ok):
        nonlocal count
        count+=1;need(ok,'FIXTURE_ASSERTION')
    def refuse(fn):
        try:fn()
        except ValueError:check(True)
        else:check(False)
    for task,want in [(None,'TASK_UNKNOWN'),('Reasoning/predictive','TASK_UNKNOWN'),('other/x','TASK_UNKNOWN'),('reasoning//x','TASK_UNKNOWN'),('navigation/room_to_room_image','AUXILIARY_IMAGE_REQUIRED'),('navigation/object_retrieval_image','AUXILIARY_IMAGE_REQUIRED'),('reasoning/spatial/layout','AUXILIARY_IMAGE_REQUIRED'),('reasoning/predictive','PREDICTIVE_PREFIX_REQUIRED'),('reasoning/temporal','OUTSIDE_049_TIME_SCOPE'),('reasoning/chronological_events','OUTSIDE_049_TIME_SCOPE'),('perception/object','NO_LISTED_SPECIAL_BRANCH')]:check(classify(task,'ELIGIBLE_NONGOLD')['protocol_class']==want)
    check(classify('perception/object','TIME_DEPENDENT')['protocol_class']=='TEXT_SCOPE_CONFLICT');check(classify('reasoning/predictive','TIME_DEPENDENT')['protocol_class']=='PREDICTIVE_PREFIX_REQUIRED')
    raw=b'{"owned":{"benchmark_dataset":[{"question":"Owned object?","mcq_test":"A. red\\nB. blue\\nC. green\\nD. gray\\nE. yellow","task":"perception/object","correct_answer_label":NaN,"canary":{"forbidden":"never retained"}}]}}'
    projected,gold=api.projected_json(raw,{'owned':{0}},{'question','mcq_test','task'});check(gold==0 and set(projected['owned'][0])=={'question','mcq_test','task'})
    check(binder.bind_original_nongold(projected['owned'][0],'Owned object?',['red','blue','green','gray','yellow'])['gold_values_accessed']==0)
    cells=[dict(question=i,condition=c,correct=0,state='VALID_WRONG') for i in range(24) for c in ARMS];check(len(validate_cells(cells))==168);refuse(lambda:validate_cells(cells[:-1]));refuse(lambda:validate_cells(cells+[cells[0]]));refuse(lambda:validate_cells([dict(cells[0],correct=True)]+cells[1:]))
    rows=[dict(source_alias='S'+str(i//6+1).zfill(2),family='perception',task_alias='T01',protocol_class='NO_LISTED_SPECIAL_BRANCH') for i in range(24)];table=aggregate(rows,validate_cells(cells));check(next(x for x in table if x['group_kind']=='overall' and x['source']=='ALL')['n']==24)
    zero=next(x for x in table if x['group_kind']=='family' and x['group_id']=='navigation' and x['source']=='ALL');check(zero['n']==0 and all(zero[k]==0 for k in COUNTS))
    view=Selective('{"slots":[{"question":0,"condition":"SO","correct":1,"state":"VALID_CORRECT","unused":"NEVER_RETAIN"}]}');key,a,b=next(view.members(0));x,y=next(view.elements(a));check(view.fields(x,{'correct','state'})=={'correct':1,'state':'VALID_CORRECT'})
    write(Path(root)/'self-tests.json',dict(status='PASS',assertions=count,owned_only=True));print('NECESSARY_FIXTURES_PASS',count)


def reference_stage(root):
    import urllib.request
    root=Path(root);rows=[]
    names={'gpt4_qa.py':'66751c01ba5f3e01581bd9376b33cdbc0705daf6','gpt4_utils.py':'a49991caf2f8bb300e9f8d9b6ae3ea40f1becd3c','gemini_utils.py':'68d15dee4bb7902daf93b7353f8939224f164f16'}
    for name,expected in names.items():
        try:
            url='https://raw.githubusercontent.com/keshik6/HourVideo/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/'+name
            with urllib.request.urlopen(url,timeout=8) as f:b=f.read(128*1024)
            need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected,'REFERENCE_GIT_BLOB');(root/('public-reference-'+name)).write_bytes(b);rows.append(dict(name=name,status='VERIFIED',returned=len(b),blob=expected))
        except Exception as e:rows.append(dict(name=name,status='UNKNOWN',exception=type(e).__name__))
    write(root/'public-reference-receipt.json',dict(rows=rows,public_text_reference_requests=3,experiment_network_requests=0));print(json.dumps(rows))


def supervise(root,role):
    root=Path(root);cfg=read(root/'coordinator-config.json');need(time.time()<cfg['deadline_epoch'],'PARENT_DEADLINE');platform,_=load_helper(cfg['repo'],'auditable_runner_040.py');caps={'suite':30,'reference':40,'classify':90,'analyze':60,'verify':60}
    used=sum(read(p)['wall'] for p in root.glob('*-phase.json'));cap=min(caps[role],300-used,cfg['deadline_epoch']-time.time());need(cap>5 and not (root/(role+'-phase.json')).exists(),'RESTART_OR_CPU_BUDGET')
    job=platform.Job(memory=1024**3,active_limit=4);limit=platform.Extended();need(job.api.QueryInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit),None),'JOB_QUERY');limit.basic.flags|=0x10;limit.basic.affinity=1;need(job.api.SetInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit)),'JOB_AFFINITY')
    script=root/'independent-review-052.py' if role=='verify' else Path(__file__);args=[cfg['python'],'-I','-S','-B',str(script)] + ([str(root)] if role=='verify' else [role,str(root)])
    start=time.monotonic();child=None
    try:
        child=platform.Process(args,root/(role+'.log'),job)
        while job.active():
            if time.monotonic()-start>cap-4:job.kill();break
            time.sleep(.005)
        need(job.empty(start+cap-1),'OWN_JOB_EXIT_UNKNOWN');receipt=dict(role=role,wall=time.monotonic()-start,exitcode=child.poll(),**job.snapshot());write(root/(role+'-phase.json'),receipt);print(json.dumps(receipt));print((root/(role+'.log')).read_text(encoding='utf-8',errors='replace')[-1200:].encode('ascii','backslashreplace').decode())
    finally:
        if child:child.close()
        job.close()


if __name__=='__main__':
    role,path,*extra=sys.argv[1:];root=Path(path)
    if role=='launch':supervise(root,extra[0])
    else:
        {'suite':suite,'reference':reference_stage,'classify':classify_stage,'analyze':analyze_stage}[role](root)
        need(not any(x.split('.')[0] in {'torch','transformers','numpy','PIL','cv2'} for x in sys.modules),'FORBIDDEN_RUNTIME_IMPORT')
        need(threading.active_count()==1,'PYTHON_THREAD_COUNT')
