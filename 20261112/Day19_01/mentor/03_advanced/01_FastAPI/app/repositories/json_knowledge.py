"""제공 코드. 파일 읽기/쓰기는 호출자가 같은 LOCK 안에서 수행합니다."""
import json
from pathlib import Path
from threading import Lock

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data" / "knowledge.json"
LOCK = Lock()


def read_data() -> dict:
    # 파일 손상/누락을 빈 데이터로 숨기지 않습니다.
    with DATA.open(encoding="utf-8") as f:
        return json.load(f)


def write_data(data: dict) -> None:
    # 단일 프로세스에서 완성한 임시 파일을 교체합니다. DB 트랜잭션의 대체물이 아닙니다.
    temporary = DATA.with_suffix(".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temporary.replace(DATA)
    finally:
        temporary.unlink(missing_ok=True)


def list_entries(category: str | None = None) -> list[dict]:
    with LOCK:
        entries = read_data()["entries"]
    # BEGIN H-API-01
    # 해설 H-API-01: category가 None이 아닐 때만 entries를 분류 완전 일치로 필터링하고 ID 오름차순 목록을
    # 반환하세요.
    if category is not None:
        entries = [e for e in entries if e["category"] == category]
    return sorted(entries, key=lambda e: e["id"])
    # END H-API-01
def find_entry(knowledge_id: int) -> dict | None:
    with LOCK:
        data = read_data()
    # BEGIN H-API-02
    # 해설 H-API-02: 파일에서 읽은 entries에서 knowledge_id와 같은 id의 항목을 반환하고 없으면 None을
    # 반환하세요.
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    return None
    # END H-API-02
def create(fields: dict) -> dict:
    with LOCK:
        data = read_data()
        # BEGIN H-API-03
        # 해설 H-API-03: fields를 복사해 entry를 만들고 next_id로 ID를 발급하세요. entries에 추가하고
        # next_id를 1 늘리세요. 아직 여기서는 저장하지 않습니다.
        entry = dict(fields)
        entry["id"] = data["next_id"]
        data["entries"].append(entry)
        data["next_id"] += 1
        # END H-API-03
        # BEGIN H-API-04
        # 해설 H-API-04: 변경된 data를 저장하고 entry를 반환하세요. 저장 실패를 성공 결과로 바꾸지 마세요.
        write_data(data)
        return entry
        # END H-API-04
def update(knowledge_id: int, fields: dict) -> dict | None:
    with LOCK:
        data = read_data()
        # BEGIN H-API-05
        # 해설 H-API-05: 해당 ID가 있는 위치만 fields 복사본과 같은 ID로 교체·저장·반환하세요. 없으면 None을 반환하세요.
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = dict(fields)
                updated["id"] = knowledge_id
                data["entries"][i] = updated
                write_data(data)
                return updated
        return None
        # END H-API-05
def delete(knowledge_id: int) -> bool:
    with LOCK:
        data = read_data()
        # BEGIN H-API-06
        # 해설 H-API-06: 같은 ID가 있으면 그 항목만 삭제·저장하고 True, 없으면 False를 반환하세요. HTTP 상태코드는
        # 여기에서 결정하지 않습니다.
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                data["entries"].pop(i)
                write_data(data)
                return True
        return False
        # END H-API-06
