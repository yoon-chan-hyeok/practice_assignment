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


def test_attention_padding_invariant():
    torch.manual_seed(3); module=nn.MultiheadAttention(8,2,dropout=0,batch_first=True).double()
    x=torch.randn(2,5,8,dtype=torch.float64,requires_grad=True); mask=torch.tensor([[False]*3+[True]*2,[False]*5])
    changed=x.detach().clone(); changed[mask]=1000
    a,p,w=masked_attention(module,x,mask); b,q,_=masked_attention(module,changed,mask)
    torch.testing.assert_close(a[~mask],b[~mask]); torch.testing.assert_close(p,q)
    assert w.shape==(2,2,5,5) and not w.requires_grad and w[0,:,:,3:].abs().max().item()==0
    p.square().sum().backward(); assert x.grad is not None

def test_attention_causal():
    torch.manual_seed(3); module=nn.MultiheadAttention(8,2,dropout=0,batch_first=True)
    x=torch.randn(1,6,8); mask=torch.zeros(1,6,dtype=torch.bool)
    a,_,w=masked_attention(module,x,mask,True); changed=x.clone(); changed[:,3:]+=50
    b,_,_=masked_attention(module,changed,mask,True)
    torch.testing.assert_close(a[:,:3],b[:,:3],atol=1e-5,rtol=1e-5)
    assert w.triu(1).abs().max().item()==0

@pytest.mark.parametrize('mask',[torch.ones(1,4,dtype=torch.bool),torch.zeros(1,4),torch.tensor([[False,True,False,True]])])
def test_attention_reject(mask):
    with pytest.raises((ValueError,TypeError)): masked_attention(nn.MultiheadAttention(8,2,batch_first=True),torch.randn(1,4,8),mask)

@pytest.mark.skipif(not torch.cuda.is_available(),reason='Actual CUDA GPU required')
def test_cuda_attention():
    module=nn.MultiheadAttention(8,2,batch_first=True).cuda(); x=torch.randn(2,5,8,device='cuda',requires_grad=True)
    mask=torch.zeros(2,5,dtype=torch.bool,device='cuda'); _,p,_=masked_attention(module,x,mask)
    p.sum().backward(); assert torch.isfinite(x.grad).all()

def test_head_stats_uniform():
    w=torch.full((2,2,3,3),1/3);mask=torch.zeros(2,3,dtype=torch.bool)
    rows=head_statistics(w,mask)
    assert all(r['queries']==6 and r['mean_entropy']==pytest.approx(np.log(3),rel=1e-6) for r in rows)
def test_head_stats_invalid_distribution():
    w=torch.ones(1,2,3,3);mask=torch.zeros(1,3,dtype=torch.bool)
    with pytest.raises(ValueError):head_statistics(w,mask)
