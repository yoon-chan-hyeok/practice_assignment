"""제공 도구. 실행 환경을 확인할 뿐 시스템 설정을 바꾸지 않습니다."""
import importlib.metadata as meta
import json
import platform
import sys

if __name__ == "__main__":
    result = {"python": platform.python_version(), "executable": sys.executable, "platform": platform.platform()}
    for name in ["fastapi", "pydantic", "starlette", "uvicorn", "httpx", "pytest", "jinja2"]:
        try:
            result[name] = meta.version(name)
        except meta.PackageNotFoundError:
            result[name] = "미설치 (pytest/httpx는 심화, jinja2는 선택 시연용)"
    print(json.dumps(result, ensure_ascii=False, indent=2))
