import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

events = connection.execute("""
    SELECT
        payment_id,
        amount,
        status,
        method,
        failure_reason,
        retry_count,
        recovery_status
    FROM payment_events
""").fetchall()

connection.close()


for event in events:
    print(event)