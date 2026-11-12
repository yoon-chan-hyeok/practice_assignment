"""명시적 복습 초기화. 서버를 Ctrl+C로 종료한 후 실행하세요."""
from pathlib import Path
import argparse
import json
import shutil
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="이 폴더의 JSON 작업 데이터만 초기화합니다.")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    if not args.confirm:
        parser.error("서버를 종료하고 python reset_data.py --confirm 으로 실행하세요.")
    root = Path(__file__).resolve().parent
    seed, target = root/"data/knowledge.seed.json", root/"data/knowledge.json"
    json.loads(seed.read_text(encoding="utf-8"))
    if target.exists():
        backup = root/"data"/f"knowledge.backup-{datetime.now():%Y%m%d-%H%M%S-%f}.json"
        shutil.copy2(target, backup)
        print("기존 파일 백업:", backup.name)
    shutil.copy2(seed, target)
    print("이 프로젝트의 knowledge.json을 S0로 초기화했습니다. DB는 변경하지 않았습니다.")
