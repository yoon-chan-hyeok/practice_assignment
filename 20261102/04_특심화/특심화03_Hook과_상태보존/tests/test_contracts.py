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

    def test_reused_module_has_two_calls(self):
        class Reuse(nn.Module):
            def __init__(self):super().__init__();self.r=nn.ReLU()
            def forward(self,x):return self.r(self.r(x))
        rows=t.trace_leaves(Reuse(),torch.rand(2,3))
        self.assertEqual([r['call'] for r in rows],[1,2])
        report=t.summarize_trace(rows);self.assertEqual(report['unique_modules'],1)
    def test_state_and_external_hook_preserved(self):
        m=small_model(batchnorm=True,dropout=.5);m.train();m[-1].eval();calls=[]
        h=m[0].register_forward_hook(lambda *args:calls.append(1))
        for p in m.parameters():p.grad=torch.ones_like(p)
        x=torch.rand(2,3,16,16);before=snapshot(m);rng=torch.get_rng_state().clone()
        n=len(m[0]._forward_hooks);rows=t.trace_leaves(m,x)
        self.assertEqual(len(m[0]._forward_hooks),n);self.assertEqual(len(calls),1)
        self.assertEqual(before['modes'],snapshot(m)['modes']);self.assertTrue(torch.equal(rng,torch.get_rng_state()))
        for k,v in m.state_dict().items():self.assertTrue(torch.equal(v,before['state'][k]))
        for name,p in m.named_parameters():self.assertTrue(torch.equal(p.grad,before['grads'][name]))
        json.dumps(rows);h.remove()
    def test_failure_cleanup(self):
        class Broken(nn.Module):
            def __init__(self):super().__init__();self.fc=nn.Linear(3,2)
            def forward(self,x): self.fc(x);raise RuntimeError('planned')
        m=Broken().train()
        with self.assertRaises(RuntimeError):t.trace_leaves(m,torch.rand(2,3))
        self.assertTrue(m.training);self.assertEqual(len(m.fc._forward_hooks),0)
    def test_trace_statistics(self):
        rows=t.trace_leaves(nn.Identity(),torch.tensor([[1.,3.]]));r=rows[0]
        self.assertEqual(r['mean'],2.);self.assertEqual(r['std'],1.);self.assertEqual(r['activation_bytes'],8)
    def test_summary_counts_unique_parameters(self):
        r=dict(name='shared',call=1,parameters=6,activation_bytes=16)
        s=t.summarize_trace([r,{**r,'call':2}]);self.assertEqual(s['parameters_once'],6)
        self.assertEqual(s['calls'],2)
    def test_invalid_summary_and_output(self):
        with self.assertRaises(ValueError): t.summarize_trace([])
        with self.assertRaises(ValueError): t.trace_leaves(nn.Identity(),torch.ones(2,3,dtype=torch.long))

if __name__=='__main__':unittest.main()
