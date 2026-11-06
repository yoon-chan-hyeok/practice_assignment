"""실습 04. 무작위 초기화 YOLO26의 1 epoch 학습 연결 점검. 성능 실험이 아닙니다."""
from pathlib import Path
import yaml
import torch
from ultralytics import YOLO
BASE = Path(__file__).resolve().parent
# Windows에서도 읽기 worker가 스크립트를 재실행하지 않도록 진입점을 구분합니다.
if __name__ == "__main__":
    torch.set_num_threads(1)
    config = {"train": str(BASE/"data/images/train"), "val": str(BASE/"data/images/val"),
              "names": ["square", "circle", "triangle"]}
    config_path = BASE / "p04_dataset.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    model = YOLO("yolo26n.yaml")  # 구조만 생성합니다. COCO 사전학습 .pt와 다릅니다.
    # >>> B05
    # 요구: config_path로 1 epoch, imgsz=160, batch=4, CPU 학습을 호출하세요.
    # 나머지 옵션은 제공한 그대로 유지하세요. test 경로는 전달하지 않습니다.
    pass  # TODO B05: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< B05
    print("task:", model.task, "names:", model.names, "device:", model.device)
    print("학습 결과:", BASE/"p04_runs/smoke")
