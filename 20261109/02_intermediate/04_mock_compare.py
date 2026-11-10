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
    for answer in doc['mock_vlm']['responses']:
        # 문자열 포함 검사는 1차 점검일 뿐 의미상 올바른 답임을 증명하지 않습니다.
# TODO A04
        evidence_found = False
# TODO 끝 A04
        rows.append({'document_id':name, 'backend':'mock', **answer, 'evidence_found':evidence_found, 'review':not evidence_found})
table = pd.DataFrame(rows)
table.to_csv(out / 'p04_mock_review.csv', index=False, encoding='utf-8-sig')
print('mock 필드:', len(table), '근거 문자열 발견:', int(table['evidence_found'].sum()))
print('모의 응답의 평가 연습이며 실제 VLM 정확도가 아닙니다.')
