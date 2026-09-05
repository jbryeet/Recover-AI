import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

columns = connection.execute("""
    PRAGMA table_info(payment_events)
""").fetchall()

column_names = [column[1] for column in columns]


if "ai_recommendation" not in column_names:
    connection.execute("""
        ALTER TABLE payment_events
        ADD COLUMN ai_recommendation TEXT
    """)
    print("Added ai_recommendation")


if "ai_diagnosis" not in column_names:
    connection.execute("""
        ALTER TABLE payment_events
        ADD COLUMN ai_diagnosis TEXT
    """)
    print("Added ai_diagnosis")


if "ai_confidence" not in column_names:
    connection.execute("""
        ALTER TABLE payment_events
        ADD COLUMN ai_confidence REAL
    """)
    print("Added ai_confidence")


connection.commit()
connection.close()

print("AI database migration completed.")