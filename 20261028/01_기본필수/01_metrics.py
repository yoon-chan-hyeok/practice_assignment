"""실습 01: 실제 실패 6건인 손계산 예제입니다. 아직 모델을 학습하지 않습니다."""
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
# 행은 실제, 열은 예측입니다. 1은 좋은 결과가 아니라 관심 클래스인 '실패'입니다.
y = [0]*14 + [1]*6
pred = [0]*10 + [1]*4 + [0]*4 + [1]*2
print("혼동행렬(행 실제 / 열 예측, 성공0·실패1)")
print(confusion_matrix(y, pred, labels=[0, 1]))
# TODO B01: 네 지표 함수에 실제값 y와 예측값 pred를 순서대로 넣으세요. zero_division=0은 분모가 0일 때 0으로 표시하는 정책입니다.
acc = precision = recall = f1 = 0.0
# TODO 끝
print(f"Accuracy={acc:.3f}, Precision={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}")
print("실제 실패 6건 중 발견: 2건")
