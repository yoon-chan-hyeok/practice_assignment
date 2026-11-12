from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db import get_engine
from app.errors import DataConflictError, KnowledgeNotFoundError
from app.routers.knowledge import router

app = FastAPI(title="Knowledge API · PostgreSQL · Advanced")
app.include_router(router)

@app.exception_handler(KnowledgeNotFoundError)
async def not_found_handler(_, exc: KnowledgeNotFoundError):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=404, content={"detail":"Knowledge not found", "knowledge_id":exc.knowledge_id})

@app.exception_handler(DataConflictError)
async def conflict_handler(_, exc: DataConflictError):
    from fastapi.responses import JSONResponse
    # TODO H14: DataConflictError를 내부 SQL 노출 없이 409 JSON으로 변환하세요.
    raise NotImplementedError("TODO H14")

@app.get("/health")
def health():
    try:
        # TODO H15: 별도 Connection으로 SELECT 1을 실행하고 정상 상태를 반환하세요.
        raise NotImplementedError("TODO H15")
    except OperationalError as exc:
        raise HTTPException(503, "Database unavailable") from exc
