"""실습 08 추가: pytest 없이 표준 unittest로 두 검증을 직접 완성합니다."""
import sys
from pathlib import Path
import unittest
import copy
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import SimpleANN
from train import train_one_epoch, evaluate

class TrainingChecks(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        torch.set_num_threads(1)
        self.model = SimpleANN()
        self.X = torch.tensor([[1.,2.], [-1.,0.], [2.,1.], [0.,0.], [1.,-1.], [-2.,1.], [3.,2.]])
        self.y = torch.tensor([1,0,1,0,1,0,1])

    def test_last_batch_weighting(self):
        loader = DataLoader(TensorDataset(self.X, self.y), batch_size=3, shuffle=False)
        loss_fn = nn.CrossEntropyLoss()
        # lr=0은 검사용입니다. 가중치를 고정해야 배치 분할 효과만 비교할 수 있습니다.
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.0)
        expected = loss_fn(self.model(self.X), self.y).item()
        actual = train_one_epoch(self.model, loader, loss_fn, optimizer, torch.device("cpu"))
        # H11 요구: 7건을 3·3·1로 나눈 손실이 전체 손실과 소수점5자리까지 같음을 검사하세요.
        # 수치를 출력만 하지 말고 self.assertAlmostEqual을 사용합니다.
        # >>> H11
        # TODO H11: actual과 expected가 같은지 검사하세요.
        self.fail("TODO H11 미완성")
        # <<< H11

    def test_evaluation_does_not_learn(self):
        self.model(self.X).sum().backward()
        before = copy.deepcopy(self.model.state_dict())
        grads = [p.grad.clone() for p in self.model.parameters()]
        loss, accuracy, prediction = evaluate(self.model, self.X, self.y, nn.CrossEntropyLoss(), torch.device("cpu"))
        # H12 요구: 평가 전후 각 Parameter 값과 기존 grad가 모두 같은지 assertTrue로 검사하세요.
        # 추가: prediction에 requires_grad가 없음을 assertFalse로 확인합니다.
        # 모델의 eval 모드 전환은 정상입니다. 이 단계는 모드 복구까지 요구하지 않습니다.
        # >>> H12
        # TODO H12: 가중치·gradient·예측의 그래프 여부를 검사하세요.
        self.fail("TODO H12 미완성")
        # <<< H12

if __name__ == "__main__":
    unittest.main(verbosity=2)
