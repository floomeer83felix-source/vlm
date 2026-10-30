"""Frozen-feature temporal head and explicit CPU training; no import-time I/O.

Qwen extraction/tubelet runtime is UNVERIFIED. Fixtures are software evidence.
Only train() initiates research updates; 056 executes fixture() only (8 steps).
"""
import copy
import inspect
import json
import math
import os
from pathlib import Path
import time

import torch
from torch import nn
from torch.nn import functional as F

SEEDS=(19,73)
ARMS=('A','V','S','I')
STEPS=250


class TemporalHead(nn.Module):
    def __init__(self,dv,dq):
        super().__init__(); r=64
        if dv<=0 or dq<=0: raise ValueError('DIMENSIONS')
        self.video=nn.Linear(dv,r)
        self.question=nn.Linear(dq,r)
        self.norm=nn.LayerNorm(r,elementwise_affine=False)
        self.conv=nn.Conv1d(r,r,3,padding=1)
        self.mlp=nn.Sequential(nn.Linear(4*r,r),nn.GELU(),nn.Linear(r,1))
        count=sum(p.numel() for p in self.parameters())
        if count!=r*(dv+dq)+7*r*r+5*r+1 or count>1000000: raise ValueError('PARAMETER_COUNT')

    def forward(self,V,q):
        if V.device.type!='cpu' or q.device.type!='cpu': raise ValueError('CPU_ONLY')
        if V.ndim!=3 or q.ndim!=2 or V.shape[0]!=q.shape[0] or V.shape[1]<2: raise ValueError('INPUT_SHAPE')
        if V.dtype!=torch.float32 or q.dtype!=torch.float32 or not torch.isfinite(V).all() or not torch.isfinite(q).all(): raise ValueError('INVALID_FEATURES')
        n,t,_=V.shape
        position=torch.arange(t,dtype=V.dtype).unsqueeze(1)
        frequency=torch.exp(torch.arange(0,64,2,dtype=V.dtype)*(-math.log(10000)/64))
        encoding=torch.zeros(t,64,dtype=V.dtype)
        encoding[:,0::2]=torch.sin(position*frequency); encoding[:,1::2]=torch.cos(position*frequency)
        base=self.video(V)+encoding
        h=F.gelu(base+self.conv(self.norm(base).transpose(1,2)).transpose(1,2))
        g=F.gelu(self.question(q))
        alpha=torch.softmax((h*g[:,None,:]).sum(-1)/8,dim=1)
        u=(alpha[:,:,None]*h).sum(1)
        xi=torch.linspace(-1,1,t,dtype=V.dtype)
        o=(alpha[:,:,None]*xi[None,:,None]*h).sum(1)
        return self.mlp(torch.cat((u,o,g,u*g),dim=-1)).squeeze(-1)


def canonical_indices(y):
    if y.shape!=(8,2,2) or not torch.all((y==0)|(y==1)): raise ValueError('BATCH_LABELS')
    if not (torch.equal(y[:,0,0],y[:,1,1]) and torch.equal(y[:,0,1],y[:,1,0]) and torch.all(y[:,0,0]+y[:,0,1]==1)): raise ValueError('FOUR_CELL_RELATION')
    original=torch.arange(32).reshape(8,4)
    order=torch.tensor([1,0,3,2])
    return torch.stack([original[k] if y[k,0,0]==1 else original[k,order] for k in range(8)])


def shuffled_indices(y):
    canonical=canonical_indices(y)
    return torch.stack([canonical[(torch.arange(8)+j)%8,j] for j in range(4)],dim=1)


def objective(z,y,arm):
    if z.shape!=(8,2,2) or y.shape!=z.shape or arm not in ARMS: raise ValueError('LOSS_INPUT')
    canonical_indices(y)
    margins=(2*y-1)*z
    bce=F.softplus(-margins).mean()
    if arm=='A': return bce
    if arm=='V':
        video=F.softplus(1-(2*y[:,0,:]-1)*(z[:,0,:]-z[:,1,:])/2).mean()
        return bce+.25*video
    if arm=='S':
        values=z.reshape(-1)[shuffled_indices(y)]
        margins=values*torch.tensor([1.,-1.,-1.,1.])
    c=margins.mean(dim=tuple(range(1,margins.ndim)),keepdim=True)
    joint=F.softplus(1-c).mean()+((margins-c)**2).mean()
    return bce+.25*joint


def shared_plan(dv,dq,n,seed):
    if seed not in SEEDS or n<1: raise ValueError('PLAN')
    torch.manual_seed(seed)
    state=copy.deepcopy(TemporalHead(dv,dq).state_dict())
    generator=torch.Generator().manual_seed(seed)
    sequence=torch.randint(n,(250,8),generator=generator)
    return state,sequence


def pack(V,q,indices):
    v=V[indices]; text=q[indices]
    if v.ndim!=4 or v.shape[1]!=2 or text.ndim!=3 or text.shape[1]!=2: raise ValueError('TRAIN_FEATURE_SHAPE')
    return v[:,:,None].expand(-1,-1,2,-1,-1).reshape(-1,v.shape[-2],v.shape[-1]),text[:,None].expand(-1,2,-1,-1).reshape(-1,text.shape[-1])


def optimizer(model):
    return torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01,betas=(.9,.999),eps=1e-8)


@torch.no_grad()
def predict(model,V,q):
    """Exactly one current video and current question; no label/pair input."""
    if V.ndim!=2 or q.ndim!=1: raise ValueError('SINGLE_CELL_ONLY')
    model.eval()
    return bool(model(V.unsqueeze(0),q.unsqueeze(0))[0]>0)


