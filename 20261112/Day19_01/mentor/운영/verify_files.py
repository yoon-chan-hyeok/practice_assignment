"""읽기 전용 정적 검사. 실제 PostgreSQL 검사는 verify_postgres.py로 별도 실행합니다."""
from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[1]
STUDENT = ROOT.parent / "수강생용"
pattern = re.compile(r"(?ms)^[ \t]*(?:#|--) BEGIN (?P<id>[BAH]-(?:API|DDL|SQL)-\d+)\n.*?^[ \t]*(?:#|--) END (?P=id)[ \t]*$")
if __name__ == "__main__":
    result = {"python_syntax": 0, "json": 0, "paired_blocks": 0, "student_pair_check": "skipped: 통합본에 수강생용이 있을 때만 수행", "postgresql_executed": False}
    for path in ROOT.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        result["python_syntax"] += 1
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8")); result["json"] += 1
    if STUDENT.is_dir():
        for path in STUDENT.rglob("*"):
            if not path.is_file() or path.suffix not in (".py", ".sql"): continue
            target = ROOT / path.relative_to(STUDENT)
            answers = {m["id"]: m[0] for m in pattern.finditer(target.read_text(encoding="utf-8"))}
            filled = pattern.sub(lambda m: answers[m["id"]], path.read_text(encoding="utf-8"))
            assert filled == target.read_text(encoding="utf-8"), path
            result["paired_blocks"] += len(answers)
        result["student_pair_check"] = "passed"
    print(json.dumps(result, ensure_ascii=False, indent=2))
