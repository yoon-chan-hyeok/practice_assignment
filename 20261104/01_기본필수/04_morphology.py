from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("objects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold_value, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), dtype=np.uint8)
# >>> TODO B04
# binary에 3×3 kernel을 사용한 Opening을 적용하세요. 결과 이름은 opened입니다.
opened = binary.copy()
# <<< TODO B04
cv2.imwrite("p04_gray.png", gray)
cv2.imwrite("p04_binary.png", binary)
cv2.imwrite("p04_open.png", opened)
print("임계값:", threshold_value)
print("전경 픽셀:", int(np.count_nonzero(binary)), "->", int(np.count_nonzero(opened)))
print("결과 값:", np.unique(opened).tolist())
