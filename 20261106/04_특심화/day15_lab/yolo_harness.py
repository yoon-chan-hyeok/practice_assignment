"""선택: 실제 YOLO 스트리밍 + artifact manifest. 사전 준비 모델이 필요합니다."""
from pathlib import Path
import argparse,json,hashlib
from artifacts import run_artifacts,canonical_hash

class Detector:
    def __init__(self,weight):
        from ultralytics import YOLO
        self.model=YOLO(str(weight))
    def __call__(self,path):
        r=self.model.predict(source=str(path),conf=.25,imgsz=160,device='cpu',verbose=False)[0]
        return dict(backend='ultralytics_yolo26',image=path.name,boxes=r.boxes.xyxy.cpu().tolist(),classes=r.boxes.cls.cpu().int().tolist(),confidence=r.boxes.conf.cpu().tolist())

if __name__=='__main__':
    import torch
    torch.set_num_threads(1)
    base=Path(__file__).resolve().parent;weight=base/'data/demo.pt'
    config=dict(backend='ultralytics_yolo26',weight_sha=hashlib.sha256(weight.read_bytes()).hexdigest(),conf=.25,imgsz=160,device='cpu')
    processor=Detector(weight)
    events=run_artifacts(sorted((base/'data/images/val').glob('*.png')),base/'outputs/yolo_artifacts',config,processor)
    print(events)
