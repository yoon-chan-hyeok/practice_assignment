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

    def make(self):
        from torchvision.models import resnet18
        m=resnet18(weights=None);m.fc=nn.Linear(m.fc.in_features,2);return m
    def test_head_parameters(self):
        m=self.make();o=t.configure_transfer(m,'head');rows=t.trainable_report(m,o)
        self.assertEqual(sum(r['numel'] for r in rows if r['trainable']),1026)
        self.assertTrue(all(not b.training for b in m.modules() if isinstance(b,nn.BatchNorm2d)))
    def test_partial_retains_head_optimizer_state(self):
        m=self.make();o=t.configure_transfer(m,'head')
        x=torch.rand(2,3,32,32);y=torch.tensor([0,1]);nn.functional.cross_entropy(m(x),y).backward();o.step()
        saved=copy.deepcopy(o.state[m.fc.weight]);identity=id(o)
        o=t.configure_transfer(m,'partial',o);t.configure_transfer(m,'partial',o)
        self.assertEqual(id(o),identity);self.assertEqual(len(o.param_groups),2)
        for key,v in saved.items():self.assertTrue(torch.equal(v,o.state[m.fc.weight][key]))
        t.trainable_report(m,o)
    def test_backward_stage_forbidden(self):
        m=self.make();o=t.configure_transfer(m,'partial')
        with self.assertRaises(ValueError):t.configure_transfer(m,'head',o)
    def test_report_rejects_duplicate_or_missing(self):
        m=self.make();o=t.configure_transfer(m,'head');o.param_groups[0]['params'].append(m.fc.weight)
        with self.assertRaises(ValueError):t.trainable_report(m,o)
        o.param_groups[0]['params']=[m.fc.weight]
        with self.assertRaises(ValueError):t.trainable_report(m,o)
    def test_bn_buffers_frozen_after_step(self):
        m=self.make();o=t.configure_transfer(m,'partial');before={n:b.clone() for n,b in m.named_buffers()}
        x=torch.rand(2,3,32,32);y=torch.tensor([0,1]);o.zero_grad();nn.functional.cross_entropy(m(x),y).backward();o.step()
        for n,b in m.named_buffers():self.assertTrue(torch.equal(b,before[n]))
        self.assertTrue(all(not p.requires_grad for n,p in m.named_parameters() if not n.startswith(('layer4.','fc.'))))

if __name__=='__main__':unittest.main()
