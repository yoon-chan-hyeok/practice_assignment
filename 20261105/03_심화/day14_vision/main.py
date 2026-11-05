from pathlib import Path
import json
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import classification_report,confusion_matrix
from engine import experiment
from explain import save_explanations

BASE=Path(__file__).resolve().parent;DATA=BASE/"data";OUT=BASE/"outputs"
OUT.mkdir(exist_ok=True);torch.set_num_threads(1)
# TODO D07: 같은 8회 예산에서 네 후보를 명시하세요. Scratch는 비교표의 별도 보조 후보입니다.
# BEGIN D07
experiments=[("head","none")]  # 나머지 세 후보를 추가하세요.
# END D07
rows=[];histories=[];best_key=None
for strategy,balance in experiments:
    model,summary,history,prediction=experiment(DATA,strategy=strategy,balance=balance,epochs=8)
    rows.append(summary);history["candidate"]=strategy+"_"+balance;histories.append(history)
    # TODO D08: Macro F1을 최대화하고 동률이면 loss가 작은 후보를 고르세요. test는 보지 않습니다.
    # BEGIN D08
    key=(summary["accuracy"],)  # Macro F1, loss 순서로 바꾸세요.
    # END D08
    if best_key is None or key>best_key:
        best_key=key;chosen=summary;chosen_pred=prediction;chosen_state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
pd.DataFrame(rows).to_csv(OUT/"metrics.csv",index=False)
pd.concat(histories,ignore_index=True).to_csv(OUT/"history.csv",index=False)
model.load_state_dict(chosen_state);model.eval()
chosen_pred.to_csv(OUT/"predictions.csv",index=False)
report=classification_report(chosen_pred.actual,chosen_pred.predicted,labels=[0,1,2],target_names=["circle","square","triangle"],output_dict=True,zero_division=0)
(OUT/"metrics.json").write_text(json.dumps({"selected":chosen,"report":report,"test_used":False},indent=2,ensure_ascii=False),encoding="utf-8")
pd.DataFrame(confusion_matrix(chosen_pred.actual,chosen_pred.predicted,labels=[0,1,2])).to_csv(OUT/"confusion.csv",index=False)
explanations=save_explanations(DATA,OUT,model,chosen_pred)
(OUT/"cam_index.json").write_text(json.dumps(explanations,ensure_ascii=False,indent=2),encoding="utf-8")
# TODO D09: 선택 가중치와 클래스 매핑·입력 계약을 함께 저장하세요.
# BEGIN D09
pass  # torch.save로 필요한 상태·계약을 저장하세요.
# END D09
print(pd.DataFrame(rows).drop(columns="seconds").round(4).to_string(index=False))
print("선택:",chosen["strategy"],chosen["balance"],"test 사용: False")
