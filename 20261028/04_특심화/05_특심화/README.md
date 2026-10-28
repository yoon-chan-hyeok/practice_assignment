# 실습 05 · 심화 · 번호대신소속구조비교

PPT: **57·89·91 / E24**. 기본필수부터 수행하고 응용·심화는 선택적으로 확장합니다. 한 시간에 세 단계를 모두 끝내야 하는 과제가 아닙니다.

## 목표와 범위
군집은 train 수치2열을 사용하는 독립적인 탐색 활동입니다. 성공·실패 라벨을 군집 학습에 넣지 않습니다.

수강생용: main.py의 NotImplementedError가 있는 함수만 우선 완성합니다. 입력과 실행 골격은 제공되어 있습니다.

## 입력과 구현 계약
외부 다운로드나 API 호출은 없습니다. 작은 수치 예제는 main.py에, 공통 요청100건과 고정 분할은 역할 폴더의 data/에 있습니다. 제공 로더는 train60·valid20만 반환하고 test는 설정 확정 단계 전 모델에 전달하지 않습니다.

- `compare_cluster_labels(a, b)` — [D8-05H] 번호일치율,ARI,쌍별소속구조동일여부반환. 키same_number_fraction,ARI,same_partition.

## 실행
역할 폴더를 VS Code의 **폴더 열기**로 열고, 같은 폴더에서 다음 명령을 실행합니다. Python 환경은 최상위 README를 따릅니다.

```text
python "ex05_kmeans/03_심화/main.py"
python tools/check_practice.py --exercise 5 --level advanced
```

실제 출력은 이 실습 폴더의 `outputs/`에 생성됩니다. 실행 중 생성한 파일을 `expected_outputs/`에 복사하여 맞추는 것이 아니라, 소스코드로 다시 만들어야 합니다.

## 완료 기준
번호일치율0 / ARI1 / same_partition=True

출력 파일: **label_permutation.json**. `expected_output.txt`는 정답 코드의 실제 표준출력이고, `expected_outputs/`는 실제 생성한 예시 파일입니다. 검사는 부동소수점 허용오차를 사용합니다. 환경이나 실험 조건을 바꾼 결과는 별도 실험으로 구분하세요.

## 힌트와 점검
정답클래스와군집번호를직접정확도로평가하지않습니다. 군집특성확장은설계기록에씁니다.

이 실습의 모델 실험과 군집 분석에는 보관 test20을 사용하지 않습니다. 설명용 작은 배열은 test 데이터가 아닙니다.

## 제출
main.py, outputs/, worksheet.md를 보관합니다. 기본필수를 마친 후 이전 함수를 다음 단계에 재사용할 수 있습니다. 07~08에서는 `day8_final/` 한 프로젝트를 이어서 사용합니다.
