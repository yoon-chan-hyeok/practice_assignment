"""실습07: 같은 설정에서 규제 하나씩 바꾸고 valid loss로 후보를 선택합니다."""
from pathlib import Path
import json
import torch
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from data import load_data
from train import fit

torch.set_num_threads(1)
base = Path(__file__).resolve().parent
out = base / "outputs"
checkpoint_dir = base / "checkpoints"
out.mkdir(exist_ok=True)
checkpoint_dir.mkdir(exist_ok=True)
device = torch.device("cpu")
X, y, Xv, yv, ids = load_data(base / "data" / "points.csv")
default = dict(width=32, bn=False, dropout=0.0, weight_decay=0.0, lr=.01,
               batch_size=32, epochs=80, seed=42, patience=8, min_delta=.001)
configs = [{**default,"name":"baseline"}, {**default,"name":"dropout","dropout":.3},
           {**default,"name":"batchnorm","bn":True}, {**default,"name":"weight_decay","weight_decay":.01}]
rows = []
winning_loss = float("inf")
for config in configs:
    model, history, summary, predicted = fit(config, X, y, Xv, yv, device)
    table = pd.DataFrame(history)
    table.to_csv(out / f"history_{config['name']}.csv", index=False)
    rows.append({**config, **summary})
    if summary["best_valid_loss"] < winning_loss:
        winning_loss = summary["best_valid_loss"]
        winner, best_config, winning_history, winning_prediction = model, config, table, predicted
    print(summary["name"], "best epoch:",summary["best_epoch"], "stop:",summary["stop_epoch"],
          "best valid loss:",round(summary["best_valid_loss"],6))
pd.DataFrame(rows).to_csv(out / "experiment_table.csv",index=False)
(out / "best_config.json").write_text(json.dumps(best_config,ensure_ascii=False,indent=2),encoding="utf-8")
# 선택한 모델의 state_dict를 checkpoints/best_model.pt에 저장하세요.
# 선택 config는 best_config.json에 이미 기록됩니다. 학습 재개용이 아닌 추론 복원용입니다.
# >>> S09
# TODO S09: 위 요구사항에 맞게 이 블록만 완성합니다.
pass
# <<< S09
pd.DataFrame({"id":ids,"actual":yv.tolist(),"predicted":winning_prediction.tolist()}).to_csv(
    out / "validation_predictions.csv",index=False)
plt.figure(figsize=(8,5))
plt.plot(winning_history["epoch"],winning_history["train_loss_eval"],label="train (eval)")
plt.plot(winning_history["epoch"],winning_history["valid_loss"],label="valid")
plt.axvline(winning_history.loc[winning_history.valid_loss.idxmin(),"epoch"],linestyle="--",label="best epoch")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.tight_layout()
plt.savefig(out / "learning_curves.png",dpi=150)
plt.close()
print("선택:",best_config["name"],"/ test 미사용 / validation 재사용에 따른 선택 편향 주의")
