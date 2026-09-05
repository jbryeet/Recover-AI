import sqlite3

from app.database import DB_PATH
from app.recovery_actions import execute_recovery_action


connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

payments = connection.execute("""
    SELECT *
    FROM payment_events
    WHERE payment_id IN (
        'test_retry_001',
        'test_link_001',
        'test_stop_001'
    )
""").fetchall()

connection.close()


for payment in payments:
    payment = dict(payment)

    action = {
        "test_retry_001": "retry",
        "test_link_001": "send_recovery_link",
        "test_stop_001": "stop"
    }[payment["payment_id"]]

    result = execute_recovery_action(payment, action)

    print(
        f"Payment: {payment['payment_id']} | "
        f"Action: {result['action']} | "
        f"Result: {result['result']}"
    )