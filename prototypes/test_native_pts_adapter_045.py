"""045 independent rational oracle, rejection checks and actual CPU boundaries."""
from fractions import Fraction as Q
from pathlib import Path
import math
import socket
import sys
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parent))
import native_pts_adapter_045 as c

def oracle_indices():
    out=[]
    for j in range(48):
        whole,rem=divmod(j*95,47);out.append(whole+int(2*rem>47 or (2*rem==47 and whole%2==1)))
    return out

def oracle_times(table):
    def at(i):
        if table=='CFR':return Q(i)
        if table=='A':return Q(i,2) if i<=48 else Q(24)+Q(3*(i-48),2)
        if table=='B':return Q(3*i,2) if i<=48 else Q(72)+Q(i-48,2)
        if table=='Q':return Q(0) if i==0 else Q(i)+Q(1,100)
        raise ValueError('TABLE')
    ix=oracle_indices();return [(at(ix[k])+at(ix[k+1]))/2 for k in range(0,48,2)]

def suite(root):
    root=Path(root);checks=[]
    def check(name,ok):c.require(ok,name);checks.append(name)
    def rejects(name,fn,types=(ValueError,)):
        try:fn()
        except types:checks.append(name);return
        raise AssertionError(name)
    ix=oracle_indices();mapping={i:Q(i) for i in range(96)};request=c.RequestClock(mapping,ix,1)
    check('independent_indices',list(c.selected())==ix)
    check('ties_even',round(Q(5,2))==2 and round(Q(7,2))==4)
    for table in ('CFR','A','B','Q'):
        f=c.fixture(table);r=c.RequestClock({i:Q(x,1000) for i,x in enumerate(f['pts'])},ix,1)
        check('oracle_'+table,list(r.resolve(ix,1,2))==oracle_times(table) and sum(f['durations'])==96000)
    expected=['1.0','5.0','9.0','13.0','17.0','21.0','25.0','29.0','33.0','37.0','41.0','45.0','50.0','54.0','58.0','62.0','66.0','70.0','74.0','78.0','82.0','86.0','90.0','94.0']
    check('frozen_CFR_times',[f'{float(t):.1f}' for t in oracle_times('CFR')]==expected)
    check('Q_quantized_equal',[f'{float(t):.1f}' for t in oracle_times('Q')]==expected and oracle_times('Q')!=oracle_times('CFR'))
    rejects('missing_map',lambda:c.RequestClock(None,ix,1));rejects('missing_key',lambda:c.RequestClock({k:v for k,v in mapping.items() if k!=95},ix,1))
    for label,value in [('nan',float('nan')),('inf',float('inf')),('negative',-1),('nonincreasing',Q(0))]:
        bad=dict(mapping);bad[1 if label=='nonincreasing' else 0]=value
        rejects(label+'_PTS',lambda b=bad:c.RequestClock(b,ix,1))
    for value in (None,0,-1,float('nan'),float('inf'),True):rejects('bad_fps_'+str(value),lambda v=value:c.RequestClock(mapping,ix,v))
    for label,actual in [('unknown',ix[:-1]+[96]),('reversed',list(reversed(ix))),('float',[float(x) for x in ix]),('47',ix[:-1])]:rejects(label+'_indices',lambda v=actual:request.resolve(v,1,2))
    for merge in (0,1,3,2.0,True):rejects('merge_'+str(merge),lambda m=merge:request.resolve(ix,1,m))
    rejects('changed_callback_fps',lambda:request.resolve(ix,2,2));rejects('missing_callback_fps',lambda:request.resolve(ix,None,2))
    mapping[0]=999;check('input_mapping_copied',request.mapping[0]==0)
    rejects('immutable_mapping',lambda:request.mapping.__setitem__(0,999),(AttributeError,TypeError))
    rejects('immutable_request',lambda:setattr(request,'fps',Q(2)),(AttributeError,))
    def kwargs():return dict(text=['owned'],videos=[SimpleNamespace(shape=(48,192,288,3))],video_metadata=[SimpleNamespace(total_num_frames=96,duration=96,width=288,height=192,fps=1,frames_indices=ix)],do_sample_frames=False,do_resize=False,return_tensors='pt')
    c.validate_inputs(request,(),kwargs(),2);check('valid_preflight',True)
    for label,mutate in [('batch2',lambda k:k.update(videos=k['videos']*2)),('frames47',lambda k:k.update(videos=[SimpleNamespace(shape=(47,192,288,3))])),('metadata_missing',lambda k:k.update(video_metadata=[])),('sampling',lambda k:k.update(do_sample_frames=True)),('resize',lambda k:k.update(do_resize=True)),('missing_fps',lambda k:setattr(k['video_metadata'][0],'fps',None))]:
        k=kwargs();mutate(k);rejects(label,lambda x=k:c.validate_inputs(request,(),x,2))
    blocked=[]
    for label,fn in [('socket',lambda:socket.socket()),('dns',lambda:socket.getaddrinfo('localhost',80))]:
        try:fn()
        except PermissionError:blocked.append(label)
        else:raise AssertionError('NETWORK_GUARD')
    canary=root/'owned-weight-denial-canary.safetensors';canary.write_bytes(b'')
    rejects('weight_body_guard',lambda:canary.read_bytes());check('network_guard',len(blocked)==2)
    rejects('optional_decoder_import_unavailable',lambda:__import__('av'),(ImportError,))
    c.write(root/'suite.json',dict(status='PASS',assertions=checks,processor_calls=0,guard_blocked=blocked))

