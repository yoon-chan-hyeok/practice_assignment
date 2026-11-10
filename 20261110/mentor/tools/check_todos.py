"""제공 도구. 미완성 표시를 찾는 보조 점검이며 정답 채점기는 아닙니다."""
from pathlib import Path
import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".", help="검사할 현재 교시 폴더")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    found = []
    pattern = re.compile(r"# BEGIN ([BAH]\d{2}-\d{2})\n(.*?)# END \1", re.S)
    for path in root.rglob("*.py"):
        if any(part in {".venv", "__pycache__", ".git"} for part in path.parts):
            continue
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            body = "\n".join(line.split("#", 1)[0] for line in match.group(2).splitlines())
            if "NotImplementedError" in body or "TODO:" in body or re.search(r"^\s*pass\s*$", body, re.M):
                found.append((str(path.relative_to(root)), match.group(1)))
    for path, tid in found:
        print(tid, path)
    print(f"미완성 표시: {len(found)}개. 0개라도 요청·응답·파일 검증을 해야 합니다.")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
