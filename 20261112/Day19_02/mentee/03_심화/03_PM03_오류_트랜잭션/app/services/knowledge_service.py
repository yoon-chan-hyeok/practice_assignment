from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.errors import DataConflictError, KnowledgeNotFoundError
from app.db import transaction
from app.repositories import knowledge as repo
from app.schemas import KnowledgeWrite

def _constraint_name(exc: IntegrityError) -> str | None:
    return getattr(getattr(exc.orig, "diag", None), "constraint_name", None)

def _raise_conflict(exc: IntegrityError) -> None:
    # TODO H13: rollback은 transaction이 수행했습니다. constraint_name을 안전한 DataConflictError로 매핑하세요.
    raise NotImplementedError("TODO H13")

def list_knowledge(db: Session, category: str | None = None):
    return repo.list_knowledge(db, category)

def get_knowledge(db: Session, knowledge_id: int):
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise KnowledgeNotFoundError(knowledge_id)
    return item

def create_knowledge(db: Session, payload: KnowledgeWrite):
    try:
        with transaction(db):
            category = repo.get_or_create_category(db, payload.category)
            item = repo.add_knowledge(db, title=payload.title, content=payload.content, category_id=category.id)
            item.category = category
            db.flush()
            item_id = item.id
        return repo.get_knowledge(db, item_id)
    except IntegrityError as exc:
        _raise_conflict(exc)

def update_knowledge(db: Session, knowledge_id: int, payload: KnowledgeWrite):
    item = get_knowledge(db, knowledge_id)
    try:
        with transaction(db):
            category = repo.get_or_create_category(db, payload.category)
            item.title, item.content, item.category_id = payload.title, payload.content, category.id
            item.category = category
            db.flush()
        return repo.get_knowledge(db, knowledge_id)
    except IntegrityError as exc:
        _raise_conflict(exc)

def delete_knowledge(db: Session, knowledge_id: int):
    item = get_knowledge(db, knowledge_id)
    try:
        with transaction(db):
            repo.delete_knowledge(db, item)
    except IntegrityError as exc:
        _raise_conflict(exc)
