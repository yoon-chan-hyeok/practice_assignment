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

-- CASE C01
-- 1. BEGIN만 선택하여 실행합니다.
BEGIN;
-- 2. 아래 INSERT ... RETURNING만 실행하고 실제 ID를 기록합니다.
-- BEGIN H-SQL-10
-- 해설 H-SQL-10: title='보충 학습', content='복습 자료는 개인 폴더에서 확인합니다.', category_id=1인
-- 행을 INSERT하고 id·title·category_id를 RETURNING하세요. 실제 id를 기억합니다. ID는 제목이나 목록
-- 위치와 다릅니다. 영향받은 행 1건을 확인합니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES ('보충 학습','복습 자료는 개인 폴더에서 확인합니다.',1)
RETURNING id,title,category_id;
-- END H-SQL-10
-- 3. COMMIT만 실행한 뒤 다음 SELECT를 따로 실행합니다.
COMMIT;
SELECT COUNT(*) AS knowledge_count FROM public.knowledge;
-- ENDCASE C01
