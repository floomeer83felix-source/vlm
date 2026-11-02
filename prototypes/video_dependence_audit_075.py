"""075 explicit CPU audit. Import does not read data or initialize Torch.

Original predictions are reused. Only two fixed video-reference interventions
have learned-head calls; the 720 text orders use integer comparisons only.
"""
import argparse, collections, csv, hashlib, importlib.util, io, itertools, json
import math, os, re, time
from pathlib import Path

SEEDS=(137,263,419,557,733,911)
METHODS=('C_NATIVE','D_NATIVE','CONCAT','FACTOR','REVERSE','ANCHOR')
CONTROLS=('ORIGINAL_CACHED','GLOBAL_MEAN_V','ZERO_V')
PATTERN=r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.'
TEMPLATE='Does the event "{}" happen before the event "{}"? Answer Yes or No.'
MIB=1024**2

def packed(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,x):
 with open(p,'x',encoding='utf-8') as f:f.write(packed(x)+'\n');f.flush();os.fsync(f.fileno())
def event(p,**x):
 with open(p,'a',encoding='utf-8') as f:f.write(packed(dict(epoch=time.time(),**x))+'\n');f.flush();os.fsync(f.fileno())
def digest(p):return sha(Path(p).read_bytes())
def require(root,ok,reason,actual=None,limit=None):
 if not ok:
  event(Path(root)/'failures.jsonl',reason=reason,actual=actual,limit=limit)
  raise RuntimeError(reason)
