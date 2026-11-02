import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)

from torch.nn.utils.rnn import pad_sequence
# 서로 길이가 다른 3개 자료. 각 시점의 특성 수는 3개이다.
sequences = [torch.ones(4,3), torch.ones(2,3)*2, torch.ones(5,3)*3]
# TODO B01: B가 첫 축인 [3,5,3] Padding Tensor를 만든다.
# batch_first의 기본값은 False이다. 여기서는 True로 바꾼다.
# BEGIN B01
padded = pad_sequence(sequences, batch_first=False)
# END B01
print("입력 길이:", [len(x) for x in sequences])
print("Padding shape:", tuple(padded.shape))
print("두 번째 자료:\n", padded[1])
