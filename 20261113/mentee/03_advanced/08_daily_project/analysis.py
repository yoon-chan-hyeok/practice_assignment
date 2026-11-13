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
def run_analysis():
    texts=[d["content"] for d in DATA]
    tokenizer=ToyTokenizer(texts)

    # TODO D20-08-A01: 공통 지식 A의 문장을 Token·ID로 분석하고 Token 수·Context 제한을 기록하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A01
    raise NotImplementedError("D20-08-A01: TODO를 완성하세요")
    # END D20-08-A01

    # TODO D20-08-A02: 교육용 벡터 A/B/C의 Cosine 표를 만들고 비슷한 방향을 찾아보세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A02
    raise NotImplementedError("D20-08-A02: TODO를 완성하세요")
    # END D20-08-A02

    # TODO D20-08-A03: Q/K/V 3×2 Attention에 Causal Mask를 적용하고 행 합=1·미래 가중치=0을 확인하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A03
    raise NotImplementedError("D20-08-A03: TODO를 완성하세요")
    # END D20-08-A03

    # TODO D20-08-A04: Logit→Softmax→Greedy 다음 Token 선택 흐름을 구현하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A04
    raise NotImplementedError("D20-08-A04: TODO를 완성하세요")
    # END D20-08-A04

    # TODO D20-08-A05: 개인 문장 세 개를 바꾸어 입력 길이·padding과 truncation 상태를 비교하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A05
    raise NotImplementedError("D20-08-A05: TODO를 완성하세요")
    # END D20-08-A05

    # TODO D20-08-A06: Mask 없는 Attention과 Causal Attention의 차이를 정량 비교하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A06
    raise NotImplementedError("D20-08-A06: TODO를 완성하세요")
    # END D20-08-A06

    # TODO D20-08-A07: 데이터·모델·검색 책임을 FastAPI/DB/LLM/RAG/Agent로 명확히 매핑하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A07
    raise NotImplementedError("D20-08-A07: TODO를 완성하세요")
    # END D20-08-A07

    # TODO D20-08-A08: 임의 2D 좌표와 Attention Weight가 의미 이해를 증명하지 못한다는 한계 설명을 추가하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A08
    raise NotImplementedError("D20-08-A08: TODO를 완성하세요")
    # END D20-08-A08

    # TODO D20-08-A09: PPT의 네 단계와 플랫폼 연결 그림을 Markdown으로 완성하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A09
    raise NotImplementedError("D20-08-A09: TODO를 완성하세요")
    # END D20-08-A09

    # TODO D20-08-A10: Token·Cosine·Attention·Logit 검증 결과를 종합 JSON으로 저장하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-A10
    raise NotImplementedError("D20-08-A10: TODO를 완성하세요")
    # END D20-08-A10

