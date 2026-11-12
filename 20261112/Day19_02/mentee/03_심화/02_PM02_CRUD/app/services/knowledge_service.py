from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.errors import DataConflictError, KnowledgeNotFoundError
from app.db import transaction
from app.repositories import knowledge as repo
from app.schemas import KnowledgeWrite

def _constraint_name(exc: IntegrityError) -> str | None:
    return getattr(getattr(exc.orig, "diag", None), "constraint_name", None)

def _raise_conflict(exc: IntegrityError) -> None:
    name = _constraint_name(exc)
    safe = {
        "categories_name_key": "Category conflict",
        "categories_name_length": "Category rule conflict",
        "knowledge_title_length": "Title rule conflict",
        "knowledge_content_length": "Content rule conflict",
        "knowledge_category_fk": "Category reference conflict",
    }.get(name, "Database constraint conflict")
    raise DataConflictError(safe) from exc

def list_knowledge(db: Session, category: str | None = None):
    return repo.list_knowledge(db, category)

def get_knowledge(db: Session, knowledge_id: int):
    item = repo.get_knowledge(db, knowledge_id)
    if item is None: raise KnowledgeNotFoundError(knowledge_id)
    return item

def create_knowledge(db: Session, payload: KnowledgeWrite):
    # TODO H09: 분류·지식 추가를 같은 Transaction 경계에서 commit하고 재조회하세요.
    raise NotImplementedError("TODO H09")

def update_knowledge(db: Session, knowledge_id: int, payload: KnowledgeWrite):
    # TODO H10: 존재 확인→분류 연결→세 필드 교체→commit 순서로 수정하세요.
    raise NotImplementedError("TODO H10")

def delete_knowledge(db: Session, knowledge_id: int):
    # TODO H11: 존재 확인 뒤 삭제하고 같은 Service 경계에서 commit하세요.
    raise NotImplementedError("TODO H11")
