# TODO 위치와 완료 요구사항

같은 ID가 강사용 정답의 같은 위치에 있습니다. 일반 힌트보다 각 코드 안의 요구사항을 먼저 읽으세요.

| ID | 위치 | 요구사항 |
|---|---|---|
| A01-01 | `01_first_server/main.py` | FastAPI 앱의 title을 Knowledge API로, description을 AI 플랫폼의 원본 지식 관리 연습으로 설정하세요. |
| A01-02 | `01_first_server/main.py` | GET /health에서 status=ok인 dict를 반환하세요. |
| A01-03 | `01_first_server/main.py` | name을 포함한 안녕하세요, {name} 문자열을 message 값으로 반환하세요. |
| A02-01 | `02_read/main.py` | category와 정확히 일치하는 항목만 result에 남기세요. 일치 항목이 없으면 빈 목록이어야 합니다. |
| A02-02 | `02_read/main.py` | entries를 순회하여 id가 knowledge_id인 지식을 반환하세요. 찾지 못하면 반복문 다음으로 진행하세요. |
| A02-03 | `02_read/main.py` | 반복문에서 찾지 못한 경우 HTTPException으로 404와 Knowledge not found를 전달하세요. |
| A03-01 | `03_create/main.py` | 검증된 payload를 dict로 변환하여 entry에 저장하세요. |
| A03-02 | `03_create/main.py` | 현재 data의 next_id를 새 entry의 id로 지정하세요. |
| A03-03 | `03_create/main.py` | entries에 새 지식을 추가한 뒤 다음 ID를 1 올리세요. |
| A03-04 | `03_create/main.py` | 변경된 data를 파일에 저장하세요. |
| A04-01 | `04_update/main.py` | 현재 항목이 수정 대상인지 비교 결과를 same_id에 넣으세요. |
| A04-02 | `04_update/main.py` | 새 입력을 dict로 만들고 기존 knowledge_id를 유지하여 updated를 구성하세요. |
| A04-03 | `04_update/main.py` | 대상 위치 i를 updated로 교체하세요. |
| A04-04 | `04_update/main.py` | 변경 내용을 저장하세요. |
| A05-01 | `05_delete/main.py` | 현재 entry가 요청 ID와 같을 때만 위치 i의 항목을 제거·저장하고 본문 없는 204를 반환하세요. |
| A05-02 | `05_delete/main.py` | 대상을 찾지 못하면 404를 raise하세요. next_id나 파일을 변경하지 마세요. |
| A05-03 | `05_delete/main.py` | 삭제 뒤 다시 생성해도 중복되지 않도록 next_id에서 ID를 발급하세요. |
| A06-01 | `06_structure/queries.py` | category가 있는 경우 정확히 일치하는 항목들의 목록을 반환하세요. 이 함수에서 파일을 읽거나 HTTPException을 사용하지 마세요. |
| A06-02 | `06_structure/queries.py` | entries에서 ID가 같은 항목을 찾아 반환하세요. 없으면 아래 return None으로 진행하세요. |
| A07-01 | `07_project/main.py` | 읽은 entries와 category를 select_category에 넘겨 결과를 응답하세요. |
| A07-02 | `07_project/main.py` | 생성할 entry를 한 번 추가하고 next_id를 한 번 증가시키세요. |
| A07-03 | `07_project/main.py` | 수정 대상 위치를 updated로 교체하세요. |
| A07-04 | `07_project/main.py` | 삭제 성공에서 빈 204 응답을 반환하세요. |
