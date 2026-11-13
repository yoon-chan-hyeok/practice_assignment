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

    # TODO D20-07-B01: 3개 답변에서 정해 둔 형태·근거·사실 불일치를 분류하세요.
    # 입력·대상: 제공된 F01/F02/F03 사례만 대상으로 분류합니다.
    # 완료 확인: outputs/review.json, review.md에서 사실 불일치/형식 누락/근거 누락을 확인합니다.
    # 주의: 사전 설계된 규칙 기반 점검이며 실제 생성형 AI의 진위 판정기가 아닙니다.
    # BEGIN D20-07-B01
    issues = []
    for case in CASES:
        if "sources" not in case:
            kind = ""  # TODO: 필수 필드 자체가 없으면 "format"
        elif not case["sources"]:
            kind = ""  # TODO: 출처 목록이 비어 있으면 "evidence"
        elif case["answer"] != case["source"]:
            kind = ""  # TODO: 제공 원본과 내용이 다르면 "factual_mismatch"
        else:
            kind = "ok"
        issues.append({"id": case["id"], "kind": kind})
    raise NotImplementedError("D20-07-B01: TODO를 완성하세요")
    # END D20-07-B01

    # TODO D20-07-B02: 사실성·형식·근거 검증을 서로 다른 검사라고 설명하세요.
    # 입력·대상: 제공된 F01/F02/F03 사례만 대상으로 분류합니다.
    # 완료 확인: outputs/review.json, review.md에서 사실 불일치/형식 누락/근거 누락을 확인합니다.
    # 주의: 사전 설계된 규칙 기반 점검이며 실제 생성형 AI의 진위 판정기가 아닙니다.
    # BEGIN D20-07-B02
    explanations = {
        "format": "",           # TODO: JSON에 필수 필드가 있는지
        "evidence": "",         # TODO: 출처의 존재·적절성
        "factual_mismatch": "", # TODO: 확인된 원본과 주장의 불일치
    }
    raise NotImplementedError("D20-07-B02: TODO를 완성하세요")
    # END D20-07-B02
    mitigation={}
    additional_checks=[]
    agent_case={}
    trust_rules=[]

    # TODO D20-07-B03: 검증 결과와 향후 후속 수업 연결을 review.json 및 review.md로 저장하세요.
    # 입력·대상: 제공된 F01/F02/F03 사례만 대상으로 분류합니다.
    # 완료 확인: outputs/review.json, review.md에서 사실 불일치/형식 누락/근거 누락을 확인합니다.
    # 주의: 사전 설계된 규칙 기반 점검이며 실제 생성형 AI의 진위 판정기가 아닙니다.
    # BEGIN D20-07-B03
    report = {
        "classification": issues,
        "definitions": explanations,
        "mitigation": mitigation,
        "checks": additional_checks,
        "agent_case": agent_case,
        "trust_rules": trust_rules,
        "disclaimer": "교육용 규칙이며 실제 LLM 사실성 자동 판정 아님",
    }
    write_json(HERE / "outputs" / "review.json", report)
    lines = ["# LLM 답변 검증 결과", "", "교육용 사례의 분류 결과", ""]
    lines += []  # TODO: issues를 순회하여 F01~F03의 kind를 한 줄씩 기록
    lines += ["", "## 플랫폼 연결", ""]  # TODO: FastAPI·DB·RAG·Agent의 역할 기록
    write_md(HERE / "outputs" / "review.md", "\n".join(lines) + "\n")
    raise NotImplementedError("D20-07-B03: TODO를 완성하세요")
    # END D20-07-B03

if __name__=="__main__":
    main()
