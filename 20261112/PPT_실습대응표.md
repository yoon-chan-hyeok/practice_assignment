# PPT와 실습자료 대응표

기준: 업로드한 최신 PPT 91장. 각 실습의 번호·목표를 그대로 대응시켰습니다.

| 실습 | PPT 쪽 | 주제 | 기본필수 TODO | 응용 TODO | 심화 TODO | 특심화 TODO |
|---|---:|---|---:|---:|---:|---:|
| 01 | 14 | FastAPI–PostgreSQL 연결 지도 | 2 | 3 | 2 | 2 |
| 02 | 22 | Engine·Pool·Session 준비 | 2 | 3 | 3 | 3 |
| 03 | 32 | ORM Model·Session·조회 | 3 | 4 | 3 | 2 |
| 04 | 41 | ORM CRUD Route 구현 | 4 | 5 | 4 | 3 |
| 05 | 50 | Transaction·오류·Service 분리 | 3 | 4 | 3 | 3 |
| 06 | 60 | Alembic Migration | 2 | 3 | 4 | 3 |
| 07 | 69 | CRUD·DB 반영·오류 통합 테스트 | 4 | 5 | 3 | 3 |
| 08 | 77 | PostgreSQL 연동 FastAPI CRUD API 통합 | 5 | 6 | 4 | 2 |

## 실습 01 · FastAPI–PostgreSQL 연결 지도 · PPT 14쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | 연결 URL의 Driver·User·Host·Port·Database를 표시하고, 환경변수로 읽은 값을 출력한다. | [01_기본필수/실습01_DB연결지도](01_기본필수/실습01_DB연결지도/README.md) |
| 응용 | pgAdmin과 Python에서 같은 DB에 접속해 SELECT 1과 SELECT current_database()를 확인한다. | [02_응용/실습01_DB연결지도](02_응용/실습01_DB연결지도/README.md) |
| 심화 | Settings·Engine·연결 점검 코드를 파일로 분리하고 비밀번호 노출 없이 실패 원인을 기록한다. | [03_심화/실습01_DB연결지도](03_심화/실습01_DB연결지도/README.md) |
| 특심화 | 다중 환경(local·test·production)의 URL 규칙, Secret 주입, Pool·Timeout 정책을 설계하고 자동 점검을 작성한다. | [04_특심화/실습01_DB연결지도](04_특심화/실습01_DB연결지도/README.md) |

## 실습 02 · Engine·Pool·Session 준비 · PPT 22쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | Engine과 SessionLocal을 만들고 check_database.py에서 DB 이름과 사용자 정보를 출력한다. | [01_기본필수/실습02_Engine_Pool_Session](01_기본필수/실습02_Engine_Pool_Session/README.md) |
| 응용 | pool_pre_ping·echo 옵션을 바꾸어 Log 차이를 관찰하고 접속 오류 2가지를 해결 기록으로 남긴다. | [02_응용/실습02_Engine_Pool_Session](02_응용/실습02_Engine_Pool_Session/README.md) |
| 심화 | settings.py·engine.py·db.py로 책임을 나누고 Pool 상태·Timeout·환경별 URL을 점검한다. | [03_심화/실습02_Engine_Pool_Session](03_심화/실습02_Engine_Pool_Session/README.md) |
| 특심화 | 동기·비동기 Driver와 Pool 정책을 비교하고 장애·재연결·Secret 교체를 검증하는 Health Check를 구현한다. | [04_특심화/실습02_Engine_Pool_Session](04_특심화/실습02_Engine_Pool_Session/README.md) |

## 실습 03 · ORM Model·Session·조회 · PPT 32쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | Item ORM Model을 만들고 Session으로 목록 3건과 상세 1건을 조회한다. | [01_기본필수/실습03_ORM모델과조회](01_기본필수/실습03_ORM모델과조회/README.md) |
| 응용 | Category–Item FK·relationship을 추가하고 category 이름과 함께 조회한다. | [02_응용/실습03_ORM모델과조회](02_응용/실습03_ORM모델과조회/README.md) |
| 심화 | Repository 함수로 목록·상세·필터를 분리하고 Lazy load·JOIN query 횟수를 비교한다. | [03_심화/실습03_ORM모델과조회](03_심화/실습03_ORM모델과조회/README.md) |
| 특심화 | Identity map·Loader strategy·Transaction scope를 관찰하는 진단 도구와 Query 회귀 테스트를 작성한다. | [04_특심화/실습03_ORM모델과조회](04_특심화/실습03_ORM모델과조회/README.md) |

## 실습 04 · ORM CRUD Route 구현 · PPT 41쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | ItemCreate·ItemRead를 만들고 목록·상세·등록 Route를 구현해 200·201·404·422를 확인한다. | [01_기본필수/실습04_CRUD_API](01_기본필수/실습04_CRUD_API/README.md) |
| 응용 | ItemUpdate와 PATCH·DELETE를 추가하고 Category 필터·정렬·limit까지 연결한다. | [02_응용/실습04_CRUD_API](02_응용/실습04_CRUD_API/README.md) |
| 심화 | Router·Schema·Repository·Service로 분리하고 관계 조회·페이지 처리·응답 계약 테스트를 작성한다. | [03_심화/실습04_CRUD_API](03_심화/실습04_CRUD_API/README.md) |
| 특심화 | Optimistic concurrency·Soft delete·Idempotency·Bulk API를 포함한 실무형 CRUD 계약과 Race condition 테스트를 구현한다. | [04_특심화/실습04_CRUD_API](04_특심화/실습04_CRUD_API/README.md) |

