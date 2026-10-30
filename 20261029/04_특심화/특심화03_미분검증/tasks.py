"""실습 03 · 해석 미분 / 수치 미분 / Autograd를 독립적으로 대조합니다."""
import torch

def analytic_mse(X, target, w, b):
    # [요구사항 X03-1 | 선형식 MSE의 해석 미분]
    # 입력: CPU float64의 X=(N,D), target=(N,), w=(D,), b=스칼라. 정상 입력은 제공된다.
    # 식: prediction=X@w+b, loss=mean((prediction-target)^2).
    # 반환: (loss, grad_w, grad_b). shape는 각각 (), (D,), (). dtype은 float64.
    # 규칙: N으로 평균한 손실에 대한 미분이어야 한다. sum 손실의 기울기를 반환하면 안 된다.
    # 금지: backward, autograd.grad, nn.MSELoss, 수치 미분 함수를 호출해서 답을 얻기.
    # 입력 w/b/X/target을 수정하거나 .grad를 변경하지 않는다.
    # 완료 기준: 제공된 정상 사례에서 Autograd와 rtol=1e-8, atol=1e-10으로 일치한다.
    # 한 번 맞춘 숫자를 하드코딩하지 말고 N,D가 다른 데이터에도 적용한다.
    # >>> X03-1
    # TODO X03-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-1")
    # <<< X03-1

def central_difference(fn, w, epsilon=1e-6):
    # [요구사항 X03-2 | 중앙 차분]
    # 입력: fn은 1차원 float64 Tensor를 받아 스칼라 Tensor를 반환하는 순수 함수.
    # w는 CPU float64 1차원 Tensor, epsilon은 양수이며 기본값 1e-6.
    # 반환: w와 같은 shape/dtype/device인 기울기 Tensor, requires_grad=False.
    # 좌표 i마다 (fn(w+epsilon*e_i)-fn(w-epsilon*e_i))/(2*epsilon)을 계산한다.
    # epsilon<=0이면 ValueError. 원본 w는 값·requires_grad·기존 grad 모두 보존한다.
    # 금지: backward/autograd.grad, 원본 w를 in-place로 증감, ReLU 경계점으로 정확성 판정.
    # 매 좌표에서 분리된 복사본을 만들어야 다른 좌표의 변경이 다음 계산에 섞이지 않는다.
    # 완료 기준: 선형식 MSE처럼 매끄러운 함수에서 해석 미분과 rtol=1e-5, atol=1e-6 일치.
    # 실수 허용오차는 수치 미분용이다. CPU/GPU 전체 재현성 보장으로 해석하지 않는다.
    # >>> X03-2
    # TODO X03-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-2")
    # <<< X03-2
