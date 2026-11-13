from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LEVEL_ROOT = HERE.parent
sys.path.insert(0, str(LEVEL_ROOT))  # 어느 작업 폴더에서 실행해도 common 패키지를 찾습니다.
from common.support import write_json, write_md

# 세 예시는 수업용으로 사람이 미리 설계한 사례입니다. 실제 자동 사실성 검사기가 아닙니다.
CASES = [
    {"id":"F01","question":"파일을 어디에 보관하나요?",
     "source":"실습 파일은 개인 폴더에 보관합니다.",
     "answer":"실습 파일은 공용 서버 폴더에 보관합니다.","sources":["K01"]},
    {"id":"F02","question":"서버는 어디에서 실행하나요?",
     "source":"프로젝트 폴더에서 서버를 실행합니다.",
     "answer":"프로젝트 폴더에서 서버를 실행합니다."},
    {"id":"F03","question":"질문할 때 무엇을 함께 적나요?",
     "source":"오류 메시지와 시도한 작업을 함께 적습니다.",
     "answer":"오류 메시지와 시도한 작업을 함께 적습니다.","sources":[]},
]

def main():

    # BEGIN D20-07-B01
    # 해설: 형식 누락→근거 누락→출처와 내용 불일치 순으로 교육용 규칙을 적용합니다.
    issues=[]
    for case in CASES:
        if "sources" not in case:
            kind="format"
        elif not case["sources"]:
            kind="evidence"
        elif case["answer"] != case["source"]:
            kind="factual_mismatch"
        else:
            kind="ok"
        issues.append({"id":case["id"],"kind":kind})
    # 해설: 문자열 동일성은 실제 복잡한 주장 검증을 대신하지 않습니다.
    # END D20-07-B01

    # BEGIN D20-07-B02
    explanations={
        "format":"JSON/응답에 필수 필드가 존재하는지 보는 구조 검증",
        "evidence":"인용·출처 정보가 있는지와 적절한 근거인지 구분",
        "factual_mismatch":"주장과 승인된 정답/원본이 모순되는지 사람·검증 규칙으로 확인",
    }
    # END D20-07-B02
    mitigation={}
    additional_checks=[]
    agent_case={}
    trust_rules=[]

    # BEGIN D20-07-B03
    report={"classification":issues,"definitions":explanations,"mitigation":mitigation,
            "checks":additional_checks,"agent_case":agent_case,"trust_rules":trust_rules,
            "disclaimer":"예상 문제 유형을 분류한 수업용 규칙이며 실제 LLM 사실성 자동 판정이 아님"}
    write_json(HERE/"outputs"/"review.json",report)
    lines=["# LLM 답변 실패·검증 결과", "", "이 결과는 사전 정의된 수업용 예시를 사용했습니다.", ""]
    lines += [f"- {row['id']}: {row['kind']}" for row in issues]
    lines += ["", "## 플랫폼 연결", "FastAPI: 입력·출력 계약 / PostgreSQL: 원본 / RAG: 검색 근거 / Agent: 도구 권한(후속)"]
    write_md(HERE/"outputs"/"review.md","\n".join(lines)+"\n")
    print("[07]",[(r["id"],r["kind"]) for r in issues])
    # END D20-07-B03

if __name__=="__main__":
    main()
