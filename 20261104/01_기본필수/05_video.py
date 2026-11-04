from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

cap = cv2.VideoCapture("sample.avi")
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter("p05_gray.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (width, height))
print("열림(입력/출력):", cap.isOpened(), writer.isOpened())
print("입력 FPS/크기:", fps, (width, height))
count = 0
while cap.isOpened() and writer.isOpened():
    ok, frame = cap.read()
    if not ok:  # 영상 끝에 도달하면 반복을 끝냅니다. 예외처리 과제가 아닙니다.
        break
    # >>> TODO B05
    # 현재 frame을 Gray로 변환하여 gray에 넣으세요. VideoCapture는 반복문 밖에서 이미 열었습니다.
    gray = frame[:, :, 0]
    # <<< TODO B05
    # 컬러 Writer에 맞춰 Gray를 3채널로 돌립니다. 색이 생기는 것은 아닙니다.
    writer.write(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))
    count += 1
cap.release()
writer.release()
check = cv2.VideoCapture("p05_gray.avi")
print("처리/재읽기 Frame:", count, int(check.get(cv2.CAP_PROP_FRAME_COUNT)))
print("재읽기 FPS:", check.get(cv2.CAP_PROP_FPS))
check.release()
