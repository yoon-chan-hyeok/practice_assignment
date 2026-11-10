"""제공 fixture: 각 테스트마다 새로운 임시 저장소를 사용합니다."""
import json
import pytest
from fastapi.testclient import TestClient
from main import app

SEED = {'next_id': 4, 'entries': [{'id': 1, 'title': '가상환경', 'category': 'setup', 'content': '프로젝트별 패키지를 분리한다.'}, {'id': 2, 'title': '서버 실행', 'category': 'api', 'content': 'uvicorn으로 개발 서버를 켠다.'}, {'id': 3, 'title': '입력 오류', 'category': 'api', 'content': '422이면 입력값을 확인한다.'}]}

@pytest.fixture
def isolated_client():
    with TestClient(app) as client:
        yield client, None
