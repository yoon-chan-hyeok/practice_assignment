from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models import Category, Knowledge

def list_knowledge(db: Session, category: str | None = None) -> list[Knowledge]:
    stmt = select(Knowledge).options(joinedload(Knowledge.category)).order_by(Knowledge.id)
    if category is not None:
        stmt = stmt.join(Knowledge.category).where(Category.name == category)
    return list(db.scalars(stmt).unique().all())

def get_knowledge(db: Session, knowledge_id: int) -> Knowledge | None:
    return db.scalar(select(Knowledge).options(joinedload(Knowledge.category)).where(Knowledge.id == knowledge_id))

def get_or_create_category(db: Session, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if category is None:
        category = Category(name=name)
        db.add(category)
        db.flush()
    return category

def add_knowledge(db: Session, *, title: str, content: str, category_id: int) -> Knowledge:
    item = Knowledge(title=title, content=content, category_id=category_id)
    db.add(item)
    return item

def delete_knowledge(db: Session, item: Knowledge) -> None:
    db.delete(item)
