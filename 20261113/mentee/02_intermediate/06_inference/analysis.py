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

    # TODO D20-06-I01: Logit[2,1,0]을 Softmax로 바꾸어 확률의 합이 1인지 확인하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I01
    raise NotImplementedError("D20-06-I01: TODO를 완성하세요")
    # END D20-06-I01

    # TODO D20-06-I02: Temperature 0.5·1.0·2.0에서 확률 분포를 비교하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I02
    raise NotImplementedError("D20-06-I02: TODO를 완성하세요")
    # END D20-06-I02

    # TODO D20-06-I03: Greedy로 다음 Token 후보를 선택하고 학습/추론 차이를 기록하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I03
    raise NotImplementedError("D20-06-I03: TODO를 완성하세요")
    # END D20-06-I03

    # TODO D20-06-I04: Top-k(k=2)의 후보 집합과 정규화된 확률을 구하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I04
    raise NotImplementedError("D20-06-I04: TODO를 완성하세요")
    # END D20-06-I04

    # TODO D20-06-I05: 같은 seed로 확률 샘플링을 재현하고 Greedy와 차이를 설명하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I05
    raise NotImplementedError("D20-06-I05: TODO를 완성하세요")
    # END D20-06-I05
    top_p={}
    training_check={}
    kv_note={"stores":"이전 K/V 재사용","not":"학습이나 장기 기억이 아님"}

    # TODO D20-06-I06: 확률·선택·학습/추론 차이를 inference_report.json에 기록하세요.
    # 입력·대상: PPT의 예시 Logit [2,1,0]을 사용합니다.
    # 완료 확인: outputs/inference_report.json의 확률합=1과 T별 확률 변화·후보를 확인합니다.
    # 주의: Logit은 확률이 아니며 학습과 추론에서 parameter 변화 여부가 다릅니다.
    # BEGIN D20-06-I06
    raise NotImplementedError("D20-06-I06: TODO를 완성하세요")
    # END D20-06-I06

