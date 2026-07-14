from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "nova_memory.db"
connection = initialize_database(DEFAULT_DB_PATH)
manager = KnowledgeManager(connection)
service = None


class LearnerService:
    """Expõe operações de memória e estatísticas para a API da NOVA."""

    def __init__(self, manager: KnowledgeManager, started_at: Optional[datetime] = None) -> None:
        self.manager = manager
        self.started_at = started_at or datetime.now(timezone.utc)

    def list_knowledge(self) -> List[Dict[str, Any]]:
        return self.manager.list_concepts()

    def learn_concept(self, *, name: str, category: str, description: str, source: str, confidence: float) -> int:
        return self.manager.add_concept(
            name=name,
            category=category,
            description=description,
            source=source,
            confidence=confidence,
        )

    def learn_from_url(self, url: str) -> int:
        """Busca uma página web e tenta extrair um conceito simples para aprender.

        Usa uma heurística leve (título + primeiro parágrafo) para criar um conceito.
        """
        try:
            import requests
            from bs4 import BeautifulSoup
        except Exception as error:  # pragma: no cover - runtime dependency check
            raise RuntimeError("Dependências para scraping não estão instaladas: requests, beautifulsoup4") from error

        resp = requests.get(url, timeout=8, headers={"User-Agent": "NOVA/0.2 (+https://example)"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title = (soup.title.string.strip() if soup.title and soup.title.string else None) or Path(url).stem.capitalize()
        p = soup.find("p")
        description = (p.get_text().strip() if p else "").strip() or (soup.get_text(separator=" ", strip=True)[:200])

        lower = (title + " " + description).lower()
        if any(term in lower for term in ["program", "python", "code", "javascript", "java", "syntax"]):
            category = "Programação"
        elif any(term in lower for term in ["database", "sql", "sqlite", "postgres", "mysql"]):
            category = "Banco de dados"
        else:
            category = "Geral"

        confidence = 0.7

        concept_id = self.learn_concept(
            name=title,
            category=category,
            description=description,
            source=url,
            confidence=confidence,
        )
        # broadcast asynchronously if possible
        try:
            import asyncio
            from src.events.broadcast import broadcast as _broadcast
            asyncio.create_task(_broadcast(f"[WEB] Aprendido: {title} ({url})"))
        except Exception:
            pass
        return concept_id

    def get_stats(self) -> Dict[str, Any]:
        concepts = self.manager.list_concepts()
        categories = sorted({concept["category"] for concept in concepts})
        elapsed_seconds = max(0, int((datetime.now(timezone.utc) - self.started_at).total_seconds()))
        return {
            "knowledge_count": len(concepts),
            "categories": categories,
            "last_learning": concepts[0]["created_at"] if concepts else None,
            "learning_time_seconds": elapsed_seconds,
        }


def get_learner_service() -> LearnerService:
    global service
    if service is None:
        service = LearnerService(manager)
    return service
