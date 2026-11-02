"""공개 테스트: 해당 교시 요구사항의 일부를 확인한다. 정답 코드는 제공하지 않는다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import random
from copy import deepcopy
import numpy as np
import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from torch.nn.utils.rnn import pad_sequence,pad_packed_sequence
from support import identical,capture_rng
from tasks import *
torch.set_num_threads(1)


@pytest.mark.parametrize('seed',[2,8])
def test_lstm_values_and_gradients(seed):
    torch.manual_seed(seed); ref=nn.LSTM(2,3,batch_first=True).double(); cell=nn.LSTMCell(2,3).double()
    with torch.no_grad():
        for name,p in cell.named_parameters(): p.copy_(getattr(ref,name+'_l0'))
    x=torch.randn(2,4,2,dtype=torch.float64,requires_grad=True); x2=x.detach().clone().requires_grad_()
    a,(ha,ca)=ref(x); b,h,c,gates=trace_lstm(cell,x2)
    for y,z in [(a,b),(ha[0],h),(ca[0],c)]: torch.testing.assert_close(y,z,atol=1e-9,rtol=1e-7)
    (a.square().sum()+ha.sum()+ca.sum()).backward(); (b.square().sum()+h.sum()+c.sum()).backward()
    torch.testing.assert_close(x.grad,x2.grad,atol=1e-9,rtol=1e-7)
    for name,p in cell.named_parameters(): torch.testing.assert_close(p.grad,getattr(ref,name+'_l0').grad,atol=1e-9,rtol=1e-7)
    for key,value in gates.items():
        assert not value.requires_grad and value.shape==(2,4,3)
        assert bool((value<=1).all()) and bool((value>=(-1 if key=='g' else 0)).all())

def test_gate_summary_padding_excluded():
    gates={k:torch.full((2,4,3),.5) for k in ['i','f','g','o']}
    for t in gates.values():t[1,2:]=99
    rows=summarize_gates(gates,torch.tensor([4,2]));assert all(r['count']==18 and r['mean']==.5 for r in rows)
def test_gate_summary_reject_invalid():
    gates={k:torch.zeros(2,4,3) for k in ['i','f','g','o']}
    with pytest.raises(ValueError):summarize_gates(gates,torch.tensor([4,0]))
    gates['f'][0,0,0]=float('nan')
    with pytest.raises(ValueError):summarize_gates(gates,torch.tensor([4,2]))
def test_lstm_nonzero_initial_state():
    ref=nn.LSTM(2,3,batch_first=True).double();cell=nn.LSTMCell(2,3).double()
    with torch.no_grad():
        for n,p in cell.named_parameters():p.copy_(getattr(ref,n+'_l0'))
    x=torch.randn(2,3,2,dtype=torch.float64);h=torch.randn(2,3,dtype=torch.float64);c=torch.randn(2,3,dtype=torch.float64)
    a,(ha,ca)=ref(x,(h[None],c[None]));b,hb,cb,_=trace_lstm(cell,x,h,c)
    for u,v in [(a,b),(ha[0],hb),(ca[0],cb)]:torch.testing.assert_close(u,v,atol=1e-9,rtol=1e-7)
