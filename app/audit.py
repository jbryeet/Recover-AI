import sqlite3
from datetime import datetime, timezone

from app.database import DB_PATH


def init_audit_table():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recovery_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT,
            action TEXT,
            result TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


def log_recovery_action(payment_id, action, result):
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        INSERT INTO recovery_audit (
            payment_id,
            action,
            result,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        payment_id,
        action,
        result,
        datetime.now(timezone.utc).isoformat()
    ))

    connection.commit()
    connection.close()