import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "recruitlens.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS parse_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            filename        TEXT,
            parsed_at       TEXT,
            name            TEXT,
            email           TEXT,
            phone           TEXT,
            linkedin        TEXT,
            skills          TEXT,
            experience      TEXT,
            education       TEXT,
            summary         TEXT,
            ats_score       INTEGER DEFAULT 0,
            years_experience REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def save_parse_result(
    filename: str,
    parsed: dict,
    ats_score: int = 0,
    years_exp: float = 0.0,
):
    init_db()
    conn = _get_conn()
    conn.execute(
        """
        INSERT INTO parse_history
          (filename, parsed_at, name, email, phone, linkedin,
           skills, experience, education, summary, ats_score, years_experience)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            datetime.now().isoformat(timespec="seconds"),
            parsed.get("name", ""),
            parsed.get("email", ""),
            parsed.get("phone", ""),
            parsed.get("linkedin", ""),
            json.dumps(parsed.get("skills", [])),
            json.dumps(parsed.get("experience", [])),
            json.dumps(parsed.get("education", [])),
            parsed.get("summary", ""),
            ats_score,
            years_exp,
        ),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 100) -> list[dict]:
    init_db()
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM parse_history ORDER BY parsed_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["skills"] = json.loads(d["skills"] or "[]")
        d["experience"] = json.loads(d["experience"] or "[]")
        d["education"] = json.loads(d["education"] or "[]")
        result.append(d)
    return result


def delete_record(record_id: int):
    init_db()
    conn = _get_conn()
    conn.execute("DELETE FROM parse_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def clear_history():
    init_db()
    conn = _get_conn()
    conn.execute("DELETE FROM parse_history")
    conn.commit()
    conn.close()
