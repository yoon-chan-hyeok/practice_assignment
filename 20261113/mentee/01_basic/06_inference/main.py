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

def main():
    logits=torch.tensor([2.0,1.0,0.0])
    labels=["출력A","출력B","출력C"]

    # TODO D20-06-B01: Logit[2,1,0]을 Softmax로 바꾸어 확률의 합이 1인지 확인하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-B01
    prob = torch.zeros_like(logits)  # TODO: torch.softmax(logits, dim=0)
    # TODO: assert torch.isclose(prob.sum(), torch.tensor(1.0), atol=1e-6)
    raise NotImplementedError("D20-06-B01: TODO를 완성하세요")
    # END D20-06-B01

    # TODO D20-06-B02: Temperature 0.5·1.0·2.0에서 확률 분포를 비교하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-B02
    temperature_results = {}
    for temperature in (0.5, 1.0, 2.0):
        temperature_results[str(temperature)] = []  # TODO: softmax(logits/temperature) 결과
    raise NotImplementedError("D20-06-B02: TODO를 완성하세요")
    # END D20-06-B02

    # TODO D20-06-B03: Greedy로 다음 Token 후보를 선택하고 학습/추론 차이를 기록하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-B03
    selected_index = -1    # TODO: int(torch.argmax(prob).item())
    selected_token = ""     # TODO: labels[selected_index]
    training_vs_inference = {
        "training": "",       # TODO: loss·backward·파라미터 업데이트
        "inference": "",      # TODO: 가중치를 바꾸지 않고 다음 Token 예측
        "autoregressive": "", # TODO: 생성 Token을 다시 문맥에 추가
    }
    raise NotImplementedError("D20-06-B03: TODO를 완성하세요")
    # END D20-06-B03
    top_k={}
    sampled_index=None
    sampled_token=None
    top_p={}
    training_check={}
    kv_note={"stores":"이전 K/V 재사용","not":"학습이나 장기 기억이 아님"}

    # TODO D20-06-B04: 확률·선택·학습/추론 차이를 inference_report.json에 기록하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-B04
    report = {
        "logits": logits.tolist(),
        "probs": [],          # TODO: prob.tolist()
        "temperature": temperature_results,
        "greedy": {"index": selected_index, "token": selected_token},
        "sampling": {"index": sampled_index, "token": sampled_token},
        "top_k": top_k,
        "top_p": top_p,
        "training_vs_inference": training_vs_inference,
        "training_step": training_check,
        "kv_cache": kv_note,
    }
    write_json(HERE / "outputs" / "inference_report.json", report)
    raise NotImplementedError("D20-06-B04: TODO를 완성하세요")
    # END D20-06-B04

if __name__=="__main__":
    main()
