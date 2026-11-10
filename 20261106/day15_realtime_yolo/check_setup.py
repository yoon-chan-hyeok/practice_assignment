"""수업 전 점검: 설치 환경 확인 → 공식 모델 준비 → 빈 이미지 추론. 카메라는 선택 검사."""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=int, default=None, help="예: --camera 0. 생략 시 카메라를 열지 않음")
    args = parser.parse_args()
    missing = []
    for name in ("cv2", "numpy", "torch", "yaml", "ultralytics"):
        try:
            importlib.import_module(name)
            print(f"[OK] {name}")
        except Exception as exc:
            missing.append(f"{name}: {exc}")
    if missing:
        raise RuntimeError("\n".join(missing) + "\n현재 Python에서 python -m pip install -r requirements.txt 실행 후 재점검하세요.")

    import cv2
    import numpy as np
    import torch
    from runtime import BASE, choose_device, environment, load_detector, open_capture, write_json
    torch.set_num_threads(4)
    device = choose_device("auto")
    print(json.dumps(environment(), indent=2, ensure_ascii=False))
    print("CUDA 사용 가능:", torch.cuda.is_available(), "/ 선택 장치:", device)
    model, weight_path = load_detector()
    result = model.predict(np.zeros((240, 320, 3), dtype=np.uint8), imgsz=320, device=device, verbose=False)[0]
    print("[OK] 모델 로딩/빈 이미지 추론 완료. 실제 탐지 성능 평가는 아닙니다.")
    print("모델 클래스 수:", len(model.names), "/ 가중치:", weight_path)
    write_json(BASE / "weights/classes.json", model.names)

    camera_checked = False
    if args.camera is not None:
        cap = open_capture(args.camera)
        try:
            ok, frame = cap.read()
            if not ok or frame is None:
                raise RuntimeError("카메라 프레임을 읽지 못했습니다. 권한 및 카메라 점유 앱을 확인하세요.")
            camera_checked = True
            print("[OK] 카메라 프레임:", frame.shape)
        finally:
            cap.release()
    write_json(BASE / "outputs/setup_check.json", {
        "environment": environment(), "device": device, "model": str(weight_path),
        "model_loaded": True, "blank_frame_inference": True, "camera_checked": camera_checked,
        "camera_id": args.camera, "note": "웹캠 GUI와 실제 탐지 품질은 main.py로 별도 확인합니다.",
    })
    print("\n준비 완료. python main.py 로 실행하세요.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[점검 실패] {exc}")
        raise SystemExit(1)
