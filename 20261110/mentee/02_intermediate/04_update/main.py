"""같은 지식의 본문 수정. 실행: python -m uvicorn main:app --reload"""
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
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
    # 201을 선언하는 것만으로 저장되지는 않습니다. 실제 저장 성공 뒤 응답합니다.
    return entry

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            # BEGIN A04-01
            # TODO A04-01: 현재 항목이 수정 대상인지 비교 결과를 same_id에 넣으세요.
            # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
            raise NotImplementedError("A04-01를 먼저 완성하세요.")
            # END A04-01
            if same_id:
                # BEGIN A04-02
                # TODO A04-02: 새 입력을 dict로 만들고 기존 knowledge_id를 유지하여 updated를 구성하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("A04-02를 먼저 완성하세요.")
                # END A04-02
                # BEGIN A04-03
                # TODO A04-03: 대상 위치 i를 updated로 교체하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("A04-03를 먼저 완성하세요.")
                # END A04-03
                # BEGIN A04-04
                # TODO A04-04: 변경 내용을 저장하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("A04-04를 먼저 완성하세요.")
                # END A04-04
                return updated
    # 없는 ID를 새로 생성하지 않습니다. PUT에서도 세 입력 필드가 모두 필수입니다.
    raise HTTPException(404, "Knowledge not found")
