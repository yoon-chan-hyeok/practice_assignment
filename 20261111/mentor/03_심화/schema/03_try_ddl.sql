-- Day18 | 실습 03: 두 테이블·키·ERD | PPT 21~28, 69~70, 73 | 30분
-- SQL 편집: VS Code / 실행: pgAdmin Query Tool (주 경로), psql (선택 경로)
-- @step은 실행 단위를 표시하는 주석입니다. SQL 명령이 아닙니다.
-- 한 @step 구간씩 선택 실행합니다. 오류 뒤 ROLLBACK은 반드시 별도 실행합니다.
-- __TODO_...__는 구현할 빈칸, __NEW_ID__/__A_ID__/__B_ID__/__C_ID__는 실제 실행 입력입니다.
-- 입력 ID는 RETURNING에서 읽어 해당 토큰을 실제 정수로 바꿉니다. 4·5·6으로 예측하지 않습니다.
-- 아직 남은 토큰 때문에 생긴 문법 오류는 의도한 제약 실패로 인정하지 않습니다.

-- @step E3_GUARD expect=00000 capture=- reconnect=false
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

-- @step E3_BEGIN expect=00000 capture=- reconnect=false
BEGIN;

-- @step E3_CREATE expect=00000 capture=- reconnect=false
CREATE TABLE public.categories_try (
-- BEGIN TASK H03_01
-- 해설 H03_01
-- PRIMARY KEY는 유일성과 NULL 금지를 적용합니다. _try의 수동 번호는 공통 모델의 IDENTITY를 대체하지 않습니다.
id INTEGER PRIMARY KEY,
-- END TASK H03_01
-- BEGIN TASK H03_03
-- 해설 H03_03
-- NOT NULL은 NULL만, UNIQUE는 중복을, CHECK는 빈 문자열을 포함한 길이를 검사합니다. 세 역할을 구분합니다.
name VARCHAR(30) NOT NULL UNIQUE
  CHECK (char_length(name) BETWEEN 1 AND 30)
-- END TASK H03_03
);
CREATE TABLE public.knowledge_try (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
-- BEGIN TASK H03_02
-- 해설 H03_02
-- REFERENCES는 없는 부모 키의 저장을 거부합니다. NOT NULL과 함께 사용해 분류를 필수로 만듭니다.
category_id INTEGER NOT NULL
  REFERENCES public.categories_try(id)
-- END TASK H03_02
-- BEGIN TASK H03_04
-- 해설 H03_04
-- ON DELETE RESTRICT는 연결된 분류를 지울 때 거부합니다. 지식 한 행 삭제와 분류 삭제의 영향은 다릅니다.
ON DELETE RESTRICT
-- END TASK H03_04
);
