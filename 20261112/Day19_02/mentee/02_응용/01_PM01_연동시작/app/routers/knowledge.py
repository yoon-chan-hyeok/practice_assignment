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
    try:
        with transaction(db):
            category = repo.get_or_create_category(db, payload.category)
            item = repo.add_knowledge(db, title=payload.title, content=payload.content, category_id=category.id)
            item.category = category
            db.flush()
            item_id = item.id
        return to_read(repo.get_knowledge(db, item_id))
    except IntegrityError as exc:
        raise_409(exc)

@router.put("/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite, db: Session = Depends(get_db)):
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise HTTPException(404, "Knowledge not found")
    category = repo.get_or_create_category(db, payload.category)
    try:
        with transaction(db):
            item.title, item.content, item.category_id = payload.title, payload.content, category.id
            item.category = category
            db.flush()
        return to_read(repo.get_knowledge(db, knowledge_id))
    except IntegrityError as exc:
        raise_409(exc)

@router.delete("/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)) -> Response:
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise HTTPException(404, "Knowledge not found")
    try:
        with transaction(db):
            repo.delete_knowledge(db, item)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError as exc:
        raise_409(exc)
