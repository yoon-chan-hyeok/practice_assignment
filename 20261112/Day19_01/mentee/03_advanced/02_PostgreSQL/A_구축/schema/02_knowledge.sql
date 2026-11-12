BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_h, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.knowledge (
    -- BEGIN H-DDL-04
    -- TODO H-DDL-04: knowledge.id의 BIGINT·ALWAYS IDENTITY·PK를 선언하세요.
    __TODO_H_DDL_04__
    -- END H-DDL-04
    -- BEGIN H-DDL-05
    -- TODO H-DDL-05: title VARCHAR(80), content TEXT, category_id BIGINT를 모두 필수 열로
    -- 선언하세요.
    __TODO_H_DDL_05__
    -- END H-DDL-05
    -- BEGIN H-DDL-06
    -- TODO H-DDL-06: knowledge_title_length라는 CHECK로 제목 길이 1~80자를 검사하세요.
    __TODO_H_DDL_06__
    -- END H-DDL-06
    -- BEGIN H-DDL-07
    -- TODO H-DDL-07: knowledge_content_length라는 CHECK로 본문 길이 1~2000자를 검사하세요.
    __TODO_H_DDL_07__
    -- END H-DDL-07
    -- BEGIN H-DDL-08
    -- TODO H-DDL-08: knowledge_category_fk를 선언하여 필수 분류 참조와 RESTRICT를 구현하세요.
    __TODO_H_DDL_08__
    -- END H-DDL-08
);
COMMIT;
