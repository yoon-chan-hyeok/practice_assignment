"""HTTP 경로·입력·응답. 저장 구현은 repository에 위임합니다."""
from fastapi import APIRouter, HTTPException, Response
from app.schemas import Knowledge, KnowledgeWrite
from app.repositories import json_knowledge as repo

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.get("", response_model=list[Knowledge])
def list_knowledge(category: str | None = None):
    return repo.list_entries(category)

@router.get("/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    entry = repo.find_entry(knowledge_id)
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry

@router.post("", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # BEGIN H06-03
    # 해설 H06-03: Router는 HTTP 약속, Repository는 발급·저장 구현을 담당합니다.
    return repo.create(payload.model_dump())
    # END H06-03

@router.put("/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    updated = repo.update(knowledge_id, payload.model_dump())
    if updated is None:
        raise HTTPException(404, "Knowledge not found")
    return updated

@router.delete("/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    deleted = repo.delete(knowledge_id)
    if not deleted:
        raise HTTPException(404, "Knowledge not found")
    return Response(status_code=204)

