import json
import pytest

"""HTTP 입력·응답과 저장 결과를 실제 임시 파일로 확인합니다."""
def test_health(isolated_client):
    client, _ = isolated_client
    r = client.get("/health")
    # BEGIN H01-02
    # 해설 H01-02: TestClient는 실제 앱 경로를 호출하지만 별도 Uvicorn 서버를 시작하지 않습니다.
    assert r.status_code == 200
    # END H01-02
    # BEGIN H01-03
    # 해설 H01-03: 200만 검사하면 잘못된 본문을 놓칠 수 있습니다. 상태와 내용을 함께 검사합니다.
    assert r.json() == {"status": "ok"}
    # END H01-03
