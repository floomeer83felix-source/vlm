"""050 owned mathematical tests and independent stdlib review, no gold reopen."""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def read(p):return json.loads(Path(p).read_bytes())


def suite(root):
    spec=importlib.util.spec_from_file_location('coverage050',Path(__file__).with_name('coverage_aggregation_050.py'));c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    assertions=0;rows=[]
    def check(ok):
        nonlocal assertions
        assertions+=1;assert ok
    def refused(fn):
        try:fn()
        except ValueError:check(True)
        else:check(False)
    def case(name,fn):
        try:fn();rows.append(dict(name=name,status='PASS'))
        except Exception as e:rows.append(dict(name=name,status='FAIL',exception=type(e).__name__))
    def rec(a):return dict(state='INVALID',prediction=None,eos=False) if a=='INVALID' else dict(state='VALID',prediction=a,eos=True)
    for data,expected in [(['A','A','B','C'],'A'),(['A','B','B','A'],'A'),(['INVALID','C','C','B'],'C'),(['INVALID']*4,None)]:
        case('vote_'+''.join(data),lambda data=data,expected=expected:check(c.plurality([rec(a) for a in data])['prediction']==expected))
    case('tie_is_earliest_not_alphabetical',lambda:check(c.plurality([rec(a) for a in ['B','A','A','B']])['prediction']=='B'))
    case('all_invalid_vote_count_zero',lambda:check(c.plurality([rec('INVALID')]*4)['valid_votes']==0))
    def partition():
        groups=[c.positions('P'+str(j)) for j in range(4)]
        check(groups[0]==[0,4,8,12,16,20,24,28,32,36,40,44])
        check(all(len(g)==12 for g in groups) and set().union(*map(set,groups))==set(range(48)))
        check(all(set(groups[a]).isdisjoint(groups[b]) for a in range(4) for b in range(a)))
        check(c.positions('F48')==list(range(48)))
        for j,g in enumerate(groups):check([(g[k]+g[k+1])/2 for k in range(0,12,2)]==[j+2+8*m for m in range(6)])
        check([(i+i+1)/2 for i in range(0,48,2)]==[.5+2*m for m in range(24)])
    case('partition_and_independent_native_clock_formulas',partition)
    def schema():
        q={'question':'Owned fixture','options':['a','b','c','d','e']};check(c.canonical_question(q)[:2]==('Owned fixture',['a','b','c','d','e']))
        d={'question':'Owned fixture','options':dict(zip('ABCDE',['a','b','c','d','e']))};check(c.canonical_question(d)[1]==q['options'])
        top={'question':'Owned fixture',**dict(zip('ABCDE',q['options']))};check(c.canonical_question(top)[1]==q['options'])
        check(c.canonical_question(dict(top,options=q['options']))[1]==q['options'])
        refused(lambda:c.canonical_question({'options':q['options']}))
        refused(lambda:c.canonical_question({'question':'x'}))
        refused(lambda:c.canonical_question(dict(top,options=['WRONG','b','c','d','e'])))
        refused(lambda:c.canonical_question({'question':'x','A':'a'}))
    case('strict_original_three_schemas_no_fallback',schema)
    def selective():
        v=c.JSONView(b'{"wanted":{"prediction":"A","state":"VALID"},"gray":{"prediction":"DO_NOT_CONSUME"}}')
        result={k:v.atom(a,b) for k,a,b in v.members() if k=='wanted'};check(set(result)=={'wanted'} and result['wanted']['prediction']=='A')
    case('closed_natural_records_only',selective)
    def paired():check(c.paired([1,0,1,0],[0,1,1,0])==dict(correction=1,harm=1,both_correct=1,both_wrong=1,unknown=0))
    case('net_correction_harm_fourfold',paired)
    def fixture(ns,unknown=False):
        qs=[];slots={};diag=[]
        for s,n in enumerate(ns):
            for j in range(n):
                i=len(qs);qs.append(dict(source='S'+str(s)))
                for condition in c.ARMS+['V4']+c.BASES+['O4','O5']:
                    good=int(s==0 and condition=='F48');slots[i,condition]=dict(correct=good,state='VALID_CORRECT' if good else 'VALID_WRONG')
                diag.append({k:0 for k in ('full_only','split_only','split_only_recovered_by_vote','vote_missed','all_five_wrong')})
        if unknown:slots[0,'SO']=dict(correct=None,state='SCORING_UNKNOWN')
        return qs,['S'+str(s) for s in range(4)],slots,diag
    def source_weight():
        out=c.aggregate(*fixture([3,4,5,6]),True,True)
        check(out['N']==18 and out['gates']['F48']['mean_net_exact']=='1/4' and out['gates']['F48']['positive_sources']==1)
        check(out['decision']=='NO_MATERIAL_DEPLOYABLE_GAIN')
    case('different_n_source_equal_not_question_weighted',source_weight)
    def unknown():
        out=c.aggregate(*fixture([6]*4,True),True,True);check(out['decision']=='INCOMPLETE_OR_UNKNOWN' and out['gates']['F48']['passed'] is None)
        args=fixture([6]*4);args[2][0,'P0']=dict(correct=0,state='NOT_RUN');out=c.aggregate(*args,True,False)
        check(out['decision']=='INCOMPLETE_OR_UNKNOWN' and out['per_source']['S0']['arms']['P0']['N']==6)
    case('unknown_or_failed_keeps_denominator_and_blocks_GO',unknown)
    def mismatch():check(c.aggregate(*fixture([6]*4),False,True)['decision']=='INCOMPLETE_OR_UNKNOWN')
    case('baseline_scoring_mismatch_blocks_main_conclusion',mismatch)
    def cost():
        out=c.phase_costs([dict(role='prepare',wall=2),dict(role='infer',wall=10)],{'prefill':3,'decode':4})
        check(out['supervised_outer_wall_sum']==12 and out['GPU_supervised_outer']==10 and out['CPU_supervised_wall']==2)
        refused(lambda:c.phase_costs([dict(role='infer',wall=10),dict(role='infer',wall=10)],{}))
    case('inclusive_cost_not_double_counted',cost)
    def oracle():
        votes=[rec(a) for a in ['B','B','A','C']];gold='A';v=c.plurality(votes);o4=any(x['prediction']==gold for x in votes)
        check(o4 and v['prediction']!=gold)
        for f in (0,1):check(int(f or o4)>=max(f,int(v['prediction']==gold)))
    case('finite_oracle_not_deployable_and_bounds',oracle)
    def dedup():
        logical=['one','same','same','other'];unique=list(dict.fromkeys(logical))
        check(len(logical)==4 and len(unique)==3 and unique==['one','same','other'])
    case('dedup_preserves_logical_rows',dedup)
    result=dict(cases=rows,assertions=assertions,passed=sum(r['status']=='PASS' for r in rows),failed=sum(r['status']=='FAIL' for r in rows));(root/'necessary-tests.json').write_text(json.dumps(result));print('CASES',len(rows),'ASSERTIONS',assertions,'FAIL',result['failed']);return result['failed']==0


