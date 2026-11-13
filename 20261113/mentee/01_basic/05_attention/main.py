from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
import math
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from common.support import write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def main():
    q=torch.tensor([[1.,0.],[0.,1.],[1.,1.]])
    k,v=q.clone(),q.clone()

    # TODO D20-05-B01: Scaled Dot-Product Q@K.T/sqrt(d_k)로 (3,3) Score를 계산하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-B01
    scores = q @ k.T  # TODO: / math.sqrt(q.shape[-1])로 Scale 적용
    # TODO: assert scores.shape == (3, 3) 확인
    raise NotImplementedError("D20-05-B01: TODO를 완성하세요")
    # END D20-05-B01

    # TODO D20-05-B02: 미래 Key를 차단하는 upper-triangle Causal Mask를 작성하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-B02
    mask = torch.zeros((3, 3), dtype=torch.bool)  # TODO: torch.triu(..., diagonal=1)
    masked_scores = scores.clone()               # TODO: mask=True 위치를 -inf로 채우기
    raise NotImplementedError("D20-05-B02: TODO를 완성하세요")
    # END D20-05-B02

    # TODO D20-05-B03: Score를 Softmax Weight로 바꾸고 Mask된 칸=0, 행 합=1을 확인하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-B03
    weights = torch.softmax(torch.zeros_like(scores), dim=-1)  # TODO: masked_scores 사용
    row_sums = weights.sum(dim=-1)  # 각 Query 행의 합
    # TODO: assert torch.allclose(row_sums, torch.ones(3))
    # TODO: assert torch.all(weights[mask] == 0)
    raise NotImplementedError("D20-05-B03: TODO를 완성하세요")
    # END D20-05-B03
    plain_weights=torch.empty(0)
    diff=None
    head_weights={}
    interpretation_limit=["Attention Weight만으로 모델의 최종 판단 전체를 설명할 수 없다"]

    # TODO D20-05-B04: Score·Causal Mask·Weight·행 합과 Output을 JSON으로 저장하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-B04
    output = torch.zeros_like(v)  # TODO: weights @ v
    report = {
        "scores": [],        # TODO: scores.tolist()
        "causal_mask": [],   # TODO: mask.tolist()
        "weights": [],       # TODO: weights.tolist()
        "row_sums": [],      # TODO: row_sums.tolist()
        "output": [],        # TODO: output.tolist()
        "no_mask_weights": plain_weights.tolist(),
        "masked_vs_unmasked_l1": diff,
        "multi_head": head_weights,
        "limits": interpretation_limit,
    }
    write_json(HERE / "outputs" / "attention_report.json", report)
    raise NotImplementedError("D20-05-B04: TODO를 완성하세요")
    # END D20-05-B04

if __name__=="__main__":
    main()
