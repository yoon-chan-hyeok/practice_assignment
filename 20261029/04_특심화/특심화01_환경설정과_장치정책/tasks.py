"""실습 01 · 장치 선택. 함수 문법보다 요구사항의 분기·검증 범위를 읽으세요."""
import torch

def choose_device(requested: str = "cpu") -> torch.device:
    # [요구사항 X01-1 | 장치 선택]
    # 입력: requested는 "cpu", "auto", "cuda" 중 하나인 문자열이다.
    # 출력: torch.device 객체. "cuda"를 반환할 때는 인덱스를 0으로 명시한다.
    # 규칙 1: cpu는 CUDA 검사 결과와 무관하게 cpu를 반환한다.
    # 규칙 2: auto는 is_available()이 True일 때 cuda:0, 아니면 cpu를 반환한다.
    # 규칙 3: 명시적 cuda 요청인데 사용할 수 없으면 RuntimeError를 발생시킨다.
    # 규칙 4: 그 외 값은 ValueError. 잘못된 요청을 조용히 cpu로 바꾸지 않는다.
    # 부작용 금지: 드라이버 설치, 파일 수정, shell 명령 실행, 전역 기본장치 변경을 하지 않는다.
    # CPU 환경 완료 기준: cpu/auto 성공, cuda는 명확한 실패, 잘못된 문자열은 ValueError.
    # GPU 보유 여부는 점수 조건이 아니다. 실제 CUDA 연산 검사는 장치가 있을 때만 수행한다.
    # >>> X01-1
    # TODO X01-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-1")
    # <<< X01-1

def environment_record(device):
    # 아래 기록 코드는 제공됩니다. 드라이버 버전은 README의 nvidia-smi 절차로 별도 기록합니다.
    info = {"torch": str(torch.__version__), "cuda_build": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(), "selected_device": str(device)}
    if device.type == "cuda":
        info["gpu_name"] = torch.cuda.get_device_name(device)
        info["vram_bytes"] = torch.cuda.get_device_properties(device).total_memory
    return info


def probe_device(requested="cpu"):
    # [요구사항 X01-2 | 실제 연산 결과를 환경 기록에 연결]
    # choose_device로 장치를 선택한 뒤 [1.,2.] float32 Tensor를 해당 장치에서 생성합니다.
    # +1 연산을 수행하고 결과를 CPU Python list로 옮깁니다.
    # 반환 dict: environment_record의 항목 + tensor_device(str) + result([2.0,3.0]).
    # requested="cuda" 실패를 잡아서 CPU 성공처럼 기록하면 안 됩니다. 오류는 호출자에게 전달합니다.
    # 전역 기본 장치 변경·드라이버 설치·nvidia-smi 실행·난수 사용 금지.
    # CPU의 gpu_name/VRAM을 꾸며 넣지 않습니다. str(torch.__version__)을 사용합니다.
    # 완료: json.dumps 가능한 dict이며 selected_device와 tensor_device가 일치합니다.
    # >>> X01-2
    # TODO X01-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X01-2")
    # <<< X01-2
