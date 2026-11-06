"""실습 03. 정상 라벨의 면적·비율·클래스 수와 그룹 분리를 확인합니다."""
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
manifest=pd.read_csv(BASE/"data/manifest.csv")
rows=[]
for image in manifest.itertuples():
    for line in (BASE/"data"/image.label).read_text(encoding="utf-8").splitlines():
        cls,cx,cy,w,h=map(float,line.split())
        # >>> A03
        # 요구: 정규화 면적 w*h와 원본 pixel 기준 가로세로비를 기록하세요.
        pass  # TODO A03: 위 요구사항의 핵심 코드를 작성하세요.
        # <<< A03
r=pd.DataFrame(rows);r.to_csv(out/"label_audit.csv",index=False)
print(r.groupby(["split","class_id"]).size().unstack(fill_value=0).to_string())
print("split 간 그룹 중복:", int((manifest.groupby("group_id").split.nunique()>1).sum()))
print("정확히 같은 파일:", int(manifest.sha256.duplicated().sum()))
print("빈 라벨은 정상 negative 이미지이며 누락 라벨과 다릅니다.")
