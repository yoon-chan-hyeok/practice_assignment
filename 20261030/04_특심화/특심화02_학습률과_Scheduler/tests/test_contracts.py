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
    def build(self,kind='plateau',epochs=4):
        p=nn.Parameter(torch.ones(1));o=torch.optim.SGD([p],lr=.1)
        return o,tasks.make_scheduler(o,kind,epochs)
    def test_plateau_boundary(self):
        o,s=self.build();nexts=[]
        for value in [1.,1.,1.,1.]:
            o.step();nexts.append(tasks.advance_scheduler(s,value)['lr_next'][0])
        np.testing.assert_allclose(nexts,[.1,.1,.1,.05])
    def test_cosine_final(self):
        o,s=self.build('cosine',4);rows=[]
        for i in range(4):o.step();rows.append(tasks.advance_scheduler(s,999.))
        self.assertAlmostEqual(rows[0]['lr_used'][0],.1)
        self.assertAlmostEqual(rows[-1]['lr_next'][0],1e-5)
    def test_invalid_factory(self):
        for kind,epochs in [('bad',4),('cosine',0),('cosine',True),('cosine',2.5)]:
            with self.assertRaises(ValueError):self.build(kind,epochs)
    def test_bad_metric_no_state_change(self):
        o,s=self.build();before=copy.deepcopy(s.state_dict());lr=o.param_groups[0]['lr']
        with self.assertRaises(ValueError):tasks.advance_scheduler(s,float('nan'))
        self.assertEqual(before,s.state_dict());self.assertEqual(lr,o.param_groups[0]['lr'])
    def test_groups_recorded(self):
        o=torch.optim.SGD([{'params':[nn.Parameter(torch.ones(1))],'lr':.1},{'params':[nn.Parameter(torch.ones(1))],'lr':.01}],lr=.1)
        s=tasks.make_scheduler(o,'cosine',2);o.step();r=tasks.advance_scheduler(s,1.)
        self.assertEqual(r['lr_used'],[.1,.01]);self.assertEqual(len(r['lr_next']),2)

if __name__=='__main__': unittest.main()
