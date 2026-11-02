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

from copy import deepcopy
from time import perf_counter
from torch.nn.utils.rnn import pack_padded_sequence
rows=[]; prediction_rows=[]; history=[]; class_rows=[]; error_rows=[]
# 03·04의 예측/재구성 표와 함께 제출하는 분류 비교. 작업별 지표는 평균내지 않는다.
for name in ["LSTM","Transformer"]:
    torch.manual_seed(42)
    if name=="LSTM":
        parts=nn.ModuleDict({"core":nn.LSTM(3,8,batch_first=True),"head":nn.Linear(8,2)})
    else:
        parts=nn.ModuleDict({"projection":nn.Linear(3,8),"position":nn.Embedding(12,8),
            "encoder":nn.TransformerEncoder(nn.TransformerEncoderLayer(8,2,dim_feedforward=16,dropout=0,batch_first=True),1,enable_nested_tensor=False),
            "head":nn.Linear(8,2)})
    optimizer=torch.optim.Adam(parts.parameters(),lr=0.01); best=float("inf"); start=perf_counter()
    for epoch in range(1,31):
        parts.train(); optimizer.zero_grad()
        if name=="LSTM":
            output,(h,c)=parts["core"](pack_padded_sequence(xt,lt,batch_first=True,enforce_sorted=False))
            # TODO A08: Packed LSTM의 실제 마지막 상태를 분류 Head에 전달한다.
            # Packed output.data는 순서가 다른 압축된 모든 시점이다. h[-1]은 원래 배치 순서의 마지막 상태이다.
            # BEGIN A08
            pooled=output.data[:len(xt)]
            # END A08
        else:
            z=parts["projection"](xt)+parts["position"](torch.arange(xt.size(1)))
            z=parts["encoder"](z,src_key_padding_mask=mt)
            pooled=(z*(~mt).unsqueeze(-1)).sum(1)/lt.unsqueeze(-1)
        loss=nn.CrossEntropyLoss()(parts["head"](pooled),yt); loss.backward(); optimizer.step()
        parts.eval()
        with torch.inference_mode():
            if name=="LSTM":
                _,(h,c)=parts["core"](pack_padded_sequence(xv,lv,batch_first=True,enforce_sorted=False)); vpool=h[-1]
            else:
                z=parts["projection"](xv)+parts["position"](torch.arange(xv.size(1)))
                z=parts["encoder"](z,src_key_padding_mask=mv)
                vpool=(z*(~mv).unsqueeze(-1)).sum(1)/lv.unsqueeze(-1)
            logits=parts["head"](vpool); score=nn.CrossEntropyLoss()(logits,yv).item(); pred=logits.argmax(1)
        history.append({"model":name,"epoch":epoch,"train_online_loss":loss.item(),"valid_loss":score})
        if score<best:
            best=score; best_epoch=epoch; best_pred=pred.clone(); best_logits=logits.detach().clone(); best_state=deepcopy(parts.state_dict())
    # TODO A09: 저장한 best_state를 모델에 복원한 뒤 valid를 다시 예측한다.
    # 마지막 epoch의 logits를 best 결과로 혼동하지 않는다. 학습·optimizer.step은 다시 하지 않는다.
    # 다음 코드가 사용할 restored_logits는 [valid 수, 2]이다. 기존 예측과의 일치는 아래 제공 코드가 확인한다.
    # BEGIN A09
    pass  # best_state를 parts에 복원하세요.
    # END A09
    parts.eval()
    with torch.inference_mode():
        if name=="LSTM":
            _,(h,c)=parts["core"](pack_padded_sequence(xv,lv,batch_first=True,enforce_sorted=False))
            restored_logits=parts["head"](h[-1])
        else:
            z=parts["projection"](xv)+parts["position"](torch.arange(xv.size(1)))
            z=parts["encoder"](z,src_key_padding_mask=mv)
            restored_logits=parts["head"]((z*(~mv).unsqueeze(-1)).sum(1)/lv.unsqueeze(-1))
    print(name,"최적 모델 출력 일치:",torch.allclose(restored_logits,best_logits,atol=1e-6,rtol=1e-5))
    restored_pred=restored_logits.argmax(1)
    # TODO A10: 클래스별 실제 수·정답 수·Recall 및 실제 오답 목록을 만든다.
    # class_rows: model,class_id,support,correct,recall. 분모0은 recall=0.0.
    # error_rows: model,id,actual,prediction,length. ID는 va 원래 순서로 유지한다.
    # 오답이 없으면 아무 행도 추가하지 않는다. 오답을 만들려고 라벨/모델을 바꾸지 않는다.
    # BEGIN A10
    pass  # 위 요구사항의 class_rows·error_rows를 채우세요.
    # END A10
    elapsed=perf_counter()-start
    rows.append({"model":name,"params":sum(p.numel() for p in parts.parameters()),"best_epoch":best_epoch,
                 "valid_loss":best,"valid_accuracy":(best_pred==yv).float().mean().item(),"training_seconds":elapsed})
    prediction_rows.extend({"model":name,"id":r["id"],"actual":r["label"],"prediction":int(p)} for r,p in zip(va,best_pred))
    torch.save({"state_dict":best_state,"name":name,"max_len":12,"input_features":3,"hidden":8,"class_names":["decreasing","increasing"]},OUT/(name.lower()+"_best.pt"))
pd.DataFrame(rows).to_csv(OUT/"architecture_comparison.csv",index=False)
pd.DataFrame(history).to_csv(OUT/"classification_history.csv",index=False)
pd.DataFrame(prediction_rows).to_csv(OUT/"classification_predictions.csv",index=False)
print(pd.DataFrame(rows).drop(columns="training_seconds").round(6).to_string(index=False))
print("시계열·재구성 비교표: 03_forecast.py와 04_latent.py를 실행해 함께 제출")
print("test: 학습·평가 미사용")

pd.DataFrame(class_rows,columns=["model","class_id","support","correct","recall"]).to_csv(OUT/"class_metrics.csv",index=False)
pd.DataFrame(error_rows,columns=["model","id","actual","prediction","length"]).to_csv(OUT/"error_samples.csv",index=False)
print("클래스 지표 행:",len(class_rows),"실제 오답 행:",len(error_rows))
