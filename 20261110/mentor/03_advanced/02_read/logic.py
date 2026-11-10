"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    # BEGIN H02-01
    # 해설 H02-01: 읽기 함수는 데이터 변경을 하지 않습니다. HTTP 상태는 Router가 결정합니다.
    return entries
    # END H02-01


def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    # BEGIN H02-02
    # 해설 H02-02: None은 조회 결과가 없다는 데이터 계층의 표현입니다. 이 함수에서 HTTPException을 쓰지 않습니다.
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    # END H02-02
    return None
