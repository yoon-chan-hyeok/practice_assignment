-- Day18 | 실습 05: JOIN·분류별 집계 | PPT 35~41, 74 | 35분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E5_GUARD expect=00000 capture=- reconnect=false
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

-- @step E5_JOIN expect=00000 capture=- reconnect=false
-- BEGIN TASK B05_01
-- TODO B05_01
-- 분류 PK와 지식 FK를 맞춰 분류명을 붙이세요. 결과 한 행은 지식 한 건이며 S0는 3행입니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON __TODO_JOIN_CONDITION__
ORDER BY k.id;
-- END TASK B05_01

-- @step E5_GROUP expect=00000 capture=- reconnect=false
-- BEGIN TASK B05_02
-- TODO B05_02
-- 분류를 왼쪽에 두고 분류별 실제 지식 수를 세세요. 빈 reference 분류는 0이어야 합니다.
-- 힌트: NULL인 자식 ID를 세지 않는 COUNT를 사용합니다.
SELECT c.name AS category, __TODO_CHILD_COUNT__ AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id = c.id
__TODO_GROUP_BY__ c.id, c.name
ORDER BY c.id;
-- END TASK B05_02

-- @step E5_LENGTH expect=00000 capture=- reconnect=false
SELECT COUNT(*) AS knowledge_count,SUM(char_length(content)) AS total_chars,
MIN(char_length(content)) AS min_chars,MAX(char_length(content)) AS max_chars FROM public.knowledge;
