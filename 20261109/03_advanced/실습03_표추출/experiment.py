from pathlib import Path
import sys
import json
import cv2
import numpy as np
import pandas as pd
base = Path(__file__).resolve().parent
root = base.parent
data = root / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
sys.path.insert(0, str(root / 'day16_documents'))
from fields import extract, extract_items, validate, reconcile
from evaluate import cer
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

doc=lesson['documents']['doc03']
fields=extract(doc['ocr']['text'],doc['ocr']['tokens'])
# TODO C03
items = []
# TODO 끝 C03
reasons=validate(fields,items)
record={'schema_version':'invoice-v1','document_id':'doc03','fields':fields,'items':items,'review_reasons':reasons}
(out/'invoice.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print('품목 수:',len(items),'총금액:',fields['total_amount']['value'],'검토 이유:',reasons)
