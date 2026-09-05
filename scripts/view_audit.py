import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

records = connection.execute("""
    SELECT
        payment_id,
        action,
        result,
        timestamp
    FROM recovery_audit
    ORDER BY id
""").fetchall()

connection.close()


if not records:
    print("No audit records found.")

else:
    print(f"Audit records: {len(records)}\n")

    for record in records:
        print(
            f"Payment: {record[0]}\n"
            f"Action: {record[1]}\n"
            f"Result: {record[2]}\n"
            f"Timestamp: {record[3]}\n"
        )