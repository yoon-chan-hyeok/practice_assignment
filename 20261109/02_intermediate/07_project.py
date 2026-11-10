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

results = []
for name, doc in lesson['documents'].items():
    image = cv2.imread(str(data / doc['file']))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(str(out / f'{name}_binary.png'), binary)
    text = doc['ocr']['text']
# TODO A07
    fields = {'issued_at':'','supplier':'','total_amount':0}
# TODO 끝 A07
    for response in doc['mock_vlm']['responses']:
# TODO A08
        review = False
# TODO 끝 A08
        results.append({'document_id':name, 'field':response['field'], 'ocr_value':fields[response['field']], 'vlm_answer':response['answer'], 'evidence':response['evidence'], 'review':review, 'ocr_backend':'recorded_tesseract', 'vlm_backend':'mock'})
(out / 'final_fields.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
pd.DataFrame(results).to_csv(out / 'review.csv', index=False, encoding='utf-8-sig')
print('문서:', len(lesson['documents']), '필드:', len(results), '검토:', sum(r['review'] for r in results))
print('정답 파일은 추출·검토 판단에 사용하지 않았습니다.')