def verify(root):
    # Never imports the implementation or opens the original annotation.
    if not (root/'binding-receipt.json').exists():
        return verify_input_failure(root)
    q=read(root/'nongold.json');selection=read(root/'source-selection.json');queue=read(root/'input-queue-seal.json');score=read(root/'score-private.json');old=read(root/'old-natural-private.json');phase=read(root/'infer-phase.json');done=read(root/'inference-complete.json');pred=read(root/'predictions-private.json');result=score['result']
    mapping={(r['question'],r['arm']):r['identity'] for r in queue['logical']};slots={(r['question'],r['condition']):r for r in score['slots']};count=0
    def check(ok):
        nonlocal count
        count+=1;assert ok
    check(phase['active']==0 and phase['exitcode']==0);check(len(q)==24 and len(queue['logical'])==120)
    check(queue['nongold_sha']==hashlib.sha256((root/'nongold.json').read_bytes()).hexdigest())
    check(result['gold_open_count']==1 and result['gold_values_decoded']==24 and result['baseline_mismatch_count']==0)
    for i in range(24):
        parts=[pred.get(mapping[i,'P'+str(j)]) for j in range(4)];valid=[(j,r['prediction']) for j,r in enumerate(parts) if r and r['state']=='VALID' and r['eos'] and r['prediction'] in tuple('ABCDE')]
        if valid:
            counts={x:sum(v==x for _,v in valid) for _,x in valid};maximum=max(counts.values());winners={x for x,n in counts.items() if n==maximum};j,choice=next((j,v) for j,v in valid if v in winners);expected=slots[i,'P'+str(j)]['correct']
            check(score['vote_stats'][i]['valid_votes']==len(valid) and score['vote_stats'][i]['tied']==(len(winners)>1))
        else:expected=None if slots[i,'P0']['correct'] is None else 0
        check(slots[i,'V4']['correct']==expected)
        o4=None if slots[i,'P0']['correct'] is None else int(any(slots[i,'P'+str(j)]['correct'] for j in range(4)))
        o5=None if o4 is None else int(o4 or slots[i,'F48']['correct'])
        check(slots[i,'O4']['correct']==o4 and slots[i,'O5']['correct']==o5)
        if o4 is not None:check(o4>=slots[i,'V4']['correct'] and o5>=max(slots[i,'F48']['correct'],slots[i,'V4']['correct']))
        for base in ('SO','UO','UR','SR'):check(slots[i,base]['correct']==old['correct'][str(i)+':'+base])
    for info in queue['info']:
        arm=info['arm'];expected=list(range(48)) if arm=='F48' else list(range(int(arm[1]),48,4));times=[.5+2*m for m in range(24)] if arm=='F48' else [int(arm[1])+2+8*m for m in range(6)]
        check(info['indices']==expected and info['times']==times and info['grid']==([[24,12,18]] if arm=='F48' else [[6,12,18]]) and info['visual_tokens']==(1296 if arm=='F48' else 324) and info['tokens']<=4096)
    means={};positives={}
    for arm in ('F48','V4'):
        deltas=[]
        for source in selection['aliases']:
            ids=[i for i,row in enumerate(q) if row['source']==source];n=len(ids);net=sum(slots[i,arm]['correct']-slots[i,'SO']['correct'] for i in ids);delta=F(net,n);deltas.append(delta)
            check(result['per_source'][source]['n']==n==6 and result['per_source'][source]['net_vs_SO_exact'][arm]==str(delta))
        means[arm]=sum(deltas)/4;positives[arm]=sum(d>0 for d in deltas)
        check(result['gates'][arm]['mean_net_exact']==str(means[arm]) and result['gates'][arm]['positive_sources']==positives[arm])
    expected='OBSERVED_HEADROOM / OWNER_REVIEW_REQUIRED' if any(means[a]>=F(1,6) and positives[a]>=3 for a in means) else 'NO_MATERIAL_DEPLOYABLE_GAIN'
    check(result['decision']==expected)
    check(done['new_attempts']<=120 and done['new_returns']==done['new_attempts'])
    (root/'independent-review.json').write_text(json.dumps(dict(status='PASS',assertions=count,decision=expected,gold_reopens=0,implementation_imported=False)))
    print('INDEPENDENT_REVIEW_PASS',count,'assertions');return True


