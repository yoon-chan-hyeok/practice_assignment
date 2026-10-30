from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
import copy,tempfile
from model import SimpleANN
from tasks import save_checkpoint,restore_checkpoint,same_state
class Checks(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42);self.m=SimpleANN();self.o=torch.optim.SGD(self.m.parameters(),lr=.1,momentum=.9);self.g=torch.Generator().manual_seed(43);self.config={'device':'cpu','hidden':8};self.ids={'train':['a'],'valid':['b'],'test':['c']}
        self.m(torch.tensor([[1.,2.]])).sum().backward();self.o.step();self.o.zero_grad()
    def test_save_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'state.pt';rng=torch.get_rng_state().clone();save_checkpoint(p,self.m,self.o,2,self.g,self.config,self.ids);self.assertTrue(torch.equal(rng,torch.get_rng_state()))
            m=SimpleANN();o=torch.optim.SGD(m.parameters(),lr=.1,momentum=.9);g=torch.Generator().manual_seed(999)
            self.assertEqual(restore_checkpoint(p,m,o,g,self.config,self.ids,'cpu'),2);self.assertTrue(same_state(m.state_dict(),self.m.state_dict()));self.assertTrue(same_state(o.state_dict(),self.o.state_dict()));self.assertTrue(torch.equal(g.get_state(),self.g.get_state()))
    def test_bad_config_no_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'state.pt';save_checkpoint(p,self.m,self.o,2,self.g,self.config,self.ids)
            before=copy.deepcopy(self.m.state_dict());rng=torch.get_rng_state().clone();gs=self.g.get_state().clone()
            with self.assertRaises(ValueError):restore_checkpoint(p,self.m,self.o,self.g,{'wrong':True},self.ids,'cpu')
            self.assertTrue(same_state(before,self.m.state_dict()));self.assertTrue(torch.equal(rng,torch.get_rng_state()));self.assertTrue(torch.equal(gs,self.g.get_state()))
    def test_bad_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'s.pt';save_checkpoint(p,self.m,self.o,2,self.g,self.config,self.ids)
            with self.assertRaises(ValueError):restore_checkpoint(p,self.m,self.o,self.g,self.config,{'train':['x']},'cpu')
    def test_comparison(self):
        a={'tensor':torch.ones(2),'seq':[1,True,None],'step':2};self.assertTrue(same_state(a,copy.deepcopy(a)))
        for b in [{'tensor':torch.zeros(2),'seq':[1,True,None],'step':2},{'tensor':torch.ones(2),'seq':[1,True,None],'step':3}]:self.assertFalse(same_state(a,b))
        self.assertFalse(same_state(torch.ones(2),torch.ones(2,dtype=torch.float64)));self.assertFalse(same_state([1],(1,)));self.assertFalse(same_state({'a':1},{'b':1}))
