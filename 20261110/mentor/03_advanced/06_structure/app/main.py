"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI
from app.routers import knowledge

app = FastAPI(title="Knowledge API")
# BEGIN H06-01
# 해설 H06-01: APIRouter가 선언되어도 앱에 등록하지 않으면 해당 요청을 처리하지 못합니다.
app.include_router(knowledge.router)
# END H06-01

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}
