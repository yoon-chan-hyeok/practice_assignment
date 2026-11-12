-- Day18 | 실습 07: 취소·확정·인덱스·실행계획 | PPT 48~54, 76 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E7_GUARD expect=00000 capture=- reconnect=false
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

-- @step E7_BEFORE expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_CANCEL_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_TEMP expect=00000 capture=- reconnect=false
UPDATE public.knowledge SET content='취소할 임시 안내입니다.' WHERE id=2 RETURNING id,content;

-- @step E7_CANCEL expect=00000 capture=- reconnect=false
-- BEGIN TASK H07_01
-- TODO H07_01
-- 임시 본문 수정을 확정하지 않고 취소하는 명령을 넣으세요. 다음 SELECT에서 시작 본문이 보여야 합니다.
__TODO_END_CANCEL__;
-- END TASK H07_01

-- @step E7_CANCEL_READ expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_SAVE_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_SAVE expect=00000 capture=- reconnect=false
UPDATE public.knowledge SET content='실행 전에 가상환경을 확인합니다.' WHERE id=2 RETURNING id,content;

-- @step E7_COMMIT expect=00000 capture=- reconnect=false
-- BEGIN TASK H07_02
-- TODO H07_02
-- 가상환경 확인 안내를 확정하세요. 이 명령 후 새 연결에서 조회해도 같은 본문이 나와야 합니다.
__TODO_END_SAVE__;
-- END TASK H07_02

-- @step E7_RECONNECT expect=00000 capture=- reconnect=true
SELECT current_database() AS database_name;
SELECT id,content FROM public.knowledge WHERE id=2;

-- @step E7_PAIR_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_PAIR expect=00000 capture=- reconnect=false
-- BEGIN TASK H07_03
-- TODO H07_03
-- 같은 트랜잭션에서 id 3의 content를 묶음 연습 2로 바꾸는 두 번째 UPDATE를 작성하세요. 두 변경 모두 ROLLBACK합니다.
UPDATE public.knowledge SET content='묶음 연습 1' WHERE id=1;
__TODO_SECOND_UPDATE__
RETURNING id, content;
-- END TASK H07_03

-- @step E7_PAIR_READ expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id IN (1,3) ORDER BY id;

-- @step E7_PAIR_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E7_ATOMIC_BEFORE expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id IN (2,3) ORDER BY id;

-- @step E7_ATOMIC_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E7_ATOMIC_FIRST expect=00000 capture=- reconnect=false
-- BEGIN TASK H07_04
-- TODO H07_04
-- 첫 번째 변경의 대상은 실제 존재하는 지식 id 2입니다. 뒤의 id 3 빈 본문 실패와 같은 BEGIN에 묶으세요.
UPDATE public.knowledge
SET content='확정되면 안 되는 임시 본문'
WHERE __TODO_FIRST_TARGET__;
-- END TASK H07_04

-- @step E7_ATOMIC_FAIL expect=23514 capture=- reconnect=false
UPDATE public.knowledge SET content='' WHERE id=3;

-- @step E7_ATOMIC_CANCEL expect=00000 capture=- reconnect=false
ROLLBACK;

-- @step E7_ATOMIC_AFTER expect=00000 capture=- reconnect=false
SELECT id,content FROM public.knowledge WHERE id IN (2,3) ORDER BY id;
