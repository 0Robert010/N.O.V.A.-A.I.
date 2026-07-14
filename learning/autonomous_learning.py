from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from src.memory.database import initialize_database
from src.memory.knowledge import KnowledgeManager


class AutonomousLearner:
    """Simula um processo simples de aprendizado autônomo a partir de arquivos de texto."""

    def __init__(
        self,
        *,
        manager: Optional[KnowledgeManager] = None,
        input_dir: Optional[Path | str] = None,
        log_path: Optional[Path | str] = None,
        db_path: Optional[Path | str] = None,
    ) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.input_dir = Path(input_dir or os.getenv("NOVA_INPUT_DIR") or base_dir / "knowledge_input").resolve()
        self.log_path = Path(log_path or os.getenv("NOVA_LOG_PATH") or base_dir / "logs" / "learning.log").resolve()
        self.db_path = Path(db_path or os.getenv("NOVA_DB_PATH") or base_dir / "nova_memory.db").resolve()
        self.connection = initialize_database(self.db_path)
        self.manager = manager or KnowledgeManager(self.connection)
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def scan_for_new_files(self) -> List[Path]:
        """Verifica arquivos .txt e tenta transformar seu conteúdo em conhecimento."""
        discovered_files = sorted(self.input_dir.glob("*.txt"))
        learned_files: List[Path] = []
        for file_path in discovered_files:
            if file_path.name.startswith("."):
                continue
            self._log(f"Analisando arquivo {file_path.name}")
            content = file_path.read_text(encoding="utf-8")
            concept = self._extract_concept(file_path.name, content)
            if concept is None:
                continue
            self.manager.add_concept(
                name=concept["name"],
                category=concept["category"],
                description=concept["description"],
                source=file_path.name,
                confidence=0.8,
            )
            self._log(
                "Novo conhecimento adquirido:\n"
                f"Nome:\n{concept['name']}\n\n"
                f"Categoria:\n{concept['category']}\n\n"
                f"Fonte:\n{file_path.name}"
            )
            learned_files.append(file_path)
        return learned_files

    def _extract_concept(self, filename: str, content: str) -> Optional[dict]:
        cleaned_content = re.sub(r"\s+", " ", content).strip()
        if not cleaned_content:
            return None

        name = self._infer_name(filename, cleaned_content)
        category = self._infer_category(filename, cleaned_content)
        description = cleaned_content[:180]
        return {"name": name, "category": category, "description": description}

    def _infer_name(self, filename: str, content: str) -> str:
        stem = Path(filename).stem.replace("_", " ").replace("-", " ")
        words = [part for part in re.split(r"[^A-Za-z0-9]+", stem) if part]
        if words:
            return " ".join(word.capitalize() for word in words)
        first_sentence = content.split(".")[0]
        return first_sentence[:40].strip() or "Conhecimento"

    def _infer_category(self, filename: str, content: str) -> str:
        lower_content = content.lower()
        if any(term in lower_content for term in ["program", "python", "code", "syntax"]):
            return "Programação"
        if any(term in lower_content for term in ["database", "sql", "table"]):
            return "Banco de dados"
        return "Geral"

    def _log(self, message: str) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        entry = f"[{timestamp}]\n{message}\n"
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(entry + "\n")
        # Try to broadcast to any connected websocket clients (non-blocking)
        try:
            import asyncio
            from src.events.broadcast import broadcast as _broadcast
            asyncio.create_task(_broadcast(f"[{timestamp}] {message}"))
        except Exception:
            pass
