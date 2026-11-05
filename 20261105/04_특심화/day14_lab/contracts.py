"""특심화 요구사항. 함수 문법 대신 계약·불변 조건·실패 조건을 먼저 읽으세요."""
from pathlib import Path
import csv,hashlib,json,copy,random,os,tempfile
from contextlib import nullcontext
from collections import defaultdict
import numpy as np
from PIL import Image
import torch
from torch import nn
import torch.nn.functional as F
from sklearn.metrics import f1_score


def audit_manifest(root, manifest='manifest.csv', near_bits=4):
    # 요구 S01 — 데이터 감사. root 아래 manifest CSV의 path, split, group_id, id를 읽는다.
    # 파일은 수정하지 않는다. 상대 경로만 허용하고 root 밖 경로/중복 ID/없는 파일은 ValueError.
    # SHA256은 바이트 동일 그룹, dHash(8×8=64bit)는 '검토 후보'만 판정한다.
    # dHash는 grayscale→9×8 resize→가로 인접 비교. 같은 hash라도 실제 같은 개체라고 단정 금지.
    # 다른 split 사이 근접쌍만 반환하며 class 이름/원본 basename으로 동일성을 추정하지 않는다.
    # 반환 dict: records(sha256,dhash 포함), exact_groups, near_pairs, group_leaks.
    # near_pairs 각 원소는 id_a,id_b,distance. near_bits는 0..64 정수.
    # 해설: 손실 압축/재인코딩은 바이트 hash로 놓칠 수 있다. 지각 hash 역시 오탐이 있으므로 삭제 명령이 아니다.
    # BEGIN S01
    raise NotImplementedError("S01: 위 요구사항을 구현하세요.")
    # END S01


def trainable_groups(model, strategy, head_lr=.01, backbone_lr=.001):
    # 요구 S02 — TinyShapeCNN의 학습 범위 설정. head=9, partial=4·5·9, full=전체.
    # 이전 .grad를 모두 None으로 지우고 requires_grad를 먼저 완전히 초기화한다.
    # Head 그룹을 먼저, Backbone 그룹을 두 번째로 반환. 각 params는 실제 Parameter의 list.
    # 모든 학습 가능 Parameter가 정확히 1회 포함되어야 한다. 동결 Parameter는 포함 금지.
    # 모든 BatchNorm을 eval로 설정한다. affine requires_grad와 running 통계는 별개다.
    # model의 층 구조는 제공 계약을 사용한다. 알 수 없는 전략/0 이하 lr는 ValueError.
    # 해설: optimizer를 만든 뒤 requires_grad만 열면 새 파라미터가 optimizer에 등록되지 않는다.
    # BEGIN S02
    raise NotImplementedError("S02: 위 요구사항을 구현하세요.")
    # END S02


def imbalance_weights(labels, classes=3):
    # 요구 S03 — labels는 train의 1차원 정수 Tensor. 비어 있거나 범위 밖/빠진 클래스는 ValueError.
    # class_weights=(1/count)/(1/count의 평균), sample_weights=1/count[각 라벨].
    # 원본 labels를 변경하지 않고 CPU float32 Tensor 두 개를 반환한다.
    # validation/test의 수를 인자로 받거나 확률적 재표집에 쓰지 않는다.
    # WeightedRandomSampler에는 class별 3개가 아니라 sample별 N개 weights를 넘긴다.
    # 해설: weight와 sampler를 동시에 기본 적용하면 보정을 중복할 수 있어 별개 후보로 실험한다.
    # BEGIN S03
    raise NotImplementedError("S03: 위 요구사항을 구현하세요.")
    # END S03


def weighted_ce(logits, targets, weights):
    # 요구 S04 — 클래스 가중 CE의 batch 평균을 직접 구성한다.
    # 분자=sum(w[y_i]*CE_i), 분모=sum(w[y_i]); 단순 batch size로 나누지 않는다.
    # logits[N,C], targets[N] long, weights[C] 양수·유한이며 device가 같아야 한다.
    # logits의 autograd 연결을 보존한 scalar 반환. .item(), detach(), numpy 변환 금지.
    # N=0, shape·label·weight 계약 위반은 ValueError. 입력을 변경하지 않는다.
    # 해설: reduction='none'은 per-sample loss이므로 전역 분모를 명시할 수 있다.
    # BEGIN S04
    raise NotImplementedError("S04: 위 요구사항을 구현하세요.")
    # END S04


def group_bootstrap(actual,predicted,groups,repeats=200,seed=14):
    # 요구 S05 — 행이 아닌 group ID를 복원 추출하는 percentile bootstrap.
    # 뽑힌 group의 모든 행을 포함하며 같은 group이 2번 뽑히면 해당 행도 2번 포함한다.
    # Macro F1 labels=[0,1,2], zero_division=0을 고정. 각 반복의 missing class도 동일 규칙.
    # 반환 estimate,low,high,groups,repeats. low/high는 2.5/97.5 백분위.
    # 길이 불일치·그룹 2개 미만·repeats<2는 ValueError. 입력/전역 난수 상태 보존.
    # 해설: 그룹 독립성·대표성이 가정이다. 이 구간으로 모델 선택 편향을 제거했다고 주장하지 않는다.
    # BEGIN S05
    raise NotImplementedError("S05: 위 요구사항을 구현하세요.")
    # END S05


