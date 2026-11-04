# Vision Pipeline 엔지니어링 보고서

환경·명령·버전·코덱: ___
핵심/선택으로 완성한 TODO: ___

## 좌표·배열 계약
입력 stride·메모리 공유와 기준 색 검사: ___
실제 sx/sy·padding·왕복 오차: ___

## 품질와 비용
참조영상/마스크 출처와 품질 정의: ___
Pareto 후보·시간 변동·객체 손실: ___

## 병렬 처리·재현
Worker1/2의 PNG hash·설정 비교: ___
seed/ID/variant와 전역 RNG 보존: ___
valid/test 무작위 증강 금지 근거: ___

## 영상 회계와 한계
block/drop의 decoded·written·dropped: ___
큐 capacity·지연 측정 범위·Frame index 기록: ___
CFR 재생시간 변화·PTS 미보존: ___

## 실패 복구
원본/config/출력 변경 시 처리한 항목: ___
실패 로그·최종 종료코드·재시도 결과: ___

## 검증 결론
통과·실패·skip 테스트와 미검증 환경: ___
성능이 좋아 보인다는 이유만으로 배포할 수 없는 조건: ___
