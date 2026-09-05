import sqlite3

from app.database import DB_PATH, init_db


init_db()

connection = sqlite3.connect(DB_PATH)

test_events = [
    (
        "test_retry_001",
        "order_test_001",
        249900,
        "INR",
        "failed",
        "card",
        "customer1@example.com",
        "9999999991",
        "PAYMENT_FAILED",
        "Payment failed temporarily",
        "gateway",
        "payment",
        "payment_failed",
        0
    ),
    (
        "test_link_001",
        "order_test_002",
        399900,
        "INR",
        "failed",
        "card",
        "customer2@example.com",
        "9999999992",
        "AUTHENTICATION_FAILED",
        "Customer authentication failed",
        "customer",
        "authentication",
        "authentication_failed",
        0
    ),
    (
        "test_stop_001",
        "order_test_003",
        999900,
        "INR",
        "failed",
        "card",
        "customer3@example.com",
        "9999999993",
        "PAYMENT_FAILED",
        "Maximum retry limit reached",
        "gateway",
        "payment",
        "payment_failed",
        2
    )
]


for event in test_events:
    connection.execute("""
        INSERT OR IGNORE INTO payment_events (
            payment_id,
            order_id,
            amount,
            currency,
            status,
            method,
            email,
            contact,
            failure_code,
            failure_description,
            failure_source,
            failure_step,
            failure_reason,
            retry_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, event)


connection.commit()
connection.close()

print("Synthetic recovery events created successfully.")