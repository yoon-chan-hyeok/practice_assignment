import torch
from torch import nn
torch.set_num_threads(1)  # 작은 CPU 실습의 실행 조건을 고정한다.
torch.manual_seed(42)
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
OUT.mkdir(exist_ok=True)
import json
from torch.nn.utils.rnn import pad_sequence
items=json.loads((ROOT/"data"/"sequences.json").read_text(encoding="utf-8"))
tr=[r for r in items if r["split"]=="train"]; va=[r for r in items if r["split"]=="valid"]
max_len=12
xt=pad_sequence([torch.tensor(r["values"]) for r in tr],batch_first=True)
xv=pad_sequence([torch.tensor(r["values"]) for r in va],batch_first=True)
lt=torch.tensor([r["length"] for r in tr]); lv=torch.tensor([r["length"] for r in va])
yt=torch.tensor([r["label"] for r in tr]); yv=torch.tensor([r["label"] for r in va])
mt=torch.arange(xt.size(1)).unsqueeze(0)>=lt.unsqueeze(1)
mv=torch.arange(xv.size(1)).unsqueeze(0)>=lv.unsqueeze(1)
parts=nn.ModuleDict({
    "projection":nn.Linear(3,8),"position":nn.Embedding(12,8),
    "encoder":nn.TransformerEncoder(nn.TransformerEncoderLayer(8,2,dim_feedforward=16,dropout=0,batch_first=True),1,enable_nested_tensor=False),
    "head":nn.Linear(8,2)})

optimizer=torch.optim.Adam(parts.parameters(),lr=0.01)
for epoch in range(30):
    parts.train(); optimizer.zero_grad()
    embedded=parts["projection"](xt)+parts["position"](torch.arange(xt.size(1)))
    # TODO A06: Transformer에 실제 길이로 만든 Padding Mask를 전달한다.
    # 위치 임베딩은 값 임베딩과 더한다. masked mean에서는 Padding query도 제외한다.
    # BEGIN A06
    encoded=parts["encoder"](embedded)
    # END A06
    pooled=(encoded*(~mt).unsqueeze(-1)).sum(1)/lt.unsqueeze(-1)
    loss=nn.CrossEntropyLoss()(parts["head"](pooled),yt); loss.backward(); optimizer.step()
parts.eval()
with torch.inference_mode():
    embedded=parts["projection"](xv)+parts["position"](torch.arange(xv.size(1)))
    encoded=parts["encoder"](embedded,src_key_padding_mask=mv)
    pooled=(encoded*(~mv).unsqueeze(-1)).sum(1)/lv.unsqueeze(-1)
    pred=parts["head"](pooled).argmax(1)
print("train/valid:",len(tr),len(va),"위치 최대 길이:",12)
print("params:",sum(p.numel() for p in parts.parameters()))
print("valid accuracy:",round((pred==yv).float().mean().item(),3))
pd.DataFrame({"id":[r["id"] for r in va],"actual":yv.tolist(),"prediction":pred.tolist()}).to_csv(OUT/"transformer_predictions.csv",index=False)
