"""제공 코드. 파일 읽기/쓰기는 호출자가 같은 LOCK 안에서 수행합니다."""
import json
from pathlib import Path
from threading import Lock

BASE = Path(__file__).resolve().parent
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
