"""
Camada de acesso ao banco de dados.
Aqui centralizamos a conexão com o SQLite e a criação das tabelas
a partir do arquivo schema.sql.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.config import DATABASE_PATH

SCHEMA_FILE = Path(__file__).parent.parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome (ex: linha["email"])
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_db():
    """
    Context manager usado nas rotas com 'with get_db() as conn:'.
    Garante commit automático em caso de sucesso e rollback em caso de erro.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Cria as tabelas do banco (se ainda não existirem). Chamado ao iniciar a API."""
    conn = get_connection()
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as arquivo:
            conn.executescript(arquivo.read())
        conn.commit()
    finally:
        conn.close()
