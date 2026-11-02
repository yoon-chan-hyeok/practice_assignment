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


@pytest.mark.parametrize('seed',[1,5,42])
def test_rnn_values_and_gradients(seed):
    torch.manual_seed(seed); ref=nn.RNN(3,4,batch_first=True).double(); cell=nn.RNNCell(3,4).double()
    with torch.no_grad():
        for name,p in cell.named_parameters(): p.copy_(getattr(ref,name+'_l0'))
    x=torch.randn(2,5,3,dtype=torch.float64,requires_grad=True); h=torch.randn(2,4,dtype=torch.float64,requires_grad=True)
    x2=x.detach().clone().requires_grad_(); h2=h.detach().clone().requires_grad_()
    a,ha=ref(x,h[None]); b,hb=unroll_rnn(cell,x2,h2)
    torch.testing.assert_close(a,b,atol=1e-9,rtol=1e-7); torch.testing.assert_close(ha[0],hb,atol=1e-9,rtol=1e-7)
    (a.square().sum()+ha.sum()).backward(); (b.square().sum()+hb.sum()).backward()
    torch.testing.assert_close(x.grad,x2.grad,atol=1e-9,rtol=1e-7); torch.testing.assert_close(h.grad,h2.grad,atol=1e-9,rtol=1e-7)
    for name,p in cell.named_parameters(): torch.testing.assert_close(p.grad,getattr(ref,name+'_l0').grad,atol=1e-9,rtol=1e-7)

def test_rnn_empty():
    with pytest.raises(ValueError): unroll_rnn(nn.RNNCell(3,4),torch.zeros(2,0,3))

def test_copy_preserves_parameters_and_source():
    ref=nn.RNN(3,4,batch_first=True);cell=nn.RNNCell(3,4);state=deepcopy(ref.state_dict());ids=[id(p) for p in cell.parameters()]
    assert copy_rnn_weights(ref,cell) is cell
    assert ids==[id(p) for p in cell.parameters()] and identical(state,ref.state_dict())
    for name,p in cell.named_parameters():
        q=getattr(ref,name+'_l0');assert torch.equal(p,q) and p.data_ptr()!=q.data_ptr()
def test_copy_unsupported_before_change():
    ref=nn.RNN(3,4,num_layers=2);cell=nn.RNNCell(3,4);state=deepcopy(cell.state_dict())
    with pytest.raises(ValueError):copy_rnn_weights(ref,cell)
    assert identical(state,cell.state_dict())
