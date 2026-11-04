import cv2
from time import perf_counter
from image_ops import prepare_image

def process_video(source,destination):
    """한 번 열고 Frame을 순서대로 처리합니다. 코덱 성공 여부도 반환합니다."""
    cap=cv2.VideoCapture(str(source));fps=cap.get(cv2.CAP_PROP_FPS)
    writer=cv2.VideoWriter(str(destination),cv2.VideoWriter_fourcc(*"MJPG"),fps,(160,120))
    opened=cap.isOpened() and writer.isOpened();count=0;start=perf_counter()
    while opened:
        ok,frame=cap.read()
        if not ok:break
        # >>> TODO H08
        # prepare_image(frame)의 edge 결과를 3채널로 바꾸고 writer에 전달하세요.
        writer.write(cv2.resize(frame,(160,120)))
        # <<< TODO H08
        count+=1
    cap.release();writer.release()
    check=cv2.VideoCapture(str(destination))
    report={"opened":opened,"written":count,"decoded":int(check.get(7)),"fps":check.get(5),"width":int(check.get(3)),"height":int(check.get(4)),"wall_s":perf_counter()-start}
    check.release();return report
