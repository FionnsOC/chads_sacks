import sqlite3
from db import DATABASE

EMPLOYEES = ["Jeff", "Crickets", "Steam", "Name4",
             "Name5", "Name6", "Name7", "Name8"]   # put your 8 real names here

con = sqlite3.connect(DATABASE)
with open(BASE_DIR / "schema.sql") as f:
    con.executescript(f.read())          # creates the tables if they don't exist

for name in EMPLOYEES:
    con.execute("INSERT OR IGNORE INTO people (name, kind) VALUES (?, 'employee')", (name,))
con.execute("INSERT OR IGNORE INTO people (name, kind) VALUES ('H&E Fund', 'fund')")

con.commit()
con.close()