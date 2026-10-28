"""054 sealed finite-view analysis. Stdlib only; old scalar tables, no model."""
import ctypes as C
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
import threading
import time

MIB=1024**2
METHODS=('F','M','A','I','C','R')
CONDITIONS=METHODS+('E15','B0','O15','O1','O2','O3')
LETTERS='ABCDE'
OLD_CODE_SHA='d83f2d1f0e64039f16d973b6dbc2d50943bded8b5a31b40577102f055f51d6f5'


def need(ok,reason):
    if not ok:raise ValueError(reason)


def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())


def write(p,x,replace=False):
    p=Path(p);b=pack(x);need(len(b)<=8*MIB,'OUTPUT_FILE_CAP');tmp=p.with_name(p.name+'.writing') if replace else p
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    if replace:os.replace(tmp,p)


def regular(p,cap):
    p=Path(p);s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_size<=cap,'FILE_TYPE_SIZE')
    for q in [p,*p.parents]:
        a=q.lstat();need(not stat.S_ISLNK(a.st_mode) and not getattr(a,'st_file_attributes',0)&1024,'FILE_REPARSE')
    return s


def old_read(root,path,role):
    root=Path(root);path=Path(path);s=regular(path,2*MIB);budget=read(root/'read-budget.json');need(budget['metadata_returned']+s.st_size<=8*MIB,'OLD_METADATA_CAP')
    with path.open('rb') as f:b=f.read(s.st_size);after=os.fstat(f.fileno())
    budget['metadata_returned']+=len(b);budget['metadata_opens'].append(dict(name=path.name,bytes=len(b),role=role));write(root/'read-budget.json',budget,True)
    need(len(b)==s.st_size and (s.st_ino,s.st_size,s.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns),'OLD_FILE_CHANGED');return b


