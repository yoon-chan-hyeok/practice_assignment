"""실습 02 · 입력 계약. 오류 처리는 특심화에만 요구합니다."""
import torch

def validate_batch(X: torch.Tensor, y: torch.Tensor) -> None:
    # [요구사항 S02 | ANN 입력 계약]
    # 입력: X와 y. 허용 X는 float32/float64 Tensor, shape (N,2), N>=1, 모든 값 finite.
    # 허용 y는 torch.long Tensor, shape (N,), 값은 0 또는 1, X와 동일 device.
    # 반환: 조건을 만족하면 None. 입력·dtype·device·shape를 자동 수정하지 않는다.
    # 예외: Tensor가 아니거나 dtype이 잘못되면 TypeError.
    # shape/행 수/빈 입력/비유한 값/라벨 범위/device 불일치는 ValueError.
    # 검사 순서: Tensor 여부 → dtype → shape/행 수 → device → 값.
    # 금지: 잘못된 행 삭제, y.float() 허용, X.nan_to_num() 같은 자동 복구, test 호출.
    # 검사 후 X와 y의 값·device·requires_grad는 그대로 유지되어야 한다.
    # 필수 예: N=1 정상 통과, y=(N,1) 거부, NaN 거부, 라벨2 거부, N=0 거부.

    # 지도 포인트: 이 단계에서는 자동 보정보다 계약 위반을 드러냅니다. 기본필수에는 이런 검사 부담을 옮기지 않습니다.
    # 해설 S02: 아래 구현은 위 요구사항을 충족하는 정답 예시입니다.
    if not isinstance(X, torch.Tensor) or not isinstance(y, torch.Tensor):
        raise TypeError("X와 y는 Tensor여야 합니다.")
    if X.dtype not in (torch.float32, torch.float64) or y.dtype != torch.long:
        raise TypeError("X는 float32/float64, y는 long이어야 합니다.")
    if X.ndim != 2 or X.shape[1] != 2 or y.ndim != 1:
        raise ValueError("X=(N,2), y=(N,)이어야 합니다.")
    if len(X) == 0 or len(X) != len(y):
        raise ValueError("행 수가 일치하는 비어 있지 않은 입력이어야 합니다.")
    if X.device != y.device:
        raise ValueError("X와 y의 device가 다릅니다.")
    if not bool(torch.isfinite(X).all()) or not bool(((y == 0) | (y == 1)).all()):
        raise ValueError("X는 유한해야 하고 y는 0 또는 1이어야 합니다.")
    # 검사만 하고 변환하지 않으므로 이후 모델에 원래 입력이 그대로 전달됩니다.
    return None

