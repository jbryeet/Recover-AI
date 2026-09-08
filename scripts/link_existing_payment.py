import sqlite3

from app.database import DB_PATH


PAYMENT_ID = "test_link_001"
LINK_ID = "plink_1XIDmIrFFKGiI"
LINK_URL = "https://rzp.io/rzp/6szCM09"


connection = sqlite3.connect(DB_PATH)

connection.execute("""
    UPDATE payment_events
    SET
        recovery_link_id = ?,
        recovery_link_url = ?
    WHERE payment_id = ?
""", (
    LINK_ID,
    LINK_URL,
    PAYMENT_ID
))

connection.commit()
connection.close()

print("Existing recovery link linked successfully.")
print("Payment:", PAYMENT_ID)
print("Link ID:", LINK_ID)
print("URL:", LINK_URL)
