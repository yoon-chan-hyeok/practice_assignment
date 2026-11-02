"""실습 08 심화 추가 검증. 프로젝트 폴더에서 python -m unittest discover -s tests -v."""
from pathlib import Path
import sys,unittest
from copy import deepcopy
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from models import classifier
from train import evaluate

class ContractTests(unittest.TestCase):
    def test_evaluation_preserves_state(self):
        torch.manual_seed(18)
        model=classifier('Transformer').train()
        model.head.eval()  # 일부 하위 모듈은 별도 모드여도 원래대로 돌아와야 한다.
        for p in model.parameters(): p.grad=torch.ones_like(p)
        state=deepcopy(model.state_dict()); modes=[m.training for m in model.modules()]
        grads=[p.grad.clone() for p in model.parameters()]
        batch={'x':torch.randn(3,6,3),'lengths':torch.tensor([6,4,5]),'y':torch.tensor([0,1,0])}
        result=evaluate(model,batch,'classification')
        # TODO D11: 상태·기존 gradient·하위모드·결과 그래프를 검사한다.
        # 정상 실행 여부만 검사하지 않는다. 반환 예측은 requires_grad=False여야 한다.
        # BEGIN D11
        self.fail('TODO D11: 평가 상태 보존 검사')
        # END D11

    def test_padding_does_not_change_valid_prediction(self):
        torch.manual_seed(19)
        x=torch.randn(3,6,3); lengths=torch.tensor([6,3,5])
        mask=torch.arange(6).unsqueeze(0)>=lengths.unsqueeze(1)
        changed=x.clone(); changed[mask]=1234.0
        # TODO D12: LSTM/Transformer 각각의 정상 출력과 Padding 변경 출력을 대조한다.
        # 실제 관측값과 lengths는 바꾸지 않는다. eval에서 atol=1e-5, rtol=1e-5로 검사한다.
        # BEGIN D12
        self.fail('TODO D12: Padding 불변 검사')
        # END D12

if __name__=='__main__': unittest.main()
