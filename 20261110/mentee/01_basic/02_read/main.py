"""JSON 목록·상세 조회. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

@app.get("/api/knowledge")
def list_knowledge():
    with LOCK:
        data = read_data()
    # 파일 전체에는 내부용 next_id도 있으므로 entries만 응답합니다.
    # BEGIN B02-01
    # TODO B02-01: 파일 전체 data에서 entries 목록만 반환하세요. next_id가 포함된 dict 전체를 반환하지 마세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("B02-01를 먼저 완성하세요.")
    # END B02-01

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        # BEGIN B02-02
        # TODO B02-02: 현재 entry의 id와 요청 knowledge_id가 같은지 비교하여 same_id에 저장하세요.
        # 힌트: 비교 결과는 True 또는 False입니다.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        raise NotImplementedError("B02-02를 먼저 완성하세요.")
        # END B02-02
        if same_id:
            return entry
    # 입력은 정수이지만 저장된 항목이 없으면 404입니다. foo 같은 Path는 먼저 422입니다.
    raise HTTPException(404, "Knowledge not found")
