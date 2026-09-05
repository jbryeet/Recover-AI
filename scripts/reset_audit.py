import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

connection.execute("DELETE FROM recovery_audit")

connection.commit()
connection.close()

print("Audit trail reset successfully.")