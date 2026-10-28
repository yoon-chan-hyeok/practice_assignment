"""지표 계산을 한곳에 모읍니다. 정상적인 0/1 두 클래스 입력을 전제로 합니다."""
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def summarize(y, prediction, probability):
    """판정은 F1에, 연속 점수는 AUC에 사용합니다. 사람의 보고서 판단은 자동 채점하지 않습니다."""
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    # TODO H07m: F1은 prediction으로, ROC-AUC는 probability로 계산하세요.
    f1 = auc = 0.0
    # TODO 끝
    return {"n": len(y), "Accuracy": accuracy_score(y, prediction),
            "Precision": precision_score(y, prediction, zero_division=0),
            "Recall": recall_score(y, prediction, zero_division=0), "F1": f1, "ROC_AUC": auc,
            "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp), "actual_failed": int(sum(y))}
