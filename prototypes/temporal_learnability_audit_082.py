"""082 CPU-only read-only cache audit. No predictor is instantiated or replayed.

All feature operations below are descriptive tensor statistics, never learned
weight projection. Separate count oracle does not call the production helper.
Private manifests locate inputs; only aggregate evidence may be published.
"""
import os,sys,time,json,hashlib,io,itertools,collections,ast,importlib.util
from pathlib import Path
PERMS=list(itertools.permutations(range(3)))
PAIRS=list(itertools.permutations(range(3),2))
SEEDS=(19,73,101,137,181,229)
SPLITS={'train':list(range(20)),'development':list(range(20,24)),'test':list(range(24,32))}
CAP=256*1024**2
def check(x,why):
 if not x:raise ValueError(why)
def dump(p,x):
 with p.open('xb') as f:f.write((json.dumps(x,sort_keys=True,allow_nan=False)+'\n').encode('utf-8'));f.flush();os.fsync(f.fileno())
def h(b):return hashlib.sha256(b).hexdigest()
def pack(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode('utf-8')
def raw(t):return t.detach().contiguous().view(__import__('torch').uint8).numpy().tobytes()
def exact(t):return pack({'dtype':str(t.dtype),'shape':list(t.shape)})+b'\0'+raw(t)
class Reader:
 def __init__(self,source,root):self.s=source.resolve();self.r=root;self.cache={};self.digests={};self.tensors={};self.total=0;self.allow=set();self.reserved=0
 def grant(self,p):
  p=Path(p).resolve();check(p.is_relative_to(self.s),'PATH_OUTSIDE_REGISTERED_081');check(not any(x in p.parts for x in ('pixels','blocks','tokens','media','parts','model')),'FORBIDDEN_PAYLOAD');self.allow.add(p);return p
 def get(self,p):
  p=Path(p).resolve();check(p in self.allow,'UNREGISTERED_FILE')
  if p not in self.cache:
   n=p.stat().st_size;check(len(self.cache)<512 and self.total+n<=CAP,'READ_BUDGET')
   with (self.r/'read-ledger.jsonl').open('ab') as f:f.write(pack(dict(event='RESERVED',file=str(p),bytes=n))+b'\n');f.flush();os.fsync(f.fileno())
   b=p.read_bytes();check(len(b)==n,'SOURCE_SIZE_CHANGED');self.total+=len(b);self.cache[p]=b;self.digests[p]=h(b)
   with (self.r/'read-ledger.jsonl').open('ab') as f:f.write(pack(dict(event='CLOSED',file=str(p),bytes=n,sha256=self.digests[p]))+b'\n');f.flush();os.fsync(f.fileno())
  return self.cache[p]
 def meta(self,name):return json.loads(self.get(self.grant(self.s/name)).decode('utf-8-sig'))
 def tensor(self,rec,t):
  path=self.grant(rec['path']);b=self.get(path);check(self.digests[path]==rec['sha256'] and len(b)==rec['bytes'],'SEALED_TENSOR_IDENTITY')
  if path not in self.tensors:self.tensors[path]=t.load(io.BytesIO(b),map_location='cpu',weights_only=True)
  return self.tensors[path]
def tensor_stats(x,t):
 return dict(shape=list(x.shape),dtype=str(x.dtype),finite=bool(t.isfinite(x).all()),l2=float(t.linalg.vector_norm(x.double())),max_abs=float(x.abs().max()))
def difference(a,b,t):
 d=a.double()-b.double();return dict(equal=raw(a)==raw(b),changed_elements=int((a!=b).sum()),l2=float(t.linalg.vector_norm(d)),max_abs=float(d.abs().max()),relative_l2=float(t.linalg.vector_norm(d)/t.linalg.vector_norm(b.double()).clamp_min(1e-300)))
def interval(xs):return dict(min=min(xs),max=max(xs),count=len(xs)) if xs else dict(min=None,max=None,count=0)
def metric_oracle(rows,truth,gs):
 vals={(x['group'],x['permutation'],x['question']):x for x in rows};check(len(vals)==36*len(gs),'ORACLE_KEY_COUNT');out=collections.Counter()
 for g in gs:
  ok={(p,q):vals[g,p,q]['prediction']==truth[g,p,q] and vals[g,p,q]['status']=='CLOSED' for p,q in itertools.product(range(6),repeat=2)}
  out['items']+=sum(ok.values());out['native']+=sum(all(ok[p,q] for q in range(6)) for p in range(6));out['sources']+=all(ok.values())
  for pi,p in enumerate(PERMS):
   for swap in (0,1):
    z=list(p);z[swap],z[swap+1]=z[swap+1],z[swap];pj=PERMS.index(tuple(z))
    if pj<pi:continue
    for qi,qrev in ((0,2),(1,4),(3,5)):
     good=all(ok[k] for k in ((pi,qi),(pi,qrev),(pj,qi),(pj,qrev)));out['quartets']+=good;out['FLIP' if truth[g,pi,qi]!=truth[g,pj,qi] else 'HOLD']+=good
 return out
def response_oracle(real,c1,c2,truth,gs):
 index=lambda xs:{(x['group'],x['permutation'],x['question']):x['prediction'] for x in xs}
 a,b,c=map(index,(real,c1,c2));out=collections.Counter()
 for g,q in itertools.product(gs,range(6)):
  answers=[a[g,p,q] for p in range(6)];sensitive=any(v!=answers[0] for v in answers[1:]);correct=sum(a[g,p,q]==truth[g,p,q] for p in range(6));out['permutation_sensitive_views' if sensitive else 'permutation_invariant_views']+=1;out['correct_sensitive_items' if sensitive else 'correct_invariant_items']+=correct
  if not sensitive:check(correct==3,'INDEPENDENT_BALANCE_IDENTITY')
 for key in a:
  out['real_control1_agree_items']+=a[key]==b[key];out['real_control2_agree_items']+=a[key]==c[key];out['control1_control2_agree_items']+=b[key]==c[key]
 return out
def audit(r):
 start=time.monotonic();os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch as t
 t.set_num_threads(4);t.set_num_interop_threads(1);check(not t.cuda.is_initialized(),'CUDA_INITIALIZED_BEFORE')
 parent=json.loads((r/'parent.json').read_text(encoding='utf-8'));s=Path(parent['source_root']);a=Reader(s,r);binding_checks=0;independent_checks=0
 def demand(v,why):
  nonlocal binding_checks;binding_checks+=1;check(v,why)
 spec=importlib.util.spec_from_file_location('arithmetic082',r/'response.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 # One tiny fixture uses only synthetic closed values; no learned computation.
 fixture=[dict(group=0,permutation=p,question=q,yes=int(PERMS[p].index(PAIRS[q][0])<PERMS[p].index(PAIRS[q][1])),prediction=0,status='CLOSED') for p,q in itertools.product(range(6),repeat=2)]
 f=helper.response_summary(fixture,fixture,fixture,fixture,[0]);check(f['permutation_invariant_views']==6 and f['correct_items']==18,'HELPER_NONLIVE_FIXTURE')
 obs=a.meta('observations.json');truthrows=a.meta('truth.json');relations=a.meta('relations.json');prepared=a.meta('prepared-index.json');plan=a.meta('inference-plan.json');fi=a.meta('feature-index.json');gpu=a.meta('gpu-output-seal.json');ps=a.meta('prediction-seal.json');ts=a.meta('training-seal.json');fp=a.meta('feature-pack-seal.json');tm=a.meta('train/manifest.json');pi=a.meta('prediction-input-index.json');base=a.meta('baseline-outputs.json');heads=a.meta('head-outputs.json');roots=a.meta('unique-root-results.json');agg=a.meta('aggregate-results.json');source_stats=a.meta('source-statistics.json');pres=a.meta('prepared-seal.json');code1=a.meta('all-code-seals.json');code2=a.meta('all-code-seals-v2.json')
 demand(h(a.get(a.s/'baseline-outputs.json'))==gpu['outputs_sha256'],'BASE_OUTPUT_IDENTITY');demand(h(a.get(a.s/'unique-root-results.json'))==gpu['root_results_sha256'],'ROOT_OUTPUT_IDENTITY');demand(h(a.get(a.s/'feature-index.json'))==gpu['features_sha256'],'FEATURE_INDEX_IDENTITY');demand(h(a.get(a.s/'head-outputs.json'))==ps['outputs_sha256'],'HEAD_OUTPUT_IDENTITY');demand(h(a.get(a.s/'prepared-index.json'))==pres['index_sha256'],'PREPARED_INDEX_IDENTITY')
 truth={(g,p,q):int(PERMS[p].index(left)<PERMS[p].index(right)) for g in range(32) for p in range(6) for q,(left,right) in enumerate(PAIRS)}
 actualtruth={(x['group'],x['permutation'],x['question']):x['yes'] for x in truthrows};demand(actualtruth==truth and len(truthrows)==1152,'TRUTH_AXES')
 for g,p,q in truth:
  demand(truth[g,p,q]+truth[g,p,PAIRS.index(PAIRS[q][::-1])]==1,'QUESTION_TAU_COMPLEMENT')
 relationkeys=set()
 for rel in relations:
  g,p,pj,q=(rel[k] for k in ('group','left','right','question'));delta=truth[g,pj,q]-truth[g,p,q];demand((g,p,pj,q) not in relationkeys and rel['difference']==delta and rel['relation']==('FLIP' if delta else 'HOLD'),'RELATION_TRUTH');relationkeys.add((g,p,pj,q))
 demand(len(relations)==2304,'RELATION_COUNT')
 import re
 for o in obs:
  parsed=[re.fullmatch(r'Does the event "(.*)" happen before the event "(.*)"\? Answer Yes or No\.',q) for q in o['questions']];demand(all(parsed),'LITERAL_QUESTION_TEMPLATE');events={}
  for pair,m in zip(PAIRS,parsed):
   for slot,event in zip(pair,m.groups()):
    if slot in events:demand(events[slot]==event,'LITERAL_ROLE_DIRECTION')
    else:events[slot]=event
 VQ=a.tensor(pi,t);train=a.tensor(tm['training'],t);V,Q=VQ['V'],VQ['Q'];demand(tuple(V.shape)==(32,6,18,2560) and tuple(Q.shape)==(32,6,2560),'BUNDLE_AXES')
 demand(pi==fp['prediction'] and tm['training']==fp['train'],'PACK_MANIFEST_LINKS');demand(set(train)=={'V','Q','Y'} and set(VQ)=={'V','Q','BLACK','TRAIN_MEAN'},'LABEL_ISOLATION_SCHEMA')
 demand(raw(train['V'])==raw(V[:20]) and raw(train['Q'])==raw(Q[:20]),'TRAIN_FEATURE_SUBSET');demand(all(float(train['Y'][g,p,q])==truth[g,p,q] for g,p,q in itertools.product(range(20),range(6),range(6))),'TRAIN_LABEL_SUBSET')
 demand(raw(V[:20].reshape(120,18,2560).double().sum(0).div(120).float())==raw(VQ['TRAIN_MEAN']),'TRAIN_MEAN_BINDING')
 capturedV={k:a.tensor(rec,t) for k,rec in fi['v'].items()};capturedQ={k:a.tensor(rec,t) for k,rec in fi['q'].items()};demand(len(capturedV)==193 and len(capturedQ)==138,'FEATURE_COUNTS')
 for x in list(capturedV.values())+list(capturedQ.values())+[V,Q]:demand(x.dtype==t.float32 and bool(t.isfinite(x).all()),'FEATURE_DTYPE_FINITE')
 demand(all(tuple(x.shape)==(18,2560) for x in capturedV.values()) and all(tuple(x.shape)==(2560,) for x in capturedQ.values()),'CAPTURED_SHAPES')
 demand(raw(capturedV[fi['black_pixel_key']])==raw(VQ['BLACK']),'BLACK_FEATURE_BINDING')
 rows=prepared['matrix'];realmap={(x['group'],x['permutation'],x['question']):x for x in rows if x['condition']=='REAL'};textmap={(x['group'],x['question']):x for x in rows if x['condition']=='TEXT'};qdict={};qtoken={};nonpixel=0
 for g,p,q in itertools.product(range(32),range(6),range(6)):
  x=realmap[g,p,q];qt=obs[g]['questions'][q];tk=textmap[g,q]['token_key'];demand(raw(V[g,p])==raw(capturedV[x['pixel_key']]),'V_PIXEL_KEY_BINDING');demand(raw(Q[g,q])==raw(capturedQ[tk]),'Q_TEXT_TOKEN_KEY_BINDING');demand(obs[g]['group']==g and obs[g]['split']==('train' if g<20 else 'development' if g<24 else 'test'),'SOURCE_SPLIT_BINDING')
  if qt in qdict:demand(qdict[qt]==exact(Q[g,q]) and qtoken[qt]==tk,'CROSS_SOURCE_LITERAL_Q_BINDING')
  else:qdict[qt]=exact(Q[g,q]);qtoken[qt]=tk
 demand(len(realmap)==1152 and len(qdict)==138,'ALL_MATRIX_KEYS')
 # Original logical identities and alias decisions are checked, not re-created.
 uid={x['uid']:x for x in roots};bind={(x['condition'],x['group'],x['permutation'],x['question']):x['uid'] for x in plan['logical']};seen=set()
 for x in base:
  key=(x['condition'],x['group'],x['permutation'],x['question']);u=bind[key];demand(x['uid']==u and x['prediction']==uid[u]['prediction'] and x['status']=='CLOSED','B0_ALIAS_OUTPUT_BINDING');demand(x['kind']==('ALIAS' if u in seen else 'NEW'),'B0_ALIAS_KIND');seen.add(u)
 demand(len(base)==3456 and len(heads)==62208 and len(uid)==1428 and len(bind)==3456,'PREDICTION_COUNTS');demand(sum(x['kind']=='NEW' for x in heads)==ps['actual_new']==25704,'HEAD_NEW_COUNT');demand(all(x['status']=='CLOSED' for x in heads),'HEAD_CLOSED');demand(len({(x['arm'],x['seed'],x['condition'],x['group'],x['permutation'],x['question']) for x in heads})==62208,'HEAD_UNIQUE_KEYS')
 # CPU feature-only statistics and exact contradiction limits.
 feature_report={};vbytes={(g,p):exact(V[g,p]) for g,p in itertools.product(range(32),range(6))};qbytes={(g,q):exact(Q[g,q]) for g,q in itertools.product(range(32),range(6))}
 for split,gs in {**SPLITS,'all':list(range(32))}.items():
  align=[];means=[];ordered=[]
  for g in gs:
   canonical=V[g,0]
   for p,perm in enumerate(PERMS):
    inv=[perm.index(k) for k in range(3)];aligned=V[g,p].reshape(3,6,2560)[inv].reshape(18,2560)
    if p:align.append(difference(aligned,canonical,t));means.append(difference(V[g,p].mean(0),canonical.mean(0),t))
   ordered.append(len({vbytes[g,p] for p in range(6)}))
  qs={obs[g]['questions'][q] for g,q in itertools.product(gs,range(6))};qtaus=[]
  for g in gs:
   for q,rev in ((0,2),(1,4),(3,5)):
    x,y=Q[g,q].double(),Q[g,rev].double();qtaus.append(dict(equal=qbytes[g,q]==qbytes[g,rev],relative_l2=float(t.linalg.vector_norm(x-y)/t.linalg.vector_norm(y).clamp_min(1e-300)),cosine=float(t.dot(x,y)/(t.linalg.vector_norm(x)*t.linalg.vector_norm(y)).clamp_min(1e-300))))
  feature_inputs={(g,p,q):(vbytes[g,p],qbytes[g,q]) for g,p,q in itertools.product(gs,range(6),range(6))};subtruth=[x for x in truthrows if x['group'] in gs];limits=helper.exact_feature_collision_limits(feature_inputs,subtruth,gs)
  # Separate exact-byte class oracle, without calling the helper.
  counts={};local={g:{} for g in gs}
  for key,features in feature_inputs.items():
   labels=counts.setdefault(features,[0,0]);labels[truth[key]]+=1;local[key[0]].setdefault(features,set()).add(truth[key])
  independent_limits=dict(unique_exact_inputs=len(counts),conflicting_exact_input_classes=sum(all(x) for x in counts.values()),deterministic_item_correct_upper=sum(max(x) for x in counts.values()),within_source_impossible36_groups=sum(any(len(z)>1 for z in m.values()) for m in local.values()))
  for key,val in independent_limits.items():demand(limits[key]==val,'INDEPENDENT_EXACT_CLASS_ORACLE');independent_checks+=1
  feature_report[split]=dict(source_groups=len(gs),ordered_V_unique=sum(ordered),ordered_unique_per_source=interval(ordered),canonical_block_aligned_comparisons=len(align),canonical_block_aligned_exact_equal=sum(x['equal'] for x in align),canonical_aligned_max_abs=interval([x['max_abs'] for x in align]),canonical_aligned_relative_l2=interval([x['relative_l2'] for x in align]),temporal_mean_exact_equal=sum(x['equal'] for x in means),temporal_mean_max_abs=interval([x['max_abs'] for x in means]),temporal_mean_relative_l2=interval([x['relative_l2'] for x in means]),literal_q_unique=len(qs),raw_q_unique=len({qdict[q] for q in qs}),different_literal_q_feature_collision_classes=sum(len(z)>1 for z in collections.defaultdict(set).values()),q_tau_pairs=len(qtaus),q_tau_exact_collision=sum(z['equal'] for z in qtaus),q_tau_relative_l2=interval([z['relative_l2'] for z in qtaus]),q_tau_cosine=interval([z['cosine'] for z in qtaus]),exact_input_limits=limits)
  classes=collections.defaultdict(set)
  for q in qs:classes[qdict[q]].add(q)
  feature_report[split]['different_literal_q_feature_collision_classes']=sum(len(v)>1 for v in classes.values())
 blackbytes=exact(VQ['BLACK']);meanbytes=exact(VQ['TRAIN_MEAN']);headseen={};headpred={}
 for x in heads:
  cfg=(x['seed'],x['arm']);vb=vbytes[x['group'],x['permutation']] if x['condition']=='REAL' else blackbytes if x['condition']=='BLACK' else meanbytes;key=(vb,qbytes[x['group'],x['question']]);seen=headseen.setdefault(cfg,set());previous=headpred.setdefault(cfg,{})
  demand(x['kind']==('ALIAS' if key in seen else 'NEW'),'HEAD_EXACT_ALIAS_KIND')
  if key in previous:demand(previous[key]==x['prediction'],'HEAD_EXACT_ALIAS_DECISION')
  else:previous[key]=x['prediction']
  seen.add(key)
 coverage={}
 trainqs={obs[g]['questions'][q] for g,q in itertools.product(SPLITS['train'],range(6))}
 for split,gs in SPLITS.items():
  qs={obs[g]['questions'][q] for g,q in itertools.product(gs,range(6))};coverage[split]=dict(unique_literal_questions=len(qs),seen_in_train_unique=len(qs&trainqs),unseen_in_train_unique=len(qs-trainqs),question_views_seen_in_train=sum(obs[g]['questions'][q] in trainqs for g,q in itertools.product(gs,range(6))))
 # 57 response rows and independent reductions for every original aggregate row.
 diag=[];disagreements=[]
 for split,gs in SPLITS.items():
  for arm,seed in [('B0',None)]+[(arm,seed) for arm in ('A','I','S') for seed in SEEDS]:
   orig=base if arm=='B0' else [x for x in heads if x['arm']==arm and x['seed']==seed];conds=('REAL','BLACK','TEXT' if arm=='B0' else 'TRAIN_MEAN');sub=[[x for x in orig if x['group'] in gs and x['condition']==c] for c in conds];summ=helper.response_summary(*sub,[x for x in truthrows if x['group'] in gs],gs);oracle=response_oracle(*sub,truth,gs)
   for k,val in oracle.items():demand(summ[k]==val,'INDEPENDENT_RESPONSE');independent_checks+=1
   m=metric_oracle(sub[0],truth,gs)
   for k,val in (('correct_items',m['items']),('source36_correct',m['sources'])):demand(summ[k]==val,'RESPONSE_METRIC_MATCH')
   diag.append(dict(split=split,method=arm,seed=seed if seed is not None else 'single',planned_sources=len(gs),actual_sources=len({x['group'] for x in sub[0]}),planned_items=36*len(gs),actual_items=len(sub[0]),planned_views=6*len(gs),actual_views=summ['source_question_views'],closed_items=sum(x['status']=='CLOSED' for x in sub[0]),actual_new=sum(x['kind']=='NEW' for x in sub[0]),aliases=sum(x['kind']=='ALIAS' for x in sub[0]),correct_items=summ['correct_items'],source36_correct=summ['source36_correct'],correct_FLIP=m['FLIP'],correct_HOLD=m['HOLD'],permutation_sensitive_views=summ['permutation_sensitive_views'],permutation_invariant_views=summ['permutation_invariant_views'],correct_invariant_items=summ['correct_invariant_items'],correct_sensitive_items=summ['correct_sensitive_items'],control1='BLACK',control2=conds[2],real_control1_agree_items=summ['real_control1_agree_items'],real_control2_agree_items=summ['real_control2_agree_items'],control1_control2_agree_items=summ['control1_control2_agree_items']))
  for seed in SEEDS:
   ix={arm:{(x['group'],x['permutation'],x['question']):x['prediction'] for x in heads if x['arm']==arm and x['seed']==seed and x['condition']=='REAL' and x['group'] in gs} for arm in ('A','I','S')}
   disagreements.append(dict(split=split,seed=seed,items=36*len(gs),**{left+'-'+right:sum(ix[left][k]!=ix[right][k] for k in ix[left]) for left,right in (('I','A'),('I','S'),('A','S'))}))
 for row in agg['baseline']+agg['heads']:
  ishead='arm' in row;gs=SPLITS[row['split']];rs=[x for x in (heads if ishead else base) if x['group'] in gs and x['condition']==row['condition'] and (not ishead or (x['arm'],x['seed'])==(row['arm'],row['seed']))];m=metric_oracle(rs,truth,gs)
  for k in ('items','native','sources','quartets','FLIP','HOLD'):demand(m[k]==row['correct_'+k],'ORIGINAL_AGGREGATE_REDUCTION');independent_checks+=1
  demand(len(rs)==row['closed']==row['planned_items'] and row['unknown']==0 and row['actual_new']+row['aliases']==len(rs),'ORIGINAL_AGGREGATE_DENOMINATOR')
 sourcecorrect={}
 for arm,seed,split in itertools.product(('A','I','S'),SEEDS,SPLITS):
  gs=SPLITS[split];xs=[x for x in heads if x['arm']==arm and x['seed']==seed and x['condition']=='REAL' and x['group'] in gs]
  for g in gs:sourcecorrect[arm,seed,split,g]=int(metric_oracle([x for x in xs if x['group']==g],truth,[g])['sources'])
 for row in agg['paired']:
  split=row['split'];gs=SPLITS[split];ss=SEEDS if row['seed']=='mean' else [row['seed']];vals=[(sourcecorrect['I',seed,split,g],sourcecorrect[row['right'],seed,split,g]) for seed,g in itertools.product(ss,gs)];left=sum(x for x,y in vals);right=sum(y for x,y in vals);corrected=sum(x==1 and y==0 for x,y in vals);harmed=sum(x==0 and y==1 for x,y in vals)
  demand((row['left_correct_sources'],row['right_correct_sources'],row['corrected'],row['harmed'],row['net'])==(left,right,corrected,harmed,left-right),'42_PAIRED_ORACLE');demand(abs(row['delta_pp']-100*(left-right)/(len(ss)*len(gs)))<1e-10 and row['independent_source_groups']==len(gs),'PAIRED_DENOMINATOR');independent_checks+=2
 # States, positional condition and losses, without network construction.
 state_records=[];state_diffs=[];loss_records=[];states={};initials={};ledger=[json.loads(line) for line in a.get(a.grant(s/'training-ledger.jsonl')).splitlines()];steps=collections.defaultdict(list)
 for x in ledger:steps[x['seed'],x['arm'],x['step']].append(x)
 demand(len(steps)==4500 and all([z['event'] for z in v]==['STARTED','CLOSED'] and v[1]['backward']==v[1]['optimizer_step']==1 for v in steps.values()),'ORIGINAL_4500_STEP_LEDGER')
 for config in ts['configs']:
  seed,arm=config['seed'],config['arm'];ini=a.tensor(config['initial'],t);final=a.tensor(config['state'],t);states[seed,arm]=final;initials[seed]=ini;demand(sum(x.numel() for x in final.values())==sum(x.numel() for x in ini.values())==341633,'STATE_PARAMETER_COUNT')
  diffs={k:{**difference(final[k],ini[k],t),'initial':tensor_stats(ini[k],t),'final':tensor_stats(final[k],t)} for k in final};pos=final['pos'];blocks=pos.reshape(3,6,64);position=dict(initial_all_zero=bool((ini['pos']==0).all()),final_finite=bool(t.isfinite(pos).all()),all_rows_exact_equal=all(raw(pos[k])==raw(pos[0]) for k in range(1,18)),three_blocks_exact_equal=raw(blocks[0])==raw(blocks[1])==raw(blocks[2]),changed_elements=int((pos!=ini['pos']).sum()),block_pair_differences=[difference(blocks[i],blocks[j],t) for i,j in ((0,1),(0,2),(1,2))]);state_records.append(dict(seed=seed,arm=arm,parameters=341633,changed_parameters=sum(z['changed_elements'] for z in diffs.values()),families=diffs,position=position))
  closed=[steps[seed,arm,k][1] for k in range(1,251)];demand(all(all(__import__('math').isfinite(x[k]) for k in ('loss','bce','relation')) for x in closed),'LOSS_FINITE')
  loss_records.append(dict(seed=seed,arm=arm,steps=250,samples={str(k):{n:closed[k-1][n] for n in ('loss','bce','relation')} for k in (1,10,50,100,250)},first10_mean={n:sum(x[n] for x in closed[:10])/10 for n in ('loss','bce','relation')},last10_mean={n:sum(x[n] for x in closed[-10:])/10 for n in ('loss','bce','relation')}))
 for seed in SEEDS:
  configs=[x for x in ts['configs'] if x['seed']==seed];demand(len({x['initial']['sha256'] for x in configs})==len({x['batch_sha256'] for x in configs})==1,'MATCHED_INITIAL_BATCH')
  for left,right in (('I','A'),('I','S'),('A','S')):
   families={k:difference(states[seed,left][k],states[seed,right][k],t) for k in states[seed,left]};state_diffs.append(dict(seed=seed,left=left,right=right,all_tensors_equal=all(x['equal'] for x in families.values()),delta_l2=float(sum(x['l2']**2 for x in families.values())**.5),families=families))
 # Clock exclusion: arithmetic is auditable; no existing explicit pause evidence is invented.
 clock={n:a.meta(n) for n in ('parent-clock.json','infra-repair-v2.json','train-started.json','train-job.json','predict-started.json','predict-job.json','control-predict-io.json','parent-closed.json')};v1=a.get(a.grant(s/'pipeline-v1.py')).decode('utf-8-sig');v2=a.get(a.grant(s/'pipeline.py')).decode('utf-8-sig');names={'head_class','relation','train','predict','metrics','scoring'}
 def funcs(source):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names}
 repair=clock['infra-repair-v2.json'];demand(funcs(v1)==funcs(v2),'CLOCK_REPAIR_SCIENCE_AST');demand(h(v1.replace('\r\n','\n').encode())==code1['files'][0]['lf_sha256'] and h(v2.replace('\r\n','\n').encode())==code2['files'][0]['lf_sha256'],'V1_V2_CODE_SEALS');demand(abs(repair['idle_end_epoch']-repair['idle_start_epoch']-60-repair['excluded_seconds'])<1e-5,'IDLE_ARITHMETIC');demand(clock['train-job.json']['active']==0 and clock['predict-started.json']['epoch']>repair['idle_end_epoch'] and clock['predict-job.json']['active']==0,'TRAIN_TO_PREDICT_CHAIN')
 closure=clock['parent-closed.json'];clock_public=dict(status='IDLE_EXCLUSION_UNVERIFIED / RAW_PARENT_CAP_EXCEEDED / CHARGED_ARITHMETIC_REPORTED',excluded_seconds=repair['excluded_seconds'],retained_overhead_seconds=60,prior_parent_seconds=closure['prior_parent_seconds'],raw081_final_seconds=closure['raw_wall_seconds'],charged081_final_seconds=closure['parent081_seconds'],raw_four_parent_seconds=closure['raw_wall_seconds']+closure['prior_parent_seconds'],charged_four_parent_seconds=closure['four_parent_executed_seconds'],new_parent_cap=12000,four_parent_cap=14400,explicit_preexisting_user_pause_evidence='NOT_PRESENT_IN_REGISTERED_CLOCK_RECORDS',clock_chain_arithmetic_pass=True,scientific_AST_unchanged=True,prediction_stage_started_once=True,limitation='Original failed launch stderr was not sealed separately; control receipt exists but active0 and file timestamps do not establish authorization to exclude idle time.')
 # Minimal separate inspection validates loss and position summaries from same cached tensors.
 for rec in state_records:
  pos=states[rec['seed'],rec['arm']]['pos'];independent=all(bool(t.equal(pos.reshape(3,6,64)[0],pos.reshape(3,6,64)[i])) for i in (1,2));demand(independent==rec['position']['three_blocks_exact_equal'],'INDEPENDENT_POSITION_EQUALITY');independent_checks+=1
 for rec in loss_records:
  for n in ('loss','bce','relation'):
   vals=[z[1][n] for key,z in sorted(steps.items()) if key[0]==rec['seed'] and key[1]==rec['arm']];demand(abs(sum(vals[-10:])/10-rec['last10_mean'][n])<1e-12,'INDEPENDENT_LOSS_REDUCTION');independent_checks+=1
 demand(len(diag)==57,'57_DIAGNOSTIC_ROWS');demand(not t.cuda.is_initialized(),'CUDA_INITIALIZED_AFTER')
 conclusions=['CACHE_INTEGRITY_PASS','CAUSE_UNRESOLVED']
 if any(feature_report[k]['exact_input_limits']['conflicting_exact_input_classes'] for k in feature_report):conclusions.append('EXACT_FEATURE_CONTRADICTION')
 # Joint empirical symmetry needs both exact feature equivariance and positional repetition.
 symmetry=feature_report['all']['canonical_block_aligned_exact_equal']==160 and all(x['position']['three_blocks_exact_equal'] for x in state_records)
 if symmetry:conclusions.append('POSITION_SYMMETRY_CONDITION_MET')
 report=dict(status='CACHE_DIAGNOSTIC_COMPLETE / NO_NEW_PREDICTION_OR_TRAINING / ORIGINAL_RECIPE_CLOSED',conclusions=conclusions,binding=dict(status='PASS',checks=binding_checks,groups=32,source_split=[20,4,8],truth_items=1152,relations=2304,captured_V=193,captured_q=138,training_subsets_bit_exact=True,V_pixel_keys_and_literal_q_token_keys_pass=True,all_output_identity_and_aggregate_rows_pass=True),features=feature_report,literal_coverage=coverage,decision_disagreement=disagreements,states=state_records,final_state_comparisons=state_diffs,losses=loss_records,stored_evidence=dict(head_continuous_logits='NOT_STORED',gradients='NOT_STORED',cannot_infer_zero_gradient_or_convergence=True),position_symmetry=dict(joint_empirical_condition_met=symmetry,algebra='In ideal real arithmetic, repeated P blocks and block-permuted V make query-attention pooling permutation invariant. Approximate equality or floating-point differences do not imply this exact condition or exact decision invariance.'),clock=clock_public,independent=dict(status='PASS',checks=independent_checks,production_helper_or_old_scorer_used_in_oracle=False,new_predictor_forward=0),resources=dict(source_files=len(a.cache),source_read_bytes=a.total,source_read_cap=CAP,source_file_cap=512,worker_seconds=time.monotonic()-start,CUDA_initialized=False,new_model_or_head_forward=0,training_updates=0,network_media_processor=0,explicit_read_scope='unique registered logical bytes; native/OS physical IO not certified'))
 dump(r/'diagnostic-private.json',report);dump(r/'diagnostic-rows.json',diag);dump(r/'read-summary.json',dict(files=len(a.cache),bytes=a.total,cap=CAP,all_files_hash_once=True,shared_bytecache=True));print(json.dumps(dict(status=report['status'],files=len(a.cache),bytes=a.total,checks=binding_checks,independent_checks=independent_checks,seconds=time.monotonic()-start)),flush=True)

# Native supervision classes are vendored below from the previously published
# Windows implementation; no historic scientific module is imported or executed.

import ctypes as C
from ctypes import wintypes as W
import subprocess
MIB=1024**2
def require(ok,reason):
    if not ok:raise ValueError(reason)

class Basic(C.Structure):
    _fields_=[('process_time',C.c_int64),('job_time',C.c_int64),('flags',W.DWORD),
              ('min_ws',C.c_size_t),('max_ws',C.c_size_t),('active_limit',W.DWORD),
              ('affinity',C.c_size_t),('priority',W.DWORD),('scheduling',W.DWORD)]

class IO(C.Structure):
    _fields_=[(n,C.c_uint64) for n in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]

class Extended(C.Structure):
    _fields_=[('basic',Basic),('io',IO),('process_memory',C.c_size_t),('job_memory',C.c_size_t),
              ('peak_process',C.c_size_t),('peak_job',C.c_size_t)]

class Accounting(C.Structure):
    _fields_=[('user',C.c_int64),('kernel',C.c_int64),('period_user',C.c_int64),('period_kernel',C.c_int64),
              ('faults',W.DWORD),('total',W.DWORD),('active',W.DWORD),('terminated',W.DWORD)]

class Startup(C.Structure):
    _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
              ('x',W.DWORD),('y',W.DWORD),('xsize',W.DWORD),('ysize',W.DWORD),('xchars',W.DWORD),
              ('ychars',W.DWORD),('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('reserved_size',W.WORD),
              ('reserved_ptr',C.POINTER(C.c_byte)),('stdin',W.HANDLE),('stdout',W.HANDLE),('stderr',W.HANDLE)]

class ProcessInfo(C.Structure):
    _fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]