def helper(repo,name,blob):
    path=Path(repo)/'prototypes'/name;b=path.read_bytes();lf=b.replace(b'\r\n',b'\n');need(hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest()==blob,'HELPER_GIT_IDENTITY')
    spec=importlib.util.spec_from_file_location('helper054_'+path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    no_runtime();return m


def no_runtime():
    need(not any(x.split('.')[0] in {'torch','transformers','numpy','PIL','cv2'} for x in sys.modules),'FORBIDDEN_RUNTIME_IMPORT');need(threading.active_count()==1,'THREAD_COUNT')


def finite(v):need(isinstance(v,(list,tuple)) and len(v)==5 and all(type(x) in (int,float) and math.isfinite(x) for x in v),'FINITE_FIVE_SCORES')
def top(v):finite(v);return max(range(5),key=lambda a:(v[a],-a))
def margin(v,a):return v[a]-max(v[b] for b in range(5) if b!=a)
def bits(mask):return bin(mask).count('1')


def e15(states):
    need(set(states)==set(range(16)),'SIXTEEN_STATES');candidates=[]
    for mask in range(1,16):
        a=top(states[mask]);candidates.append(dict(mask=mask,a=a,margin=margin(states[mask],a)))
    return max(candidates,key=lambda x:(x['margin'],bits(x['mask']),-x['mask'],-x['a']))


def validate_join(rows,methods=METHODS):
    found={}
    for x in rows:
        i,m=x['question'],x['method'];need(type(i) is int and 0<=i<24 and m in methods and (i,m) not in found,'DUPLICATE_OR_INVALID_JOIN');found[i,m]=x
    need(set(found)=={(i,m) for i in range(24) for m in methods},'MISSING_JOIN');return found


def nongold(root):
    root=Path(root);cfg=read(root/'nongold-config.json');raw={n:old_read(root,p,'nongold') for n,p in cfg['inputs'].items()};d={n:json.loads(b) for n,b in raw.items()};q=d['nongold.json'];aliases=d['source-selection.json']['aliases'];initial=d['initial-input-seal.json'];scores=d['scores-private.json'];selection=d['selection-seal.json'];seal=d['output-seal.json'];done=d['inference-complete.json'];review=d['independent-review.json']
    need(sha((Path(cfg['repo'])/'prototypes/block_interaction_053.py').read_bytes())==OLD_CODE_SHA==initial['code_sha']==selection['code_sha']==seal['code_sha'],'053_ACTUAL_LF_CODE_IDENTITY')
    need(len(q)==24 and [x['id'] for x in q]==['Q'+str(i+1).zfill(2) for i in range(24)] and len(aliases)==len(set(aliases))==4 and all(sum(x['source']==a for x in q)==6 for a in aliases),'FIXED_COHORT')
    need(sha(raw['nongold.json'])==cfg['cohort_byte_sha']==initial['nongold_sha']==seal['nongold_sha'],'NONGOLD_SHA')
    need(sha(raw['scores-private.json'])==seal['scores_sha'] and sha(raw['initial-input-seal.json'])==selection['initial_queue_sha'],'SCORE_SELECTION_SHA')
    for p in ('infer-phase.json','verify-phase.json'):
        x=d[p];need(x['active']==0 and x['exitcode']==0 and not x['killed'],'OLD_PROCESS_NOT_CLOSED')
    need(done['attempts']==done['returns']==done['forward_steps']==437 and review['status']=='PASS' and review['outputs_rebuilt']==144 and seal['new_returns']==437 and seal['logical_outputs']==144,'OLD_COMPLETE_COUNTS')
    public=read(Path(cfg['repo'])/'docs/codex-artifacts/VLM-BLOCK-INTERACTION-053/execution-summary.json');need(public['actual_model']['loads']==1 and all(x['active']==0 and x['exitcode']==0 and not x['killed'] for x in public['resource']['phases']),'OLD_MODEL_AND_CPU_RECEIPTS')
    need(len(scores)==437 and len(initial['logical'])==len(initial['unique'])==384 and len(set(initial['unique']))==384,'INITIAL_TABLE_COUNTS')
    table=[];seen=set();identities=set()
    for x in initial['logical']:
        i,mask,identity=x['question'],x['mask'],x['identity'];need(type(i) is int and 0<=i<24 and type(mask) is int and 0<=mask<=15 and x['fill']==128 and (i,mask) not in seen and identity not in identities,'INITIAL_STATE_JOIN');seen.add((i,mask));identities.add(identity)
        record=scores[identity];need(record['state']=='RETURNED' and record['forward_steps']==1,'CLOSED_ONE_FORWARD');finite(record['scores']);a=top(record['scores']);table.append(dict(question=i,mask=mask,identity=identity,scores=record['scores'],a=a,margin=margin(record['scores'],a)))
    need(seen=={(i,m) for i in range(24) for m in range(16)} and identities==set(initial['unique']),'INITIAL_COMPLETE_UNIQUE')
    need(len(selection['rows'])==24 and all(x['question']==i for i,x in enumerate(selection['rows'])),'SELECTION_INDEX')
    choices=[]
    for i in range(24):
        states={x['mask']:x['scores'] for x in table if x['question']==i};chosen=e15(states);old={}
        for method in ('I','A'):
            s=selection['rows'][i]['methods'][method];need(s['state']=='VALID' and type(s['a']) is int and 0<=s['a']<5 and type(s['mask']) is int and 1<=s['mask']<=15,'FROZEN_IA_SELECTION')
            observed=top(states[s['mask']]);old[method]=dict(a=s['a'],mask=s['mask'],observed_top=observed,top_match=s['a']==observed,original_observed_masks=s['observed_masks'])
        choices.append(dict(question=i,E15=chosen,IA=old))
    write(root/'nongold.json',q);write(root/'source-selection.json',dict(aliases=aliases));write(root/'initial-states-private.json',table);write(root/'nongold-choices-private.json',choices)
    write(root/'nongold-seal.json',dict(status='PASS',N=24,states=384,nonempty_states=360,excluded_selective_zero_states=len(scores)-384,code_sha=sha(Path(__file__).read_bytes()),state_sha=sha((root/'initial-states-private.json').read_bytes()),choice_sha=sha((root/'nongold-choices-private.json').read_bytes()),nongold_sha=sha((root/'nongold.json').read_bytes()),old_output_sha=seal['outputs_sha'],old_output_seal_byte_sha=sha(raw['output-seal.json']),old_output_seal_code=seal['code_sha'],scope_caveat=d['binding-receipt.json']['scope_caveat_count'],at=time.time(),no_original_or_old_correct_path_in_nongold_configuration=True,analysis_plan={'E15':'EXACT_MARGIN_CARDINALITY_MASK_ALPHABETIC_NO_MASK0','O15':'GOLD_FINITE_ORACLE_NONEMPTY_ONLY','quantiles':'LINEAR_TYPE7','H_min':4,'H_positive_sources_min':3,'missed_min':2}))
    print('NONGOLD_CHOICES_SEALED_24_INITIAL_STATES_384')


def question_metrics(states,label,choice):
    correct={m:int(top(states[m])==label) for m in range(16)};successful=[m for m in range(1,16) if correct[m]];f=correct[15];e=int(choice['a']==label);o=int(bool(successful));minimum=min(map(bits,successful)) if successful else 'NONE'
    return dict(F=f,E15=e,B0=correct[0],O15=o,**{'O'+str(k):int(any(correct[m] for m in range(1,16) if bits(m)==k)) for k in (1,2,3)},H=int(not f and o),recovered=int(not f and e),harm=int(f and not e),missed=int(not f and o and not e),K=minimum)


def decision(H,positive_sources,missed):
    return 'FINITE_VIEW_HEADROOM_TOO_SMALL' if H<4 or positive_sources<3 else 'RANKING_GAP_OBSERVED' if missed>=2 else 'SIMPLE_CONFIDENCE_USES_MOST_HEADROOM'


def quantile(values,p):
    xs=sorted(values);index=(len(xs)-1)*p;lo=int(math.floor(index));hi=int(math.ceil(index));return xs[lo]+(xs[hi]-xs[lo])*(index-lo)


def analyze(root):
    root=Path(root);cfg=read(root/'scoring-config.json');phase=read(root/'nongold-phase.json');seal=read(root/'nongold-seal.json');need(phase['active']==0 and phase['exitcode']==0 and not phase['killed'],'NONGOLD_NOT_EXITED')
    need(seal['code_sha']==sha(Path(__file__).read_bytes()) and seal['choice_sha']==sha((root/'nongold-choices-private.json').read_bytes()) and seal['state_sha']==sha((root/'initial-states-private.json').read_bytes()) and seal['nongold_sha']==sha((root/'nongold.json').read_bytes()),'NONGOLD_SEALS_CHANGED')
    oldraw={n:old_read(root,p,'scoring') for n,p in cfg['inputs'].items()};old={n:json.loads(b) for n,b in oldraw.items()};need(sha(oldraw['outputs-private.json'])==seal['old_output_sha'],'OLD_OUTPUT_SHA');outputs=validate_join(old['outputs-private.json']);derived=validate_join(old['scored-derived-private.json']);q=read(root/'nongold.json');mapping=read(root/'scoring-map-private.json');table=read(root/'initial-states-private.json');choices=read(root/'nongold-choices-private.json')
    wanted={}
    for x in q:wanted.setdefault(mapping['uids'][x['source']],set()).add(x['ordinal'])
    need(wanted=={k:set(v) for k,v in mapping['wanted'].items()} and sum(map(len,wanted.values()))==24,'SCORING_ORDINAL_UID_JOIN')
    for key,o in outputs.items():need(o['state']=='VALID' and type(o['prediction']) is str and o['prediction'] in tuple(LETTERS) and o['source']==q[key[0]]['source'],'OLD_VALID_OUTPUT')
    need(old['scoring-receipt.json']['all_known'] and old['scoring-receipt.json']['cells']==144 and old['scoring-receipt.json']['gold_values_decoded']==24 and old['scoring-receipt.json']['output_seal_sha']==seal['old_output_seal_byte_sha'],'OLD_SCORING_CLOSURE')
    api=helper(cfg['repo'],'selection_channel_049.py','407cbbd77daa2d4d2d9d6c5fad8fec8b83b49991');binder=helper(cfg['repo'],'hourvideo_mcq_schema_051.py','1e1e306de3d76c476701ba68a5a6f638d5f631cc')
    budget=read(root/'read-budget.json');need(budget['original_opens']==0,'ORIGINAL_REOPEN_FORBIDDEN');s=regular(cfg['annotation'],4*MIB);budget['original_opens']=1;write(root/'read-budget.json',budget,True)
    with open(cfg['annotation'],'rb') as f:raw=f.read(s.st_size);after=os.fstat(f.fileno())
    budget['original_returned']=len(raw);write(root/'read-budget.json',budget,True);need(len(raw)==s.st_size and (after.st_ino,after.st_size,after.st_mtime_ns)==(s.st_ino,s.st_size,s.st_mtime_ns) and sha(raw)==cfg['annotation_sha256'],'ORIGINAL_SNAPSHOT')
    original,decoded=api.projected_json(raw,wanted,{'question','mcq_test','correct_answer_label'});need(decoded==24,'EXACT24_LABEL_VALUES');del raw
    labels=[];old_cells=[];metrics=[]
    for i,x in enumerate(q):
        row=original[mapping['uids'][x['source']]][x['ordinal']];binder.bind_original_nongold(row,x['question'],x['options']);label=row['correct_answer_label'];need(type(label) is str and label.strip().upper() in tuple(LETTERS),'ORIGINAL_LABEL_FORMAT');label=LETTERS.index(label.strip().upper());labels.append(label)
        states={r['mask']:r['scores'] for r in table if r['question']==i};need(outputs[i,'F']['prediction']==LETTERS[top(states[15])],'F_FULL_SCORE_OUTPUT_JOIN')
        z=question_metrics(states,label,choices[i]['E15']);z.update(question=i,source=x['source'])
        for method in METHODS:
            answer=outputs[i,method]['prediction'];correct=int(answer==LETTERS[label]);oldrow=derived[i,method];need(type(oldrow['correct']) is int and oldrow['correct']==correct and oldrow['state']==('VALID_CORRECT' if correct else 'VALID_WRONG') and oldrow['source']==x['source'],'OLD144_CORRECTNESS_MISMATCH')
            z[method]=correct;old_cells.append(dict(question=i,method=method,prediction=answer,correct=correct,state=oldrow['state']))
        for method in ('I','A'):
            selected=choices[i]['IA'][method];category='candidate_mismatch' if not selected['top_match'] else 'top_match_correct' if selected['observed_top']==label else 'top_match_wrong';z[method+'_category']=category
            changed=outputs[i,method].get('changed');need(type(changed) is bool and changed==(outputs[i,method]['prediction']!=outputs[i,'F']['prediction']),'OLD_CHANGE_FLAG');z[method+'_changed']=int(changed)
        need(z['H']==z['O15']-z['F'] and z['E15']-z['F']==z['recovered']-z['harm'] and z['missed']==z['H']-z['recovered']>=0,'HEADROOM_IDENTITIES');metrics.append(z)
    need({m:sum(z[m] for z in metrics) for m in METHODS}=={'F':9,'M':7,'A':10,'I':8,'C':10,'R':11},'OLD_TOTALS')
    public=read(Path(cfg['repo'])/'docs/codex-artifacts/VLM-BLOCK-INTERACTION-053/execution-summary.json');aliases=read(root/'source-selection.json')['aliases'];source_alias={a:'S'+str(i+1).zfill(2) for i,a in enumerate(aliases)}
    for a in aliases:
        ids=[i for i,x in enumerate(q) if x['source']==a];need(len(ids)==6,'SOURCE_N')
        for m in METHODS:
            expected=next(c['correct'] for c in public['conditions'] if c['source']==source_alias[a] and c['method']==m);need(sum(metrics[i][m] for i in ids)==expected,'OLD_SOURCE_TOTALS')
    write(root/'labels-private.json',labels);write(root/'old144-verified-private.json',old_cells);write(root/'question-metrics-private.json',metrics)
    conditions=[];heads=[];rank_profiles=[]
    for a in ['ALL']+aliases:
        ids=[i for i,x in enumerate(q) if a=='ALL' or x['source']==a];source=source_alias.get(a,a);n=len(ids)
        for c in CONDITIONS:
            kind='FROZEN_053_METHOD' if c in METHODS else 'POSTHOC_UNGATED_CONFIDENCE_CONTROL' if c=='E15' else 'MASKED_CONTROL' if c=='B0' else 'FINITE_GOLD_ORACLE_NOT_DEPLOYABLE';conditions.append(dict(source=source,condition=c,kind=kind,N=n,correct=sum(metrics[i][c] for i in ids),unknown=0))
        h=dict(source=source,N=n,**{k:sum(metrics[i][k] for i in ids) for k in ('F','O15','E15','H','recovered','harm','missed')},**{('NONE' if k=='NONE' else 'K'+str(k)):sum(metrics[i]['K']==k for i in ids) for k in (1,2,3,4,'NONE')})
        for m in ('I','A'):
            for cat in ('candidate_mismatch','top_match_wrong','top_match_correct'):h[m+'_'+cat]=sum(metrics[i][m+'_category']==cat for i in ids)
            h[m+'_final_correct']=sum(metrics[i][m] for i in ids);h[m+'_final_changed']=sum(metrics[i][m+'_changed'] for i in ids)
        heads.append(h)
        for group in ('ALL_STATES','NONEMPTY','K0','K1','K2','K3','K4'):
            rs=[r for r in table if r['question'] in ids and (group=='ALL_STATES' or group=='NONEMPTY' and r['mask']>0 or group.startswith('K') and bits(r['mask'])==int(group[1:]))];ranks=[];margins=[]
            for row in rs:
                target=labels[row['question']];ordered=sorted(range(5),key=lambda b:(-row['scores'][b],b));ranks.append(ordered.index(target)+1);margins.append(margin(row['scores'],target))
            rank_profiles.append(dict(source=source,group=group,question_N=n,state_vectors=len(rs),target_rank_histogram={str(k):ranks.count(k) for k in range(1,6)},target_margin=dict(min=min(margins),q25=quantile(margins,.25),median=quantile(margins,.5),q75=quantile(margins,.75),max=max(margins),mean=sum(margins)/len(margins))))
    positive=sum(h['H']>0 for h in heads if h['source']!='ALL');overall=heads[0];state=decision(overall['H'],positive,overall['missed']);write(root/'condition-table.json',conditions);write(root/'headroom-table.json',heads);write(root/'rank-margin-profiles.json',rank_profiles)
    write(root/'analysis-receipt.json',dict(status=state,N=24,old_cells_matched=144,old_mismatches=0,original_opens=1,original_bytes=budget['original_returned'],gold_values_decoded=decoded,H_positive_sources=positive,conditions=60,headroom_rows=5,classification_sealed_before_gold=True,analysis_code_sha=sha(Path(__file__).read_bytes()),labels_sha=sha((root/'labels-private.json').read_bytes()),metrics_sha=sha((root/'question-metrics-private.json').read_bytes())))
    print('FINITE_VIEW_RECOUNT_COMPLETE',state)


def suite(root):
    n=0
    def check(ok):
        nonlocal n
        n+=1;need(ok,'FIXTURE_ASSERTION')
    def refuse(fn):
        try:fn()
        except ValueError:check(True)
        else:check(False)
    check(top([1,1,0,0,0])==0);states={m:[0,0,0,0,0] for m in range(16)};check(e15(states)['mask']==15)
    states[0]=[100,0,0,0,0];check(e15(states)['mask']==15);states[3]=[2,0,0,0,0];states[5]=[2,0,0,0,0];check(e15(states)['mask']==3)
    refuse(lambda:e15({k:v for k,v in states.items() if k!=2}));refuse(lambda:top([math.nan]*5))
    states={m:[2,0,0,0,0] for m in range(16)};states[1]=[0,3,0,0,0];z=question_metrics(states,1,e15(states));check(z['O1']==1 and z['O2']==0 and z['O15']==1 and z['K']==1 and z['H']==z['recovered']==1 and z['missed']==0)
    states[15]=[0,4,0,0,0];states[2]=[5,0,0,0,0];z=question_metrics(states,1,e15(states));check(z['F']==1 and z['E15']==0 and z['harm']==1 and z['H']==z['missed']==0)
    rows=[dict(question=i,method=m) for i in range(24) for m in METHODS];check(len(validate_join(rows))==144);refuse(lambda:validate_join(rows[:-1]));refuse(lambda:validate_join(rows+[rows[0]]))
    check(decision(3,4,2)=='FINITE_VIEW_HEADROOM_TOO_SMALL');check(decision(4,2,2)=='FINITE_VIEW_HEADROOM_TOO_SMALL');check(decision(4,3,2)=='RANKING_GAP_OBSERVED');check(decision(4,3,1)=='SIMPLE_CONFIDENCE_USES_MOST_HEADROOM');check(quantile([0,2,4,6],.25)==1.5)
    write(Path(root)/'necessary-tests.json',dict(status='PASS',assertions=n,owned_only=True));print('NECESSARY_FIXTURES_PASS',n)


def emit_review(root):
    compile(REVIEW_SOURCE,'independent-review-054.py','exec')
    with (Path(root)/'independent-review-054.py').open('x',encoding='utf-8') as f:f.write(REVIEW_SOURCE)
    write(Path(root)/'review-config.json',dict(code_path=str(Path(__file__).resolve())))


def supervise(root,role):
    root=Path(root);cfg=read(root/'coordinator-config.json');need(time.time()<cfg['deadline_epoch'],'PARENT_DEADLINE');platform=helper(cfg['repo'],'auditable_runner_040.py','3e56faf30afea1bed850c085bceb2afcc4fb257c');caps=dict(suite=30,review_setup=30,nongold=90,analyze=90,verify=60);used=sum(read(p)['wall'] for p in root.glob('*-phase.json'));cap=min(caps[role],300-used,cfg['deadline_epoch']-time.time());need(cap>5 and not (root/(role+'-phase.json')).exists(),'RESTART_OR_BUDGET')
    job=platform.Job(memory=1024**3,active_limit=4);limit=platform.Extended();need(job.api.QueryInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit),None),'JOB_QUERY');limit.basic.flags|=0x10;limit.basic.affinity=1;need(job.api.SetInformationJobObject(job.handle,9,C.byref(limit),C.sizeof(limit)),'JOB_AFFINITY');start=time.monotonic();child=None
    try:
        script=root/'independent-review-054.py' if role=='verify' else Path(__file__).resolve();argv=[cfg['python'],'-I','-S','-B',str(script)]+([str(root)] if role=='verify' else [role,str(root)]);child=platform.Process(argv,root/(role+'.log'),job)
        while job.active():
            if time.monotonic()-start>cap-3:job.kill();break
            time.sleep(.005)
        need(job.empty(start+cap-1),'OWN_JOB_EXIT_UNKNOWN');result=dict(role=role,wall=time.monotonic()-start,exitcode=child.poll(),**job.snapshot());write(root/(role+'-phase.json'),result);print(json.dumps(result));print((root/(role+'.log')).read_text(encoding='utf-8',errors='replace')[-1200:].encode('ascii','backslashreplace').decode())
    finally:
        if child:child.close()
        job.close()


