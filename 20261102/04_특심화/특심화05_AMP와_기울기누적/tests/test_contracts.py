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

    def scaler(self): return torch.amp.GradScaler('cuda',enabled=False)
    def test_unequal_accumulation_matches_full(self):
        x,y=synthetic(10);m=small_model().eval();n=copy.deepcopy(m)
        a=torch.optim.SGD(m.parameters(),lr=.03);b=torch.optim.SGD(n.parameters(),lr=.03)
        one=t.accumulated_step(m,a,[(x,y)],torch.device('cpu'),self.scaler(),100.)
        many=t.accumulated_step(n,b,[(x[:3],y[:3]),(x[3:8],y[3:8]),(x[8:],y[8:])],torch.device('cpu'),self.scaler(),100.)
        self.assertAlmostEqual(one['loss'],many['loss'],places=6);self.assertEqual(many['samples'],10)
        for p,q in zip(m.parameters(),n.parameters()):torch.testing.assert_close(p,q,atol=1e-6,rtol=1e-5)
    def test_invalid_before_any_update(self):
        x,y=synthetic(3);m=small_model();old=snapshot(m);o=torch.optim.SGD(m.parameters(),lr=.1)
        with self.assertRaises(ValueError):t.accumulated_step(m,o,[(x,y),(x[:0],y[:0])],'cpu',self.scaler())
        for k,v in m.state_dict().items():self.assertTrue(torch.equal(v,old['state'][k]))
    def test_does_not_change_mode(self):
        x,y=synthetic(4);m=small_model(batchnorm=True).eval();old=snapshot(m)
        t.accumulated_step(m,torch.optim.SGD(m.parameters(),lr=.01),[(x,y)],'cpu',self.scaler())
        self.assertEqual(old['modes'],snapshot(m)['modes'])
        for name,b in m.named_buffers():self.assertTrue(torch.equal(b,old['state'][name]))
    def test_clipping_applied(self):
        x,y=synthetic(4);m=small_model();r=t.accumulated_step(m,torch.optim.SGD(m.parameters(),lr=.01),[(x,y)],'cpu',self.scaler(),.001)
        norm=torch.linalg.vector_norm(torch.stack([p.grad.norm() for p in m.parameters()]))
        self.assertLessEqual(float(norm),.00101);self.assertGreaterEqual(r['unclipped_grad_norm'],0)
    def test_evaluation_weighting_and_preservation(self):
        x,y=synthetic(5);m=small_model(batchnorm=True,dropout=.3).train();m[-1].eval()
        for p in m.parameters():p.grad=torch.ones_like(p)
        old=snapshot(m);ref=copy.deepcopy(m).eval()
        with torch.no_grad():expected=nn.functional.cross_entropy(ref(x),y).item()
        report=t.evaluate(m,DataLoader(TensorDataset(x,y),batch_size=3),'cpu')
        self.assertAlmostEqual(report['loss'],expected,places=6);self.assertEqual(report['samples'],5)
        self.assertEqual(old['modes'],snapshot(m)['modes'])
        for name,p in m.named_parameters():self.assertTrue(torch.equal(p.grad,old['grads'][name]))
    def test_empty_evaluation_restores_mode(self):
        m=small_model().train()
        with self.assertRaises(ValueError):t.evaluate(m,[],'cpu')
        self.assertTrue(m.training)
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 장치 없음')
    def test_cuda_amp(self):
        x,y=synthetic(4);m=small_model().cuda();o=torch.optim.SGD(m.parameters(),lr=.01)
        r=t.accumulated_step(m,o,[(x,y)],'cuda',torch.amp.GradScaler('cuda'))
        self.assertTrue(r['amp_active']);self.assertTrue(torch.isfinite(torch.tensor(r['loss'])))

if __name__=='__main__':unittest.main()
