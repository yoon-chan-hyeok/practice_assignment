# 환경 기록과 장치 연산

해당 폴더를 VS Code로 열어 `main.py`의 TODO를 완성합니다. 함수를 처음부터 재설계하지 않고 제공된 흐름을 사용합니다.

**H01** — CUDA 사용 가능 여부를 보고 실행할 장치를 선택하세요. 드라이버가 있다는 사실만으로 CUDA를 선택하지 마세요.

```powershell
python main.py
```

## 예상 출력

```text
{
  "torch": "2.10.0+cpu",
  "cuda_build": null,
  "cuda_available": false,
  "selected_device": "cpu",
  "calculation": [
    [
      5.0,
      11.0
    ],
    [
      11.0,
      25.0
    ]
  ]
}
```

CPU 검수 결과이며 device·버전과 학습 수치는 환경에 따라 달라질 수 있습니다. 상세 출력은 `expected/console.txt`에도 있습니다.

## 완료 조건

TODO의 계산을 코드로 확인하고 예상 결과와 비교합니다. 자신의 말로 입력 shape, 처리한 단계, 출력의 의미를 설명하세요. 단순히 실행 종료 코드가0인 것만으로 완료하지 않습니다.

## 내 기록

- 확인한 입력 / 출력: 
- 결과의 의미: 
- 잘못 이해했던 내용 또는 질문:
