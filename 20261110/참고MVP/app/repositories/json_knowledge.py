"""제공 코드: 파일 접근 보조 함수. 호출자가 같은 LOCK으로 읽기~저장을 묶습니다."""
import json
from pathlib import Path
from threading import Lock

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data" / "knowledge.json"
LOCK = Lock()


def read_data() -> dict:
    # 파일이 없거나 JSON이 손상되면 예외를 알립니다. 빈 목록으로 덮어쓰지 않습니다.
    with DATA.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_data(data: dict) -> None:
    # 원본부터 비우지 않고 같은 폴더의 임시 파일을 완성한 다음 교체합니다.
    # 단일 프로세스의 같은 LOCK 아래에서만 호출합니다. DB 트랜잭션은 아닙니다.
    temp = DATA.with_suffix(".tmp")
    try:
        with temp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp.replace(DATA)
    finally:
        temp.unlink(missing_ok=True)

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
        # 구조를 나눠도 저장이 실제로 수행되어야 합니다.
        write_data(data)
    return entry

def update(knowledge_id: int, fields: dict) -> dict | None:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = dict(fields)
                updated["id"] = knowledge_id
                data["entries"][i] = updated
                write_data(data)
                return updated
    return None

def delete(knowledge_id: int) -> bool:
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                data["entries"].pop(i)
                write_data(data)
                return True
    return False
