"""Explicit059 CPU2x2 experiment. No task I/O, forward or training on import."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import time
import torch
from torch import nn
from torch.nn import functional as F

ARMS=('P0','P1','R0','R1')
SPLITS=('train','validation','development_test')


def save(path,data):
    with open(path,'x',encoding='utf-8') as f:
        json.dump(data,f,indent=2,sort_keys=True);f.flush();os.fsync(f.fileno())


def event(path,**record):
    with open(path,'a',encoding='utf-8') as f:
        f.write(json.dumps(record,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def head_helpers():
    spec=importlib.util.spec_from_file_location('head056',Path(__file__).with_name('question_temporal_056.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class PairHead(nn.Module):
    def __init__(self,arm):
        super().__init__()
        if arm not in ARMS:raise ValueError('ARM')
        self.arm=arm
        self.video=nn.Linear(2560,64);self.question=nn.Linear(2560,64)
        self.hidden=nn.Linear(64,64);self.a=nn.Linear(64,64,bias=False);self.b=nn.Linear(64,64,bias=False)
        self.f=nn.Linear(256,64);self.out=nn.Linear(64,1,bias=False);self.tau=nn.Parameter(torch.zeros(()))
        self.ln=nn.LayerNorm(64,eps=1e-5,elementwise_affine=False)
        if sum(p.numel() for p in self.parameters())!=356673:raise ValueError('PARAMETERS')

    def forward(self,V,q):
        if V.device.type!='cpu' or q.device.type!='cpu' or V.dtype!=torch.float32 or q.dtype!=torch.float32:raise ValueError('CPU_FLOAT32')
        if V.ndim!=3 or V.shape[1:]!=(6,2560) or q.shape!=(V.shape[0],2560):raise ValueError('FEATURE_SHAPE')
        if not torch.isfinite(V).all() or not torch.isfinite(q).all():raise ValueError('NONFINITE_INPUT')
        x=self.video(V);h=self.ln(F.gelu(x+self.hidden(self.ln(x)),approximate='none'))
        g=self.ln(F.gelu(self.question(q),approximate='none'))
        alpha=torch.softmax((h*g[:,None,:]).sum(-1)/8,dim=1)
        u=(alpha[:,:,None]*h).sum(1)
        early=self.arm[1]=='1'
        a=F.gelu(self.a(h)+(g[:,None,:] if early else 0),approximate='none')
        b=F.gelu(self.b(h)-(g[:,None,:] if early else 0),approximate='none')
        t,s=torch.triu_indices(6,6,1)
        weights=(alpha[:,t]+alpha[:,s])/5 if early else torch.full((V.shape[0],15),1/15,dtype=V.dtype)
        if self.arm[0]=='P':d=((a[:,s]-a[:,t])+(b[:,s]-b[:,t]))/2
        else:d=a[:,t]*b[:,s]-a[:,s]*b[:,t]
        raw=(weights[:,:,None]*d).sum(1)
        o=raw/torch.sqrt((raw*raw).mean(-1,keepdim=True)+1e-6)
        def f(direction):return self.out(F.gelu(self.f(torch.cat((u,direction,g,u*g),dim=-1)),approximate='none')).squeeze(-1)
        z=torch.exp(torch.clamp(self.tau,-2,2))*(f(o)-f(-o))/2
        if not torch.isfinite(z).all():raise ValueError('NONFINITE_LOGIT')
        return z


def mapped_initial(original):
    return {'video.weight':original['video.weight'].clone(),'video.bias':original['video.bias'].clone(),
        'question.weight':original['question.weight'].clone(),'question.bias':original['question.bias'].clone(),
        'hidden.weight':original['conv.weight'][:,:,0].contiguous().clone(),'hidden.bias':original['conv.bias'].clone(),
        'a.weight':original['conv.weight'][:,:,1].contiguous().clone(),'b.weight':original['conv.weight'][:,:,2].contiguous().clone(),
        'f.weight':original['mlp.0.weight'].clone(),'f.bias':original['mlp.0.bias'].clone(),
        'out.weight':original['mlp.2.weight'].clone(),'tau':original['mlp.2.bias'][0].clone()}


@torch.no_grad()
def predict(model,V,q):
    if V.shape!=(6,2560) or q.shape!=(2560,):raise ValueError('SINGLE_CELL_ONLY')
    model.eval();return int(model(V.unsqueeze(0),q.unsqueeze(0))[0]>0)


def cpu_setup():
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    if torch.cuda.is_initialized() or os.environ.get('CUDA_VISIBLE_DEVICES')!='':raise ValueError('CPU_ONLY')


def prepare(root,prior):
    cpu_setup();root=Path(root);prior=Path(prior);checks=0;assets=[]
    def check(ok):
        nonlocal checks
        if not ok:raise ValueError('INPUT_CHECK_'+str(checks))
        checks+=1
    def record(path):assets.append(dict(path=str(path),sha256=digest(path),bytes=Path(path).stat().st_size))
    check(json.loads((prior/'parent-closed.json').read_text(encoding='utf-8-sig'))['push']=='SUCCEEDED')
    check(json.loads((prior/'training-job.json').read_text(encoding='utf-8'))['active']==0)
    original_seal=json.loads((prior/'evaluation-input-seal.json').read_text(encoding='utf-8'))
    known={str(Path(x['path']).resolve()):x['sha256'] for x in original_seal['files']}
    for path in [prior/'feature-index.json',prior/'head-outputs-sealed.json',prior/'all-outputs-seal.json']:
        check(digest(path)==known[str(path.resolve())]);record(path)
    old=json.loads((prior/'head-outputs-sealed.json').read_text(encoding='utf-8'));a=[x for x in old if x['arm']=='A']
    check(len(a)==408 and all(x['status']=='CLOSED' for x in a));save(root/'a-cached-sealed.json',a)
    check(json.loads((prior/'all-outputs-seal.json').read_text(encoding='utf-8'))['outputs_sha256']==digest(prior/'head-outputs-sealed.json'))
    body=(prior/'pilot-input-seal.json').read_text(encoding='utf-8')
    body,n=re.subn(r'"labels"\s*:\s*\[\s*\[\s*[01]\s*,\s*[01]\s*\]\s*,\s*\[\s*[01]\s*,\s*[01]\s*\]\s*\]','"labels":null',body)
    check(n==51);source=json.loads(body)['selected'];record(prior/'pilot-input-seal.json');bindings={};groups={}
    for split,n in zip(SPLITS,[25,2,24]):
        path=prior/(split+'-observations.json');rows=json.loads(path.read_text(encoding='utf-8'));record(path)
        check(len(rows)==n and [r['index'] for r in rows]==list(range(n)))
        check(all(r['videos']==s['videos'] and r['questions']==s['questions'] for r,s in zip(rows,source[split])))
        save(root/(split+'-observations.json'),rows)
        bindings[split]=[dict(index=i,group_key=s['group_key']) for i,s in enumerate(source[split])];groups[split]={r['group_key'] for r in bindings[split]}
    check([len(groups[s]) for s in SPLITS]==[16,2,15])
    for s,t in [('train','validation'),('train','development_test'),('validation','development_test')]:check(not groups[s]&groups[t])
    save(root/'source-bindings.json',bindings)
    path=prior/'train-labels.json';record(path)
    with open(root/'train-labels.json','xb') as f:f.write(path.read_bytes())
    index=json.loads((prior/'feature-index.json').read_text(encoding='utf-8'));check(len(index['video'])==102 and len(index['text'])==54)
    for kind,shape in [('video',(6,2560)),('text',(2560,))]:
        for row in index[kind].values():
            path=prior/'features'/row['path'];check(digest(path)==known[str(path.resolve())]);record(path)
            value=torch.load(path,map_location='cpu',weights_only=True)
            check(value.device.type=='cpu' and value.dtype==torch.float32 and value.shape==shape and bool(torch.isfinite(value).all()))
    plans={}
    for seed in [19,73]:
        p=prior/('pretrain-seed'+str(seed)+'.pt');q=prior/'training'/('plan-'+str(seed)+'.pt')
        original=torch.load(p,map_location='cpu',weights_only=True);other=torch.load(q,map_location='cpu',weights_only=True)
        check(torch.equal(original['sequence'],other['sequence']) and original['sequence'].shape==(250,8))
        check(set(original['state'])==set(other['state']) and all(torch.equal(original['state'][k],other['state'][k]) for k in original['state']))
        record(p);record(q)
        with open(root/('original-seed'+str(seed)+'.pt'),'xb') as f:torch.save(original,f)
        mapped=mapped_initial(original['state']);check(sum(x.numel() for x in mapped.values())==356673)
        for arm in ARMS:
            model=PairHead(arm);model.load_state_dict(mapped)
            check(all(torch.equal(model.state_dict()[k],mapped[k]) for k in mapped));del model
        target=root/('mapped-seed'+str(seed)+'.pt')
        with open(target,'xb') as f:torch.save(dict(state=mapped,sequence=original['sequence']),f)
        plans[str(seed)]=dict(path=target.name,sha256=digest(target))
    for name in ['question_temporal_056.py','question_temporal_train_057.py']:
        path=Path(__file__).with_name(name);check(digest(path)==known[str(path.resolve())]);record(path)
    check(not torch.cuda.is_initialized())
    save(root/'training-config.json',dict(prior=str(prior),features=index,plans=plans,arms=ARMS,seeds=[19,73],steps=250))
    save(root/'input-seal.json',dict(status='SEALED_BEFORE_CONFIG_STARTED',assets=assets,checks=checks,
        code_lf_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        formulas='059 README exact2x2;15 t<s pairs;normalized odd readout;BCE only',parameters=356673,
        research_steps_planned=2000,software_forward_planned=24,software_cells_planned=96,fixture_updates=0))
    print('INPUT_MAPPING_SEAL_PASS',checks,flush=True)


def training(root):
    cpu_setup();root=Path(root);config=json.loads((root/'training-config.json').read_text(encoding='utf-8'));prior=Path(config['prior'])
    helper=head_helpers();index=config['features'];observations={s:json.loads((root/(s+'-observations.json')).read_text(encoding='utf-8')) for s in SPLITS}
    def v(name):return torch.load(prior/'features'/index['video'][name]['path'],map_location='cpu',weights_only=True)
    def q(text):return torch.load(prior/'features'/index['text'][text]['path'],map_location='cpu',weights_only=True)
    V=torch.stack([torch.stack([v(n) for n in r['videos']]) for r in observations['train']]);Q=torch.stack([torch.stack([q(t) for t in r['questions']]) for r in observations['train']])
    labels=torch.tensor([r['labels'] for r in json.loads((root/'train-labels.json').read_text(encoding='utf-8'))],dtype=torch.float32)
    directory=root/'training';directory.mkdir();deadline=time.monotonic()+1080;records=[];outputs=[];software=0;failed=False
    for seed in [19,73]:
        plan=torch.load(root/config['plans'][str(seed)]['path'],map_location='cpu',weights_only=True);state=plan['state'];sequence=plan['sequence']
        for arm in ARMS:
            path=directory/('059-'+arm+'-seed'+str(seed));path.mkdir()
            journal=path/'steps.jsonl';event(journal,event='STARTED',task='059',arm=arm,seed=seed,loss='BCE')
            start=time.monotonic()
            try:
                model=PairHead(arm);model.load_state_dict(state)
                if not all(torch.equal(model.state_dict()[k],state[k]) for k in state):raise ValueError('INITIAL_STATE')
                with open(path/'initial-used.pt','xb') as f:torch.save(model.state_dict(),f)
                video,text=helper.pack(V,Q,torch.tensor([0]));model.eval()
                with torch.no_grad():
                    event(path/'software.jsonl',event='STARTED',kind='original',batch_cells=4);z=model(video,text);software+=1
                    event(path/'software.jsonl',event='STARTED',kind='reversed',batch_cells=4);zr=model(video.flip(1),text);software+=1
                    event(path/'software.jsonl',event='STARTED',kind='repeated_first',batch_cells=4);zz=model(video[:,:1].expand(-1,6,-1).contiguous(),text);software+=1
                    reverse_error=float((zr+z).abs().max());zero_error=float(zz.abs().max())
                    if not bool(torch.all((zr+z).abs()<=1e-5+1e-5*z.abs())) or zero_error>1e-6:raise ValueError('SOFTWARE_SYMMETRY_FAILED')
                    save(path/'software-check.json',dict(status='PASS',forward_calls=3,cells=12,reverse_error=reverse_error,repeated_error=zero_error,
                        original=z.tolist(),reversed=zr.tolist(),repeated=zz.tolist()))
                model.train();optimizer=helper.optimizer(model)
                for step,ids in enumerate(sequence):
                    if time.monotonic()>deadline:raise TimeoutError('TRAIN_DEADLINE')
                    event(journal,event='STEP_STARTED',step=step)
                    video,text=helper.pack(V,Q,ids);logits=model(video,text).reshape(8,2,2)
                    loss=F.softplus(-(2*labels[ids]-1)*logits).mean()
                    if not torch.isfinite(loss):raise ValueError('NONFINITE_LOSS')
                    optimizer.zero_grad(set_to_none=True);loss.backward()
                    if any(p.grad is None or not torch.isfinite(p.grad).all() for p in model.parameters()):raise ValueError('PARAMETER_GRADIENT')
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1);optimizer.step()
                    event(journal,event='STEP_CLOSED',step=step,loss=float(loss.detach()))
                with open(path/'final.pt','xb') as f:torch.save(model.state_dict(),f);f.flush();os.fsync(f.fileno())
                event(journal,event='CLOSED',optimizer_steps=250)
                change=sum(float((model.state_dict()[k]-state[k]).abs().sum()) for k in state)
                for split,rows in observations.items():
                    for row in rows:
                        for vi,name in enumerate(row['videos']):
                            for qi,question in enumerate(row['questions']):
                                if time.monotonic()>deadline:raise TimeoutError('EVAL_DEADLINE')
                                outputs.append(dict(arm=arm,seed=seed,split=split,index=row['index'],video=vi,question=qi,prediction=predict(model,v(name),q(question)),status='CLOSED'))
                records.append(dict(arm=arm,seed=seed,status='CLOSED',steps=250,parameters=sum(p.numel() for p in model.parameters()),parameter_l1_change=change,
                    outer_s=time.monotonic()-start,software_forward=3,reverse_error=reverse_error,repeated_error=zero_error))
                del model
            except Exception as error:
                event(journal,event='FAILED',reason=str(error));records.append(dict(arm=arm,seed=seed,status='FAILED',reason=str(error)));failed=True
            print('CONFIG',seed,arm,records[-1]['status'],flush=True)
            if failed:break
        if failed:break
    save(root/'new-outputs-sealed.json',outputs);save(root/'training-summary.json',records)
    identities=[root/'new-outputs-sealed.json',root/'input-seal.json',Path(__file__)]+list(root.glob('mapped-seed*.pt'))+list(directory.glob('*/*.pt'))
    save(root/'outputs-identity-seal.json',dict(status='SEALED_BEFORE_SCORING',files=[dict(path=str(p),sha256=digest(p)) for p in identities],
        software_forward=software,software_cells=4*software,cuda_initialized=torch.cuda.is_initialized(),complete=not failed))
    if failed:raise RuntimeError('STARTED_CONFIGURATION_FAILED_NO_RESTART')


def bootstrap(group_values,group_sizes):
    rng=random.Random(55059);keys=sorted(group_values);values=[]
    for _ in range(10000):
        sampled=rng.choices(keys,k=15);values.append(100*sum(group_values[k] for k in sampled)/sum(group_sizes[k] for k in sampled))
    values.sort();result=[]
    for p in [.025,.975]:
        position=9999*p;i=int(position);result.append(values[i]+(position-i)*(values[min(i+1,9999)]-values[i]))
    return result


def scoring(root):
    import csv
    cpu_setup();root=Path(root);config=json.loads((root/'training-config.json').read_text(encoding='utf-8'));prior=Path(config['prior'])
    job=json.loads((root/'training-job.json').read_text(encoding='utf-8'))
    if job['active']!=0:raise RuntimeError('TRAINING_NOT_EXITED')
    for row in json.loads((root/'outputs-identity-seal.json').read_text(encoding='utf-8'))['files']:
        if digest(row['path'])!=row['sha256']:raise ValueError('OUTPUT_SEAL')
    labels={s:json.loads((prior/(s+'-labels.json')).read_text(encoding='utf-8')) for s in SPLITS}
    old=json.loads((root/'a-cached-sealed.json').read_text(encoding='utf-8'));new=json.loads((root/'new-outputs-sealed.json').read_text(encoding='utf-8'));lookup={}
    for row in old+new:
        arm='A_CACHED' if row['arm']=='A' else row['arm'];key=(row['split'],arm,row['seed'],row['index'],row['video'],row['question'])
        if key in lookup:raise ValueError('DUPLICATE_PREDICTION')
        lookup[key]=row
    original_path=Path(__file__).parent.parent/'docs/codex-artifacts/VLM-TEMPORAL-TRAIN-PILOT-057/condition-summary.csv'
    with open(original_path,encoding='utf-8',newline='') as f:baseline={(r['split'],int(r['seed'])):r for r in csv.DictReader(f) if r['arm']=='A'}
    conditions=[];four={};integers=[]
    for split,n in zip(SPLITS,[25,2,24]):
        for seed in [19,73]:
            for arm in ('A_CACHED',)+ARMS:
                row=dict(dataset='DyBench_Breakfast_059',split=split,arm=arm,seed=seed,n_instances=n,n_cells=4*n,complete_cells=0,correct_cells=0,
                    video_pair_correct=0,question_pair_correct=0,four_way_correct=0,failed_cells=0,invalid_cells=0,not_run_cells=0,unknown_cells=0,status='COMPLETE',prediction_origin='057_CACHED' if arm=='A_CACHED' else '059_NEW')
                four[split,arm,seed]=[]
                for i in range(n):
                    flags=[];unknown=False
                    for vi in [0,1]:
                        for qi in [0,1]:
                            result=lookup.get((split,arm,seed,i,vi,qi),dict(status='NOT_RUN',prediction=None));status=result['status']
                            if status=='CLOSED':row['complete_cells']+=1
                            else:
                                field={'NOT_RUN':'not_run_cells','FAILED':'failed_cells','INVALID':'invalid_cells'}.get(status,'unknown_cells');row[field]+=1;unknown=True
                            correct=int(status=='CLOSED' and result['prediction']==labels[split][i]['labels'][vi][qi]);row['correct_cells']+=correct;flags.append(correct)
                            integers.append(dict(split=split,arm=arm,seed=seed,index=i,video=vi,question=qi,status=status,correct=correct))
                    row['video_pair_correct']+=flags[0]*flags[2]+flags[1]*flags[3];row['question_pair_correct']+=flags[0]*flags[1]+flags[2]*flags[3]
                    row['four_way_correct']+=int(all(flags));four[split,arm,seed].append(None if unknown else int(all(flags)))
                if any(row[k] for k in ['failed_cells','invalid_cells','not_run_cells','unknown_cells']):row['status']='INCOMPLETE'
                if arm=='A_CACHED' and any(row[k]!=int(baseline[split,seed][k]) for k in ['n_instances','n_cells','complete_cells','correct_cells','video_pair_correct','question_pair_correct','four_way_correct','failed_cells','invalid_cells','not_run_cells']):raise ValueError('ORIGINAL_A_BINDING')
                conditions.append(row)
    bindings=json.loads((root/'source-bindings.json').read_text(encoding='utf-8'));groups={}
    for row in bindings['development_test']:groups.setdefault(row['group_key'],[]).append(row['index'])
    sizes={g:len(ids) for g,ids in groups.items()};pairs=[];profile=[];interactions=[]
    for seed in [19,73]:
        for comparator in ('A_CACHED','P0','P1','R0'):
            r=four['development_test','R1',seed];c=four['development_test',comparator,seed]
            row=dict(seed=seed,comparator=comparator,n_instances=24,r1_only=0,comparator_only=0,both_correct=0,both_wrong=0,unknown=0,net_instances='NA',delta_four_way_pp='NA',bootstrap_low_pp='NA',bootstrap_high_pp='NA')
            for a,b in zip(r,c):
                if a is None or b is None:row['unknown']+=1
                else:row['r1_only' if a and not b else 'comparator_only' if b and not a else 'both_correct' if a else 'both_wrong']+=1
            group_net={}
            for number,g in enumerate(sorted(groups)):
                item=dict(source='S'+str(number+1).zfill(2),seed=seed,comparator=comparator,n=sizes[g],r1_only=0,comparator_only=0,both_correct=0,both_wrong=0,unknown=0,net='NA')
                for i in groups[g]:
                    if r[i] is None or c[i] is None:item['unknown']+=1
                    else:item['r1_only' if r[i] and not c[i] else 'comparator_only' if c[i] and not r[i] else 'both_correct' if r[i] else 'both_wrong']+=1
                if not item['unknown']:item['net']=item['r1_only']-item['comparator_only'];group_net[g]=item['net']
                profile.append(item)
            if not row['unknown']:
                row['net_instances']=row['r1_only']-row['comparator_only'];row['delta_four_way_pp']=100*row['net_instances']/24
                row['bootstrap_low_pp'],row['bootstrap_high_pp']=bootstrap(group_net,sizes)
            pairs.append(row)
        values=[four['development_test',a,seed] for a in ['R1','R0','P1','P0']]
        interaction=dict(seed=seed,delta_instances='NA',delta_pp='NA',bootstrap_low_pp='NA',bootstrap_high_pp='NA',status='INCOMPLETE')
        if all(all(x is not None for x in value) for value in values):
            net={g:sum(values[0][i]-values[1][i]-values[2][i]+values[3][i] for i in ids) for g,ids in groups.items()}
            interaction.update(delta_instances=sum(net.values()),delta_pp=100*sum(net.values())/24,status='COMPLETE')
            interaction['bootstrap_low_pp'],interaction['bootstrap_high_pp']=bootstrap(net,sizes)
        interactions.append(interaction)
    complete=all(r['status']=='COMPLETE' for r in conditions)
    gate=complete and all(next(p for p in pairs if p['seed']==seed and p['comparator']==c)['net_instances']>=threshold for seed in [19,73] for c,threshold in [('A_CACHED',2),('P1',2),('R0',1)]) and all(x['delta_instances']>=1 for x in interactions)
    status='DIRECTED_PAIR_DEVELOPMENT_SIGNAL' if gate else 'NO_SUPPORT_FOR_THIS_DIRECTED_PAIR_RECIPE' if complete else 'INCOMPLETE'
    for name,rows in [('condition-summary.csv',conditions),('paired-summary.csv',pairs)]:
        with open(root/name,'x',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    save(root/'score-integers.json',integers);save(root/'scoring-summary.json',dict(status=status,gate=gate,complete=complete,conditions=conditions,paired=pairs,interactions=interactions,source_profile=profile))
    if torch.cuda.is_initialized():raise ValueError('SCORING_CUDA')
    print(status,'Delta',[(x['seed'],x['delta_instances']) for x in interactions],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['prepare','training','scoring']);parser.add_argument('--root',required=True);parser.add_argument('--prior')
    args=parser.parse_args()
    if args.phase=='prepare':prepare(args.root,args.prior)
    else:globals()[args.phase](args.root)
