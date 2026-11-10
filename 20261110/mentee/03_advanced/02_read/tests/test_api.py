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
    # TODO H02-04: 정상·404·422 GET 이후 파일 바이트가 before와 같은지 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H02-04를 먼저 완성하세요.")
    # END H02-04
