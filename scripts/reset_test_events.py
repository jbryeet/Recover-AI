import sqlite3

from app.database import DB_PATH


connection = sqlite3.connect(DB_PATH)

connection.execute("""
    UPDATE payment_events
    SET
        recovery_status = 'pending',
        recovery_eligible = 0,
        processed_at = NULL,

        ai_recommendation = NULL,
        ai_diagnosis = NULL,
        ai_confidence = NULL,

        recovery_outcome = NULL,
        recovered_amount = NULL,
        recovered_at = NULL

    WHERE payment_id IN (
        'test_retry_001',
        'test_link_001',
        'test_stop_001'
    )
""")

connection.commit()
connection.close()

print("Synthetic test events reset successfully.")
print("Eligibility, AI analysis, decisions, and outcomes cleared.")