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
from common.support import cosine, write_json

torch.manual_seed(42)
torch.set_num_threads(1)

def main():
    # PPT 33장과 같은 교육용 2D 벡터. SentenceTransformer가 만든 실제 의미 벡터가 아닙니다.
    coords = {"A":[1.0,0.0],"B":[0.8,0.2],"C":[-1.0,0.0]}

    # TODO D20-03-B01: A-B와 A-C 벡터의 Cosine Similarity를 계산하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-B01
    s_ab = 0.0  # TODO: cosine(coords["A"], coords["B"])
    s_ac = 0.0  # TODO: cosine(coords["A"], coords["C"])
    raise NotImplementedError("D20-03-B01: TODO를 완성하세요")
    # END D20-03-B01

    # TODO D20-03-B02: 점수의 부호·범위를 보고 어느 벡터 방향이 유사한지 판별하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-B02
    interpretation = {
        "A_B": "",  # TODO: s_ab의 방향 해석 (힌트: 1에 가까운가?)
        "A_C": "",  # TODO: s_ac의 방향 해석 (힌트: -1에 가까운가?)
        "note": "유사도 점수만으로 답변의 사실성을 보장하지 않는다",
    }
    raise NotImplementedError("D20-03-B02: TODO를 완성하세요")
    # END D20-03-B02
    ranked = []
    matrix=torch.tensor(list(coords.values()),dtype=torch.float32)
    shapes={"vector":list(matrix[0].shape),"matrix":list(matrix.shape)}
    token_shape = []
    pooled_shape = []
    limitations = ["이 숫자는 예시 벡터이며 문장 의미 품질을 증명하지 않는다"]

    # TODO D20-03-B03: 2D 점 그래프와 cosine_report.json을 outputs에 저장하세요.
    # 입력·대상: PPT의 A/B/C 2차원 좌표를 사용합니다.
    # 완료 확인: outputs/cosine_report.json, vectors.png를 확인합니다.
    # 주의: 수치 비교는 모델의 문장 의미 이해나 RAG 정확성 평가가 아닙니다.
    # BEGIN D20-03-B03
    fig, ax = plt.subplots(figsize=(6, 4))
    for label, (x, y) in coords.items():
        ax.scatter(x, y)  # 각 벡터를 점으로 표시
        # TODO: ax.annotate(...)로 점 옆에 A/B/C 이름 표시
    ax.set(xlabel="x1", ylabel="x2", title="Educational 2D vectors")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    (HERE / "outputs").mkdir(exist_ok=True)
    fig.savefig(HERE / "outputs" / "vectors.png")
    plt.close(fig)
    write_json(HERE / "outputs" / "cosine_report.json", {
        "vectors": coords,
        "cosine": {"AB": 0.0, "AC": 0.0},  # TODO: 계산한 s_ab와 s_ac
        "interpretation": interpretation,
        "ranked": ranked,
        "shapes": shapes,
        "token_shape": token_shape,
        "pooled_shape": pooled_shape,
        "limitations": limitations,
    })
    raise NotImplementedError("D20-03-B03: TODO를 완성하세요")
    # END D20-03-B03

if __name__=="__main__":
    main()
