from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

import csv

# 결과 이름의 p07_ 접두어가 입력 파일 덮어쓰기를 방지합니다.
rows = []
for filename in ["scene.png", "noisy.png", "objects.png"]:
    image = cv2.imread(filename)
    # >>> TODO B07
    # image를 Gray로 만든 뒤 (너비160, 높이120)으로 축소하세요. 변수는 gray, small입니다.
    gray = image[:, :, 0]
    small = gray.copy()
    # <<< TODO B07
    # >>> TODO B08
    # 축소한 small에 Canny 80,160을 적용하여 edge를 만드세요.
    edge = small.copy()
    # <<< TODO B08
    stem = Path(filename).stem
    cv2.imwrite(f"p07_{stem}_gray.png", gray)
    cv2.imwrite(f"p07_{stem}_small.png", small)
    cv2.imwrite(f"p07_{stem}_edge.png", edge)
    rows.append([filename, image.shape[1], image.shape[0], small.shape[1], small.shape[0], int(np.count_nonzero(edge))])

cap = cv2.VideoCapture("sample.avi")
fps = cap.get(cv2.CAP_PROP_FPS)
writer = cv2.VideoWriter("p07_video.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (160, 120))
print("Writer:", writer.isOpened())
count = 0
while cap.isOpened() and writer.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    # >>> TODO B09
    # 각 frame에도 같은 Gray→160×120 Resize→Canny 순서를 적용하세요. 마지막 변수는 frame_edge입니다.
    frame_gray = frame[:, :, 0]
    frame_small = cv2.resize(frame_gray, (160, 120))
    frame_edge = frame_small.copy()
    # <<< TODO B09
    writer.write(cv2.cvtColor(frame_edge, cv2.COLOR_GRAY2BGR))
    count += 1
cap.release()
writer.release()
with open("p07_summary.csv", "w", encoding="utf-8-sig", newline="") as f:
    output = csv.writer(f)
    output.writerow(["source", "source_w", "source_h", "output_w", "output_h", "edge_pixels"])
    output.writerows(rows)

# 실습08: 파일을 실제로 다시 읽습니다. 성공 메시지만으로 완료 판단하지 않습니다.
check = cv2.VideoCapture("p07_video.avi")
print("이미지 수/Frame 수:", len(rows), count)
print("재읽기 이미지 Shape:", cv2.imread("p07_scene_edge.png", 0).shape)
print("재읽기 영상 Frame/FPS:", int(check.get(cv2.CAP_PROP_FRAME_COUNT)), check.get(cv2.CAP_PROP_FPS))
check.release()
print("결과: p07_ PNG 9개 + AVI 1개 + CSV 1개")
