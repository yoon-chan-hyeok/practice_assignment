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

    # BEGIN D20-06-A01
    prob=torch.softmax(logits,dim=0)
    assert torch.isclose(prob.sum(),torch.tensor(1.0),atol=1e-6)
    # 해설: Logit은 확률이 아니라 상대 점수입니다. Softmax 출력이 확률 분포입니다.
    # END D20-06-A01

    # BEGIN D20-06-A02
    temperature_results={str(t):torch.softmax(logits/t,dim=0).tolist() for t in (0.5,1.0,2.0)}
    # 해설: 같은 Logit에서 T가 낮으면 상위 후보 집중, 높으면 분포 평탄화.
    # END D20-06-A02

    # BEGIN D20-06-A03
    selected_index=int(torch.argmax(prob).item())
    selected_token=labels[selected_index]
    training_vs_inference={
        "training":"정답 Token과 예측을 비교해 loss/backward/optimizer.step으로 파라미터 갱신",
        "inference":"가중치를 갱신하지 않고 현재 문맥에서 다음 Token을 선택",
        "autoregressive":"선택한 Token을 문맥에 추가하고 EOS/길이 제한까지 반복",
    }
    # END D20-06-A03

    # BEGIN D20-06-A04
    k=2
    values,indices=torch.topk(prob,k)
    normalized=(values/values.sum()).tolist()
    top_k={"indices":indices.tolist(),"labels":[labels[i] for i in indices],"normalized_probs":normalized}
    # END D20-06-A04

    # BEGIN D20-06-A05
    generator=torch.Generator().manual_seed(42)
    sampled_index=int(torch.multinomial(prob,1,generator=generator).item())
    sampled_token=labels[sampled_index]
    # 해설: Sampling은 분포에 따라 Greedy와 같을 수도 다를 수도 있습니다.
    # END D20-06-A05

    # BEGIN D20-06-A06
    sorted_p,sorted_ix=torch.sort(prob,descending=True)
    csum=torch.cumsum(sorted_p,dim=0)
    remove=csum>0.75
    remove[1:]=remove[:-1].clone()
    remove[0]=False
    keep=~remove
    kept_ix=sorted_ix[keep]
    kept_p=sorted_p[keep]
    top_p={"indices":kept_ix.tolist(),"labels":[labels[i] for i in kept_ix],
           "normalized_probs":(kept_p/kept_p.sum()).tolist()}
    # 해설: 누적확률이 p를 처음 넘기는 후보까지 포함해야 합니다.
    # END D20-06-A06

    # BEGIN D20-06-A07
    model=torch.nn.Linear(4,3,bias=False)
    optimizer=torch.optim.SGD(model.parameters(),lr=0.1)
    x=torch.tensor([[1.,0.,0.,0.]])
    target=torch.tensor([1])
    old_weight=model.weight.detach().clone()
    optimizer.zero_grad()
    loss=F.cross_entropy(model(x),target)
    loss.backward()
    optimizer.step()
    changed=not torch.allclose(old_weight,model.weight.detach())
    assert changed
    with torch.no_grad():
        eval_scores=model(x)
    training_check={"train_loss":float(loss.item()),"weights_changed":changed,
                    "inference_scores":eval_scores.squeeze(0).tolist()}
    # 해설: 이 모델은 next-token 대형 Transformer가 아닌 학습/추론 구분용 Linear 장난감입니다.
    # END D20-06-A07

    # BEGIN D20-06-A08
    kv_note={
        "stores":"이전에 계산한 Attention Key/Value를 재사용해 반복 계산을 줄임",
        "not":"영구 기억이나 사실성 검증, 학습된 새 지식이 아님",
        "tradeoff":"시퀀스가 길면 Cache 메모리 사용량이 증가",
    }
    # END D20-06-A08

    # BEGIN D20-06-A09
    write_json(HERE/"outputs"/"inference_report.json",{
        "logits":logits.tolist(),"probs":prob.tolist(),"temperature":temperature_results,
        "greedy":{"index":selected_index,"token":selected_token},
        "sampling":{"index":sampled_index,"token":sampled_token},
        "top_k":top_k,"top_p":top_p,"training_vs_inference":training_vs_inference,
        "training_step":training_check,"kv_cache":kv_note,
    })
    print("[06]",selected_token,"probs",prob.round(decimals=3).tolist())
    # END D20-06-A09

