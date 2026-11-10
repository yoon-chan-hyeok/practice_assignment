"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    return entries


def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None

def create(fields: dict) -> dict:
    with LOCK:
        data = read_data()
        # BEGIN H03-01
        # 해설 H03-01: 입력 dict를 직접 변경하지 않도록 복사합니다. ID 발급은 같은 LOCK 안에서 수행합니다.
        entry = dict(fields)
        entry["id"] = data["next_id"]
        # END H03-01
        # BEGIN H03-02
        # 해설 H03-02: 읽기→변경→저장 전체를 잠금으로 묶습니다. 단일 프로세스 범위이며 DB 트랜잭션은 아닙니다.
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
        # END H03-02
    return entry
