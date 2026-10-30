"""모델 구조만 정의합니다. 이 파일을 실행해도 학습하지 않습니다."""
from torch import nn

class SimpleANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2,8), nn.ReLU(), nn.Linear(8,2))

    def forward(self, x):
        return self.net(x)
