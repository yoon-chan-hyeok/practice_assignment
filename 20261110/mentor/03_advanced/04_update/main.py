"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response
import logic as repo
from schemas import Knowledge, KnowledgeWrite

app = FastAPI(title="Knowledge API")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    return repo.create(payload.model_dump())

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    updated = repo.update(knowledge_id, payload.model_dump())
    # BEGIN H04-03
    # 해설 H04-03: Repository는 HTTP를 모르고 Router가 오류 상태로 변환합니다.
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    # END H04-03
    return updated
