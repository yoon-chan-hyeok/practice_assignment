"""같은 Session에서 DB 제약 실패 뒤 rollback이 필요한 이유를 확인합니다."""
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.db import get_session_factory
from app.models import Category, Knowledge

name = "__pm_atomicity_probe__"
with get_session_factory()() as db:
    try:
        cat = Category(name=name)
        db.add(cat); db.flush()
        db.add(Knowledge(title="probe", content="", category_id=cat.id))  # DB CHECK 실패 유도
        db.commit()
    except IntegrityError:
        print("expected IntegrityError")
        db.rollback()
    remained = db.scalar(select(Category).where(Category.name == name))
    print("category remained after rollback:", remained is not None)