def grad_cam(model,image,layer,target):
    # 요구 S06 — 단일 이미지 [1,3,H,W], target logit에 대한 layer 출력의 Grad-CAM.
    # model.eval()에서 수행하지만 gradient는 켠다. 동결 Backbone이면 image clone에 requires_grad=True.
    # forward hook 1개로 activation을 얻고 autograd.grad 사용. Parameter .grad는 변경 금지.
    # alpha=공간 평균 gradient; CAM=ReLU(sum(alpha*A)); 입력 크기로 bilinear resize.
    # 최대가 0이면 0 지도 반환. 다른 경우 0..1 정규화. 반환은 detached CPU Tensor [H,W].
    # 성공/실패 모두: hook 제거, 각 submodule의 원래 training flag, buffer, CPU/CUDA RNG 복구.
    # 입력/가중치/기존 gradient/requires_grad를 변경하지 않는다. inference_mode 안에서는 ValueError.
    # 다른 클래스/층 지도를 평균해 '진짜 원인'이라고 선언하지 않는다.
    # 해설: backward 대신 autograd.grad를 써 기존 Parameter.grad를 누적하지 않는다.
    # BEGIN S06
    raise NotImplementedError("S06: 위 요구사항을 구현하세요.")
    # END S06


def occlusion_map(model,image,target,patch=8):
    # 요구 S07 — 같은 target logit을 고정하고 patch 단위로 0 값을 대입한다(RGB[0,1] 입력 계약).
    # 반환: baseline_logit(float), drop_map[H,W] CPU Tensor. 값=원본 logit-가림 logit.
    # 음수 감소량도 보존한다. 마지막 잘리는 patch도 빠뜨리지 않는다. patch는 양의 정수.
    # 입력·모드·가중치·BN buffer·기존 gradient를 보존하고 eval+no_grad로 수행한다.
    # 해설: 검은 패치도 분포 밖 조작일 수 있다. 점수 감소는 인과성 증명이 아니다.
    # BEGIN S07
    raise NotImplementedError("S07: 위 요구사항을 구현하세요.")
    # END S07


def train_epoch(model,loader,optimizer,weights,scaler,amp=False):
    # 요구 S08 — batch는 (image,target,id). 모든 step은 train loader만 이용한다.
    # model.train 후 BN을 eval로 다시 고정. optimizer.zero_grad(set_to_none=True)→forward→loss→backward→step.
    # weighted_ce를 사용한다. epoch objective는 batch loss의 단순 평균이 아니라 전역 가중 분모 집계.
    # AMP는 CUDA에서만 활성화; scaler.scale(loss).backward(), scaler.step(), scaler.update() 순서.
    # CPU는 동일 코드의 AMP 비활성 경로. 예측 시점의 gradient를 끊지 않는다.
    # 반환 (objective:float, seen_ids:list[int]); shuffled ID 순서를 그대로 기록한다.
    # 해설: 클래스 가중 평균은 표본 수가 아니라 해당 batch의 sum(weight[y])가 분모다.
    # BEGIN S08
    raise NotImplementedError("S08: 위 요구사항을 구현하세요.")
    # END S08


def signature(data):
    """train/valid의 상대 경로와 실제 바이트 hash. test는 재개 계약에 포함하지 않습니다."""
    data=Path(data);items=[]
    for split in ('train','valid'):
        for path in sorted((data/split).rglob('*.png')):items.append((path.relative_to(data).as_posix(),hashlib.sha256(path.read_bytes()).hexdigest()))
    items.append(('source_backbone.npz',hashlib.sha256((data/'source_backbone.npz').read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(items,sort_keys=True).encode()).hexdigest()


def save_checkpoint(path,model,optimizer,scheduler,scaler,generator,epoch,history,config,data_signature):
    # 요구 S09 — epoch 경계에서만 저장. 중간 batch 재개를 지원한다고 주장하지 않는다.
    # model/optimizer/scheduler/scaler, epoch/history, config, signature, CPU RNG, CUDA RNG,
    # DataLoader generator, Python RNG, NumPy RNG(직렬화 가능한 list 표현), classes, 입력 계약을 저장.
    # path 부모 생성 후 같은 폴더의 임시 파일로 저장하고 os.replace. 불완전 파일을 최종 파일로 남기지 않는다.
    # 직접 생성한 파일만 로드할 전제. torch.save 이후 메모리의 모델을 변경하지 않는다.
    # 해설: model만 복원하면 모멘텀·학습률·배치 순서가 이어지지 않으므로 재개와 추론을 구분한다.
    # BEGIN S09
    raise NotImplementedError("S09: 위 요구사항을 구현하세요.")
    # END S09


def load_checkpoint(path,model,optimizer,scheduler,scaler,generator,config,data_signature):
    # 요구 S10 — 자신이 생성한 파일만 weights_only=True/map_location=cpu로 읽는다.
    # config·data_signature·classes·input 계약을 먼저 비교한다. 불일치면 어떤 실행 상태도 수정하지 않고 ValueError.
    # 같은 구조·파라미터 그룹 순서의 모델/optimizer에 복원한다. rng는 마지막에 복원한다.
    # CUDA 재개는 같은 장치/버전 조건을 전제하며 CPU 검사로 GPU 완전 재현을 주장하지 않는다.
    # 반환 epoch, history. model·optimizer·scheduler·scaler·loader_rng·global RNG가 연속 실행과 같아야 한다.
    # 해설: epoch 수 변경은 이번 계약에서 허용하지 않는다. '다른 실험'은 새 config로 실행한다.
    # BEGIN S10
    raise NotImplementedError("S10: 위 요구사항을 구현하세요.")
    # END S10
