from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
import torch
import torch.nn.functional as F
from common.support import write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def run_analysis():
    logits=torch.tensor([2.0,1.0,0.0])
    labels=["출력A","출력B","출력C"]

    # BEGIN D20-06-I01
    prob=torch.softmax(logits,dim=0)
    assert torch.isclose(prob.sum(),torch.tensor(1.0),atol=1e-6)
    # 해설: Logit은 확률이 아니라 상대 점수입니다. Softmax 출력이 확률 분포입니다.
    # END D20-06-I01

    # BEGIN D20-06-I02
    temperature_results={str(t):torch.softmax(logits/t,dim=0).tolist() for t in (0.5,1.0,2.0)}
    # 해설: 같은 Logit에서 T가 낮으면 상위 후보 집중, 높으면 분포 평탄화.
    # END D20-06-I02

    # BEGIN D20-06-I03
    selected_index=int(torch.argmax(prob).item())
    selected_token=labels[selected_index]
    training_vs_inference={
        "training":"정답 Token과 예측을 비교해 loss/backward/optimizer.step으로 파라미터 갱신",
        "inference":"가중치를 갱신하지 않고 현재 문맥에서 다음 Token을 선택",
        "autoregressive":"선택한 Token을 문맥에 추가하고 EOS/길이 제한까지 반복",
    }
    # END D20-06-I03

    # BEGIN D20-06-I04
    k=2
    values,indices=torch.topk(prob,k)
    normalized=(values/values.sum()).tolist()
    top_k={"indices":indices.tolist(),"labels":[labels[i] for i in indices],"normalized_probs":normalized}
    # END D20-06-I04

    # BEGIN D20-06-I05
    generator=torch.Generator().manual_seed(42)
    sampled_index=int(torch.multinomial(prob,1,generator=generator).item())
    sampled_token=labels[sampled_index]
    # 해설: Sampling은 분포에 따라 Greedy와 같을 수도 다를 수도 있습니다.
    # END D20-06-I05
    top_p={}
    training_check={}
    kv_note={"stores":"이전 K/V 재사용","not":"학습이나 장기 기억이 아님"}

    # BEGIN D20-06-I06
    write_json(HERE/"outputs"/"inference_report.json",{
        "logits":logits.tolist(),"probs":prob.tolist(),"temperature":temperature_results,
        "greedy":{"index":selected_index,"token":selected_token},
        "sampling":{"index":sampled_index,"token":sampled_token},
        "top_k":top_k,"top_p":top_p,"training_vs_inference":training_vs_inference,
        "training_step":training_check,"kv_cache":kv_note,
    })
    print("[06]",selected_token,"probs",prob.round(decimals=3).tolist())
    # END D20-06-I06