def kernel():
    require(os.name=='nt','WINDOWS_ONLY')
    api=C.WinDLL('kernel32',use_last_error=True)
    signatures={
      'CreateJobObjectW':([W.LPVOID,W.LPCWSTR],W.HANDLE),
      'SetInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD],W.BOOL),
      'QueryInformationJobObject':([W.HANDLE,C.c_int,W.LPVOID,W.DWORD,W.LPVOID],W.BOOL),
      'AssignProcessToJobObject':([W.HANDLE,W.HANDLE],W.BOOL),
      'TerminateJobObject':([W.HANDLE,W.UINT],W.BOOL),
      'CloseHandle':([W.HANDLE],W.BOOL),
      'CreateProcessW':([W.LPCWSTR,W.LPWSTR,W.LPVOID,W.LPVOID,W.BOOL,W.DWORD,W.LPVOID,W.LPCWSTR,C.POINTER(Startup),C.POINTER(ProcessInfo)],W.BOOL),
      'ResumeThread':([W.HANDLE],W.DWORD),
      'GetExitCodeProcess':([W.HANDLE,C.POINTER(W.DWORD)],W.BOOL),
      'TerminateProcess':([W.HANDLE,W.UINT],W.BOOL),
      'OpenProcess':([W.DWORD,W.BOOL,W.DWORD],W.HANDLE),
      'IsProcessInJob':([W.HANDLE,W.HANDLE,C.POINTER(W.BOOL)],W.BOOL)}
    for name,(args,ret) in signatures.items():getattr(api,name).argtypes=args;getattr(api,name).restype=ret
    return api

