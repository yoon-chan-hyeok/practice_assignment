"""실습 07~08: 기본 recorded OCR + mock VLM. --ocr live는 실제 OCR을 한 번에 호출합니다."""
from pathlib import Path
import argparse
import json
import hashlib
import cv2
import pandas as pd
from fields import extract, extract_items, validate, reconcile
from evaluate import field_scores

base=Path(__file__).resolve().parent
data=base.parent/'data'
out=base/'outputs';out.mkdir(exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--ocr',choices=['recorded','live'],default='recorded')
args=parser.parse_args()
lesson=json.loads((data/'lesson.json').read_text(encoding='utf-8'))
docs=lesson['documents']; records=[d['ocr'] for d in docs.values()]; batch_seconds=None
if args.ocr=='live':
    from ocr_backend import live_batch
    records,batch_seconds=live_batch([data/d['file'] for d in docs.values()])
final=[]; scores=[]
for (name,doc),ocr in zip(docs.items(),records):
    image=cv2.imread(str(data/doc['file']))
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,binary=cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    cv2.imwrite(str(out/f'{name}_binary.png'),binary)
    annotated=image.copy()
    for t in ocr['tokens']:
        x1,y1,x2,y2=t['bbox'];cv2.rectangle(annotated,(x1,y1),(x2,y2),(255,0,0),1)
    cv2.imwrite(str(out/f'{name}_boxes.png'),annotated)
    fields=extract(ocr['text'],ocr['tokens']); items=extract_items(ocr['text'])
    reasons=validate(fields,items)
    combined=reconcile(fields,doc['mock_vlm']['responses'])
    for k,field in fields.items():
        if field['bbox'] is not None:
            x1,y1,x2,y2=field['bbox'];cv2.imwrite(str(out/f'{name}_{k}_evidence.png'),image[y1:y2,x1:x2])
    final.append({'schema_version':'invoice-v1','document_id':name,'image_sha256':hashlib.sha256((data/doc['file']).read_bytes()).hexdigest(),'ocr_backend':ocr['backend'],'vlm_backend':'mock','raw_text':ocr['text'],'fields':combined,'items':items,'validation':reasons})
    # 정답은 추출이 끝난 후 평가에만 사용합니다.
    scores.extend({'document_id':name,**r} for r in field_scores(fields,doc['truth']))
# TODO C10
pass
# TODO 끝 C10
pd.DataFrame(scores).to_csv(out/'field_evaluation.csv',index=False,encoding='utf-8-sig')
(out/'run_status.json').write_text(json.dumps({'ocr':args.ocr,'vlm':'mock','actual_vlm_inference':False,'ocr_batch_seconds':batch_seconds,'per_document_inference_seconds':None},indent=2),encoding='utf-8')
print('문서:',len(final),'필드 일치:',sum(r['exact'] for r in scores),'/',len(scores))
print('검토 필드:',sum(f['review'] for d in final for f in d['fields'].values()),'VLM: mock')
