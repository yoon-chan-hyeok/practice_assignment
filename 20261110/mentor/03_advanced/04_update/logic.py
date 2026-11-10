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
        entry = dict(fields)
        entry["id"] = data["next_id"]
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
    return entry

def update(knowledge_id: int, fields: dict) -> dict | None:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                # BEGIN H04-01
                # 해설 H04-01: 수정에서 새 ID를 발급하지 않습니다. 입력 모델은 title·content·category 세 필드를 모두 요구합니다.
                updated = dict(fields)
                updated["id"] = knowledge_id
                # END H04-01
                # BEGIN H04-02
                # 해설 H04-02: id와 index를 분리해 생각해야 삭제로 생긴 ID 빈칸에서도 올바르게 동작합니다.
                data["entries"][i] = updated
                write_data(data)
                # END H04-02
                return updated
    return None
