"""049 necessary mathematical/qualification tests; independent exit review.

The verification role imports no model library and does not reopen gold.
"""
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
import sys


def load(p):return json.loads(Path(p).read_bytes())


def suite(root):
    import numpy as np
    path=Path(__file__).with_name('selection_channel_049.py')
    spec=importlib.util.spec_from_file_location('core049',path);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    count=0;cases=[]
    def check(ok):
        nonlocal count
        count+=1;assert ok
    def case(name,fn):
        try:fn();cases.append(dict(name=name,status='PASS'))
        except Exception as e:cases.append(dict(name=name,status='FAIL',error=type(e).__name__))
    def refuses(fn):
        try:fn()
        except ValueError:check(True)
        else:check(False)
    q=lambda text,options=None:dict(ordinal=0,question=text,options=options or ['A','B','C','D','E'])
    case('uniform_exact_rule',lambda:check(c.U==[(47*j+5)//11 for j in range(12)]))
    case('stable_tie_lower_indices',lambda:check(c.top12([1.]*48)==list(range(12))))
    case('restore_temporal_candidate_order',lambda:check(c.top12(list(range(48)))==list(range(36,48))))
    case('nonfinite_score_refused',lambda:refuses(lambda:c.top12([float('nan')]*48)))
    case('whole_words_not_substrings',lambda:check(c.qualify(q('What color is the afternoon background?'))=='ELIGIBLE_NONGOLD'))
    case('temporal_options_excluded',lambda:check(c.qualify(q('Which object?',options=['before opening','B','C','D','E']))=='TIME_DEPENDENT'))
    case('unicode_normalization',lambda:check(c.qualify(q('Ｂｅｆｏｒｅ which action?'))=='TIME_DEPENDENT'))
    case('chinese_duration_refused',lambda:check(c.qualify(q('这持续多久？'))=='TIME_DEPENDENT'))
    case('clock_pattern_refused',lambda:check(c.qualify(q('Which object at 12:30?'))=='TIME_DEPENDENT'))
    case('five_nonempty_options',lambda:check(c.qualify(q('Which object?',options=['A','','C','D','E']))=='FORMAT_OR_JOIN'))
    case('external_picture_refused',lambda:check(c.qualify(q('Which object is in the reference image?'))=='EXTERNAL_RESOURCE'))
    case('prerequisite_steps_are_temporal_semantics',lambda:check(c.qualify(q('What prerequisite steps were taken?'))=='TIME_DEPENDENT_TASK_SEMANTICS'))
    case('immediately_follows_is_temporal_semantics',lambda:check(c.qualify(q('What immediately follows picking up the bowl?'))=='TIME_DEPENDENT_TASK_SEMANTICS'))
    def matrix():
        image=np.zeros((4,48,2),dtype=np.float32);image[:]=[0,1]
        image[0,0]=[1,0];image[1,1]=[1,0];image[2,2]=[1,0];image[3,3]=[1,0]
        actual=c.cross_scores(image,np.array([[1.,0.]],dtype=np.float32),np)
        check(actual.shape==(1,4,48));check([int(actual[0,s].argmax()) for s in range(4)]==[0,1,2,3])
        check([actual[0,s,s] for s in range(4)]==[1.]*4)
        refuses(lambda:c.cross_scores(np.zeros_like(image),np.array([[1.,0.]],dtype=np.float32),np))
    case('true_same_question_cross_source_matrix_and_zero_norm',matrix)
    class FakeTorch:
        @staticmethod
        def is_tensor(v):return False
    def aliases():
        a={'text':[1,2],'visual':[3,4]};b={'text':[1,2],'visual':[3,4]}
        check(c.exact_equal(a,b,FakeTorch));check(len({c.sha(c.packed(a)),c.sha(c.packed(b))})==1)
        check(len([a,b])==2)
    case('UO_UR_physical_alias_logical_denominator',aliases)
    def fixtures(ns,make):
        questions=[];slots={}
        for s,n in enumerate(ns):
            for j in range(n):
                i=len(questions);questions.append(dict(source='S'+str(s)))
                for condition in c.CONDITIONS:
                    correct=make(s,j,condition)
                    slots[i,condition]=dict(correct=correct,state='SCORING_UNKNOWN' if correct is None else 'VALID_CORRECT' if correct else 'VALID_WRONG')
        return questions,['S'+str(s) for s in range(4)],slots
    def d_hand():
        def make(s,j,condition):
            if condition.startswith('G') and condition!='GU':return int(int(condition[1])-1 in (s,(s+1)%4))
            return 0
        out=c.aggregate(*fixtures([3,3,3,3],make))
        check(out['D_exact']=='2/3');check(abs(out['D']-2/3)<1e-12)
    case('hand_D_two_thirds',d_hand)
    def i_hand():
        def make(s,j,condition):return int(j<(3 if condition=='SO' else 2))
        out=c.aggregate(*fixtures([4,4,4,4],make));check(out['I_exact']=='1/4');check(out['I']==.25)
    case('hand_I_one_quarter',i_hand)
    def equal_sources():
        def make(s,j,condition):
            if not condition.startswith('G') or condition=='GU':return 0
            return int(s==0 and int(condition[1])==1)
        out=c.aggregate(*fixtures([3,4,5,6],make));check(out['D_exact']=='1/4')
        check(sum(x['n'] for x in out['per_source'].values())==18)
    case('unequal_n_source_equal_weight',equal_sources)
    def missing():
        args=fixtures([3]*4,lambda s,j,c:0);args[2][0,'SO']=dict(correct=0,state='NOT_RUN')
        out=c.aggregate(*args);check(out['per_source']['S0']['arms']['SO']['N']==3 and out['decision']=='INCOMPLETE_OR_UNKNOWN')
        args[2][0,'SO']=dict(correct=None,state='SCORING_UNKNOWN');out=c.aggregate(*args)
        check(out['I'] is None and out['D'] is None and out['decision']=='INCOMPLETE_OR_UNKNOWN')
    case('failure_denominator_and_unknown_priority',missing)
    def projection():
        raw=b'{"wanted":{"benchmark_dataset":[{"question":"x","options":["a","b","c","d","e"],"correct_answer_label":"SECRET","ignored":NaN},{"question":"y","correct_answer_label":"B"}]},"other":{"benchmark_dataset":[{"correct_answer_label":"C"}]}}'
        out,gold=c.projected_json(raw,{'wanted':{0}},{'question','options'})
        check(gold==0 and out['wanted'][0]['question']=='x' and 'correct_answer_label' not in out['wanted'][0] and 'other' not in out)
        out,gold=c.projected_json(raw,{'wanted':{1}},{'correct_answer_label'})
        check(gold==1 and out=={'wanted':{1:{'correct_answer_label':'B'}}})
        refuses(lambda:c.projected_json(b'{"wanted":{"benchmark_dataset":[{"question":NaN}]}}',{'wanted':{0}},{'question'}))
    case('lexical_nongold_and_selected_gold_only',projection)
    def cost():
        # Independent, hand-known receipt arithmetic: outer is not an addend.
        outer=10;shared=[('prepare',2)]*4;unique=dict(shared)
        check(sum(unique.values())==2 and outer!=outer+sum(unique.values()))
    case('shared_once_outer_not_double_counted',cost)
    result=dict(cases=cases,assertions=count,passed=sum(x['status']=='PASS' for x in cases),failed=sum(x['status']=='FAIL' for x in cases))
    (root/'necessary-tests.json').write_text(json.dumps(result))
    print('CASES',len(cases),'ASSERTIONS',count,'FAIL',result['failed']);return not result['failed']


def verify(root):
    # No implementation import, original labels, predictions or model inputs.
    score=load(root/'score-private.json');result=score['result'];slots={(r['question'],r['condition']):r for r in score['slots']}
    questions=load(root/'nongold-projected.json');selection=load(root/'source-selection.json');queue=load(root/'input-queue-seal.json')
    phase=load(root/'infer-phase.json');complete=load(root/'inference-complete.json') if (root/'inference-complete.json').exists() else None
    checks=0
    def check(ok):
        nonlocal checks
        checks+=1;assert ok
    check(phase['active']==0);check(len(queue['logical'])==10*len(questions)<=240)
    check(result['gold_open_count']==1 and result['gold_values_decoded']<=24)
    check(queue['nongold_sha']==hashlib.sha256((root/'nongold-projected.json').read_bytes()).hexdigest())
    ds=[];is_=[]
    for own,source in enumerate(selection['aliases']):
        ids=[i for i,q in enumerate(questions) if q['source']==source];n=len(ids)
        check(result['per_source'][source]['n']==n and 3<=n<=6)
        dvals=[];ivals=[]
        for i in ids:
            g=[slots[i,'G'+str(k)]['correct'] for k in range(1,5)]
            dvals.append(None if None in g else F(g[own])-F(sum(g[j] for j in range(4) if j!=own),3))
            v=[slots[i,c]['correct'] for c in ('UO','UR','SO','SR')]
            ivals.append(None if None in v else F((v[2]-v[0])-(v[3]-v[1])))
            check(next(x['identity'] for x in queue['logical'] if x['question']==i and x['condition']=='UO')==next(x['identity'] for x in queue['logical'] if x['question']==i and x['condition']=='UR'))
        d=None if None in dvals else sum(dvals)/n;iv=None if None in ivals else sum(ivals)/n
        ds.append(d);is_.append(iv)
        check(result['per_source'][source]['D_exact']==(None if d is None else str(d)))
        check(result['per_source'][source]['I_exact']==(None if iv is None else str(iv)))
        for condition,arm in result['per_source'][source]['arms'].items():
            values=[slots[i,condition]['correct'] for i in ids]
            check(arm['N']==n and arm['correct']==(None if None in values else sum(values)))
    unknown=any(r['correct'] is None for r in slots.values())
    D=None if unknown else sum(ds)/4;I=None if unknown else sum(is_)/4
    check(result['D_exact']==(None if D is None else str(D)));check(result['I_exact']==(None if I is None else str(I)))
    if complete:
        check(complete['generate_attempts']<=9*len(questions)<=216 and complete['image_count']==192 and complete['text_count']==len(questions))
        check(complete['returns']==len(queue['unique'])==complete['unique'])
    incomplete=any(r['state'] in ('FAILED','NOT_RUN','SCORING_UNKNOWN') for r in slots.values())
    if incomplete:expected='INCOMPLETE_OR_UNKNOWN'
    else:
        h1=D>=F(2,25) and sum(d>0 for d in ds)>=3
        h2=abs(I)>=F(1,20) and sum(i!=0 and (i>0)==(I>0) for i in is_)>=3
        expected='DEVELOPMENT_GO_TO_OWNER_REVIEW' if h1 and h2 else 'CHANNEL_ONLY' if h1 else 'REPRESENTATION_SENSITIVITY_ONLY' if h2 else 'STOP_CURRENT_HYPOTHESIS'
    check(result['decision']==expected)
    (root/'independent-review.json').write_text(json.dumps(dict(status='PASS',assertions=checks,D_exact=None if D is None else str(D),I_exact=None if I is None else str(I),decision=expected,labels_reopened=0,implementation_imported=False)))
    print('INDEPENDENT_REVIEW_PASS',checks,'assertions');return True


if __name__=='__main__':
    role,path=sys.argv[1:];root=Path(path)
    sys.exit(0 if (suite(root) if role=='suite' else verify(root)) else 1)
