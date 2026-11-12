-- 현재 연결 대상과 시작 행을 확인합니다. 기대값을 고정하지 말고 실제 값을 기록합니다.
SELECT current_database() AS database_name, current_user AS user_name;
SELECT COUNT(*) AS category_count FROM categories;
SELECT COUNT(*) AS knowledge_count FROM knowledge;
SELECT k.id, k.title, k.content, c.name AS category
FROM knowledge AS k JOIN categories AS c ON c.id = k.category_id
ORDER BY k.id;
