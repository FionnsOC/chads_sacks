import sqlite3
from pathlib import Path
from db import DATABASE

BASE_DIR = Path(__file__).resolve().parent

EMPLOYEES = ["Jeff", "Crickets", "Steam", "Bree",
             "Shardon", "Jobyn", "Jiff", "Suffer"]

con = sqlite3.connect(DATABASE)
with open(BASE_DIR / "schema.sql") as f:
    con.executescript(f.read())          # creates the tables if they don't exist

for name in EMPLOYEES:
    con.execute("INSERT OR IGNORE INTO people (name, kind) VALUES (?, 'employee')", (name,))
con.execute("INSERT OR IGNORE INTO people (name, kind) VALUES ('H&E Fund', 'fund')")

con.commit()
con.close()