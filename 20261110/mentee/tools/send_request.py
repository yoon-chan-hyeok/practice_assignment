"""/docs가 열리지 않을 때 사용하는 선택 도구. Python 표준 라이브러리만 사용합니다."""
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="로컬 실습 API 요청")
    parser.add_argument("method", choices=["GET", "POST", "PUT", "DELETE"])
    parser.add_argument("url", help="예: http://127.0.0.1:8000/api/knowledge")
    parser.add_argument("--json-file", type=Path, help="UTF-8 JSON Body 파일. id는 서버 응답에서 받습니다.")
    args = parser.parse_args()
    parts = urllib.parse.urlsplit(args.url)
    if parts.scheme != "http" or parts.hostname not in {"127.0.0.1", "localhost"}:
        parser.error("이 도구는 로컬 HTTP 실습 서버만 호출합니다.")
    if args.method in {"GET", "DELETE"} and args.json_file:
        parser.error("이번 실습에서 GET·DELETE에는 Body를 보내지 않습니다.")
    data = None
    headers = {}
    if args.json_file:
        obj = json.loads(args.json_file.read_text(encoding="utf-8-sig"))
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    safe_url = urllib.parse.urlunsplit((parts.scheme, parts.netloc,
        urllib.parse.quote(parts.path, safe="/%"), urllib.parse.quote(parts.query, safe="=&%"), ""))
    request = urllib.request.Request(safe_url, data=data, headers=headers, method=args.method)
    try:
        with urllib.request.urlopen(request, timeout=10) as r:
            print("Status:", r.status)
            print("Content-Type:", r.headers.get("Content-Type"))
            body = r.read()
            print(body.decode("utf-8") if body else "(본문 없음)")
    except urllib.error.HTTPError as e:
        print("Status:", e.code)
        print(e.read().decode("utf-8", errors="replace"))
        return 2  # 예상된 404·422도 HTTP 오류 응답이므로 명시적으로 구분합니다.
    except urllib.error.URLError as e:
        print("서버 연결 실패:", e.reason)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
