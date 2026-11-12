-- 오전 DB가 준비되지 않았을 때만 사용합니다. 기존 테이블이 있으면 실행하지 마세요.
CREATE TABLE categories (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(30) NOT NULL UNIQUE,
  CONSTRAINT categories_name_length CHECK (char_length(name) BETWEEN 1 AND 30)
);
CREATE TABLE knowledge (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(80) NOT NULL,
  content TEXT NOT NULL,
  category_id BIGINT NOT NULL,
  CONSTRAINT knowledge_title_length CHECK (char_length(title) BETWEEN 1 AND 80),
  CONSTRAINT knowledge_content_length CHECK (char_length(content) BETWEEN 1 AND 2000),
  CONSTRAINT knowledge_category_fk FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);
INSERT INTO categories (name) VALUES ('learning'),('environment'),('reference');
INSERT INTO knowledge (title, content, category_id)
SELECT '실습 파일 보관','실습 파일은 개인 폴더에 보관합니다.',id FROM categories WHERE name='learning';
INSERT INTO knowledge (title, content, category_id)
SELECT '서버 실행','프로젝트 폴더에서 서버를 실행합니다.',id FROM categories WHERE name='environment';
INSERT INTO knowledge (title, content, category_id)
SELECT '질문 작성','오류 메시지와 시도한 작업을 함께 적습니다.',id FROM categories WHERE name='learning';
