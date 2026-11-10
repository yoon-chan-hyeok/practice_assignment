# TODO 위치와 완료 요구사항

같은 ID가 강사용 정답의 같은 위치에 있습니다. 일반 힌트보다 각 코드 안의 요구사항을 먼저 읽으세요.

| ID | 위치 | 요구사항 |
|---|---|---|
| B01-01 | `01_first_server/main.py` | status 키의 값이 ok인 dict를 반환하세요. GET /health의 본문은 {"status":"ok"}여야 합니다. |
| B02-01 | `02_read/main.py` | 파일 전체 data에서 entries 목록만 반환하세요. next_id가 포함된 dict 전체를 반환하지 마세요. |
| B02-02 | `02_read/main.py` | 현재 entry의 id와 요청 knowledge_id가 같은지 비교하여 same_id에 저장하세요. |
| B03-01 | `03_create/main.py` | 새 entry를 data 안의 entries 목록 끝에 한 번 추가하세요. |
| B03-02 | `03_create/main.py` | 다음 생성에 쓸 next_id 값을 1 증가시키세요. |
| B03-03 | `03_create/main.py` | 변경된 data 전체를 write_data에 전달해 저장하세요. LOCK 블록 안에서 호출하세요. |
| B04-01 | `04_update/main.py` | 현재 지식의 id와 요청 ID를 비교해 same_id에 넣으세요. |
| B04-02 | `04_update/main.py` | 찾은 위치 i의 지식 한 개를 updated로 교체하세요. append로 추가하지 마세요. |
| B04-03 | `04_update/main.py` | 교체한 data를 같은 LOCK 블록 안에서 파일에 저장하세요. |
| B05-01 | `05_delete/main.py` | 찾은 위치 i의 지식 한 개만 entries에서 제거하세요. 파일 전체를 삭제하지 마세요. |
| B05-02 | `05_delete/main.py` | 제거한 결과를 파일에 저장하세요. 다른 항목과 next_id는 유지하세요. |
| B07-01 | `07_project/main.py` | 통합 목록 Route에서 entries만 응답하도록 연결하세요. |
| B07-02 | `07_project/main.py` | 생성된 지식과 증가한 next_id를 파일에 함께 저장하세요. |
| B07-03 | `07_project/main.py` | 같은 ID의 위치 i를 updated로 교체하세요. |
| B07-04 | `07_project/main.py` | 삭제 저장 후 본문 없는 204 응답을 반환하세요. dict 또는 JSON 문자열을 넣지 마세요. |
