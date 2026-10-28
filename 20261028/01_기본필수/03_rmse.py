"""실습 03: 같은 회귀 문제에서도 주 지표에 따라 후보의 순서가 달라집니다."""
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
y = [100, 200, 300, 400]  # 실제 실행시간(ms)
predictions = {"A": [100, 200, 300, 480], "B": [130, 230, 330, 430]}
for name, pred in predictions.items():
    mae = mean_absolute_error(y, pred)
    # TODO B03: 같은 y·pred로 RMSE를 계산하세요. 함수 이름의 root는 제곱근을 뜻합니다.
    rmse = 0.0
    # TODO 끝
    print(f"{name}: MAE={mae:.1f}ms, RMSE={rmse:.1f}ms")
print("실행시간 단위 ms를 함께 적으세요. 교차검증은 06번에서 이어집니다.")
