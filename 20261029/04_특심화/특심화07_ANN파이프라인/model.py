"""실습 04 · nn.Module 기반 ANN. 클래스 기초 설명은 생략하고 구조 계약만 명시합니다."""
from torch import nn

class SimpleANN(nn.Module):
    def __init__(self):
        super().__init__()
        # [요구사항 S05 | 등록된 파라미터 42개]
        # 구조: self.net에 Linear(2,8) → ReLU → Linear(8,2)를 등록한다.
        # 반환 logits는 입력 (N,2)에 대해 (N,2). 마지막 softmax를 붙이지 않는다.
        # Linear의 bias=True를 유지한다. 총 파라미터 수는 2*8+8+8*2+2=42.
        # net 이름과 Sequential의 모듈 순서를 유지해 저장 파일을 같은 구조로 복원할 수 있게 한다.
        # 아래 제공된 forward는 self.net(x)를 반환한다. 데이터를 .detach()하거나 CPU로 강제 이동하지 않는다.
        # 완료 기준: N=1·7의 shape, 42개 파라미터, backward 후 모든 Parameter.grad 존재.
        # 모델을 float64로 바꾸거나 .to(device)하면 내부 파라미터도 함께 변환되어야 한다.

        # 지도 포인트: 일반 Python 리스트가 아닌 Sequential로 등록하여 parameters/state_dict/to가 계층을 추적하도록 합니다.
        # 해설 S05: 아래 구현은 위 요구사항을 충족하는 정답 예시입니다.
        self.net = nn.Sequential(nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2))

    def forward(self, x):
        return self.net(x)
