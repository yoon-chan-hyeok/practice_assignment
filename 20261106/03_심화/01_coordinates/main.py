"""실습 01. 실제 이미지 경계로 clip하고 면적이 달라지는 이유를 설명합니다."""
from pathlib import Path
import numpy as np
import pandas as pd
BASE=Path(__file__).resolve().parent
out=BASE/"outputs";out.mkdir(exist_ok=True)
boxes=np.array([[-5,10,25,40],[140,100,180,150],[10,10,11,11]],float)
# >>> C01
# 요구: x를 [0,160], y를 [0,128]로 clip한 새 배열을 만드세요.
# 원본은 보존합니다. 여기서는 clip 뒤에도 모두 양의 면적입니다.
pass  # TODO C01: 위 요구사항의 핵심 코드를 작성하세요.
# <<< C01
area=(clipped[:,2]-clipped[:,0])*(clipped[:,3]-clipped[:,1])
r=pd.DataFrame(clipped,columns=["x1","y1","x2","y2"]);r["area"]=area
r.to_csv(out/"clipped.csv",index=False);print(r.to_string(index=False))
print("경계 밖 입력은 설명용입니다. 원본 라벨을 무조건 clip하여 덮어쓰지 마세요.")
