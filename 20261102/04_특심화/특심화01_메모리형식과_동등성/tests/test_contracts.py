"""공개 계약 테스트. 정답 구현은 import하지 않으며 해당 폴더의 tasks.py를 검사한다."""
from pathlib import Path
import sys, copy, tempfile, json, unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
import tasks as t
from support import seed_all,synthetic,small_model,snapshot

class Contracts(unittest.TestCase):
    def setUp(self): seed_all()

    def test_shape_values_and_independent_storage(self):
        x=torch.rand(2,3,5,7);y=t.channels_last_copy(x)
        self.assertEqual(x.shape,y.shape);self.assertTrue(torch.equal(x,y));self.assertNotEqual(x.data_ptr(),y.data_ptr())
        self.assertTrue(y.is_contiguous(memory_format=torch.channels_last))
    def test_already_channels_last_still_copies(self):
        x=torch.rand(2,3,5,7).to(memory_format=torch.channels_last);y=t.channels_last_copy(x)
        y.add_(1);self.assertFalse(torch.equal(x,y))
    def test_noncontiguous_and_gradient(self):
        raw=torch.rand(2,3,5,7,requires_grad=True);x=raw.transpose(2,3)
        old=x.stride();t.channels_last_copy(x).sum().backward()
        self.assertEqual(x.stride(),old);torch.testing.assert_close(raw.grad,torch.ones_like(raw))
    def test_invalid_inputs(self):
        for x in [torch.rand(3,4),torch.zeros(0,3,2,2),torch.ones(2,3,2,2,dtype=torch.long),[1,2]]:
            with self.subTest(value=type(x)):
                with self.assertRaises(ValueError): t.channels_last_copy(x)
    def test_model_and_rng_preserved(self):
        m=small_model(batchnorm=True,dropout=.3).train();m[-1].eval()
        for p in m.parameters(): p.grad=torch.ones_like(p)
        old=snapshot(m);x=torch.rand(2,3,16,16);rng=torch.get_rng_state().clone()
        report=t.compare_layouts(m,x)
        self.assertLess(max(report.values()),1e-5)
        self.assertTrue(torch.equal(rng,torch.get_rng_state()))
        now=snapshot(m);self.assertEqual(old['modes'],now['modes'])
        for field in ['state','grads']:
            for k in old[field]: self.assertTrue(torch.equal(old[field][k],now[field][k]))
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 장치 없음')
    def test_cuda_copy(self):
        x=torch.rand(2,3,8,8,device='cuda');y=t.channels_last_copy(x)
        self.assertEqual(y.device,x.device);self.assertTrue(torch.equal(x,y))

if __name__=='__main__':unittest.main()
