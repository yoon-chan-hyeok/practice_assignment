from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db import get_engine
from app.routers.knowledge import router

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
