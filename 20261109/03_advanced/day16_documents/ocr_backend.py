"""선택 실제 OCR backend: 파일 목록을 한 번에 읽습니다. 실패를 기록 재생으로 바꾸지 않습니다."""
from pathlib import Path
import tempfile
import os
import time
from collections import defaultdict
import pytesseract

def live_batch(paths, psm=6):
    pytesseract.pytesseract.tesseract_cmd=os.environ.get('TESSERACT_CMD','tesseract')
    with tempfile.TemporaryDirectory() as tmp:
        manifest=Path(tmp)/'images.txt'
        manifest.write_text('\n'.join(str(Path(p).resolve()) for p in paths),encoding='utf-8')
        start=time.perf_counter()
        data=pytesseract.image_to_data(str(manifest),lang='eng',config=f'--psm {psm}',output_type=pytesseract.Output.DICT,timeout=60)
        elapsed=time.perf_counter()-start
    records=[]
    for page in range(1,len(paths)+1):
        tokens=[]
        for i,text in enumerate(data['text']):
            if int(data['page_num'][i])!=page or not str(text).strip() or float(data['conf'][i])<0:continue
            x,y,w,h=[int(data[k][i]) for k in ('left','top','width','height')]
            tokens.append({'text':str(text),'conf':float(data['conf'][i]),'bbox':[x,y,x+w,y+h],'page':1,'block':int(data['block_num'][i]),'paragraph':int(data['par_num'][i]),'line':int(data['line_num'][i]),'word':int(data['word_num'][i])})
        groups=defaultdict(list)
        for t in tokens:groups[(t['page'],t['block'],t['paragraph'],t['line'])].append(t['text'])
        records.append({'backend':'live_tesseract','text':'\n'.join(' '.join(v) for v in groups.values()),'tokens':tokens,'inference_seconds':None,'timing_note':'batch time stored separately'})
    return records,elapsed
