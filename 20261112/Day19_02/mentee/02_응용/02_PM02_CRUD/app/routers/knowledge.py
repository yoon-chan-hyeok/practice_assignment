from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db, transaction
from app.schemas import KnowledgeRead, KnowledgeWrite
from app.repositories import knowledge as repo

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

def to_read(item) -> KnowledgeRead:
    return KnowledgeRead(id=item.id, title=item.title, content=item.content, category=item.category.name)

def raise_409(exc: IntegrityError) -> None:
    raise HTTPException(409, "Database constraint conflict") from exc

@router.get("", response_model=list[KnowledgeRead])
def list_knowledge(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    return [to_read(x) for x in repo.list_knowledge(db, category)]

@router.get("/{knowledge_id}", response_model=KnowledgeRead)
def read_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise HTTPException(404, "Knowledge not found")
    return to_read(item)

@router.post("", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(payload: KnowledgeWrite, db: Session = Depends(get_db)):
    # TODO A08: Repository를 조합해 분류 연결→지식 추가→commit→재조회 순서로 POST를 완성하세요.
    raise NotImplementedError("TODO A08")

@router.put("/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite, db: Session = Depends(get_db)):
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise HTTPException(404, "Knowledge not found")
    category = repo.get_or_create_category(db, payload.category)
    # TODO A09: 기존 id를 유지한 PUT 전체 수정을 완성하세요.
    raise NotImplementedError("TODO A09")

@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)) -> Response:
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise HTTPException(404, "Knowledge not found")
    # TODO A10: Repository 삭제→commit→빈 204 응답을 완성하세요.
    raise NotImplementedError("TODO A10")
