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

def run_analysis():
    q=torch.tensor([[1.,0.],[0.,1.],[1.,1.]])
    k,v=q.clone(),q.clone()

    # BEGIN D20-05-I01
    scores=q@k.T/math.sqrt(q.shape[-1])
    assert scores.shape==(3,3)
    # 해설: 행은 Query, 열은 Key 위치입니다. Softmax 전 Score는 확률이 아닙니다.
    # END D20-05-I01

    # BEGIN D20-05-I02
    mask=torch.triu(torch.ones(3,3,dtype=torch.bool),diagonal=1)
    masked_scores=scores.masked_fill(mask,float("-inf"))
    # 해설: Bool Mask=True를 막는 의미로 사용하는 여기의 표현은 MultiheadAttention과 같습니다.
    # END D20-05-I02

    # BEGIN D20-05-I03
    weights=torch.softmax(masked_scores,dim=-1)
    row_sums=weights.sum(dim=-1)
    assert torch.allclose(row_sums,torch.ones(3),atol=1e-6)
    assert torch.all(weights[mask]==0)
    # 해설: 모든 Query 행에 유효한 Key가 최소 한 개 있어야 NaN을 피할 수 있습니다.
    # END D20-05-I03

    # BEGIN D20-05-I04
    plain_weights=torch.softmax(scores,dim=-1)
    diff=float(torch.abs(plain_weights-weights).sum())
    # 해설: 미래 Token의 Weight가 0으로 바뀌고 나머지 허용 위치는 재정규화됩니다.
    # END D20-05-I04

    # BEGIN D20-05-I05
    fig,ax=plt.subplots(figsize=(4.8,4))
    heat=ax.imshow(weights.numpy(),vmin=0,vmax=1,cmap="Blues")
    ax.set(xticks=range(3),yticks=range(3),xlabel="Key index",ylabel="Query index")
    for i in range(3):
        for j in range(3):
            ax.text(j,i,f"{weights[i,j]:.2f}",ha="center",va="center")
    fig.colorbar(heat,ax=ax)
    fig.tight_layout()
    (HERE/"outputs").mkdir(exist_ok=True)
    fig.savefig(HERE/"outputs"/"attention_heatmap.png",dpi=130)
    plt.close(fig)
    # END D20-05-I05
    head_weights={}
    interpretation_limit=["Attention Weight만으로 모델의 최종 판단 전체를 설명할 수 없다"]

    # BEGIN D20-05-I06
    output=weights@v
    write_json(HERE/"outputs"/"attention_report.json",{
        "scores":scores.tolist(),"causal_mask":mask.tolist(),
        "weights":weights.tolist(),"row_sums":row_sums.tolist(),
        "output":output.tolist(),"no_mask_weights":plain_weights.tolist(),
        "masked_vs_unmasked_l1":diff,"multi_head":head_weights,
        "limits":interpretation_limit,
    })
    print("[05]",weights.round(decimals=2).tolist(),"row_sums",row_sums.tolist())
    # END D20-05-I06

