import sqlite3

from app.audit import init_audit_table, log_recovery_action
from app.database import DB_PATH


init_audit_table()

log_recovery_action(
    "test_retry_001",
    "retry",
    "Retry scheduled"
)


connection = sqlite3.connect(DB_PATH)

audit = connection.execute("""
    SELECT
        payment_id,
        action,
        result,
        timestamp
    FROM recovery_audit
    ORDER BY id DESC
    LIMIT 1
""").fetchone()

connection.close()


print("Audit record:")
print(audit)