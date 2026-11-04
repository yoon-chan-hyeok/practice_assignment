from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("scene.png")
# >>> TODO B02
# image를 Gray와 RGB로 각각 변환하여 gray, rgb에 넣으세요. 두 번째 인자는 변환 코드입니다.
gray = image.copy()
rgb = image.copy()
# <<< TODO B02
small = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
cv2.imwrite("p02_gray.png", gray)
cv2.imwrite("p02_small.png", small)
# RGB 배열은 화면 표시용입니다. imwrite에 그대로 넣지 않습니다.
print("Gray shape:", gray.shape)
print("RGB 빨강:", rgb[30, 30].tolist())
print("Resize shape:", small.shape)
