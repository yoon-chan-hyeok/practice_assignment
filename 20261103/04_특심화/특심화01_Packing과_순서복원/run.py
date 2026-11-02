"""제공 실행기. 학습 대상은 tasks.py이며 이전 실습 파일은 필요 없다."""
from pathlib import Path
import json
import torch
from torch import nn
from support import init,write_json
from tasks import *
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)
init()

from torch.nn.utils.rnn import pad_sequence
lengths=torch.tensor([4,2,5,4])
x=pad_sequence([torch.randn(int(n),3) for n in lengths],batch_first=True)
restored=[]; gradients=[]
for sort in [False,True]:
    source=x.clone().requires_grad_()
    packed,undo=pack_ordered(source,lengths,sort)
    back,lens=restore_padded(packed,undo,5)
    assert torch.equal(back,x) and torch.equal(lens,lengths)
    back.square().sum().backward()
    restored.append(back.detach());gradients.append(source.grad)
assert torch.equal(gradients[0],gradients[1])
result={'shape':list(x.shape),'packed_rows':int(lengths.sum()),'lengths':lengths.tolist(),
        'value_roundtrip':True,'gradient_equivalent':True,'independent_lesson':1}
write_json(OUT,'packing_check.json',result)
print(json.dumps(result,ensure_ascii=False,sort_keys=True))
