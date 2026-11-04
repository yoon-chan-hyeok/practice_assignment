"""제한 큐 Decode→Process→Encode. 드롭은 live 정책 모의이며 원본 PTS를 보존하지 않습니다."""
from pathlib import Path
from queue import Queue,Full,Empty
from threading import Event,Thread,Lock
from time import perf_counter,sleep
import cv2
import numpy as np

_SENTINEL=object()

def offer_frame(queue,item,policy,cancel):
    # >>> TODO X07
    # 요구사항 X07 — bounded Queue의 두 정책. 제어 sentinel에는 이 함수를 쓰지 않습니다.
    # queue는 maxsize>0의 Queue, item은 (index,frame,decode_done_time), cancel은 Event입니다.
    # block: Full이면 timeout0.05초 단위로 기다리며 cancel을 다시 확인합니다. 성공 True, 취소 False.
    # drop_latest: put_nowait 한 번만 시도. Full이면 새 item을 버리고 False. 오래된 item을 꺼내면 안 됩니다.
    # 지원하지 않는 policy는 ValueError. cancel이 이미 켜져 있으면 즉시 False.
    # 무한 대기·busy spin·큐 크기 강제 변경 금지. 외부 수치를 직접 갱신하지 마세요.
    # 실제 drop 수는 스케줄링에 따라 변합니다. tests는 고정 큐의 정책과 전체 수 회계로 검증합니다.
    # Frame 순서를 유지하고, 드롭 영상은 원본 fps로 쓰므로 출력 재생시간이 짧아짐을 기록합니다.
    # 이 실습은 유한 파일을 빠르게 읽는 live 정책 모의입니다. 실제 카메라 지연이나 원본 PTS 보존을 주장하지 않습니다.
    raise NotImplementedError("TODO X07: 요구사항을 구현하세요")
    # <<< TODO X07

def process_frame(frame,size=(160,120)):
    # >>> TODO X08
    # 요구사항 X08 — 상태 없는 Frame 변환.
    # 입력은 HWC BGR uint8, size=(W,H) 기본160×120. 계약 위반은 ValueError.
    # Resize AREA → Gray → Gaussian3×3 sigmaX0 → Canny80/160 → Gray2BGR 순서로 처리합니다.
    # 반환 shape=(size[1],size[0],3), dtype=uint8. 입력을 수정하거나 메모리를 공유하지 않습니다.
    # VideoCapture/Writer·전역 카운터·난수·파일 입출력을 이 함수 안에서 사용하지 마세요.
    # 동일 Frame은 같은 결과를 내야 합니다. CPU 직렬 경로와 큐 처리 경로가 이 함수를 공유합니다.
    # 이 결과는 Edge 시각화입니다. 저장된 MJPG 영상을 완전 이진/픽셀 동일 영상이라고 주장하지 않습니다.
    raise NotImplementedError("TODO X08: 요구사항을 구현하세요")
    # <<< TODO X08

