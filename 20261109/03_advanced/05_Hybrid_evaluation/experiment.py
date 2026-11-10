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
    combined=reconcile(fields,doc['mock_vlm']['responses'])
    responses={r['field']:r for r in doc['mock_vlm']['responses']}
    for field,gold in doc['truth'].items():
        choices={'ocr_recorded':fields[field]['value'],'vlm_mock':responses[field]['answer'],'hybrid_review':combined[field]['final_value']}
        for mode,value in choices.items():
# TODO C05
            pass
# TODO 끝 C05
table=pd.DataFrame(rows)
table.to_csv(out/'field_evaluation.csv',index=False,encoding='utf-8-sig')
summary=table.groupby('mode')[['exact','answered','review']].sum()
print(summary.to_string()); print('각 mode 분모 15. 답변 보류를 정답으로 세지 않습니다. 속도 비교 없음.')
