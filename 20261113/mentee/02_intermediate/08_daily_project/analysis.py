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

    # TODO D20-08-I01: 공통 지식 A의 문장을 Token·ID로 분석하고 Token 수·Context 제한을 기록하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I01
    raise NotImplementedError("D20-08-I01: TODO를 완성하세요")
    # END D20-08-I01

    # TODO D20-08-I02: 교육용 벡터 A/B/C의 Cosine 표를 만들고 비슷한 방향을 찾아보세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I02
    raise NotImplementedError("D20-08-I02: TODO를 완성하세요")
    # END D20-08-I02

    # TODO D20-08-I03: Q/K/V 3×2 Attention에 Causal Mask를 적용하고 행 합=1·미래 가중치=0을 확인하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I03
    raise NotImplementedError("D20-08-I03: TODO를 완성하세요")
    # END D20-08-I03

    # TODO D20-08-I04: Logit→Softmax→Greedy 다음 Token 선택 흐름을 구현하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I04
    raise NotImplementedError("D20-08-I04: TODO를 완성하세요")
    # END D20-08-I04

    # TODO D20-08-I05: 개인 문장 세 개를 바꾸어 입력 길이·padding과 truncation 상태를 비교하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I05
    raise NotImplementedError("D20-08-I05: TODO를 완성하세요")
    # END D20-08-I05

    # TODO D20-08-I06: Mask 없는 Attention과 Causal Attention의 차이를 정량 비교하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I06
    raise NotImplementedError("D20-08-I06: TODO를 완성하세요")
    # END D20-08-I06
    platform_map={"FastAPI":"요청·응답","PostgreSQL":"원본 저장","LLM":"Token 출력", "RAG":"외부 근거(후속)", "Agent":"도구 제어(후속)"}
    limitations=["교육용 수치 예제는 실제 학습된 LLM과 다르다"]

    # TODO D20-08-I07: PPT의 네 단계와 플랫폼 연결 그림을 Markdown으로 완성하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I07
    raise NotImplementedError("D20-08-I07: TODO를 완성하세요")
    # END D20-08-I07

    # TODO D20-08-I08: Token·Cosine·Attention·Logit 검증 결과를 종합 JSON으로 저장하세요.
    # 입력·대상: 앞 실습의 ToyTokenizer·벡터·Attention·Logit 예시를 함께 사용합니다.
    # 완료 확인: outputs/daily_project.json과 one_page_summary.md의 네 단계가 일치해야 합니다.
    # 주의: 실제 LLM·RAG·Agent를 새로 구현했다고 보고하지 않습니다.
    # BEGIN D20-08-I08
    raise NotImplementedError("D20-08-I08: TODO를 완성하세요")
    # END D20-08-I08

