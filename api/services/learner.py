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
