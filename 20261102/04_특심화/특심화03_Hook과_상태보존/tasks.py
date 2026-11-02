"""특심화03: forward hook을 관찰 도구로 쓰되 호출 대상의 상태를 훼손하지 않는다."""
import torch
from support import snapshot, restore_snapshot, preserve_rng

def trace_leaves(model,x):
    # [요구 X03-1] leaf module마다 forward hook을 설치하고 실제 호출 순서대로 기록한다.
    # 지원 출력은 비어 있지 않은 floating Tensor. tuple 등은 ValueError로 범위를 명시한다.
    # record: name(str), call(동일 module의 1-based 호출 번호), shape(list), elements(int),
    # activation_bytes(numel*element_size), mean/std(unbiased=False), parameters(직접 소유 수).
    # Tensor/계산 그래프를 기록 안에 남기지 않는다. 공유 module의 재호출은 각각 한 행.
    # 임시 eval + inference_mode. 정상/실패 모두 기존 모드·가중치·buffer·grad·RNG 보존.
    # 자신이 설치한 handle만 finally에서 remove. 기존 외부 hook은 유지해야 한다.
    # 빈 모델도 지원: 최상위 모듈이 leaf이면 name=''의 한 행을 기록한다.
    # >>> X03-1
    # TODO X03-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-1")
    # <<< X03-1

def summarize_trace(rows):
    # [요구 X03-2] 호출 행 목록을 요약한다. 빈 목록은 ValueError.
    # 반환 calls, unique_modules, parameters_once, max_activation_bytes, max_activation_name.
    # 같은 이름이 여러 번 호출되어도 parameters는 한 번만 합한다. 같은 이름의 수가 다르면 오류.
    # 최대 활성 크기 동점이면 먼저 관찰한 행의 이름을 유지한다. rows 변경 금지.
    # activation_bytes 최대는 '한 출력 Tensor' 크기이며 peak GPU VRAM이나 총 학습 메모리가 아니다.
    # >>> X03-2
    # TODO X03-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X03-2")
    # <<< X03-2
