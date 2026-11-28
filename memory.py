import sqlite3
from config import DB_PATH

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS facts ("
        "id INTEGER PRIMARY KEY, text TEXT NOT NULL, "
        "created TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn

def save_fact(text):
    conn = _connect()
    with conn:
        conn.execute("INSERT INTO facts (text) VALUES (?)", (text,))
    conn.close()
    
def all_facts():
    conn = _connect()
    rows = conn.execute("SELECT text FROM facts ORDER BY id").fetchall()
    conn.close()
    return [row[0] for row in rows]

def clear():
    conn = _connect()
    with conn:
        conn.execute("DELETE FROM facts")
    conn.close()
