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

    def test_cost_against_actual_layers(self):
        for co,k,s,p,d,g in [(16,3,1,1,1,1),(8,3,1,1,1,8),(16,1,1,0,1,1),(16,3,2,2,2,4)]:
            with self.subTest(groups=g):
                m=nn.Conv2d(8,co,k,stride=s,padding=p,dilation=d,groups=g)
                r=t.conv_cost((2,8,16,14),co,k,s,p,d,g)
                self.assertEqual(r['shape'],tuple(m(torch.rand(2,8,16,14)).shape))
                self.assertEqual(r['parameters'],sum(p.numel() for p in m.parameters()))
    def test_known_mac_and_bias(self):
        r=t.conv_cost((1,3,5,5),8,3,padding=1,bias=False)
        self.assertEqual(r['parameters'],216);self.assertEqual(r['macs'],5400)
    def test_invalid_costs(self):
        for kw in [dict(groups=2),dict(stride=0),dict(padding=-1),dict(kernel=20),dict(groups=True)]:
            args=dict(cout=8,kernel=3);args.update(kw)
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError): t.conv_cost((1,3,5,5),**args)
    def test_forward_and_gradient_grouped(self):
        for g in [1,2,4]:
            x=torch.rand(2,4,7,8,dtype=torch.float64,requires_grad=True)
            w=torch.rand(8,4//g,3,3,dtype=torch.float64,requires_grad=True)
            b=torch.rand(8,dtype=torch.float64,requires_grad=True)
            a=t.grouped_reference(x,w,b,padding=2,dilation=2,groups=g)
            ref=nn.functional.conv2d(x,w,b,padding=2,dilation=2,groups=g)
            torch.testing.assert_close(a,ref,atol=1e-9,rtol=1e-9)
            ga=torch.autograd.grad(a.square().mean(),(x,w,b),retain_graph=True)
            gr=torch.autograd.grad(ref.square().mean(),(x,w,b))
            for l,r in zip(ga,gr): torch.testing.assert_close(l,r,atol=1e-9,rtol=1e-9)
    def test_no_bias_and_no_mutation(self):
        x=torch.rand(2,4,6,6);w=torch.rand(4,1,3,3);old=x.clone()
        a=t.grouped_reference(x,w,groups=4)
        torch.testing.assert_close(a,nn.functional.conv2d(x,w,groups=4))
        self.assertTrue(torch.equal(x,old))
    def test_bad_weight(self):
        with self.assertRaises(ValueError):t.grouped_reference(torch.rand(1,4,6,6),torch.rand(4,3,3,3),groups=2)

if __name__=='__main__':unittest.main()
