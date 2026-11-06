"""실습 07~08. 실제 모델의 이미지 탐지와 영상 추적을 연결합니다."""
from pathlib import Path
import cv2
import torch
import pandas as pd
from ultralytics import YOLO
BASE = Path(__file__).resolve().parent
torch.set_num_threads(1)
model = YOLO(str(BASE / "data/demo.pt"))
rows = []
for r in model.predict(source=str(BASE/"data/images/val"), conf=0.25, imgsz=160, device="cpu", verbose=False):
    for box, cls, score in zip(r.boxes.xyxy.cpu().tolist(), r.boxes.cls.cpu().tolist(), r.boxes.conf.cpu().tolist()):
        rows.append([Path(r.path).name, int(cls), score, *box])
pd.DataFrame(rows, columns=["image", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv(BASE/"p07_predictions.csv", index=False)
# 새 영상은 새 모델 인스턴스로 시작하여 이전 추적 상태를 이어붙이지 않습니다.
tracker = YOLO(str(BASE / "data/demo.pt"))
cap = cv2.VideoCapture(str(BASE / "data/demo.avi"))
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
cap.release()
writer = cv2.VideoWriter(str(BASE / "p07_tracked.avi"), cv2.VideoWriter_fourcc(*"MJPG"), fps, size)
tracks = []; frame_rows = []
# >>> B08
# 요구: demo.avi를 ByteTrack으로 읽는 stream=True 결과 generator를 만드세요.
# persist=False는 새로운 파일 스트림의 시작입니다. 같은 파일 내부 프레임은 이어집니다.
pass  # TODO B08: 위 요구사항의 핵심 코드를 작성하세요.
# <<< B08
for frame, result in enumerate(results):
    writer.write(result.plot())
    frame_rows.append([frame, len(result.boxes)])
    if result.boxes.id is not None:
        for box, cls, score, tid in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.cls.cpu().tolist(), result.boxes.conf.cpu().tolist(), result.boxes.id.cpu().tolist()):
            tracks.append([frame, int(tid), int(cls), score, *box])
writer.release()
# >>> B09
# 요구: tracks를 지정한 열 이름의 CSV로 저장하세요. index=False를 사용합니다.
pass  # TODO B09: 위 요구사항의 핵심 코드를 작성하세요.
# <<< B09
pd.DataFrame(frame_rows, columns=["frame", "detections"]).to_csv(BASE/"p07_frames.csv", index=False)
print("입력 fps/size:", fps, size, "처리 Frame:", len(frame_rows))
print("실습 08: 설정을 바꾸지 말고 다시 실행해 Frame 수·CSV·영상을 확인하세요.")
