def test_invalid_input_is_read_only(isolated):
    client, data_file = isolated
    before = data_file.read_bytes()
    response = client.post("/api/knowledge", json={"title":"실패 검사", "content":"", "category":"learning"})
    # BEGIN H-API-11
    # TODO H-API-11: 빈 content 요청이 422인지 검사하고, 파일 bytes가 요청 전과 완전히 같은지 assert하세요.
    raise NotImplementedError("H-API-11: 주석 요구사항을 완성하세요.")
    # END H-API-11
def test_delete_contract(isolated):
    client, data_file = isolated
    created = client.post("/api/knowledge", json={"title":"삭제 검사", "content":"가상 안내입니다.", "category":"learning"})
    assert created.status_code == 201
    created_id = created.json()["id"]
    response = client.delete(f"/api/knowledge/{created_id}")
    # BEGIN H-API-12
    # TODO H-API-12: 삭제 응답이204이고 빈 본문인지, 같은ID 상세 재조회가404인지 assert하세요.
    raise NotImplementedError("H-API-12: 주석 요구사항을 완성하세요.")
    # END H-API-12