def sealed(root):
 for x in read(Path(root)/'code-seal.json')['files']:assert sha(Path(x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256'],'CODE_CHANGED'
def cpu():
 os.environ['CUDA_VISIBLE_DEVICES']=''
 import torch
 torch.set_num_threads(4);torch.set_num_interop_threads(1);assert not torch.cuda.is_initialized();return torch
def helper(name):
 p=Path(__file__).with_name(name+'.py');spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def tau(q):
 m=re.fullmatch(PATTERN,q)
 if not m:raise ValueError('STRICT_QUESTION_PARSE')
 return TEMPLATE.format(m[2],m[1])
def words(q):
 m=re.fullmatch(PATTERN,q)
 if not m:raise ValueError('STRICT_QUESTION_PARSE')
 return m.groups()
def pair(q):return tuple(sorted(' '.join(x.replace('_',' ').split()).casefold() for x in words(q)))
def anchor(q,canonical):
 q=min(q,tau(q),key=lambda s:s.encode());start=int.from_bytes(hashlib.sha256(b'VLM070/c-anchor/'+q.encode()).digest()[:8],'big')%42
 return next(canonical[(start+i)%42] for i in range(42) if pair(canonical[(start+i)%42])!=pair(q))
def valid_orders(qs):
 events=sorted({x for q in qs for x in words(q)},key=lambda s:s.encode());assert len(events)==3 and len(qs)==6
 return {tuple(int(p.index(a)<p.index(b)) for a,b in map(words,qs)) for p in itertools.permutations(events)}
def fixture():
 qs=[TEMPLATE.format(a,b) for a,b in itertools.permutations(('alpha','beta','gamma'),2)];patterns=valid_orders(qs)
 assert len(patterns)==6 and all(sum(p)==3 for p in patterns)
 assert all(tau(tau(q))==q and tau(q) in qs for q in qs)
 cycle=(1,0,0,1,1,0);assert cycle not in patterns and all(cycle[i]+cycle[qs.index(tau(q))]==1 for i,q in enumerate(qs))
 return dict(status='PASS',integer_text_only=True,coherent_patterns=6,complementary_cycle_rejected=True,learned_forward=0)

class Access:
 """Bounded reads from the one authorized074root only, cached per role."""
 def __init__(self,root,role):self.root=Path(root);self.prior=Path(read(self.root/'parent.json')['prior074']).resolve();self.role=role;self.cache={};self.counts=collections.Counter();self.files=[]
 def data(self,p,kind='metadata',expected=None):
  p=Path(p).resolve();key=str(p);assert p.is_relative_to(self.prior),'OUTSIDE_AUTHORIZED_074'
  if key not in self.cache:
   b=p.read_bytes();self.cache[key]=b;self.counts[kind]+=len(b);self.files.append(dict(path=key,kind=kind,bytes=len(b),sha256=sha(b)))
   earlier=collections.Counter()
   for f in self.root.glob('*-access.json'):earlier.update(read(f)['counts'])
   for category,cap in [('feature',64*MIB),('state',128*MIB),('metadata',32*MIB)]:require(self.root,earlier[category]+self.counts[category]<=cap,'OLD_READ_LIMIT',dict(kind=category,bytes=earlier[category]+self.counts[category]),cap)
   (self.root/(self.role+'-access-progress.json')).write_text(packed(dict(counts=self.counts,files=self.files)),encoding='utf-8')
  b=self.cache[key]
  if expected:require(self.root,sha(b)==expected,'OLD_CONTENT_IDENTITY',p.name,'closed original identity')
  return b
 def meta(self,p,expected=None):return json.loads(self.data(p,'metadata',expected).decode('utf-8-sig'))
 def tensor(self,p,kind,expected):
  import torch
  return torch.load(io.BytesIO(self.data(p,kind,expected)),map_location='cpu',weights_only=True)
 def finish(self):save(self.root/(self.role+'-access.json'),dict(counts=self.counts,files=self.files))

def prepare(root):
 t=cpu();root=Path(root);sealed(root);save(root/'fixture.json',fixture());a=Access(root,'preparation');p=a.prior
 closure=a.meta(p/'parent-closed.json');assert closure['push']=='SUCCEEDED' and closure['all_jobs_actual_active_zero'] and closure['new_head_forwards']==5184
 for name in ('unpack','assets','decode','gpu','prediction','scoring','independent-review','closure-audit','package-closure-review'):
  j=a.meta(p/(name+'-job.json'));assert j['active']==j['exit_code']==0 and not j['killed']
 bootstrap=a.meta(p/'assets-bootstrap-job.json');assert bootstrap['active']==0 and bootstrap['exit_code']==1
 oldcode=a.meta(p/'code-seal.json')
 for name in ('question_temporal_056.py','semantic_role_factor_070.py'):
  rec=[x for x in oldcode['files'] if Path(x['path']).name==name];assert len(rec)==1
  assert sha(Path(__file__).with_name(name).read_bytes().replace(b'\r\n',b'\n'))==rec[0]['lf_sha256'],'ARCHITECTURE_IDENTITY'
 inp=a.meta(p/'input-seal.json');cat=a.meta(p/'asset-catalog.json',inp['assets']);obs=a.meta(p/'observations.json',inp['observations']);a.data(p/'prepared-inputs.json','metadata',inp['prepared_inputs'])
 fs=a.meta(p/'feature-seal.json');ix=a.meta(p/'feature-index.json',fs['index_sha256']);ps=a.meta(p/'prediction-seal.json');ob=a.data(p/'outputs.json','metadata',ps['output_sha256']);outputs=json.loads(ob)
 assert len(outputs)==5184 and len({(x['method'],x['seed'],x['index'],x['question']) for x in outputs})==5184 and all(x['status']=='CLOSED' and type(x['prediction']) is int and x['prediction'] in (0,1) and math.isfinite(x['logit']) and x['prediction']==int(x['logit']>0) for x in outputs)
 oldledger=a.data(p/'prediction-ledger.jsonl');lr=[json.loads(x) for x in oldledger.decode().splitlines()];assert [x['key'] for x in lr if x['event']=='STARTED']==[x['key'] for x in lr if x['event']=='CLOSED'] and len(lr)==10368
 assert len(obs)==24 and [x['index'] for x in obs]==list(range(24))
 qs=sorted({q for x in obs for q in x['questions']},key=lambda q:q.encode());assert len(qs)==28 and set(qs)==set(ix['text']) and set(ix['video'])=={str(i) for i in range(24)}
 assert all(tau(q) in qs and tau(tau(q))==q for q in qs)
 V=[a.tensor(ix['video'][str(i)]['path'],'feature',ix['video'][str(i)]['sha256']) for i in range(24)]
 Q={q:a.tensor(ix['text'][q]['path'],'feature',ix['text'][q]['sha256']) for q in qs}
 assert all(v.shape==(6,2560) and v.dtype==t.float32 and t.isfinite(v).all() for v in V) and all(v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all() for v in Q.values())
 stats_bytes=a.data(p/'frozen-statistics.pt','state',cat['statistics_sha256']);stats=t.load(io.BytesIO(stats_bytes),map_location='cpu',weights_only=True)
 for st in (stats['normalizer']['C_CENTER'],stats['normalizer']['D_ROLE'],stats['S_normalizer']):assert st['mu'].shape==(2560,) and st['mu'].dtype==t.float64 and st['scale'].shape==() and st['scale'].dtype==t.float64 and t.isfinite(st['mu']).all() and t.isfinite(st['scale']) and st['scale']>1e-8
 canonical=stats['canonical'];assert len(canonical)==len(set(canonical))==42 and canonical==sorted(canonical,key=lambda q:q.encode())
 assert set(stats['anchor_S'])==set(canonical) and all(v.shape==(2560,) and v.dtype==t.float32 and t.isfinite(v).all() for v in stats['anchor_S'].values())
 C={q:((v.double()-stats['normalizer']['C_CENTER']['mu'])/stats['normalizer']['C_CENTER']['scale']).float() for q,v in Q.items()}
 R={q:(((v.double()-Q[tau(q)].double())/2-stats['normalizer']['D_ROLE']['mu'])/stats['normalizer']['D_ROLE']['scale']).float() for q,v in Q.items()}
 S={q:(((v.double()+Q[tau(q)].double())/2-stats['S_normalizer']['mu'])/stats['S_normalizer']['scale']).float() for q,v in Q.items()};anchors={q:anchor(q,canonical) for q in qs};A={q:stats['anchor_S'][anchors[q]] for q in qs}
 accumulator=t.zeros((6,2560),dtype=t.float64)
 for i in range(24):accumulator+=V[i].double()
 refs={'GLOBAL_MEAN_V':(accumulator/24).float(),'ZERO_V':t.zeros((6,2560),dtype=t.float32)}
 vocab=sorted({w for q in qs for w in words(q)},key=lambda w:w.encode());triples={tuple(sorted({w for q in x['questions'] for w in words(q)},key=lambda w:w.encode())) for x in obs};assert len(vocab)==6 and len(triples)==12
 assert all(len(valid_orders(x['questions']))==6 for x in obs)
 save(root/'observations.json',[dict(index=x['index'],questions=x['questions']) for x in obs]);save(root/'questions.json',qs)
 (root/'original-outputs.json').write_bytes(ob);(root/'frozen-statistics.pt').write_bytes(stats_bytes)
 newheads=[]
 assert len(cat['heads'])==36 and {(x['method'],x['seed']) for x in cat['heads']}==set(itertools.product(METHODS,SEEDS))
 shapes={'video.weight':(64,2560),'video.bias':(64,),'question.weight':(64,2560),'question.bias':(64,),'conv.weight':(64,64,3),'conv.bias':(64,),'mlp.0.weight':(64,256),'mlp.0.bias':(64,),'mlp.2.weight':(1,64),'mlp.2.bias':(1,)}
 for x in sorted(cat['heads'],key=lambda x:(METHODS.index(x['method']),SEEDS.index(x['seed']))):
  source=Path(x['path']).resolve();assert source.is_relative_to(p.resolve()) and source.is_file()
  newheads.append(dict(method=x['method'],seed=x['seed'],path=str(source),sha256=x['sha256']))
 t.save(dict(V=V,Q=Q,C=C,R=R,S=S,A=A,anchors=anchors,refs=refs),root/'inputs.pt');save(root/'heads.json',newheads)
 # Only derived labels/manifest are registered here; actual labels are read by
 # the scorer after both learned and integer predictions have closed.
 gate=a.meta(p/'gate.json');members=gate['metadata_members'];label_member=next(n for n in members if Path(n).name=='labels.json');manifest=next(n for n in members if Path(n).name=='source-package-manifest.json')
 save(root/'scoring-registration.json',dict(root_labels=str(p/'scoring-labels.json'),handed_labels=str(p/'package'/label_member),handed_manifest=str(p/'package'/manifest),member=label_member))
 records=[]
 for name in ('observations.json','questions.json','original-outputs.json','frozen-statistics.pt','inputs.pt','heads.json','scoring-registration.json'):records.append(dict(name=name,sha256=digest(root/name)))
 save(root/'input-seal.json',dict(status='CLOSED',files=records,heads=newheads,source074_prediction_seal=ps,source074_feature_seal=fs,source074_input_seal=inp,source074_statistics_sha256=cat['statistics_sha256'],logical_original=5184,logical_interventions=10368,maximum_new_forward=2016,baseline_unique_integer_predictions=20160,baseline_logical_answers=103680))
 a.finish();assert not t.cuda.is_initialized();print('PREPARED36_HEADS24V28Q',flush=True)

def check_inputs(root):
 root=Path(root);sealed(root);s=read(root/'input-seal.json');assert s['status']=='CLOSED'
 for x in s['files']:assert digest(root/x['name'])==x['sha256']
 return s
def tensor_bytes(v):return v.detach().contiguous().numpy().tobytes()
def input_vectors(data,method,q,V):
 if method=='C_NATIVE':return [V,data['C'][q]]
 if method=='D_NATIVE':return [V,data['R'][q]]
 if method=='ANCHOR':return [V,data['A'][q],data['R'][q]]
 return [V,data['S'][q],data['R'][q]]
def input_identity(item,vectors):
 header=packed(dict(state=item['sha256'],method=item['method'],graph='056TemporalHead' if item['method'] in METHODS[:2] else '070factored',shapes=[list(x.shape) for x in vectors],dtype='torch.float32')).encode()+b'\0'
 raw=header+b''.join(tensor_bytes(v) for v in vectors);return sha(raw),raw

def predict(root):
 t=cpu();root=Path(root);check_inputs(root);gate=read(root/'state-oracle.json');assert gate['status']=='PASS' and read(root/'state-oracle-job.json')['exit_code']==read(root/'state-oracle-job.json')['active']==0
 access=Access(root,'prediction');data=t.load(root/'inputs.pt',map_location='cpu',weights_only=True);heads=read(root/'heads.json');qs=read(root/'questions.json');obs=read(root/'observations.json');original=read(root/'original-outputs.json');oldlookup={(x['method'],x['seed'],x['index'],x['question']):x for x in original};oldgraph=helper('semantic_role_factor_070');base=helper('question_temporal_056');unique=[];querymap={};new_count=0;cache={};start=time.monotonic();old_reference_matches={}
 for control,V in data['refs'].items():old_reference_matches[control]=[i for i,v in enumerate(data['V']) if tensor_bytes(V)==tensor_bytes(v)]
 with t.no_grad():
  for item in heads:
   method=item['method'];seed=item['seed'];model=base.TemporalHead(2560,2560) if method in METHODS[:2] else oldgraph.headclass()(2560,2560)
   model.load_state_dict(access.tensor(item['path'],'state',item['sha256']),strict=True);model.eval();model.requires_grad_(False);assert sum(p.numel() for p in model.parameters())==356673
   oldcache={}
   relevant=set(i for ids in old_reference_matches.values() for i in ids)
   for i in relevant:
    for qi,q in enumerate(obs[i]['questions']):
     sig,raw=input_identity(item,input_vectors(data,method,q,data['V'][i]));o=oldlookup[method,seed,i,qi]
     if sig in oldcache:assert oldcache[sig]['raw']==raw and oldcache[sig]['logit']==o['logit']
     oldcache[sig]=dict(raw=raw,logit=o['logit'],old_key=[method,seed,i,qi])
   for control in CONTROLS[1:]:
    V=data['refs'][control]
    for qindex,q in enumerate(qs):
     vectors=input_vectors(data,method,q,V);sig,raw=input_identity(item,vectors);key=(control,method,seed,qindex)
     if sig in cache:
      assert cache[sig]['raw']==raw;querymap[key]=cache[sig]['uid'];continue
     uid=len(unique)
     if sig in oldcache:
      assert oldcache[sig]['raw']==raw;z=oldcache[sig]['logit'];origin='ORIGINAL_EXACT_REUSE';old_key=oldcache[sig]['old_key']
     else:
      require(root,new_count<2016 and time.monotonic()-start<550,'NEW_FORWARD_OR_TIME_LIMIT',dict(forward=new_count,seconds=time.monotonic()-start),dict(forward=2016,seconds=600))
      event(root/'forward-ledger.jsonl',event='STARTED',uid=uid,signature=sig,method=method,seed=seed,control=control,question_index=qindex);new_count+=1
      if method in METHODS[:2]:out=model(V[None],vectors[1][None])
      else:out=model(V[None],data['S'][q][None],data['R'][q][None],data['A'][q][None],method)
      require(root,out.numel()==1 and t.isfinite(out).all(),'NONFINITE_HEAD_OUTPUT',list(out.shape),'one finite scalar');z=float(out.item());origin='NEW';old_key=None
      event(root/'forward-ledger.jsonl',event='CLOSED',uid=uid,signature=sig,prediction=int(z>0))
     row=dict(uid=uid,signature=sig,method=method,seed=seed,control=control,question_index=qindex,origin=origin,original_key=old_key,logit=z,prediction=int(z>0),status='CLOSED');unique.append(row);cache[sig]=dict(raw=raw,uid=uid);querymap[key]=uid
   assert all(not p.requires_grad and p.grad is None for p in model.parameters());print('FIXED_REFERENCES_CLOSED',method,seed,flush=True)
 outputs=[];used=set()
 for control in CONTROLS:
  for method in METHODS:
   for seed in SEEDS:
    for o in obs:
     for qi,q in enumerate(o['questions']):
      if control=='ORIGINAL_CACHED':x=oldlookup[method,seed,o['index'],qi];kind='CACHED';uid=None
      else:
       uid=querymap[control,method,seed,qs.index(q)];x=unique[uid];kind=('NEW' if x['origin']=='NEW' else 'CACHED') if uid not in used else 'ALIAS';used.add(uid)
      outputs.append(dict(control=control,method=method,seed=seed,index=o['index'],question=qi,uid=uid,kind=kind,status='CLOSED',logit=x['logit'],prediction=x['prediction']))
 assert len(outputs)==15552 and sum(x['kind']=='NEW' for x in outputs)==new_count
 save(root/'unique-results.json',unique);save(root/'outputs.json',outputs);save(root/'query-bindings.json',[dict(control=k[0],method=k[1],seed=k[2],question_index=k[3],uid=v) for k,v in querymap.items()])
 save(root/'prediction-seal.json',dict(status='CLOSED',outputs_sha256=digest(root/'outputs.json'),unique_sha256=digest(root/'unique-results.json'),bindings_sha256=digest(root/'query-bindings.json'),new_forward=new_count,original_cached=5184,intervention_logical=10368,logical_total=15552,aliases=sum(x['kind']=='ALIAS' for x in outputs),original_exact_reuse_unique=sum(x['origin']=='ORIGINAL_EXACT_REUSE' for x in unique),old_reference_matches=old_reference_matches,backward=0,optimizer=0));access.finish();assert not t.cuda.is_initialized()

def structural(root):
 root=Path(root);check_inputs(root);qs=read(root/'questions.json');obs=read(root/'observations.json');vocab=sorted({w for q in qs for w in words(q)},key=lambda w:w.encode());assert len(vocab)==6
 event(root/'integer-ledger.jsonl',event='STARTED',permutations=720,unique_answers=20160,logical_answers=103680)
 permutations=list(itertools.permutations(range(6)));pairs=[tuple(vocab.index(w) for w in words(q)) for q in qs];predictions=[]
 for p in permutations:
  ranks={word:i for i,word in enumerate(p)};predictions.append([int(ranks[a]<ranks[b]) for a,b in pairs])
 mapping=[[qs.index(q) for q in o['questions']] for o in obs];assert len(predictions)==720 and sum(map(len,predictions))==20160
 save(root/'structural-predictions.json',dict(vocab=vocab,permutations=permutations,question_pairs=pairs,predictions=predictions,mapping=mapping,unique_integer_predictions=20160,logical_answers=103680))
 save(root/'structural-seal.json',dict(status='CLOSED',sha256=digest(root/'structural-predictions.json'),label_access=0,model_forward=0));event(root/'integer-ledger.jsonl',event='CLOSED',permutations=720,unique_answers=20160,logical_answers=103680)

def measure(preds,ys,obs):
 cnt=collections.Counter();detail=[]
 for p,y,o in zip(preds,ys,obs):
  exact=int(p==y);coherent=int(tuple(p) in valid_orders(o['questions']));cnt['correct_cells']+=sum(a==b for a,b in zip(p,y));cnt['six_way_correct']+=exact;cnt['constant_videos']+=len(set(p))==1;cnt['coherent_and_correct']+=coherent and exact;cnt['coherent_but_wrong']+=coherent and not exact;cnt['incoherent']+=not coherent
  qs=o['questions'];cnt['complementary_pairs']+=sum(p[i]!=p[qs.index(tau(q))] for i,q in enumerate(qs))//2;detail.append(exact)
 assert cnt['coherent_and_correct']==cnt['six_way_correct'] and sum(cnt[k] for k in ['coherent_and_correct','coherent_but_wrong','incoherent'])==24
 cnt.update(cell_accuracy_pct=100*cnt['correct_cells']/144,six_way_accuracy_pct=100*cnt['six_way_correct']/24,complementary_pct=100*cnt['complementary_pairs']/72,constant_pct=100*cnt['constant_videos']/24)
 return dict(cnt),detail

def score(root):
 root=Path(root);check_inputs(root)
 for name in ('prediction','structural'):
  j=read(root/(name+'-job.json'));assert j['active']==j['exit_code']==0 and not j['killed']
 seal=read(root/'prediction-seal.json');assert digest(root/'outputs.json')==seal['outputs_sha256'] and digest(root/'structural-predictions.json')==read(root/'structural-seal.json')['sha256']
 outputs=read(root/'outputs.json');lookup={(x['control'],x['method'],x['seed'],x['index'],x['question']):x for x in outputs};assert len(lookup)==len(outputs)==15552 and set(lookup)==set(itertools.product(CONTROLS,METHODS,SEEDS,range(24),range(6)))
 assert all(x['status']=='CLOSED' and math.isfinite(x['logit']) and type(x['prediction']) is int and x['prediction']==int(x['logit']>0) for x in outputs)
 access=Access(root,'scoring');reg=read(root/'scoring-registration.json');labels=access.meta(reg['root_labels']);manifest=access.meta(reg['handed_manifest']);entry=next(x for x in manifest['members'] if x['path']==reg['member']);handed=access.meta(reg['handed_labels'],entry['sha256']);assert len(labels)==len(handed)==24
 obs=read(root/'observations.json');ys=[]
 for i,(row,other) in enumerate(zip(labels,handed)):
  assert row['index']==i and other['order_valid'] is True and [x['question'] for x in other['questions']]==obs[i]['questions'] and [x['label'] for x in other['questions']]==row['labels'] and len(row['labels'])==6 and sum(row['labels'])==3 and tuple(row['labels']) in valid_orders(obs[i]['questions']);ys.append(row['labels'])
 save(root/'scoring-labels.json',labels);conditions=[];details={};predictions={}
 for control in CONTROLS:
  for method in METHODS:
   for seed in SEEDS:
    rows=[lookup[control,method,seed,i,q] for i in range(24) for q in range(6)];ps=[[lookup[control,method,seed,i,q]['prediction'] for q in range(6)] for i in range(24)];m,ds=measure(ps,ys,obs);kinds=collections.Counter(x['kind'] for x in rows)
    conditions.append(dict(control=control,method=method,seed=seed,status='CLOSED',planned_items=24,planned_cells=144,new_cells=kinds['NEW'],cached_cells=kinds['CACHED'],alias_cells=kinds['ALIAS'],CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,**m));details[control,method,seed]=ds;predictions[control,method,seed]=ps
 pairs=[];summaries=[]
 for control in CONTROLS[1:]:
  for method in METHODS:
   group=[]
   for seed in SEEDS:
    left=details[control,method,seed];right=details['ORIGINAL_CACHED',method,seed];p=predictions[control,method,seed];q=predictions['ORIGINAL_CACHED',method,seed];lo=sum(a and not b for a,b in zip(left,right));ro=sum(b and not a for a,b in zip(left,right));changed=sum(a!=b for aa,bb in zip(p,q) for a,b in zip(aa,bb));changedgroups=sum(a!=b for a,b in zip(p,q))
    row=dict(left=control,right='ORIGINAL_CACHED',method=method,seed=seed,status='CLOSED',planned_items=24,evaluated_items=24,left_only=lo,right_only=ro,both_correct=sum(a and b for a,b in zip(left,right)),both_wrong=sum(not a and not b for a,b in zip(left,right)),unknown=0,net=lo-ro,delta_six_way_pp=100*(lo-ro)/24,changed_cells=changed,changed_videos=changedgroups);pairs.append(row);group.append(row)
   summaries.append(dict(control=control,method=method,status='CLOSED',seeds=6,planned_items_per_seed=24,mean_six_way_difference_pp=sum(x['delta_six_way_pp'] for x in group)/6,positive_seeds=sum(x['net']>0 for x in group),negative_seeds=sum(x['net']<0 for x in group),zero_seeds=sum(x['net']==0 for x in group),changed_cells=sum(x['changed_cells'] for x in group),planned_cells=864,changed_cells_pct=100*sum(x['changed_cells'] for x in group)/864,changed_videos=sum(x['changed_videos'] for x in group),identical_prediction_seeds=sum(x['changed_cells']==0 for x in group)))
 # Reproduce original metrics only; execution costs belong to074, not075.
 published=list(csv.DictReader(Path(__file__).parent.parent.joinpath('docs/codex-artifacts/VLM-MULTIEVENT-FROZEN-074/condition-summary.csv').open(encoding='utf-8-sig')))
 for row in conditions[:36]:
  old=next(x for x in published if x['method']==row['method'] and int(x['seed'])==row['seed'])
  for key in ('correct_cells','six_way_correct','complementary_pairs','constant_videos','cell_accuracy_pct','six_way_accuracy_pct','complementary_pct'):assert abs(float(old[key])-row[key])<1e-10
 baseline=read(root/'structural-predictions.json');hist=collections.Counter();correct_by_video=[0]*24;correct_cells=comp=constant=0
 for pred in baseline['predictions']:
  ps=[[pred[k] for k in ids] for ids in baseline['mapping']];m,ds=measure(ps,ys,obs);hist[m['six_way_correct']]+=1;correct_cells+=m['correct_cells'];comp+=m['complementary_pairs'];constant+=m['constant_videos'];correct_by_video=[a+b for a,b in zip(correct_by_video,ds)]
 assert correct_by_video==[120]*24 and sum(hist.values())==720 and sum(k*n for k,n in hist.items())==2880 and correct_cells==51840 and comp==51840 and constant==0
 bs=dict(status='COMPLETE_EXHAUSTIVE_INTEGER_BASELINE',vocabulary_size=6,unordered_triples=12,exact_questions=28,permutations=720,unique_integer_predictions=20160,logical_answers=103680,logical_video_groups=17280,correct_groups=2880,correct_cells=51840,per_video_correct_permutations=120,mean_six_way_accuracy_pct=100*2880/17280,mean_item_accuracy_pct=100*51840/103680,complementary_pairs=51840,planned_reverse_pairs=51840,complementary_pct=100.0,constant_videos=0,coherent_groups=17280,model_forward=0,selected_permutation=None,bootstrap_draws=0)
 save(root/'aggregates.json',dict(conditions=conditions,pairs=pairs,method_controls=summaries,baseline=bs,histogram=[dict(correct_groups=k,count=hist[k],status='CLOSED') for k in range(25)]));access.finish();print('SCORED108_CONDITIONS72_PAIRS720_BASELINE',flush=True)

def state_oracle(root):
 """Independent pre-call state gate; no head construction or learned forward."""
 import torch as T
 from pathlib import Path as P
 import hashlib as H,json as J,io as I
 T.set_num_threads(4);T.set_num_interop_threads(1);assert not T.cuda.is_initialized()
 r=P(root);prior=P(J.loads((r/'parent.json').read_bytes())['prior074']).resolve();counts={'metadata':0,'state':0};records=[];cache={};checks=0
 def old(path,kind):
  path=P(path).resolve();assert path.is_relative_to(prior);key=str(path)
  if key not in cache:
   cache[key]=path.read_bytes();counts[kind]+=len(cache[key]);records.append(dict(path=key,kind=kind,bytes=len(cache[key]),sha256=H.sha256(cache[key]).hexdigest()))
  return cache[key]
 inp=J.loads(old(prior/'input-seal.json','metadata'));body=old(prior/'asset-catalog.json','metadata');assert H.sha256(body).hexdigest()==inp['assets'];cat=J.loads(body);heads=J.loads((r/'heads.json').read_bytes());assert {(x['method'],x['seed'],x['path'],x['sha256']) for x in heads}=={(x['method'],x['seed'],str(P(x['path']).resolve()),x['sha256']) for x in cat['heads']}
 expected={'video.weight':(64,2560),'video.bias':(64,),'question.weight':(64,2560),'question.bias':(64,),'conv.weight':(64,64,3),'conv.bias':(64,),'mlp.0.weight':(64,256),'mlp.0.bias':(64,),'mlp.2.weight':(1,64),'mlp.2.bias':(1,)};summaries=[]
 for x in heads:
  data=old(x['path'],'state');assert H.sha256(data).hexdigest()==x['sha256'];checks+=1;state=T.load(I.BytesIO(data),map_location='cpu',weights_only=True);assert set(state)==set(expected);checks+=1
  for k,v in state.items():assert tuple(v.shape)==expected[k] and v.dtype==T.float32 and T.isfinite(v).all();checks+=1
  assert sum(v.numel() for v in state.values())==356673;checks+=1;st=P(x['path']).stat();summaries.append(dict(method=x['method'],seed=x['seed'],path=x['path'],sha256=x['sha256'],size=st.st_size,mtime_ns=st.st_mtime_ns,parameters=356673))
 previous={'state':0,'metadata':0}
 for p in r.glob('*-access.json'):
  q=J.loads(p.read_bytes())['counts']
  for k in previous:previous[k]+=q.get(k,0)
 assert previous['state']+counts['state']<=128*1024**2 and previous['metadata']+counts['metadata']<=32*1024**2
 with open(r/'state-oracle-access.json','x',encoding='utf-8') as f:J.dump(dict(counts=counts,files=records),f);f.flush();os.fsync(f.fileno())
 save(r/'state-oracle.json',dict(status='PASS',checks=checks,heads=summaries,learned_forward=0,state_copies=0));assert not T.cuda.is_initialized();print('INDEPENDENT_STATE_GATE_PASS',checks,flush=True)

def independent(root):
 """Rebuilds reference/input/alias identity and every score without inference.

    Does not call/import the producer's predictor, scorer, transform or metric
    helpers. The earlier independent state gate and prediction's verified read
    are the two old-state payload passes; this final oracle does not read them a
    third time or copy the weights. No learned computation is replayed.
 """
 import torch as T
 import json as J,hashlib as H,re as R,itertools as IT,io as I
 from collections import Counter as CT
 from pathlib import Path as P
 T.set_num_threads(4);T.set_num_interop_threads(1);assert not T.cuda.is_initialized()
 r=P(root);prior=P(J.loads((r/'parent.json').read_bytes())['prior074']).resolve();checks=0;cache={};counts=CT();records=[];newbytes=0
 def test(v,reason):
  nonlocal checks
  checks+=1
  if not v:raise AssertionError(reason)
 def canon(v):return J.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
 def oldbytes(path,kind='metadata',expected=None):
  path=P(path).resolve();test(path.is_relative_to(prior),'authorized_root');key=str(path)
  if key not in cache:
   cache[key]=path.read_bytes();counts[kind]+=len(cache[key]);records.append(dict(path=key,kind=kind,bytes=len(cache[key]),sha256=H.sha256(cache[key]).hexdigest()))
  b=cache[key]
  if expected:test(H.sha256(b).hexdigest()==expected,'source_identity')
  return b
 def source(path,expected=None):return J.loads(oldbytes(path,expected=expected))
 def new(path):
  nonlocal newbytes
  b=(r/path).read_bytes();newbytes+=len(b);return J.loads(b)
 def tensor_bytes(v):return v.detach().contiguous().numpy().tobytes()
 def endpoints(q):
  m=R.fullmatch(r'Does the event "(.+)" happen before the event "(.+)"\? Answer Yes or No\.',q);test(m is not None,'strict_parser');return m.groups()
 def reverse(q):
  a,b=endpoints(q);return 'Does the event "%s" happen before the event "%s"? Answer Yes or No.'%(b,a)
 code=new('code-seal.json')
 for f in code['files']:test(H.sha256(P(f['path']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==f['lf_sha256'],'code_seal')
 ins=new('input-seal.json')
 for f in ins['files']:test(H.sha256((r/f['name']).read_bytes()).hexdigest()==f['sha256'],'input_seal')
 priorin=source(prior/'input-seal.json');cat=source(prior/'asset-catalog.json',priorin['assets']);originalobs=source(prior/'observations.json',priorin['observations']);obs=new('observations.json');test(obs==[dict(index=x['index'],questions=x['questions']) for x in originalobs],'observations')
 fs=source(prior/'feature-seal.json');ix=source(prior/'feature-index.json',fs['index_sha256']);ps=source(prior/'prediction-seal.json');original=J.loads(oldbytes(prior/'outputs.json',expected=ps['output_sha256']));test(original==new('original-outputs.json'),'original_cache_exact')
 V=[T.load(I.BytesIO(oldbytes(ix['video'][str(i)]['path'],'feature',ix['video'][str(i)]['sha256'])),map_location='cpu',weights_only=True) for i in range(24)];qs=sorted({q for x in originalobs for q in x['questions']},key=lambda s:s.encode());Q={q:T.load(I.BytesIO(oldbytes(ix['text'][q]['path'],'feature',ix['text'][q]['sha256'])),map_location='cpu',weights_only=True) for q in qs}
 statbytes=oldbytes(prior/'frozen-statistics.pt','state',cat['statistics_sha256']);st=T.load(I.BytesIO(statbytes),map_location='cpu',weights_only=True);test((r/'frozen-statistics.pt').read_bytes()==statbytes,'statistics_unchanged');data=T.load(r/'inputs.pt',map_location='cpu',weights_only=True)
 for i,v in enumerate(V):test(T.equal(v,data['V'][i]) and v.dtype==T.float32 and v.shape==(6,2560) and T.isfinite(v).all(),'V_unchanged')
 for q,v in Q.items():test(T.equal(v,data['Q'][q]) and v.dtype==T.float32 and v.shape==(2560,) and T.isfinite(v).all(),'h_unchanged')
 acc=T.zeros((6,2560),dtype=T.float64)
 for i in range(24):acc=acc+V[i].to(dtype=T.float64)
 mean=(acc/24).to(dtype=T.float32);zero=T.zeros((6,2560),dtype=T.float32)
 test(T.equal(mean,data['refs']['GLOBAL_MEAN_V']) and mean.shape==(6,2560),'mean_ordered24_no_temporal_pool');test(T.equal(zero,data['refs']['ZERO_V']),'zero')
 C={};S={};D={};A={}
 canonical=st['canonical'];test(len(canonical)==len(set(canonical))==42 and canonical==sorted(canonical,key=lambda s:s.encode()),'canonical42')
 def eventpair(q):return sorted(' '.join(v.replace('_',' ').split()).casefold() for v in endpoints(q))
 for q in qs:
  t=reverse(q);test(t in Q and reverse(t)==q,'tau_closed');x=Q[q].double();y=Q[t].double();nc=st['normalizer']['C_CENTER'];nd=st['normalizer']['D_ROLE'];ns=st['S_normalizer']
  C[q]=((x-nc['mu'])/nc['scale']).float();D[q]=(((x-y)/2-nd['mu'])/nd['scale']).float();S[q]=(((x+y)/2-ns['mu'])/ns['scale']).float()
  c=min(q,t,key=lambda s:s.encode());start=int.from_bytes(H.sha256(b'VLM070/c-anchor/'+c.encode()).digest()[:8],'big')%42;selected=next(canonical[(start+j)%42] for j in range(42) if eventpair(canonical[(start+j)%42])!=eventpair(q));A[q]=st['anchor_S'][selected]
  test(data['anchors'][q]==selected,'anchor_binding')
  for k,value in [('C',C[q]),('R',D[q]),('S',S[q]),('A',A[q])]:test(T.equal(data[k][q],value),'exact_transform_'+k)
 heads=new('heads.json');test(heads==sorted([dict(method=x['method'],seed=x['seed'],path=str(P(x['path']).resolve()),sha256=x['sha256']) for x in cat['heads']],key=lambda x:(['C_NATIVE','D_NATIVE','CONCAT','FACTOR','REVERSE','ANCHOR'].index(x['method']),[137,263,419,557,733,911].index(x['seed']))),'original_head_registration')
 gate=new('state-oracle.json');predaccess=new('prediction-access.json');pa={x['path']:x for x in predaccess['files']}
 for f in gate['heads']:
  test(f['parameters']==356673 and pa[f['path']]['sha256']==f['sha256'],'independent_gate_and_forward_state_same');s=P(f['path']).stat();test(s.st_size==f['size'] and s.st_mtime_ns==f['mtime_ns'],'original_state_file_unchanged')
 hmap={(x['method'],x['seed']):x for x in heads}
 def identity(method,seed,q,v):
  if method=='C_NATIVE':vv=[v,C[q]]
  elif method=='D_NATIVE':vv=[v,D[q]]
  elif method=='ANCHOR':vv=[v,A[q],D[q]]
  else:vv=[v,S[q],D[q]]
  header=canon(dict(state=hmap[method,seed]['sha256'],method=method,graph='056TemporalHead' if method in ['C_NATIVE','D_NATIVE'] else '070factored',shapes=[list(x.shape) for x in vv],dtype='torch.float32')).encode()+b'\0';raw=header+b''.join(tensor_bytes(x) for x in vv);return H.sha256(raw).hexdigest(),raw
 seal=new('prediction-seal.json')
 for name,key in [('outputs.json','outputs_sha256'),('unique-results.json','unique_sha256'),('query-bindings.json','bindings_sha256')]:test(H.sha256((r/name).read_bytes()).hexdigest()==seal[key],'output_seal')
 unique=new('unique-results.json');bindings=new('query-bindings.json');outputs=new('outputs.json');methods=['C_NATIVE','D_NATIVE','CONCAT','FACTOR','REVERSE','ANCHOR'];seeds=[137,263,419,557,733,911];controls=['ORIGINAL_CACHED','GLOBAL_MEAN_V','ZERO_V'];query={(x['control'],x['method'],x['seed'],x['question_index']):x['uid'] for x in bindings}
 test(len(query)==len(bindings)==2016 and set(query)==set(IT.product(controls[1:],methods,seeds,range(28))),'2016_query_bindings');raws={};oldlookup={(x['method'],x['seed'],x['index'],x['question']):x for x in original}
 for row in bindings:
  m=row['method'];s=row['seed'];q=qs[row['question_index']];u=unique[row['uid']];sig,raw=identity(m,s,q,data['refs'][row['control']]);test(u['signature']==sig,'complete_input_hash')
  if u['uid'] in raws:test(raws[u['uid']]==raw,'full_bytes_alias_identity')
  else:raws[u['uid']]=raw
  test(u['status']=='CLOSED' and math.isfinite(u['logit']) and u['prediction']==int(u['logit']>0),'unique_result_valid')
  matches=[]
  for i,v in enumerate(V):
   if tensor_bytes(v)==tensor_bytes(data['refs'][row['control']]):
    for qi,qold in enumerate(obs[i]['questions']):
     if identity(m,s,qold,v)[1]==raw:matches.append(oldlookup[m,s,i,qi])
  if matches:test(u['origin']=='ORIGINAL_EXACT_REUSE' and any(x['logit']==u['logit'] for x in matches),'original_exact_reuse_not_reasked')
  else:test(u['origin']=='NEW','new_input_no_old_exact_match')
 ledger=[J.loads(x) for x in (r/'forward-ledger.jsonl').read_text(encoding='utf-8').splitlines()];starts=[x for x in ledger if x['event']=='STARTED'];closed=[x for x in ledger if x['event']=='CLOSED'];newuids=[x['uid'] for x in unique if x['origin']=='NEW'];test([x['uid'] for x in starts]==[x['uid'] for x in closed]==newuids and len(set(newuids))==len(newuids)<=2016,'new_call_ledger')
 for a,b in zip(starts,closed):test(a['signature']==b['signature']==unique[a['uid']]['signature'],'ledger_identity')
 test(seal['new_forward']==len(starts),'actual_forward_count')
 lut={(x['control'],x['method'],x['seed'],x['index'],x['question']):x for x in outputs};test(len(lut)==len(outputs)==15552 and set(lut)==set(IT.product(controls,methods,seeds,range(24),range(6))),'15552_full_keys');used=set()
 for row in outputs:
  m=row['method'];s=row['seed'];i=row['index'];qi=row['question'];test(row['status']=='CLOSED','all_logical_closed')
  if row['control']=='ORIGINAL_CACHED':expected=oldlookup[m,s,i,qi];test(row['kind']=='CACHED' and row['uid'] is None,'original_no_new_forward')
  else:
   uid=query[row['control'],m,s,qs.index(obs[i]['questions'][qi])];expected=unique[uid];kind=('NEW' if expected['origin']=='NEW' else 'CACHED') if uid not in used else 'ALIAS';used.add(uid);test(row['kind']==kind and row['uid']==uid,'alias_logical_binding')
  test(row['prediction']==expected['prediction'] and row['logit']==expected['logit'],'logical_exact_value')
 reg=new('scoring-registration.json');labels=source(reg['root_labels']);manifest=source(reg['handed_manifest']);entry=next(x for x in manifest['members'] if x['path']==reg['member']);handed=source(reg['handed_labels'],entry['sha256']);test(labels==new('scoring-labels.json'),'scoring_labels_snapshot');ys=[];coherent=[];reversepairs=[]
 for i,o in enumerate(obs):
  test([x['question'] for x in handed[i]['questions']]==o['questions'] and [x['label'] for x in handed[i]['questions']]==labels[i]['labels'],'handed_label_binding');y=labels[i]['labels'];test(len(y)==6 and sum(y)==3 and all(type(k) is int and k in [0,1] for k in y),'binary_balanced_labels');ys.append(y)
  ev=sorted({w for q in o['questions'] for w in endpoints(q)},key=lambda w:w.encode());patterns={tuple(int(p.index(a)<p.index(b)) for a,b in [endpoints(q) for q in o['questions']]) for p in IT.permutations(ev)};test(len(ev)==3 and len(patterns)==6 and tuple(y) in patterns,'six_complete_orders');coherent.append(patterns);edges=set()
  for qi,q in enumerate(o['questions']):edges.add(tuple(sorted([qi,o['questions'].index(reverse(q))])))
  test(len(edges)==3,'three_reverse_pairs');reversepairs.append(sorted(edges))
 agg=new('aggregates.json');expectedrows={};detail={};allpred={}
 def metrics(pp):
  correct=allcorrect=cp=const=good=wrong=bad=0;ds=[]
  for i,p in enumerate(pp):
   exact=p==ys[i];isorder=tuple(p) in coherent[i];correct+=sum(a==b for a,b in zip(p,ys[i]));allcorrect+=exact;cp+=sum(p[a]!=p[b] for a,b in reversepairs[i]);const+=len(set(p))==1;good+=exact and isorder;wrong+=isorder and not exact;bad+=not isorder;ds.append(int(exact))
  return dict(correct_cells=correct,six_way_correct=allcorrect,complementary_pairs=cp,constant_videos=const,coherent_and_correct=good,coherent_but_wrong=wrong,incoherent=bad,cell_accuracy_pct=100*correct/144,six_way_accuracy_pct=100*allcorrect/24,complementary_pct=100*cp/72,constant_pct=100*const/24),ds
 for control,m,s in IT.product(controls,methods,seeds):
  pp=[[lut[control,m,s,i,q]['prediction'] for q in range(6)] for i in range(24)];values,ds=metrics(pp);detail[control,m,s]=ds;allpred[control,m,s]=pp;actual=next(x for x in agg['conditions'] if (x['control'],x['method'],x['seed'])==(control,m,s));kinds=CT(lut[control,m,s,i,q]['kind'] for i in range(24) for q in range(6));values.update(new_cells=kinds['NEW'],cached_cells=kinds['CACHED'],alias_cells=kinds['ALIAS'],CLOSED=144,INVALID=0,FAILED=0,NOT_RUN=0,execution_unknown=0,scoring_unknown=0,planned_items=24,planned_cells=144)
  for key,value in values.items():test(abs(actual[key]-value)<1e-10,'condition_'+key)
  test(values['coherent_and_correct']==values['six_way_correct'] and values['coherent_and_correct']+values['coherent_but_wrong']+values['incoherent']==24,'coherence_partition')
 for control,m,s in IT.product(controls[1:],methods,seeds):
  a=detail[control,m,s];b=detail['ORIGINAL_CACHED',m,s];pp=allpred[control,m,s];op=allpred['ORIGINAL_CACHED',m,s];lo=sum(x and not y for x,y in zip(a,b));ro=sum(y and not x for x,y in zip(a,b));values=dict(left_only=lo,right_only=ro,both_correct=sum(x and y for x,y in zip(a,b)),both_wrong=sum(not x and not y for x,y in zip(a,b)),unknown=0,net=lo-ro,delta_six_way_pp=100*(lo-ro)/24,changed_cells=sum(x!=y for p,q in zip(pp,op) for x,y in zip(p,q)),changed_videos=sum(p!=q for p,q in zip(pp,op)),planned_items=24,evaluated_items=24);actual=next(x for x in agg['pairs'] if (x['left'],x['method'],x['seed'])==(control,m,s))
  for key,val in values.items():test(abs(actual[key]-val)<1e-10,'paired_'+key)
 for control,m in IT.product(controls[1:],methods):
  rows=[x for x in agg['pairs'] if x['left']==control and x['method']==m];actual=next(x for x in agg['method_controls'] if x['control']==control and x['method']==m);values=dict(positive_seeds=sum(x['net']>0 for x in rows),negative_seeds=sum(x['net']<0 for x in rows),zero_seeds=sum(x['net']==0 for x in rows),changed_cells=sum(x['changed_cells'] for x in rows),changed_videos=sum(x['changed_videos'] for x in rows),identical_prediction_seeds=sum(x['changed_cells']==0 for x in rows),mean_six_way_difference_pp=100*sum(x['net'] for x in rows)/144,changed_cells_pct=100*sum(x['changed_cells'] for x in rows)/864)
  for key,val in values.items():test(abs(actual[key]-val)<1e-10,'method_control_'+key)
 structure=new('structural-predictions.json');test(H.sha256((r/'structural-predictions.json').read_bytes()).hexdigest()==new('structural-seal.json')['sha256'],'structural_seal');vocab=sorted({w for q in qs for w in endpoints(q)},key=lambda w:w.encode());test(len(vocab)==6 and vocab==structure['vocab'],'vocabulary6');triples={tuple(sorted({w for q in x['questions'] for w in endpoints(q)},key=lambda w:w.encode())) for x in obs};test(len(triples)==12,'triples12')
 expectedperms=[list(p) for p in IT.permutations(range(6))];test(structure['permutations']==expectedperms,'all720_orders');mapping=[[qs.index(q) for q in o['questions']] for o in obs];test(mapping==structure['mapping'],'baseline_mapping');hist=CT();pervideo=[0]*24;correct=cp=constant=0
 for pi,p in enumerate(expectedperms):
  rank={word:i for i,word in enumerate(p)};pred=[int(rank[vocab.index(a)]<rank[vocab.index(b)]) for a,b in [endpoints(q) for q in qs]];test(pred==structure['predictions'][pi],'20160_integer_predictions');pp=[[pred[k] for k in group] for group in mapping];values,ds=metrics(pp);hist[values['six_way_correct']]+=1;correct+=values['correct_cells'];cp+=values['complementary_pairs'];constant+=values['constant_videos'];pervideo=[a+b for a,b in zip(pervideo,ds)];test(values['incoherent']==0,'all_orders_coherent')
 test(pervideo==[120]*24 and correct==51840 and cp==51840 and constant==0,'exact_baseline_calibration')
 for row in agg['histogram']:test(row['count']==hist[row['correct_groups']],'histogram25')
 test(len(agg['histogram'])==25 and sum(hist.values())==720 and sum(k*n for k,n in hist.items())==2880,'histogram_moments');bs=agg['baseline']
 for key,val in dict(permutations=720,unique_integer_predictions=20160,logical_answers=103680,logical_video_groups=17280,correct_groups=2880,correct_cells=51840,per_video_correct_permutations=120,mean_six_way_accuracy_pct=100/6,mean_item_accuracy_pct=50,complementary_pct=100,constant_videos=0,coherent_groups=17280,model_forward=0,bootstrap_draws=0).items():test(abs(bs[key]-val)<1e-10,'baseline_'+key)
 test(bs['selected_permutation'] is None,'no_permutation_selection')
 # Public original074 integer/percentage reproduction, with no original forward.
 public=P(__file__).parent.parent/'docs/codex-artifacts/VLM-MULTIEVENT-FROZEN-074/condition-summary.csv'
 with public.open(encoding='utf-8-sig') as f:published=list(csv.DictReader(f))
 for oldrow in published:
  x=next(x for x in agg['conditions'] if x['control']=='ORIGINAL_CACHED' and x['method']==oldrow['method'] and x['seed']==int(oldrow['seed']))
  for key in ['correct_cells','six_way_correct','complementary_pairs','constant_videos','cell_accuracy_pct','six_way_accuracy_pct','complementary_pct']:test(abs(float(oldrow[key])-x[key])<1e-10,'original_public_reproduction')
 for phase in ['preparation','state-oracle','prediction','structural','scoring']:
  j=new(phase+'-job.json');test(j['exit_code']==j['active']==0 and not j['killed'],'job_closed')
 earlier=CT()
 for f in r.glob('*-access.json'):earlier.update(J.loads(f.read_bytes())['counts'])
 for k,cap in [('metadata',32*1024**2),('state',128*1024**2),('feature',64*1024**2)]:test(earlier[k]+counts[k]<=cap,'old_read_cap')
 test(not T.cuda.is_initialized(),'no_cuda');save(r/'independent-review-access.json',dict(counts=dict(counts),files=records));save(r/'independent-review.json',dict(status='PASS',checks=checks,producer_predictor_scorer_imports=0,learned_forward=0,original_forward=0,new_artifact_bytes_explicit=newbytes,old_read_counts=dict(counts),state_gate_independent_checks=gate['checks']));print('INDEPENDENT_ALL_METRICS_INPUTS_BASELINE_PASS',checks,flush=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('role',choices=['prepare','state_oracle','predict','structural','score','independent']);p.add_argument('--root',required=True);args=p.parse_args();root=Path(args.root)
 try:globals()[args.role](root)
 except Exception as e:event(root/'stops.jsonl',stage=args.role,reason=str(e) or type(e).__name__,error_type=type(e).__name__,action='STOP_NO_FAILED_INPUT_RETRY');raise
if __name__=='__main__':main()
