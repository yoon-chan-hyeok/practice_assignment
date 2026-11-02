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

    def test_benchmark_scope_and_original_state(self):
        x,y=synthetic(5);m=small_model(batchnorm=True,dropout=.2).train()
        for p in m.parameters():p.grad=torch.ones_like(p)
        old=snapshot(m);rng=torch.get_rng_state().clone()
        result=t.benchmark(m,[(x[:3],y[:3]),(x[3:],y[3:])],'cpu',2,1)
        self.assertEqual(result['status'],'measured');self.assertEqual(len(result['rows']),2)
        for r in result['rows']:
            self.assertEqual(r['samples'],5);self.assertGreater(r['seconds'],0);self.assertIsNone(r['peak_vram_mib'])
        self.assertTrue(torch.equal(rng,torch.get_rng_state()));self.assertEqual(old['modes'],snapshot(m)['modes'])
        for k,v in m.state_dict().items():self.assertTrue(torch.equal(v,old['state'][k]))
        for n,p in m.named_parameters():self.assertTrue(torch.equal(p.grad,old['grads'][n]))
    def test_missing_cuda_is_not_fabricated(self):
        if torch.cuda.is_available():self.skipTest('이 검사는 CUDA 없는 경로')
        x,y=synthetic(2);r=t.benchmark(small_model(),[(x,y)],'cuda')
        self.assertEqual(r,{'status':'SKIP_NO_CUDA','rows':[]})
    def test_invalid_counts(self):
        x,y=synthetic(2)
        with self.assertRaises(ValueError):t.benchmark(small_model(),[(x,y)],'cpu',0)
        with self.assertRaises(ValueError):t.benchmark(small_model(),[],'cpu')
    def test_profile_named_ranges(self):
        x,y=synthetic(5);m=small_model()
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'trace.json';r=t.profile_steps(m,DataLoader(TensorDataset(x,y),batch_size=3),'cpu',p)
            self.assertTrue(p.exists())
            self.assertTrue({'DataLoader.next','H2D','forward','backward','optimizer.step'}.issubset(r['events']))
    def test_summary_and_scope_guard(self):
        rows=[dict(repeat=i,device='cpu',layout='contiguous',samples=6,scope='same',seconds=s) for i,s in enumerate([1.,2.,3.])]
        r=t.summarize_times(rows);self.assertEqual(r['median_seconds'],2.)
        self.assertEqual(r['median_images_per_second'],3.)
        rows[-1]['scope']='different'
        with self.assertRaises(ValueError):t.summarize_times(rows)
    def test_summary_rejects_nonfinite(self):
        rows=[dict(repeat=i,device='cpu',layout='x',samples=2,scope='same',seconds=s) for i,s in enumerate([1.,float('nan')])]
        with self.assertRaises(ValueError):t.summarize_times(rows)

if __name__=='__main__':unittest.main()
