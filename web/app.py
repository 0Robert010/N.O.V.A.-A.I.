from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from api.services.learner import LearnerService
from learning.autonomous_learning import AutonomousLearner
from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "nova_memory.db"
connection = initialize_database(DB_PATH)
manager = KnowledgeManager(connection)
service = LearnerService(manager)

app = FastAPI(title="NOVA AI v0.2", version="0.2")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home() -> HTMLResponse:
    index_path = BASE_DIR / "web" / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/knowledge")
async def knowledge() -> JSONResponse:
    return JSONResponse(service.list_knowledge())


@app.get("/stats")
async def stats() -> JSONResponse:
    return JSONResponse(service.get_stats())


@app.post("/learn")
async def learn_concept(payload: dict) -> JSONResponse:
    try:
        concept_id = service.learn_concept(
            name=str(payload.get("name", "")).strip(),
            category=str(payload.get("category", "")).strip(),
            description=str(payload.get("description", "")).strip(),
            source=str(payload.get("source", "")).strip(),
            confidence=float(payload.get("confidence", 0.0)),
        )
        return JSONResponse({"success": True, "concept_id": concept_id})
    except ValueError as error:
        return JSONResponse({"success": False, "error": str(error)}, status_code=400)


@app.post("/learning/run")
async def run_learning() -> JSONResponse:
    learner = AutonomousLearner()
    processed_files = learner.scan_for_new_files()
    return JSONResponse(
        {
            "status": "completed",
            "processed_count": len(processed_files),
            "files": [path.name for path in processed_files],
        }
    )


@app.post("/ask")
async def ask_question(payload: dict) -> JSONResponse:
    question = str(payload.get("question", "")).strip()
    if not question:
        return JSONResponse({"answer": "Por favor, formule uma pergunta."}, status_code=400)
    answer = manager.build_contextual_answer(question)
    return JSONResponse({"answer": answer})


@app.get("/memory")
async def memory_list() -> JSONResponse:
    return JSONResponse(service.list_knowledge())


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
