"""실습 01 · RGB 이미지의 N,C,H,W를 확인한다. 실제 사진 대신 정상 Tensor 4장."""
import torch

torch.manual_seed(42)
# 해설 B01: rand의 네 크기는 이미지 수, 채널, 높이, 너비이다.
# 필수: 각 차원의 크기. 선택: dtype, device. 기본 float32·CPU를 사용한다.
# BEGIN B01
# TODO B01: RGB 이미지 4장, 높이·너비 32인 Tensor를 만든다.
images = torch.rand(1, 3, 32, 32)
# END B01
print("shape:", tuple(images.shape))
print("dtype:", images.dtype)
print("device:", images.device)
print("첫 이미지:", tuple(images[0].shape))
