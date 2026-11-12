"""제공 검사 도구. 임시 복사본만 검사하며 원본 JSON은 수정하지 않습니다."""
from pathlib import Path
import argparse
import importlib
import json
import shutil
import subprocess
import sys
import tempfile

LEVEL = "H"


def worker(root: Path) -> dict:
    from fastapi.testclient import TestClient
    sys.path.insert(0, str(root))
    if LEVEL == "H":
        app = importlib.import_module("app.main").app
        store = importlib.import_module("app.repositories.json_knowledge")
    else:
        app = importlib.import_module("main").app
        store = importlib.import_module("storage")
    seed = json.loads((root / "data/knowledge.seed.json").read_text(encoding="utf-8"))
    path = root / "data/knowledge.json"
    shutil.copy2(root / "data/knowledge.seed.json", path)
    checks = []

    def check(ok: bool, message: str) -> None:
        if not ok:
            raise AssertionError(message)
        checks.append(message)

    def data() -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    new = {"title": "보충 학습", "content": "복습 자료는 개인 폴더에서 확인합니다.", "category": "learning"}
    changed = {**new, "content": "복습 자료와 예제 코드를 함께 확인합니다."}
    with TestClient(app, raise_server_exceptions=True) as client:
        def request(method: str, url: str, status: int, payload=None):
            kw = {} if payload is None else {"json": payload}
            r = client.request(method, url, **kw)
            check(r.status_code == status, f"{method} {url}: {status} 응답")
            return r

        r = request("GET", "/health", 200)
        check(r.json() == {"status": "ok"}, "health 본문")
        check(client.get("/openapi.json").status_code == 200, "OpenAPI 생성")
        r = request("GET", "/api/knowledge", 200)
        check(r.json() == seed["entries"], "S0 목록 값·순서")
        r = request("GET", "/api/knowledge/2", 200)
        check(r.json() == seed["entries"][1], "ID2 상세")
        for method in ("GET", "PUT", "DELETE"):
            before = path.read_bytes()
            r = request(method, "/api/knowledge/999999", 404, changed if method == "PUT" else None)
            check(r.json() == {"detail": "Knowledge not found"}, f"{method} 404 본문")
            check(path.read_bytes() == before, f"{method} 404 파일 보존")
        for method, url, payload, field, where in [
            ("GET", "/api/knowledge/foo", None, "knowledge_id", "path"),
            ("POST", "/api/knowledge", {**new, "content": ""}, "content", "body"),
            ("PUT", "/api/knowledge/2", {"content": changed["content"]}, "title", "body"),
        ]:
            before = path.read_bytes()
            r = request(method, url, 422, payload)
            locations = [e.get("loc", []) for e in r.json().get("detail", [])]
            check(any(loc[:2] == [where, field] for loc in locations), f"422 위치: {where}.{field}")
            check(path.read_bytes() == before, "422 파일·next_id 보존")
        if LEVEL != "B":
            before = path.read_bytes()
            for cat, ids in [("learning", [1, 3]), ("reference", []), ("unknown", []), ("", []), ("Learning", [])]:
                r = client.get("/api/knowledge", params={"category": cat})
                check(r.status_code == 200 and [x["id"] for x in r.json()] == ids, f"category={cat!r} 결과")
            check(path.read_bytes() == before, "필터는 파일을 변경하지 않음")
        r = request("POST", "/api/knowledge", 201, new)
        created = r.json()
        new_id = created["id"]
        check(isinstance(new_id, int) and new_id == seed["next_id"], "서버에서 next_id 발급")
        check(created == {"id": new_id, **new}, "POST 입력·응답 값")
        check(data() == {"next_id": seed["next_id"] + 1, "entries": seed["entries"] + [created]}, "POST 실제 파일·기존 행 보존")
        r = request("PUT", f"/api/knowledge/{new_id}", 200, changed)
        updated = {"id": new_id, **changed}
        check(r.json() == updated, "PUT 같은 ID·세 필드")
        check(data() == {"next_id": seed["next_id"] + 1, "entries": seed["entries"] + [updated]}, "PUT 저장·개수·next_id 유지")
        check(request("GET", f"/api/knowledge/{new_id}", 200).json() == updated, "PUT 뒤 재조회")
        r = request("DELETE", f"/api/knowledge/{new_id}", 204)
        check(r.content == b"", "204 본문 길이 0")
        request("GET", f"/api/knowledge/{new_id}", 404)
        check(data() == {"next_id": seed["next_id"] + 1, "entries": seed["entries"]}, "삭제 후 기존 데이터·next_id 보존")
        check(request("GET", "/api/knowledge", 200).json() == seed["entries"], "최종 목록 S0")
        # Isolation: these boundary checks do not modify the student's file or the main scenario.
        if LEVEL == "H":
            for field, limit in [("title", 80), ("content", 2000), ("category", 30)]:
                path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")
                r = request("POST", "/api/knowledge", 201, {**new, field: "가" * limit})
                check(r.json()[field] == "가" * limit, f"{field} 최대 길이 허용")
                before = path.read_bytes()
                request("POST", "/api/knowledge", 422, {**new, field: "가" * (limit + 1)})
                check(path.read_bytes() == before, f"{field} 초과 길이 저장 금지")
            path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")
            r = request("POST", "/api/knowledge", 201, {**new, "title": seed["entries"][0]["title"]})
            check(r.json()["id"] not in [e["id"] for e in seed["entries"]], "제목 중복 허용·ID 별도 발급")
    return {"level": LEVEL, "passed": len(checks), "checks": checks, "scope": "임시 파일 + TestClient; 실제 서버 재시작은 별도 확인"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        try:
            print(json.dumps(worker(args.worker.resolve()), ensure_ascii=False))
            return 0
        except Exception as exc:
            print(f"검사 실패: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 1
    source = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="day19_api_check_") as temp:
        copy = Path(temp) / "api"
        shutil.copytree(source, copy, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache", "*.backup-*.json"))
        result = subprocess.run([sys.executable, str(copy / "check_api.py"), "--worker", str(copy)], cwd=copy, text=True, encoding="utf-8", capture_output=True)
        if result.returncode:
            print(result.stderr.strip() or result.stdout.strip())
            print("요구사항과 해당 TODO를 확인한 뒤 다시 실행하세요. 원본 파일은 변경하지 않았습니다.")
            return result.returncode
        report = json.loads(result.stdout)
        print(f"검사 통과: {report['passed']}개 확인 / {LEVEL} / 임시 데이터만 사용")
        print(report["scope"])
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
