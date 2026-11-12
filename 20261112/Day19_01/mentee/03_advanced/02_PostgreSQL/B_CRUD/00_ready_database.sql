BEGIN;
-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_h' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_h, got %', current_database();
    END IF;
END;
$guard$;
-- 제공된 완성 DB의 재현 SQL입니다. 구축 과제의 미완성 여부와 무관하게 사용합니다.
-- 새 전용 DB에 한 번 실행합니다. 기존 표가 있으면 오류로 중단하며 자동으로 삭제하지 않습니다.
CREATE TABLE public.categories (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT categories_name_length CHECK (char_length(name) BETWEEN 1 AND 30)
);
CREATE TABLE public.knowledge (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    category_id BIGINT NOT NULL,
    CONSTRAINT knowledge_title_length CHECK (char_length(title) BETWEEN 1 AND 80),
    CONSTRAINT knowledge_content_length CHECK (char_length(content) BETWEEN 1 AND 2000),
    CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id)
        REFERENCES public.categories(id) ON DELETE RESTRICT
);
CREATE INDEX idx_knowledge_category_id ON public.knowledge(category_id);
INSERT INTO public.categories(name)
VALUES ('learning'), ('environment'), ('reference');
INSERT INTO public.knowledge(title, content, category_id)
SELECT '실습 파일 보관', '실습 파일은 개인 폴더에 보관합니다.', id
FROM public.categories WHERE name = 'learning';
INSERT INTO public.knowledge(title, content, category_id)
SELECT '서버 실행', '프로젝트 폴더에서 서버를 실행합니다.', id
FROM public.categories WHERE name = 'environment';
INSERT INTO public.knowledge(title, content, category_id)
SELECT '질문 작성', '오류 메시지와 시도한 작업을 함께 적습니다.', id
FROM public.categories WHERE name = 'learning';
COMMIT;
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
