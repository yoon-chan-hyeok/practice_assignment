# 실습 02 · 심화 · AUC계산불가와OOF탐색

PPT: **27·88·90 / E25·E26**. 기본필수부터 수행하고 응용·심화는 선택적으로 확장합니다. 한 시간에 세 단계를 모두 끝내야 하는 과제가 아닙니다.

## 목표와 범위
ROC-AUC는 연속 점수의 순위를, 임계값은 실제로 행동할 클래스를 결정합니다. 두 문제를 구분합니다.

수강생용: main.py의 NotImplementedError가 있는 함수만 우선 완성합니다. 입력과 실행 골격은 제공되어 있습니다.

## 입력과 구현 계약
외부 다운로드나 API 호출은 없습니다. 작은 수치 예제는 main.py에, 공통 요청100건과 고정 분할은 역할 폴더의 data/에 있습니다. 제공 로더는 train60·valid20만 반환하고 test는 설정 확정 단계 전 모델에 전달하지 않습니다.

- `safe_auc(y, score)` — [D8-02H1] 두클래스면float,한클래스면None. 빈입력·길이다름·잘못된라벨·NaN은ValueError.
- `oof_threshold_study(dev)` — [D8-02H2] train60의Logistic OOF확률로t=.3,.5,.7의F1/Recall표반환. 기본최종lock과분리.

## 실행
역할 폴더를 VS Code의 **폴더 열기**로 열고, 같은 폴더에서 다음 명령을 실행합니다. Python 환경은 최상위 README를 따릅니다.

```text
python "ex02_roc_threshold/03_심화/main.py"
python tools/check_practice.py --exercise 2 --level advanced
```

실제 출력은 이 실습 폴더의 `outputs/`에 생성됩니다. 실행 중 생성한 파일을 `expected_outputs/`에 복사하여 맞추는 것이 아니라, 소스코드로 다시 만들어야 합니다.

## 완료 기준
AUC:null / OOF F1 .625,.533,.435

출력 파일: **single_class.json, oof_threshold_study.csv**. `expected_output.txt`는 정답 코드의 실제 표준출력이고, `expected_outputs/`는 실제 생성한 예시 파일입니다. 검사는 부동소수점 허용오차를 사용합니다. 환경이나 실험 조건을 바꾼 결과는 별도 실험으로 구분하세요.

## 힌트와 점검
OOF예측으로임계값을고르면그점수에도선택편향이있습니다. 최종test를이용한임계값변경은하지않습니다.

이 실습의 모델 실험과 군집 분석에는 보관 test20을 사용하지 않습니다. 설명용 작은 배열은 test 데이터가 아닙니다.

## 제출
main.py, outputs/, worksheet.md를 보관합니다. 기본필수를 마친 후 이전 함수를 다음 단계에 재사용할 수 있습니다. 07~08에서는 `day8_final/` 한 프로젝트를 이어서 사용합니다.
