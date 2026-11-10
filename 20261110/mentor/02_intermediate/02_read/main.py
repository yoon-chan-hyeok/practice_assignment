"""JSON 목록·상세 조회. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "수강생"):
    return {"message": f"안녕하세요, {name}"}

@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    with LOCK:
        data = read_data()
    result = data["entries"]
    if category is not None:
        # BEGIN A02-01
        # 해설 A02-01: category를 생략한 None과 category=인 빈 문자열은 다릅니다.
        # 해설 A02-01: 이 필터는 문자열 일치 비교이지 의미 검색이나 RAG가 아닙니다.
        result = [entry for entry in result if entry["category"] == category]
        # END A02-01
    # 조건에 맞는 지식이 없으면 정상 조회 200과 빈 배열 []입니다.
    return result

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    # BEGIN A02-02
    # 해설 A02-02: 찾은 경우만 반환해야 합니다. 첫 항목이 다르다고 바로 404를 보내면 뒤 항목을 찾지 못합니다.
    for entry in data["entries"]:
        same_id = entry["id"] == knowledge_id
        if same_id:
            return entry
    # END A02-02
    # 입력은 정수이지만 저장된 항목이 없으면 404입니다. foo 같은 Path는 먼저 422입니다.
    # BEGIN A02-03
    # 해설 A02-03: HTTPException은 return이 아니라 raise하여 현재 요청을 중단합니다.
    raise HTTPException(404, "Knowledge not found")
    # END A02-03
