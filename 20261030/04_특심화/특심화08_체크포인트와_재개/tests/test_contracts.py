from pathlib import Path
import sys,copy,math,unittest,tempfile,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
import pandas as pd
import numpy as np
import tasks

torch.set_num_threads(1)
def equal_nested(a,b):
    if isinstance(a,torch.Tensor): return isinstance(b,torch.Tensor) and a.dtype==b.dtype and torch.equal(a,b)
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(equal_nested(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return len(a)==len(b) and all(equal_nested(x,y) for x,y in zip(a,b))
    return a==b

from stopping import EarlyStop

def fixture():
    torch.manual_seed(4);m=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Dropout(.2),nn.Linear(8,2))
    o=torch.optim.AdamW(m.parameters(),lr=.01);s=torch.optim.lr_scheduler.ReduceLROnPlateau(o,patience=1)
    g=torch.Generator().manual_seed(9);stop=EarlyStop();x=torch.ones(5,2);y=torch.arange(5)%2
    o.zero_grad();loss=nn.functional.cross_entropy(m(x),y);loss.backward();o.step();s.step(float(loss.detach()));stop.update(float(loss.detach()),1,m)
    meta=dict(config={'lr':.01},fingerprint='abc',split_ids={'train':[1,2],'valid':[3]},device='cpu',
              environment={'torch':str(torch.__version__),'threads':1},completed_epochs=1)
    return m,o,s,stop,g,meta

class Contracts(unittest.TestCase):
    def test_save_load_roundtrip(self):
        m,o,s,stop,g,meta=fixture()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'state.pt';tasks.save_checkpoint(p,m,o,s,stop,g,meta,[{'epoch':1}],[[0,1]])
            a=torch.load(p,weights_only=True);m2,o2,s2,t2,g2,_=fixture()
            epoch,h,tr=tasks.restore_checkpoint(p,m2,o2,s2,t2,g2,meta)
            self.assertEqual(epoch,1);self.assertEqual(tr,[[0,1]])
            self.assertTrue(equal_nested(m.state_dict(),m2.state_dict()));self.assertTrue(equal_nested(o.state_dict(),o2.state_dict()))
            self.assertTrue(equal_nested(s.state_dict(),s2.state_dict()));self.assertTrue(equal_nested(stop.state_dict(),t2.state_dict()))
            self.assertTrue(torch.equal(a['cpu_rng'],torch.get_rng_state()));self.assertTrue(torch.equal(a['loader_rng'],g2.get_state()))
    def test_save_is_observation(self):
        m,o,s,t,g,meta=fixture();before=copy.deepcopy(m.state_dict());rng=torch.get_rng_state().clone();gen=g.get_state().clone()
        with tempfile.TemporaryDirectory() as d:tasks.save_checkpoint(Path(d)/'x.pt',m,o,s,t,g,meta,[],[])
        self.assertTrue(equal_nested(before,m.state_dict()));self.assertTrue(torch.equal(rng,torch.get_rng_state()));self.assertTrue(torch.equal(gen,g.get_state()))
    def test_bad_metadata_before_mutation(self):
        m,o,s,t,g,meta=fixture()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x.pt';tasks.save_checkpoint(p,m,o,s,t,g,meta,[],[])
            for key,value in [('config',{}),('fingerprint','changed'),('split_ids',{}),('environment',{})]:
                expected=copy.deepcopy(meta);expected[key]=value;before=copy.deepcopy(m.state_dict());rng=torch.get_rng_state().clone()
                with self.assertRaises(ValueError):tasks.restore_checkpoint(p,m,o,s,t,g,expected)
                self.assertTrue(equal_nested(before,m.state_dict()));self.assertTrue(torch.equal(rng,torch.get_rng_state()))
    def test_compare_tensors_and_paths(self):
        a={'m':torch.tensor([1.,2.]),'h':[{'loss':.2}],'epoch':4};b=copy.deepcopy(a)
        self.assertEqual(tasks.compare_states(a,b),[])
        b['h'][0]['loss']=.3;self.assertEqual(tasks.compare_states(a,b),['root.h[0].loss'])
        b=copy.deepcopy(a);b['m']=b['m'].double();self.assertIn('root.m',tasks.compare_states(a,b))
    def test_compare_nested_lengths_and_keys(self):
        self.assertEqual(tasks.compare_states([1,2],[1]),['root.length'])
        self.assertEqual(tasks.compare_states({'x':1},{}),['root.keys'])
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 환경 필요')
    def test_cuda_state_payload(self):
        m,o,s,t,g,meta=fixture()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.pt';tasks.save_checkpoint(p,m,o,s,t,g,meta,[],[])
            state=torch.load(p,weights_only=True);self.assertEqual(len(state['cuda_rng']),torch.cuda.device_count())

if __name__=='__main__': unittest.main()
