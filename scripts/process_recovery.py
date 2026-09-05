import sqlite3
from datetime import datetime, timezone

from app.database import DB_PATH
from app.recovery_actions import execute_recovery_action
from app.audit import init_audit_table, log_recovery_action


init_audit_table()

connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

payments = connection.execute("""
    SELECT *
    FROM payment_events
    WHERE recovery_status IN (
        'retry',
        'send_recovery_link',
        'stop',
        'investigate'
    )
    AND processed_at IS NULL
    ORDER BY id
""").fetchall()

connection.close()


if not payments:
    print("No unprocessed recovery decisions found.")

else:
    print(f"Processing {len(payments)} recovery decisions...\n")

    for payment in payments:

        payment = dict(payment)
        action = payment["recovery_status"]

        result = execute_recovery_action(
            payment,
            action
        )

        log_recovery_action(
            payment["payment_id"],
            action,
            result["result"]
        )

        connection = sqlite3.connect(DB_PATH)

        connection.execute("""
            UPDATE payment_events
            SET processed_at = ?
            WHERE payment_id = ?
        """, (
            datetime.now(timezone.utc).isoformat(),
            payment["payment_id"]
        ))

        connection.commit()
        connection.close()

        print(
            f"Payment: {payment['payment_id']}\n"
            f"Action: {action}\n"
            f"Result: {result['result']}\n"
        )

    print("Recovery pipeline completed.")
    print("All actions recorded in audit trail.")