class Job:
    def __init__(self,memory=512*MIB,active_limit=0):
        self.api=kernel();self.handle=self.api.CreateJobObjectW(None,None);require(self.handle,'JOB_CREATE')
        limits=Extended();limits.basic.flags=0x2000|0x100|0x200
        if active_limit:limits.basic.flags|=0x8;limits.basic.active_limit=active_limit
        limits.process_memory=limits.job_memory=memory
        require(self.api.SetInformationJobObject(self.handle,9,C.byref(limits),C.sizeof(limits)),'JOB_LIMITS')
        self.killed=False
    def assign(self,process):require(self.api.AssignProcessToJobObject(self.handle,process.handle),'JOB_ASSIGN')
    def snapshot(self):
        a=Accounting();e=Extended()
        require(self.api.QueryInformationJobObject(self.handle,1,C.byref(a),C.sizeof(a),None),'JOB_ACCOUNT')
        require(self.api.QueryInformationJobObject(self.handle,9,C.byref(e),C.sizeof(e),None),'JOB_MEMORY')
        return dict(active=a.active,total_processes=a.total,user_seconds=a.user/1e7,kernel_seconds=a.kernel/1e7,
                    peak_commit=e.peak_job,killed=self.killed)
    def active(self):return self.snapshot()['active']
    def empty(self,deadline):
        while self.active():
            if time.monotonic()>=deadline:return False
            time.sleep(.001)
        return True
    def kill(self):
        require(self.api.TerminateJobObject(self.handle,99),'OWN_JOB_TERMINATION');self.killed=True
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None

