-- 기존 knowledge_lab은 사용하거나 초기화하지 않습니다.
-- pgAdmin에서 Databases 우클릭 → Create → Database로 아래 두 DB를 각각 만들 수 있습니다.
-- SQL로 만들 경우 postgres DB에 접속하고 Auto commit ON에서 한 문장씩 선택·실행합니다.
-- 이 파일 전체를 BEGIN/COMMIT으로 감싸거나 한꺼번에 실행하지 마세요.
CREATE DATABASE day19_build_h;
CREATE DATABASE day19_crud_h;
-- 만들어졌다면 각각 새 Query Tool을 열고 SELECT current_database();로 확인합니다.
-- 같은 이름이 이미 있으면 삭제하지 말고 테이블/작업 상태를 먼저 확인하세요.
