from app.database import DB_PATH
from app.razorpay_client import create_recovery_payment_link

import sqlite3


connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

payment = connection.execute("""
    SELECT *
    FROM payment_events
    WHERE payment_id = 'test_link_001'
""").fetchone()

connection.close()

if not payment:
    raise RuntimeError("test_link_001 not found in database.")

payment = dict(payment)

print("Creating Razorpay recovery link...")
print(f"Payment: {payment['payment_id']}")
print(f"Amount: ₹{payment['amount'] / 100:.2f}")

link = create_recovery_payment_link(payment)

print("\nRecovery Payment Link created successfully.")
print("Link ID:", link["id"])
print("Short URL:", link["short_url"])
print("Status:", link["status"])
print("Reference ID:", link["reference_id"])