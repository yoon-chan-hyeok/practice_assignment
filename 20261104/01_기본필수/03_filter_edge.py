from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("noisy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# >>> TODO B03
# gray를 (5,5), sigmaX=0으로 흐리게 하여 blur를 만드세요. blur에 Canny 80,160을 적용하여 edge를 만드세요.
blur = gray.copy()
edge = gray.copy()
# <<< TODO B03
cv2.imwrite("p03_blur.png", blur)
cv2.imwrite("p03_edge.png", edge)
print("설정: Gaussian (5,5), sigmaX=0, Canny 80/160")
print("Shape:", blur.shape, edge.shape)
print("Edge 픽셀:", int(np.count_nonzero(edge)))
