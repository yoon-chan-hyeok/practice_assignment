# ANN 학습 설명

## 파일별 책임
main / model / train / check_gpu / restore의 역할: 

## 학습 순서와 손실 집계
zero_grad → forward → loss → backward → step의 의미: 
마지막 batch24건을 어떻게 집계했는가: 

## 검증과 한계
실제로 사용한 device: 
train/valid/test 각 표본 수와 사용 범위: 
valid 결과: 
단순 합성 데이터에서 높은 정확도가 실제 성능 증명이 아닌 이유: 

## 복원
새 프로세스에서 ID 순서와 예측이 같은가: 
학습 버전과 장치:
