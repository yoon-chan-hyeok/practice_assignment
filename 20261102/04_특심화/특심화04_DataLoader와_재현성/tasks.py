"""특심화04: DataLoader 구성과 host 로딩 관찰. Windows에서는 run.py의 main guard를 유지한다."""
import time
import torch
from torch.utils.data import DataLoader
from support import seed_worker

def make_loader(dataset,batch_size=16,workers=0,shuffle=True,seed=42,device=torch.device('cpu')):
    # [요구 X04-1] 반환: (loader, loader에 전달한 동일 CPU Generator).
    # batch_size 양의 int, workers 0이상 int, shuffle bool, seed int. bool 크기 사용 금지.
    # drop_last=False. CPU에서 pin_memory=False; 실제 CUDA 요청만 True.
    # workers=0: persistent=False, multiprocessing_context 생략.
    # workers>0: persistent=True, spawn, 제공된 top-level seed_worker 사용.
    # dataset/transform/samples 변경 금지. 환경 전역 seed를 이 함수에서 변경하지 않는다.
    # CUDA 명시 요청인데 사용 불가능하면 RuntimeError(자동 CPU 대체 금지).
    # 완료: 60건/batch16 => 16,16,16,12. 동일 seed의 새 loader에서 첫 epoch 순서 동일.
    # >>> X04-1
    # TODO X04-1: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X04-1")
    # <<< X04-1

def measure_loading(loader,epochs=2):
    # [요구 X04-2] loader 항목은 (images,labels,ids). epochs는 양의 int.
    # epoch마다 iter(loader) 생성 직전부터 완전 순회까지 perf_counter로 측정.
    # images 수, batch_sizes, 순서 ids, seconds, images_per_second, epoch(1-based), scope 기록.
    # scope='host_decode_transform_collate'. 모델/장치 이동 없음; GPU 대기시간으로 주장하지 않는다.
    # 첫 epoch worker 시작 비용과 이후 epoch 재사용 비용을 분리하여 남긴다.
    # 누락·중복 ID, 빈 loader이면 ValueError. iterator의 끝을 건너뛰거나 고정 시간값 사용 금지.
    # loader/generator는 정상 순회만큼 소비된다. 동일 결과 비교는 새 loader를 다시 구성한다.
    # >>> X04-2
    # TODO X04-2: 바로 위의 입력·출력·보존·실패 조건을 만족하도록 구현하세요.
    raise NotImplementedError("TODO X04-2")
    # <<< X04-2
