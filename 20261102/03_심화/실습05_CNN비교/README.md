# 모델 폭 비교 · 심화

PPT 58쪽. `03_심화` 전체 구조를 유지합니다. 이 실습 폴더에서 실행합니다.

```powershell
python main.py
```

## 구현할 부분

**D05**: 같은 분할에서 폭 8과 16을 비교한다. 힌트: [('small',8,3),('small',16,3)].

## 입력·출력

입력: `../day11_image_classification/data/`의 train/valid 또는 코드에 주어진 정상 Tensor. test는 사용하지 않습니다. 출력은 이 실습의 `outputs/`입니다. 비교용 결과는 `expected/`에서 확인합니다.

```text
small_w8 best 3 valid loss 0.6068 accuracy 0.65
small_w16 best 3 valid loss 0.3722 accuracy 0.95
```

## 완료 기준·기록

코드와 출력 파일을 대조하고 바꾼 조건 1개·고정한 조건 2개를 설명하세요. 원래 입력 shape와 처리 후 shape, 결과를 일반화하기 어려운 이유를 한 문장씩 기록합니다.

- 바꾼 조건: ______
- 고정 조건: ______
- 관찰과 한계: ______
