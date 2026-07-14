from pathlib import Path
import sqlite3
from typing import Optional, Any

from src.memory.db import initialize_database as sa_initialize_database


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "nova_memory.db"


def connect_database(db_path: Optional[Path | str] = None) -> sqlite3.Connection:
    """Compat shim to create or open a sqlite3 connection (used by tests)."""
    resolved_path = Path(db_path or DEFAULT_DB_PATH)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(resolved_path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Optional[Path | str] = None, connection: Optional[Any] = None) -> Any:
    """Initialize database. If a DB-API `connection` is passed, create tables on it.

    Otherwise delegate to SQLAlchemy-based initializer (which may fall back to sqlite3).
    """
    if connection is not None:
        # create tables using raw SQL on the provided connection
        connection.execute(
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
        connection.execute(
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
        connection.commit()
        return connection

    # delegate to SQLAlchemy initializer (will handle env DATABASE_URL or sqlite fallback)
    return sa_initialize_database(db_path)

