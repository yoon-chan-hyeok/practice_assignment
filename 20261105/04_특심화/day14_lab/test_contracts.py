"""특심화 공개 검사: python -m unittest -v test_contracts.py
수치 정답뿐 아니라 입력·모드·gradient 보존을 검사합니다. TODO가 남으면 실패가 정상입니다.
"""
import unittest,tempfile,json,copy,random,csv,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from models import build_model
from contracts import *
BASE=Path(__file__).resolve().parent

class LabTests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(1);torch.manual_seed(14)
        self.model=build_model(BASE/'data');self.x=torch.rand(1,3,32,32)
    def test_01_audit_real(self):
        r=audit_manifest(BASE/'data');self.assertEqual(len(r['records']),300);self.assertEqual(r['exact_groups'],[]);self.assertEqual(r['group_leaks'],{})
    def test_02_audit_unsafe_path(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'manifest.csv').write_text('id,path,group_id,split\nx,../outside.png,g,train\n')
            with self.assertRaises(ValueError):audit_manifest(p)
    def test_03_audit_duplicate_fixture(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);Image.new('RGB',(16,16),(50,60,70)).save(p/'a.png');(p/'b.png').write_bytes((p/'a.png').read_bytes())
            (p/'manifest.csv').write_text('id,path,group_id,split\na,a.png,g,train\nb,b.png,g,valid\n')
            r=audit_manifest(p);self.assertEqual(len(r['exact_groups']),1);self.assertIn('g',r['group_leaks'])
    def test_04_audit_dhash_not_identity(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);Image.new('RGB',(16,16),'black').save(p/'a.png');Image.new('RGB',(16,16),'white').save(p/'b.png')
            (p/'manifest.csv').write_text('id,path,group_id,split\na,a.png,g1,train\nb,b.png,g2,valid\n')
            r=audit_manifest(p,near_bits=0);self.assertEqual(r['exact_groups'],[]);self.assertEqual(len(r['near_pairs']),1)
    def test_05_head_only(self):
        groups=trainable_groups(self.model,'head');self.assertEqual(sum(p.numel() for g in groups for p in g['params']),771)
        self.assertTrue(all(not m.training for m in self.model.modules() if isinstance(m,nn.BatchNorm2d)))
    def test_06_partial_no_duplicate(self):
        groups=trainable_groups(self.model,'partial');ids=[id(p) for g in groups for p in g['params']]
        self.assertEqual(len(ids),len(set(ids)));self.assertEqual(set(ids),{id(p) for p in self.model.parameters() if p.requires_grad})
    def test_07_bad_strategy(self):
        with self.assertRaises(ValueError):trainable_groups(self.model,'oops')
    def test_08_weights(self):
        y=torch.tensor([0]*120+[1]*40+[2]*20);cw,sw=imbalance_weights(y)
        torch.testing.assert_close(cw,torch.tensor([.3,.9,1.8]));self.assertEqual(sw.shape,y.shape)
        mass=torch.stack([sw[y==i].sum() for i in range(3)]);torch.testing.assert_close(mass,torch.ones(3))
    def test_09_missing_class(self):
        with self.assertRaises(ValueError):imbalance_weights(torch.tensor([0,1]))
    def test_10_bad_labels(self):
        with self.assertRaises(ValueError):imbalance_weights(torch.tensor([0.,1.,2.]))
    def test_11_weighted_loss_reference(self):
        x=torch.randn(5,3,requires_grad=True);y=torch.tensor([0,0,0,1,2]);w=torch.tensor([.3,.9,1.8])
        torch.testing.assert_close(weighted_ce(x,y,w),nn.functional.cross_entropy(x,y,weight=w))
    def test_12_weighted_gradient(self):
        x=torch.randn(5,3,requires_grad=True);y=torch.tensor([0,0,0,1,2]);w=torch.tensor([.3,.9,1.8])
        a=torch.autograd.grad(weighted_ce(x,y,w),x)[0];b=torch.autograd.grad(nn.functional.cross_entropy(x,y,weight=w),x)[0]
        torch.testing.assert_close(a,b)
    def test_13_weighted_empty(self):
        with self.assertRaises(ValueError):weighted_ce(torch.empty(0,3),torch.empty(0,dtype=torch.long),torch.ones(3))
    def test_14_weighted_negative(self):
        with self.assertRaises(ValueError):weighted_ce(torch.ones(3,3),torch.tensor([0,1,2]),torch.tensor([1.,0.,1.]))
    def test_15_bootstrap_repeatable(self):
        y=np.array([0,0,1,1,2,2]);p=np.array([0,1,1,1,2,0]);g=['a','a','b','b','c','c']
        self.assertEqual(group_bootstrap(y,p,g,50),group_bootstrap(y,p,g,50))
    def test_16_bootstrap_perfect(self):
        y=[0,1,2]*6;r=group_bootstrap(y,y,list(range(18)),50)
        self.assertEqual(r['estimate'],1.);self.assertLessEqual(r['low'],r['high'])
    def test_17_bootstrap_single_group(self):
        with self.assertRaises(ValueError):group_bootstrap([0,1],[0,1],['a','a'])
    def test_18_cam_shape_range(self):
        a=grad_cam(self.model,self.x,self.model[6],0);self.assertEqual(a.shape,(32,32));self.assertFalse(a.requires_grad);self.assertTrue(torch.isfinite(a).all());self.assertGreaterEqual(a.min().item(),0);self.assertLessEqual(a.max().item(),1)
    def test_19_cam_preserves_states(self):
        self.model.train();self.model[5].eval();flags=[m.training for m in self.model.modules()]
        state=copy.deepcopy(self.model.state_dict());before=self.x.clone()
        for p in self.model.parameters():p.grad=torch.ones_like(p)
        rng=torch.get_rng_state().clone();grad_cam(self.model,self.x,self.model[6],1)
        self.assertEqual(flags,[m.training for m in self.model.modules()]);torch.testing.assert_close(before,self.x)
        for k,v in self.model.state_dict().items():torch.testing.assert_close(v,state[k],rtol=0,atol=0)
        for p in self.model.parameters():torch.testing.assert_close(p.grad,torch.ones_like(p))
        torch.testing.assert_close(rng,torch.get_rng_state(),rtol=0,atol=0)
    def test_20_cam_frozen(self):
        for p in self.model.parameters():p.requires_grad_(False)
        out=grad_cam(self.model,self.x,self.model[6],0);self.assertTrue(torch.isfinite(out).all())
        self.assertFalse(any(p.requires_grad for p in self.model.parameters()))
    def test_21_cam_bad_target_cleanup(self):
        before=len(self.model[6]._forward_hooks)
        with self.assertRaises(ValueError):grad_cam(self.model,self.x,self.model[6],99)
        self.assertEqual(before,len(self.model[6]._forward_hooks))
    def test_22_cam_no_inference_mode(self):
        with torch.inference_mode():
            with self.assertRaises(ValueError):grad_cam(self.model,self.x,self.model[6],0)
    def test_23_cam_zero(self):
        for p in self.model.parameters():p.data.zero_()
        cam=grad_cam(self.model,self.x,self.model[6],0);torch.testing.assert_close(cam,torch.zeros(32,32))
    def test_24_occlusion_preserves(self):
        state=copy.deepcopy(self.model.state_dict());x=self.x.clone();flags=[m.training for m in self.model.modules()]
        _,drop=occlusion_map(self.model,self.x,0,patch=7)
        self.assertEqual(drop.shape,(32,32));self.assertTrue(torch.isfinite(drop).all());torch.testing.assert_close(x,self.x)
        self.assertEqual(flags,[m.training for m in self.model.modules()])
        for k,v in self.model.state_dict().items():torch.testing.assert_close(v,state[k],atol=0,rtol=0)
    def test_25_occlusion_patch_zero(self):
        with self.assertRaises(ValueError):occlusion_map(self.model,self.x,0,patch=0)
    def test_26_epoch_weighted_global(self):
        m=nn.Linear(3,3);x=torch.randn(7,3);y=torch.tensor([0,0,0,1,1,2,2]);w=torch.tensor([.3,.9,1.8]);opt=torch.optim.SGD(m.parameters(),lr=0.)
        loader=DataLoader(TensorDataset(x,y,torch.arange(7)),batch_size=3,shuffle=False);scaler=torch.amp.GradScaler('cuda',enabled=False)
        expected=weighted_ce(m(x),y,w).item();value,order=train_epoch(m,loader,opt,w,scaler)
        self.assertAlmostEqual(value,expected,places=6);self.assertEqual(order,list(range(7)))
    def test_27_epoch_updates(self):
        opt=torch.optim.SGD(trainable_groups(self.model,'head'),lr=.1);x=torch.randn(4,3,32,32);y=torch.tensor([0,1,2,0]);before=self.model[9].weight.clone()
        train_epoch(self.model,DataLoader(TensorDataset(x,y,torch.arange(4)),batch_size=4),opt,torch.ones(3),torch.amp.GradScaler('cuda',enabled=False))
        self.assertFalse(torch.equal(before,self.model[9].weight))
    def test_28_checkpoint_roundtrip(self):
        opt=torch.optim.AdamW(trainable_groups(self.model,'head'));sch=torch.optim.lr_scheduler.StepLR(opt,2);sc=torch.amp.GradScaler('cuda',enabled=False);g=torch.Generator().manual_seed(99)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'own.pt';save_checkpoint(p,self.model,opt,sch,sc,g,2,[{'epoch':2}],{'run':'a'},'abc')
            old=copy.deepcopy(self.model.state_dict());self.model[9].weight.data.zero_()
            e,h=load_checkpoint(p,self.model,opt,sch,sc,g,{'run':'a'},'abc');self.assertEqual(e,2);self.assertEqual(h,[{'epoch':2}])
            for k,v in self.model.state_dict().items():torch.testing.assert_close(v,old[k],atol=0,rtol=0)
    def test_29_checkpoint_contract_before_mutation(self):
        opt=torch.optim.AdamW(trainable_groups(self.model,'head'));sch=torch.optim.lr_scheduler.StepLR(opt,2);sc=torch.amp.GradScaler('cuda',enabled=False);g=torch.Generator().manual_seed(99)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'own.pt';save_checkpoint(p,self.model,opt,sch,sc,g,1,[],{'run':'a'},'abc');before=self.model[9].weight.clone()
            with self.assertRaises(ValueError):load_checkpoint(p,self.model,opt,sch,sc,g,{'run':'changed'},'abc')
            torch.testing.assert_close(before,self.model[9].weight,atol=0,rtol=0)
    def test_30_data_signature(self):
        a=signature(BASE/'data');self.assertEqual(a,signature(BASE/'data'));self.assertEqual(len(a),64)
    @unittest.skipUnless(torch.cuda.is_available(),'CUDA device unavailable')
    def test_31_cuda_cam(self):
        m=self.model.cuda();cam=grad_cam(m,self.x.cuda(),m[6],0);self.assertEqual(cam.device.type,'cpu')
    @unittest.skipUnless(torch.cuda.is_available(),'CUDA device unavailable')
    def test_32_cuda_amp(self):
        m=self.model.cuda();opt=torch.optim.AdamW(trainable_groups(m,'head'));x=torch.rand(6,3,32,32);y=torch.tensor([0,1,2,0,1,2])
        loss,ids=train_epoch(m,DataLoader(TensorDataset(x,y,torch.arange(6)),batch_size=3),opt,torch.ones(3),torch.amp.GradScaler('cuda'),amp=True)
        self.assertTrue(np.isfinite(loss));self.assertEqual(len(ids),6)

if __name__=='__main__':unittest.main(verbosity=2)
