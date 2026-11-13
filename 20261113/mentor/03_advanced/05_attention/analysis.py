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
from plotting import save_attention_heatmap
from common.support import write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def run_analysis():
    q=torch.tensor([[1.,0.],[0.,1.],[1.,1.]])
    k,v=q.clone(),q.clone()

    # BEGIN D20-05-A01
    scores=q@k.T/math.sqrt(q.shape[-1])
    assert scores.shape==(3,3)
    # 해설: 행은 Query, 열은 Key 위치입니다. Softmax 전 Score는 확률이 아닙니다.
    # END D20-05-A01

    # BEGIN D20-05-A02
    mask=torch.triu(torch.ones(3,3,dtype=torch.bool),diagonal=1)
    masked_scores=scores.masked_fill(mask,float("-inf"))
    # 해설: Bool Mask=True를 막는 의미로 사용하는 여기의 표현은 MultiheadAttention과 같습니다.
    # END D20-05-A02

    # BEGIN D20-05-A03
    weights=torch.softmax(masked_scores,dim=-1)
    row_sums=weights.sum(dim=-1)
    assert torch.allclose(row_sums,torch.ones(3),atol=1e-6)
    assert torch.all(weights[mask]==0)
    # 해설: 모든 Query 행에 유효한 Key가 최소 한 개 있어야 NaN을 피할 수 있습니다.
    # END D20-05-A03

    # BEGIN D20-05-A04
    plain_weights=torch.softmax(scores,dim=-1)
    diff=float(torch.abs(plain_weights-weights).sum())
    # 해설: 미래 Token의 Weight가 0으로 바뀌고 나머지 허용 위치는 재정규화됩니다.
    # END D20-05-A04

    # BEGIN D20-05-A05
    save_attention_heatmap(weights,HERE/"outputs"/"attention_heatmap.png")
    # END D20-05-A05

    # BEGIN D20-05-A06
    # 해설: 각 모듈은 학습되지 않은 서로 다른 랜덤 projection입니다. 품질 우열 비교가 아닙니다.
    x=torch.tensor([[[1.,0.,0.,1.],[0.,1.,1.,0.],[1.,1.,0.,0.]]])
    head_weights={}
    for heads in (1,2):
        torch.manual_seed(42)
        mha=torch.nn.MultiheadAttention(4,heads,batch_first=True,dropout=0.0)
        mha.eval()
        with torch.no_grad():
            out,w=mha(x,x,x,attn_mask=mask,need_weights=True,average_attn_weights=False)
        assert w.shape==(1,heads,3,3)
        assert torch.all(w[:,:][...,mask]==0)
        head_weights[str(heads)]={"shape":list(w.shape),"query0":w[0,:,0,:].tolist()}
    # END D20-05-A06

    # BEGIN D20-05-A07
    interpretation_limit=[
        "Attention은 Value 혼합 비율이지 모든 후속 FFN·Residual·Head 계산을 포함하지 않는다",
        "학습되지 않은 장난감 Head의 가중치에서 자연어 이해를 추론할 수 없다",
        "Head 수 변화 외에도 투영 파라미터·분할 차원이 달라 직접 성능 비교가 아니다",
    ]
    # END D20-05-A07

    # BEGIN D20-05-A08
    output=weights@v
    write_json(HERE/"outputs"/"attention_report.json",{
        "scores":scores.tolist(),"causal_mask":mask.tolist(),
        "weights":weights.tolist(),"row_sums":row_sums.tolist(),
        "output":output.tolist(),"no_mask_weights":plain_weights.tolist(),
        "masked_vs_unmasked_l1":diff,"multi_head":head_weights,
        "limits":interpretation_limit,
    })
    print("[05]",weights.round(decimals=2).tolist(),"row_sums",row_sums.tolist())
    # END D20-05-A08