REVIEW_SOURCE=r'''"""054 independent stdlib reconstruction; no tested selector import or old opens."""
from pathlib import Path
import json,hashlib,math,sys,threading
r=Path(sys.argv[1]);rd=lambda n:json.loads((r/n).read_bytes());digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();n=0
def check(ok):
 global n
 n+=1;assert ok
seal=rd('nongold-seal.json');q=rd('nongold.json');table=rd('initial-states-private.json');choices=rd('nongold-choices-private.json');labels=rd('labels-private.json');old=rd('old144-verified-private.json');metrics=rd('question-metrics-private.json');conditions=rd('condition-table.json');heads=rd('headroom-table.json');profiles=rd('rank-margin-profiles.json');receipt=rd('analysis-receipt.json')
check(seal['state_sha']==digest(r/'initial-states-private.json') and seal['choice_sha']==digest(r/'nongold-choices-private.json') and seal['nongold_sha']==digest(r/'nongold.json'))
check(seal['code_sha']==receipt['analysis_code_sha']==digest(Path(rd('review-config.json')['code_path'])))
check(receipt['labels_sha']==digest(r/'labels-private.json') and receipt['metrics_sha']==digest(r/'question-metrics-private.json'))
for role in ('nongold','analyze'):
 p=rd(role+'-phase.json');check(p['active']==0 and p['exitcode']==0 and not p['killed'])
check(rd('scoring-config.json')['nongold_actual_exit_before_scoring_config'] and rd('scoring-config.json')['at']>=seal['at'])
check(len(q)==len(choices)==len(labels)==len(metrics)==24 and len(table)==384 and len(old)==144)
check(all(type(a) is int and 0<=a<5 for a in labels))
states={};seen=set()
for x in table:
 key=x['question'],x['mask'];check(key not in seen and type(key[0]) is int and 0<=key[0]<24 and type(key[1]) is int and 0<=key[1]<16);seen.add(key);states[key]=x['scores'];check(len(x['scores'])==5 and all(math.isfinite(v) for v in x['scores']))
check(seen=={(i,m) for i in range(24) for m in range(16)})
top=lambda scores:min(range(5),key=lambda a:(-scores[a],a));gap=lambda scores,a:scores[a]-max(scores[b] for b in range(5) if b!=a);bits=lambda m:bin(m).count('1')
oldmap={};methods=['F','M','A','I','C','R'];expected=[]
for x in old:
 key=x['question'],x['method'];check(key not in oldmap);oldmap[key]=x;check(x['correct']==int(x['prediction']=='ABCDE'[labels[key[0]]]) and x['state']==('VALID_CORRECT' if x['correct'] else 'VALID_WRONG'))
check(set(oldmap)=={(i,m) for i in range(24) for m in methods})
for i in range(24):
 candidates=[]
 for mask in range(16):
  vs=states[i,mask];a=top(vs);entry=next(x for x in table if x['question']==i and x['mask']==mask);check(entry['a']==a and entry['margin']==gap(vs,a))
  if mask:candidates.append((gap(vs,a),bits(mask),mask,a))
 margin,_,mask,a=min(candidates,key=lambda z:(-z[0],-z[1],z[2],z[3]));choice=choices[i];check(choice['question']==i and choice['E15']=={'a':a,'mask':mask,'margin':margin})
 good={m:top(states[i,m])==labels[i] for m in range(16)};successful=[m for m in range(1,16) if good[m]];f=int(good[15]);e=int(a==labels[i]);o=int(bool(successful));minimum=min(map(bits,successful)) if successful else 'NONE'
 z={'question':i,'source':q[i]['source'],'F':f,'E15':e,'B0':int(good[0]),'O15':o,'O1':int(any(good[m] for m in range(1,16) if bits(m)==1)),'O2':int(any(good[m] for m in range(1,16) if bits(m)==2)),'O3':int(any(good[m] for m in range(1,16) if bits(m)==3)),'H':int(not f and o),'recovered':int(not f and e),'harm':int(f and not e),'missed':int(not f and o and not e),'K':minimum}
 check(oldmap[i,'F']['prediction']=='ABCDE'[top(states[i,15])])
 for method in methods:z[method]=oldmap[i,method]['correct']
 for method in ('I','A'):
  s=choice['IA'][method];measured=top(states[i,s['mask']]);check(s['observed_top']==measured and s['top_match']==(s['a']==measured))
  z[method+'_category']='candidate_mismatch' if s['a']!=measured else 'top_match_correct' if measured==labels[i] else 'top_match_wrong'
  z[method+'_changed']=int(oldmap[i,method]['prediction']!=oldmap[i,'F']['prediction'])
 check(z==metrics[i]);check(o>=f and o>=e and z['missed']==z['H']-z['recovered']>=0 and e-f==z['recovered']-z['harm']);expected.append(z)
check({m:sum(z[m] for z in expected) for m in methods}=={'F':9,'M':7,'A':10,'I':8,'C':10,'R':11})
aliases=rd('source-selection.json')['aliases'];src={s:'S'+str(i+1).zfill(2) for i,s in enumerate(aliases)}
conds=methods+['E15','B0','O15','O1','O2','O3'];check(len(conditions)==60 and len({(x['source'],x['condition']) for x in conditions})==60 and len(heads)==5)
for source in ['ALL']+list(src.values()):
 ids=[i for i,x in enumerate(q) if source=='ALL' or src[x['source']]==source];check(len(ids)==(24 if source=='ALL' else 6))
 for c in conds:
  row=next(x for x in conditions if x['source']==source and x['condition']==c);kind='FROZEN_053_METHOD' if c in methods else 'POSTHOC_UNGATED_CONFIDENCE_CONTROL' if c=='E15' else 'MASKED_CONTROL' if c=='B0' else 'FINITE_GOLD_ORACLE_NOT_DEPLOYABLE'
  check(row=={'source':source,'condition':c,'kind':kind,'N':len(ids),'correct':sum(expected[i][c] for i in ids),'unknown':0})
 h=next(x for x in heads if x['source']==source);check(h['N']==len(ids))
 for k in ('F','O15','E15','H','recovered','harm','missed'):check(h[k]==sum(expected[i][k] for i in ids))
 for k in (1,2,3,4,'NONE'):check(h['NONE' if k=='NONE' else 'K'+str(k)]==sum(expected[i]['K']==k for i in ids))
 check(h['H']==h['O15']-h['F'] and h['missed']==h['H']-h['recovered'] and h['E15']-h['F']==h['recovered']-h['harm'])
 for method in ('I','A'):
  for cat in ('candidate_mismatch','top_match_wrong','top_match_correct'):check(h[method+'_'+cat]==sum(expected[i][method+'_category']==cat for i in ids))
  check(sum(h[method+'_'+cat] for cat in ('candidate_mismatch','top_match_wrong','top_match_correct'))==len(ids))
  check(h[method+'_final_correct']==sum(expected[i][method] for i in ids) and h[method+'_final_changed']==sum(expected[i][method+'_changed'] for i in ids))
def percentile(xs,p):
 ys=sorted(xs);v=(len(ys)-1)*p;lo=int(v);hi=min(lo+1,len(ys)-1);return ys[lo]+(v-lo)*(ys[hi]-ys[lo])
check(len(profiles)==35)
for row in profiles:
 ids=[i for i,x in enumerate(q) if row['source']=='ALL' or src[x['source']]==row['source']];group=row['group'];masks=list(range(16)) if group=='ALL_STATES' else list(range(1,16)) if group=='NONEMPTY' else [m for m in range(16) if bits(m)==int(group[1:])];ranks=[];margins=[]
 for i in ids:
  for m in masks:
   vs=states[i,m];ranks.append(sorted(range(5),key=lambda b:(-vs[b],b)).index(labels[i])+1);margins.append(gap(vs,labels[i]))
 check(row['question_N']==len(ids) and row['state_vectors']==len(ranks) and row['target_rank_histogram']=={str(k):ranks.count(k) for k in range(1,6)})
 values={'min':min(margins),'max':max(margins),'mean':sum(margins)/len(margins),'q25':percentile(margins,.25),'median':percentile(margins,.5),'q75':percentile(margins,.75)}
 check(all(abs(row['target_margin'][k]-v)<=1e-12 for k,v in values.items()))
h=next(x for x in heads if x['source']=='ALL');positive=sum(x['H']>0 for x in heads if x['source']!='ALL');state='FINITE_VIEW_HEADROOM_TOO_SMALL' if h['H']<4 or positive<3 else 'RANKING_GAP_OBSERVED' if h['missed']>=2 else 'SIMPLE_CONFIDENCE_USES_MOST_HEADROOM';check(receipt['status']==state and receipt['H_positive_sources']==positive and receipt['old_cells_matched']==144 and receipt['old_mismatches']==0)
for c in conds:check(next(x['correct'] for x in conditions if x['source']=='ALL' and x['condition']==c)==sum(x['correct'] for x in conditions if x['source']!='ALL' and x['condition']==c))
budget=rd('read-budget.json');check(budget['original_opens']==1 and budget['original_returned']<=4*1024**2 and budget['metadata_returned']<=8*1024**2)
check(receipt['gold_values_decoded']==24 and all(x['role']=='scoring' for x in budget['metadata_opens'] if x['name'] in ('outputs-private.json','scored-derived-private.json','scoring-receipt.json')))
phases=[json.loads(p.read_bytes()) for p in r.glob('*-phase.json')];check(sum(x['wall'] for x in phases)<=300 and all(x['active']==0 and not x['killed'] and x['peak_commit']<=1024**3 for x in phases))
check(threading.active_count()==1 and not any(x.split('.')[0] in ('torch','transformers','numpy','PIL','cv2') for x in sys.modules))
(r/'independent-review.json').write_text(json.dumps({'status':'PASS','assertions':n,'state_vectors':384,'nonempty_state_correctness_rebuilt':360,'old_correctness_cells_rebuilt':144,'condition_rows':60,'headroom_rows':5,'rank_margin_profiles':35,'decision':state,'tested_E15_or_aggregation_imported':False,'old_data_opens':0,'original_reopens':0}));print('INDEPENDENT_REVIEW_PASS',n)
'''


if __name__=='__main__':
    role,path,*extra=sys.argv[1:];root=Path(path)
    if role=='launch':supervise(root,extra[0])
    else:
        {'suite':suite,'review_setup':emit_review,'nongold':nongold,'analyze':analyze}[role](root)
        no_runtime()
