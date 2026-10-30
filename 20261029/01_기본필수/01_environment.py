"""실습 01: 설치된 PyTorch와 CUDA 노출을 확인합니다. GPU가 없어도 CPU로 진행합니다."""
import torch

print("PyTorch:", torch.__version__)
print("PyTorch CUDA 빌드:", torch.version.cuda)
print("CUDA 사용 가능:", torch.cuda.is_available())
# GPU 함수는 사용 가능한 경우에만 호출합니다. 드라이버 번호는 터미널 nvidia-smi에서 별도로 기록합니다.
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM GiB:", round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2))
else:
    print("GPU: 이번 실행에서는 사용하지 않음")
print("이 단계의 연산 장치: cpu")
# 정상 숫자 1.0, 2.0을 담은 Tensor를 sample에 저장하세요.
# 아래 덧셈 결과가 [2.0, 3.0]이면 계산 환경이 준비된 것입니다.
# >>> B01
# TODO B01: 위 요구사항을 읽고 이 블록을 완성하세요.
sample = torch.tensor([0.0, 0.0])
# <<< B01
print("덧셈:", (sample + 1).tolist())
