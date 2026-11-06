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

def save_payout(bags, per_employee, fund, dr_year, dr_month, dr_day):
    """Store one payout: one row in payouts, one entry per person."""
    db = get_db()
    with db:  # commits if everything works, undoes everything if not
        cur = db.execute(
            "INSERT INTO payouts (bags, dr_year, dr_month, dr_day) VALUES (?, ?, ?, ?)",
            (bags, dr_year, dr_month, dr_day),
        )
        payout_id = cur.lastrowid
        rows = []
        for p in db.execute("SELECT id, kind FROM people"):
            amount = fund if p["kind"] == "fund" else per_employee
            rows.append((payout_id, p["id"], amount))
        db.executemany(
            "INSERT INTO entries (payout_id, person_id, amount_cp) VALUES (?, ?, ?)",
            rows,
        )

def get_payouts():
    """All payouts, newest in-game date first."""
    return get_db().execute("""
        SELECT id, bags, dr_year, dr_month, dr_day FROM payouts
        ORDER BY dr_year DESC, dr_month DESC, dr_day DESC, id DESC
    """).fetchall()


def get_balances(payout_id):
    """For each person: what the chosen payout added, and the total
    up to and including it (in in-game date order)."""
    return get_db().execute("""
        SELECT p.name, p.kind,
               COALESCE(SUM(e.amount_cp), 0) AS total,
               COALESCE(SUM(CASE WHEN e.payout_id = :pid THEN e.amount_cp END), 0) AS added
        FROM people p
        LEFT JOIN entries e ON e.person_id = p.id
             AND e.payout_id IN (
                 SELECT po.id FROM payouts po, payouts ch
                 WHERE ch.id = :pid
                   AND (po.dr_year, po.dr_month, po.dr_day, po.id)
                       <= (ch.dr_year, ch.dr_month, ch.dr_day, ch.id)
             )
        GROUP BY p.id
        ORDER BY p.kind, p.name
    """, {"pid": payout_id}).fetchall()