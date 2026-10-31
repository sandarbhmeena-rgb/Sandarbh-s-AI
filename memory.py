import sqlite3
from pathlib import Path

DB_PATH = Path("database/memory.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def connect():
    return sqlite3.connect(DB_PATH)


def setup_memory():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                information TEXT NOT NULL
            )
        """)


def save_memory(information):
    with connect() as db:
        db.execute(
            "INSERT INTO memories (information) VALUES (?)",
            (information,)
        )


def get_memories():
    with connect() as db:
        rows = db.execute(
            "SELECT id, information FROM memories ORDER BY id DESC"
        ).fetchall()

    return rows


def delete_memory(memory_id):
    with connect() as db:
        db.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,)
        )