import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

columns = [
    ("recovery_outcome", "TEXT DEFAULT 'pending'"),
    ("recovered_amount", "INTEGER DEFAULT 0"),
    ("recovered_at", "TEXT")
]

for column_name, column_definition in columns:
    try:
        connection.execute(
            f"""
            ALTER TABLE payment_events
            ADD COLUMN {column_name} {column_definition}
            """
        )
        print(f"Added column: {column_name}")

    except sqlite3.OperationalError:
        print(f"Column already exists: {column_name}")

connection.commit()
connection.close()

print("Recovery outcome fields ready.")