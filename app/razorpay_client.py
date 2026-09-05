import os

import razorpay
from dotenv import load_dotenv


load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

if not key_id or not key_secret:
    raise RuntimeError("Razorpay credentials not found.")

client = razorpay.Client(auth=(key_id, key_secret))


def create_recovery_payment_link(payment):
    amount = payment["amount"]
    payment_id = payment["payment_id"]

    data = {
        "amount": amount,
        "currency": payment["currency"],
        "accept_partial": False,
        "reference_id": f"recovery_{payment_id}",
        "description": "RecoverAI payment recovery",
        "customer": {
            "email": payment["email"],
            "contact": payment["contact"]
        },
        "reminder_enable": True
    }

    payment_link = client.payment_link.create(data)

    return payment_link