BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_a, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- BEGIN A-DDL-04
    -- TODO A-DDL-04: knowledge의 title VARCHAR(80), content TEXT, category_id
    -- BIGINT를 각각 NOT NULL로 선언하세요. 각 줄에 쉼표를 붙입니다.
    __TODO_A_DDL_04__
    -- END A-DDL-04
    -- BEGIN A-DDL-05
    -- TODO A-DDL-05: knowledge_title_length와 knowledge_content_length CHECK를
    -- 작성하세요. 각각 1~80자, 1~2000자이며 뒤에 쉼표를 붙입니다.
    __TODO_A_DDL_05__
    -- END A-DDL-05
    -- BEGIN A-DDL-06
    -- TODO A-DDL-06: knowledge_category_fk라는 FK로 category_id를 categories.id에 연결하고
    -- ON DELETE RESTRICT를 설정하세요.
    __TODO_A_DDL_06__
    -- END A-DDL-06
);
COMMIT;
