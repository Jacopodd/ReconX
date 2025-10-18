# Gestione SQLite
import sqlite3
import json
from datetime import datetime

DB_PATH = "reconx.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        module TEXT,
        type TEXT,
        confidence REAL,
        priority INTEGER,
        evidence TEXT,
        meta TEXT,
        scanned_at TEXT
    )
    """)
    conn.close()

def save_findings(results):
    conn = sqlite3.connect(DB_PATH)
    for r in results:
        conn.execute("""
        INSERT INTO findings (target, module, type, confidence, priority, evidence, meta, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["target"],
            r["module"],
            r["type"],
            r["confidence"],
            r["priority"],
            json.dumps(r["evidence"]),
            json.dumps(r["meta"]),
            r.get("scanned_at", datetime.utcnow().isoformat() + "Z")
        ))
    conn.commit()
    conn.close()

def export_results(filename, fmt="json"):
    """Esporta i risultati dal database in un file JSON o CSV."""
    import csv
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM findings")
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    conn.close()

    if fmt == "json":
        data = [dict(zip(cols, row)) for row in rows]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[storage] Esportati {len(data)} risultati in {filename} (JSON)")

    elif fmt == "csv":
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"[storage] Esportati {len(rows)} risultati in {filename} (CSV)")
