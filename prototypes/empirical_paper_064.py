"""064 public arithmetic/figures and separately invoked narrow B0 bridge.

No torch, research-module imports, model operations or network requests.
Public mode reads public aggregates only; bridge is never automatic.
"""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import random
import statistics
import struct
import time
import xml.etree.ElementTree as ET
NEW=(137,263,419,557,733,911)
ALL=(19,73)+NEW
SOURCE='source_holdout50'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,x):
 with open(p,'x',encoding='utf-8') as f:json.dump(x,f,indent=2,sort_keys=True);f.flush();os.fsync(f.fileno())
def qtile(v,p):
 v=sorted(v);x=(len(v)-1)*p;i=int(x);return v[i]+(x-i)*(v[min(i+1,len(v)-1)]-v[i])
def bridge(root,prior063,prior060,report):
 root=Path(root);p63=Path(prior063).resolve();p60=Path(prior060).resolve();start=time.monotonic();used=0;blobs={};records={};status='UNVERIFIED';reason='NOT_COMPLETED';counts=dict(planned=200,actual060=0,actual063=0,equal=0,unequal=0,missing=0,unknown=200);binding=False;original_seal=False
 def raw(p):
  nonlocal used
  p=Path(p).resolve();key=str(p)
  if key not in blobs:
   n=p.stat().st_size
   if used+n>16*1024**2 or time.monotonic()-start>50:raise RuntimeError('BRIDGE_READ_OR_TIME_BUDGET')
   b=p.read_bytes();used+=len(b);assert len(b)==n;h=hashlib.sha256(b).hexdigest();blobs[key]=b;records[key]=dict(path=key,bytes=n,sha256=h)
  return blobs[key]
 def j(p):return json.loads(raw(p).decode('utf-8-sig'))
 def sealed(p,expected):
  p=Path(p).resolve();b=raw(p);assert str(p) in expected and hashlib.sha256(b).hexdigest()==expected[str(p)],'ORIGINAL_SEAL_IDENTITY';return json.loads(b.decode('utf-8-sig'))
 def mapping(rows):
  result={}
  for r in rows:
   if (r.get('method'),r.get('seed'),r.get('split'))!=('B0','NA',SOURCE):continue
   key=(r['split'],r['index'],r['video'],r['question']);assert key not in result;result[key]=r
  return result
 try:
  assert j(p63/'parent-closed.json')['push']=='SUCCEEDED' and j(p60/'parent-closed.json')['push']=='SUCCEEDED'
  assert Path(j(p63/'old-assets.json')['prior060']).resolve()==p60
  j(p63/'cache-read-seal.json');s63=j(p63/'output-seal.json');e63={str(Path(x['path']).resolve()):x['sha256'] for x in s63['files']};i63=sealed(p63/'input-seal.json',e63);e63.update({str(Path(x['path']).resolve()):x['sha256'] for x in i63['files']})
  s60=j(p60/'outputs-identity-seal.json');e60={str(Path(x['path']).resolve()):x['sha256'] for x in s60['files']};i60=sealed(p60/'pre-consumption-seal.json',e60);e60.update({str(Path(x['path']).resolve()):x['sha256'] for x in i60['files']})
  old=sealed(p60/'all-outputs-sealed.json',e60);original_seal=True;current=j(p63/'all-outputs.json')
  a=sealed(p60/(SOURCE+'-observations.json'),e60);b=sealed(p63/(SOURCE+'-observations.json'),e63)
  assert len(a)==len(b)==50
  aa={x['index']:(x['videos'],x['questions']) for x in a};bb={x['index']:(x['videos'],x['questions']) for x in b};binding=aa==bb and set(aa)==set(range(50))
  l=mapping(old);r=mapping(current);counts['actual060']=len(l);counts['actual063']=len(r);keys={(SOURCE,i,v,q) for i in range(50) for v in (0,1) for q in (0,1)};counts.update(equal=0,unequal=0,missing=0,unknown=0)
  for key in keys:
   if key not in l or key not in r:counts['missing']+=1;continue
   x,y=l[key],r[key]
   if any(z.get('status')!='CLOSED' or type(z.get('prediction')) is not int or z.get('prediction') not in (0,1) for z in (x,y)):counts['unknown']+=1
   elif x['prediction']==y['prediction']:counts['equal']+=1
   else:counts['unequal']+=1
  if set(l)!=keys or set(r)!=keys:reason='MEMBERSHIP_MISMATCH';status='MISMATCH'
  else:status='PASS' if binding and counts['equal']==200 else 'MISMATCH';reason='EXACT_PREDICTIONS_AND_BINDINGS' if status=='PASS' else 'PREDICTION_OR_BINDING_MISMATCH'
  for rec in list(records.values()):
   n=rec['bytes']
   if used+n>16*1024**2 or time.monotonic()-start>50:raise RuntimeError('POST_READ_BUDGET')
   data=Path(rec['path']).read_bytes();used+=len(data);assert hashlib.sha256(data).hexdigest()==rec['sha256'],'CHANGED_DURING_BRIDGE'
 except Exception as exc:status='UNVERIFIED';reason=str(exc)
 result=dict(status=status,reason=reason,counts=counts,binding_check=binding,original060_output_seal=original_seal,logical_read_bytes=used,outer_s=time.monotonic()-start,current_retrospective_check_only=True,old_files_unchanged=status in ('PASS','MISMATCH'))
 write(root/'bridge-private.json',dict(result=result,files=list(records.values())));write(root/'bridge-summary.json',result)
 text=f"# B0 cache bridge\n\nStatus: {status}\n\n2026-10-31 Asia/Shanghai. Planned200; actual060={counts['actual060']}; actual063={counts['actual063']}; equal={counts['equal']}; unequal={counts['unequal']}; missing={counts['missing']}; unknown={counts['unknown']}.\n\nBindings={'PASS' if binding else 'UNVERIFIED_OR_MISMATCH'}; original060 output seal={'VERIFIED' if original_seal else 'UNVERIFIED'}. Reason:{reason}. Logical read bytes={used}; worker outer={result['outer_s']:.3f}s. No labels, features, weights, media or model operations.\n\nThis is a new064 retrospective read-only equality check against original060 sealed outputs and exact video/question/index bindings. It does not retroactively seal062/063 artifacts or certify OS/physical provenance. No old file was written or old B0 regenerated. B0 accuracy, if used, remains the original public0607/50 aggregate, not a new label-based score.\n"
 Path(report).write_text(text,encoding='utf-8');print('B0_BRIDGE',status,counts['equal'],used,flush=True)
