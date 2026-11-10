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
    # BEGIN H03-03
    # TODO H03-03: 초기 3건 기준 생성된 entry가 요청 필드와 새 id=4를 포함하는지 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H03-03를 먼저 완성하세요.")
    # END H03-03
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
    # BEGIN H03-04
    # TODO H03-04: 잘못된 입력에 422가 나오고 파일이 변경되지 않았는지 모두 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H03-04를 먼저 완성하세요.")
    # END H03-04


def test_json_syntax_error(isolated_client):
    client, path = isolated_client
    before = path.read_bytes()
    r = client.post("/api/knowledge", content='{"title":', headers={"Content-Type": "application/json"})
    assert r.status_code == 422
    assert path.read_bytes() == before
