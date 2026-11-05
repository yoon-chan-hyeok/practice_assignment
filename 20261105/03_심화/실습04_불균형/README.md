# 실습04_불균형 · 가중치·샘플러
PPT 실습 04, 47쪽. 직접 완성할 곳: D04.
`main.py`의 TODO 위 주석에 요구사항이 있습니다. 자료와 학습 골격은 제공되어 있습니다.

```powershell
python main.py
```
파일이 있는 폴더에서 실행합니다. 입력: `../data/`, 결과: 이 폴더의 `outputs/`.
참고하는 제공 모듈: `../day14_vision/models.py`, `engine.py`, `explain.py`.

## 예상 출력
```text
balance  accuracy  macro_f1  triangle_recall
   none       1.0       1.0              1.0
 weight       1.0       1.0              1.0
sampler       1.0       1.0              1.0
sampler는 train만 재추출합니다. valid는 원래 분포 그대로입니다.
```
실행시간은 환경별로 달라집니다. exact label 값·배열 모양·행 수와 평가 정책을 우선 대조하세요.

## 설명
Accuracy는 높고 minority Recall은 0일 수 있는가? weight와 sampler는 무엇을 각각 바꾸는가?

본인 답: ___________________

## 완료 기준
요구 코드와 출력 표를 확인합니다. CSV·PNG가 만들어지면 실제로 열어 수치와 표시가 일치하는지 봅니다. test를 모델에 넣지 않습니다.
`f1_score(y_true, y_pred, average="macro", labels=[0,1,2], zero_division=0)`: 실제값·예측값 **필수**, 나머지는 선택 옵션. macro는 클래스별 F1의 동일 가중 평균입니다. `CrossEntropyLoss(weight=...)`는 train 손실에만 클래스 가중치를 적용합니다.
