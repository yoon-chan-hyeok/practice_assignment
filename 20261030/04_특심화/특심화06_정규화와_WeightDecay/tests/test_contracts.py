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
    def test_probe_shape_and_seen(self):
        x=torch.arange(65*4,dtype=torch.float32).reshape(65,4)/10
        r=tasks.normalization_probe(x)
        self.assertEqual(len(r),30);self.assertTrue((r.seen==64).all())
        self.assertTrue(r.loc[r.norm=='LayerNorm','running_mean_mse'].isna().all())
        self.assertLess(r.loc[r.norm=='LayerNorm','output_mean_abs'].max(),1e-4)
    def test_probe_is_repeatable_and_preserves_input(self):
        x=torch.randn(64,4);before=x.clone();a=tasks.normalization_probe(x);b=tasks.normalization_probe(x)
        pd.testing.assert_frame_equal(a,b);self.assertTrue(torch.equal(x,before))
    def test_probe_rejects_short_or_nonfinite(self):
        for x in [torch.ones(20,4),torch.ones(32,4,dtype=torch.float64),torch.full((32,4),float('nan'))]:
            with self.assertRaises(ValueError):tasks.normalization_probe(x)
    def test_group_policy_not_name(self):
        m=nn.Sequential(nn.Linear(2,4),nn.BatchNorm1d(4),nn.LayerNorm(4),nn.Linear(4,2))
        groups=tasks.decay_groups(m,.03);decay={id(p) for p in groups[0]['params']};nod={id(p) for p in groups[1]['params']}
        self.assertEqual(decay,{id(m[0].weight),id(m[3].weight)})
        self.assertEqual(decay|nod,{id(p) for p in m.parameters()});self.assertFalse(decay&nod)
        self.assertEqual([g['weight_decay'] for g in groups],[.03,0.])
    def test_shared_and_frozen(self):
        shared=nn.Linear(2,2);shared.bias.requires_grad_(False);m=nn.Sequential(shared,shared)
        groups=tasks.decay_groups(m)
        params=[p for g in groups for p in g['params']];self.assertEqual(len(params),1);self.assertIs(params[0],shared.weight)
    def test_bad_decay(self):
        for wd in [-1.,float('inf')]:
            with self.assertRaises(ValueError):tasks.decay_groups(nn.Linear(2,2),wd)

if __name__=='__main__': unittest.main()
