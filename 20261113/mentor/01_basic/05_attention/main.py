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

    # BEGIN D20-05-B01
    scores=q@k.T/math.sqrt(q.shape[-1])
    assert scores.shape==(3,3)
    # 해설: 행은 Query, 열은 Key 위치입니다. Softmax 전 Score는 확률이 아닙니다.
    # END D20-05-B01

    # BEGIN D20-05-B02
    mask=torch.triu(torch.ones(3,3,dtype=torch.bool),diagonal=1)
    masked_scores=scores.masked_fill(mask,float("-inf"))
    # 해설: Bool Mask=True를 막는 의미로 사용하는 여기의 표현은 MultiheadAttention과 같습니다.
    # END D20-05-B02

    # BEGIN D20-05-B03
    weights=torch.softmax(masked_scores,dim=-1)
    row_sums=weights.sum(dim=-1)
    assert torch.allclose(row_sums,torch.ones(3),atol=1e-6)
    assert torch.all(weights[mask]==0)
    # 해설: 모든 Query 행에 유효한 Key가 최소 한 개 있어야 NaN을 피할 수 있습니다.
    # END D20-05-B03
    plain_weights=torch.empty(0)
    diff=None
    head_weights={}
    interpretation_limit=["Attention Weight만으로 모델의 최종 판단 전체를 설명할 수 없다"]

    # BEGIN D20-05-B04
    output=weights@v
    write_json(HERE/"outputs"/"attention_report.json",{
        "scores":scores.tolist(),"causal_mask":mask.tolist(),
        "weights":weights.tolist(),"row_sums":row_sums.tolist(),
        "output":output.tolist(),"no_mask_weights":plain_weights.tolist(),
        "masked_vs_unmasked_l1":diff,"multi_head":head_weights,
        "limits":interpretation_limit,
    })
    print("[05]",weights.round(decimals=2).tolist(),"row_sums",row_sums.tolist())
    # END D20-05-B04

if __name__=="__main__":
    main()
