from pathlib import Path
import sys,copy,math,unittest,tempfile,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
import pandas as pd
import numpy as np
import tasks

torch.set_num_threads(1)
def equal_nested(a,b):
    if isinstance(a,torch.Tensor): return isinstance(b,torch.Tensor) and a.dtype==b.dtype and torch.equal(a,b)
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(equal_nested(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return len(a)==len(b) and all(equal_nested(x,y) for x,y in zip(a,b))
    return a==b

class Contracts(unittest.TestCase):
    def test_grouping(self):
        b=[(object(),object()) for _ in range(9)];g=tasks.group_microbatches(iter(b),4)
        self.assertEqual([len(x) for x in g],[4,4,1]);self.assertIs(g[0][0][0],b[0][0])
        self.assertEqual(tasks.group_microbatches([],4),[])
    def test_bad_groups(self):
        for n in [0,-1,True,1.5]:
            with self.assertRaises(ValueError):tasks.group_microbatches([],n)
    def check_equivalent(self,sizes):
        torch.manual_seed(13);n=sum(sizes);X=torch.randn(n,3,dtype=torch.float64);y=torch.arange(n)%2
        a=nn.Sequential(nn.Linear(3,7),nn.Tanh(),nn.Linear(7,2)).double();b=copy.deepcopy(a)
        oa=torch.optim.SGD(a.parameters(),lr=.03,momentum=.9);ob=torch.optim.SGD(b.parameters(),lr=.03,momentum=.9)
        # 이전 gradient가 있어도 현재 그룹만으로 다시 계산하는지 확인합니다.
        for p in b.parameters():p.grad=torch.ones_like(p)
        oa.zero_grad(set_to_none=True);loss=nn.functional.cross_entropy(a(X),y);loss.backward();grad=[p.grad.clone() for p in a.parameters()];oa.step()
        result=tasks.accumulated_step(b,ob,list(zip(X.split(sizes),y.split(sizes))))
        self.assertAlmostEqual(result['loss'],loss.item(),places=10);self.assertEqual(result['samples'],n)
        for x,z in zip(grad,result['gradients']):torch.testing.assert_close(x,z,atol=1e-10,rtol=1e-8)
        for x,z in zip(a.parameters(),b.parameters()):torch.testing.assert_close(x,z,atol=1e-10,rtol=1e-8)
        for pa,pb in zip(a.parameters(),b.parameters()):torch.testing.assert_close(oa.state[pa]['momentum_buffer'],ob.state[pb]['momentum_buffer'],atol=1e-10,rtol=1e-8)
    def test_equal_microbatches(self):self.check_equivalent([16]*4)
    def test_unequal_microbatches(self):self.check_equivalent([17,13])
    def test_final_small_group(self):self.check_equivalent([3])
    def test_reject_batch_dependent_models(self):
        for m in [nn.Sequential(nn.Linear(2,2),nn.BatchNorm1d(2)),nn.Sequential(nn.Linear(2,2),nn.Dropout(.3))]:
            with self.assertRaises(ValueError):tasks.accumulated_step(m,torch.optim.SGD(m.parameters(),lr=.1),[(torch.ones(4,2),torch.zeros(4,dtype=torch.long))])
    def test_empty_no_update(self):
        m=nn.Linear(2,2);o=torch.optim.SGD(m.parameters(),lr=.1);before=copy.deepcopy(m.state_dict())
        with self.assertRaises(ValueError):tasks.accumulated_step(m,o,[])
        self.assertTrue(equal_nested(before,m.state_dict()))

if __name__=='__main__': unittest.main()
