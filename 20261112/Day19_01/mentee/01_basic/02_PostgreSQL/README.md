# 실습 2 · 기본필수 PostgreSQL 구축·CRUD

이 실습은 **A: ERD·명세서로 DB 구축**, **B: 완성된 DB에서 SQL 작성**의 두 부분입니다.
**A가 미완성이어도 B를 진행할 수 있습니다.** A의 테이블을 B의 시작점으로 쓰지 않습니다.

| 구분 | 전용 DB | 시작 상태 | 할 일 |
|---|---|---|---|
| A 구축 | `day19_build_b` | 빈 개인 DB | DDL TODO 4개 |
| B CRUD | `day19_crud_b` | 제공 복원 SQL로 만든 완성 DB | SQL TODO 8개 |

전날의 `knowledge_lab`과 다른 DB입니다. **기존 DB를 초기화·삭제하거나 기존 자료에 덮어쓰지 않습니다.**
오전에는 드라이버·ORM·FastAPI 연동을 사용하지 않습니다. Python 없이 pgAdmin Query Tool로 수행할 수 있습니다.

## 준비
PostgreSQL 설치·접속은 전날 정상 환경을 재사용합니다. pgAdmin에서 두 DB를 만들거나 `00_접속준비.sql`의 CREATE DATABASE를 한 문장씩 실행합니다.
CREATE DATABASE는 트랜잭션 밖에서 실행하며, 기존 DB가 있다면 내용을 먼저 확인합니다.
권한이 없으면 강사의 사전 준비가 필요합니다. 비밀번호나 보안 정책을 바꾸는 것을 과제로 삼지 않습니다.

**각 DB의 Query Tool을 따로 열고 `SELECT current_database();`로 실행 대상을 확인합니다.**
DB 생성·전환은 준비 절차이며 API와 DB를 비교하는 별도 과제가 아닙니다.

## A · 구축 순서
[ERD·스키마 명세서](스키마명세서.md)를 보고 아래 파일을 완성·실행합니다.
1. `A_구축/build.sql`

파일의 제공 안전장치와 BEGIN/COMMIT은 유지합니다. 구문 오류가 나면 ROLLBACK 후 미완성 부분을 고쳐 해당 파일을 다시 실행합니다.
이미 성공한 CREATE 파일은 반복하지 않습니다. 완료 후 `A_구축/check_structure.sql`과 `check_insert.sql`로 확인합니다.

## B · 완성 DB에서 CRUD
`day19_crud_b` Query Tool에서 **`B_CRUD/00_ready_database.sql`을 새 빈 DB에 한 번 실행**합니다.
이 파일은 DDL과 데이터를 모두 갖춘 완성 DB의 복원용 SQL이며 **수강생이 완성할 과제가 아닙니다.** 이미 만들어진 표가 있으면 중단하고 상태를 확인합니다.

초기 상태 S0는 분류3·지식3입니다. [SQL 문제와 예상 결과](CRUD_명세와_예상결과.md)에 실제 표와 실행 순서가 있습니다.
완성 DB 준비 SQL이 A 과제의 답을 포함할 수 있으므로, A는 먼저 명세로 직접 작성하고 막힌 경우 참고자료로 사용합니다.

**B 문제 파일 전체를 한 번에 실행하지 않습니다.** 조회 R은 CASE 한 개씩 실행합니다. 변경 C/U/D는 CASE 안에서도 **BEGIN → 변경문 RETURNING → 결과 확인 → COMMIT/ROLLBACK → 후속 SELECT**를 각각 선택·실행합니다. 한 번에 실행하면 pgAdmin 화면에 마지막 결과만 보여 생성 ID를 놓칠 수 있습니다.
초기 조회 R 문제 → C01 생성 → U01 취소 → U02 확정 → D01 삭제 → 오류 E 문제 순서입니다.
`__NEW_ID__`는 C01의 RETURNING에서 받은 실제 정수로 치환합니다. 이 표시는 강사용에도 남는 실행 입력값입니다.

| 상황 | 진행 방법 |
|---|---|
| A 구축이 막힘 | A를 남겨두고 B 완성 DB로 이동 가능 |
| BEGIN 뒤 오류 | 같은 Query Tool에서 ROLLBACK만 먼저 실행 |
| INSERT 0행 | 부모 분류·조건·현재 DB 확인 |
| 결과가 다른 경우 | 문제의 시작 상태와 실행 순서·WHERE·ORDER BY 확인 |
| B 전체를 처음부터 다시 연습 | 정상 완료 후 지식 데이터는 S0로 돌아옵니다. ID 번호는 건너뛸 수 있으므로 새 RETURNING을 사용 |

새 접속·DB 비교·장문 보고서의 별도 과제는 없습니다. 명세별 결과가 맞으면 해당 문제를 완료합니다.
