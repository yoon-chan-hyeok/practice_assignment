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

    def objects(self):
        m=small_model(batchnorm=True,dropout=.2);o=torch.optim.AdamW(m.parameters(),lr=.01)
        s=torch.optim.lr_scheduler.StepLR(o,1,.5);sc=torch.amp.GradScaler('cuda',enabled=False)
        return m,o,s,sc,torch.Generator().manual_seed(42)
    def packed(self,objs):
        return t.pack_state(*objs,2,[{'epoch':2,'order':[2,1,0]}],{'seed':42},'hash')
    def test_snapshot_is_independent(self):
        objs=self.objects();saved=self.packed(objs);old=copy.deepcopy(saved)
        with torch.no_grad(): next(objs[0].parameters()).add_(10)
        self.assertEqual(t.compare_states(saved,old),[])
    def test_roundtrip_weights_only(self):
        objs=self.objects();x,y=synthetic(3)
        loss=nn.functional.cross_entropy(objs[0](x),y);loss.backward();objs[1].step();objs[2].step()
        saved=self.packed(objs)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'state.pt';torch.save(saved,p);read=torch.load(p,map_location='cpu',weights_only=True)
            other=self.objects();epoch,history=t.restore_state(read,*other,{'seed':42},'hash')
            repacked=t.pack_state(*other,epoch,history,{'seed':42},'hash')
            self.assertEqual(t.compare_states(saved,repacked),[])
    def test_rng_and_generator_replay(self):
        import random,numpy as np
        objs=self.objects();saved=self.packed(objs)
        expected=(random.random(),float(np.random.rand()),torch.rand(3),torch.randperm(5,generator=objs[-1]))
        other=self.objects();t.restore_state(saved,*other,{'seed':42},'hash')
        actual=(random.random(),float(np.random.rand()),torch.rand(3),torch.randperm(5,generator=other[-1]))
        self.assertEqual(expected[0:2],actual[0:2]);self.assertTrue(torch.equal(expected[2],actual[2]));self.assertTrue(torch.equal(expected[3],actual[3]))
    def test_contract_mismatch_before_mutation(self):
        objs=self.objects();saved=self.packed(objs);other=self.objects();before=snapshot(other[0])
        with self.assertRaises(ValueError):t.restore_state(saved,*other,{'seed':99},'hash')
        for k,v in other[0].state_dict().items():self.assertTrue(torch.equal(v,before['state'][k]))
        with self.assertRaises(ValueError):t.restore_state(saved,*other,{'seed':42},'other')
    def test_comparison_reports_nested_path(self):
        a={'a':{'order':[1,2]},'v':torch.tensor([1.])};b=copy.deepcopy(a);b['a']['order'][1]=9
        self.assertIn('root/a/order/1',t.compare_states(a,b))
    def test_comparison_dtype_and_sequence_type(self):
        self.assertTrue(t.compare_states(torch.tensor([1]),torch.tensor([1.])) )
        self.assertTrue(t.compare_states([1],(1,)))
    def test_existing_gradients_restored(self):
        objs=self.objects()
        for p in objs[0].parameters():p.grad=torch.ones_like(p)
        saved=self.packed(objs);other=self.objects();t.restore_state(saved,*other,{'seed':42},'hash')
        for p in other[0].parameters():self.assertTrue(torch.equal(p.grad,torch.ones_like(p)))

if __name__=='__main__':unittest.main()
