"""실습 02: AUC에는 0/1 판정이 아니라 실패 클래스의 연속 점수를 넣습니다."""
from sklearn.metrics import roc_auc_score, roc_curve
# 정상적인 원리 예제 4건입니다. 수업용 파일의 test 결과가 아닙니다.
y = [0, 0, 1, 1]
score = [0.10, 0.40, 0.35, 0.80]
# TODO B02: roc_auc_score에 실제값과 연속 점수를 넣으세요.
auc = 0.0
# TODO 끝
fpr, tpr, thresholds = roc_curve(y, score)
print("FPR:", fpr.round(2).tolist())
print("TPR:", tpr.round(2).tolist())
print(f"AUC: {auc:.2f}")
print("양성 점수 0.35·0.80과 음성 점수 0.10·0.40을 네 번 비교하세요.")
