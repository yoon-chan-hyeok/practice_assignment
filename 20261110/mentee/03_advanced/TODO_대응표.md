# TODO 위치와 완료 요구사항

같은 ID가 강사용 정답의 같은 위치에 있습니다. 일반 힌트보다 각 코드 안의 요구사항을 먼저 읽으세요.

| ID | 위치 | 요구사항 |
|---|---|---|
| H01-01 | `01_first_server/main.py` | status=ok인 dict를 반환하는 health를 완성하세요. |
| H01-02 | `01_first_server/tests/test_api.py` | r의 HTTP 상태가 200인지 assert로 검사하세요. |
| H01-03 | `01_first_server/tests/test_api.py` | r의 JSON 본문이 정확히 status=ok인지 검사하세요. |
| H02-03 | `02_read/main.py` | 조회 결과가 None이면 HTTP의 404로 변환하세요. |
| H02-01 | `02_read/logic.py` | 읽고 필터링한 entries 목록을 반환하세요. 저장 함수를 호출하지 마세요. |
| H02-02 | `02_read/logic.py` | 항목의 id와 knowledge_id가 일치하면 그 dict를 반환하세요. 없으면 아래 None으로 진행하세요. |
| H02-04 | `02_read/tests/test_api.py` | 정상·404·422 GET 이후 파일 바이트가 before와 같은지 검사하세요. |
| H03-01 | `03_create/logic.py` | fields를 복사한 entry를 만들고 현재 next_id를 id로 지정하세요. |
| H03-02 | `03_create/logic.py` | entry를 추가하고 다음 ID를 증가시켜 data 전체를 저장하세요. |
| H03-03 | `03_create/tests/test_api.py` | 초기 3건 기준 생성된 entry가 요청 필드와 새 id=4를 포함하는지 검사하세요. |
| H03-04 | `03_create/tests/test_api.py` | 잘못된 입력에 422가 나오고 파일이 변경되지 않았는지 모두 검사하세요. |
| H04-03 | `04_update/main.py` | 데이터 함수가 None을 반환하면 Router에서 404를 보내세요. |
| H04-01 | `04_update/logic.py` | fields의 복사본 updated를 만들고 기존 요청 ID를 유지하세요. |
| H04-02 | `04_update/logic.py` | 찾은 위치 i를 교체하고 저장하세요. 다른 항목과 next_id는 그대로 두세요. |
| H04-04 | `04_update/tests/test_api.py` | 두 번 수정한 뒤 next_id와 항목 수가 변하지 않았는지 검사하세요. |
| H05-02 | `05_delete/main.py` | 삭제 성공 시 본문 없는 204를 반환하세요. |
| H05-01 | `05_delete/logic.py` | 대상 위치를 제거하고 저장한 뒤 True를 반환하세요. next_id는 변경하지 마세요. |
| H05-03 | `05_delete/tests/test_api.py` | 삭제 상태가 204이고 실제 응답 바이트가 비어 있는지 확인하세요. |
| H05-04 | `05_delete/tests/test_api.py` | 404와 422 삭제 요청 이후 파일 내용이 이전과 같은지 확인하세요. |
| H06-01 | `06_structure/app/main.py` | knowledge 모듈의 router를 app에 포함하세요. 추가 prefix를 붙이지 마세요. |
| H06-02 | `06_structure/app/repositories/json_knowledge.py` | Repository의 목록 조회 결과를 반환하세요. HTTP Response를 만들지 마세요. |
| H06-03 | `06_structure/app/routers/knowledge.py` | 검증된 payload를 dict로 바꾸어 repo.create에 전달하고 결과를 반환하세요. |
| H06-04 | `06_structure/tests/test_api.py` | 상세 응답의 키가 id·title·content·category 네 가지인지 검사하세요. |
| H07-01 | `07_project/app/repositories/json_knowledge.py` | 생성 데이터와 next_id를 파일에 저장하는 연결을 완성하세요. |
| H07-02 | `07_project/app/routers/knowledge.py` | Repository 삭제가 성공한 경우 빈 204 응답을 반환하세요. |
| H07-03 | `07_project/tests/test_api.py` | 잘못된 입력이 422이며 저장 파일을 바꾸지 않는지 검사하세요. |
| H07-04 | `07_project/tests/test_api.py` | 없는 category를 조회한 목록이 200과 빈 배열인지 검사하세요. |
| H08-01 | `07_project/tests/test_daily_project.py` | B 수정의 200과 같은 ID의 재조회 본문을 검사하세요. expected는 changed와 B의 기존 ID입니다. |
| H08-02 | `07_project/tests/test_daily_project.py` | 빈 본문 입력의 422와 파일 불변을 검사하세요. |
| H08-03 | `07_project/tests/test_daily_project.py` | C 삭제의 204·빈 본문과 삭제 후 상세 GET의 404를 모두 확인하세요. |
