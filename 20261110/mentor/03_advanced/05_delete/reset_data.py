"""서버를 끈 상태에서만 명시적으로 초기화합니다. 서버 시작 시 호출하지 마세요."""
import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil


def main() -> None:
    parser = argparse.ArgumentParser(description="현재 폴더의 학습 데이터 초기화")
    parser.add_argument("--confirm-reset", action="store_true", help="기존 작업 데이터 초기화를 명시적으로 승인")
    args = parser.parse_args()
    if not args.confirm_reset:
        parser.error("서버를 먼저 종료하세요. 초기화가 필요할 때만 --confirm-reset을 붙입니다.")
    base = Path(__file__).resolve().parent
    data = base / "data" / "knowledge.json"
    seed = base / "data" / "knowledge.seed.json"
    obj = json.loads(seed.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or not isinstance(obj.get("entries"), list) or not isinstance(obj.get("next_id"), int):
        raise ValueError("초기 데이터 형식이 올바르지 않습니다. 현재 파일은 유지합니다.")
    if data.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup = data.with_name(f"knowledge.backup_{stamp}.json")
        shutil.copy2(data, backup)
        print("백업:", backup)
    temp = data.with_suffix(".reset.tmp")
    try:
        temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(data)
    finally:
        temp.unlink(missing_ok=True)
    print("초기화 완료:", data)
    print("일일프로젝트의 재시작 확인 중에는 이 명령을 실행하지 않습니다.")


if __name__ == "__main__":
    main()
