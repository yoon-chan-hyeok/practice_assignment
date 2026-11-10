# Day17 · FastAPI 지식 관리 API 실습 (수강생용)

**기준: 2026년 11월 10일 / 84장 PPT / 기본필수·응용·심화 / 마지막 일일프로젝트 포함**

오늘은 원본 지식을 HTTP로 생성·조회·수정·삭제하는 작은 서비스를 만듭니다. RAG·Agent·LLM·DB는 아직 연결하지 않습니다.

## 1. 시작 순서

압축을 푼 **수강생용 폴더를 VS Code에서 폴더 열기** 합니다. 압축파일 안에서 직접 실행하지 마세요.
가능하면 `C:\workspace\day17`처럼 짧은 로컬 경로를 사용하세요. GPU·CUDA·API 키는 필요 없습니다.
Python 문법은 3.10 이상, 실제 검수 버전과 한계는 검수결과.md에 기록했습니다.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
python tools/show_versions.py
```

VS Code의 Python: Select Interpreter에서 이 폴더의 .venv를 선택합니다.
활성화가 차단되면 정책을 바꾸지 말고 .venv Python 직접 실행 안내를 따릅니다.

심화를 선택한 경우만 추가 설치합니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
```

Linux/macOS는 `.venv/bin/python -m pip install -r requirements.txt`, `source .venv/bin/activate`를 사용합니다.
같은 수준의 01→07을 진행한 뒤 08 안내를 읽고 07의 코드를 재사용합니다.

## 2. 한 수준 선택

| 수준 | 핵심 앱 구조 | Python TODO 블록 | 학습 초점 |
|---|---|---:|---|
| [기본필수](01_기본필수/README.md) | main.py·storage.py·data | 15 | 핵심 동작과 수동 확인 |
| [응용](02_응용/README.md) | 기본 구조 + queries.py | 23 | 직접 작성 확대·category·함수 분리 |
| [심화](03_심화/README.md) | 함수 분리 → app/Router·Schema·Repository·tests | 30 | 책임 분리·임시 파일 자동 검사 |

폴더가 많은 것은 교시 시작점을 따로 제공하기 때문입니다. 기본필수 앱 자체의 핵심 Python 파일은 1~2개입니다.
TODO의 개수는 BEGIN/END로 묶은 Python 구현 블록 수입니다. 역할 설명·개인 지식 초안·기록 과제는 별도입니다.

## 3. 첫 서버

```powershell
cd ".\01_기본필수\01_first_server"
# main.py의 B01-01을 먼저 완성한 뒤 실행합니다.
python -m uvicorn main:app --reload
```

브라우저에 `http://127.0.0.1:8000/health`와 `http://127.0.0.1:8000/docs`를 엽니다.
앱은 기본적으로 로컬에만 엽니다. --workers 옵션이나 외부 공개 옵션을 추가하지 않습니다.
기본필수·응용과 심화 01~05는 main:app, 심화 06~07은 app.main:app입니다.

## 4. 수강생용과 강사용

수강생용의 미완성 코드는 NotImplementedError 또는 Route 등록 전 pass로 명확히 표시했습니다.
TODO 주석의 요구사항을 구현하고, 같은 블록의 미완성 표시를 제거합니다. 정답을 쓰지 않고 pass로 숨기지 마세요.
같은 ID·파일·함수가 강사용에 대응합니다. 이전 교시의 기능은 다음 교시 시작본에 완성 골격으로 포함됩니다.
기본필수는 pytest를 사용하지 않아도 됩니다. 심화 테스트는 실제 작업 파일이 아닌 tmp_path를 사용합니다.

## 5. 데이터와 과제

각 02~07은 자체 data/knowledge.json과 변경하지 않는 knowledge.seed.json을 가집니다.
초기화가 정말 필요할 때만 서버 종료 후 `python reset_data.py --confirm-reset`을 실행합니다. 기존 파일은 백업됩니다.
08의 A/B/C 프로젝트 중에는 초기화하지 않습니다. 07의 `일일프로젝트_기록.md`에 실제 ID·N·파일 상태를 적습니다.

공통 API 계약은 [공통안내/API_계약.md](공통안내/API_계약.md), 문제 해결은 [공통안내/오류해결.md](공통안내/오류해결.md)를 확인합니다.

## 6. /docs 대안과 보조 도구 (필수 아님)

다른 터미널을 수강생용 루트에서 열고 활성화한 뒤 실행할 수 있습니다.

```powershell
python tools/send_request.py GET http://127.0.0.1:8000/api/knowledge
python tools/send_request.py POST http://127.0.0.1:8000/api/knowledge --json-file 공통안내/요청예시/create.json
```

PUT·DELETE는 방금 받은 실제 ID로 호출합니다. 204에는 본문이 없습니다. 이 도구는 예상 404·422에도 종료코드 2를 돌려 상태를 구분합니다.
현재 교시 폴더에서 `python ../../tools/check_todos.py .`로 미완성 표시를 찾을 수 있습니다. 이것은 정답 채점기가 아닙니다.

별도 제공된 완성형 참고 MVP는 수업 중 전체 구조를 참고하기 위한 자료입니다. 수강생용 ZIP에는 정답본이나 MVP를 포함하지 않았습니다.
