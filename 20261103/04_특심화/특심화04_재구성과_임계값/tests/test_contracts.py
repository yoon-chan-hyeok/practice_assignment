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


def test_masked_mse_weighting_gradient():
    pred=torch.tensor([[[2.],[4.],[100.]],[[6.],[100.],[100.]]],requires_grad=True)
    target=torch.zeros_like(pred); mask=torch.tensor([[False,False,True],[False,True,True]])
    loss=masked_mse(pred,target,mask); assert loss.item()==pytest.approx(56/3)
    loss.backward(); assert torch.equal(pred.grad[mask],torch.zeros_like(pred.grad[mask]))

@pytest.mark.parametrize('case',['empty','all','shape','dtype'])
def test_masked_mse_reject(case):
    a=torch.zeros(2,3,4); b=a.clone(); mask=torch.zeros(2,3,dtype=torch.bool)
    if case=='empty': a=b=torch.zeros(2,0,4); mask=torch.zeros(2,0,dtype=torch.bool)
    if case=='all': mask[:]=True
    if case=='shape': b=torch.zeros(2,3,3)
    if case=='dtype': mask=mask.float()
    with pytest.raises((ValueError,TypeError)): masked_mse(a,b,mask)

def test_threshold_policy():
    errors=torch.tensor([.1,.2,.6,.8]); labels=torch.tensor([0,0,1,1])
    best,rows=choose_threshold(errors,labels)
    assert best['f1']==1 and .2<best['threshold']<.6
    assert all(set(r)=={'threshold','f1','tp','fp','fn'} for r in rows)
    changed,other=choose_threshold(errors,labels); assert best==changed and rows==other

@pytest.mark.parametrize('bad',['single','nan','negative','shape'])
def test_threshold_invalid(bad):
    e=torch.tensor([.1,.2]); y=torch.tensor([0,1])
    if bad=='single': y[:]=0
    if bad=='nan': e[0]=float('nan')
    if bad=='negative': e[0]=-1
    if bad=='shape': y=y[:1]
    with pytest.raises(ValueError): choose_threshold(e,y)

def test_padding_nan_is_excluded():
    p=torch.tensor([[[2.],[float('nan')]]],requires_grad=True);t=torch.tensor([[[0.],[float('nan')]]])
    loss=masked_mse(p,t,torch.tensor([[False,True]]));assert loss==4;loss.backward()
    assert p.grad[0,1,0]==0 and p.grad[0,0,0]==4
def test_valid_nan_rejected():
    with pytest.raises(ValueError):masked_mse(torch.full((1,1,1),float('nan')),torch.zeros(1,1,1),torch.zeros(1,1,dtype=torch.bool))
def test_threshold_tie_and_purity():
    e=torch.tensor([.1,.1,.2,.2]);y=torch.tensor([0,1,0,1]);before=e.clone();best,rows=choose_threshold(e,y)
    assert best==max(rows,key=lambda r:(r['f1'],r['threshold'])) and torch.equal(e,before)
