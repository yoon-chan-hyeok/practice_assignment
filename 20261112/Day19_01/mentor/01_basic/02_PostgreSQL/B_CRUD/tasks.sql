-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_b' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_b, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE R01
-- BEGIN B-SQL-01
-- 해설 B-SQL-01: 초기 S0에서 id·title만 id 오름차순으로 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를
-- 고정합니다.
SELECT id, title FROM public.knowledge ORDER BY id;
-- END B-SQL-01
-- ENDCASE R01

-- CASE R02
-- BEGIN B-SQL-02
-- 해설 B-SQL-02: ID 2의 id·title·content·category_id를 조회하세요. 빈 결과도 정상이며, ORDER
-- BY로 결과 순서를 고정합니다.
SELECT id, title, content, category_id FROM public.knowledge WHERE id = 2;
-- END B-SQL-02
-- ENDCASE R02

-- CASE R03
-- BEGIN B-SQL-03
-- 해설 B-SQL-03: knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id
-- 오름차순으로 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를 고정합니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;
-- END B-SQL-03
-- ENDCASE R03

-- CASE R04
-- BEGIN B-SQL-04
-- 해설 B-SQL-04: LEFT JOIN은 지식이 없는 reference 분류도 남깁니다. COUNT(k.id)는 NULL을 제외하므로
-- 0이고 COUNT(*)는 바깥 조인 행 자체를 세어 1이 됩니다.
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.id;
-- END B-SQL-04
-- ENDCASE R04

-- CASE C01
-- 1. BEGIN만 선택하여 실행합니다.
BEGIN;
-- 2. 아래 INSERT ... RETURNING만 실행하고 실제 ID를 기록합니다.
-- BEGIN B-SQL-05
-- 해설 B-SQL-05: title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인
-- 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. ID는 제목이나 목록
-- 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('보충 학습','복습 자료는 개인 폴더에서 확인합니다.',1)
RETURNING id,title,category_id;
-- END B-SQL-05
-- 3. COMMIT만 실행한 뒤 다음 SELECT를 따로 실행합니다.
COMMIT;
SELECT COUNT(*) AS knowledge_count FROM public.knowledge;
-- ENDCASE C01

-- CASE U01
BEGIN;
-- BEGIN B-SQL-06
-- 해설 B-SQL-06: C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로
-- UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다. ID는 제목이나 목록
-- 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END B-SQL-06
ROLLBACK;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U01

-- CASE U02
BEGIN;
-- BEGIN B-SQL-07
-- 해설 B-SQL-07: C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야
-- 합니다. ID는 제목이나 목록 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END B-SQL-07
COMMIT;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U02

-- CASE D01
BEGIN;
-- BEGIN B-SQL-08
-- 해설 B-SQL-08: C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤
-- 원래 지식 3건이 모두 그대로 남아야 합니다. ID는 제목이나 목록 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
DELETE FROM public.knowledge WHERE id=__NEW_ID__ RETURNING id;
-- END B-SQL-08
COMMIT;
SELECT id FROM public.knowledge WHERE id=__NEW_ID__;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE D01
