from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
import copy
from torch import nn
from torch.utils.data import TensorDataset,DataLoader
from tasks import train_one_epoch,evaluate
class Checks(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42);self.model=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Linear(8,2));self.x=torch.randn(7,2);self.y=torch.tensor([0,1,0,1,1,0,1]);self.loader=DataLoader(TensorDataset(self.x,self.y),batch_size=3)
    def test_weighted_no_update(self):
        expected=nn.CrossEntropyLoss()(self.model(self.x),self.y).item();opt=torch.optim.SGD(self.model.parameters(),lr=0)
        got=train_one_epoch(self.model,self.loader,opt,'cpu');self.assertAlmostEqual(got['loss'],expected,places=6);self.assertEqual((got['samples'],got['batches']),(7,3))
    def test_updates(self):
        before=copy.deepcopy(self.model.state_dict());opt=torch.optim.SGD(self.model.parameters(),lr=.1);train_one_epoch(self.model,self.loader,opt,'cpu')
        self.assertTrue(any(not torch.equal(before[k],v) for k,v in self.model.state_dict().items()))
    def test_preserves_state(self):
        self.model(self.x).sum().backward();before=copy.deepcopy(self.model.state_dict());grads=[p.grad.clone() for p in self.model.parameters()]
        self.model.train();self.model[0].eval();modes=[m.training for m in self.model.modules()]
        result=evaluate(self.model,self.loader,'cpu')
        self.assertEqual(modes,[m.training for m in self.model.modules()]);self.assertTrue(all(torch.equal(v,before[k]) for k,v in self.model.state_dict().items()));self.assertTrue(all(torch.equal(p.grad,g) for p,g in zip(self.model.parameters(),grads)));self.assertFalse(result['probabilities'].requires_grad)
        self.assertEqual(tuple(result['probabilities'].shape),(7,2))
    def test_empty_restores(self):
        empty=DataLoader(TensorDataset(torch.empty(0,2),torch.empty(0,dtype=torch.long)),batch_size=2)
        self.model.train();self.model[0].eval();modes=[m.training for m in self.model.modules()]
        with self.assertRaises(ValueError):evaluate(self.model,empty,'cpu')
        self.assertEqual(modes,[m.training for m in self.model.modules()])
    def test_invalid_restores(self):
        invalid=DataLoader(TensorDataset(torch.ones(2,2),torch.tensor([5,5])),batch_size=2);self.model.train()
        with self.assertRaises(ValueError):evaluate(self.model,invalid,'cpu')
        self.assertTrue(self.model.training)
