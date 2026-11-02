"""이번 교시에서 수정할 구현 파일. 함수별 계약을 읽고 BEGIN/END 구간만 완성한다."""
from copy import deepcopy
from time import perf_counter
import math, random
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

def measure(model, x, lengths, repeats=5, warmup=2, training=False):
    # TODO X07-1
    # 같은 입력·모델로 반복 측정. repeats>=1,warmup>=0. 입력과 파라미터 장치는 같아야 한다.
    # 워밍업·H2D전송은 측정에서 제외. training=False는 순전파, True는 순전파+제곱평균손실+역전파; step 없음.
    # CUDA는 시작·종료에 synchronize, 워밍업 뒤 allocated peak를 reset. CPU VRAM은 None으로 기록한다.
    # samples_s=B*repeats/seconds, scope·gradient_norm·device·peak_vram_bytes도 반환한다.
    # 모델 weight/buffer/grad/mode/RNG를 성공/예외 모두 보존한다. 입력 gradient에 결과를 남기지 않는다.
    # 반복 횟수·길이·장치·모드가 다른 행을 같은 조건인 것처럼 평균내지 않는다. 시간값은 실행마다 달라도 정상.
    # BEGIN X07-1
    raise NotImplementedError('X07-1 요구사항을 구현하세요.')
    # END X07-1

def profile_workload(model, cpu_x, lengths, device):
    # TODO X07-2
    # 제공 profiler가 이 함수를 호출한다. model은 device에 준비되어 있다.
    # record_function 이름을 data.prepare, h2d, forward, backward로 정확히 기록한다.
    # data.prepare에서 입력 복사, h2d에서 device 이동, forward에서 모델+제곱평균loss, backward에서 역전파.
    # optimizer.step은 하지 않는다. 기록 뒤 모델/grad/mode/RNG와 입력은 원상복구한다.
    # 반환은 detached loss Python float. profiler trace 생성은 제공 run.py --profile 담당.
    # CPU 구간시간 합을 CUDA 비동기 전체 지연과 동일하다고 주장하지 않는다.
    # BEGIN X07-2
    raise NotImplementedError('X07-2 요구사항을 구현하세요.')
    # END X07-2

def summarize_runs(rows):
    # TODO X07-3
    # 선택 확장. 같은 model,length,scope,device,batch,repeats,warmup 행을 묶는다.
    # seconds는 양수 유한 값만 허용한다. group별 runs,mean_seconds,median_seconds,std_seconds를 반환한다.
    # 표준편차는 표본(ddof=1); n=1은 None. 원본 rows를 변경하지 않는다. 빈 입력은 ValueError.
    # 빠른 한 번만 골라 보고하지 않는다. 같은 조건의 반복 원시값도 별도 CSV에 보존한다.
    # BEGIN X07-3
    raise NotImplementedError('X07-3 요구사항을 구현하세요.')
    # END X07-3
