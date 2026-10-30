"""실습 04 · nn.Module 기반 ANN. 클래스 기초 설명은 생략하고 구조 계약만 명시합니다."""
from torch import nn

class SimpleANN(nn.Module):
    def __init__(self):
        super().__init__()
        # [요구사항 X04-1 | 등록된 파라미터 42개]
        # 구조: self.net에 Linear(2,8) → ReLU → Linear(8,2)를 등록한다.
        # 반환 logits는 입력 (N,2)에 대해 (N,2). 마지막 softmax를 붙이지 않는다.
        # Linear의 bias=True를 유지한다. 총 파라미터 수는 2*8+8+8*2+2=42.
        # net 이름과 Sequential의 모듈 순서를 유지해 저장 파일을 같은 구조로 복원할 수 있게 한다.
        # 아래 제공된 forward는 self.net(x)를 반환한다. 데이터를 .detach()하거나 CPU로 강제 이동하지 않는다.
        # 완료 기준: N=1·7의 shape, 42개 파라미터, backward 후 모든 Parameter.grad 존재.
        # 모델을 float64로 바꾸거나 .to(device)하면 내부 파라미터도 함께 변환되어야 한다.
        # >>> X04-1
        # TODO X04-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
        raise NotImplementedError("TODO X04-1")
        # <<< X04-1

    def forward(self, x):
        return self.net(x)


def copy_from_sequential(model, sequential):
    # [요구사항 X04-2 | 동일 값 복사]
    # 입력: 위 SimpleANN과 동일 2→8→2 구조의 nn.Sequential. 정상 구조·dtype는 제공됩니다.
    # sequential.state_dict를 model.net.load_state_dict(..., strict=True)로 복사합니다.
    # 반환: model. Parameter 객체나 self.net을 sequential에 직접 바인딩하지 않습니다.
    # 금지: model.net=sequential, 파라미터를 공유해 값 변경이 전파되는 구조, detach한 순전파.
    # 완료: 출력과 입력 gradient는 같고 Parameter data_ptr는 다릅니다.
    # 원본 sequential의 값·모드·gradient는 변경하지 않습니다.
    # >>> X04-2
    # TODO X04-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X04-2")
    # <<< X04-2
