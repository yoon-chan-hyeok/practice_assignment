import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db import get_db
from app.main import app

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    pytest.skip("TEST_DATABASE_URL이 없어서 PostgreSQL 통합 테스트를 건너뜁니다.", allow_module_level=True)

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def override_get_db():
    # 강사 해설: 개발 DB가 아니라 Test DB Session을 요청에 주입합니다.
    with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_row_and_delete():
    response = client.post("/api/knowledge", json={"title":"__test_create__","content":"통합 검증","category":"learning"})
    assert response.status_code == 201
    created = response.json()
    with TestSessionLocal() as db:
        row = db.execute(text("SELECT title FROM knowledge WHERE id=:id"), {"id":created["id"]}).one()
        assert row[0] == "__test_create__"
    deleted = client.delete(f"/api/knowledge/{created['id']}")
    assert deleted.status_code == 204
    with TestSessionLocal() as db:
        remaining = db.execute(text("SELECT COUNT(*) FROM knowledge WHERE id=:id"), {"id":created["id"]}).scalar_one()
        assert remaining == 0
