-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_a, got %', current_database();
    END IF;
END;
$guard$;
-- 전체 실행 금지. CASE E 하나씩 선택해 실행하고 오류 확인 뒤 바로 해당 ROLLBACK 구간만 별도로 실행합니다.
-- CASE E01
-- 기대 SQLSTATE 23514, constraint knowledge_content_length
BEGIN;
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 검사','',1);
-- ENDCASE E01
-- CASE RECOVER_E01
ROLLBACK;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE RECOVER_E01
-- CASE E02
-- 기대 SQLSTATE 23503, constraint knowledge_category_fk
-- 아래 분류 ID가 0행인지 먼저 확인합니다. 존재한다면 다른 없는 ID로 바꿉니다.
SELECT id FROM public.categories WHERE id=999999;
BEGIN;
INSERT INTO public.knowledge(title,content,category_id) VALUES ('실패 검사','정상 길이',999999);
-- ENDCASE E02
-- CASE RECOVER_E02
ROLLBACK;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE RECOVER_E02
-- CASE E03
-- 기대 SQLSTATE 23505
BEGIN;
INSERT INTO public.categories(name) VALUES ('learning');
-- ENDCASE E03
-- CASE RECOVER_E03
ROLLBACK;
SELECT id,title,content,category_id FROM public.knowledge ORDER BY id;
-- ENDCASE RECOVER_E03
