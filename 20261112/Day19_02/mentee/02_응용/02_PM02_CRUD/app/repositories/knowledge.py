from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models import Category, Knowledge

def list_knowledge(db: Session, category: str | None = None) -> list[Knowledge]:
    stmt = select(Knowledge).options(joinedload(Knowledge.category)).order_by(Knowledge.id)
    if category is not None:
        stmt = stmt.join(Knowledge.category).where(Category.name == category)
    return list(db.scalars(stmt).unique().all())

def get_knowledge(db: Session, knowledge_id: int) -> Knowledge | None:
    # TODO A05: PK와 joinedload를 사용해 지식 한 건을 조회하세요.
    raise NotImplementedError("TODO A05")

def get_or_create_category(db: Session, name: str) -> Category:
    # TODO A06: 분류명을 찾고 없으면 같은 Session에서 add→flush하세요.
    raise NotImplementedError("TODO A06")

def add_knowledge(db: Session, *, title: str, content: str, category_id: int) -> Knowledge:
    # TODO A07: Knowledge ORM 객체를 만들고 Session에 등록해 반환하세요.
    raise NotImplementedError("TODO A07")

def delete_knowledge(db: Session, item: Knowledge) -> None:
    db.delete(item)
