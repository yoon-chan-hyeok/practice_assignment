# Day18 · PostgreSQL·SQL·ERD 실습

실습환경 준비 :  
1. postgresql 다운로드 (18.6.x 버전으로 받아질거에요)
https://www.postgresql.org/download/windows/
2. 다운로드 완료 되면 설치! 비밀번호는 꼭 기억해주세요!  

2026년 11월 11일(수) / 생성형 AI·LLM 및 RAG 엔지니어링 2/18

전날의 상품 API가 메모리에만 저장하던 데이터를, 오늘은 **관계형 데이터베이스의 표와 관계**로 설계합니다. 오늘은 FastAPI와 DB를 연결하지 않습니다. Python ORM·Migration 라이브러리·배포까지 한꺼번에 배우지 않습니다.

## 먼저 한 단계만 선택하세요

| 단계 | 시작 문서 | TODO | 목표 |
|---|---|---:|---|
| 기본필수 | [기본필수 README](01_기본필수/README.md) | 9 | 제공된 구조에서 짧은 SQL과 ERD 관계 한 줄 |
| 응용 | [응용 README](02_응용/README.md) | 10 | 검색·정렬·조회 제한·집계·제약조건을 연결 |
| 심화 | [심화 README](03_심화/README.md) | 12 | 파일 역할 분리, 재고 이력·주문 합계·안전한 변경 |
| 특심화 | [특심화 README](04_특심화/README.md) | 10 | 동시 주문·멱등성·Migration·검증 계약 |

기본필수는 **평평한 8개 파일**, 응용은 **sql/와 outputs/**, 심화는 **역할별 SQL 프로젝트**, 특심화는 **Migration·운영·테스트**로 확장합니다. 폴더를 늘리는 이유는 실무에서 변경 범위와 검증 책임을 분리하기 위해서입니다.

강사용은 완성된 정답·해설이며 수강생용은 TODO 골격입니다. 수강생용의 `WHERE FALSE`, `0`, 주석 처리된 빈 부분은 **일단 실행 형태를 읽을 수 있게 둔 미완성 값**입니다. 오류 없이 끝나더라도 완료가 아닙니다. 요구사항의 열·행·수치·관계를 확인해야 합니다.

## 오늘의 공통 사례

`users → orders → order_items ← items ← categories`의 상품 주문 서비스입니다. 첫 세 상품은 PPT와 같은 Python Book(30000원), USB Hub(25000원), Notebook(5000원)입니다. 사용자와 주문은 수치 검산이 가능하도록 구성한 합성 seed입니다. `.test` 이메일은 수업용 가상 값입니다.

실습 01·02는 문서 작성·설치 활동이므로 별도 Python 파일을 만들지 않습니다. 03은 DBML, 04~08은 SQL입니다. 기본필수·응용·심화는 **Python 없이도** pgAdmin/psql/dbdiagram.io로 완료할 수 있습니다.

## 필수 운영 원칙

수업용 `day18_*` 데이터베이스만 사용합니다. 기존 데이터베이스를 지우는 명령은 포함하지 않습니다. 초기화 SQL은 한 번 실행하고, 쓰기 연습은 명시적 ROLLBACK으로 되돌립니다. 동시성·Migration 테스트는 **별도 새 검증 DB**에서 실행합니다. 비밀번호·운영 데이터·실제 고객 정보를 Git이나 dbdiagram.io에 올리지 않습니다.

학습 시간은 PPT의 8교시 순서를 따릅니다. 설명을 포함한 50분 수업에서 실습 01~02 각 20분, 03~07 각 25분, 08은 35분을 기준으로 합니다. 설치가 늦어지면 응용·심화를 서두르지 말고 기본필수의 연결·조회·JOIN까지 먼저 완료합니다.

> **검증 범위:** 이 패키지는 PostgreSQL 18용 SQL입니다. 제작 환경에서 PostgreSQL 서버 설치·실행은 불가능했습니다. 아래 수치 예상값은 동일 seed의 관계 연산을 Python/SQLite로 독립 검산한 결과이며, PostgreSQL 실행 로그가 아닙니다. 인덱스 계획·트랜잭션·잠금·SQLSTATE·DBML 웹 렌더링은 교실에서 별도로 확인해야 합니다. 검증 도구는 강사용에 포함되어 있습니다.

## 공식 참고자료

- [PostgreSQL Windows 다운로드](https://www.postgresql.org/download/windows/)
- [EDB Windows 설치 안내](https://www.enterprisedb.com/docs/supported-open-source/postgresql/installing/windows/)
- [PostgreSQL 18 입문](https://www.postgresql.org/docs/18/tutorial.html)
- [제약조건](https://www.postgresql.org/docs/18/ddl-constraints.html)
- [트랜잭션](https://www.postgresql.org/docs/18/tutorial-transactions.html)
- [EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html)
- [psql](https://www.postgresql.org/docs/18/app-psql.html)
- [pgAdmin Query Tool](https://www.pgadmin.org/docs/pgadmin4/latest/query_tool.html)
- [dbdiagram.io](https://dbdiagram.io/)
- [DBML 공식 문법](https://dbml.dbdiagram.io/docs/)

자료 작성 시 확인일: 2026-10-26. 수업 기준은 PostgreSQL **18 계열**이며, 설치 파일의 세부 버전·화면은 바뀔 수 있습니다. PostgreSQL 18 전용 신규 기능은 과제로 요구하지 않지만 다른 버전에서의 동작을 검증했다고 표시하지 않습니다.
