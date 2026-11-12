-- 제공 안전장치: 아래 DO 구문은 수정 과제가 아닙니다.
DO $guard$
BEGIN
    IF current_database() <> 'day19_crud_a' THEN
        RAISE EXCEPTION 'Wrong database: expected day19_crud_a, got %', current_database();
    END IF;
END;
$guard$;
-- 파일 전체 실행 금지: 조회는 CASE 단위, 변경은 BEGIN → DML RETURNING → 종료문 → SELECT를 각각 선택합니다.
-- __NEW_ID__는 C01 RETURNING으로 받은 실제 정수로 치환합니다. 구현 TODO와 다릅니다.

-- CASE R01
-- BEGIN A-SQL-01
-- 해설 A-SQL-01: 초기 S0에서 id·title만 id 오름차순으로 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를
-- 고정합니다.
SELECT id, title FROM public.knowledge ORDER BY id;
-- END A-SQL-01
-- ENDCASE R01

-- CASE R02
-- BEGIN A-SQL-02
-- 해설 A-SQL-02: ID 2의 id·title·content·category_id를 조회하세요. 빈 결과도 정상이며, ORDER
-- BY로 결과 순서를 고정합니다.
SELECT id, title, content, category_id FROM public.knowledge WHERE id = 2;
-- END A-SQL-02
-- ENDCASE R02

-- CASE R03
-- BEGIN A-SQL-03
-- 해설 A-SQL-03: knowledge와 categories를 FK로 연결해 id·title·분류명(category)을 지식 id
-- 오름차순으로 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를 고정합니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge AS k
JOIN public.categories AS c ON c.id = k.category_id
ORDER BY k.id;
-- END A-SQL-03
-- ENDCASE R03

-- CASE R04
-- BEGIN A-SQL-04
-- 해설 A-SQL-04: LEFT JOIN은 지식이 없는 reference 분류도 남깁니다. COUNT(k.id)는 NULL을 제외하므로
-- 0이고 COUNT(*)는 바깥 조인 행 자체를 세어 1이 됩니다.
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories AS c
LEFT JOIN public.knowledge AS k ON k.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.id;
-- END A-SQL-04
-- ENDCASE R04

-- CASE R05
-- BEGIN A-SQL-05
-- 해설 A-SQL-05: 분류가 learning이면서 제목에 실습이 포함된 지식의 id·title·분류명(category)을 id 순으로
-- 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를 고정합니다.
SELECT k.id, k.title, c.name AS category
FROM public.knowledge k JOIN public.categories c ON c.id=k.category_id
WHERE c.name='learning' AND k.title ILIKE '%실습%' ORDER BY k.id;
-- END A-SQL-05
-- ENDCASE R05

-- CASE R06
-- BEGIN A-SQL-06
-- 해설 A-SQL-06: 분류가 reference인 지식의 id·title을 id 순으로 조회하세요. 분류는 있지만 지식이 없으므로
-- 0행입니다. 빈 결과도 정상이며, ORDER BY로 결과 순서를 고정합니다.
SELECT k.id, k.title FROM public.knowledge k
JOIN public.categories c ON c.id=k.category_id
WHERE c.name='reference' ORDER BY k.id;
-- END A-SQL-06
-- ENDCASE R06

-- CASE R07
-- BEGIN A-SQL-07
-- 해설 A-SQL-07: 분류별 지식 수를 구한 뒤 2건 이상인 분류명(category)과 개수(knowledge_count)만 분류 id
-- 순으로 조회하세요. 빈 결과도 정상이며, ORDER BY로 결과 순서를 고정합니다.
SELECT c.name AS category, COUNT(k.id) AS knowledge_count
FROM public.categories c LEFT JOIN public.knowledge k ON k.category_id=c.id
GROUP BY c.id,c.name HAVING COUNT(k.id)>=2 ORDER BY c.id;
-- END A-SQL-07
-- ENDCASE R07
