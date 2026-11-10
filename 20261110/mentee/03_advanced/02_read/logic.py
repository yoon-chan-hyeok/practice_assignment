"""데이터 처리 함수. HTTPException을 만들지 않고 dict·None·bool을 반환합니다."""
from storage import LOCK, read_data, write_data

def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        data = read_data()
    entries = data["entries"]
    if category is not None:
        entries = [entry for entry in entries if entry["category"] == category]
    # BEGIN H02-01
    # TODO H02-01: 읽고 필터링한 entries 목록을 반환하세요. 저장 함수를 호출하지 마세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H02-01를 먼저 완성하세요.")
    # END H02-01


def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    # BEGIN H02-02
    # TODO H02-02: 항목의 id와 knowledge_id가 일치하면 그 dict를 반환하세요. 없으면 아래 None으로 진행하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("H02-02를 먼저 완성하세요.")
    # END H02-02
    return None
