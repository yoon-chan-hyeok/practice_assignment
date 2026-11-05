# 실습03_단계적해제 · 단계적 해제
PPT 실습 03, 35쪽. 직접 완성할 곳: D03.
`main.py`의 TODO 위 주석에 요구사항이 있습니다. 자료와 학습 골격은 제공되어 있습니다.

```powershell
python main.py
```
파일이 있는 폴더에서 실행합니다. 입력: `../data/`, 결과: 이 폴더의 `outputs/`.
참고하는 제공 모듈: `../day14_vision/models.py`, `engine.py`, `explain.py`.

## 예상 출력
```text
plan  accuracy  macro_f1  best_epoch
partial_from_start       1.0       1.0           8
 head_then_partial       1.0       1.0           8
epoch 5에서 optimizer 재구성: Head의 이전 적응 상태 초기화. 같은 총 8회 예산 비교.
```
실행시간은 환경별로 달라집니다. exact label 값·배열 모양·행 수와 평가 정책을 우선 대조하세요.

## 설명
requires_grad=False와 eval()은 어떤 점에서 다른가? partial은 어떤 층을 여는가?

본인 답: ___________________

## 완료 기준
요구 코드와 출력 표를 확인합니다. CSV·PNG가 만들어지면 실제로 열어 수치와 표시가 일치하는지 봅니다. test를 모델에 넣지 않습니다.
`AdamW(params, lr=..., weight_decay=...)`: **params 필수**, lr·weight_decay 선택. `zero_grad()`는 누적 기울기 초기화, `backward()`는 미분, `step()`은 실제 갱신입니다. `.eval()`은 gradient를 끄는 함수가 아닙니다.
