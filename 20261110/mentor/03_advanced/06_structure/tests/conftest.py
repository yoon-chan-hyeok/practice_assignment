"""제공 fixture: 각 테스트마다 새로운 임시 저장소를 사용합니다."""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories import json_knowledge as store

SEED = {'next_id': 4, 'entries': [{'id': 1, 'title': '가상환경', 'category': 'setup', 'content': '프로젝트별 패키지를 분리한다.'}, {'id': 2, 'title': '서버 실행', 'category': 'api', 'content': 'uvicorn으로 개발 서버를 켠다.'}, {'id': 3, 'title': '입력 오류', 'category': 'api', 'content': '422이면 입력값을 확인한다.'}]}

@pytest.fixture
def isolated_client(tmp_path, monkeypatch):
    # 실제 data/knowledge.json을 읽거나 바꾸지 않습니다. 독립적인 고정 입력을 만듭니다.
    test_file = tmp_path / "knowledge.json"
    test_file.write_text(json.dumps(SEED, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(store, "DATA", test_file)
    with TestClient(app) as client:
        yield client, test_file
