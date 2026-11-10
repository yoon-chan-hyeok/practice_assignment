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
for key, sample in lesson['variants'].items():
    rows.append({'case':sample['slice'],'candidate':sample['candidate'],'cer':cer(sample['reference_text'],sample['ocr']['text']), 'backend':'recorded_tesseract','inference_ms':None})
table=pd.DataFrame(rows)
# 같은 개발 문서에서 선택한 결과입니다. 독립 test 성능이 아닙니다.
# TODO C01
best = table.head(3)
# TODO 끝 C01
table.to_csv(out/'candidates.csv',index=False,encoding='utf-8-sig')
best.to_csv(out/'selected.csv',index=False,encoding='utf-8-sig')
print(best[['case','candidate','cer']].round(4).to_string(index=False))
