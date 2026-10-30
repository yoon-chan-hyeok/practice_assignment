"""실습 02: reshape와 broadcasting을 확인합니다."""
import torch

a = torch.arange(6, dtype=torch.float32)
# 원소 6개를 2행 3열로 바꾸어 matrix에 저장하세요.
# 아래 bias는 각 열에 더해집니다.
# >>> A02
# TODO A02: 위 요구사항을 읽고 이 블록을 완성하세요.
matrix = a.reshape(1, 6)
# <<< A02
bias = torch.tensor([10., 20., 30.])
result = matrix + bias
print("변환 전:", tuple(a.shape))
print("행렬:", tuple(matrix.shape), matrix.tolist())
print("보정 후:", tuple(result.shape), result.tolist())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
moved = result.to(device)
print("이동 장치:", moved.device)
print("CPU에서 확인:", moved.cpu().tolist())
