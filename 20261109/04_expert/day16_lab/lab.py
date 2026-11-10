"""실습 01~08을 잇는 특심화 offline 실행. 실제 VLM/TensorRT 실행으로 보고하지 않습니다."""
from pathlib import Path
import json
import cv2
import numpy as np
from contracts import DocumentPreprocessor,OCRPage,character_error
from extractors import extract_invoice
from policy import parse_vlm,decide,redact_for_demo
from backends import make_backend
from deployment import inspect_plan
from harness import run_documents,atomic_json

base=Path(__file__).resolve().parent;data=base/'data';out=base/'outputs';out.mkdir(exist_ok=True)
lesson=json.loads((data/'lesson.json').read_text(encoding='utf-8'))
image=cv2.imread(str(data/'perspective.png'))
gray,M=DocumentPreprocessor().rectify(image,lesson['perspective']['corners'],(1000,700))
cv2.imwrite(str(out/'rectified.png'),gray)
pts=np.array([[180.,200.],[700.,500.]])
back=DocumentPreprocessor.map_points(DocumentPreprocessor.map_points(pts,M),np.linalg.inv(M))
roundtrip=float(np.abs(back-pts).max())
quality=[]
for name,doc in lesson['documents'].items():
    page=OCRPage.from_tokens(doc['ocr']['tokens'],1000,700)
    extracted=extract_invoice(page,name)
    raw=make_backend('mock',lesson['documents']).ask(name,data/doc['file'])
    parsed=parse_vlm(raw['raw'])
    decisions=decide(extracted['fields'],parsed)
    quality.append({'id':name,'cer':character_error(doc['reference_text'],page.text()),'review_fields':sum(f['status']=='review' for f in decisions.values()),'vlm_backend':'mock'})
manifest={'platform':'Linux','architecture':'x86_64','gpu':'EXAMPLE_ONLY','tensorrt':'11.2','input_name':'images','precision':'fp16','profile':{'min':[1,3,224,224],'opt':[2,3,224,224],'max':[4,3,224,224]},'flags':[]}
contract=inspect_plan(manifest,{k:manifest[k] for k in ('platform','architecture','gpu','tensorrt')},[2,3,224,224])
atomic_json(out/'design_contract.json',{'manifest_is_example':True,**contract})
atomic_json(out/'quality.json',quality)
counts=run_documents(data,out/'documents',{'backend':'mock','min_confidence':80.0,'schema_version':'invoice-v1'})
print('문서:',len(quality),'왕복 오차:',round(roundtrip,8),'픽셀')
print('검토 필드:',sum(r['review_fields'] for r in quality),'실제 VLM 추론: 아니오')
print('처리/재사용/실패:',counts['processed'],counts['reused'],counts['failed'])
print('TensorRT runtime_verified:',contract['runtime_verified'])
print('로그 마스킹 예시:',redact_for_demo('demo@example.invalid 010-0000-0000'))
