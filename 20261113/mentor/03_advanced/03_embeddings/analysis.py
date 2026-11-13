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

    # BEGIN D20-03-A01
    s_ab=cosine(coords["A"],coords["B"])
    s_ac=cosine(coords["A"],coords["C"])
    # 해설: A-B는 약 0.9701, A-C는 -1.0입니다. 벡터 길이 대신 방향을 비교합니다.
    # END D20-03-A01

    # BEGIN D20-03-A02
    interpretation={"A_B":"방향이 비슷함" if s_ab>0.9 else "차이 있음",
                    "A_C":"반대 방향" if s_ac<-0.99 else "차이 있음",
                    "note":"코사인이 높다는 사실만으로 RAG 답변의 사실성을 보장하지 않는다"}
    # END D20-03-A02

    # BEGIN D20-03-A03
    coords["D"]=[0.5,0.8]
    ranked=sorted(((key,cosine(coords["A"],val)) for key,val in coords.items() if key!="A"),
                  key=lambda x:(-x[1],x[0]))
    # END D20-03-A03

    # BEGIN D20-03-A04
    matrix=torch.tensor(list(coords.values()),dtype=torch.float32)
    shapes={"vector":list(matrix[0].shape), "matrix":list(matrix.shape)}
    # END D20-03-A04

    # BEGIN D20-03-A05
    embedding=torch.nn.Embedding(12,4)
    ids=torch.tensor([[2,5,3,0],[2,7,8,3]],dtype=torch.long)
    token_vectors=embedding(ids)
    token_shape=list(token_vectors.shape)
    # 해설: (2,4,4)는 B=2,T=4,D=4이며 문장 벡터 두 개가 아닙니다.
    # END D20-03-A05

    # BEGIN D20-03-A06
    toy_pooled=token_vectors.mean(dim=1)
    pooled_shape=list(toy_pooled.shape)
    limitations=["임의 초기화된 Token 벡터의 평균은 학습된 Sentence Embedding이 아니다",
                 "2D 투영에서 가까워 보여도 원래 고차원 이웃 관계가 보존된다고 보장되지 않는다"]
    # END D20-03-A06

    # BEGIN D20-03-A07
    save_vector_plot(coords,HERE/"outputs"/"vectors.png")
    write_json(HERE/"outputs"/"cosine_report.json",{
        "vectors":coords,"cosine":{"AB":s_ab,"AC":s_ac},
        "interpretation":interpretation,"ranked":ranked,"shapes":shapes,
        "token_shape":token_shape,"pooled_shape":pooled_shape,"limitations":limitations,
    })
    print(f"[03] AB={s_ab:.4f} AC={s_ac:.4f}, shape={shapes['matrix']}")
    # END D20-03-A07

