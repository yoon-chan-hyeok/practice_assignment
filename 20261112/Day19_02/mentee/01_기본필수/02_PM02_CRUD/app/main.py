from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, joinedload
from app.db import get_db, transaction
from app.models import Category, Knowledge
from app.schemas import KnowledgeRead, KnowledgeWrite

app = FastAPI(title="Knowledge API · PostgreSQL")

def to_read(item: Knowledge) -> KnowledgeRead:
    return KnowledgeRead(id=item.id, title=item.title, content=item.content, category=item.category.name)

def load_one(db: Session, knowledge_id: int) -> Knowledge | None:
    return db.scalar(select(Knowledge).options(joinedload(Knowledge.category)).where(Knowledge.id == knowledge_id))

def get_or_create_category(db: Session, name: str) -> Category:
    # TODO B04: 분류명을 조회하고 없으면 Category를 add→flush하여 같은 Transaction에서 id를 확보하세요.
    raise NotImplementedError("TODO B04")

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
    # TODO B05: PK로 조회하고 없으면 404, 있으면 KnowledgeRead 형식으로 반환하세요.
    raise NotImplementedError("TODO B05")

@app.post("/api/knowledge", response_model=KnowledgeRead, status_code=status.HTTP_201_CREATED)
def create_knowledge(payload: KnowledgeWrite, db: Session = Depends(get_db)):
    # TODO B06: 분류를 연결하고 Knowledge를 저장한 뒤 commit하고 생성된 id를 포함해 반환하세요.
    raise NotImplementedError("TODO B06")

@app.put("/api/knowledge/{knowledge_id}", response_model=KnowledgeRead)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite, db: Session = Depends(get_db)):
    item = load_one(db, knowledge_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    category = get_or_create_category(db, payload.category)
    # TODO B07: 기존 id는 유지하고 title·content·category를 교체한 뒤 commit하세요.
    raise NotImplementedError("TODO B07")

@app.delete("/api/knowledge/{knowledge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_knowledge(knowledge_id: int, db: Session = Depends(get_db)) -> Response:
    item = load_one(db, knowledge_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    # TODO B08: 대상 행을 삭제하고 commit한 뒤 Body 없는 204를 반환하세요.
    raise NotImplementedError("TODO B08")
