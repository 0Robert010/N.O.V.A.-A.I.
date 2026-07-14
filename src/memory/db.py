import os
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "nova_memory.db"

# Try to use SQLAlchemy if available; otherwise fall back to a lightweight sqlite3 initializer
SQLALCHEMY_AVAILABLE = False
knowledge = None
relationships = None

try:
    from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        Integer,
        String,
        Text,
        Float,
        DateTime,
        ForeignKey,
    )
    from sqlalchemy.engine import Engine

    SQLALCHEMY_AVAILABLE = True
    metadata = MetaData()

    knowledge = Table(
        "knowledge",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String, nullable=False, unique=True),
        Column("category", String, nullable=False),
        Column("description", Text, nullable=False),
        Column("source", String, nullable=False),
        Column("confidence", Float, nullable=False),
        Column("created_at", String, nullable=False),
    )

    relationships = Table(
        "relationships",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("source_id", Integer, ForeignKey("knowledge.id"), nullable=False),
        Column("target_id", Integer, ForeignKey("knowledge.id"), nullable=False),
        Column("relation_type", String, nullable=False),
        Column("created_at", String, nullable=False),
    )


    def get_database_url(explicit: Optional[str] = None) -> str:
        env = os.getenv("DATABASE_URL")
        if explicit:
            return explicit
        if env:
            return env
        return f"sqlite:///{DEFAULT_DB_PATH}"


    def get_engine(database_url: Optional[str] = None) -> Engine:
        url = get_database_url(database_url)
        connect_args = {}
        if url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        engine = create_engine(url, connect_args=connect_args)
        return engine


    def initialize_database(database_url: Optional[str] = None) -> Engine:
        engine = get_engine(database_url)
        metadata.create_all(engine)
        return engine

except Exception:  # pragma: no cover - fallback when SQLAlchemy is not installed
    import sqlite3

    def initialize_database(database_url: Optional[str] = None):
        resolved = Path(database_url) if database_url else DEFAULT_DB_PATH
        resolved = Path(resolved)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(resolved, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                relation_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        return conn