def verify_input_failure(root):
    """Review an observed admission failure; never retry the failed binding."""
    phase=read(root/'bind-phase.json');initial=read(root/'necessary-tests-initial.json');final=read(root/'necessary-tests.json');receipt=read(root/'input-failure-closure.json')
    log=(root/'bind.log').read_text(encoding='utf-8',errors='replace');count=0
    def check(ok):
        nonlocal count
        count+=1;assert ok
    check(phase['exitcode']!=0 and phase['active']==0 and not phase['killed'])
    check('MISSING_OR_CONFLICTING_OPTIONS' in log and 'canonical_question(row)' in log)
    check(initial['failed']==1 and final['failed']==0 and final['passed']==16)
    check(receipt['status']=='INPUT_BINDING_UNKNOWN' and receipt['decision']=='INCOMPLETE_OR_UNKNOWN')
    check(receipt['planned_questions']==24 and receipt['planned_new_model_cells']==120)
    check(receipt['new_generate_attempts']==receipt['model_loads']==receipt['gold_value_reads']==0)
    for name in ('binding-receipt.json','nongold.json','input-queue-seal.json','050-call-ledger.jsonl','predictions-private.json','score-private.json','infer-phase.json','probe-phase.json','preflight_gpu-phase.json'):
        check(not (root/name).exists())
    check(len(receipt['source_rows'])==4 and sum(r['N'] for r in receipt['source_rows'])==24)
    for row in receipt['source_rows']:
        check(row['N']==6 and row['planned_new_cells']==row['NOT_RUN']==30)
    for p in root.glob('*-phase.json'):
        r=read(p);check(r['active']==0 and not r['killed'])
    result=dict(status='PASS_AVAILABLE_FAILURE_EVIDENCE_ONLY',assertions=count,decision='INCOMPLETE_OR_UNKNOWN',gold_reopens=0,implementation_imported=False,full_model_review='NOT_RUN')
    (root/'independent-review.json').write_text(json.dumps(result));print('INDEPENDENT_FAILURE_REVIEW_PASS',count,'assertions');return True


if __name__=='__main__':
    role,path=sys.argv[1:];root=Path(path);sys.exit(0 if (suite(root) if role=='suite' else verify(root)) else 1)
