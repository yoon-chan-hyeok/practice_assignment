# 04 · 예상 결과

Token IDs (2,5) → Token Vectors (2,5,8) → Encoder 출력 (2,5,8). nhead=2는 d_model=8을 나눌 수 있음.

## 완료 검증

Padding Key Mask는 PAD Query 출력까지 자동 0으로 만들지 않음
