"""실습 03: 실제 OCR 기록에서 필요한 3개 필드를 추출합니다. 정상 자료만 사용합니다."""
from pathlib import Path
import json
import re

base = Path(__file__).resolve().parent
docs = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))['documents']
records = []
for name in ['doc01', 'doc02', 'doc03']:
    text = docs[name]['ocr']['text']
    # DATE 줄 뒤의 날짜 부분을 추출합니다. OCR 원문도 함께 보존합니다.
# TODO B03
    issued_at = ''
# TODO 끝 B03
    supplier = re.search(r'^SUPPLIER: (.+)$', text, re.MULTILINE).group(1)
# TODO B04
    total_amount = 0
# TODO 끝 B04
    records.append({'document_id': name, 'issued_at': issued_at, 'supplier': supplier, 'total_amount': total_amount, 'currency': 'KRW', 'ocr_source': 'recorded Tesseract', 'raw_text': text})
    print(name, issued_at, supplier, total_amount)
(base / 'p03_fields.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
