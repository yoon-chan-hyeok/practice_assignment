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
    return JSONResponse(status_code=409, content={"detail":exc.message})

@app.get("/health")
def health():
    try:
        with get_engine().connect() as conn: conn.execute(text("SELECT 1"))
        return {"status":"ok", "database":"reachable"}
    except OperationalError as exc:
        raise HTTPException(503, "Database unavailable") from exc
