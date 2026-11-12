def test_invalid_input_is_read_only(isolated):
    client, data_file = isolated
    before = data_file.read_bytes()
    response = client.post("/api/knowledge", json={"title":"실패 검사", "content":"", "category":"learning"})
    # BEGIN H-API-11
    # 해설 H-API-11: 422는 저장 로직 전에 거부됩니다. entries와 next_id 모두 보존되어야 합니다.
    assert response.status_code == 422
    assert data_file.read_bytes() == before
    # END H-API-11
def test_delete_contract(isolated):
    client, data_file = isolated
    created = client.post("/api/knowledge", json={"title":"삭제 검사", "content":"가상 안내입니다.", "category":"learning"})
    assert created.status_code == 201
    created_id = created.json()["id"]
    response = client.delete(f"/api/knowledge/{created_id}")
    # BEGIN H-API-12
    # 해설 H-API-12: 상태코드, 본문 없음, 실제 삭제를 각각 검사합니다. 테스트는 임시 파일을 사용하므로 작업 파일을 지우지
    # 않습니다.
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/knowledge/{created_id}").status_code == 404
    # END H-API-12
