from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import DATA, ToyTokenizer, context_budget, write_json

# 주의: 여기의 ToyTokenizer는 규칙 기반 학습용이며 실제 BERT 서브워드 출력과 다릅니다.
def run_analysis():
    texts = [item["content"] for item in DATA]
    tok = ToyTokenizer(texts + ["AI", "FastAPI와 PostgreSQL", "print(x) // code"])

    # TODO D20-02-I01: 제공된 지식 A/B/C 세 문장을 학습용 Token·Token ID로 변환하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I01
    raise NotImplementedError("D20-02-I01: TODO를 완성하세요")
    # END D20-02-I01

    # TODO D20-02-I02: 길이가 다른 두 입력을 Padding하고 attention_mask의 0/1을 확인하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I02
    raise NotImplementedError("D20-02-I02: TODO를 완성하세요")
    # END D20-02-I02

    # TODO D20-02-I03: PPT 문맥 예시(300+1200+2000+150, 출력 예약 850)의 합과 남는 예산을 계산하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I03
    raise NotImplementedError("D20-02-I03: TODO를 완성하세요")
    # END D20-02-I03

    # TODO D20-02-I04: max_length=5와 12의 Truncation 여부·실제 길이를 비교하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I04
    raise NotImplementedError("D20-02-I04: TODO를 완성하세요")
    # END D20-02-I04

    # TODO D20-02-I05: 실제 Token 수와 패딩 포함 Tensor 길이를 나누어 기록하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I05
    raise NotImplementedError("D20-02-I05: TODO를 완성하세요")
    # END D20-02-I05
    mixed_rows = []
    small_budget = None
    policy = "예산과 잘림의 차이를 설명"

    # TODO D20-02-I06: Token·Mask·문맥 예산 결과를 outputs/token_report.json에 저장하세요.
    # 입력·대상: 공통 A/B/C 문장을 쓰고 특수 토큰과 PAD를 구분합니다.
    # 완료 확인: outputs/token_report.json 의 tokens·ids·count·mask·budget 값을 확인합니다.
    # 주의: ToyTokenizer는 실제 서브워드 토크나이저가 아니며 임의 모델의 Token 수를 대표하지 않습니다.
    # BEGIN D20-02-I06
    raise NotImplementedError("D20-02-I06: TODO를 완성하세요")
    # END D20-02-I06

