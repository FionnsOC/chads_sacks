import sqlite3
from flask import g
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "business.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with open(BASE_DIR / "schema.sql") as f:
        get_db().executescript(f.read())

def save_payout(bags, per_employee, fund):
    """Store one payout: one row in payouts, one entry per person."""
    db = get_db()
    with db:  # commits if everything works, undoes everything if not
        cur = db.execute("INSERT INTO payouts (bags) VALUES (?)", (bags,))
        payout_id = cur.lastrowid
        rows = []
        for p in db.execute("SELECT id, kind FROM people"):
            amount = fund if p["kind"] == "fund" else per_employee
            rows.append((payout_id, p["id"], amount))
        db.executemany(
            "INSERT INTO entries (payout_id, person_id, amount_cp) VALUES (?, ?, ?)",
            rows,
        )

def get_balances():
    return get_db().execute("""
        SELECT p.name, p.kind, COALESCE(SUM(e.amount_cp), 0) AS balance
        FROM people p
        LEFT JOIN entries e ON e.person_id = p.id
        GROUP BY p.id
        ORDER BY p.kind, p.name
    """).fetchall()