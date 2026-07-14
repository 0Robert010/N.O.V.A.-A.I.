import sqlite3
from pathlib import Path
from typing import Optional


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "nova_memory.db"


def connect_database(db_path: Optional[Path | str] = None) -> sqlite3.Connection:
    """Cria ou abre uma conexão com o banco SQLite da NOVA."""
    # O SQLite é usado aqui para manter a memória persistente e simples, sem dependências externas.
    """Cria ou abre uma conexão com o banco SQLite da NOVA."""
    resolved_path = Path(db_path or DEFAULT_DB_PATH)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(resolved_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: Optional[Path | str] = None, connection: Optional[sqlite3.Connection] = None) -> sqlite3.Connection:
    """Cria as tabelas básicas do sistema de memória artificial."""
    active_connection = connection or connect_database(db_path)
    active_connection.execute(
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
    active_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            target_id INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(source_id) REFERENCES knowledge(id),
            FOREIGN KEY(target_id) REFERENCES knowledge(id)
        )
        """
    )
    active_connection.commit()
    return active_connection
