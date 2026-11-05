# 실습02_BN정책 · BatchNorm 동결
PPT 실습 02, 25쪽. 직접 완성할 곳: D02.
`main.py`의 TODO 위 주석에 요구사항이 있습니다. 자료와 학습 골격은 제공되어 있습니다.

```powershell
python main.py
```
파일이 있는 폴더에서 실행합니다. 입력: `../data/`, 결과: 이 폴더의 `outputs/`.
참고하는 제공 모듈: `../day14_vision/models.py`, `engine.py`, `explain.py`.

## 예상 출력
```text
freeze_bn  accuracy  macro_f1  bn_shift
      True       1.0       1.0    0.0000
     False       1.0       1.0    0.0777
```
실행시간은 환경별로 달라집니다. exact label 값·배열 모양·행 수와 평가 정책을 우선 대조하세요.

## 설명
고정 Backbone과 새 Head는 각각 무엇을 학습하는가? 공식 ResNet18과 소형 source의 출처는 같은가?

본인 답: ___________________

## 완료 기준
요구 코드와 출력 표를 확인합니다. CSV·PNG가 만들어지면 실제로 열어 수치와 표시가 일치하는지 봅니다. test를 모델에 넣지 않습니다.
`nn.Linear(in_features, out_features, bias=True)`: 입력·출력 수 **필수**, bias는 선택. `resnet18(*, weights=None, progress=True)`는 필수 위치 인자가 없으며 `weights`는 키워드 인자입니다. `np.load(file, allow_pickle=False)`는 배열 묶음을 읽는 제공 코드입니다. `.requires_grad`는 함수가 아니라 Parameter 속성입니다.
