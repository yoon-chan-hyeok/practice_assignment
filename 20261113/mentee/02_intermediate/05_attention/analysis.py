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

    # TODO D20-05-I01: Scaled Dot-Product Q@K.T/sqrt(d_k)로 (3,3) Score를 계산하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I01
    raise NotImplementedError("D20-05-I01: TODO를 완성하세요")
    # END D20-05-I01

    # TODO D20-05-I02: 미래 Key를 차단하는 upper-triangle Causal Mask를 작성하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I02
    raise NotImplementedError("D20-05-I02: TODO를 완성하세요")
    # END D20-05-I02

    # TODO D20-05-I03: Score를 Softmax Weight로 바꾸고 Mask된 칸=0, 행 합=1을 확인하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I03
    raise NotImplementedError("D20-05-I03: TODO를 완성하세요")
    # END D20-05-I03

    # TODO D20-05-I04: Mask 없는 Softmax 결과와 Mask 있는 결과를 비교하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I04
    raise NotImplementedError("D20-05-I04: TODO를 완성하세요")
    # END D20-05-I04

    # TODO D20-05-I05: Causal Weight를 Query행·Key열 기준으로 Heatmap에 저장하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I05
    raise NotImplementedError("D20-05-I05: TODO를 완성하세요")
    # END D20-05-I05
    head_weights={}
    interpretation_limit=["Attention Weight만으로 모델의 최종 판단 전체를 설명할 수 없다"]

    # TODO D20-05-I06: Score·Causal Mask·Weight·행 합과 Output을 JSON으로 저장하세요.
    # 입력·대상: PPT Q/K/V 3×2 예제와 Bool Causal Mask를 사용합니다.
    # 완료 확인: outputs/attention_report.json의 masked weights=0, row_sums=1을 확인합니다.
    # 주의: Softmax 이전 scores와 이후 weights를 구분하고, 행=Query·열=Key로 표시합니다.
    # BEGIN D20-05-I06
    raise NotImplementedError("D20-05-I06: TODO를 완성하세요")
    # END D20-05-I06

