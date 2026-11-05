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
from sklearn.model_selection import GroupShuffleSplit,train_test_split
manifest=pd.read_csv(DATA/"manifest.csv")
# 실제 배포 분할은 이미 그룹 독립. 비교 시연에는 train 행만 사용합니다.
rows=manifest[manifest.split=="train"].reset_index(drop=True)
train_i,valid_i=train_test_split(np.arange(len(rows)),test_size=.25,random_state=14)
random_overlap=set(rows.iloc[train_i].group_id)&set(rows.iloc[valid_i].group_id)
splitter=GroupShuffleSplit(n_splits=1,test_size=.25,random_state=14)
# TODO D01: groups에 group_id를 전달하고 두 인덱스를 꺼내세요.
# BEGIN D01
group_train,group_valid=train_i,valid_i  # GroupShuffleSplit의 인덱스로 바꾸세요.
# END D01
group_overlap=set(rows.iloc[group_train].group_id)&set(rows.iloc[group_valid].group_id)
print("이미지 무작위 분할 그룹 중복:",len(random_overlap))
print("그룹 단위 분할 그룹 중복:",len(group_overlap))
print("주의: GroupShuffleSplit이 클래스 비율까지 보장하지 않습니다.")
rows.assign(demo_split=np.where(rows.index.isin(group_train),"train","valid")).to_csv(OUT/"group_split.csv",index=False)
