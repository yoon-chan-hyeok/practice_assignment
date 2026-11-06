"""실습 08. 새로운 프로세스에서 같은 모델·입력·설정의 검출을 대조합니다."""
from pathlib import Path
import torch
import pandas as pd
import numpy as np
from vision import detect_images
BASE=Path(__file__).resolve().parent
if __name__=='__main__':
    torch.set_num_threads(1);out=BASE/'outputs'
    restored,counts=detect_images(out/'model.pt',BASE/'data/images/val',out/'restored_images')
    old=pd.read_csv(out/'predictions.csv');sort=['image','class_id','confidence','x1','y1']
    old=old.sort_values(sort).reset_index(drop=True);restored=restored.sort_values(sort).reset_index(drop=True)
    # >>> C10
    # 요구: 행 수·이미지·클래스가 같은지와 점수·좌표 오차를 함께 비교하세요.
    # 탐지가 0건인 경우에도 처리 이미지 수를 image_counts.csv와 대조합니다.
    pass  # TODO C10: 위 요구사항의 핵심 코드를 작성하세요.
    # <<< C10
    expected=pd.read_csv(out/'image_counts.csv')
    print('예측 일치:',same,'이미지 처리 일치:',counts.equals(expected))
    print('동일 모델의 재현이며 test로 모델을 다시 선택한 것이 아닙니다.')
