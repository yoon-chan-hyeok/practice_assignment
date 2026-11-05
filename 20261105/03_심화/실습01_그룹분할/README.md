# 실습01_그룹분할 · 그룹 분할
PPT 실습 01, 15쪽. 직접 완성할 곳: D01.
`main.py`의 TODO 위 주석에 요구사항이 있습니다. 자료와 학습 골격은 제공되어 있습니다.

```powershell
python main.py
```
파일이 있는 폴더에서 실행합니다. 입력: `../data/`, 결과: 이 폴더의 `outputs/`.
참고하는 제공 모듈: `../day14_vision/models.py`, `engine.py`, `explain.py`.

## 예상 출력
```text
이미지 무작위 분할 그룹 중복: 37
그룹 단위 분할 그룹 중복: 0
주의: GroupShuffleSplit이 클래스 비율까지 보장하지 않습니다.
```
실행시간은 환경별로 달라집니다. exact label 값·배열 모양·행 수와 평가 정책을 우선 대조하세요.

## 설명
클래스 이름을 바꾸면 어떤 계약이 바뀌는가? train의 비율과 valid의 비율을 왜 따로 보는가?

본인 답: ___________________

## 완료 기준
요구 코드와 출력 표를 확인합니다. CSV·PNG가 만들어지면 실제로 열어 수치와 표시가 일치하는지 봅니다. test를 모델에 넣지 않습니다.
`ImageFolder(root, transform=None)`: **root 필수**, 이미지 변환 transform은 선택. `.class_to_idx`는 클래스 이름→번호, `.targets`는 파일 순서와 같은 라벨 목록입니다. `.samples`를 보는 것은 학습이 아닙니다.
