import sqlite3
from datetime import datetime, timezone

from app.database import DB_PATH


outcomes = {
    "test_retry_001": ("recovered", 249900),
    "test_link_001": ("recovered", 399900),
    "test_stop_001": ("not_recovered", 0)
}


connection = sqlite3.connect(DB_PATH)

for payment_id, (outcome, amount) in outcomes.items():

    recovered_at = (
        datetime.now(timezone.utc).isoformat()
        if outcome == "recovered"
        else None
    )

    connection.execute("""
        UPDATE payment_events
        SET
            recovery_outcome = ?,
            recovered_amount = ?,
            recovered_at = ?
        WHERE payment_id = ?
    """, (
        outcome,
        amount,
        recovered_at,
        payment_id
    ))

connection.commit()
connection.close()

print("Synthetic recovery outcomes recorded.")

for payment_id, (outcome, amount) in outcomes.items():
    print(
        f"{payment_id}: "
        f"{outcome}, "
        f"₹{amount / 100:.2f}"
    )