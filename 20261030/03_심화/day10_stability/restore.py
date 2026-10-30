"""실습08: 새 프로세스에서 best 모델의 예측과 loss를 대조합니다."""
from pathlib import Path
import json
import torch
import pandas as pd
from data import load_data
from model import build_model
from evaluate import evaluate

torch.set_num_threads(1)
base = Path(__file__).resolve().parent
config = json.loads((base / "outputs" / "best_config.json").read_text(encoding="utf-8"))
_, _, Xv, yv, ids = load_data(base / "data" / "points.csv")
model = build_model(config)
# 직접 생성한 state_dict만 torch.load(..., map_location="cpu", weights_only=True)로 읽어 모델에 적용하세요.
# 복원한 모델을 eval로 바꾸는 것과 no_grad를 쓰는 것은 별개입니다. 그 아래 evaluate가 처리합니다.
# >>> S10
# TODO S10: 위 요구사항에 맞게 이 블록만 완성합니다.
pass
# <<< S10
loss, accuracy, predicted = evaluate(model, Xv, yv, torch.device("cpu"))
saved = pd.read_csv(base / "outputs" / "validation_predictions.csv")
comparison = pd.read_csv(base / "outputs" / "experiment_table.csv")
expected_loss = float(comparison.loc[comparison["name"]==config["name"],"best_valid_loss"].iloc[0])
result = {"ids_equal":ids==saved["id"].tolist(),"predictions_equal":predicted.tolist()==saved["predicted"].tolist(),
          "valid_loss":loss,"expected_loss":expected_loss,"loss_matches":abs(loss-expected_loss)<1e-6,
          "valid_accuracy":accuracy,"test_used":False}
(base / "outputs" / "restore_report.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
