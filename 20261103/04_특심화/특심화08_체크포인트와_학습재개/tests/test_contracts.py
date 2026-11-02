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


def checkpoint_objects():
    model=RecurrentModel('LSTM',3,4,2); optimizer=torch.optim.Adam(model.parameters(),lr=.01)
    scheduler=torch.optim.lr_scheduler.StepLR(optimizer,2,.5); gen=torch.Generator().manual_seed(12)
    return model,optimizer,scheduler,gen

def test_checkpoint_roundtrip_and_rng(tmp_path):
    torch.manual_seed(5); random.seed(5); np.random.seed(5)
    model,opt,sch,gen=checkpoint_objects(); config={'seed':5}; path=tmp_path/'a.pt'
    loss=model(torch.randn(2,4,3),torch.tensor([4,3])).square().mean(); loss.backward(); opt.step(); sch.step(); opt.zero_grad(set_to_none=True)
    saved=deepcopy(model.state_dict()); saved_opt=deepcopy(opt.state_dict())
    save_checkpoint(path,model,opt,sch,gen,1,[{'epoch':1}],config,'abc')
    expected=(torch.rand(3),torch.randperm(5,generator=gen),random.random(),np.random.rand())
    with torch.no_grad():
        for p in model.parameters(): p.add_(1)
    epoch,history=load_checkpoint(path,model,opt,sch,gen,config,'abc')
    actual=(torch.rand(3),torch.randperm(5,generator=gen),random.random(),np.random.rand())
    assert epoch==1 and history==[{'epoch':1}] and identical(saved,model.state_dict()) and identical(saved_opt,opt.state_dict())
    assert identical(expected,actual)

@pytest.mark.parametrize('field',['config','data'])
def test_checkpoint_reject_before_mutation(tmp_path,field):
    model,opt,sch,gen=checkpoint_objects(); path=tmp_path/'a.pt'
    save_checkpoint(path,model,opt,sch,gen,0,[],{'seed':42},'abc')
    state=deepcopy(model.state_dict()); rng=torch.get_rng_state().clone()
    with pytest.raises(ValueError): load_checkpoint(path,model,opt,sch,gen,{'seed':43} if field=='config' else {'seed':42},'wrong' if field=='data' else 'abc')
    assert identical(state,model.state_dict()) and torch.equal(rng,torch.get_rng_state())

def test_epoch_sample_weighted():
    torch.manual_seed(9); model=RecurrentModel('RNN',3,4,2)
    x=torch.randn(11,4,3); lengths=torch.full((11,),4); y=torch.tensor([0,1,0,0,1,1,1,0,1,1,0])
    with torch.no_grad(): expected=nn.CrossEntropyLoss()(model(x,lengths),y).item()
    loader=DataLoader(TensorDataset(x,lengths,y,torch.arange(11)),batch_size=4,shuffle=False)
    loss,order=train_epoch(model,loader,torch.optim.SGD(model.parameters(),lr=0))
    assert loss==pytest.approx(expected,rel=1e-6) and order==list(range(11))

def test_empty_epoch():
    model=RecurrentModel('RNN',3,4,2)
    with pytest.raises(ValueError): train_epoch(model,[],torch.optim.SGD(model.parameters(),lr=0))

from models import RecurrentModel

def test_checkpoint_requires_boundary(tmp_path):
    m,o,s,g=checkpoint_objects();next(m.parameters()).grad=torch.ones_like(next(m.parameters()))
    with pytest.raises(ValueError):save_checkpoint(tmp_path/'bad.pt',m,o,s,g,0,[],{},'hash')

def test_failed_load_rolls_back(tmp_path):
    m,o,s,g=checkpoint_objects();path=tmp_path/'a.pt';save_checkpoint(path,m,o,s,g,0,[],{},'hash')
    p=torch.load(path,weights_only=True);p['optimizer']['param_groups']=[];torch.save(p,path)
    state=deepcopy(m.state_dict());rng=capture_rng();old_opt=deepcopy(o.state_dict())
    with pytest.raises(ValueError):load_checkpoint(path,m,o,s,g,{},'hash')
    assert identical(state,m.state_dict()) and identical(rng,capture_rng()) and identical(old_opt,o.state_dict())