class Process:
    """CREATE_SUSPENDED -> assign Job -> ResumeThread, before Python user code."""
    def __init__(self,args,log,job=None):
        import msvcrt
        self.api=kernel();self.handle=None;self.pid=None
        si=Startup();si.cb=C.sizeof(si);si.flags=0x100
        pi=ProcessInfo();env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
        block=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
        command=C.create_unicode_buffer(subprocess.list2cmdline([str(x) for x in args]))
        with open(log,'xb') as output,open(os.devnull,'rb') as incoming:
            out=msvcrt.get_osfhandle(output.fileno());inp=msvcrt.get_osfhandle(incoming.fileno())
            os.set_handle_inheritable(out,True);os.set_handle_inheritable(inp,True)
            si.stdout=si.stderr=out;si.stdin=inp
            ok=self.api.CreateProcessW(None,command,None,None,True,0x08000000|0x4|0x400,block,None,C.byref(si),C.byref(pi))
            os.set_handle_inheritable(out,False);os.set_handle_inheritable(inp,False)
            require(ok,'CREATE_PROCESS_'+str(C.get_last_error()))
        self.handle,self.pid=pi.process,pi.pid
        try:
            if job is not None:job.assign(self)
            require(self.api.ResumeThread(pi.thread)!=0xffffffff,'RESUME_THREAD')
        except Exception:
            self.api.TerminateProcess(self.handle,98);raise
        finally:self.api.CloseHandle(pi.thread)
    @classmethod
    def registered(cls,pid,job):
        obj=cls.__new__(cls);obj.api=kernel();obj.pid=pid
        obj.handle=obj.api.OpenProcess(0x1000|0x100000,False,pid)
        require(obj.handle,'REGISTERED_PROCESS_OPEN')
        inside=W.BOOL();require(obj.api.IsProcessInJob(obj.handle,job.handle,C.byref(inside)) and inside.value,'REGISTERED_PROCESS_NOT_OWNED')
        return obj
    def poll(self):
        code=W.DWORD();require(self.api.GetExitCodeProcess(self.handle,C.byref(code)),'PROCESS_QUERY')
        return None if code.value==259 else code.value
    def wait(self,deadline):
        while self.poll() is None:
            if time.monotonic()>=deadline:raise TimeoutError('PROCESS_TIMEOUT')
            time.sleep(.001)
        return self.poll()
    def kill(self):require(self.api.TerminateProcess(self.handle,99),'OWN_PROCESS_TERMINATION')
    def close(self):
        if self.handle:self.api.CloseHandle(self.handle);self.handle=None





