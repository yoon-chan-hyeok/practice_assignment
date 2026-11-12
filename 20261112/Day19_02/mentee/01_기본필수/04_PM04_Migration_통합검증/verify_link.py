"""서버를 실행한 상태에서 API 응답의 id와 DB 행을 대조합니다."""
import json, os
from urllib.request import Request, urlopen
from sqlalchemy import create_engine, text
from app.settings import get_settings

BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
url = get_settings().database_url
body = json.dumps({"title":"__verify_link__","content":"API와 DB를 함께 확인합니다.","category":"learning"}).encode()
req = Request(BASE+"/api/knowledge", data=body, headers={"Content-Type":"application/json"}, method="POST")
with urlopen(req) as r:
    created = json.loads(r.read())
print("API created:", created)
with create_engine(url).connect() as conn:
    # TODO B11: API 응답의 id와 같은 DB 행을 JOIN으로 조회하세요.
    row = conn.execute(text("SELECT NULL, NULL, NULL")).one()
    print("DB row:", row)
req = Request(BASE+f"/api/knowledge/{created['id']}", method="DELETE")
with urlopen(req) as r: print("DELETE status:", r.status)
with create_engine(url).connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM knowledge WHERE id=:id"), {"id":created["id"]}).scalar_one()
    print("DB remaining:", count)
