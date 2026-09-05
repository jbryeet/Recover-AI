import sqlite3

from app.database import DB_PATH


def calculate_recovery_metrics():
    connection = sqlite3.connect(DB_PATH)

    payments = connection.execute("""
        SELECT
            amount,
            recovery_eligible,
            recovery_outcome,
            recovered_amount
        FROM payment_events
        WHERE status = 'failed'
    """).fetchall()

    connection.close()

    # Total revenue from failed payments.
    total_failed_revenue = sum(
        payment[0] for payment in payments
    )

    # Revenue explicitly marked as recovery-eligible.
    eligible_revenue = sum(
        payment[0]
        for payment in payments
        if payment[1] == 1
    )

    # Revenue recovered during the evaluation.
    recovered_revenue = sum(
        payment[3] or 0
        for payment in payments
    )

    recovered_transactions = sum(
        1
        for payment in payments
        if payment[2] == "recovered"
    )

    total_failed_transactions = len(payments)

    if total_failed_revenue:
        revenue_recovery_rate = (
            recovered_revenue / total_failed_revenue
        ) * 100
    else:
        revenue_recovery_rate = 0

    if total_failed_transactions:
        transaction_recovery_rate = (
            recovered_transactions
            / total_failed_transactions
        ) * 100
    else:
        transaction_recovery_rate = 0

    return {
        "failed_transactions": total_failed_transactions,
        "revenue_at_risk": total_failed_revenue,
        "eligible_revenue": eligible_revenue,
        "recovered_revenue": recovered_revenue,
        "recovered_transactions": recovered_transactions,
        "revenue_recovery_rate": revenue_recovery_rate,
        "transaction_recovery_rate": transaction_recovery_rate
    }