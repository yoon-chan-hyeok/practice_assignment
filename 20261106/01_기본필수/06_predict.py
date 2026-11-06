"""실습 06. 강사가 준비한 실제 도형 YOLO weight로 valid 이미지만 추론합니다."""
from pathlib import Path
import cv2
import torch
import pandas as pd
from ultralytics import YOLO
BASE = Path(__file__).resolve().parent
torch.set_num_threads(1)
# data/demo.pt는 교실 사전 준비 도구로 생성합니다. 임의 모델로 자동 대체하지 않습니다.
model = YOLO(str(BASE / "data/demo.pt"))
rows = []; counts = []
# >>> B07
# 요구: data/images/val을 conf=0.25, imgsz=160, CPU로 predict 하세요.
# source는 입력 경로, conf/imgsz/device는 선택 인자입니다.
pass  # TODO B07: 위 요구사항의 핵심 코드를 작성하세요.
# <<< B07
for result in results:
    name = Path(result.path).stem
    counts.append({"image": name, "detections": len(result.boxes)})
    cv2.imwrite(str(BASE / ("p06_" + name + ".png")), result.plot())
    for box, cls, score in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.cls.cpu().tolist(), result.boxes.conf.cpu().tolist()):
        rows.append([name, int(cls), score, *box])
pd.DataFrame(rows, columns=["image", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv(BASE/"p06_predictions.csv", index=False)
pd.DataFrame(counts).to_csv(BASE/"p06_counts.csv", index=False)
print("처리 이미지:", len(counts), "탐지 수:", len(rows))
