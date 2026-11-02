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


@pytest.mark.parametrize('sort',[False,True])
def test_pack_roundtrip(sort):
    seq=[torch.randn(n,3) for n in [4,2,5,4]]; x=pad_sequence(seq,batch_first=True); original=x.clone()
    packed,undo=pack_ordered(x,torch.tensor([4,2,5,4]),sort)
    padded,lengths=pad_packed_sequence(packed,batch_first=True)
    torch.testing.assert_close(padded[undo],original); assert lengths[undo].tolist()==[4,2,5,4]
    assert torch.equal(x,original) and packed.data.shape==(15,3)

@pytest.mark.parametrize('lengths',[torch.tensor([0,2]),torch.tensor([6,2]),torch.tensor([1]),torch.tensor([2.,3.])])
def test_pack_reject(lengths):
    with pytest.raises((ValueError,TypeError)): pack_ordered(torch.randn(2,5,3),lengths)

def test_inverse_restore_and_gradient():
    x=torch.randn(4,5,3,requires_grad=True); lens=torch.tensor([4,2,5,4]);p,u=pack_ordered(x,lens)
    z,l=restore_padded(p,u,5);z.sum().backward()
    mask=torch.arange(5)[None,:]<lens[:,None]
    assert torch.equal(l,lens) and torch.equal(x.grad[~mask],torch.zeros_like(x.grad[~mask]))
    assert torch.equal(x.grad[mask],torch.ones_like(x.grad[mask]))
def test_bad_inverse():
    p,u=pack_ordered(torch.randn(2,3,2),torch.tensor([3,2]))
    with pytest.raises(ValueError):restore_padded(p,torch.tensor([0,0]),3)
def test_nonfloat_rejected():
    with pytest.raises(TypeError):pack_ordered(torch.ones(2,3,2,dtype=torch.long),torch.tensor([3,2]))
