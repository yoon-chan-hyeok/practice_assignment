"""실습 06 · 학습과 평가. 반환 지표는 샘플 수 기준이고 test 데이터는 전달하지 않습니다."""
import torch
from contracts import validate_batch

def train_one_epoch(model, loader, optimizer, device):
    # [요구사항 X06-1 | 한 epoch 학습]
    # 입력: float32 2→8→2 model, 정상 train DataLoader, SGD optimizer, model과 같은 device.
    # loader는 TensorDataset(X,y)이며 drop_last=False, num_workers=0, 마지막 batch는 작을 수 있다.
    # 각 배치에서: device 이동 → validate_batch → zero_grad(set_to_none=True) → 순전파 →
    # CrossEntropyLoss(mean) → backward → step. model.train()을 시작 시 호출한다.
    # 반환 dict: loss=float, accuracy=float, samples=int, batches=int.
    # loss는 각 배치 평균*실제 배치 수의 합 / 실제 전체 행 수이다. 배치 평균의 단순 평균 금지.
    # accuracy는 해당 학습 step의 갱신 전 logits에서 맞힌 총수/전체수. 0~1 비율이다.
    # 학습 중 모델이 바뀌므로 반환 loss는 online 평균이다. 최종 고정 모델의 평가 loss와 구분한다.
    # loader가 비어 있으면 ValueError. 파라미터 gradient를 epoch 사이로 누적하지 않는다.
    # 금지: valid/test 사용, 반환 Tensor에 그래프 보관, batch_size를 마지막 배치 크기로 가정.
    # 검사: 7행·batch3에서 samples=7,batches=3. lr=0에서 일괄 loss와 가중 loss가 일치한다.
    # >>> X06-1
    # TODO X06-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-1")
    # <<< X06-1

def evaluate(model, loader, device):
    # [요구사항 X06-2 | 부작용 없는 평가]
    # 입력: model, 정상 train 또는 valid DataLoader, model과 같은 device. shuffle=False 권장.
    # 반환 dict: loss,accuracy,samples,batches는 X06-1과 동일. probabilities=(N,2) CPU Tensor,
    # predictions=(N,) CPU long Tensor도 반환한다. loader의 원래 행 순서를 유지한다.
    # model.eval()과 torch.no_grad()를 함께 사용한다. 반환 Tensor는 requires_grad=False.
    # CrossEntropyLoss(mean)를 샘플 수로 가중 집계한다. probabilities는 softmax(dim=1)다.
    # backward/optimizer.step/zero_grad 호출 금지. 기존 .grad, Parameter 값은 변경하지 않는다.
    # 성공 또는 입력 오류로 종료해도 호출 전 각 하위 모듈의 training 모드를 복구한다. 부모·자식 모드가 서로 다를 수도 있다.
    # 빈 loader는 ValueError. 해당 오류가 발생해도 모드는 복구해야 한다.
    # 특정 모델 점수를 하드코딩하지 않는다. train/valid의 길이·마지막 배치 수에 의존하지 않는다.
    # 허용오차: 고정 모델의 일괄 계산과 loss/확률은 float32 rtol=1e-5, atol=1e-6 비교.
    # 완료 기준: test가 아니라 valid 결과이며 평가 전후 가중치와 기존 grad가 동일함을 보여준다.
    # >>> X06-2
    # TODO X06-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X06-2")
    # <<< X06-2
