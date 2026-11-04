"""이미지 계약. 일반 사진만 보고 BGR/RGB를 보편적으로 판별할 수는 없습니다."""
import numpy as np

def normalize_bgr(image, known_patches=None):
    """BGR uint8 HWC → 독립적인 C-contiguous 배열과 진단 정보."""
    # >>> TODO X01
    # 요구사항 X01 — 실제 배열 계약과 색상 기준점을 분리해 검사합니다.
    # 입력 image: uint8, H×W×3 ndarray. H,W>0. 음수 stride/비연속 view도 허용합니다.
    # known_patches: 선택 dict {(y,x):(B,G,R)}. 보정용으로 위치·색을 알고 있는 경우만 전달합니다.
    # uint16/float는 TypeError, Gray·빈 배열·4채널은 ValueError. 임의 자동 정규화 금지.
    # 패치가 주어지면 범위와 정확한 BGR 값 검증. 불일치는 ValueError로 명시하세요.
    # 패치가 없으면 색 순서를 '추측하여 교정'하지 마세요. 자연 영상만으로 확정할 수 없습니다.
    # 출력은 (독립 C-contiguous 복사본, info dict). 원본과 메모리를 공유하지 않아야 합니다.
    # info에는 shape,dtype,input_strides,input_c_contiguous,output_c_contiguous,shares_memory를 기록합니다.
    # 원본 데이터·stride·전역 난수 상태 변경 금지. 테스트에서 view·역순 채널·원본 보존을 확인합니다.
    raise NotImplementedError("TODO X01: 요구사항을 구현하세요")
    # <<< TODO X01
