"""실습 02 · 입력 계약. 오류 처리는 특심화에만 요구합니다."""
import torch

def validate_batch(X: torch.Tensor, y: torch.Tensor) -> None:
    # [요구사항 X02-1 | ANN 입력 계약]
    # 입력: X와 y. 허용 X는 float32/float64 Tensor, shape (N,2), N>=1, 모든 값 finite.
    # 허용 y는 torch.long Tensor, shape (N,), 값은 0 또는 1, X와 동일 device.
    # 반환: 조건을 만족하면 None. 입력·dtype·device·shape를 자동 수정하지 않는다.
    # 예외: Tensor가 아니거나 dtype이 잘못되면 TypeError.
    # shape/행 수/빈 입력/비유한 값/라벨 범위/device 불일치는 ValueError.
    # 검사 순서: Tensor 여부 → dtype → shape/행 수 → device → 값.
    # 금지: 잘못된 행 삭제, y.float() 허용, X.nan_to_num() 같은 자동 복구, test 호출.
    # 검사 후 X와 y의 값·device·requires_grad는 그대로 유지되어야 한다.
    # 필수 예: N=1 정상 통과, y=(N,1) 거부, NaN 거부, 라벨2 거부, N=0 거부.
    # >>> X02-1
    # TODO X02-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-1")
    # <<< X02-1


def move_batch(X, y, device):
    # [요구사항 X02-2 | 검증 후 이동, 원본 보존]
    # 먼저 validate_batch(X,y). 정상 입력의 shape/dtype는 변경하지 않습니다.
    # 반환: (X.to(device), y.to(device)). X=float64인 경우도 float64를 유지합니다.
    # 같은 장치이면 Tensor가 같은 객체여도 됩니다. 이 함수는 복사 API가 아닙니다.
    # 원본의 값·requires_grad·기존 .grad를 변경하지 말고 미분 연결을 끊지 않습니다.
    # CPU/GPU 실제 장치 이동만 수행하며, 없는 CUDA 요청의 RuntimeError를 숨기지 않습니다.
    # 완료: 이동된 X,y의 장치가 같고, (moved_X.sum()).backward()가 원본 X.grad에 도달합니다.
    # >>> X02-2
    # TODO X02-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X02-2")
    # <<< X02-2
