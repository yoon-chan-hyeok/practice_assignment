from functools import lru_cache
from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings import get_settings

@lru_cache
def get_engine() -> Engine:
    # TODO H02: 설정 검증과 pool_pre_ping을 포함한 Engine Factory를 완성하세요.
    raise NotImplementedError("TODO H02")

@lru_cache
def get_session_factory():
    # TODO H03: Engine에 바인딩된 sessionmaker를 반환하세요.
    raise NotImplementedError("TODO H03")

def get_db() -> Generator[Session, None, None]:
    # TODO H04: 요청 단위 Session Dependency를 완성하세요.
    raise NotImplementedError("TODO H04")


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
