from fastapi import FastAPI
from app.routers.knowledge import router

app = FastAPI(title="Day19 AM Knowledge API - Advanced")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
