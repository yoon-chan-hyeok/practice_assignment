from pathlib import Path
import json
import torch
import pandas as pd
BASE=Path(__file__).resolve().parent
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)

import copy
from torch import nn
from tasks import group_microbatches,accumulated_step
rows=[]
for sizes in ([16,16,16,16],[17,13],[9]):
    torch.manual_seed(42);n=sum(sizes)
    X=torch.randn(n,2,dtype=torch.float64);y=torch.arange(n)%2
    large=nn.Sequential(nn.Linear(2,8),nn.Tanh(),nn.Linear(8,2)).double();small=copy.deepcopy(large)
    a=torch.optim.SGD(large.parameters(),lr=.03,momentum=.9)
    b=torch.optim.SGD(small.parameters(),lr=.03,momentum=.9)
    a.zero_grad(set_to_none=True);loss=nn.functional.cross_entropy(large(X),y);loss.backward()
    refgrad=[p.grad.clone() for p in large.parameters()];a.step()
    batches=list(zip(X.split(sizes),y.split(sizes)))
    result=accumulated_step(small,b,batches)
    gd=max(float((p-q).abs().max()) for p,q in zip(refgrad,result['gradients']))
    pdiff=max(float((p-q).abs().max().detach()) for p,q in zip(large.parameters(),small.parameters()))
    rows.append(dict(sizes=list(sizes),samples=result['samples'],gradient_close=gd<1e-10,parameter_close=pdiff<1e-10))
(OUT/'accumulation_report.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
print('9개 micro-batch의 묶음:',[len(g) for g in group_microbatches([(None,None)]*9,4)])
