from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
import torch
import torch.nn.functional as F
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from plotting import save_vector_plot
from common.support import cosine, write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def run_analysis():
    # PPT 33장과 같은 교육용 2D 벡터. SentenceTransformer가 만든 실제 의미 벡터가 아닙니다.
    coords = {"A":[1.0,0.0],"B":[0.8,0.2],"C":[-1.0,0.0]}

    # TODO D20-03-A01: A-B와 A-C 벡터의 Cosine Similarity를 계산하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A01
    raise NotImplementedError("D20-03-A01: TODO를 완성하세요")
    # END D20-03-A01

    # TODO D20-03-A02: 점수의 부호·범위를 보고 어느 벡터 방향이 유사한지 판별하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A02
    raise NotImplementedError("D20-03-A02: TODO를 완성하세요")
    # END D20-03-A02

    # TODO D20-03-A03: 2차원 후보 D를 추가해 가장 유사한 벡터를 점수순으로 정리하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A03
    raise NotImplementedError("D20-03-A03: TODO를 완성하세요")
    # END D20-03-A03

    # TODO D20-03-A04: 벡터를 행렬로 쌓은 Tensor shape (개수, 차원)를 기록하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A04
    raise NotImplementedError("D20-03-A04: TODO를 완성하세요")
    # END D20-03-A04

    # TODO D20-03-A05: Token ID를 nn.Embedding에 넣고 출력 shape를 확인하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A05
    raise NotImplementedError("D20-03-A05: TODO를 완성하세요")
    # END D20-03-A05

    # TODO D20-03-A06: 임의 Token 벡터 평균을 계산하고 의미 검색용 모델과 차이를 기록하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A06
    raise NotImplementedError("D20-03-A06: TODO를 완성하세요")
    # END D20-03-A06

    # TODO D20-03-A07: 2D 점 그래프와 cosine_report.json을 outputs에 저장하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-A07
    raise NotImplementedError("D20-03-A07: TODO를 완성하세요")
    # END D20-03-A07

