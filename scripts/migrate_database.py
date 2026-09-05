import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

columns = connection.execute("""
    PRAGMA table_info(payment_events)
""").fetchall()

column_names = [column[1] for column in columns]

if "recovery_link_id" not in column_names:
    connection.execute("""
        ALTER TABLE payment_events
        ADD COLUMN recovery_link_id TEXT
    """)
    print("Added recovery_link_id")

if "recovery_link_url" not in column_names:
    connection.execute("""
        ALTER TABLE payment_events
        ADD COLUMN recovery_link_url TEXT
    """)
    print("Added recovery_link_url")

connection.commit()
connection.close()

print("Database migration completed.")