"""실습 05 · 안정적인 Cross Entropy. 구현 요구는 여기, 비교 정답은 공개 테스트에 있습니다."""
import torch

def stable_cross_entropy(logits, target):
    # [요구사항 X05-1 | logits에서 안정적으로 손실 계산]
    # 입력: 정상 유한 logits=(N,C), float32 또는 float64, target=(N,) long, 0<=target<C.
    # 반환: 샘플 평균 Cross Entropy인 스칼라 Tensor. 입력 dtype/device와 미분 경로를 유지한다.
    # 식: sample_loss=logsumexp(logits,dim=1)-각 행 정답 클래스의 logit.
    # 사용 가능: torch.logsumexp, gather 또는 index 선택, mean.
    # 금지: nn.CrossEntropyLoss/F.cross_entropy/F.log_softmax/softmax 호출, exp를 직접 합산,
    #        loss.item()을 반환하거나 detach하여 gradient를 끊기, 입력 logits 수정.
    # 큰 값 사례: [1000,-1000], [-1000,1000]에서도 NaN/inf가 발생하지 않아야 한다.
    # 완료 기준: torch.nn.functional.cross_entropy와 값·gradient가 float64에서
    #            rtol=1e-8, atol=1e-10으로 일치한다. 평균 reduction을 사용한다.
    # 일반 학습 코드에서는 공식 CrossEntropyLoss를 써도 된다. 이 함수는 원리 검증 과제다.
    # >>> X05-1
    # TODO X05-1: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X05-1")
    # <<< X05-1


def weighted_batch_mean(pairs):
    # [요구사항 X05-2 | 마지막 작은 배치의 가중치]
    # pairs: (평균손실 float, 실제 표본 수 int) 튜플의 반복 가능한 객체.
    # 반환: sum(loss*n)/sum(n)인 Python float. pairs가 비면 ValueError.
    # n은 bool이 아닌 양의 int, loss는 유한한 숫자여야 합니다. 아니면 ValueError.
    # 금지: batch 평균의 단순 평균, 고정 batch_size 곱셈, 입력 list 변경.
    # 완료: [(0.1,4),(0.2,4),(0.9,2)] -> 0.3. iterator 입력도 한 번 순회하여 처리합니다.
    # >>> X05-2
    # TODO X05-2: 위 요구사항과 공개 테스트를 만족하도록 구현하세요.
    raise NotImplementedError("TODO X05-2")
    # <<< X05-2
