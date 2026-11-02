import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

from time import perf_counter
x = torch.randn(16,12,3)
model = nn.RNN(3,8,batch_first=True).eval()
repeats = 30
with torch.inference_mode():
    for _ in range(5): model(x)  # 워밍업은 측정에서 제외
    start = perf_counter()
    for _ in range(repeats): model(x)
    elapsed = perf_counter()-start
# TODO B07: 반복 전체에서 처리한 샘플 수를 경과 시간으로 나눈다.
# 초당 샘플 수 = batch 수 × 반복 수 / 초. 숫자는 PC마다 달라진다.
# BEGIN B07
throughput = len(x)/elapsed
# END B07
print("범위: CPU / forward만 / gradient 없음 / B=16,T=12,F=3")
print("반복:",repeats,"경과 초:",round(elapsed,6))
print("samples/s:",round(throughput,2))
print("GPU peak VRAM: N/A (이 파일은 CPU 전용)")
