"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

import pandas as pd
ref=nn.LSTM(2,3,batch_first=True).double();cell=nn.LSTMCell(2,3).double()
with torch.no_grad():
    for n,p in cell.named_parameters():p.copy_(getattr(ref,n+'_l0'))
x=torch.randn(2,5,2,dtype=torch.float64,requires_grad=True);x2=x.detach().clone().requires_grad_()
a,(ha,ca)=ref(x);b,h,c,gates=trace_lstm(cell,x2)
for u,v in [(a,b),(ha[0],h),(ca[0],c)]:torch.testing.assert_close(u,v,atol=1e-9,rtol=1e-7)
(a.square().sum()+ha.sum()+ca.sum()).backward();(b.square().sum()+h.sum()+c.sum()).backward()
torch.testing.assert_close(x.grad,x2.grad,atol=1e-9,rtol=1e-7)
for n,p in cell.named_parameters():torch.testing.assert_close(p.grad,getattr(ref,n+'_l0').grad,atol=1e-9,rtol=1e-7)
rows=summarize_gates(gates,torch.tensor([5,3]));pd.DataFrame(rows).to_csv(OUT/'gate_summary.csv',index=False)
print(pd.DataFrame(rows).round(6).to_string(index=False));print('output/state/gradient: 일치 / 실제 시점만 gate 집계')
