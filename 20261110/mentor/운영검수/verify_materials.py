"""강사용 선택 검사. 실제 지식은 바꾸지 않고 앱별 임시 파일로 계약을 검사합니다.
먼저 강사용 루트에서 python -m pip install -r requirements-test.txt 를 실행하세요.
사용: python 운영검수/verify_materials.py [--include-student]
"""
from pathlib import Path
import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-student", action="store_true", help="형제 폴더 수강생용도 정답 대입 후 검사")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    teacher = here.parent
    student = teacher.parent / "수강생용"
    apps = json.loads((here / "apps.json").read_text(encoding="utf-8"))
    levels = {"B": "01_기본필수", "A": "02_응용", "H": "03_심화"}
    steps = {1:"01_first_server",2:"02_read",3:"03_create",4:"04_update",5:"05_delete",6:"06_structure",7:"07_project"}
    marker = re.compile(r"(?m)^[ \t]*# BEGIN ([BAH]\d{2}-\d{2})\n.*?^[ \t]*# END \1", re.S)
    results = []
    with tempfile.TemporaryDirectory(prefix="day17_verify_") as tmp:
        variants = [("teacher", teacher)]
        if args.include_student:
            if not student.is_dir():
                parser.error("통합 ZIP을 풀어 강사용과 수강생용을 같은 상위 폴더에 두세요.")
            solved = Path(tmp) / "solved"
            shutil.copytree(student, solved, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache"))
            count = 0
            for path in solved.rglob("*.py"):
                rel = path.relative_to(solved)
                answer = (teacher / rel).read_text(encoding="utf-8")
                blocks = {m.group(1):m.group(0) for m in marker.finditer(answer)}
                original = path.read_text(encoding="utf-8")
                count += len(list(marker.finditer(original)))
                completed = marker.sub(lambda m: blocks[m.group(1)], original)
                if ast.dump(ast.parse(completed)) != ast.dump(ast.parse(answer)):
                    raise AssertionError(f"정답 대입 후 불일치: {rel}")
                path.write_text(completed, encoding="utf-8")
            print("정답 대입 블록:", count)
            variants.append(("student_completed", solved))
        for variant, base in variants:
            for config in apps:
                project = base / levels[config["level"]] / steps[config["step"]]
                command = [sys.executable, str(here / "contract_worker.py"), str(project), json.dumps(config)]
                process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                    timeout=90, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1"))
                try:
                    result = json.loads(process.stdout.strip().splitlines()[-1])
                except (IndexError, json.JSONDecodeError):
                    result = {"status":"failed", "stdout":process.stdout, "stderr":process.stderr}
                result.update(variant=variant, level=config["level"], step=config["step"])
                results.append(result)
                print(variant, config["level"], config["step"], result["status"])
    destination = here / "verification_local.json"
    destination.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("검사 결과:", destination)
    print("이 검사는 실제 서버 프로세스 재시작과 학생 설명을 대신하지 않습니다.")
    return 0 if all(r["status"] == "passed" for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
