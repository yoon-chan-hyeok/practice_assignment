"""조회 계산만 분리합니다. HTTP 응답이나 파일 저장은 여기서 처리하지 않습니다."""
def select_category(entries: list[dict], category: str | None) -> list[dict]:
    if category is None:
        return entries
    return [entry for entry in entries if entry["category"] == category]


def find_entry(entries: list[dict], knowledge_id: int) -> dict | None:
    for entry in entries:
        if entry["id"] == knowledge_id:
            return entry
    return None
