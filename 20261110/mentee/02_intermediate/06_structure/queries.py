"""조회 계산만 분리합니다. HTTP 응답이나 파일 저장은 여기서 처리하지 않습니다."""
def select_category(entries: list[dict], category: str | None) -> list[dict]:
    if category is None:
        return entries
    # BEGIN A06-01
    # TODO A06-01: category가 있는 경우 정확히 일치하는 항목들의 목록을 반환하세요. 이 함수에서 파일을 읽거나 HTTPException을 사용하지 마세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("A06-01를 먼저 완성하세요.")
    # END A06-01


def find_entry(entries: list[dict], knowledge_id: int) -> dict | None:
    # BEGIN A06-02
    # TODO A06-02: entries에서 ID가 같은 항목을 찾아 반환하세요. 없으면 아래 return None으로 진행하세요.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("A06-02를 먼저 완성하세요.")
    # END A06-02
    return None
