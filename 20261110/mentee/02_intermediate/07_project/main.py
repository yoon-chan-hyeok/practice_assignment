"""함께 통합하고 프로젝트 준비. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data
from queries import select_category, find_entry

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
    # BEGIN A07-01
    # TODO A07-01: 읽은 entries와 category를 select_category에 넘겨 결과를 응답하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("A07-01를 먼저 완성하세요.")
    # END A07-01

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    entry = find_entry(data["entries"], knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # 하나의 잠금으로 현재 데이터 읽기 → ID 발급 → 저장을 함께 보호합니다.
    with LOCK:
        data = read_data()
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        # BEGIN A07-02
        # TODO A07-02: 생성할 entry를 한 번 추가하고 next_id를 한 번 증가시키세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        raise NotImplementedError("A07-02를 먼저 완성하세요.")
        # END A07-02
        write_data(data)
    # 201을 선언하는 것만으로 저장되지는 않습니다. 실제 저장 성공 뒤 응답합니다.
    return entry

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            same_id = entry["id"] == knowledge_id
            if same_id:
                updated = payload.model_dump()
                updated["id"] = knowledge_id
                # BEGIN A07-03
                # TODO A07-03: 수정 대상 위치를 updated로 교체하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("A07-03를 먼저 완성하세요.")
                # END A07-03
                write_data(data)
                return updated
    # 없는 ID를 새로 생성하지 않습니다. PUT에서도 세 입력 필드가 모두 필수입니다.
    raise HTTPException(404, "Knowledge not found")

@app.delete("/api/knowledge/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                data["entries"].pop(i)
                write_data(data)
                # BEGIN A07-04
                # TODO A07-04: 삭제 성공에서 빈 204 응답을 반환하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("A07-04를 먼저 완성하세요.")
                # END A07-04
    raise HTTPException(404, "Knowledge not found")
