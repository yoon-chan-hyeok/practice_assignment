"""실습 01: 정상 문서 3장을 Gray와 Otsu로 변환합니다. 원본을 덮어쓰지 않습니다."""
from pathlib import Path
import cv2

base = Path(__file__).resolve().parent
for name in ['doc01', 'doc02', 'doc03']:
    image = cv2.imread(str(base / f'{name}.png'))
    # 아래 두 줄만 완성합니다. 출력은 채널이 없는 (높이, 너비) 배열입니다.
# TODO B01
    gray = image[:, :, 0] * 0
    threshold, binary = 0, gray
# TODO 끝 B01
    cv2.imwrite(str(base / f'p01_{name}_gray.png'), gray)
    cv2.imwrite(str(base / f'p01_{name}_binary.png'), binary)
    print(name, 'shape:', gray.shape, 'threshold:', threshold)
