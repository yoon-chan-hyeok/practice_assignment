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
    assert path.read_bytes() == before

def test_create_and_read_back(isolated_client):
    client, path = isolated_client
    payload = {"title": "새 안내", "content": "로컬 폴더를 확인합니다.", "category": "guide"}
    r = client.post("/api/knowledge", json=payload)
    assert r.status_code == 201
    entry = r.json()
    assert entry == dict(payload, id=4)
    assert client.get(f"/api/knowledge/{entry['id']}").json() == entry
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert len(saved["entries"]) == 4
    assert saved["next_id"] == 5
    assert saved["entries"][-1] == entry


@pytest.mark.parametrize("payload", [
    {"content": "본문", "category": "guide"},
    {"title": "제목", "category": "guide"},
    {"title": "제목", "content": "본문"},
    {"title": "", "content": "본문", "category": "guide"},
    {"title": "제목", "content": "", "category": "guide"},
    {"title": "제목", "content": "본문", "category": ""},
    {"title": "가" * 81, "content": "본문", "category": "guide"},
    {"title": "제목", "content": "가" * 2001, "category": "guide"},
    {"title": "제목", "content": "본문", "category": "가" * 31},
])
def test_invalid_post_preserves_file(isolated_client, payload):
    client, path = isolated_client
    before = path.read_bytes()
    r = client.post("/api/knowledge", json=payload)
    assert r.status_code == 422
    assert path.read_bytes() == before


def test_json_syntax_error(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    r = client.post("/api/knowledge", content='{"title":', headers={"Content-Type": "application/json"})
    assert r.status_code == 422
    assert path.read_bytes() == before

def test_update_preserves_id_count_and_other_entries(isolated_client):
    client, path = isolated_client
    before = json.loads(path.read_text(encoding="utf-8"))
    payload = {"title": "서버 실행", "content": "새 안내 내용입니다.", "category": "api"}
    for _ in range(2):
        r = client.put("/api/knowledge/2", json=payload)
        assert r.status_code == 200
        assert r.json() == dict(payload, id=2)
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["next_id"] == before["next_id"]
    assert len(saved["entries"]) == len(before["entries"])
    assert saved["entries"][0] == before["entries"][0]
    assert saved["entries"][2] == before["entries"][2]
    assert client.get("/api/knowledge/2").json()["content"] == payload["content"]


def test_update_404_and_422_preserve_file(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    valid = {"title": "제목", "content": "본문", "category": "guide"}
    assert client.put("/api/knowledge/9999", json=valid).status_code == 404
    assert client.put("/api/knowledge/2", json={"content": "본문만"}).status_code == 422
    assert path.read_bytes() == before

def test_delete_empty_body_and_other_entries(isolated_client):
    client, path = isolated_client
    before = json.loads(path.read_text(encoding="utf-8"))
    r = client.delete("/api/knowledge/2")
    assert r.status_code == 204
    assert r.content == b""
    assert client.get("/api/knowledge/2").status_code == 404
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["entries"] == [entry for entry in before["entries"] if entry["id"] != 2]
    assert saved["next_id"] == before["next_id"]


def test_delete_errors_preserve_file(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    assert client.delete("/api/knowledge/9999").status_code == 404
    assert client.delete("/api/knowledge/foo").status_code == 422
    assert path.read_bytes() == before


def test_create_after_last_id_deleted(isolated_client):
    client, path = isolated_client
    assert client.delete("/api/knowledge/3").status_code == 204
    r = client.post("/api/knowledge", json={"title":"새 지식", "content":"새 내용", "category":"guide"})
    assert r.status_code == 201
    assert r.json()["id"] == 4
    assert json.loads(path.read_text(encoding="utf-8"))["next_id"] == 5

def test_openapi_and_response_fields(isolated_client):
    client, _ = isolated_client
    doc = client.get("/openapi.json").json()
    assert {"get", "post"} <= set(doc["paths"]["/api/knowledge"])
    assert {"get", "put", "delete"} <= set(doc["paths"]["/api/knowledge/{knowledge_id}"])
    r = client.get("/api/knowledge/1")
    assert r.status_code == 200
    # BEGIN H06-04
    # TODO H06-04: 상세 응답의 키가 id·title·content·category 네 가지인지 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H06-04를 먼저 완성하세요.")
    # END H06-04
    assert client.get("/docs").status_code == 200
