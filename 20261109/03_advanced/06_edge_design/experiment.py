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

plan={'status':'DESIGN_ONLY','pipeline':['decode','nvstreammux','nvinfer','optional nvtracker','nvdsosd','sink'],'target_device':None,'jetpack':None,'tensorrt':None,'deepstream':None,'warmup_frames':30,'measure_frames':300,'runs':3,'include_decode':True,'input_size':[640,480],'fps_limit':None}
# TODO C06
plan['measurements'] = []
# TODO 끝 C06
plan['results']={name:None for name in plan['measurements']}
plan['note']='Jetson 공유 메모리를 dGPU 전용 VRAM과 같다고 해석하지 않는다. nvinfer만 연결해 임의 OCR/VLM을 자동 지원한다고 주장하지 않는다.'
(out/'deployment_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(' -> '.join(plan['pipeline'])); print('측정 항목:',len(plan['measurements']),'하드웨어 실행: 미수행')
