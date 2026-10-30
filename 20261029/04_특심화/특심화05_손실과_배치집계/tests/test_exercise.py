from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
from tasks import stable_cross_entropy,weighted_batch_mean
class Checks(unittest.TestCase):
    def test_loss_gradient(self):
        for raw in [[[2.,0.],[0.,2.]],[[1000.,-1000.],[-1000.,1000.]]]:
            x=torch.tensor(raw,dtype=torch.float64,requires_grad=True);z=x.detach().clone().requires_grad_();y=torch.tensor([1,0])
            a=stable_cross_entropy(x,y);b=torch.nn.functional.cross_entropy(z,y);a.backward();b.backward()
            torch.testing.assert_close(a,b,rtol=1e-8,atol=1e-10);torch.testing.assert_close(x.grad,z.grad,rtol=1e-8,atol=1e-10)
    def test_shift(self):
        x=torch.tensor([[2.,1.,-1.]],dtype=torch.float64);y=torch.tensor([1])
        torch.testing.assert_close(stable_cross_entropy(x,y),stable_cross_entropy(x+500,y))
    def test_weighting(self):self.assertAlmostEqual(weighted_batch_mean(iter([(0.1,4),(0.2,4),(0.9,2)])),.3)
    def test_bad_counts(self):
        for pairs in [[],[(0.2,0)],[(0.2,-1)],[(0.2,True)],[(float('nan'),2)]]:
            with self.assertRaises(ValueError):weighted_batch_mean(pairs)
