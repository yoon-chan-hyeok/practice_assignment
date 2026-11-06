"""실습 03. 같은 그룹의 이미지는 분할 경계를 넘지 않도록 배정합니다."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
m=pd.read_csv(BASE.parent/"data/manifest.csv")
# 기존 test는 보관합니다. train+val의 개발 그룹만 새 분할을 설명합니다.
dev=m[m.split!="test"].copy();groups=sorted(dev.group_id.unique())
cut=int(len(groups)*.75)
# >>> C03
# 요구: 앞 75%의 group을 train, 나머지를 val로 배정하세요. 그룹별로 하나의 값만 갖게 합니다.
pass  # TODO C03: 위 요구사항의 핵심 코드를 작성하세요.
# <<< C03
naive=["train" if i%2==0 else "val" for i in range(len(dev))]
dev["image_split"]=naive
print("그룹 분할의 중복 그룹:",int((dev.groupby("group_id").new_split.nunique()>1).sum()))
print("이미지 번갈아 분할의 중복 그룹:",int((dev.groupby("group_id").image_split.nunique()>1).sum()))
dev.to_csv(out/"split_demo.csv",index=False)
