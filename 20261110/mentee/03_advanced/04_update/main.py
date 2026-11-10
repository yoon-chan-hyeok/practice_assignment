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
    # TODO H04-03: 데이터 함수가 None을 반환하면 Router에서 404를 보내세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H04-03를 먼저 완성하세요.")
    # END H04-03
    return updated
