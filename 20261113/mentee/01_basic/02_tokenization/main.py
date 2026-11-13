from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import DATA, ToyTokenizer, context_budget, write_json

# 주의: 여기의 ToyTokenizer는 규칙 기반 학습용이며 실제 BERT 서브워드 출력과 다릅니다.
def main():
    texts = [item["content"] for item in DATA]
    tok = ToyTokenizer(texts + ["AI", "FastAPI와 PostgreSQL", "print(x) // code"])

    # TODO D20-02-B01: 제공된 지식 A/B/C 세 문장을 학습용 Token·Token ID로 변환하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-B01
    rows = []
    for item in DATA:
        record = tok.encode("")  # TODO: item의 content 문자열로 바꾸세요.
        rows.append({
            "id": item["id"],
            "text": item["content"],
            "tokens": [],    # TODO: record에서 Token 목록 가져오기
            "ids": [],       # TODO: record에서 input_ids 가져오기
            "count": 0,      # TODO: PAD 제외 유효 Token 개수
            "special_count": 0,  # TODO: 이 ToyTokenizer의 BOS/EOS 개수
        })
    raise NotImplementedError("D20-02-B01: TODO를 완성하세요")
    # END D20-02-B01

    # TODO D20-02-B02: 길이가 다른 두 입력을 Padding하고 attention_mask의 0/1을 확인하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-B02
    batch = tok.batch(["", ""])  # TODO: "AI", "FastAPI와 PostgreSQL" 입력
    # TODO: batch[0]과 batch[1]의 input_ids 길이를 비교하는 assert
    # TODO: attention_mask와 input_ids의 길이를 비교하는 assert
    raise NotImplementedError("D20-02-B02: TODO를 완성하세요")
    # END D20-02-B02

    # TODO D20-02-B03: PPT 문맥 예시(300+1200+2000+150, 출력 예약 850)의 합과 남는 예산을 계산하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-B03
    parts = {"system": 0, "history": 0, "evidence": 0, "user": 0}  # TODO: PPT 수치 입력
    budget = context_budget(5000, parts, 0)  # TODO: 출력 예약 850 Token
    # 힌트: budget["remaining"]은 입력+출력 예약 뒤 남는 Token입니다.
    raise NotImplementedError("D20-02-B03: TODO를 완성하세요")
    # END D20-02-B03
    trunc_cases = {}
    batch_report = []
    mixed_rows = []
    small_budget = None
    policy = "예산과 잘림의 차이를 설명"

    # TODO D20-02-B04: Token·Mask·문맥 예산 결과를 outputs/token_report.json에 저장하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-B04
    result = {
        "tokenizer_kind": "교육용 규칙 기반 (실제 사전학습 모델 아님)",
        "records": [],          # TODO: 위에서 만든 rows
        "batch": [],            # TODO: Padding 결과
        "budget": {},           # TODO: Context Window 예산
        "truncation": trunc_cases,
        "batch_report": batch_report,
        "language_comparison": mixed_rows,
        "overflow_budget": small_budget,
        "policy": policy,
    }
    write_json(HERE / "outputs" / "token_report.json", result)  # 결과를 파일에 저장
    print("[02] Token 분석", [(r["id"], r["count"]) for r in rows])
    raise NotImplementedError("D20-02-B04: TODO를 완성하세요")
    # END D20-02-B04

if __name__=="__main__":
    main()
