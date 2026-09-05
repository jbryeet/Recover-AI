import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "payment_events.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS payment_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            order_id TEXT,
            amount INTEGER,
            currency TEXT,
            status TEXT,
            method TEXT,
            email TEXT,
            contact TEXT,
            failure_code TEXT,
            failure_description TEXT,
            failure_source TEXT,
            failure_step TEXT,
            failure_reason TEXT,
            retry_count INTEGER DEFAULT 0,
            recovery_status TEXT DEFAULT 'pending',
            recovery_link_id TEXT,
            recovery_link_url TEXT,
            created_at INTEGER,
            processed_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_payment_event(payment):
    connection = get_connection()

    connection.execute("""
        INSERT OR IGNORE INTO payment_events (
            payment_id,
            order_id,
            amount,
            currency,
            status,
            method,
            email,
            contact,
            failure_code,
            failure_description,
            failure_source,
            failure_step,
            failure_reason,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payment.get("id"),
        payment.get("order_id"),
        payment.get("amount"),
        payment.get("currency"),
        payment.get("status"),
        payment.get("method"),
        payment.get("email"),
        payment.get("contact"),
        payment.get("error_code"),
        payment.get("error_description"),
        payment.get("error_source"),
        payment.get("error_step"),
        payment.get("error_reason"),
        payment.get("created_at")
    ))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized: {DB_PATH}")