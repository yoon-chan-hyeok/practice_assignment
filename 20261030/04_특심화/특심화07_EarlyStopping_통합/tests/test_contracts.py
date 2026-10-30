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
    def test_stop_and_observed_best(self):
        m=nn.Linear(1,1);s=tasks.EarlyStop(2,.05);flags=[]
        for e,loss in enumerate([1.,.8,.79,.78],1):
            with torch.no_grad():m.weight.fill_(e)
            flags.append(s.update(loss,e,m))
        self.assertEqual(flags,[False,False,False,True]);self.assertEqual(s.best_epoch,4);self.assertEqual(s.best_loss,.78)
        self.assertEqual(s.reference,.8)
    def test_best_deep_copy_and_restore(self):
        m=nn.Linear(1,1);s=tasks.EarlyStop();s.update(.8,1,m);saved=copy.deepcopy(m.state_dict())
        with torch.no_grad():m.weight.add_(20)
        tasks.restore_best(m,s);self.assertTrue(equal_nested(saved,m.state_dict()))
        with torch.no_grad():m.weight.add_(10)
        self.assertTrue(equal_nested(saved,s.best_state))
    def test_invalid_update_atomic(self):
        m=nn.Linear(1,1);s=tasks.EarlyStop();s.update(.8,1,m);before=s.state_dict()
        for value,epoch in [(float('nan'),2),(.1,1),(.1,True)]:
            with self.assertRaises(ValueError):s.update(value,epoch,m)
            self.assertTrue(equal_nested(before,s.state_dict()))
    def test_weighted_mean_not_batch_mean(self):
        m=nn.Identity();x=torch.tensor([[2.,0.],[0.,2.],[1.,0.]]);y=torch.tensor([0,1,1])
        r=tasks.evaluate_batches(m,[(x[:2],y[:2]),(x[2:],y[2:])])
        self.assertAlmostEqual(r['loss'],float(nn.functional.cross_entropy(x,y)),places=6)
        self.assertEqual(r['samples'],3);self.assertAlmostEqual(r['accuracy'],2/3)
    def test_evaluation_preserves_bn_and_gradients(self):
        m=nn.Sequential(nn.Linear(2,4),nn.BatchNorm1d(4),nn.Dropout(.3),nn.Linear(4,2));m.train();m[1].eval()
        for p in m.parameters():p.grad=torch.ones_like(p)
        before=copy.deepcopy(m.state_dict());modes=[x.training for x in m.modules()];grads=[p.grad.clone() for p in m.parameters()]
        tasks.evaluate_batches(m,[(torch.ones(3,2),torch.zeros(3,dtype=torch.long))])
        self.assertTrue(equal_nested(before,m.state_dict()));self.assertEqual(modes,[x.training for x in m.modules()])
        self.assertTrue(all(torch.equal(p.grad,g) for p,g in zip(m.parameters(),grads)))
    def test_empty_and_forward_failure(self):
        m=nn.Linear(2,2);m.train()
        with self.assertRaises(ValueError):tasks.evaluate_batches(m,[])
        with self.assertRaises(RuntimeError):tasks.evaluate_batches(m,[(torch.ones(2,3),torch.zeros(2,dtype=torch.long))])
        self.assertTrue(m.training)
        with self.assertRaises(ValueError):tasks.restore_best(m,tasks.EarlyStop())

if __name__=='__main__': unittest.main()
