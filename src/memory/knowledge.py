from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from sqlalchemy.engine import Engine, Connection as SAConnection
    from sqlalchemy import select
    SQLALCHEMY_AVAILABLE = True
except Exception:
    Engine = None
    SAConnection = None
    SQLALCHEMY_AVAILABLE = False

from src.memory.db import knowledge as knowledge_table, relationships as relationships_table


class KnowledgeManager:
    """Gerencia conceitos armazenados na memória artificial da NOVA.

    Suporta tanto uma `sqlite3.Connection` quanto um `sqlalchemy.Engine`/`Connection`.
    """

    def __init__(self, connection: Any) -> None:
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

        existing = self.get_concept_by_name(name)
        if existing is not None:
            return int(existing["id"])

        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

        # sqlite3.Connection path
        if isinstance(self.connection, sqlite3.Connection):
            cursor = self.connection.execute(
                """
                INSERT INTO knowledge (name, category, description, source, confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name.strip(), category.strip(), description.strip(), source.strip(), confidence, created_at),
            )
            self.connection.commit()
            return int(cursor.lastrowid)

        # SQLAlchemy Engine/Connection path
        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True

        try:
            with sa_conn.begin():
                result = sa_conn.execute(
                    knowledge_table.insert().values(
                        name=name.strip(),
                        category=category.strip(),
                        description=description.strip(),
                        source=source.strip(),
                        confidence=float(confidence),
                        created_at=created_at,
                    )
                )
                inserted_id = None
                try:
                    inserted_id = int(result.inserted_primary_key[0])
                except Exception:
                    # fallback: try to fetch by name
                    row = sa_conn.execute(select(knowledge_table).where(knowledge_table.c.name == name.strip())).fetchone()
                    inserted_id = int(row[knowledge_table.c.id])
                return inserted_id
        finally:
            if engine_used:
                sa_conn.close()

    def get_concept_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Busca um conceito pelo nome."""
        # sqlite3 path
        if isinstance(self.connection, sqlite3.Connection):
            row = self.connection.execute(
                "SELECT * FROM knowledge WHERE name = ?",
                (name.strip(),),
            ).fetchone()
            return dict(row) if row is not None else None

        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True
        try:
            row = sa_conn.execute(select(knowledge_table).where(knowledge_table.c.name == name.strip())).fetchone()
            if row is None:
                return None
            return dict(row._mapping)
        finally:
            if engine_used:
                sa_conn.close()

    def search_concepts(self, query: str) -> List[Dict[str, Any]]:
        """Busca conceitos por nome, categoria ou descrição."""
        search_pattern = f"%{query.strip()}%"
        # sqlite3 path
        if isinstance(self.connection, sqlite3.Connection):
            rows = self.connection.execute(
                """
                SELECT * FROM knowledge
                WHERE name LIKE ? OR category LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
                """,
                (search_pattern, search_pattern, search_pattern),
            ).fetchall()
            return [dict(row) for row in rows]

        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True
        try:
            stmt = select(knowledge_table).where(
                knowledge_table.c.name.like(search_pattern)
                | knowledge_table.c.category.like(search_pattern)
                | knowledge_table.c.description.like(search_pattern)
            ).order_by(knowledge_table.c.created_at.desc())
            rows = sa_conn.execute(stmt).fetchall()
            return [dict(r._mapping) for r in rows]
        finally:
            if engine_used:
                sa_conn.close()

    def list_concepts(self) -> List[Dict[str, Any]]:
        """Lista todos os conceitos cadastrados."""
        # sqlite3 path
        if isinstance(self.connection, sqlite3.Connection):
            rows = self.connection.execute(
                "SELECT * FROM knowledge ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]

        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True
        try:
            stmt = select(knowledge_table).order_by(knowledge_table.c.created_at.desc())
            rows = sa_conn.execute(stmt).fetchall()
            return [dict(r._mapping) for r in rows]
        finally:
            if engine_used:
                sa_conn.close()

    def add_relationship(self, *, source_name: str, target_name: str, relation_type: str) -> int:
        """Cria um vínculo entre dois conceitos conhecidos."""
        source = self.get_concept_by_name(source_name)
        target = self.get_concept_by_name(target_name)
        if source is None or target is None:
            raise ValueError("Os dois conceitos precisam existir antes de criar uma relação.")
        if not relation_type.strip():
            raise ValueError("O tipo de relação não pode ficar vazio.")

        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if isinstance(self.connection, sqlite3.Connection):
            cursor = self.connection.execute(
                """
                INSERT INTO relationships (source_id, target_id, relation_type, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (source["id"], target["id"], relation_type.strip(), created_at),
            )
            self.connection.commit()
            return int(cursor.lastrowid)

        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True
        try:
            with sa_conn.begin():
                result = sa_conn.execute(
                    relationships_table.insert().values(
                        source_id=int(source["id"]),
                        target_id=int(target["id"]),
                        relation_type=relation_type.strip(),
                        created_at=created_at,
                    )
                )
                try:
                    return int(result.inserted_primary_key[0])
                except Exception:
                    row = sa_conn.execute(select(relationships_table).where(relationships_table.c.source_id == source["id"]).where(relationships_table.c.target_id == target["id"]).where(relationships_table.c.relation_type == relation_type.strip())).fetchone()
                    return int(row[relationships_table.c.id])
        finally:
            if engine_used:
                sa_conn.close()

    def list_relationships(self) -> List[Dict[str, Any]]:
        """Lista as relações atualmente registradas na memória."""
        if isinstance(self.connection, sqlite3.Connection):
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

        sa_conn = self.connection
        engine_used = False
        if SQLALCHEMY_AVAILABLE and isinstance(self.connection, Engine):
            sa_conn = self.connection.connect()
            engine_used = True
        try:
            stmt = (
                select(
                    relationships_table.c.id,
                    relationships_table.c.relation_type,
                    relationships_table.c.created_at,
                    knowledge_table.c.name.label("source_name"),
                    knowledge_table.c.name.label("target_name"),
                )
                .select_from(
                    relationships_table.join(knowledge_table.alias("k1"), relationships_table.c.source_id == knowledge_table.c.id)
                )
            )
            # simpler: perform raw join via text if needed
            rows = sa_conn.execute(
                "SELECT r.id, r.relation_type, r.created_at, k1.name AS source_name, k2.name AS target_name FROM relationships r JOIN knowledge k1 ON k1.id = r.source_id JOIN knowledge k2 ON k2.id = r.target_id ORDER BY r.created_at DESC"
            ).fetchall()
            return [dict(r._mapping) for r in rows]
        finally:
            if engine_used:
                sa_conn.close()

    def build_contextual_answer(self, question: str) -> str:
        """Constrói uma resposta mais natural e contextual com base na memória da NOVA."""
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
                    return "Ainda não tenho esse conhecimento na memória. Posso aprender isso para você, se quiser."
                concept = results[0]

        related = [
            relationship["target_name"]
            for relationship in self.list_relationships()
            if relationship["source_name"] == concept["name"]
        ]

        if related:
            related_text = ", ".join(related)
            return (
                f"Eu lembro que {concept['name']} é um conceito de {concept['category']} e está ligado a {related_text}. "
                f"Minha memória registra: {concept['description']}"
            )

        return (
            f"Eu lembro que {concept['name']} pertence à categoria {concept['category']}. "
            f"Resumo da memória: {concept['description']}"
        )
