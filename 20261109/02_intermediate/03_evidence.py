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

doc = lesson['documents']['doc01']
words = doc['ocr']['tokens']
fields = {}
for key, label in [('issued_at','DATE:'), ('supplier','SUPPLIER:'), ('total_amount','TOTAL:')]:
    anchor = next(w for w in words if w['text'] == label)
    # 같은 block/paragraph/line이고 라벨 오른쪽에 있는 단어만 선택합니다.
# TODO A03
    selected = [anchor]
# TODO 끝 A03
    raw = ' '.join(w['text'] for w in selected)
    value = int(raw) if key == 'total_amount' else raw
    box = [min(w['bbox'][0] for w in selected),min(w['bbox'][1] for w in selected),max(w['bbox'][2] for w in selected),max(w['bbox'][3] for w in selected)]
    fields[key] = {'raw': raw, 'value': value, 'confidence': min(w['conf'] for w in selected), 'bbox': box, 'coordinate_space':'original_pixels'}
(out / 'p03_evidence.json').write_text(json.dumps(fields, ensure_ascii=False, indent=2), encoding='utf-8')
print({k:v['value'] for k,v in fields.items()})
