CREATE TABLE IF NOT EXISTS people (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL CHECK (kind IN ('employee', 'fund'))
);

CREATE TABLE IF NOT EXISTS payouts (
    id         INTEGER PRIMARY KEY,
    bags       INTEGER NOT NULL,
    dr_year    INTEGER,
    dr_month   INTEGER,
    dr_day     INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS entries (
    id        INTEGER PRIMARY KEY,
    payout_id INTEGER REFERENCES payouts(id),
    person_id INTEGER NOT NULL REFERENCES people(id),
    amount_cp INTEGER NOT NULL
);