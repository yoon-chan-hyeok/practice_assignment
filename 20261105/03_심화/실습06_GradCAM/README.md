# 실습06_GradCAM · 가림 비교 Grad-CAM
PPT 실습 06, 68쪽. 직접 완성할 곳: D06.
`main.py`의 TODO 위 주석에 요구사항이 있습니다. 자료와 학습 골격은 제공되어 있습니다.

```powershell
python main.py
```
파일이 있는 폴더에서 실행합니다. 입력: `../data/`, 결과: 이 폴더의 `outputs/`.
참고하는 제공 모듈: `../day14_vision/models.py`, `engine.py`, `explain.py`.

## 예상 출력
```text
고정 target: 0
원본 확률: 0.9993 가림 확률: 0.2356
```
실행시간은 환경별로 달라집니다. exact label 값·배열 모양·행 수와 평가 정책을 우선 대조하세요.

## 설명
Heatmap의 target은 무엇인가? 같은 이미지에서 target이 바뀌면 지도가 달라질 수 있는가?

본인 답: ___________________

## 완료 기준
요구 코드와 출력 표를 확인합니다. CSV·PNG가 만들어지면 실제로 열어 수치와 표시가 일치하는지 봅니다. test를 모델에 넣지 않습니다.
`torch.autograd.grad(outputs, inputs)`: 미분할 scalar·대상 Tensor **필수**. 입력을 수정하지 않고 gradient tuple을 반환합니다. `.mean(dim=(2,3), keepdim=True)`는 공간 평균. `cv2.addWeighted(src1, alpha, src2, beta, gamma)`는 앞의 다섯 인자 **필수**, 같은 좌표·크기의 BGR 이미지끼리 합성합니다.