def public_tables(repo):
 repo=Path(repo);art=repo/'docs/codex-artifacts';sources={n:read(art/f'{name}/execution-summary.json') for n,name in [('060','VLM-POOL-TRANSFER-060'),('061','VLM-TEMPORAL-BINDING-AUDIT-061'),('062','VLM-QUESTION-ROLE-CONTRAST-062'),('063','VLM-ROLE-CONTRAST-REPLICATION-063')]};s=sources['063'];checks=0
 def check(v):
  nonlocal checks
  assert v,checks;checks+=1
 def near(a,b):check(abs(a-b)<1e-10)
 conditions=[]
 for r in s['conditions']:
  row=dict(r);n=sum(r['K'+str(k)] for k in range(5));check(n==r['n_instances']);rebuilt=dict(correct_cells=sum(k*r['K'+str(k)] for k in range(5)),four_way_correct=r['K4'],video_pair_correct=r['VIDEO_ONLY']+2*r['K4']+r['K3'],question_pair_correct=r['QUESTION_ONLY']+2*r['K4']+r['K3'],question_invariant=r['CONSTANT']+r['VIDEO_ONLY'])
  for k,v in rebuilt.items():check(v==r[k]);row[k]=v
  check(sum(r[k] for k in ('CONSTANT','VIDEO_ONLY','QUESTION_ONLY','CHECKERBOARD','MIXED'))==n and r['n_cells']==r['valid_cells']==r['complete_cells']==4*n);conditions.append(row)
 def cmp_csv(name,key):
  with open(art/'VLM-ROLE-CONTRAST-REPLICATION-063'/name,encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
  check(len(rows)==len(s[key]))
  for x,y in zip(rows,s[key]):check(all(x[k]==str(v) for k,v in y.items()))
 cmp_csv('condition-summary.csv','conditions');cmp_csv('paired-summary.csv','paired');check(len(conditions)==81 and sum(x['n_cells'] for x in conditions)==14840)
 rng=random.Random(55063);draws=[rng.choices(range(25),k=25) for _ in range(10000)];vectors={};paired=[];intervals=[]
 for row in s['paired']:
  seed,l,r=row['seed'],row['left'],row['right'];gs=sorted([g for g in s['source_profile'] if (g['seed'],g['left'],g['right'])==(seed,l,r)],key=lambda g:g['family']);check(len(gs)==25 and [g['family'] for g in gs]==[f'F{i:02}' for i in range(1,26)])
  for g in gs:check(g['n']==2 and sum(g[k] for k in ('left_only','right_only','both_correct','both_wrong','unknown'))==2)
  for key in ('left_only','right_only','both_correct','both_wrong','unknown','left_question_invariant','right_question_invariant'):check(row[key]==sum(g[key] for g in gs))
  for method,correct,qinv in [(l,row['left_only']+row['both_correct'],row['left_question_invariant']),(r,row['right_only']+row['both_correct'],row['right_question_invariant'])]:
   c=next(x for x in conditions if (x['method'],x['seed'],x['split'])==(method,seed,SOURCE));check(correct==c['four_way_correct'] and qinv==c['question_invariant'])
  for metric,f in [('answer',lambda g:g['left_only']-g['right_only']),('question_invariant',lambda g:g['left_question_invariant']-g['right_question_invariant'])]:
   v=[f(g) for g in gs];vectors[(seed,l,r,metric)]=v;samples=[100*sum(v[k] for k in draw)/sum(gs[k]['n'] for k in draw) for draw in draws];lo,hi=qtile(samples,.025),qtile(samples,.975);near(lo,row[metric+'_ci_low_pp']);near(hi,row[metric+'_ci_high_pp']);intervals.append(dict(kind='pair',seed=seed,left=l,right=r,metric=metric,estimate_pp=2*sum(v),ci_low_pp=lo,ci_high_pp=hi))
  paired.append(dict(row))
 interactions=[]
 for row in s['interactions']:
  seed=row['seed'];v=[a-b for a,b in zip(vectors[(seed,'D_NATIVE','C_NATIVE','answer')],vectors[(seed,'D_HASH','C_HASH','answer')])];samples=[sum(v[k] for k in d)*2 for d in draws];lo,hi=qtile(samples,.025),qtile(samples,.975);check(sum(v)==row['net_instances']);near(lo,row['ci_low_pp']);near(hi,row['ci_high_pp']);interactions.append(dict(row));intervals.append(dict(kind='interaction',seed=seed,metric='answer',estimate_pp=2*sum(v),ci_low_pp=lo,ci_high_pp=hi))
 srng=random.Random(55064);seed_draws=[srng.choices(range(6),k=6) for _ in range(10000)];extra=[]
 for metric in ('answer','question_invariant'):
  vs=[vectors[(seed,'D_NATIVE','C_NATIVE',metric)] for seed in NEW];values=[2*sum(v) for v in vs]
  for kind in ('new_six_family','new_six_seed'):
   samples=[sum(2*sum(v[k] for k in d) for v in vs)/6 for d in draws] if kind.endswith('family') else [sum(values[k] for k in d)/6 for d in seed_draws];row=dict(kind=kind,metric=metric,estimate_pp=sum(values)/6,ci_low_pp=qtile(samples,.025),ci_high_pp=qtile(samples,.975));original=next(x for x in s['extra_intervals'] if x['kind']==kind and x['metric']==metric)
   for k in ('estimate_pp','ci_low_pp','ci_high_pp'):near(row[k],original[k])
   extra.append(row);intervals.append(row)
 seed_summary=[]
 for seed in ALL:
  for split in ('development54',SOURCE):
   c=next(r for r in conditions if (r['method'],r['seed'],r['split'])==('C_NATIVE',seed,split));d=next(r for r in conditions if (r['method'],r['seed'],r['split'])==('D_NATIVE',seed,split));row=dict(seed=seed,split=split,C_correct=c['four_way_correct'],D_correct=d['four_way_correct'],net=d['four_way_correct']-c['four_way_correct'],C_question_invariant=c['question_invariant'],D_question_invariant=d['question_invariant']);check(row==next(x for x in s['seed_summary'] if x['seed']==seed and x['split']==split));seed_summary.append(row)
 aggregates=[]
 for seeds,name in [(NEW,'NEW_SIX'),(ALL,'ALL_EIGHT_DESCRIPTIVE')]:
  for split in ('development54',SOURCE):
   rows=[r for r in seed_summary if r['seed'] in seeds and r['split']==split];row=dict(group=name,split=split,n_seeds=len(rows))
   for k in ('C_correct','D_correct','net','C_question_invariant','D_question_invariant'):
    v=[r[k] for r in rows];row[k]=dict(mean=statistics.mean(v),median=statistics.median(v),min=min(v),max=max(v))
   check(row==next(x for x in s['seed_aggregates'] if x['group']==name and x['split']==split));aggregates.append(row)
 ns=[r for r in seed_summary if r['seed'] in NEW and r['split']==SOURCE];stable=sum(r['net']>0 for r in ns)>=5 and sum(r['net'] for r in ns)/6>=4 and sum(r['D_correct'] for r in ns)/6>=10 and sum(r['C_question_invariant']-r['D_question_invariant'] for r in ns)/6>=10;order=all(next(r for r in paired if (r['seed'],r['left'],r['right'])==(seed,'D_NATIVE','D_HASH'))['net']>=2 for seed in (19,73));interaction=all(r['net_instances']>=1 for r in interactions);check([stable,order,interaction]==[s['stability_gate'],s['D_order_gate'],s['interaction_gate']]);check(len(intervals)==34)
 return dict(schema='064-public-paper-tables-v1',replication063=dict(conditions=conditions,paired=paired,interactions=interactions,source_profile=s['source_profile'],intervals=intervals,extra_intervals=extra,seed_summary=seed_summary,seed_aggregates=aggregates,gates=dict(stability=stable,D_order=order,interaction=interaction)),anchors060=sources['060']['conditions'],anchors061=dict(conditions=sources['061']['conditions'],coverage=sources['061']['coverage'],geometry=sources['061']['geometry']),anchors062=dict(conditions=sources['062']['conditions'],paired=sources['062']['paired'],subsets=sources['062']['subsets']),provenance=dict(task060='876ededdcaa4038363fc92f9761462c42435e41c',task061='e5e479d27a5ac4f9b05f931e0602340ea6d006a7',task062='be8076782d2a813af131eff6d8dddb9fc0450e9d',task063='e91a6951a610c21453fac3723ef135afd603aeae',inputs='docs/codex-artifacts/{task}/execution-summary.json and corresponding CSVs',same_cached_data_not_extra_samples=True),arithmetic_checks=checks)
def figures(tables,paper,b0_pass):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','axes.spines.right':False,'axes.spines.top':False,'legend.frameon':False,'axes.linewidth':.8})
 paper=Path(paper);out=paper/'figures';out.mkdir(exist_ok=True);s=tables['replication063'];rows=[next(r for r in s['seed_summary'] if r['seed']==seed and r['split']==SOURCE) for seed in ALL];C='#7C97AF';D='#3A8D88';saved=[]
 def finish(fig,name):
  fig.savefig(out/(name+'.svg'),facecolor='white',bbox_inches='tight');fig.savefig(out/(name+'.png'),dpi=300,facecolor='white',bbox_inches='tight');plt.close(fig);ET.parse(out/(name+'.svg'));body=(out/(name+'.png')).read_bytes();assert body[:8]==b'\x89PNG\r\n\x1a\n';w,h=struct.unpack('>II',body[16:24]);assert w>=1500 and h>=900;saved.append(dict(name=name,png_width=w,png_height=h,svg_parsed=True))
 fig,ax=plt.subplots(figsize=(7.2,4.1),layout='constrained');x=list(range(8));ax.axvspan(-.6,1.5,color='#eeeeee',zorder=0)
 ax.bar([v-.18 for v in x],[r['C_correct']*2 for r in rows],.34,color=C,label='C: centered');ax.bar([v+.18 for v in x],[r['D_correct']*2 for r in rows],.34,color=D,label='D: role contrast')
 ax.axhline(20,color='#555555',linestyle='--',linewidth=1);ax.text(7.7,20,'Fixed target 20%',va='center',fontsize=7.5,bbox=dict(facecolor='white',edgecolor='none',pad=1));mean=sum(r['D_correct'] for r in rows[2:])/6*2;ax.axhline(mean,color=D,linestyle=':',linewidth=1.2);ax.text(7.7,mean,'New-six D mean\n17.67%',va='top',fontsize=7.2,color=D,bbox=dict(facecolor='white',edgecolor='none',pad=1))
 if b0_pass:
  b0=next(r for r in tables['anchors060'] if r['method']=='B0' and r['split']==SOURCE)['four_way_accuracy']*100;ax.axhline(b0,color='#B7855E',linestyle='-.',linewidth=1);ax.text(7.7,b0,'B0 single set 14%',va='top',fontsize=7.2,color='#996D48')
 ax.set(xticks=x,xticklabels=[str(v)+('\ncached' if i<2 else '\nnew') for i,v in enumerate(ALL)],ylabel='Four-way accuracy (%)',xlabel='Optimization seed; same 50 instances per seed',ylim=(0,40),xlim=(-.6,10));ax.set_title('All seeds: relative gain and an unmet absolute target',loc='left',fontsize=10);ax.legend(loc='upper right',ncol=2);finish(fig,'fig1-seed-accuracy')
 fig,ax=plt.subplots(figsize=(7.2,4.9),layout='constrained');y=list(range(8));pairs=[next(r for r in s['paired'] if (r['seed'],r['left'],r['right'])==(seed,'D_NATIVE','C_NATIVE')) for seed in ALL]
 for i,r in enumerate(pairs):ax.errorbar(r['delta_four_way_pp'],i,xerr=[[r['delta_four_way_pp']-r['answer_ci_low_pp']],[r['answer_ci_high_pp']-r['delta_four_way_pp']]],fmt='o',color='#8193A4' if i<2 else D,capsize=3,markersize=4)
 labels=[f'{v} '+('(old cached)' if i<2 else '(new)') for i,v in enumerate(ALL)]
 for j,kind in enumerate(('new_six_family','new_six_seed'),9):
  r=next(r for r in s['extra_intervals'] if r['kind']==kind and r['metric']=='answer');ax.errorbar(r['estimate_pp'],j,xerr=[[r['estimate_pp']-r['ci_low_pp']],[r['ci_high_pp']-r['estimate_pp']]],fmt='s' if j==9 else 'D',color='#315E8C' if j==9 else '#B07F50',capsize=4,markersize=4);y.append(j);labels.append('New-six mean: family CI' if j==9 else 'New-six mean: seed CI')
 ax.axvline(0,color='#555555',linestyle='--',linewidth=.8);ax.axhline(8,color='#dddddd');ax.set(yticks=y,yticklabels=labels,xlabel='D minus C four-way accuracy (percentage points)',xlim=(-15,45),ylim=(10.7,-.7));ax.set_title('Paired differences: 95% intervals, distinct uncertainty axes',loc='left',fontsize=10);finish(fig,'fig2-paired-intervals')
 fig,(ax,bx)=plt.subplots(1,2,figsize=(7.2,3.7),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
 for j,m in enumerate(('C_NATIVE','D_NATIVE','C_HASH','D_HASH')):
  values=[next(r['four_way_correct']*2 for r in s['conditions'] if (r['method'],r['seed'],r['split'])==(m,seed,SOURCE)) for seed in (19,73)];ax.bar([i+(j-1.5)*.18 for i in (0,1)],values,width=.17,color=C if m[0]=='C' else D,hatch='//' if m.endswith('HASH') else None,edgecolor='white',label=m.replace('_',' '))
 ax.set(xticks=[0,1],xticklabels=['19','73'],xlabel='Original optimization seed',ylabel='Four-way accuracy (%)',ylim=(0,40));ax.set_title('(a) Full C/D x order control',loc='left',fontsize=9);ax.legend(fontsize=6.4,loc='upper right')
 for i,r in enumerate(s['interactions']):bx.errorbar(r['delta_pp'],i,xerr=[[r['delta_pp']-r['ci_low_pp']],[r['ci_high_pp']-r['delta_pp']]],fmt='o',color=D,capsize=4)
 bx.axvline(0,color='#555555',linestyle='--',linewidth=.8);bx.set(yticks=[0,1],yticklabels=['19','73'],xlabel='Interaction Delta (pp)',xlim=(-20,40),ylim=(1.5,-.5));bx.set_title('(b) Interaction; family 95% CI',loc='left',fontsize=9);finish(fig,'fig3-role-order');return saved
def public(repo,paper,root,bridge_report):
 start=time.monotonic();paper=Path(paper);root=Path(root);paper.mkdir(parents=True,exist_ok=True);t=public_tables(repo);pass_b0=Path(bridge_report).exists() and '\nStatus: PASS\n' in Path(bridge_report).read_text(encoding='utf-8');t['b0_bridge_pass']=pass_b0;write(paper/'tables.json',t)
 try:figs=figures(t,paper,pass_b0);state='GENERATED'
 except ImportError:figs=[];state='FIGURES_NOT_GENERATED'
 write(root/'public-generation.json',dict(status='PASS',arithmetic_checks=t['arithmetic_checks'],figures_status=state,figures=figs,b0_reference_drawn=pass_b0,outer_s=time.monotonic()-start,torch_imported='torch' in __import__('sys').modules));print('PUBLIC_TABLES_AND_FIGURES',state,t['arithmetic_checks'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True);b=sub.add_parser('bridge');b.add_argument('--root',required=True);b.add_argument('--prior063',required=True);b.add_argument('--prior060',required=True);b.add_argument('--report',required=True);g=sub.add_parser('public');g.add_argument('--repo',required=True);g.add_argument('--paper',required=True);g.add_argument('--root',required=True);g.add_argument('--bridge-report',required=True);a=vars(p.parse_args());mode=a.pop('mode');globals()[mode](**a)
