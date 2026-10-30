"""실습08: 손실 숫자뿐 아니라 평가의 부작용과 best 복원을 검증합니다."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import copy
from unittest.mock import patch
import unittest
import torch
from torch import nn
from evaluate import evaluate
from train import fit

torch.set_num_threads(1)
class TrainingTests(unittest.TestCase):
    def test_evaluation_preserves_state(self):
        torch.manual_seed(7)
        model=nn.Sequential(nn.Linear(2,8),nn.BatchNorm1d(8),nn.ReLU(),nn.Dropout(.3),nn.Linear(8,2))
        model.train();model[1].eval()
        for p in model.parameters(): p.grad=torch.ones_like(p)
        X=torch.randn(10,2);y=torch.arange(10)%2
        before=copy.deepcopy(model.state_dict())
        grads=[p.grad.clone() for p in model.parameters()]
        modes=[m.training for m in model.modules()]
        loss,acc,pred=evaluate(model,X,y,torch.device('cpu'))
        # S11 요구: 모든 state_dict·기존 grad·하위 모드가 같고, pred에 그래프가 없는지 확인.
        # torch.equal과 self.assertTrue/self.assertEqual 사용. 한 층만 확인하면 부족합니다.
        # >>> S11
        self.fail("TODO S11: 검증문을 작성하세요.")
        # <<< S11

    def test_best_is_not_patience_reference(self):
        # 제공 fixture: 실제 갱신은 수행하되 valid 측정값만 고정해서 동작을 확정합니다.
        # min_delta=.05: .79/.78은 patience를 초기화하지 않지만 최소 모델은 epoch4입니다.
        X=torch.tensor([[0.,0.],[0.,1.],[1.,0.],[1.,1.]])
        y=torch.tensor([0,1,1,0]);Xv=X.clone();yv=y.clone()
        losses=[1.,.8,.79,.78];snapshots=[]
        def observed(model, xx, yy, device):
            if xx is Xv:
                if len(snapshots)<4:
                    snapshots.append(copy.deepcopy(model.state_dict()))
                    value=losses[len(snapshots)-1]
                else: value=.78
                return value,.5,torch.zeros(len(yy),dtype=torch.long)
            return .4,.5,torch.zeros(len(yy),dtype=torch.long)
        config=dict(name='probe',seed=8,width=8,bn=False,dropout=0.,lr=.01,
                    weight_decay=0.,batch_size=4,epochs=9,patience=2,min_delta=.05)
        with patch('train.evaluate',side_effect=observed):
            model,history,summary,pred=fit(config,X,y,Xv,yv,torch.device('cpu'))
        # S12 요구: stop=4·best=4·best loss=.78, 복원 모델이 4번 snapshot과 동일함을 확인.
        # 요약 수치만 보지 말고 Parameter/Buffer를 직접 대조합니다.
        # >>> S12
        self.fail("TODO S12: 검증문을 작성하세요.")
        # <<< S12

if __name__=='__main__': unittest.main()
