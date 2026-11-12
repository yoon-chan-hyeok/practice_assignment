from functools import lru_cache
from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings import get_settings

@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    if settings.db_password == "CHANGE_ME":
        raise RuntimeError(".env의 DB_PASSWORD를 실제 학습용 비밀번호로 바꾸세요.")
    return create_engine(settings.database_url, pool_pre_ping=True)

@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    factory = get_session_factory()
    with factory() as session:
        yield session


@contextmanager
def transaction(db: Session):
    # TODO B09: commit까지 성공하면 확정하고, flush/commit 중 예외가 나면 rollback 후 다시 raise하세요.
    raise NotImplementedError("TODO B09")
    yield  # generator 형태 유지용; 정답에서는 제거됩니다.

def check_database() -> tuple[str, str]:
    with get_engine().connect() as conn:
        row = conn.execute(text("SELECT current_database(), current_user")).one()
        return str(row[0]), str(row[1])
