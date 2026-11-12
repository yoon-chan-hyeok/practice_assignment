-- PPT 68~72. 새 개인 학습 DB에 딱 한 번 실행하는 제공 완성본입니다.
-- 두 표가 있거나 준비 중 오류가 나면 DROP/초기화하지 않습니다.
-- pgAdmin: Auto commit ON / Auto rollback on error OFF.
-- 전체 실행 중 오류가 나면 ROLLBACK만 별도로 실행하고 강사와 원인을 확인하세요.
BEGIN;
-- 제공된 안전 확인입니다. 이 블록은 TODO가 아닙니다.
-- 개인 수업용 DB에서만 실행합니다. 이름만 맞다고 운영 DB가 안전해지는 것은 아닙니다.
DO $guard$
BEGIN
  IF current_database() !~ '^knowledge_lab(_[a-z0-9_]+)?$' THEN
    RAISE EXCEPTION '개인 knowledge_lab DB에 다시 접속하세요. 현재 DB: %', current_database();
  END IF;
END;
$guard$;
SET search_path TO public;
DO $empty$
BEGIN
 IF to_regclass('public.categories') IS NOT NULL
    OR to_regclass('public.knowledge') IS NOT NULL THEN
   RAISE EXCEPTION '이미 수업 표가 있습니다. 기존 데이터를 보존하고 준비 SQL을 중단합니다.';
 END IF;
END;
$empty$;
CREATE TABLE public.categories (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(30) NOT NULL UNIQUE,
  CONSTRAINT categories_name_length
    CHECK (char_length(name) BETWEEN 1 AND 30)
);
CREATE TABLE public.knowledge (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(80) NOT NULL,
  content TEXT NOT NULL,
  category_id BIGINT NOT NULL,
  CONSTRAINT knowledge_title_length
    CHECK (char_length(title) BETWEEN 1 AND 80),
  CONSTRAINT knowledge_content_length
    CHECK (char_length(content) BETWEEN 1 AND 2000),
  CONSTRAINT knowledge_category_fk
    FOREIGN KEY (category_id)
    REFERENCES public.categories(id) ON DELETE RESTRICT
);
INSERT INTO public.categories (name)
VALUES ('learning'), ('environment'), ('reference')
RETURNING id, name;

INSERT INTO public.knowledge (title, content, category_id)
SELECT '실습 파일 보관', '실습 파일은 개인 폴더에 보관합니다.', id
FROM public.categories WHERE name = 'learning'
RETURNING id, title;

INSERT INTO public.knowledge (title, content, category_id)
SELECT '서버 실행', '프로젝트 폴더에서 서버를 실행합니다.', id
FROM public.categories WHERE name = 'environment'
RETURNING id, title;

INSERT INTO public.knowledge (title, content, category_id)
SELECT '질문 작성', '오류 메시지와 시도한 작업을 함께 적습니다.', id
FROM public.categories WHERE name = 'learning'
RETURNING id, title;
DO $check$
BEGIN
 IF (SELECT COUNT(*) FROM public.categories)<>3
    OR (SELECT COUNT(*) FROM public.knowledge)<>3 THEN
   RAISE EXCEPTION '준비 행 수가 일치하지 않습니다. COMMIT하지 마세요.';
 END IF;
END;
$check$;
COMMIT;
-- 읽기 전용. false가 나와도 초기화하지 말고, 현재 작업 상태부터 확인합니다.
SELECT current_database() AS database_name;
SELECT id, name FROM public.categories ORDER BY id;
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id=c.id
GROUP BY c.id,c.name ORDER BY c.id;
SELECT COUNT(*) AS knowledge_count,
       SUM(char_length(content)) AS total_chars,
       MIN(char_length(content)) AS min_chars,
       MAX(char_length(content)) AS max_chars
FROM public.knowledge;
-- 새로 준비한 S0: 3건 / 64자 / 20자 / 24자
-- 7교시 COMMIT 이후(S1)에는 길이 64를 정답으로 요구하지 않습니다.
