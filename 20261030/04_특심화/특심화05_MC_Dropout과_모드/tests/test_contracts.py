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

def make():return nn.Sequential(nn.Linear(2,8),nn.BatchNorm1d(8),nn.ReLU(),nn.Dropout(.5),nn.Linear(8,2))
class Contracts(unittest.TestCase):
    def test_only_dropout_mode(self):
        m=make();m.train();m[1].eval();before=[x.training for x in m.modules()]
        with tasks.dropout_only(m,123):
            self.assertFalse(m.training);self.assertFalse(m[1].training);self.assertTrue(m[3].training)
        self.assertEqual(before,[x.training for x in m.modules()])
    def test_state_gradient_rng_preserved(self):
        torch.manual_seed(8);m=make();m.train();m[1].eval();X=torch.randn(8,2)
        for p in m.parameters():p.grad=torch.ones_like(p)
        state=copy.deepcopy(m.state_dict());grads=[p.grad.clone() for p in m.parameters()];rng=torch.get_rng_state().clone()
        a=tasks.mc_predict(m,X,30,7);b=tasks.mc_predict(m,X,30,7)
        self.assertTrue(equal_nested(a,b));self.assertTrue(equal_nested(state,m.state_dict()))
        self.assertTrue(all(torch.equal(p.grad,g) for p,g in zip(m.parameters(),grads)))
        self.assertTrue(torch.equal(rng,torch.get_rng_state()));self.assertFalse(a['mean'].requires_grad)
    def test_probabilities_and_variance(self):
        torch.manual_seed(13);m=make();r=tasks.mc_predict(m,torch.ones(5,2),30)
        torch.testing.assert_close(r['mean'].sum(1),torch.ones(5));self.assertTrue((r['variance']>=0).all())
        self.assertGreater(float(r['variance'].sum()),0.)
    def test_no_dropout_variance(self):
        m=nn.Linear(2,2);r=tasks.mc_predict(m,torch.ones(3,2),4)
        torch.testing.assert_close(r['variance'],torch.zeros_like(r['variance']))
    def test_exception_restores_modes(self):
        m=make();m.train();m[1].eval();before=[x.training for x in m.modules()];rng=torch.get_rng_state().clone()
        with self.assertRaises(RuntimeError):
            with tasks.dropout_only(m):raise RuntimeError('probe')
        self.assertEqual(before,[x.training for x in m.modules()]);self.assertTrue(torch.equal(rng,torch.get_rng_state()))
    def test_bad_arguments(self):
        for n in [0,1,True,2.5]:
            with self.assertRaises(ValueError):tasks.mc_predict(make(),torch.ones(2,2),n)
        with self.assertRaises(ValueError):tasks.mc_predict(make(),torch.empty(0,2))
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 환경 필요')
    def test_cuda_rng_restored(self):
        m=make().cuda();X=torch.ones(3,2,device='cuda');before=torch.cuda.get_rng_state().clone()
        tasks.mc_predict(m,X,4);self.assertTrue(torch.equal(before,torch.cuda.get_rng_state()))

if __name__=='__main__': unittest.main()
