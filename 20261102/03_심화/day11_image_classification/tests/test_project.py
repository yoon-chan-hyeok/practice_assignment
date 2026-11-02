"""심화 추가 과제. 공개된 평가·복원 계약을 작은 데이터로 확인한다."""
from pathlib import Path
import sys, copy, tempfile, unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from train import evaluate
from models import SmallCNN

class ProjectChecks(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        torch.set_num_threads(1)

    def test_weighted_evaluation_and_preservation(self):
        # D11 요구: 5개 표본·batch=3에서 마지막 2개도 모두 반영되는지 확인한다.
        # 전체 5개를 한 번에 계산한 CE와 loss가 일치해야 한다(atol=1e-6).
        # 호출 전 혼합 train/eval 플래그, BN buffer, weight, 기존 grad를 보존한다.
        model = SmallCNN(width=4, batchnorm=True, dropout=0.3)
        model.train()
        model.fc.eval()
        x, y = torch.rand(5, 3, 16, 16), torch.tensor([0,1,1,0,1])
        loader = DataLoader(TensorDataset(x,y), batch_size=3, shuffle=False)
        for p in model.parameters(): p.grad = torch.ones_like(p)
        before = copy.deepcopy(model.state_dict())
        modes = [m.training for m in model.modules()]
        grads = [p.grad.clone() for p in model.parameters()]
        reference = copy.deepcopy(model).eval()
        with torch.no_grad(): expected = nn.functional.cross_entropy(reference(x), y).item()
        loss, accuracy, logits, labels = evaluate(model, loader, torch.device('cpu'))
        # BEGIN D11
        # TODO D11: 위 요구사항의 검증 문장을 작성하세요.
        raise NotImplementedError("TODO D11")
        # END D11

    def test_saved_state_recovers_logits(self):
        # D12 요구: 신뢰하는 자체 state_dict만 저장·weights_only로 읽는다.
        # 새 모델의 동일 입력 logits를 atol=1e-7, rtol=1e-5로 비교한다.
        # state_dict 변수를 원본 모델에 대입만 하는 검사는 실제 복원 검사가 아니다.
        model = SmallCNN(width=4).eval()
        x = torch.rand(3,3,16,16)
        with torch.no_grad(): expected = model(x)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'own_state.pt'
            torch.save({'state_dict': model.state_dict(), 'width': 4}, path)
            saved = torch.load(path, map_location='cpu', weights_only=True)
            restored = SmallCNN(width=saved['width']).eval()
            # BEGIN D12
            # TODO D12: 위 요구사항의 검증 문장을 작성하세요.
            raise NotImplementedError("TODO D12")
            # END D12

if __name__ == '__main__': unittest.main()
