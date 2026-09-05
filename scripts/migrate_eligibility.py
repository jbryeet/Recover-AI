import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

connection.execute("""
    ALTER TABLE payment_events
    ADD COLUMN recovery_eligible INTEGER DEFAULT 0
""")

connection.commit()
connection.close()

print("Added recovery_eligible field successfully.")