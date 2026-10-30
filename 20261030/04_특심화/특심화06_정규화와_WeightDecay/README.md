# 특심화 06 · BatchNorm·LayerNorm·Weight Decay

## 목표와 진행 범위
배치 정규화 통계와 가중치 감쇠를 구분하고 숫자 이름의 Sequential에도 안전한 param group을 만든다.

**이번 교시의 구현 파일은 `tasks.py`입니다.** 함수·클래스 문법을 다시 길게 설명하지 않고, 함수 바로 위의 입력·출력·금지 동작·오류 조건·상태 보존·허용오차를 읽고 구현합니다. 골격·실행기·선행 코드는 이미 제공되어 있습니다.

**이 폴더만 따로 복사해 실행할 수 있습니다.** 이전 특심화의 TODO·출력·체크포인트를 요구하지 않습니다. 단, 이 폴더의 `data/`·`tests/`도 함께 복사해야 합니다.

## 구조와 파일 책임
```text
특심화06_정규화와_WeightDecay/
├─ README.md
├─ tasks.py          # 직접 구현하는 문제
├─ run.py            # 제공된 실험 실행기
├─ tests/            # 공개 계약 테스트
├─ expected/         # 실제 CPU 실행 결과, 정답 소스가 아님
└─ reports/review.md # 판단 근거·미검증 범위 기록
```
데이터 파일은 이 폴더의 `data/points.csv`이며 train240·valid80만 사용합니다.
제공 모듈: `support.py`. `outputs/`는 실행 시 생성됩니다. 다른 실습 폴더를 import하지 않습니다.

## 직접 구현할 문제
- **X06-1**: `tasks.py`에서 같은 번호의 요구사항을 읽고 구현합니다.
- **X06-2**: `tasks.py`에서 같은 번호의 요구사항을 읽고 구현합니다.

20~30분 수업 활동에서는 요구사항과 테스트를 먼저 읽고 핵심 구현부터 진행합니다. 07·08의 세 번째 문제는 통합 검증 단계까지 포함합니다. 시간이 부족해도 다음 교시 폴더를 독립적으로 시작할 수 있습니다. 숫자·정답 파일 경로를 하드코딩하거나 `expected/`를 입력으로 사용하는 것은 구현이 아닙니다.

## 실행
VS Code에서 **이 폴더**를 열고 전날 사용한 Python 가상환경을 선택합니다. 정상인 CUDA 환경을 CPU 패키지로 덮어쓰지 않습니다.
```powershell
python -c "import torch; print(torch.__version__)"
python -m unittest discover -s tests -v
python run.py
```
추가 설치는 필요한 패키지만 `python -m pip install pandas numpy matplotlib`로 진행합니다. 이 실습은 CPU로 실행됩니다. CUDA 전용 테스트는 실제 GPU가 없으면 SKIP입니다. 모든 명령은 이 폴더의 터미널 기준이며 다른 경로에서는 run.py의 절대 경로를 사용할 수 있습니다.

미완성 `tasks.py`의 `NotImplementedError`는 정상적인 과제 표시입니다. 테스트를 통과했다는 이유만으로 문항 설명을 생략하지 않습니다.

## 산출물과 예상 결과
주요 생성 파일: `outputs/groups.json`, `outputs/normalization_probe.csv`.
`expected/`에 실제 정답 실행의 CSV·JSON·PNG와 stdout을 제공합니다. 버전·장치에 따라 부동소수점 수치는 조금 다를 수 있으며, 허용오차는 함수 요구사항과 테스트를 기준으로 합니다.

```text
seen  batch_mean_variance  running_mean_mse
norm      batch_size                                              
BatchNorm 2           240.0             0.252282          0.007867
          8           240.0             0.063338          0.001519
          32          240.0             0.013100          0.072565
LayerNorm 2           240.0             0.252282               NaN
          8           240.0             0.063338               NaN
          32          240.0             0.013100               NaN
{
  "groups": [
    {
      "weight_decay": 0.01,
      "tensors": 3,
      "parameters": 320
    },
    {
      "weight_decay": 0.0,
      "tensors": 7,
      "parameters": 98
    }
  ],
  "trainable_parameters": 418,
  "probe_rows": 30,
  "test_used": false
}
```

## 완료 기준
구현 2곳을 채우고 공개 테스트와 run.py를 실행합니다. 원본 보존·손실 집계·상태 복원을 요구한 경우 숫자 출력만 보지 말고 테스트 결과도 확인합니다. `reports/review.md`에 조건·관찰·한계·다음 확인 사항을 적습니다.

## 설명 질문
1. BN running 통계 오차는 batch 크기만으로 결정되는가?
2. 이름에 bn이 없으면 BatchNorm weight를 어떻게 찾아야 하는가?

## 검증 범위
제작 참조 환경: Python 3.13.5 / PyTorch 2.10.0+cpu / Linux. 실제 NVIDIA CUDA·Windows/macOS는 미검증입니다. test 데이터는 모형 학습·선택·추론에 쓰지 않습니다. 합성 데이터·소수 seed 결과를 실서비스 성능 또는 알고리즘의 보편적 순위로 주장하지 않습니다.
