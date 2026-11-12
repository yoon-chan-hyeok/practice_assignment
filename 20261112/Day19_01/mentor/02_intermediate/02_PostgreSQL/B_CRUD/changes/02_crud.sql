-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_a, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE C01
-- 1. BEGIN만 선택하여 실행합니다.
BEGIN;
-- 2. 아래 INSERT ... RETURNING만 실행하고 실제 ID를 기록합니다.
-- BEGIN A-SQL-08
-- 해설 A-SQL-08: title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인
-- 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. ID는 제목이나 목록
-- 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('보충 학습','복습 자료는 개인 폴더에서 확인합니다.',1)
RETURNING id,title,category_id;
-- END A-SQL-08
-- 3. COMMIT만 실행한 뒤 다음 SELECT를 따로 실행합니다.
COMMIT;
SELECT COUNT(*) AS knowledge_count FROM public.knowledge;
-- ENDCASE C01

-- CASE U01
BEGIN;
-- BEGIN A-SQL-09
-- 해설 A-SQL-09: C01의 실제 __NEW_ID__ 행만 content='복습 자료와 예제 코드를 함께 확인합니다.'로
-- UPDATE하고 id·content를 RETURNING하세요. 뒤의 ROLLBACK 후 원문이 남아야 합니다. ID는 제목이나 목록
-- 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END A-SQL-09
ROLLBACK;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U01

-- CASE U02
BEGIN;
-- BEGIN A-SQL-10
-- 해설 A-SQL-10: C01의 실제 __NEW_ID__ 행에 같은 본문 수정을 실행하세요. 뒤의 COMMIT 후 변경한 본문이 남아야
-- 합니다. ID는 제목이나 목록 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
UPDATE public.knowledge SET content='복습 자료와 예제 코드를 함께 확인합니다.'
WHERE id=__NEW_ID__ RETURNING id,content;
-- END A-SQL-10
COMMIT;
SELECT id,content FROM public.knowledge WHERE id=__NEW_ID__;
-- ENDCASE U02

-- CASE D01
BEGIN;
-- BEGIN A-SQL-11
-- 해설 A-SQL-11: C01에서 만든 실제 __NEW_ID__ 행만 DELETE하고 id를 RETURNING하세요. COMMIT 뒤
-- 원래 지식 3건이 모두 그대로 남아야 합니다. ID는 제목이나 목록 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
DELETE FROM public.knowledge WHERE id=__NEW_ID__ RETURNING id;
-- END A-SQL-11
COMMIT;
SELECT id FROM public.knowledge WHERE id=__NEW_ID__;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE D01
