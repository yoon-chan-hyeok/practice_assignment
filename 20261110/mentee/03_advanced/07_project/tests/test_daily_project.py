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
    # TODO H08-01: B 수정의 200과 같은 ID의 재조회 본문을 검사하세요. expected는 changed와 B의 기존 ID입니다.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H08-01를 먼저 완성하세요.")
    # END H08-01
    before_invalid = path.read_bytes()
    bad = {"title": "빈 본문", "content": "", "category": "help"}
    r = client.post("/api/knowledge", json=bad)
    # BEGIN H08-02
    # TODO H08-02: 빈 본문 입력의 422와 파일 불변을 검사하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H08-02를 먼저 완성하세요.")
    # END H08-02
    r = client.delete(f"/api/knowledge/{c['id']}")
    # BEGIN H08-03
    # TODO H08-03: C 삭제의 204·빈 본문과 삭제 후 상세 GET의 404를 모두 확인하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H08-03를 먼저 완성하세요.")
    # END H08-03
    final = json.loads(path.read_text(encoding="utf-8"))
    assert len(final["entries"]) == n + 2
    assert client.get(f"/api/knowledge/{a['id']}").json() == a
    for old in initial["entries"]:
        assert client.get(f"/api/knowledge/{old['id']}").json() == old
