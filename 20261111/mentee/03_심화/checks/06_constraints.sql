-- Day18 | 실습 06: 제약조건·실패·회복 | PPT 42~47 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E6_GUARD expect=00000 capture=- reconnect=false
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

-- @step E6_BEFORE expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step E6_PARENT expect=00000 capture=- reconnect=false
SELECT id,name FROM public.categories ORDER BY id;
SELECT id FROM public.categories WHERE id=-1;

-- @step E6_CHECK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E6_BAD_CONTENT expect=23514 capture=- reconnect=false
INSERT INTO public.knowledge(title,content,category_id) VALUES ('오류 확인','',1);

-- @step E6_ABORTED expect=25P02 capture=- reconnect=false
SELECT COUNT(*) FROM public.knowledge;

-- @step E6_CHECK_CANCEL expect=00000 capture=- reconnect=false
-- BEGIN TASK H06_01
-- TODO H06_01
-- 앞의 빈 본문 INSERT가 CHECK 오류로 거부된 뒤 이 구간만 따로 실행해 미확정 거래를 취소하세요.
__TODO_ROLLBACK__;
-- END TASK H06_01

-- @step E6_FK_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E6_BAD_FK expect=23503 capture=- reconnect=false
INSERT INTO public.knowledge(title,content,category_id) VALUES ('오류 확인','정상 본문',-1);

-- @step E6_FK_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E6_NULL_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E6_BAD_NULL expect=23502 capture=- reconnect=false
-- BEGIN TASK H06_03
-- TODO H06_03
-- title만 NULL로 보내 NOT NULL 오류를 분리해 재현하세요. 다른 값은 정상으로 두고 기대 SQLSTATE 23502와 대조합니다.
INSERT INTO public.knowledge(title,content,category_id)
VALUES (__TODO_NULL_TITLE__, '정상 본문', 1);
-- END TASK H06_03

-- @step E6_NULL_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E6_UNIQUE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E6_BAD_UNIQUE expect=23505 capture=- reconnect=false
INSERT INTO public.categories(name) VALUES ('learning');

-- @step E6_UNIQUE_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E6_PARENT_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E6_BAD_PARENT expect=23503 capture=- reconnect=false
-- BEGIN TASK H06_02
-- TODO H06_02
-- S0에서 지식이 참조하는 learning 분류(id=1)만 삭제하려고 시도하세요. 기대는 RESTRICT의 FK 오류 23503입니다.
DELETE FROM public.categories
WHERE __TODO_REFERENCED_PARENT__;
-- END TASK H06_02

-- @step E6_PARENT_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E6_AFTER expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
SELECT id,name FROM public.categories ORDER BY id;
