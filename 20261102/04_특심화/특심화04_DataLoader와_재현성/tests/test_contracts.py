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

    def dataset(self):
        x,y=synthetic(10);return TensorDataset(x,y,torch.arange(10))
    def test_generator_and_options(self):
        loader,g=t.make_loader(self.dataset(),4,0,True,9)
        self.assertIs(loader.generator,g);self.assertFalse(loader.drop_last)
        self.assertFalse(loader.pin_memory);self.assertFalse(loader.persistent_workers)
    def test_initial_order_reproduced(self):
        a,_=t.make_loader(self.dataset(),4,0,True,42);b,_=t.make_loader(self.dataset(),4,0,True,42)
        ra=t.measure_loading(a,1);rb=t.measure_loading(b,1)
        self.assertEqual(ra[0]['ids'],rb[0]['ids']);self.assertEqual(ra[0]['batch_sizes'],[4,4,2])
    def test_timing_scope(self):
        loader,_=t.make_loader(self.dataset(),4,0,False)
        rows=t.measure_loading(loader,2)
        self.assertEqual(len(rows),2)
        for r in rows:
            self.assertEqual(r['images'],10);self.assertGreater(r['seconds'],0)
            self.assertAlmostEqual(r['images_per_second'],10/r['seconds'])
            self.assertEqual(r['scope'],'host_decode_transform_collate')
    def test_spawn_configuration(self):
        loader,_=t.make_loader(self.dataset(),4,2,False)
        self.assertTrue(loader.persistent_workers);self.assertEqual(loader.multiprocessing_context.get_start_method(),'spawn')
    def test_invalid_options(self):
        for kw in [dict(batch_size=0),dict(workers=-1),dict(batch_size=True),dict(seed=3.2)]:
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):t.make_loader(self.dataset(),**kw)
    def test_empty_or_duplicate_ids(self):
        x,y=synthetic(3);ds=TensorDataset(x,y,torch.tensor([0,0,1]));loader,_=t.make_loader(ds,2)
        with self.assertRaises(ValueError):t.measure_loading(loader)
        with self.assertRaises(ValueError):t.measure_loading(loader,0)

if __name__=='__main__':unittest.main()
