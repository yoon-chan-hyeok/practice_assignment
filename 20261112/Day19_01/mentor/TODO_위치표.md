# TODO 위치와 요구사항

| ID | 파일 | 요구사항 |
|---|---|---|
| B-API-01 | `01_기본필수/01_FastAPI/main.py` | data의 entries를 id 오름차순으로 반환하세요. sorted(..., key=lambda e: e["id"])를 사용할 수 있습니다. next_id는 응답하지 않습니다. |
| B-API-02 | `01_기본필수/01_FastAPI/main.py` | 반복 중인 entry의 id가 knowledge_id와 같을 때 entry를 반환하세요. 목록 인덱스와 ID를 혼동하지 마세요. |
| B-API-03 | `01_기본필수/01_FastAPI/main.py` | payload를 dict로 변환하여 entry에 넣고, data의 next_id 값을 entry의 id로 넣으세요. |
| B-API-04 | `01_기본필수/01_FastAPI/main.py` | entry를 entries에 추가하고 next_id를 1 늘린 뒤 write_data(data)로 저장하세요. |
| B-API-05 | `01_기본필수/01_FastAPI/main.py` | 찾은 위치 i의 항목을 updated로 교체한 뒤 저장하세요. 같은 ID를 유지하고 다른 항목은 변경하지 않습니다. |
| B-API-06 | `01_기본필수/01_FastAPI/main.py` | 찾은 위치 i의 항목 하나만 삭제하고 저장하세요. next_id는 줄이지 않습니다. |
| B-DDL-01 | `01_기본필수/02_PostgreSQL/A_구축/build.sql` | categories의 id를 BIGINT 자동 생성 IDENTITY와 PRIMARY KEY로 선언하세요. 쉼표까지 포함합니다. |
| B-DDL-02 | `01_기본필수/02_PostgreSQL/A_구축/build.sql` | categories.name의 1~30자 길이 CHECK를 categories_name_length라는 이름으로 완성하세요. |
| B-DDL-03 | `01_기본필수/02_PostgreSQL/A_구축/build.sql` | title은 1~80자, content는 1~2000자인 두 CHECK를 명세의 이름으로 완성하세요. 각 줄 끝 쉼표가 필요합니다. |
| B-DDL-04 | `01_기본필수/02_PostgreSQL/A_구축/build.sql` | category_id가 public.categories(id)를 참조하도록 REFERENCES와 부모 삭제 RESTRICT를 완성하세요. |
| B-SQL-01 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | 초기 S0에서 id·title만 id 오름차순으로 조회하세요. |
| B-SQL-02 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | ID 2의 id·title·content·category_id를 조회하세요. |
| B-SQL-03 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id 오름차순으로 조회하세요. |
| B-SQL-04 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | 분류를 왼쪽에 두고 모든 분류명과 지식 수(knowledge_count)를 분류 id 순으로 조회하세요. reference는 0이어야 합니다. |
| B-SQL-05 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. |
| B-SQL-06 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로 UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다. |
| B-SQL-07 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야 합니다. |
| B-SQL-08 | `01_기본필수/02_PostgreSQL/B_CRUD/tasks.sql` | C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤 원래 지식 3건이 모두 그대로 남아야 합니다. |
| A-API-03 | `02_응용/01_FastAPI/main.py` | read_data()의 entries와 category를 filter_entries에 전달하여 결과를 반환하세요. |
| A-API-04 | `02_응용/01_FastAPI/main.py` | find_entry에 data의 entries와 knowledge_id를 전달해 entry를 구하세요. |
| A-API-05 | `02_응용/01_FastAPI/main.py` | entry가 None이면 HTTPException(404, "Knowledge not found")을 raise하고, 있으면 반환하세요. |
| A-API-06 | `02_응용/01_FastAPI/main.py` | payload를 dict로 변환하고 next_id를 id로 부여한 entry를 만드세요. |
| A-API-07 | `02_응용/01_FastAPI/main.py` | entry를 추가하고 next_id를 증가시킨 뒤 파일에 저장하세요. |
| A-API-08 | `02_응용/01_FastAPI/main.py` | 같은 ID의 항목만 입력 세 필드로 교체하고 저장·반환하세요. 끝까지 없으면 잠금 블록 밖의 404로 진행합니다. |
| A-API-09 | `02_응용/01_FastAPI/main.py` | 같은 ID의 항목 하나만 삭제·저장한 뒤 Response(status_code=204)를 반환하세요. 없으면 이후 404로 진행합니다. |
| A-API-01 | `02_응용/01_FastAPI/queries.py` | category가 None이 아닐 때만 entries를 분류 문자열의 완전 일치로 필터링하세요. 빈 문자열도 조건입니다. |
| A-API-02 | `02_응용/01_FastAPI/queries.py` | entries에서 id가 knowledge_id인 첫 항목을 반환하세요. 없으면 None을 반환하세요. |
| A-DDL-01 | `02_응용/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories.id를 BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY로 선언하세요. 쉼표를 포함합니다. |
| A-DDL-02 | `02_응용/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories.name을 VARCHAR(30), 필수, 중복 불가로 선언하세요. 쉼표를 포함합니다. |
| A-DDL-03 | `02_응용/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories_name_length CHECK로 name의 길이를 1~30자로 제한하세요. |
| A-DDL-04 | `02_응용/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge의 title VARCHAR(80), content TEXT, category_id BIGINT를 각각 NOT NULL로 선언하세요. 각 줄에 쉼표를 붙입니다. |
| A-DDL-05 | `02_응용/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge_title_length와 knowledge_content_length CHECK를 작성하세요. 각각 1~80자, 1~2000자이며 뒤에 쉼표를 붙입니다. |
| A-DDL-06 | `02_응용/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge_category_fk라는 FK로 category_id를 categories.id에 연결하고 ON DELETE RESTRICT를 설정하세요. |
| A-SQL-08 | `02_응용/02_PostgreSQL/B_CRUD/changes/02_crud.sql` | title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. |
| A-SQL-09 | `02_응용/02_PostgreSQL/B_CRUD/changes/02_crud.sql` | C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로 UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다. |
| A-SQL-10 | `02_응용/02_PostgreSQL/B_CRUD/changes/02_crud.sql` | C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야 합니다. |
| A-SQL-11 | `02_응용/02_PostgreSQL/B_CRUD/changes/02_crud.sql` | C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤 원래 지식 3건이 모두 그대로 남아야 합니다. |
| A-SQL-01 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 초기 S0에서 id·title만 id 오름차순으로 조회하세요. |
| A-SQL-02 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | ID 2의 id·title·content·category_id를 조회하세요. |
| A-SQL-03 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id 오름차순으로 조회하세요. |
| A-SQL-04 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류를 왼쪽에 두고 모든 분류명과 지식 수(knowledge_count)를 분류 id 순으로 조회하세요. reference는 0이어야 합니다. |
| A-SQL-05 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류가 learning이면서 제목에 실습이 포함된 지식의 id·title·분류명(category)을 id 순으로 조회하세요. |
| A-SQL-06 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류가 reference인 지식의 id·title을 id 순으로 조회하세요. 분류는 있지만 지식이 없으므로 0행입니다. |
| A-SQL-07 | `02_응용/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류별 지식 수를 구한 뒤 2건 이상인 분류명(category)과 개수(knowledge_count)만 분류 id 순으로 조회하세요. |
| H-API-01 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | category가 None이 아닐 때만 entries를 분류 완전 일치로 필터링하고 ID 오름차순 목록을 반환하세요. |
| H-API-02 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | 파일에서 읽은 entries에서 knowledge_id와 같은 id의 항목을 반환하고 없으면 None을 반환하세요. |
| H-API-03 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | fields를 복사해 entry를 만들고 next_id로 ID를 발급하세요. entries에 추가하고 next_id를 1 늘리세요. 아직 여기서는 저장하지 않습니다. |
| H-API-04 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | 변경된 data를 저장하고 entry를 반환하세요. 저장 실패를 성공 결과로 바꾸지 마세요. |
| H-API-05 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | 해당 ID가 있는 위치만 fields 복사본과 같은 ID로 교체·저장·반환하세요. 없으면 None을 반환하세요. |
| H-API-06 | `03_심화/01_FastAPI/app/repositories/json_knowledge.py` | 같은 ID가 있으면 그 항목만 삭제·저장하고 True, 없으면 False를 반환하세요. HTTP 상태코드는 여기에서 결정하지 않습니다. |
| H-API-07 | `03_심화/01_FastAPI/app/routers/knowledge.py` | entry가 None이면 404를 raise하고, 있으면 entry를 반환하세요. |
| H-API-08 | `03_심화/01_FastAPI/app/routers/knowledge.py` | payload.model_dump()를 repo.create에 전달하고 결과를 반환하세요. 201 선언과 파일 저장은 별개입니다. |
| H-API-09 | `03_심화/01_FastAPI/app/routers/knowledge.py` | repo.update에 ID와 입력 dict를 전달하세요. 결과가 None이면 404, 있으면 변경 결과를 반환하세요. |
| H-API-10 | `03_심화/01_FastAPI/app/routers/knowledge.py` | repo.delete가 False이면 404를 raise하고, True이면 본문이 없는 204를 반환하세요. |
| H-API-11 | `03_심화/01_FastAPI/tests/test_contract.py` | 빈 content 요청이 422인지 검사하고, 파일 bytes가 요청 전과 완전히 같은지 assert하세요. |
| H-API-12 | `03_심화/01_FastAPI/tests/test_contract.py` | 삭제 응답이204이고 빈 본문인지, 같은ID 상세 재조회가404인지 assert하세요. |
| H-DDL-09 | `03_심화/02_PostgreSQL/A_구축/indexes/03_category_index.sql` | idx_knowledge_category_id라는 비고유 B-tree 인덱스를 knowledge(category_id)에 만드세요. |
| H-DDL-01 | `03_심화/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories.id의 BIGINT·ALWAYS IDENTITY·PK를 선언하세요. |
| H-DDL-02 | `03_심화/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories.name의 VARCHAR(30)·NOT NULL·UNIQUE를 선언하세요. |
| H-DDL-03 | `03_심화/02_PostgreSQL/A_구축/schema/01_categories.sql` | categories_name_length CHECK를 작성하세요. |
| H-DDL-04 | `03_심화/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge.id의 BIGINT·ALWAYS IDENTITY·PK를 선언하세요. |
| H-DDL-05 | `03_심화/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | title VARCHAR(80), content TEXT, category_id BIGINT를 모두 필수 열로 선언하세요. |
| H-DDL-06 | `03_심화/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge_title_length라는 CHECK로 제목 길이 1~80자를 검사하세요. |
| H-DDL-07 | `03_심화/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge_content_length라는 CHECK로 본문 길이 1~2000자를 검사하세요. |
| H-DDL-08 | `03_심화/02_PostgreSQL/A_구축/schema/02_knowledge.sql` | knowledge_category_fk를 선언하여 필수 분류 참조와 RESTRICT를 구현하세요. |
| H-SQL-10 | `03_심화/02_PostgreSQL/B_CRUD/changes/02_create.sql` | title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. |
| H-SQL-13 | `03_심화/02_PostgreSQL/B_CRUD/changes/04_delete.sql` | C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤 원래 지식 3건이 모두 그대로 남아야 합니다. |
| H-SQL-01 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 초기 S0에서 id·title만 id 오름차순으로 조회하세요. |
| H-SQL-02 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | ID 2의 id·title·content·category_id를 조회하세요. |
| H-SQL-03 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id 오름차순으로 조회하세요. |
| H-SQL-04 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류를 왼쪽에 두고 모든 분류명과 지식 수(knowledge_count)를 분류 id 순으로 조회하세요. reference는 0이어야 합니다. |
| H-SQL-05 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류가 learning이면서 제목에 실습이 포함된 지식의 id·title·분류명(category)을 id 순으로 조회하세요. |
| H-SQL-06 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류가 reference인 지식의 id·title을 id 순으로 조회하세요. 분류는 있지만 지식이 없으므로 0행입니다. |
| H-SQL-07 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 분류별 지식 수를 구한 뒤 2건 이상인 분류명(category)과 개수(knowledge_count)만 분류 id 순으로 조회하세요. |
| H-SQL-08 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | LEFT JOIN과 IS NULL로 지식이 없는 분류의 id와 name을 분류 id 순으로 조회하세요. |
| H-SQL-09 | `03_심화/02_PostgreSQL/B_CRUD/queries/01_reads.sql` | 각 지식의 id와 본문 글자 수(content_length)를 id 오름차순으로 조회하세요. |
| H-SQL-11 | `03_심화/02_PostgreSQL/B_CRUD/transactions/03_update.sql` | C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로 UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다. |
| H-SQL-12 | `03_심화/02_PostgreSQL/B_CRUD/transactions/03_update.sql` | C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야 합니다. |
| H-SQL-14 | `03_심화/02_PostgreSQL/B_CRUD/transactions/05_atomicity.sql` | 한 트랜잭션 안에서 ID 1·2의 본문을 각각 임시 내용 1·임시 내용 2로 바꾸세요. 제공된 ROLLBACK 뒤 두 원문이 모두 유지되어야 합니다. |
