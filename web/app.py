from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager

app = FastAPI(title="NOVA AI", version="0.1")

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

DB_PATH = BASE_DIR.parent / "nova_memory.db"
connection = initialize_database(DB_PATH)
manager = KnowledgeManager(connection)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    concepts = manager.list_concepts()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "version": "v0.1",
            "knowledge_count": len(concepts),
        },
    )


@app.post("/ask")
async def ask_question(payload: dict) -> JSONResponse:
    question = (payload.get("question") or "").strip()
    if not question:
        return JSONResponse({"answer": "Por favor, formule uma pergunta."}, status_code=400)

    answer = manager.build_contextual_answer(question)
    return JSONResponse({"answer": answer})


@app.post("/learn")
async def learn_concept(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    source: str = Form(...),
    confidence: float = Form(...),
) -> JSONResponse:
    try:
        concept_id = manager.add_concept(
            name=name,
            category=category,
            description=description,
            source=source,
            confidence=confidence,
        )
        return JSONResponse({"success": True, "concept_id": concept_id})
    except ValueError as error:
        return JSONResponse({"success": False, "error": str(error)}, status_code=400)


@app.get("/memory")
async def memory_list() -> JSONResponse:
    concepts = manager.list_concepts()
    return JSONResponse(concepts)
