from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload
from app.db import get_db, transaction
from app.models import Category, Knowledge
from app.schemas import KnowledgeRead, KnowledgeWrite

# 강사 해설: Day17의 URL·Method·입력·응답 계약을 유지하고 저장소만 PostgreSQL로 교체합니다.
app = FastAPI(title="Knowledge API · PostgreSQL")

def to_read(item: Knowledge) -> KnowledgeRead:
    return KnowledgeRead(id=item.id, title=item.title, content=item.content, category=item.category.name)

def load_one(db: Session, knowledge_id: int) -> Knowledge | None:
    return db.scalar(select(Knowledge).options(joinedload(Knowledge.category)).where(Knowledge.id == knowledge_id))

def get_or_create_category(db: Session, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if category is None:
        category = Category(name=name)
        db.add(category)
        db.flush()  # 같은 Transaction 안에서 category.id를 확보합니다.
    return category

def raise_conflict(exc: IntegrityError) -> None:
    # HTTP 변환은 transaction 바깥에서 수행합니다. transaction은 먼저 rollback하고 예외를 다시 전달합니다.
    raise HTTPException(status_code=409, detail="Database constraint conflict") from exc

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except OperationalError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

@app.get("/api/knowledge", response_model=list[KnowledgeRead])
def list_knowledge(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(Knowledge).options(joinedload(Knowledge.category)).order_by(Knowledge.id)
    if category is not None:
        stmt = stmt.join(Knowledge.category).where(Category.name == category)
    return [to_read(x) for x in db.scalars(stmt).unique().all()]

@app.get("/api/knowledge/{knowledge_id}", response_model=KnowledgeRead)
def read_knowledge(knowledge_id: int, db: Session = Depends(get_db)):
    item = load_one(db, knowledge_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return to_read(item)

@app.post("/api/knowledge", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(payload: KnowledgeWrite, db: Session = Depends(get_db)):
    try:
        with transaction(db):
            category = get_or_create_category(db, payload.category)
            item = Knowledge(title=payload.title, content=payload.content, category_id=category.id, category=category)
            db.add(item)
            db.flush()  # DB가 발급한 id를 commit 전에 확인합니다.
            result = to_read(item)
        return result
    except IntegrityError as exc:
        raise_conflict(exc)

@app.put("/api/knowledge/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite, db: Session = Depends(get_db)):
    item = load_one(db, knowledge_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    try:
        with transaction(db):
            category = get_or_create_category(db, payload.category)
            item.title, item.content, item.category_id = payload.title, payload.content, category.id
            item.category = category
            db.flush()
            result = to_read(item)
        return result
    except IntegrityError as exc:
        raise_conflict(exc)

@app.delete("/api/knowledge/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)) -> Response:
    item = load_one(db, knowledge_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    try:
        with transaction(db):
            db.delete(item)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError as exc:
        raise_conflict(exc)
