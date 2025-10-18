import sqlite3
import json
from reconx.core.storage import init_db, save_findings
from datetime import datetime
from pathlib import Path

def test_database_creation_and_insertion(tmp_path):
    """Verifica che il database venga creato e popolato correttamente."""
    db_path = tmp_path / "test_reconx.db"
    init_db()  # usa il DB reale per semplicità

    sample = [{
        "target": "test.com",
        "module": "dummy",
        "type": "test_type",
        "confidence": 1.0,
        "priority": 5,
        "evidence": [{"label": "x", "value": "y"}],
        "meta": {"source": "test", "ttl_seconds": 100},
        "scanned_at": datetime.utcnow().isoformat() + "Z",
    }]
    save_findings(sample)

    conn = sqlite3.connect("reconx.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM findings")
    count = cur.fetchone()[0]
    conn.close()
    assert count > 0
