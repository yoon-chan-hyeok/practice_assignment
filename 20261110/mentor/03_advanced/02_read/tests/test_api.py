import json
import pytest

"""HTTP 입력·응답과 저장 결과를 실제 임시 파일로 확인합니다."""
def test_health(isolated_client):
    client, _ = isolated_client
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_list_and_filter(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    r = client.get("/api/knowledge")
    assert r.status_code == 200
    assert [entry["id"] for entry in r.json()] == [1, 2, 3]
    assert "next_id" not in r.text
    filtered = client.get("/api/knowledge", params={"category": "api"})
    assert [entry["id"] for entry in filtered.json()] == [2, 3]
    empty = client.get("/api/knowledge", params={"category": "unknown"})
    assert empty.status_code == 200
    assert empty.json() == []
    assert path.read_bytes() == before


def test_detail_and_errors(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    r = client.get("/api/knowledge/2")
    assert r.status_code == 200
    assert r.json()["title"] == "서버 실행"
    assert client.get("/api/knowledge/9999").status_code == 404
    assert client.get("/api/knowledge/foo").status_code == 422
    # BEGIN H02-04
    # 해설 H02-04: GET의 비변경성을 데이터로 확인합니다. 같은 모양의 목록 응답만 확인하는 것보다 강한 검사입니다.
    assert path.read_bytes() == before
    # END H02-04
