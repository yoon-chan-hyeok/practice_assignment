-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_h, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE R01
-- BEGIN H-SQL-01
-- TODO H-SQL-01: 초기 S0에서 id·title만 id 오름차순으로 조회하세요.
-- 전체 지식 목록 SQL을 작성하세요.
__TODO_H_SQL_01__;
-- END H-SQL-01
-- ENDCASE R01

-- CASE R02
-- BEGIN H-SQL-02
-- TODO H-SQL-02: ID 2의 id·title·content·category_id를 조회하세요.
-- 상세 조회 SQL을 작성하세요.
__TODO_H_SQL_02__;
-- END H-SQL-02
-- ENDCASE R02

-- CASE R03
-- BEGIN H-SQL-03
-- TODO H-SQL-03: knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id
-- 오름차순으로 조회하세요.
-- 분류명 JOIN SQL을 작성하세요.
__TODO_H_SQL_03__;
-- END H-SQL-03
-- ENDCASE R03

-- CASE R04
-- BEGIN H-SQL-04
-- TODO H-SQL-04: 분류를 왼쪽에 두고 모든 분류명과 지식 수(knowledge_count)를 분류 id 순으로 조회하세요.
-- reference는 0이어야 합니다.
-- 빈 분류 포함 집계 SQL을 작성하세요.
__TODO_H_SQL_04__;
-- END H-SQL-04
-- ENDCASE R04

-- CASE R05
-- BEGIN H-SQL-05
-- TODO H-SQL-05: 분류가 learning이면서 제목에 실습이 포함된 지식의 id·title·분류명(category)을 id
-- 순으로 조회하세요.
-- 조건 조합 SQL을 작성하세요.
__TODO_H_SQL_05__;
-- END H-SQL-05
-- ENDCASE R05

-- CASE R06
-- BEGIN H-SQL-06
-- TODO H-SQL-06: 분류가 reference인 지식의 id·title을 id 순으로 조회하세요. 분류는 있지만 지식이 없으므로
-- 0행입니다.
-- 빈 결과 SQL을 작성하세요.
__TODO_H_SQL_06__;
-- END H-SQL-06
-- ENDCASE R06

-- CASE R07
-- BEGIN H-SQL-07
-- TODO H-SQL-07: 분류별 지식 수를 구한 뒤 2건 이상인 분류명(category)과 개수(knowledge_count)만 분류
-- id 순으로 조회하세요.
-- 그룹 조건 SQL을 작성하세요.
__TODO_H_SQL_07__;
-- END H-SQL-07
-- ENDCASE R07

-- CASE R08
-- BEGIN H-SQL-08
-- TODO H-SQL-08: LEFT JOIN과 IS NULL로 지식이 없는 분류의 id와 name을 분류 id 순으로 조회하세요.
-- 자식 없는 부모 SQL을 작성하세요.
__TODO_H_SQL_08__;
-- END H-SQL-08
-- ENDCASE R08

-- CASE R09
-- BEGIN H-SQL-09
-- TODO H-SQL-09: 각 지식의 id와 본문 글자 수(content_length)를 id 오름차순으로 조회하세요.
-- 문자열 길이 조회 SQL을 작성하세요.
__TODO_H_SQL_09__;
-- END H-SQL-09
-- ENDCASE R09
