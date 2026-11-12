# 검수 도구 사용법 — 강사용 선택 도구

## 현재 제작 환경의 한계
실제 PostgreSQL 실행 파일이 없어 DB 실행 검수는 하지 못했습니다.
`verify_package.py`와 `test_tools.py`는 정적/보조 코드 검수이지 PostgreSQL 엔진 테스트가 아닙니다.
`verify_postgres.py --emit-only`도 검수 스크립트 생성일 뿐 실행 성공을 의미하지 않습니다.

## 수업 전 실제 PostgreSQL 검수
개인 강사 PC에 PostgreSQL 18 서버와 psql, 기존 Python이 필요합니다. 추가 pip 패키지는 필요 없습니다.
강사용 폴더를 현재 작업 폴더로 엽니다. DB 생성 권한이 있는 계정을 이용합니다.
비밀번호를 명령줄·소스·보고서에 쓰지 않습니다. `--password-prompt`는 숨김 입력을 받아 자식 프로세스에만 전달합니다.

```powershell
python .\운영\verify_postgres.py --run --host localhost --port 5432 --user postgres --password-prompt --cleanup
```

psql이 PATH에 없다면 실제 설치 경로를 지정합니다.

```powershell
python .\운영\verify_postgres.py --run --psql "C:\Program Files\PostgreSQL\18\bin\psql.exe" --password-prompt --cleanup
```

**서버 접근과 DB 생성은 `--run`을 붙였을 때만 수행합니다.** 기본 동작은 emit-only입니다.
검수 도구는 `knowledge_lab_verify_무작위이름`의 새 DB를 단계별로 만들고 공통 준비·과제 SQL을 실행합니다.
수업용 `knowledge_lab`이나 기존 DB를 DROP/초기화하지 않습니다. `--cleanup`은 이 실행이 직접 생성에 성공한
검수 DB만 삭제합니다. 생략하면 검수 DB를 남겨 조사할 수 있습니다.

생성된 `day18_verification/report.json`의 전체 status와 수준별 status가 모두 passed인지 확인합니다.
실패·연결 불가·미실행은 passed로 처리하지 않습니다. 실제 서버 버전, SQLSTATE 대조, 행 보존 검사와 로그가 남습니다.
stderr에는 의도한 실패 SQL의 오류도 있을 수 있습니다. 무조건 비었다는 기준 대신 기대 SQLSTATE를 대조합니다.

## 실제로 검사하도록 구성한 내용
- 초기 두 표·3/3행·본문 길이64, SELECT·JOIN·집계 결과의 중복을 포함한 대조.
- _try 생성 취소와 01~06의 기존 지식·분류 보존.
- 기대한 CHECK/FK/NOT NULL/UNIQUE/트랜잭션 중단 SQLSTATE인지 확인.
- 07 취소·확정과 **새 연결**, 응용 두 변경 취소, 심화 원자성.
- 08 전용 기존 행을 한 건 더 둬 N을 3으로 고정한 오류를 탐지. 실제 수업 데이터에는 추가하지 않음.
- A 보존·B 수정·C 삭제, 기존 모든 행·분류 보존, 실제 N+3/N+2, 집계 합계.
- 세 번의 새 연결(07 한 번, 08 두 번). 서버 강제 종료/장애 시험은 하지 않음.

실제 ID는 psql 변수로 받아 자동 전달합니다. 이 보조 자동화는 학생의 pgAdmin 수동 입력 과제를 대체하지 않습니다.
원본 .sql에는 psql 메타 명령을 섞지 않았고, 생성된 .psql만 psql에서 실행합니다.

## DB 없이 실행하는 도구 검수
```powershell
python .\운영\verify_package.py --output static_report.json
python .\운영\test_tools.py
python .\운영\verify_postgres.py --emit-only --output emitted
```

정답 대입 대응 검사는 통합본에서 강사용·수강생용이 나란히 있을 때 27개 과제 SQL을 비교합니다.
강사용만 받았다면 대응 파일 비교는 생략되며 paired_sql_files가 0으로 기록됩니다.
도구 문법 검수는 Python 3.10 이상 문법을 사용합니다. 기본 SQL 학습에는 Python 실행이 필수가 아닙니다.
