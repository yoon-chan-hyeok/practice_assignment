-- Day18 | 실습 04: SQL CRUD·RETURNING | PPT 29~34 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E4_GUARD expect=00000 capture=- reconnect=false
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

-- @step E4_BEFORE expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;

-- @step E4_INSERT_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E4_INSERT expect=00000 capture=new_ reconnect=false
-- BEGIN TASK A04_01
-- 해설 A04_01
-- INSERT의 열 목록과 VALUES 순서를 맞춥니다. RETURNING은 DB 결과이며 HTTP 201이 아닙니다.
-- ROLLBACK해도 시퀀스가 이미 발급한 번호는 다시 사용되지 않을 수 있습니다.
INSERT INTO public.knowledge (title, content, category_id)
VALUES ('임시 안내', '취소할 연습 데이터입니다.', 1)
RETURNING id, title, content, category_id;
-- END TASK A04_01

-- @step E4_NEW_READ expect=00000 capture=- reconnect=false
SELECT id,title,content,category_id FROM public.knowledge WHERE id=__NEW_ID__;

-- @step E4_UPDATE expect=00000 capture=- reconnect=false
-- BEGIN TASK A04_02
-- 해설 A04_02
-- SQL UPDATE는 SET에 지정한 열만 수정합니다. 전날 PUT의 세 필드 필수 규칙과는 다른 층의 약속입니다. WHERE 누락은 전체 행 변경입니다.
UPDATE public.knowledge
SET content = '수정 연습 안내입니다.'
WHERE id = __NEW_ID__
RETURNING id, title, content;
-- END TASK A04_02

-- @step E4_DELETE expect=00000 capture=- reconnect=false
-- BEGIN TASK A04_03
-- 해설 A04_03
-- DELETE는 조건에 맞는 행만 지웁니다. 이 연습은 ROLLBACK하므로 시작 데이터가 보존됩니다.
DELETE FROM public.knowledge
WHERE id = __NEW_ID__
RETURNING id, title;
-- END TASK A04_03

-- @step E4_ZERO expect=00000 capture=- reconnect=false
-- BEGIN TASK A04_04
-- 해설 A04_04
-- 0행 UPDATE는 정상 SQL 실행이며 제약 오류가 아닙니다. 원하는 대상이 변경되었는지는 행 수로 판단합니다.
UPDATE public.knowledge SET content = '변경되면 안 됨'
WHERE id = -1
RETURNING id;
-- END TASK A04_04

-- @step E4_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E4_AFTER expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
