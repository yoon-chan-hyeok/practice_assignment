"""공통 지원: 경로, 장치 선택, 모델 로딩, 로그. 수강생은 보통 수정하지 않습니다."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform
import sys

BASE = Path(__file__).resolve().parent
DEFAULT_MODEL = "weights/yolo26n.pt"


def project_path(value: str | Path) -> Path:
    """상대경로는 터미널 위치가 아니라 프로젝트 폴더 기준입니다."""
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (BASE / path).resolve()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def new_run_dir(prefix: str) -> Path:
    # 실행마다 새 폴더를 만들어 기존 실험 결과를 덮어쓰지 않습니다.
    path = BASE / "outputs" / f"{prefix}_{datetime.now():%Y%m%d_%H%M%S_%f}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def environment() -> dict:
    versions = {}
    for name in ("ultralytics", "torch", "torchvision", "opencv-python", "numpy", "PyYAML"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": versions}


def choose_device(requested: str = "auto") -> str:
    import torch
    requested = str(requested).lower()
    if requested == "auto":
        return "0" if torch.cuda.is_available() else "cpu"
    if requested == "cpu":
        return requested
    index = requested.replace("cuda:", "")
    if index.isdigit() and torch.cuda.is_available() and int(index) < torch.cuda.device_count():
        return index
    raise ValueError("사용할 CUDA 장치를 찾지 못했습니다. --device cpu 또는 --device auto를 사용하세요.")


def synchronize(device: str) -> None:
    import torch
    if device != "cpu":
        torch.cuda.synchronize(int(device))


def model_path(value: str = DEFAULT_MODEL) -> Path:
    if value == "custom":
        pointer = BASE / "outputs/latest_custom.json"
        if not pointer.is_file():
            raise FileNotFoundError("추가 학습 모델이 없습니다. 먼저 train_custom.py를 실행하세요.")
        value = json.loads(pointer.read_text(encoding="utf-8"))["best_pt"]
    path = project_path(value)
    if path.suffix.lower() != ".pt":
        raise ValueError("추론/추가 학습 시작에는 .yaml이 아니라 학습된 .pt 가중치를 지정하세요.")
    if not path.is_file() and path != project_path(DEFAULT_MODEL):
        raise FileNotFoundError(f"가중치 파일이 없습니다: {path}")
    return path


def load_detector(value: str = DEFAULT_MODEL):
    from ultralytics import YOLO
    path = model_path(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        print("[최초 준비] 공식 yolo26n.pt를 다운로드합니다. 인터넷 연결이 필요합니다.")
    # 공식 모델 이름을 사용하면 Ultralytics가 누락된 가중치를 다운로드합니다.
    # 알 수 없는 출처의 .pt는 로드하지 마세요.
    model = YOLO(str(path))
    if model.task != "detect":
        raise ValueError("객체 탐지(detect) 모델만 지원합니다. 분류/분할 모델은 사용할 수 없습니다.")
    return model, path


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def open_capture(source: int | str):
    """Windows 카메라는 DirectShow를 먼저 시도하고 기본 backend로 재시도합니다."""
    import cv2
    backends = [cv2.CAP_DSHOW, cv2.CAP_ANY] if isinstance(source, int) and sys.platform == "win32" else [cv2.CAP_ANY]
    for backend in backends:
        capture = cv2.VideoCapture(source, backend)
        if capture.isOpened():
            return capture
        capture.release()
    raise RuntimeError("입력을 열 수 없습니다. 카메라 권한/다른 앱 점유/--source 1 또는 영상 경로를 확인하세요.")


def save_png(path: Path, image) -> None:
    # imwrite의 Windows 비ASCII 경로 문제를 피하기 위해 인코딩 후 Path로 저장합니다.
    import cv2
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError(f"PNG 인코딩 실패: {path}")
    path.write_bytes(encoded.tobytes())
