"""실습 02: Tesseract를 실제 호출합니다. 엔진과 eng 언어팩이 필요합니다."""
from pathlib import Path
import os
import pandas as pd
import pytesseract

base = Path(__file__).resolve().parent
# Windows에서 PATH 설정이 어려우면 환경변수 TESSERACT_CMD에 exe 경로를 지정합니다.
pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_CMD', 'tesseract')
paths = [str(base / f'doc{i:02d}.png') for i in range(1, 4)]
input_list = base / 'p02_inputs.txt'
input_list.write_text('\n'.join(paths), encoding='utf-8')
# 여러 페이지를 목록으로 전달해 엔진을 한 번 호출합니다.
# TODO B02
words = pd.DataFrame(columns=['page_num', 'text', 'conf'])
# TODO 끝 B02
words = words.dropna(subset=['text'])
words = words[words['conf'] >= 0]
words.to_csv(base / 'p02_words.csv', index=False, encoding='utf-8-sig')
for page, rows in words.groupby('page_num', sort=True):
    text = ' '.join(rows['text'].astype(str))
    print('page:', page, 'words:', len(rows), 'mean confidence:', round(rows['conf'].mean(), 2))
    print(text)
print('backend: live Tesseract; confidence는 정답 확률이 아닙니다.')
