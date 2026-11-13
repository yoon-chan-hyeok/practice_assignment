from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import write_json, write_md

# 강의 PPT 15장: 개념도에 실제 구현한 것과 향후 구현할 것을 구분합니다.
# LLM을 실제 호출하지 않습니다. diagram.md는 그림을 그리는 Mermaid 텍스트입니다.
def main():

    # BEGIN D20-01-A01
    roles = {
        "FastAPI": "HTTP 요청을 검증하고 함수·응답을 연결한다",
        "PostgreSQL": "원본 지식·분류를 관계형 테이블에 저장한다",
        "LLM": "문맥과 입력을 바탕으로 다음 Token을 생성한다",
        "Response": "호출한 Client에 JSON 결과를 전달한다",
    }
    # 해설: DB는 다음 토큰을 계산하지 않고, LLM은 영구 DB를 대신하지 않습니다.
    # END D20-01-A01

    # BEGIN D20-01-A02
    edges = [
        ("Client", "FastAPI", "HTTP 요청"),
        ("FastAPI", "PostgreSQL", "원본 지식 조회·수정"),
        ("PostgreSQL", "FastAPI", "원본 데이터"),
        ("FastAPI", "LLM", "입력·문맥(후속 구현)"),
        ("LLM", "Response", "생성 결과(후속 구현)"),
        ("Response", "Client", "JSON"),
    ]
    # 해설: 이 선들은 역할의 개념 관계이며 오늘 구현하는 실제 파이프라인은 아닙니다.
    # END D20-01-A02

    # BEGIN D20-01-A03
    edges.extend([
        ("FastAPI", "Retriever", "질문·검색 조건(후속 구현)"),
        ("Retriever", "PostgreSQL", "원본·메타데이터 참조 가능"),
        ("Retriever", "LLM", "검색된 근거(후속 구현)"),
        ("LLM", "EvidenceCheck", "답변·출처 검증(후속 구현)"),
    ])
    roles["Retriever"] = "관련 근거를 찾는 검색 계층(11/20 후속 구현)"
    roles["EvidenceCheck"] = "답변의 근거·출처 일치 여부를 확인한다"
    # END D20-01-A03

    # BEGIN D20-01-A04
    responsibility = {
        "storage": "PostgreSQL은 지식 저장·관계를 책임진다",
        "generation": "LLM은 다음 Token의 분포와 출력을 책임진다",
        "implemented_today": ["역할 개념도 작성"],
        "not_implemented": ["새 RAG 검색", "새 Agent 실행", "실제 LLM API 호출"],
    }
    # END D20-01-A04

    # BEGIN D20-01-A05
    roles["ToolPermission"] = "조회/변경 권한을 실행 전에 애플리케이션이 확인한다"
    edges.append(("Agent", "ToolPermission", "도구 실행 전 승인 확인(후속 구현)"))
    edges.append(("ToolPermission", "FastAPI", "허가된 범위의 요청만 전달"))
    # END D20-01-A05

    # BEGIN D20-01-A06
    trust_boundary = {
        "untrusted": ["외부 문서 본문", "검색된 근거의 지시문"],
        "rule": "외부 텍스트는 데이터로 취급하며 시스템 권한을 부여하지 않는다",
        "scope": "설계 설명만; Agent·보안 시스템은 실제 구현하지 않음",
    }
    # END D20-01-A06

    # BEGIN D20-01-A07
    # 해설: Mermaid는 파일을 열어 그릴 수 있는 표기법이며 네트워크·API 호출이 아닙니다.
    node_names = sorted({n for a,b,_ in edges for n in (a,b)})
    node_id = {name:f"N{i}" for i,name in enumerate(node_names)}
    lines = ["flowchart LR"]
    lines += [f'  {node_id[name]}["{name}"]' for name in node_names]
    lines += [f'  {node_id[a]} -->|"{label}"| {node_id[b]}' for a,b,label in edges]
    write_md(HERE/"outputs"/"architecture.md", "# AI 지식 플랫폼 개념도\n\n```mermaid\n"+"\n".join(lines)+"\n```\n")
    write_json(HERE/"outputs"/"architecture.json", {
        "roles":roles,"edges":[list(x) for x in edges],
        "responsibility":responsibility,"trust_boundary":trust_boundary,
    })
    # END D20-01-A07
    print("[01] architecture.md / architecture.json 생성 완료")

if __name__=="__main__":
    main()
