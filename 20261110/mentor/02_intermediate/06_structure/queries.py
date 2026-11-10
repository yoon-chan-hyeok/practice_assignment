"""조회 계산만 분리합니다. HTTP 응답이나 파일 저장은 여기서 처리하지 않습니다."""
def select_category(entries: list[dict], category: str | None) -> list[dict]:
    if category is None:
        return entries
    # BEGIN A06-01
    # 해설 A06-01: 입력 목록 → 결과 목록의 계산을 분리하면 HTTP 없이도 확인하기 쉽습니다.
    return [entry for entry in entries if entry["category"] == category]
    # END A06-01


def find_entry(entries: list[dict], knowledge_id: int) -> dict | None:
    # BEGIN A06-02
    # 해설 A06-02: 조회 함수는 None을 반환하고, HTTP의 404 여부는 호출한 Route가 결정합니다.
    for entry in entries:
        if entry["id"] == knowledge_id:
            return entry
    # END A06-02
    return None
