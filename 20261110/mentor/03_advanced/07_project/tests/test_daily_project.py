"""8교시 심화: 임시 파일만 변경합니다. 실제 서버 재시작 검증은 별도로 하세요."""
import json


def test_daily_project_abc(isolated_client):
    client, path = isolated_client
    initial = json.loads(path.read_text(encoding="utf-8"))
    n = len(initial["entries"])
    payloads = [
        {"title": "파일 보관", "content": "개인 폴더에 보관합니다.", "category": "learning"},
        {"title": "질문 방법", "content": "질문을 메모합니다.", "category": "help"},
        {"title": "임시 공지", "content": "이 항목은 삭제 확인용입니다.", "category": "help"},
    ]
    created = []
    for payload in payloads:
        response = client.post("/api/knowledge", json=payload)
        assert response.status_code == 201
        created.append(response.json())
    a, b, c = created
    assert len({a["id"], b["id"], c["id"]}) == 3
    assert len(client.get("/api/knowledge").json()) == n + 3
    changed = {"title": b["title"], "content": "오류 메시지와 함께 질문합니다.", "category": b["category"]}
    r = client.put(f"/api/knowledge/{b['id']}", json=changed)
    # BEGIN H08-01
    # 해설 H08-01: 자동 테스트는 임시 파일의 수정 반영을 검사합니다. 실제 서버 재시작 두 번은 별도의 수동 확인입니다.
    assert r.status_code == 200
    assert client.get(f"/api/knowledge/{b['id']}").json() == dict(changed, id=b["id"])
    # END H08-01
    before_invalid = path.read_bytes()
    bad = {"title": "빈 본문", "content": "", "category": "help"}
    r = client.post("/api/knowledge", json=bad)
    # BEGIN H08-02
    # 해설 H08-02: 실패 요청으로 ID 발급 번호가 증가해도 잘못된 동작입니다.
    assert r.status_code == 422
    assert path.read_bytes() == before_invalid
    # END H08-02
    r = client.delete(f"/api/knowledge/{c['id']}")
    # BEGIN H08-03
    # 해설 H08-03: A는 유지, B는 수정, C는 삭제로 역할을 나누면 수정 결과와 삭제 결과를 동시에 확인할 수 있습니다.
    assert r.status_code == 204
    assert r.content == b""
    assert client.get(f"/api/knowledge/{c['id']}").status_code == 404
    # END H08-03
    final = json.loads(path.read_text(encoding="utf-8"))
    assert len(final["entries"]) == n + 2
    assert client.get(f"/api/knowledge/{a['id']}").json() == a
    for old in initial["entries"]:
        assert client.get(f"/api/knowledge/{old['id']}").json() == old