## 실습 05 · Transaction·오류·Service 분리 · PPT 50쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | 중복 상품 이름에서 rollback하고 409 JSON을 반환한 뒤 정상 등록이 계속되는지 확인한다. | [01_기본필수/실습05_트랜잭션과오류처리](01_기본필수/실습05_트랜잭션과오류처리/README.md) |
| 응용 | FK·Check 오류와 재고 부족을 구분해 404·409·422 중 기준을 정하고 응답 표를 만든다. | [02_응용/실습05_트랜잭션과오류처리](02_응용/실습05_트랜잭션과오류처리/README.md) |
| 심화 | 주문·재고·상세 저장을 Service Transaction으로 묶고 실패 시 전체 rollback을 자동 검증한다. | [03_심화/실습05_트랜잭션과오류처리](03_심화/실습05_트랜잭션과오류처리/README.md) |
| 특심화 | 동시 재고 차감·Idempotency Key·Retry 정책·Structured Error를 구현하고 Race condition 테스트를 작성한다. | [04_특심화/실습05_트랜잭션과오류처리](04_특심화/실습05_트랜잭션과오류처리/README.md) |

## 실습 06 · Alembic Migration · PPT 60쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | Alembic을 초기화하고 items Table 생성 Revision을 만들고 upgrade head를 실행한다. | [01_기본필수/실습06_Alembic_Migration](01_기본필수/실습06_Alembic_Migration/README.md) |
| 응용 | description Column을 추가한 뒤 autogenerate 결과를 검토하고 upgrade·downgrade를 각각 확인한다. | [02_응용/실습06_Alembic_Migration](02_응용/실습06_Alembic_Migration/README.md) |
| 심화 | Category 관계·Index·Constraint 변경을 Revision으로 나누고 데이터 Backfill 순서를 보고서로 작성한다. | [03_심화/실습06_Alembic_Migration](03_심화/실습06_Alembic_Migration/README.md) |
| 특심화 | Zero-downtime Schema 변경·Revision branch·실패 복구·환경별 Drift 검사 Harness를 구현한다. | [04_특심화/실습06_Alembic_Migration](04_특심화/실습06_Alembic_Migration/README.md) |

## 실습 07 · CRUD·DB 반영·오류 통합 테스트 · PPT 69쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | Test DB를 만들고 등록·조회·수정·삭제 Test 4개에서 API 응답과 Row 상태를 확인한다. | [01_기본필수/실습07_API_DB_통합테스트](01_기본필수/실습07_API_DB_통합테스트/README.md) |
| 응용 | 중복·없는 ID·422·FK 오류 Test를 추가하고 각 Test 전후의 데이터 정리 방식을 기록한다. | [02_응용/실습07_API_DB_통합테스트](02_응용/실습07_API_DB_통합테스트/README.md) |
| 심화 | Migration 적용부터 TestClient·Repository·Service·DB까지 자동화하고 실패 원인을 구간별로 분리한다. | [03_심화/실습07_API_DB_통합테스트](03_심화/실습07_API_DB_통합테스트/README.md) |
| 특심화 | 병렬 Test·Transaction 격리·Container DB·Migration Drift·Contract Snapshot을 포함한 CI 검증 Suite를 구현한다. | [04_특심화/실습07_API_DB_통합테스트](04_특심화/실습07_API_DB_통합테스트/README.md) |

## 실습 08 · PostgreSQL 연동 FastAPI CRUD API 통합 · PPT 77쪽

| 난이도 | PPT의 요구사항 | 실습 폴더 |
|---|---|---|
| 기본필수 | 제공 골격에서 Item CRUD·Migration·DB 반영 Test를 완성하고 /docs에서 시연한다. | [01_기본필수/실습08_종합프로젝트](01_기본필수/실습08_종합프로젝트/README.md) |
| 응용 | Category 관계·검색·페이지 처리·409 오류를 추가하고 README만으로 짝이 실행하게 한다. | [02_응용/실습08_종합프로젝트](02_응용/실습08_종합프로젝트/README.md) |
| 심화 | Router·Service·Repository·Migration·Test DB 구조를 완성하고 Transaction 실패·복구를 보고서로 남긴다. | [03_심화/실습08_종합프로젝트](03_심화/실습08_종합프로젝트/README.md) |
| 특심화 | Versioned API·Idempotency·동시 재고·Container Test DB·CI Migration Drift까지 포함한 현장형 검증 Harness를 구현한다. | [04_특심화/실습08_종합프로젝트](04_특심화/실습08_종합프로젝트/README.md) |
