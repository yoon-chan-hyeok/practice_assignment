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




from models import classifier

def make_loader():
    torch.manual_seed(40);x=torch.randn(11,6,3);l=torch.tensor([6,5,4,3,6,5,4,3,6,5,4]);y=torch.arange(11)%2
    return x,l,y,DataLoader(TensorDataset(x,l,y,torch.arange(11)),batch_size=4,shuffle=False)

def test_weighted_loss_order_and_state():
    x,l,y,loader=make_loader();m=classifier('LSTM').train();m.head.eval()
    for p in m.parameters():p.grad=torch.ones_like(p)
    states=deepcopy(m.state_dict());g=[p.grad.clone() for p in m.parameters()];modes=[z.training for z in m.modules()];rng=capture_rng()
    with torch.no_grad():expected=nn.CrossEntropyLoss()(m(x,l),y).item()
    r=evaluate_batches(m,loader)
    assert r['loss']==pytest.approx(expected,rel=1e-6) and r['ids']==list(range(11))
    assert identical(states,m.state_dict()) and identical(rng,capture_rng()) and modes==[z.training for z in m.modules()]
    assert all(torch.equal(a,p.grad) for a,p in zip(g,m.parameters()))
@pytest.mark.parametrize('name',['RNN','LSTM','Transformer'])
def test_padding_invariant(name):
    x,l,y,_=make_loader();m=classifier(name).train();r=check_padding_invariance(m,x,l)
    assert r['unchanged'] and r['padded_positions']>0 and m.training

def test_empty_loader_restores():
    m=classifier('RNN').train();m.head.eval();modes=[z.training for z in m.modules()]
    with pytest.raises(ValueError):evaluate_batches(m,[])
    assert modes==[z.training for z in m.modules()]

def test_error_restores_state():
    class Broken(nn.Module):
        def __init__(self):super().__init__();self.p=nn.Parameter(torch.ones(1))
        def forward(self,x,l):self.p.data.add_(1);torch.rand(1);raise RuntimeError('probe')
    m=Broken().eval();rng=capture_rng()
    with pytest.raises(RuntimeError):evaluate_batches(m,[(torch.zeros(1,2,3),torch.tensor([2]),torch.tensor([0]),torch.tensor([0]))])
    assert m.p.item()==1 and not m.training and identical(rng,capture_rng())
