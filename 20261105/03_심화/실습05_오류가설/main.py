from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
import torch
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/"day14_vision"))
DATA=BASE.parent/"data"
OUT=BASE/"outputs"
OUT.mkdir(exist_ok=True)
torch.set_num_threads(1)
from engine import experiment,datasets,metrics
from models import build_model,configure
from explain import save_explanations
# 고정된 초기 1회 학습 모델의 실제 오답을 진단합니다. 최종 모델이 아닙니다.
model,summary,history,prediction=experiment(DATA,epochs=1)
# TODO D05: 실제 라벨과 예측 라벨이 다른 행을 남기세요.
# BEGIN D05
wrong=prediction.iloc[:0].copy()  # 오답 행을 선택하세요.
# END D05
wrong["hypothesis"]="직접 관찰 후 작성: 데이터/라벨/도메인/모델"
wrong["next_check"]="가설을 검증할 추가 비교를 작성"
wrong.to_csv(OUT/"error_hypotheses.csv",index=False)
save_explanations(DATA,OUT,model,prediction)
print("오답:",len(wrong),"없는 오류 유형은 만들어내지 않습니다.")
