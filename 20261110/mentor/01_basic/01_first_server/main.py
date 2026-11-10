"""내 PC에서 첫 요청 성공시키기. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response

app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # BEGIN B01-01
    # 해설 B01-01: dict를 return하면 FastAPI가 JSON 응답으로 직렬화합니다.
    # 해설 B01-01: print는 서버 터미널 출력이므로 HTTP 응답을 대신하지 않습니다.
    return {"status": "ok"}
    # END B01-01

#   bash 창에서 아래 명령어를 통해 서버를 실행할 수 있습니다.
#   python -m uvicorn main:app --host 127.0.0.1 --port 18080 --reload