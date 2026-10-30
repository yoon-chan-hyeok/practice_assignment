from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
from torch import nn
from tasks import SimpleANN,copy_from_sequential
class Checks(unittest.TestCase):
    def test_count(self):self.assertEqual(sum(p.numel() for p in SimpleANN().parameters()),42)
    def test_shapes(self):
        m=SimpleANN()
        for n in [1,7]:self.assertEqual(tuple(m(torch.ones(n,2)).shape),(n,2))
    def test_copy_gradients(self):
        torch.manual_seed(3);a=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Linear(8,2)).double();b=SimpleANN().double()
        self.assertIs(copy_from_sequential(b,a),b)
        x=torch.randn(4,2,dtype=torch.float64,requires_grad=True);z=x.detach().clone().requires_grad_()
        out1,out2=a(x),b(z);torch.testing.assert_close(out1,out2);out1.sum().backward();out2.sum().backward();torch.testing.assert_close(x.grad,z.grad)
        for p,q in zip(a.parameters(),b.parameters()):torch.testing.assert_close(p.grad,q.grad);self.assertNotEqual(p.data_ptr(),q.data_ptr())
    def test_not_alias(self):
        a=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Linear(8,2));b=SimpleANN();copy_from_sequential(b,a)
        before=a[0].weight.clone()
        with torch.no_grad():b.net[0].weight.add_(1)
        self.assertTrue(torch.equal(a[0].weight,before))
