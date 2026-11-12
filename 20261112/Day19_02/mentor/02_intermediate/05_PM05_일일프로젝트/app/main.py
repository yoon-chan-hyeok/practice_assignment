from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db import get_engine
from app.routers.knowledge import router

# 강사 해설: Day17의 URL·Method·입력·응답 계약을 유지하고 저장소만 PostgreSQL로 교체합니다.
app = FastAPI(title="Knowledge API · PostgreSQL · Applied")
app.include_router(router)

@app.get("/health")
def health():
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status":"ok", "database":"reachable"}
    except OperationalError as exc:
        raise HTTPException(503, "Database unavailable") from exc
