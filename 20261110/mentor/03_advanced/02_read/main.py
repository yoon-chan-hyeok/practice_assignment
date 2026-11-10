"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response
import logic as repo

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
    # BEGIN H02-03
    # 해설 H02-03: 저장 함수와 HTTP 상태 정책이 서로 다른 책임입니다.
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    # END H02-03
    return entry
