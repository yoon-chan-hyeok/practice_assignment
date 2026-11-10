"""내 PC에서 첫 요청 성공시키기. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response

app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # BEGIN B01-01
    # TODO B01-01: status 키의 값이 ok인 dict를 반환하세요. GET /health의 본문은 {"status":"ok"}여야 합니다.
    # 힌트: return을 사용합니다.
    # 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
    raise NotImplementedError("B01-01를 먼저 완성하세요.")
    # END B01-01
