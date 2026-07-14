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

    def add_relationship(self, *, source_name: str, target_name: str, relation_type: str) -> int:
        """Cria um vínculo entre dois conceitos conhecidos."""
        source = self.get_concept_by_name(source_name)
        target = self.get_concept_by_name(target_name)
        if source is None or target is None:
            raise ValueError("Os dois conceitos precisam existir antes de criar uma relação.")
        if not relation_type.strip():
            raise ValueError("O tipo de relação não pode ficar vazio.")

        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        cursor = self.connection.execute(
            """
            INSERT INTO relationships (source_id, target_id, relation_type, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (source["id"], target["id"], relation_type.strip(), created_at),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_relationships(self) -> List[Dict[str, Any]]:
        """Lista as relações atualmente registradas na memória."""
        rows = self.connection.execute(
            """
            SELECT r.id, r.relation_type, r.created_at, k1.name AS source_name, k2.name AS target_name
            FROM relationships AS r
            JOIN knowledge AS k1 ON k1.id = r.source_id
            JOIN knowledge AS k2 ON k2.id = r.target_id
            ORDER BY r.created_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def build_contextual_answer(self, question: str) -> str:
        """Constrói uma resposta simples e contextual com base na memória da NOVA."""
        normalized_question = question.strip().lower()
        concept = self.get_concept_by_name(question.strip())
        if concept is None:
            keywords = [token for token in normalized_question.replace("?", "").split() if token.isalpha()]
            candidate_terms = []
            for keyword in keywords:
                candidate_terms.append(keyword)
                if len(keyword) > 3:
                    candidate_terms.append(keyword.capitalize())
            for candidate in candidate_terms:
                concept = self.get_concept_by_name(candidate)
                if concept is not None:
                    break
            if concept is None:
                keyword = question.strip().split()[-1]
                results = self.search_concepts(keyword)
                if not results:
                    return "Ainda não tenho esse conhecimento na memória. Posso aprender isso para você."
                concept = results[0]

        related = [
            relationship["target_name"]
            for relationship in self.list_relationships()
            if relationship["source_name"] == concept["name"]
        ]
        if related:
            related_text = ", ".join(related)
            return (
                f"{concept['name']} é um conceito de {concept['category']} associado a {related_text}. "
                f"Minha memória registra que: {concept['description']}"
            )

        return (
            f"{concept['name']} pertence à categoria {concept['category']}. "
            f"Resumo da memória: {concept['description']}"
        )
