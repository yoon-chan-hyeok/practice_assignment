from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("scene.png")
# >>> TODO B06
# cv2.flip(image, 1)로 좌우 반전한 flipped를 만드세요. 세로 반전은 flipCode=0입니다.
flipped = image.copy()
# <<< TODO B06
# 음수 beta를 사용해도 절댓값 반전이 생기지 않도록 float에서 clip합니다.
bright = np.clip(image.astype(np.float32) + 30, 0, 255).astype(np.uint8)
comparison = cv2.hconcat([image, flipped, bright])
cv2.imwrite("p06_comparison.png", comparison)
print("왼쪽 원본 / 가운데 좌우반전 / 오른쪽 +30 밝기")
print("비교 그림 Shape:", comparison.shape)
print("밝기 범위:", int(bright.min()), int(bright.max()))
