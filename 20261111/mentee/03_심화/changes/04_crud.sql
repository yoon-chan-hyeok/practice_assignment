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
-- BEGIN TASK H04_01
-- TODO H04_01
-- 지식 한 건을 INSERT하고 생성 결과를 RETURNING으로 받으세요. id는 입력하지 않습니다.
-- 응용·심화는 실제 id를 __NEW_ID__에 넣고 다음 변경을 같은 트랜잭션에서 진행합니다.
__TODO_INSERT__ public.knowledge (title, content, category_id)
VALUES ('임시 안내', '취소할 연습 데이터입니다.', 1)
__TODO_RETURNING__ id, title, content, category_id;
-- END TASK H04_01

-- @step E4_NEW_READ expect=00000 capture=- reconnect=false
SELECT id,title,content,category_id FROM public.knowledge WHERE id=__NEW_ID__;

-- @step E4_UPDATE expect=00000 capture=- reconnect=false
-- BEGIN TASK H04_02
-- TODO H04_02
-- 지정한 지식 한 건의 content만 수정하세요. 먼저 같은 ID의 현재 행을 SELECT합니다.
-- ID와 전체 행 수는 바뀌지 않아야 하며 제목·분류를 바꾸지 않습니다.
UPDATE public.knowledge
__TODO_SET__ content = '수정 연습 안내입니다.'
__TODO_WHERE__ id = __NEW_ID__
RETURNING id, title, content;
-- END TASK H04_02

-- @step E4_DELETE expect=00000 capture=- reconnect=false
-- BEGIN TASK H04_03
-- TODO H04_03
-- 지정된 ID의 지식만 삭제하고 삭제된 id·title을 반환하세요. 표나 분류를 삭제하지 않습니다.
__TODO_DELETE_FROM__ public.knowledge
WHERE id = __NEW_ID__
RETURNING id, title;
-- END TASK H04_03

-- @step E4_ZERO expect=00000 capture=- reconnect=false
-- BEGIN TASK H04_04
-- TODO H04_04
-- 사전 조회에서 없는 것으로 확인한 ID -1을 조건으로 써 0행 변경을 확인하세요. -1이 실제로 있으면 중단합니다.
UPDATE public.knowledge SET content = '변경되면 안 됨'
WHERE __TODO_ABSENT_ID__
RETURNING id;
-- END TASK H04_04

-- @step E4_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E4_COUNT expect=00000 capture=- reconnect=false
-- BEGIN TASK H04_05
-- TODO H04_05
-- 취소 후 실제 행 수를 세는 함수를 넣으세요. MAX(id)를 행 수로 쓰지 말고 기존 원문도 별도 비교합니다.
SELECT __TODO_COUNT__ AS knowledge_count
FROM public.knowledge;
-- END TASK H04_05

-- @step E4_AFTER expect=00000 capture=- reconnect=false
SELECT id, title, content, category_id FROM public.knowledge ORDER BY id;
