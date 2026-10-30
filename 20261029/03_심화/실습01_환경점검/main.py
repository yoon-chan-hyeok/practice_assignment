"""실습 01: 실제 선택한 device와 PyTorch 빌드를 구분해 기록합니다."""
from pathlib import Path
import json
import torch

# CUDA 사용 가능 여부를 보고 실행할 장치를 선택하세요.
# 드라이버가 있다는 사실만으로 CUDA를 선택하지 마세요.
# >>> H01
# TODO H01: 위 요구사항을 읽고 이 블록을 완성하세요.
device = torch.device("cpu")
# <<< H01
x = torch.tensor([[1., 2.], [3., 4.]]).to(device)
result = x @ x.T
record = {"torch": str(torch.__version__), "cuda_build": torch.version.cuda,
          "cuda_available": torch.cuda.is_available(), "selected_device": str(device),
          "calculation": result.cpu().tolist()}
if device.type == "cuda":
    record["gpu_name"] = torch.cuda.get_device_name(device)
    record["vram_gib"] = torch.cuda.get_device_properties(device).total_memory / 1024**3
out = Path(__file__).resolve().parent / "outputs"
out.mkdir(exist_ok=True)
(out / "environment.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
