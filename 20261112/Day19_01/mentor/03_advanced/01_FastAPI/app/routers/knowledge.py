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
    # BEGIN H-API-07
    # 해설 H-API-07: entry가 None이면 404를 raise하고, 있으면 entry를 반환하세요.
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry
    # END H-API-07
@router.post("", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # BEGIN H-API-08
    # 해설 H-API-08: payload.model_dump()를 repo.create에 전달하고 결과를 반환하세요. 201 선언과 파일
    # 저장은 별개입니다.
    return repo.create(payload.model_dump())
    # END H-API-08
@router.put("/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    # BEGIN H-API-09
    # 해설 H-API-09: repo.update에 ID와 입력 dict를 전달하세요. 결과가 None이면 404, 있으면 변경 결과를
    # 반환하세요.
    entry = repo.update(knowledge_id, payload.model_dump())
    if entry is None:
        raise HTTPException(404, "Knowledge not found")
    return entry
    # END H-API-09
@router.delete("/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    # BEGIN H-API-10
    # 해설 H-API-10: repo.delete가 False이면 404를 raise하고, True이면 본문이 없는 204를 반환하세요.
    if not repo.delete(knowledge_id):
        raise HTTPException(404, "Knowledge not found")
    return Response(status_code=204)
    # END H-API-10
