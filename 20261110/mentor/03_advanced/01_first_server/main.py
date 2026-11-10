"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI, HTTPException, Response

app = FastAPI(title="Knowledge API")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # BEGIN H01-01
    # 해설 H01-01: HTTP 응답과 서버 터미널 print는 다릅니다.
    return {"status": "ok"}
    # END H01-01
