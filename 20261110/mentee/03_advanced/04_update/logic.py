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
                # TODO H04-01: fields의 복사본 updated를 만들고 기존 요청 ID를 유지하세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("H04-01를 먼저 완성하세요.")
                # END H04-01
                # BEGIN H04-02
                # TODO H04-02: 찾은 위치 i를 교체하고 저장하세요. 다른 항목과 next_id는 그대로 두세요.
                # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
                raise NotImplementedError("H04-02를 먼저 완성하세요.")
                # END H04-02
                return updated
    return None
