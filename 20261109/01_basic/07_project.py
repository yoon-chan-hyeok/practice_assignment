"""실습 07~08: 전처리→제공된 실제 OCR 기록 읽기→필드 저장. 네트워크·GPU 불필요."""
from pathlib import Path
import json
import re
import cv2

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
records = []
for name in ['doc01', 'doc02', 'doc03']:
    image = cv2.imread(str(base / f'{name}.png'))
# TODO B08
    gray = image[:, :, 0] * 0
# TODO 끝 B08
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(str(base / f'p07_{name}_binary.png'), binary)
    # 이 기록은 원본 이미지로 실제 추론한 결과입니다. 방금 만든 binary의 추론 결과가 아닙니다.
    text = lesson['documents'][name]['ocr']['text']
    fields = {'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1), 'supplier': re.search(r'SUPPLIER: (.+)', text).group(1), 'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))}
    records.append({'document_id': name, 'fields': fields, 'raw_text': text, 'ocr_backend': 'recorded_tesseract_on_original', 'vlm_backend': 'not_used'})
    print(name, fields)
# TODO B09
pass
# TODO 끝 B09
print('문서:', len(records), '/ 이진화 PNG 3개 + 최종 JSON 1개')