def _event(path,**value):
    with open(path,'a',encoding='utf-8') as f:
        f.write(json.dumps(value,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())


def train(V,q,train_labels,arm,seed,state,sequence,output,deadline):
    """Future explicitly authorized training; no test/external labels or B0 arg.

    Existing/STARTED configurations are consumed, never resumed or restarted.
    Only final step is checkpointed. Failures persist and are re-raised.
    """
    output=Path(output); output.mkdir(exist_ok=False)
    journal=output/'steps.jsonl'
    _event(journal,event='STARTED',arm=arm,seed=seed)
    try:
        if arm not in ARMS or seed not in SEEDS or sequence.shape!=(250,8): raise ValueError('FROZEN_CONFIG')
        expected_state,expected_sequence=shared_plan(V.shape[-1],q.shape[-1],len(V),seed)
        if not torch.equal(sequence,expected_sequence) or set(state)!=set(expected_state) or any(not torch.equal(state[k],expected_state[k]) for k in state): raise ValueError('SHARED_PLAN_MISMATCH')
        model=TemporalHead(V.shape[-1],q.shape[-1]); model.load_state_dict(state); model.train(); opt=optimizer(model)
        for step,indices in enumerate(sequence):
            if time.monotonic()>deadline: raise TimeoutError('CPU_DEADLINE')
            _event(journal,event='STEP_STARTED',step=step)
            video,text=pack(V,q,indices); z=model(video,text).reshape(8,2,2)
            loss=objective(z,train_labels[indices],arm)
            if not torch.isfinite(loss): raise ValueError('NONFINITE_LOSS')
            opt.zero_grad(set_to_none=True); loss.backward()
            if any(p.grad is None or not torch.isfinite(p.grad).all() for p in model.parameters()): raise ValueError('GRADIENT')
            torch.nn.utils.clip_grad_norm_(model.parameters(),1); opt.step()
            _event(journal,event='STEP_CLOSED',step=step,loss=float(loss.detach()))
        with open(output/'final.pt','xb') as f: torch.save(model.state_dict(),f); f.flush(); os.fsync(f.fileno())
        _event(journal,event='CLOSED',optimizer_steps=250)
        return model
    except Exception as error:
        _event(journal,event='FAILED',reason=str(error)); raise


def fixture(root):
    """8 total CPU optimizer updates, synthetic features, no research claim."""
    root=Path(root); torch.set_num_threads(1); torch.set_num_interop_threads(1)
    assert not torch.cuda.is_initialized() and os.environ.get('CUDA_VISIBLE_DEVICES')==''
    checks=0; records=[]; steps=0
    def check(value):
        nonlocal checks
        assert value; checks+=1
    check(list(inspect.signature(predict).parameters)==['model','V','q'])
    check(sum(p.numel() for p in TemporalHead(2560,2560).parameters())==356673)
    torch.manual_seed(55056)
    V=torch.randn(16,2,6,8); q=torch.randn(16,2,10)
    y=torch.tensor([[[1.,0.],[0.,1.]],[[0.,1.],[1.,0.]]]*8)
    for seed in SEEDS:
        state,sequence=shared_plan(8,10,16,seed)
        check(sequence.shape==(250,8)); idx=sequence[0]; video,text=pack(V,q,idx)
        check(sorted(shuffled_indices(y[idx]).reshape(-1).tolist())==list(range(32)))
        check(torch.equal(y[idx].reshape(-1)[shuffled_indices(y[idx])],torch.tensor([1.,0.,0.,1.]).expand(8,4)))
        initial_logits=None
        for arm in ARMS:
            claim=root/('fixture-'+arm+'-'+str(seed)+'.claim'); _event(claim,event='STARTED')
            model=TemporalHead(8,10); model.load_state_dict(state); opt=optimizer(model)
            check(all(torch.equal(model.state_dict()[k],state[k]) for k in state))
            z=model(video,text).reshape(8,2,2)
            if initial_logits is None: initial_logits=z.detach().clone()
            check(torch.equal(z.detach(),initial_logits))
            loss=objective(z,y[idx],arm)
            if arm!='A': check(not torch.allclose(loss,objective(z,y[idx],'A')))
            opt.zero_grad(set_to_none=True); loss.backward()
            for p in model.parameters():
                check(p.grad is not None and bool(torch.isfinite(p.grad).all()) and bool((p.grad!=0).any()))
            torch.nn.utils.clip_grad_norm_(model.parameters(),1); opt.step(); steps+=1
            check(all(not torch.equal(model.state_dict()[k],state[k]) for k in state))
            check(isinstance(predict(model,V[0,0],q[0,0]),bool))
            _event(claim,event='CLOSED',updates=1)
            records.append(dict(arm=arm,seed=seed,parameters=sum(p.numel() for p in model.parameters()),fixture_updates=1,exposed_groups=8,exposed_cells=32))
    bad=TemporalHead(8,10)
    try: predict(bad,torch.full((6,8),float('nan')),torch.zeros(10))
    except ValueError: check(True)
    else: raise AssertionError('NONFINITE_ACCEPTED')
    _event(root/'failure-fixture.jsonl',event='STARTED')
    _event(root/'failure-fixture.jsonl',event='FAILED',reason='owned injected failure; no optimizer update')
    check(steps==8 and not torch.cuda.is_initialized())
    result=dict(status='PASS',checks=checks,fixture_optimizer_steps=steps,research_optimizer_steps=0,cuda_initialized=False,records=records,feature_runtime='UNVERIFIED')
    with open(root/'implementation.json','x') as f: json.dump(result,f,indent=2)
    print(json.dumps(result))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument('--fixture-root',required=True)
    fixture(parser.parse_args().fixture_root)
