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

def fixture():
    return pd.DataFrame([dict(seed=s,epoch=e,train_loss_eval=t,valid_loss=v) for s,vs in [(1,[1.,.5,.5]),(2,[1.2,.8,.4])]
        for e,t,v in zip([1,2,3],[.8,.4,.2],vs)])
class Contracts(unittest.TestCase):
    def test_best_tie_and_last(self):
        h=fixture();b=tasks.summarize_best(h)
        self.assertEqual(b.best_epoch.tolist(),[2,3]);np.testing.assert_allclose(b.gap_at_best,[.1,.2])
        np.testing.assert_allclose(b.last_valid_loss,[.5,.4])
    def test_curve_std(self):
        c=tasks.summarize_curve(fixture())
        self.assertEqual(c.n.tolist(),[2]*3);np.testing.assert_allclose(c.valid_mean,[1.1,.65,.45])
        np.testing.assert_allclose(c.valid_std,[math.sqrt(.02),math.sqrt(.045),math.sqrt(.005)])
    def test_preserve_unsorted_input(self):
        h=fixture().iloc[::-1].copy();before=h.copy(deep=True)
        tasks.summarize_best(h);tasks.summarize_curve(h);pd.testing.assert_frame_equal(h,before)
    def test_missing_epoch(self):
        with self.assertRaises(ValueError):tasks.summarize_best(fixture().drop(index=[0]))
    def test_duplicate(self):
        h=fixture()
        with self.assertRaises(ValueError):tasks.summarize_curve(pd.concat([h,h.iloc[:1]]))
    def test_nonfinite_or_single_seed(self):
        h=fixture();h.loc[0,'valid_loss']=float('nan')
        for q in [h,fixture().query('seed==1')]:
            with self.assertRaises(ValueError):tasks.summarize_best(q)

if __name__=='__main__': unittest.main()
