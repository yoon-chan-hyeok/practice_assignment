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

    # BEGIN D20-03-B01
    s_ab=cosine(coords["A"],coords["B"])
    s_ac=cosine(coords["A"],coords["C"])
    # 해설: A-B는 약 0.9701, A-C는 -1.0입니다. 벡터 길이 대신 방향을 비교합니다.
    # END D20-03-B01

    # BEGIN D20-03-B02
    interpretation={"A_B":"방향이 비슷함" if s_ab>0.9 else "차이 있음",
                    "A_C":"반대 방향" if s_ac<-0.99 else "차이 있음",
                    "note":"코사인이 높다는 사실만으로 RAG 답변의 사실성을 보장하지 않는다"}
    # END D20-03-B02
    ranked = []
    matrix=torch.tensor(list(coords.values()),dtype=torch.float32)
    shapes={"vector":list(matrix[0].shape),"matrix":list(matrix.shape)}
    token_shape = []
    pooled_shape = []
    limitations = ["이 숫자는 예시 벡터이며 문장 의미 품질을 증명하지 않는다"]

    # BEGIN D20-03-B03
    fig,ax=plt.subplots(figsize=(6,4))
    for label,(x,y) in coords.items():
        ax.scatter(x,y,s=70); ax.annotate(label,(x,y),xytext=(5,5),textcoords="offset points")
    ax.set(xlabel="x1",ylabel="x2",title="Educational 2D vectors")
    ax.axhline(0,lw=.6);ax.axvline(0,lw=.6);ax.grid(alpha=.2)
    fig.tight_layout()
    (HERE/"outputs").mkdir(exist_ok=True)
    fig.savefig(HERE/"outputs"/"vectors.png",dpi=125)
    plt.close(fig)
    write_json(HERE/"outputs"/"cosine_report.json",{
        "vectors":coords,"cosine":{"AB":s_ab,"AC":s_ac},
        "interpretation":interpretation,"ranked":ranked,"shapes":shapes,
        "token_shape":token_shape,"pooled_shape":pooled_shape,"limitations":limitations,
    })
    print(f"[03] AB={s_ab:.4f} AC={s_ac:.4f}, shape={shapes['matrix']}")
    # END D20-03-B03

if __name__=="__main__":
    main()
