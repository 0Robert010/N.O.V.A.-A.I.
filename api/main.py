from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from api.services.learner import LearnerService
from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "nova_memory.db"
connection = initialize_database(DB_PATH)
manager = KnowledgeManager(connection)
service = LearnerService(manager)

app = FastAPI(title="NOVA AI v0.2", version="0.2")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web")), name="static")

from api.routes.knowledge import router as knowledge_router
from api.routes.learning import router as learning_router

app.include_router(knowledge_router)
app.include_router(learning_router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    index_path = BASE_DIR / "web" / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
