# 실습 07 · 함께 통합하고 프로젝트 준비

강사용 완성본입니다. 동일한 BEGIN/END ID 위치에서 정답과 핵심 해설을 확인합니다.

**PPT 47–55쪽 / 40분 / 심화**

## 작업 순서

1. 이전 교시 서버를 Ctrl+C로 종료합니다.
2. 아래 교시 폴더를 현재 작업 폴더로 사용합니다. 이 폴더가 프로젝트 루트입니다.
3. 요구된 TODO를 구현하고 서버를 실행합니다. 앞 교시가 미완성이어도 이 폴더의 선행 기능은 제공되어 있습니다.
4. /docs에서 아래 예상 결과와 실제 파일을 대조합니다.

```powershell
# 강사용 폴더에서 시작한 경우
cd ".\03_심화\07_project"
python -m uvicorn app.main:app --reload
```

브라우저: `http://127.0.0.1:8000/docs` · 첫 확인: `http://127.0.0.1:8000/health`

활성화를 하지 않았다면 현재 교시 폴더에서 다음처럼 같은 가상환경 Python을 직접 사용합니다.

```powershell
..\..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

심화의 app.main:app 실행에서도 app 폴더 안으로 cd하지 않습니다. 새로운 교시로 이동할 때 이전 서버는 반드시 종료합니다.

## 완성할 부분

| TODO ID | 파일 | 완료 요구사항 |
|---|---|---|
| H07-01 | `app/repositories/json_knowledge.py` | 생성 데이터와 next_id를 파일에 저장하는 연결을 완성하세요. |
| H07-02 | `app/routers/knowledge.py` | Repository 삭제가 성공한 경우 빈 204 응답을 반환하세요. |
| H07-03 | `tests/test_api.py` | 잘못된 입력이 422이며 저장 파일을 바꾸지 않는지 검사하세요. |
| H07-04 | `tests/test_api.py` | 없는 category를 조회한 목록이 200과 빈 배열인지 검사하세요. |

## 요청·응답·저장 확인

1. GET /health → 200, {"status":"ok"}
2. GET /docs → 200인 문서 화면. 실행 결과는 Server response에서 읽습니다.
3. 초기 파일: next_id=4, entries 3건 (ID 1·2·3). 이 폴더에서 이미 변경했다면 실제 상태를 먼저 확인합니다.
4. GET /api/knowledge → 200, entries 배열만 반환. GET /api/knowledge/2 → title=서버 실행.
5. GET /api/knowledge/9999 → 404, detail=Knowledge not found. GET /api/knowledge/foo → 422. GET 전후 파일은 변하지 않습니다.
6. category=api → 초기 ID 2·3, category=setup → 초기 ID 1, category=unknown → 200과 []. 생략은 전체입니다.
7. 정상 POST → 201. 초기 상태에서 첫 생성 ID는 4이며 entries=4건·next_id=5입니다. 실제 응답 ID로 재조회합니다.
8. 빈 content·필수값 누락·길이 초과 POST → 422, entries와 next_id 불변. 422 문구 전체는 버전별로 다를 수 있습니다.
9. PUT은 title·content·category를 모두 보냅니다. 정상 200·같은 ID·같은 개수·같은 next_id. 존재하지 않는 ID는 404, content만 보내면 422.
10. DELETE 정상 → 204와 빈 본문. 같은 ID GET/DELETE → 404. 나머지 지식과 next_id는 유지됩니다.


## 자동 검사 (선택한 심화 수준의 과제)

가상환경에 requirements-test.txt의 패키지를 설치한 뒤, 현재 프로젝트 루트에서 실행합니다.

```powershell
python -m pytest -q tests/test_api.py
```

conftest.py가 각 테스트마다 임시 파일을 새로 만들고 DATA만 바꿉니다. 실제 data/knowledge.json을 건드리지 않습니다.
정답이 미완성이면 테스트가 실패하는 것이 정상입니다. 테스트를 지우거나 assert를 pass로 바꾸지 마세요.

8교시가 되면 tests/test_daily_project.py의 H08-01~03을 완성합니다. 7교시는 위 test_api.py만 실행하며, 일일프로젝트 이후 `python -m pytest -q`로 전체를 확인합니다.

## 다음 교시

실습07_기록.md에 강사 예시 결과를 적고, 일일프로젝트_기록.md는 8교시에 작성합니다. 08_daily_project/README.md의 안내를 읽은 뒤 이 프로젝트를 계속 사용하세요. 데이터를 초기화하지 않습니다.


## 완료 기준과 주의

요청 Method·Path·Body·상태코드와 파일의 변화를 설명할 수 있어야 합니다. 코드가 실행된다는 이유만으로 정답은 아닙니다.
이 교시의 저장 파일은 이 폴더의 data/knowledge.json이며, 다른 교시와 공유하지 않습니다. 01에는 저장 파일이 없습니다.
파일 처리·잠금·초기화 도구는 제공 코드입니다. 내부를 모두 새로 구현하는 과제가 아닙니다.
/health는 경로 응답 확인일 뿐 AI 모델·DB 준비 상태를 확인하지 않습니다. 인증·DB·LLM 호출은 오늘 추가하지 않습니다.

## 일일프로젝트 기록 (README의 이어지는 부분)

[일일프로젝트 실행 기록](일일프로젝트_기록.md)을 작성하고 이 README와 함께 제출합니다.
읽기 쉽게 분리한 짧은 기록 틀이며 별도 장문 보고서가 아닙니다. 제출할 때 README에 합쳐도 됩니다.
