from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
from tasks import validate_batch,move_batch
class Checks(unittest.TestCase):
    def test_normal(self):self.assertIsNone(validate_batch(torch.ones(1,2),torch.tensor([0])))
    def test_type(self):
        with self.assertRaises(TypeError):validate_batch([[1.,2.]],torch.tensor([0]))
    def test_dtype(self):
        with self.assertRaises(TypeError):validate_batch(torch.ones(1,2),torch.tensor([0.]))
    def test_shape(self):
        with self.assertRaises(ValueError):validate_batch(torch.ones(2,2),torch.zeros(2,1,dtype=torch.long))
    def test_empty(self):
        with self.assertRaises(ValueError):validate_batch(torch.empty(0,2),torch.empty(0,dtype=torch.long))
    def test_values(self):
        for x,y in [(torch.tensor([[float('nan'),1.]]),torch.tensor([0])),(torch.ones(1,2),torch.tensor([2]))]:
            with self.assertRaises(ValueError):validate_batch(x,y)
    def test_preserve_grad(self):
        x=torch.ones(2,2,dtype=torch.float64,requires_grad=True);y=torch.tensor([0,1]);copy=x.detach().clone()
        a,b=move_batch(x,y,'cpu');a.sum().backward()
        self.assertEqual(a.dtype,torch.float64);self.assertTrue(torch.equal(x.detach(),copy));self.assertTrue(torch.equal(x.grad,torch.ones_like(x)))
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 장치 없음')
    def test_cuda(self):
        a,b=move_batch(torch.ones(2,2),torch.tensor([0,1]),'cuda:0');self.assertEqual(a.device,b.device);self.assertEqual(a.device.type,'cuda')
