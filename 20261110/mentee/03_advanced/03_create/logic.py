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
        # TODO H03-01: fields를 복사한 entry를 만들고 현재 next_id를 id로 지정하세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        raise NotImplementedError("H03-01를 먼저 완성하세요.")
        # END H03-01
        # BEGIN H03-02
        # TODO H03-02: entry를 추가하고 다음 ID를 증가시켜 data 전체를 저장하세요.
        # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
        raise NotImplementedError("H03-02를 먼저 완성하세요.")
        # END H03-02
    return entry
