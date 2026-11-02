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
from models import RecurrentModel,classifier


@pytest.mark.parametrize('training',[False,True])
def test_benchmark_preserves_state(training):
    torch.manual_seed(5); model=classifier('Transformer'); model.train()
    x=torch.randn(3,8,3); lengths=torch.tensor([8,5,6]); before=deepcopy(model.state_dict())
    for p in model.parameters(): p.grad=torch.ones_like(p)
    gradients=[p.grad.clone() for p in model.parameters()]; rng=torch.get_rng_state().clone()
    result=measure(model,x,lengths,repeats=2,warmup=1,training=training)
    assert result['seconds']>0 and result['samples_s']==pytest.approx(6/result['seconds']) and result['peak_vram_bytes'] is None
    assert model.training and identical(before,model.state_dict()) and torch.equal(rng,torch.get_rng_state())
    assert all(torch.equal(g,p.grad) for g,p in zip(gradients,model.parameters()))

def test_benchmark_restores_on_error():
    class Broken(nn.Module):
        def __init__(self): super().__init__(); self.p=nn.Parameter(torch.ones(1))
        def forward(self,x,lengths): torch.rand(1); raise RuntimeError('intentional')
    model=Broken().eval(); rng=torch.get_rng_state().clone()
    with pytest.raises(RuntimeError): measure(model,torch.zeros(1,2,3),torch.tensor([2]),training=True)
    assert not model.training and torch.equal(rng,torch.get_rng_state()) and model.p.grad is None

@pytest.mark.skipif(not torch.cuda.is_available(),reason='Actual CUDA GPU required')
def test_cuda_benchmark():
    model=classifier('LSTM').cuda(); x=torch.randn(3,8,3,device='cuda')
    row=measure(model,x,torch.tensor([8,6,7]),repeats=2,training=True)
    assert row['seconds']>0 and row['peak_vram_bytes']>0

from models import classifier,RecurrentModel

def test_profile_workload_preserves():
    m=classifier('LSTM').train();x=torch.randn(2,4,3);l=torch.tensor([4,3]);s=deepcopy(m.state_dict());rng=capture_rng()
    loss=profile_workload(m,x,l,torch.device('cpu'))
    assert np.isfinite(loss) and identical(s,m.state_dict()) and identical(rng,capture_rng()) and all(p.grad is None for p in m.parameters())

def test_aggregate_scope_and_std():
    base=dict(model='RNN',length=16,scope='forward_only',device='cpu',batch=4,repeats=3,warmup=1)
    rows=[dict(base,seconds=s) for s in [1.,3.]]+[dict(base,scope='forward+backward',seconds=2.)]
    out=summarize_runs(rows);assert len(out)==2
    forward=next(r for r in out if r['scope']=='forward_only');assert forward['mean_seconds']==2 and forward['std_seconds']==pytest.approx(2**.5)
    assert next(r for r in out if r['scope']!='forward_only')['std_seconds'] is None

def test_aggregate_reject_nonfinite():
    with pytest.raises(ValueError):summarize_runs([])
    with pytest.raises(ValueError):summarize_runs([dict(model='RNN',length=2,scope='forward',device='cpu',batch=1,repeats=1,warmup=0,seconds=float('nan'))])
