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
image = cv2.imread(str(data / doc['file']))
for word in doc['ocr']['tokens']:
    x1, y1, x2, y2 = word['bbox']
# TODO A02
    pass
# TODO 끝 A02
cv2.imwrite(str(out / 'p02_word_boxes.png'), image)
# PSM을 실시간으로 반복 호출하지 않고 모드와 적합한 입력을 설계합니다.
print('단어:', len(doc['ocr']['tokens']), 'backend:', doc['ocr']['backend'])
print('PSM 3: 전체 문서 / PSM 6: 균일한 글 블록 / PSM 7: 한 줄 crop')
for record in lesson['psm_records']:
    print('PSM', record['psm'], record['region'], '->', repr(record['text'][:65]))
print('PSM 7은 한 줄 crop입니다. 전체 페이지와 입력 범위가 다르므로 CER을 직접 순위화하지 않습니다.')
