"""HTTP와 저장 책임을 구분하는 지식 관리 API입니다."""
from fastapi import FastAPI
from app.routers import knowledge

app = FastAPI(title="Knowledge API")
# BEGIN H06-01
# TODO H06-01: knowledge 모듈의 router를 app에 포함하세요. 추가 prefix를 붙이지 마세요.
# 아래 미완성 표시를 지우고 요구한 코드를 작성하세요.
pass  # 앱은 시작되지만 아직 지식 Router는 연결되지 않았습니다.
# END H06-01

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}
