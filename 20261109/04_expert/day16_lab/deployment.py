"""실제 GPU가 없는 환경에서는 manifest의 정적 계약만 검증합니다."""
import math


def inspect_plan(manifest,environment,shape):
    # S07 요구사항
    # 입력 키: platform,architecture,gpu,tensorrt,input_name,precision,profile(min/opt/max),flags.
    # environment의 동일 4개 환경값이 일치하는지 보수적으로 검사한다.
    # 이 예제는 호환 플래그의 예외를 지원하지 않는다. 불일치를 승인하지 않는다.
    # profile 각 축 양의 int, min<=opt<=max, request shape도 양의 int와 허용 범위.
    # TensorRT 11 이상에 --fp16/--int8/--bf16/--best를 사용하면 오류 사유.
    # 반환 {errors:list[str], contract_ok:bool, runtime_verified:False}.
    # contract_ok=True는 엔진 로딩 성공/Jetson 지원/추론 정확도의 보증이 절대 아니다.
# TODO S07
    raise NotImplementedError('S07: deployment contract, not runtime certification')
# TODO 끝 S07
