"""
database.py — SQLite persistence layer for the Personal Finance Tracker.
Stores every detected transaction across sessions.
"""
from __future__ import annotations

import sqlite3
import os
from contextlib import contextmanager
from typing import Generator

DB_PATH = os.path.join(os.path.dirname(__file__), "finanzas.db")


@contextmanager
def _get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a SQLite connection that auto-closes on exit."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist yet."""
    with _get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacciones (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha     TEXT    NOT NULL,
                concepto  TEXT    NOT NULL,
                monto     REAL    NOT NULL,
                categoria TEXT    NOT NULL,
                tipo      TEXT    NOT NULL   -- 'ingreso' | 'gasto'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reportes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha     TEXT    NOT NULL,
                nombre    TEXT    NOT NULL,
                path      TEXT    NOT NULL
            )
        """)
        conn.commit()


def insertar_transaccion(
    fecha: str,
    concepto: str,
    monto: float,
    categoria: str,
    tipo: str,
) -> None:
    """Insert a single transaction row."""
    with _get_connection() as conn:
        conn.execute(
            "INSERT INTO transacciones (fecha, concepto, monto, categoria, tipo) "
            "VALUES (?, ?, ?, ?, ?)",
            (fecha, concepto, monto, categoria, tipo),
        )
        conn.commit()


def obtener_transacciones() -> list[dict]:
    """Return all transactions ordered newest-first."""
    with _get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM transacciones ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def insertar_reporte(fecha: str, nombre: str, path: str) -> int:
    """Insert a report record and return its ID."""
    with _get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO reportes (fecha, nombre, path) VALUES (?, ?, ?)",
            (fecha, nombre, path),
        )
        conn.commit()
        return cursor.lastrowid


def obtener_reportes() -> list[dict]:
    """Return all generated reports ordered newest-first."""
    with _get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM reportes ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def eliminar_todas() -> None:
    """Delete every transaction (useful for testing)."""
    with _get_connection() as conn:
        conn.execute("DELETE FROM transacciones")
        conn.execute("DELETE FROM reportes")
        conn.commit()
