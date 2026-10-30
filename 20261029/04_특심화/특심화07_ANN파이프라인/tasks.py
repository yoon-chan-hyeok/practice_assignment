"""특심화07: 순서·분할·기록을 책임지는 세 함수입니다. 학습 엔진은 완성 코드로 제공됩니다."""
import csv
from pathlib import Path
import torch
from torch.utils.data import DataLoader, TensorDataset

def load_development(path):
    # [요구사항 X07-1 | 고정 분할 데이터 읽기]
    # 입력: UTF-8 CSV 경로. 열 id,x1,x2,label,split. split은 train/valid/test입니다.
    # 반환: (tensors, ids). tensors에는 train·valid 두 키만, 값은 (X float32 [N,2],y long [N]).
    # ids에는 train·valid·test의 ID 리스트를 원본 순서로 기록합니다.
    # test는 ID만 수집하고 수치 입력·정답을 float/int 변환하거나 Tensor로 만들지 않습니다.
    # id 중복, 알 수 없는 split, 비어 있는 train/valid는 ValueError. split 재추출·shuffle 금지.
    # 원본을 수정하지 않습니다. 200건 입력에서 train120/valid40/test40 ID가 보존됩니다.
    # >>> X07-1
    # TODO X07-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-1")
    # <<< X07-1

def build_loaders(tensors, seed=43, batch_size=32):
    # [요구사항 X07-2 | 재현 가능한 train 순서]
    # 반환 (train_loader,valid_loader,CPU_generator). train만 shuffle=True입니다.
    # 독립 torch.Generator.manual_seed(seed)를 train에 전달하고 전역 seed를 변경하지 않습니다.
    # valid shuffle=False, 두 loader 모두 drop_last=False,num_workers=0입니다.
    # 동등한 seed의 새 loader는 같은 순서이고, 이어진 epoch는 새 순열입니다.
    # batch_size<=0은 ValueError. test loader를 추가하지 않습니다.
    # >>> X07-2
    # TODO X07-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-2")
    # <<< X07-2

def write_predictions(path, ids, truth, probabilities):
    # [요구사항 X07-3 | ID별 예측 기록]
    # 입력: valid ids N개, truth long[N], probabilities float[N,2]. 정상 범위 입력은 제공됩니다.
    # 반환: 저장한 행 수(int). CSV 헤더 id,actual,probability_1,predicted 순서를 지킵니다.
    # 길이가 다르거나 probabilities가 (N,2)가 아니면 ValueError. 오류 시 파일을 생성/덮어쓰지 않습니다.
    # 같은 loader의 원래 순서 유지; predicted는 argmax(dim=1). confidence와 actual을 바꾸어 쓰지 않습니다.
    # 부모 폴더 생성 가능. 출력은 utf-8-sig/newline="". 값 저장 전 detach().cpu()로 그래프를 분리합니다.
    # >>> X07-3
    # TODO X07-3: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-3")
    # <<< X07-3