def validate_formal(receipts,states,torch,tokenizer):
    refs=dict(Q01='Q01',Q02='Q01',Q03='Q01',Q04='Q03',Q05='Q04',Q06='Q03',Q07='Q04',Q08='Q01',Q09='Q08')
    inequalities={'Q04','Q05'};byid={x['slot']:x for x in receipts};out=[]
    for slot,path,table in c.SLOTS:
        r=byid[slot];failed=[];unknown=[]
        if r['state']!='EXECUTED':out.append(dict(**r,status='FAIL',failed=['PROCESSOR_CALL_FAILED']));continue
        def check(label,ok):
            if not ok:failed.append(label)
        reference=refs[slot];ref=byid.get(reference)
        expected=oracle_times(table if path=='P' else 'CFR');expected_codes=[f'{float(t):.1f}' for t in expected]
        check('grid_tokens',r['grid']==[[24,12,18]] and r['visual_tokens']==1296)
        check('actual_callback',len(r['callback'])==1 and r['callback'][0]['indices']==oracle_indices() and r['callback'][0]['fps']==1 and r['callback'][0]['merge_size']==2)
        check('independent_raw_means',r['raw_times']==[float(t) for t in expected]);check('native_format',r['native_timecodes']==expected_codes)
        check('request_scope',len(r['request_trace'])==(1 if path=='P' else 0))
        check('base_config_unchanged',r['base_class_unchanged'] and r['base_identity_before']==r['base_identity_after'])
        state=states[slot];check('CPU_BF16',state['pixel_values_videos'].device.type=='cpu' and state['pixel_values_videos'].dtype==torch.bfloat16)
        round_ids=tokenizer.encode(r['decoded'],add_special_tokens=False)
        roundtrip=round_ids==r['input_ids'] and tokenizer.decode(round_ids,skip_special_tokens=False,clean_up_tokenization_spaces=False)==r['decoded']
        if not roundtrip:unknown.append('TEXT_DIFFERENCE_UNKNOWN_ROUNDTRIP')
        nonvisual=set(state)-c.VISUAL
        text_only=bool(roundtrip and ref and ref.get('state')=='EXECUTED' and r['without_timecodes']==ref['without_timecodes'] and nonvisual=={'input_ids','attention_mask'} and state['attention_mask'].shape==state['input_ids'].shape and torch.all(state['attention_mask']==1).item())
        if not text_only:unknown.append('TEXT_DIFFERENCE_UNKNOWN')
        if reference not in states:failed.append('REFERENCE_FAILED');full=visual=False;raw_delta=quant_delta=[]
        else:
            full=c.equal(state,states[reference],torch);visual=c.equal(state,states[reference],torch,set(state)&c.VISUAL)
            check('direct_visual_grid_equal',visual);check('direct_full_relation',full==(slot not in inequalities))
            check('full_hash_agrees',bool(r['full_hash']==ref['full_hash'])==full)
            raw_delta=[a-b for a,b in zip(r['raw_times'],ref['raw_times'])]
            quant_delta=[float(a)-float(b) for a,b in zip(r['native_timecodes'],ref['native_timecodes'])]
        out.append(dict(**r,status='FAIL' if failed else 'BOUNDARY_HOLD' if unknown else 'PASS',failed=failed,unknown=unknown,reference=reference,direct_full_equal=full,direct_visual_equal=visual,text_only_difference='PASS' if text_only else 'TEXT_DIFFERENCE_UNKNOWN',roundtrip_equal=roundtrip,raw_delta=raw_delta,quantized_delta=quant_delta,raw_oracle=[str(t) for t in expected],quantization_error=[float(a)-float(b) for a,b in zip(r['native_timecodes'],expected)]))
    return out

if __name__=='__main__':suite(sys.argv[1])
