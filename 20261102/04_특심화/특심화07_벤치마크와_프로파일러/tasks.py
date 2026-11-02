"""특심화07: 같은 초기 상태·입력·측정 범위에서만 시간 비교를 수행한다."""
import copy, math, time, statistics
from pathlib import Path
import torch
from torch import nn
from support import preserve_rng

def benchmark(source,batches,device,repeats=3,warmup=1,channels_last=False):
    # [요구 X07-1] CPU에 미리 적재한 (x,y) batch 목록. 입력 장치 CPU·4D 이미지, 전체 표본>0.
    # source를 깊은 복사해서 측정, 반복마다 같은 초기 state와 새 SGD(lr=.01) 사용.
    # RNG를 반복마다 42로 동일하게; 원본 source/입력/전역 RNG는 호출 후 보존.
    # 범위=preloaded_CPU_batches_H2D_forward_backward_step. 파일 I/O/초기화는 제외.
    # warmup은 별도 복사 모델에서 측정 전에 수행; 반복마다 CUDA synchronize 전후.
    # reset_peak_memory_stats 후 max_memory_allocated를 MiB로 기록. 이는 프로세스 allocator 전체 peak.
    # CPU VRAM=None. unavailable CUDA는 {'status':'SKIP_NO_CUDA','rows':[]} 반환.
    # 각 row: repeat/device/layout/samples/seconds/images_per_second/peak_vram_mib/scope.
    # repeats 양수·warmup>=0 int, bool 금지. 시간 하드코딩 금지; 모든 반복 결과 보존.
    # >>> X07-1
    # TODO X07-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-1")
    # <<< X07-1

def profile_steps(source,loader,device,path):
    # [요구 X07-2] source 복사 모델의 최대 2 batch를 profiler로 관찰하여 Chrome trace 저장.
    # record_function 범위 DataLoader.next/H2D/forward/backward/optimizer.step을 모두 사용.
    # CPU activity 항상, CUDA 가능·요청 시만 CUDA 추가. raw trace와 event 이름 목록 반환.
    # 원본 source·전역 RNG 보존. loader는 순회만큼 소비됨. profile 시간은 benchmark와 분리.
    # 입력 shape 기록. traces 안의 파일 경로는 공유 전 검토. 사용자 비밀 포함 금지.
    # >>> X07-2
    # TODO X07-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-2")
    # <<< X07-2

def summarize_times(rows):
    # [요구 X07-3 · 선택 확장] 같은 device/layout/samples/scope의 반복만 요약한다.
    # rows>=2. seconds 유한·양수, samples 동일 양수. repeats 중복이면 ValueError.
    # 반환 n/median_seconds/min_seconds/max_seconds/median_images_per_second.
    # 서로 다른 실험 조건을 섞어 평균내지 않는다. 최솟값 하나만 발표하지 않는다.
    # >>> X07-3
    # TODO X07-3: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X07-3")
    # <<< X07-3
