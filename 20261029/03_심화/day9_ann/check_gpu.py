"""장치 선택과 기록만 담당하는 제공 코드입니다."""
import torch

def choose_device():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    info = {"torch": str(torch.__version__), "cuda_build": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(), "selected_device": str(device)}
    if device.type == "cuda":
        info["gpu_name"] = torch.cuda.get_device_name(device)
        info["vram_gib"] = torch.cuda.get_device_properties(device).total_memory / 1024**3
    return device, info
