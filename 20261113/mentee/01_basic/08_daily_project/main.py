from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
import math
import torch
import torch.nn.functional as F
from common.support import DATA, ToyTokenizer, attention, cosine, write_json, write_md

torch.manual_seed(42)
torch.set_num_threads(1)

# PPT 78~85장의 일일프로젝트. 앞선 계산을 재사용하는 통합 결과입니다.
# 이 코드는 실제 학습된 LLM이 아니며 예시 Token·Vector·Attention·Logit을 결합합니다.
def main():
    texts=[d["content"] for d in DATA]
    tokenizer=ToyTokenizer(texts)

    # TODO D20-08-B01: 공통 지식 A의 문장을 Token·ID로 분석하고 Token 수·Context 제한을 기록하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B01
    input_sentence = ""  # TODO: DATA[0]["content"] 가져오기
    token_report = tokenizer.encode(input_sentence, max_length=12)
    # TODO: token_report["valid_length"]가 12 이하인지 assert 확인
    raise NotImplementedError("D20-08-B01: TODO를 완성하세요")
    # END D20-08-B01

    # TODO D20-08-B02: 교육용 벡터 A/B/C의 Cosine 표를 만들고 비슷한 방향을 찾아보세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B02
    coords = {"A": [1., 0.], "B": [.8, .2], "C": [-1., 0.]}
    cosine_table = {
        "A_B": 0.0,  # TODO: cosine(coords["A"], coords["B"])
        "A_C": 0.0,  # TODO: cosine(coords["A"], coords["C"])
    }
    raise NotImplementedError("D20-08-B02: TODO를 완성하세요")
    # END D20-08-B02

    # TODO D20-08-B03: Q/K/V 3×2 Attention에 Causal Mask를 적용하고 행 합=1·미래 가중치=0을 확인하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B03
    q = torch.tensor([[1., 0.], [0., 1.], [1., 1.]])  # 교육용 Q/K/V 입력
    scores, weights, attn_out, mask = attention(q, q, q, causal=False)  # TODO: causal=True
    row_sums = weights.sum(dim=-1)
    # TODO: 행 합이 1이고 미래 Token에 대한 가중치가 0인지 assert 확인
    raise NotImplementedError("D20-08-B03: TODO를 완성하세요")
    # END D20-08-B03

    # TODO D20-08-B04: Logit→Softmax→Greedy 다음 Token 선택 흐름을 구현하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B04
    logits = torch.tensor([2., 1., 0.])
    probs = torch.zeros_like(logits)  # TODO: torch.softmax(logits, dim=0)
    selected = -1                     # TODO: int(probs.argmax().item())
    next_token = ""                   # TODO: ["출력A", "출력B", "출력C"][selected]
    raise NotImplementedError("D20-08-B04: TODO를 완성하세요")
    # END D20-08-B04
    custom_lengths=[]
    mask_diff=None
    platform_map={"FastAPI":"요청·응답","PostgreSQL":"원본 저장","LLM":"Token 출력", "RAG":"외부 근거(후속)", "Agent":"도구 제어(후속)"}
    limitations=["교육용 수치 예제는 실제 학습된 LLM과 다르다"]

    # TODO D20-08-B05: PPT의 네 단계와 플랫폼 연결 그림을 Markdown으로 완성하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B05
    lines = [
        "# 일일프로젝트: 문장 하나가 LLM 출력이 되기까지", "",
        "입력: ",                 # TODO: input_sentence 연결
        "- Token 및 Token ID: ",  # TODO: token_report에서 필요한 값 가져오기
        "- Cosine A-B / A-C: ", # TODO: cosine_table 결과
        "- Attention 행 합: ",  # TODO: weights.sum(dim=-1)
        "- 다음 Token: ",        # TODO: next_token
        "", "```mermaid", "flowchart LR",
        "  U[입력] --> T[Token/ID] --> E[Embedding] --> A[Attention] --> O[출력]",
        "```", "",
        "주의: 실제 RAG·Agent를 수행한 결과가 아닙니다.",
    ]
    write_md(HERE / "outputs" / "one_page_summary.md", "\n".join(lines) + "\n")
    raise NotImplementedError("D20-08-B05: TODO를 완성하세요")
    # END D20-08-B05

    # TODO D20-08-B06: Token·Cosine·Attention·Logit 검증 결과를 종합 JSON으로 저장하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-B06
    report = {
        "source_data": DATA,
        "token": {},                # TODO: token_report
        "cosine": {},               # TODO: cosine_table
        "scores_shape": [],        # TODO: list(scores.shape)
        "attention_weights": [],   # TODO: weights.tolist()
        "row_sums": [],            # TODO: weights.sum(dim=-1).tolist()
        "causal_mask": [],         # TODO: mask.tolist()
        "logits": logits.tolist(),
        "probabilities": [],       # TODO: probs.tolist()
        "next_token_demo": "",    # TODO: next_token
        "custom_token_lengths": custom_lengths,
        "masked_unmasked_l1": mask_diff,
        "platform": platform_map,
        "limitations": limitations,
        "scope": "교육용 수치 계산: 실제 LLM/RAG/Agent 아님",
    }
    write_json(HERE / "outputs" / "daily_project.json", report)
    raise NotImplementedError("D20-08-B06: TODO를 완성하세요")
    # END D20-08-B06

if __name__=="__main__":
    main()
