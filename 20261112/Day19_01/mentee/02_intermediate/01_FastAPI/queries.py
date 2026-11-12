"""조회 조건과 대상 찾기. 파일이나 HTTP를 직접 다루지 않습니다."""
def filter_entries(entries: list[dict], category: str | None) -> list[dict]:
    # BEGIN A-API-01
    # TODO A-API-01: category가 None이 아닐 때만 entries를 분류 문자열의 완전 일치로 필터링하세요. 빈 문자열도
    # 조건입니다.
    raise NotImplementedError("A-API-01: 주석 요구사항을 완성하세요.")
    # END A-API-01
    return sorted(entries, key=lambda entry: entry["id"])


def find_entry(entries: list[dict], knowledge_id: int) -> dict | None:
    # BEGIN A-API-02
    # TODO A-API-02: entries에서 id가 knowledge_id인 첫 항목을 반환하세요. 없으면 None을 반환하세요.
    raise NotImplementedError("A-API-02: 주석 요구사항을 완성하세요.")
    # END A-API-02
