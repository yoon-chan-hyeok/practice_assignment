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

rows=[]
for name,doc in lesson['documents'].items():
    fields=extract(doc['ocr']['text'],doc['ocr']['tokens'])
# TODO C04
    result = {}
# TODO 끝 C04
    for field,f in result.items():
        rows.append({'document_id':name,'field':field,'backend':'mock','supported':f['evidence_supported_by_ocr'],'review':f['review']})
pd.DataFrame(rows).to_csv(out/'evidence_review.csv',index=False,encoding='utf-8-sig')
print('지원된 답:',sum(r['supported'] for r in rows),'검토:',sum(r['review'] for r in rows))