def run_video(source,destination,policy="block",queue_size=2,processing_delay_s=0.0,codec="MJPG"):
    if policy not in {"block","drop_latest"} or queue_size<1 or processing_delay_s<0:raise ValueError("queue policy 설정 오류")
    source,destination=Path(source),Path(destination)
    if source.resolve()==destination.resolve():raise ValueError("원본 덮어쓰기 금지")
    probe=cv2.VideoCapture(str(source))
    if not probe.isOpened():raise OSError("VideoCapture 열기 실패")
    fps=float(probe.get(cv2.CAP_PROP_FPS));expected=int(probe.get(cv2.CAP_PROP_FRAME_COUNT));probe.release()
    if fps<=0 or not np.isfinite(fps):raise ValueError("유효 FPS 필요")
    destination.parent.mkdir(parents=True,exist_ok=True)
    qin,qout=Queue(queue_size),Queue(queue_size);cancel=Event();lock=Lock();errors=[]
    stats={"decoded":0,"processed":0,"written":0,"dropped":0,"queue_in_sampled_peak":0,"queue_out_sampled_peak":0}
    mapping=[];latencies=[];dropped_ids=[]
    def fail(exc):
        with lock:errors.append(repr(exc))
        cancel.set()
    def control(q):
        while not cancel.is_set():
            try:q.put(_SENTINEL,timeout=.05);return
            except Full:pass
    def decode():
        cap=cv2.VideoCapture(str(source));index=0
        try:
            if not cap.isOpened():raise OSError("decode open 실패")
            while not cancel.is_set():
                ok,frame=cap.read()
                if not ok:break
                timestamp=perf_counter()
                with lock:stats["decoded"]+=1
                accepted=offer_frame(qin,(index,frame,timestamp),policy,cancel)
                with lock:
                    stats["queue_in_sampled_peak"]=max(stats["queue_in_sampled_peak"],qin.qsize())
                    if not accepted and not cancel.is_set():stats["dropped"]+=1;dropped_ids.append(index)
                index+=1
            control(qin)
        except Exception as exc:fail(exc)
        finally:cap.release()
    def process():
        try:
            while not cancel.is_set():
                try:item=qin.get(timeout=.05)
                except Empty:continue
                if item is _SENTINEL:control(qout);break
                index,frame,timestamp=item
                if processing_delay_s:sleep(processing_delay_s)
                result=process_frame(frame)
                with lock:stats["processed"]+=1
                offer_frame(qout,(index,result,timestamp),"block",cancel)
                with lock:stats["queue_out_sampled_peak"]=max(stats["queue_out_sampled_peak"],qout.qsize())
        except Exception as exc:fail(exc)
    def encode():
        writer=cv2.VideoWriter(str(destination),cv2.VideoWriter_fourcc(*codec),fps,(160,120))
        try:
            if not writer.isOpened():raise OSError("VideoWriter codec 열기 실패: "+codec)
            while not cancel.is_set():
                try:item=qout.get(timeout=.05)
                except Empty:continue
                if item is _SENTINEL:break
                index,result,timestamp=item
                if result.shape!=(120,160,3) or result.dtype!=np.uint8:raise ValueError("Writer frame 계약 위반")
                writer.write(result);now=perf_counter()
                with lock:
                    mapping.append({"output_index":stats["written"],"source_index":index,"source_time_s":index/fps})
                    stats["written"]+=1;latencies.append((now-timestamp)*1000)
        except Exception as exc:fail(exc)
        finally:writer.release()
    start=perf_counter()
    workers=[Thread(target=decode,daemon=True),Thread(target=process,daemon=True),Thread(target=encode,daemon=True)]
    for t in workers:t.start()
    for t in workers:t.join(timeout=20)
    alive=any(t.is_alive() for t in workers)
    if alive:
        cancel.set()
        for t in workers:t.join(timeout=2)
        raise RuntimeError("영상 worker 종료 시간 초과")
    if errors:raise RuntimeError("; ".join(errors))
    wall=perf_counter()-start
    check=cv2.VideoCapture(str(destination));decoded_output=0
    while True:
        ok,frame=check.read()
        if not ok:break
        if frame.shape!=(120,160,3):raise ValueError("재읽기 frame 크기 불일치")
        decoded_output+=1
    output_fps=check.get(cv2.CAP_PROP_FPS);check.release()
    if decoded_output!=stats["written"] or (expected>0 and expected!=stats["decoded"]):raise RuntimeError("입출력 Frame 수 검증 실패")
    if stats["decoded"]!=stats["written"]+stats["dropped"]:raise RuntimeError("프레임 회계 불일치")
    stats.update({"policy":policy,"codec":codec,"queue_capacity":queue_size,"output_frames_verified":decoded_output,"fps":output_fps,"input_duration_s":stats["decoded"]/fps,"output_duration_s":stats["written"]/output_fps,"wall_s":wall,"written_fps":stats["written"]/wall,"latency_p50_ms":float(np.percentile(latencies,50)) if latencies else None,"latency_p95_ms":float(np.percentile(latencies,95)) if latencies else None,"dropped_indices":dropped_ids,"frame_map":mapping,"simulated_processing_delay_s":processing_delay_s})
    return stats
