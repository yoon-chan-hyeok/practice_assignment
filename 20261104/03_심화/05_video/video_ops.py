import cv2

def process_frame(frame):
    """컬러 Frame을 고정 크기의 Edge 컬러 Frame으로 바꿉니다."""
    # >>> TODO H05
    # Resize160×120→Gray→Gaussian3×3→Canny80/160 순서로 edge를 만드세요. 파일 열기·종료는 main이 담당합니다.
    small=cv2.resize(frame,(160,120))
    edge=small[:,:,0]
    # <<< TODO H05
    return cv2.cvtColor(edge,cv2.COLOR_GRAY2BGR)
