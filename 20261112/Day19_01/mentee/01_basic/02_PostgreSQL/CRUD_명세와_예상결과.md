# 실습 2B · 기본필수 SQL 문제와 예상 결과

## 시작 데이터 S0
DB는 `day19_crud_b`, Schema는 public입니다. `B_CRUD/00_ready_database.sql`을 새 빈 DB에 성공적으로 한 번 실행한 상태입니다.

### categories
| id | name |
|---|---|
| 1 | learning |
| 2 | environment |
| 3 | reference |

### knowledge
| id | title | content | category_id |
|---|---|---|---|
| 1 | 실습 파일 보관 | 실습 파일은 개인 폴더에 보관합니다. | 1 |
| 2 | 서버 실행 | 프로젝트 폴더에서 서버를 실행합니다. | 2 |
| 3 | 질문 작성 | 오류 메시지와 시도한 작업을 함께 적습니다. | 1 |

초기 ID는 위 복원 SQL의 정상 완료 상태에서만 고정됩니다. 수정·삭제는 문제에서 지정한 ID에만 수행합니다.
각 CASE의 `__TODO_...__`는 코드 미완성 표식이고, `__NEW_ID__`는 실행 후 채울 실제 ID입니다. 문법 오류를 CHECK·FK 성공 증거로 세지 않습니다.

## 1. 조회 문제 · 모두 S0 기준

### R01 · 전체 지식 목록
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-01`

**요구사항:** 초기 S0에서 id·title만 id 오름차순으로 조회하세요.

**예상 결과:**
| id | title |
|---|---|
| 1 | 실습 파일 보관 |
| 2 | 서버 실행 |
| 3 | 질문 작성 |

[ ] 열 이름·값·행 수·정렬 순서 일치

### R02 · 상세 조회
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-02`

**요구사항:** ID 2의 id·title·content·category_id를 조회하세요.

**예상 결과:**
| id | title | content | category_id |
|---|---|---|---|
| 2 | 서버 실행 | 프로젝트 폴더에서 서버를 실행합니다. | 2 |

[ ] 열 이름·값·행 수·정렬 순서 일치

### R03 · 분류명 JOIN
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-03`

**요구사항:** knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id 오름차순으로 조회하세요.

**예상 결과:**
| id | title | category |
|---|---|---|
| 1 | 실습 파일 보관 | learning |
| 2 | 서버 실행 | environment |
| 3 | 질문 작성 | learning |

[ ] 열 이름·값·행 수·정렬 순서 일치

### R04 · 빈 분류 포함 집계
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-04`

**요구사항:** 분류를 왼쪽에 두고 모든 분류명과 지식 수(knowledge_count)를 분류 id 순으로 조회하세요. reference는 0이어야 합니다.

**예상 결과:**
| category | knowledge_count |
|---|---|
| learning | 2 |
| environment | 1 |
| reference | 0 |

[ ] 열 이름·값·행 수·정렬 순서 일치

## 2. 변경 문제 · C01 → U01 → U02 → D01
각 단계는 같은 Query Tool에서 실행하되 **BEGIN, 변경문(RETURNING 포함), COMMIT 또는 ROLLBACK, 후속 SELECT를 각각 따로 선택·실행**합니다. 변경문의 RETURNING 결과를 확인한 후 종료문으로 이동하세요. 특히 C01의 INSERT 결과 ID를 기록하기 전에 다른 SELECT를 실행하지 않습니다.
처음 C01에서 반환받은 ID를 나머지 `__NEW_ID__` 위치에 넣습니다. **4라는 번호를 정답으로 고정하지 않습니다.**

### C01 · 새 지식 생성
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-05`

**요구사항:** title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다.

**변경문 RETURNING 예상:**
| id | title | category_id |
|---|---|---|
| 실제 NEW_ID | 보충 학습 | 1 |

**종료 후 확인:** COMMIT 뒤 knowledge_count=4. 기존 1~3의 모든 값은 동일합니다.

[ ] 실제 ID 사용  [ ] 변경 1행  [ ] 종료 후 데이터 일치

### U01 · 수정 후 취소
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-06`

**요구사항:** C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로 UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다.

**변경문 RETURNING 예상:**
| id | content |
|---|---|
| 실제 NEW_ID | 복습 자료와 예제 코드를 함께 확인합니다. |

**종료 후 확인:** UPDATE의 RETURNING은 위 새 본문입니다. ROLLBACK 후 SELECT는 `복습 자료는 개인 폴더에서 확인합니다.`로 돌아오고 총 4행입니다.

[ ] 실제 ID 사용  [ ] 변경 1행  [ ] 종료 후 데이터 일치

### U02 · 수정 후 확정
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-07`

**요구사항:** C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야 합니다.

**변경문 RETURNING 예상:**
| id | content |
|---|---|
| 실제 NEW_ID | 복습 자료와 예제 코드를 함께 확인합니다. |

**종료 후 확인:** COMMIT 뒤 SELECT도 위 새 본문입니다. ID·전체 4행·기존 1~3은 유지됩니다.

[ ] 실제 ID 사용  [ ] 변경 1행  [ ] 종료 후 데이터 일치

### D01 · 새 행 삭제
**구현 위치:** `B_CRUD/tasks.sql`의 `B-SQL-08`

**요구사항:** C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤 원래 지식 3건이 모두 그대로 남아야 합니다.

**변경문 RETURNING 예상:**
| id |
|---|
| 실제 NEW_ID |

**종료 후 확인:** DELETE RETURNING은 위 1행, COMMIT 뒤 같은 ID 조회는 0행입니다. 최종 지식은 S0의 세 행과 완전히 같습니다.

[ ] 실제 ID 사용  [ ] 변경 1행  [ ] 종료 후 데이터 일치

## 3. 제공된 실패 요청 확인 · D01 뒤 수행
이 구간은 완성 SQL을 제공합니다. **구현 TODO가 아니라 선언한 규칙을 실제로 확인하는 문제**입니다.
`B_CRUD/errors.sql`에서 CASE E01, E02 등을 각각 실행하고, 오류를 읽은 뒤 대응하는 RECOVER 구간을 **따로 선택·실행**합니다.

- **E01 빈 본문 CHECK:** SQLSTATE `23514`, 제약조건 `knowledge_content_length` 확인 → ROLLBACK → 지식의 기존 세 행 내용 그대로.

- **E02 없는 분류 FK:** SQLSTATE `23503`, 제약조건 `knowledge_category_fk` 확인 → ROLLBACK → 지식의 기존 세 행 내용 그대로.

SQLSTATE 42601(문법 오류), 42P01(표 없음), 25P02(실패한 트랜잭션 상태)는 위 기대 제약 위반의 정답이 아닙니다.
실패 후 IDENTITY의 다음 번호는 비교하지 않습니다. 실패·취소가 ID 번호까지 원복한다는 조건은 없습니다.

## 최종 확인
`SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;` 결과는 시작 S0의 세 행과 같아야 합니다.
분류별 COUNT(k.id) 결과도 learning2·environment1·reference0입니다.
실행 결과가 맞는지 각 문제 옆에서 확인하면 충분하며 별도 비교표나 긴 보고서를 작성하지 않습니다.
