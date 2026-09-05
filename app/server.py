import os
import sqlite3

import razorpay
from flask import Flask, render_template
from dotenv import load_dotenv

from app.metrics import calculate_recovery_metrics
from app.database import DB_PATH


load_dotenv()

app = Flask(__name__)

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(key_id, key_secret))


@app.route("/")
def dashboard():
    metrics = calculate_recovery_metrics()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    payments = connection.execute("""
        SELECT
            payment_id,
            amount,
            currency,
            status,
            method,
            failure_reason,
            retry_count,
            recovery_eligible,
            recovery_status,
            ai_recommendation,
            ai_diagnosis,
            ai_confidence,
            recovery_outcome,
            recovered_amount,
            recovery_link_url
        FROM payment_events
        WHERE status = 'failed'
        ORDER BY id
    """).fetchall()

    audit_records = connection.execute("""
        SELECT
            payment_id,
            action,
            result,
            timestamp
        FROM recovery_audit
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    # Determine actual AI state from stored analysis results.
    ai_recommendations = [
        payment["ai_recommendation"]
        for payment in payments
        if payment["ai_recommendation"]
    ]

    if ai_recommendations:
        ai_status = "AI active"
        ai_status_class = "active"
    else:
        ai_status = "Fallback policy active"
        ai_status_class = "fallback"

    return render_template(
        "dashboard.html",
        metrics=metrics,
        payments=payments,
        audit_records=audit_records,
        ai_status=ai_status,
        ai_status_class=ai_status_class
    )


@app.route("/checkout")
def checkout():
    order_data = {
        "amount": 249900,
        "currency": "INR",
        "receipt": "recoverai_checkout_001"
    }

    order = client.order.create(data=order_data)

    return render_template(
        "checkout.html",
        key_id=key_id,
        amount=order["amount"],
        order_id=order["id"]
    )


if __name__ == "__main__":
    app.run(debug=True)