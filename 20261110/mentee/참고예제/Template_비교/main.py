"""PPT 45·78쪽 비교 시연. HTML 화면 제작은 필수 과제가 아닙니다."""
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from storage import LOCK, read_data

BASE = Path(__file__).resolve().parent
app = FastAPI(title="JSON / Template 비교")
templates = Jinja2Templates(directory=BASE / "templates")


@app.get("/api/knowledge")
def list_knowledge():
    with LOCK:
        return read_data()["entries"]


@app.get("/web/knowledge", response_class=HTMLResponse)
def knowledge_page(request: Request):
    with LOCK:
        data = read_data()
    return templates.TemplateResponse(
        request=request, name="knowledge.html", context={"entries": data["entries"]}
    )