def supervise(r):
 start=time.monotonic();parent=json.loads((r/'parent.json').read_text(encoding='utf-8'));check(time.time()-parent['recorded_epoch']<3500,'PARENT_CLOCK')
 for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='4'
 os.environ['CUDA_VISIBLE_DEVICES']='';os.environ['TOKENIZERS_PARALLELISM']='false'
 job=Job(memory=4*1024**3,active_limit=8);limits=Extended();check(job.api.QueryInformationJobObject(job.handle,9,C.byref(limits),C.sizeof(limits),None),'READBACK');dump(r/'job-limits.json',dict(memory=limits.job_memory,active=limits.basic.active_limit,flags=limits.basic.flags));check(limits.job_memory==4*1024**3 and limits.basic.active_limit==8,'LIMITS')
 proc=Process([sys.executable,'-I','-B',str(Path(__file__)),str(r),'worker'],r/'worker.log',job);peak_active=0;peak_threads=0;stop=None
 class Thread(C.Structure):
  _fields_=[('size',W.DWORD),('use',W.DWORD),('tid',W.DWORD),('pid',W.DWORD),('base',W.LONG),('delta',W.LONG),('flags',W.DWORD)]
 api=job.api;api.CreateToolhelp32Snapshot.argtypes=[W.DWORD,W.DWORD];api.CreateToolhelp32Snapshot.restype=W.HANDLE;api.Thread32First.argtypes=[W.HANDLE,C.POINTER(Thread)];api.Thread32First.restype=W.BOOL;api.Thread32Next.argtypes=[W.HANDLE,C.POINTER(Thread)];api.Thread32Next.restype=W.BOOL
 try:
  while proc.poll() is None:
   acc=job.snapshot();peak_active=max(peak_active,acc['active']);buf=C.create_string_buffer(8+8*16);check(api.QueryInformationJobObject(job.handle,3,buf,len(buf),None),'PIDS');n=int.from_bytes(buf.raw[4:8],'little');check(n<=16,'PID_BUFFER');pids={int.from_bytes(buf.raw[8+8*i:16+8*i],'little') for i in range(n)};counts={p:0 for p in pids};snap=api.CreateToolhelp32Snapshot(4,0);entry=Thread();entry.size=C.sizeof(entry)
   try:
    ok=api.Thread32First(snap,C.byref(entry))
    while ok:
     if entry.pid in counts:counts[entry.pid]+=1
     ok=api.Thread32Next(snap,C.byref(entry))
   finally:api.CloseHandle(snap)
   peak_threads=max(peak_threads,max(counts.values(),default=0));files=[p for p in r.rglob('*') if p.is_file()]
   if time.monotonic()-start>299:stop='CPU_STATISTICS_300S'
   elif peak_active>8 or peak_threads>256:stop='OWN_PROCESS_OR_NATIVE_THREAD_CAP'
   elif len(files)>256 or sum(p.stat().st_size for p in files)>64*1024**2:stop='OUTPUT_CAP'
   elif time.time()-parent['recorded_epoch']>=3500:stop='PARENT_RECORDED_CLOCK'
   if stop:job.kill();break
   time.sleep(.02)
  code=proc.wait(time.monotonic()+5);check(job.empty(time.monotonic()+5),'JOB_NOT_EMPTY');result=job.snapshot();result.update(exit_code=code,outer_seconds=time.monotonic()-start,peak_sampled_active=peak_active,peak_sampled_native_threads=peak_threads,stop=stop,sampling_seconds=.02,coverage='own Job limits/readback; sampled threads; no full OS/physical IO certification');dump(r/'job-summary.json',result);print(json.dumps(result),flush=True)
 finally:proc.close();job.close()
 return 0 if code==0 and not stop else 1

def main():
 r=Path(sys.argv[1]);seal=json.loads((r/'code-seal.json').read_text(encoding='utf-8'));check(h(Path(__file__).read_bytes().replace(b'\r\n',b'\n'))==seal['audit_sha256'],'AUDIT_CODE_CHANGED');check(h((r/'response.py').read_bytes().replace(b'\r\n',b'\n'))==seal['helper_sha256'],'HELPER_CODE_CHANGED')
 if sys.argv[2]=='worker':audit(r)
 else:sys.exit(supervise(r))
if __name__=='__main__':main()
