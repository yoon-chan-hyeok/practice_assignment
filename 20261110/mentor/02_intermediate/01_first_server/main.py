"""내 PC에서 첫 요청 성공시키기. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response

# BEGIN A01-01
# 해설 A01-01: title과 description은 문서의 메타정보이며 기능을 구현하는 코드는 아닙니다.
app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")
# END A01-01

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    # BEGIN A01-02
    # 해설 A01-02: 이 확인은 API 경로가 응답한다는 뜻이며 DB나 모델 전체 점검은 아닙니다.
    return {"status": "ok"}
    # END A01-02

@app.get("/hello")
def hello(name: str = "수강생"):
    # BEGIN A01-03
    # 해설 A01-03: name은 Path에 없고 기본값이 있는 문자열 매개변수이므로 선택 Query로 받습니다.
    return {"message": f"안녕하세요, {name}"}
    # END A01-03
