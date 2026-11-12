-- Day18 | 실습 02: 지식 SELECT·조건·정렬 | PPT 14~20 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E2_GUARD expect=00000 capture=- reconnect=false
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

-- @step E2_LIST expect=00000 capture=- reconnect=false
-- BEGIN TASK B02_01
-- TODO B02_01
-- 지식 표에서 id·title·category_id를 조회하세요. ID 오름차순으로 세 지식이 보여야 합니다.
SELECT id, title, category_id FROM __TODO_TABLE__ ORDER BY id;
-- END TASK B02_01

-- @step E2_DETAIL expect=00000 capture=- reconnect=false
-- BEGIN TASK B02_02
-- TODO B02_02
-- WHERE를 넣어 S0의 서버 실행 지식(id=2) 한 건만 조회하세요. 실행 전 실제 ID를 확인합니다.
SELECT id, title, content FROM public.knowledge
__TODO_WHERE__ id = 2;
-- END TASK B02_02

-- @step E2_CATEGORY expect=00000 capture=- reconnect=false
-- BEGIN TASK B02_03
-- TODO B02_03
-- 분류 1의 지식을 ID 오름차순으로 조회하세요. S0에서는 id 1·3 두 행입니다.
SELECT id, title FROM public.knowledge
WHERE category_id = 1
__TODO_ORDER__ id;
-- END TASK B02_03

-- @step E2_EMPTY expect=00000 capture=- reconnect=false
SELECT id, title FROM public.knowledge WHERE id=-1;
