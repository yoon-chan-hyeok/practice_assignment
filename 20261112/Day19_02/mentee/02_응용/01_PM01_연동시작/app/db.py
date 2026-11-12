from functools import lru_cache
from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings import get_settings

@lru_cache
def get_engine() -> Engine:
    # TODO A02: settings를 읽고 CHANGE_ME를 거부한 뒤 pool_pre_ping을 켠 Engine을 반환하세요.
    raise NotImplementedError("TODO A02")

@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    # TODO A03: 요청 단위 Session Dependency를 완성하세요.
    raise NotImplementedError("TODO A03")


@contextmanager
def transaction(db: Session):
    """한 쓰기 요청의 flush와 commit을 같은 경계로 묶습니다."""
    try:
        yield
        db.commit()
    except Exception:
        db.rollback()
        raise

def check_database() -> tuple[str, str]:
    with get_engine().connect() as conn:
        row = conn.execute(text("SELECT current_database(), current_user")).one()
        return str(row[0]), str(row[1])
