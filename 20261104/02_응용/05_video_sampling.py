from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

import csv
import json
from time import perf_counter
Path("outputs").mkdir(exist_ok=True)

rows = []
for every in [1, 3]:
    cap = cv2.VideoCapture("data/sample.avi")
    fps = cap.get(cv2.CAP_PROP_FPS)
    # >>> TODO A05
    # 매 every번째 frame만 저장해도 원래 재생시간을 유지하도록 output_fps를 계산하세요. 이 입력은 48이 1·3으로 나누어떨어집니다.
    output_fps = fps
    # <<< TODO A05
    path = f"outputs/p05_every{every}.avi"
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"MJPG"), output_fps, (160, 120))
    read_count, written = 0, 0
    start = perf_counter()
    while cap.isOpened() and writer.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        if read_count % every == 0:
            small = cv2.resize(frame, (160, 120), interpolation=cv2.INTER_AREA)
            edge = cv2.Canny(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY), 80, 160)
            writer.write(cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR))
            written += 1
        read_count += 1
    cap.release(); writer.release()
    seconds = perf_counter() - start
    check = cv2.VideoCapture(path)
    actual_count = int(check.get(cv2.CAP_PROP_FRAME_COUNT))
    actual_fps = check.get(cv2.CAP_PROP_FPS); check.release()
    rows.append([every, read_count, written, actual_count, actual_fps, read_count/fps, actual_count/actual_fps, seconds, written/seconds])
    print(f"N={every}: 읽기{read_count}, 저장{actual_count}, fps={actual_fps}, 출력초={actual_count/actual_fps:.2f}")
with open("outputs/p05_sampling.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["every", "decoded", "written", "reopened", "fps", "input_duration_s", "output_duration_s", "wall_s", "processed_fps"]); w.writerows(rows)
print("시간은 decode+처리+encode 포함. 모든 입력은 decode하므로 N배 가속을 보장하지 않습니다.")
