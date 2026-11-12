BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_build_b' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_build_b, got %', current_database();
    END IF;
END;
$guard$;
CREATE TABLE public.categories (
    -- BEGIN B-DDL-01
    -- TODO B-DDL-01: categories의 id를 BIGINT 자동 생성 IDENTITY와 PRIMARY KEY로 선언하세요.
    -- 쉼표까지 포함합니다.
    id BIGINT __TODO_B_DDL_01__,
    -- END B-DDL-01
    name VARCHAR(30) NOT NULL UNIQUE,
    -- BEGIN B-DDL-02
    -- TODO B-DDL-02: categories.name의 1~30자 길이 CHECK를 categories_name_length라는
    -- 이름으로 완성하세요.
    CONSTRAINT categories_name_length CHECK (__TODO_B_DDL_02__)
    -- END B-DDL-02
);
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    -- BEGIN B-DDL-03
    -- TODO B-DDL-03: title은 1~80자, content는 1~2000자인 두 CHECK를 명세의 이름으로 완성하세요. 각 줄
    -- 끝 쉼표가 필요합니다.
    CONSTRAINT knowledge_title_length CHECK (__TODO_B_DDL_03_A__),
    CONSTRAINT knowledge_content_length CHECK (__TODO_B_DDL_03_B__),
    -- END B-DDL-03
    CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id)
        -- BEGIN B-DDL-04
        -- TODO B-DDL-04: category_id가 public.categories(id)를 참조하도록 REFERENCES와 부모 삭제
        -- RESTRICT를 완성하세요.
        REFERENCES __TODO_B_DDL_04__
        -- END B-DDL-04
);
COMMIT;
