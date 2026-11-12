from functools import lru_cache
from contextlib import contextmanager
from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings import get_settings

# 강사 해설: Engine은 애플리케이션 수준에서 재사용하고, Session은 요청/작업 단위로 생성합니다.
@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    if settings.db_password == "CHANGE_ME":
        raise RuntimeError(".env의 DB_PASSWORD를 실제 학습용 비밀번호로 바꾸세요.")
    return create_engine(settings.database_url, pool_pre_ping=True)

@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)

# 강사 해설: yield dependency로 요청 종료 시 Session.close까지 보장합니다.
def get_db() -> Generator[Session, None, None]:
    factory = get_session_factory()
    with factory() as session:
        yield session


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
