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
# TODO C02
    score = 0.0
# TODO 끝 C02
    fields=extract(doc['ocr']['text'],doc['ocr']['tokens'])
    correct=sum(f['value']==doc['truth'][k] for k,f in fields.items())
    rows.append({'document_id':name,'cer':score,'field_exact':correct,'field_count':3,'ocr_engine':'5.5.0','inference_ms':None})
pd.DataFrame(rows).to_csv(out/'quality.csv',index=False,encoding='utf-8-sig')
print(pd.DataFrame(rows)[['document_id','cer','field_exact']].round(5).to_string(index=False))
