"""안내문 등록과 파일 저장. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

from pydantic import BaseModel, Field

# 입력 모델은 HTTP Body의 규칙입니다. DB 테이블이나 저장 코드가 아닙니다.
class KnowledgeWrite(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)


class Knowledge(KnowledgeWrite):
    id: int


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
        result = [entry for entry in result if entry["category"] == category]
    # 조건에 맞는 지식이 없으면 정상 조회 200과 빈 배열 []입니다.
    return result

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        same_id = entry["id"] == knowledge_id
        if same_id:
            return entry
    # 입력은 정수이지만 저장된 항목이 없으면 404입니다. foo 같은 Path는 먼저 422입니다.
    raise HTTPException(404, "Knowledge not found")

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # 하나의 잠금으로 현재 데이터 읽기 → ID 발급 → 저장을 함께 보호합니다.
    with LOCK:
        data = read_data()
        # BEGIN A03-01
        # 해설 A03-01: Pydantic 객체를 파일에 쓸 수 있는 dict로 변환합니다. JSON 문자열을 만드는 단계는 아닙니다.
        entry = payload.model_dump()
        # END A03-01
        # BEGIN A03-02
        # 해설 A03-02: ID는 요청 Body가 아니라 서버가 발급합니다.
        entry["id"] = data["next_id"]
        # END A03-02
        # BEGIN A03-03
        # 해설 A03-03: 목록과 발급 번호를 같은 파일에 저장해야 재시작 뒤에도 다음 번호가 유지됩니다.
        data["entries"].append(entry)
        data["next_id"] += 1
        # END A03-03
        # BEGIN A03-04
        # 해설 A03-04: 422는 Route 본문 이전에 발생하므로 이 저장 단계까지 오지 않습니다.
        write_data(data)
        # END A03-04
    # 201을 선언하는 것만으로 저장되지는 않습니다. 실제 저장 성공 뒤 응답합니다.
    return entry
