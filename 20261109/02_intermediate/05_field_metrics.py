from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
import cv2
base = Path(__file__).resolve().parent
data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

rows = []
for name, doc in lesson['documents'].items():
    for item in doc['mock_vlm']['responses']:
         # ========================================================
        # TODO A05: Mock VLM 답변과 실제 정답 비교
        # ========================================================
        #
        # [요구사항]
        # 1. 현재 VLM 응답(item)에서 평가할 필드명을 확인하세요.
        #    - item['field']: 평가 대상 필드
        #    - 예: issued_at, supplier, total_amount
        #
        # 2. 현재 VLM 응답에서 해당 필드의 예측값을 가져오세요.
        #    - 예: "2026-11-09", "ABC Company", 150000
        #
        # 3. lesson.json에서 현재 문서(doc)의 실제 정답을 가져오세요.
        #    - item['field']에 해당하는 정답값을 선택합니다.
        #
        # 4. VLM 예측값과 실제 정답값을 비교하세요.
        #    - 두 값이 정확히 일치하면 exact = True
        #    - 두 값이 일치하지 않으면 exact = False
        #
        # [비교 예시]
        # 예측: "2026-11-09" / 정답: "2026-11-09" → True
        # 예측: "ABC Company" / 정답: "XYZ Company" → False
        # 예측: 150000 / 정답: 150000 → True
        #
        # [주의사항]
        # - 실제 정답은 평가할 때만 사용합니다.
        # - 문자열과 숫자의 자료형을 확인하여 비교하세요.
        # - 공백, 대소문자 등도 정확 일치 여부에 영향을 줍니다.
        # - exact에는 반드시 True 또는 False를 저장하세요.
        # - 예측값과 정답값의 실제 JSON 키는 lesson.json에서 확인하세요.
        #
        # [기대 결과]
        # 각 문서의 Mock VLM 응답을 실제 정답과 비교하고,
        # 전체 응답 중 정확히 일치한 필드 개수를 집계합니다.
        # ========================================================
        exact = False
        # TODO 끝 A05
        grounded = item['evidence'] in doc['ocr']['text']
        rows.append({'document_id':name, 'field':item['field'], 'backend':'mock', 'exact':exact, 'evidence_found':grounded, 'review':not grounded})
table = pd.DataFrame(rows)
table.to_csv(out / 'p05_scores.csv', index=False, encoding='utf-8-sig')
print('값 일치:', int(table['exact'].sum()), '/', len(table))
print('값과 문자열 근거:', int((table['exact'] & table['evidence_found']).sum()), '/', len(table))
print('추론 지연시간: N/A (mock)')
