from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import write_json, write_md

# 강의 PPT 15장: 개념도에 실제 구현한 것과 향후 구현할 것을 구분합니다.
# LLM을 실제 호출하지 않습니다. diagram.md는 그림을 그리는 Mermaid 텍스트입니다.
def main():

    # TODO D20-01-A01: FastAPI·PostgreSQL·LLM·응답의 역할 네 가지를 짧은 문장으로 작성하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A01
    raise NotImplementedError("D20-01-A01: TODO를 완성하세요")
    # END D20-01-A01

    # TODO D20-01-A02: 요청→API→데이터·LLM→응답 연결을 올바른 순서의 화살표로 표현하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A02
    raise NotImplementedError("D20-01-A02: TODO를 완성하세요")
    # END D20-01-A02

    # TODO D20-01-A03: 검색 단계 Retriever와 근거·출처 검증 위치를 연결 목록에 추가하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A03
    raise NotImplementedError("D20-01-A03: TODO를 완성하세요")
    # END D20-01-A03

    # TODO D20-01-A04: 저장과 생성의 책임을 별도 문장으로 기록하고, 오늘 구현 여부를 구분하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A04
    raise NotImplementedError("D20-01-A04: TODO를 완성하세요")
    # END D20-01-A04

    # TODO D20-01-A05: Agent 도구의 조회·수정 권한 차이를 표현하고, 허가 없는 변경을 금지하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A05
    raise NotImplementedError("D20-01-A05: TODO를 완성하세요")
    # END D20-01-A05

    # TODO D20-01-A06: 외부 문서의 명령 문구를 상위 지시처럼 신뢰하면 안 되는 경계를 표시하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A06
    raise NotImplementedError("D20-01-A06: TODO를 완성하세요")
    # END D20-01-A06

    # TODO D20-01-A07: 완성한 연결 관계를 Mermaid 그림과 JSON 요약으로 저장하세요.
    # 입력·대상: FastAPI/DB/LLM의 역할과 실제 구현 범위를 혼동하지 않습니다.
    # 완료 확인: outputs/architecture.md 와 architecture.json을 확인합니다.
    # 주의: 그림의 RAG·Agent는 후속 수업의 개념이며 오늘 동작하지 않습니다.
    # BEGIN D20-01-A07
    raise NotImplementedError("D20-01-A07: TODO를 완성하세요")
    # END D20-01-A07
    print("[01] architecture.md / architecture.json 생성 완료")

if __name__=="__main__":
    main()
