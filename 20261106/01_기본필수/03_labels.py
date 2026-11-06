"""실습 03. 정상 이미지 6장과 YOLO TXT 라벨을 읽습니다."""
from pathlib import Path
import cv2
BASE = Path(__file__).resolve().parent
names = ["square", "circle", "triangle"]
for image_path in sorted((BASE / "data/images/train").glob("*.png"))[:6]:
    image = cv2.imread(str(image_path))
    label_path = BASE / "data/labels/train" / (image_path.stem + ".txt")
    # >>> B04
    # 요구: UTF-8 라벨 파일의 문자열을 읽고 줄 목록으로 나누세요.
    pass  # TODO B04: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< B04
    print(image_path.name, "shape:", image.shape, "boxes:", len(lines))
    for line in lines:
        cls, cx, cy, width, height = map(float, line.split())
        print(" ", names[int(cls)], "normalized:", cx, cy, width, height)
