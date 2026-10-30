from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
from tasks import analytic_mse,central_difference
class Checks(unittest.TestCase):
    def test_analytic(self):
        torch.manual_seed(7)
        for n,d in [(1,1),(3,2),(8,5)]:
            X=torch.randn(n,d,dtype=torch.float64);t=torch.randn(n,dtype=torch.float64)
            w=torch.randn(d,dtype=torch.float64,requires_grad=True);b=torch.tensor(.2,dtype=torch.float64,requires_grad=True)
            loss,gw,gb=analytic_mse(X,t,w,b);ref=((X@w+b-t)**2).mean();ref.backward()
            torch.testing.assert_close(loss,ref,rtol=1e-8,atol=1e-10);torch.testing.assert_close(gw,w.grad,rtol=1e-8,atol=1e-10);torch.testing.assert_close(gb,b.grad,rtol=1e-8,atol=1e-10)
    def test_numerical(self):
        w=torch.tensor([1.,-2.,3.],dtype=torch.float64,requires_grad=True);w.grad=torch.ones_like(w);before=w.clone()
        got=central_difference(lambda q:(q*q).sum(),w)
        torch.testing.assert_close(got,2*w,rtol=1e-5,atol=1e-6);self.assertFalse(got.requires_grad);self.assertTrue(torch.equal(w,before));self.assertTrue(torch.equal(w.grad,torch.ones_like(w)))
    def test_epsilon(self):
        for e in [0,-1]:
            with self.assertRaises(ValueError):central_difference(lambda q:q.sum(),torch.ones(2,dtype=torch.float64),e)
