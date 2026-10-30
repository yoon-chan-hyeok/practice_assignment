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
    def test_optimizer_settings(self):
        m=nn.Linear(2,2);m.bias.requires_grad_(False)
        for kind in ('sgd','adamw'):
            o=tasks.make_optimizer(m.parameters(),kind,.01,0.)
            self.assertEqual(len(o.param_groups[0]['params']),1);self.assertIs(o.param_groups[0]['params'][0],m.weight)
            self.assertEqual(o.param_groups[0]['weight_decay'],0.)
        self.assertEqual(tasks.make_optimizer(m.parameters(),'sgd',.1).defaults['momentum'],.9)
    def test_factory_does_not_update(self):
        torch.manual_seed(42);m=nn.Linear(2,2);s=copy.deepcopy(m.state_dict());rng=torch.get_rng_state().clone()
        tasks.make_optimizer(m.parameters(),'adamw',.01)
        self.assertTrue(equal_nested(s,m.state_dict()));self.assertTrue(torch.equal(rng,torch.get_rng_state()))
    def test_bad_optimizer(self):
        for kind,lr,wd in [('other',.01,0.),('sgd',0.,0.),('adamw',float('nan'),0.),('adamw',.1,-1.)]:
            with self.assertRaises(ValueError):tasks.make_optimizer(nn.Linear(2,2).parameters(),kind,lr,wd)
        with self.assertRaises(ValueError):tasks.make_optimizer([],'sgd',.1)
    def test_summary_numbers(self):
        rows=[dict(setting=a,seed=s,best_valid_loss=v) for a in ['b','a'] for s,v in [(2,1.),(1,3.)]];before=copy.deepcopy(rows)
        df=tasks.summarize_runs(rows)
        self.assertEqual(df.setting.tolist(),['a','b']);self.assertEqual(df.n.tolist(),[2,2])
        np.testing.assert_allclose(df['mean'],[2.,2.]);np.testing.assert_allclose(df['std'],[math.sqrt(2)]*2)
        self.assertEqual(before,rows)
    def test_summary_rejects_unpaired_and_duplicate(self):
        rows=[dict(setting='a',seed=i,best_valid_loss=.1) for i in [1,2]]
        for bad in [[],rows+rows,rows+[dict(setting='b',seed=3,best_valid_loss=.2)],rows[:1]]:
            with self.assertRaises(ValueError):tasks.summarize_runs(bad)
    def test_summary_rejects_nonfinite(self):
        with self.assertRaises(ValueError):tasks.summarize_runs([dict(setting='a',seed=s,best_valid_loss=float('inf')) for s in [1,2]])

if __name__=='__main__': unittest.main()
