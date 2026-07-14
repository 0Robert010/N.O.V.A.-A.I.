from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class KnowledgeManager:
    """Gerencia conceitos armazenados na memória artificial da NOVA."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add_concept(
        self,
        *,
        name: str,
        category: str,
        description: str,
        source: str,
        confidence: float,
    ) -> int:
        """Adiciona um novo conceito à base de conhecimento."""
        if not name.strip():
            raise ValueError("O nome do conceito não pode ficar vazio.")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("O nível de confiança deve estar entre 0.0 e 1.0.")

        # O timestamp de criação é salvo para manter uma ordem temporal simples dos conceitos.
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        cursor = self.connection.execute(
            """
            INSERT INTO knowledge (name, category, description, source, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name.strip(), category.strip(), description.strip(), source.strip(), confidence, created_at),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def get_concept_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Busca um conceito pelo nome."""
        row = self.connection.execute(
            "SELECT * FROM knowledge WHERE name = ?",
            (name.strip(),),
        ).fetchone()
        return dict(row) if row is not None else None

    def search_concepts(self, query: str) -> List[Dict[str, Any]]:
        """Busca conceitos por nome, categoria ou descrição."""
        search_pattern = f"%{query.strip()}%"
        rows = self.connection.execute(
            """
            SELECT * FROM knowledge
            WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
            """,
            (search_pattern, search_pattern, search_pattern),
        ).fetchall()
        return [dict(row) for row in rows]

    def list_concepts(self) -> List[Dict[str, Any]]:
        """Lista todos os conceitos cadastrados."""
        rows = self.connection.execute(
            "SELECT * FROM knowledge ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]
