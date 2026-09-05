import os
import razorpay

from dotenv import load_dotenv

from app.database import init_db, save_payment_event


load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(key_id, key_secret))


init_db()

payments = client.payment.all({
    "count": 1
})

if payments["count"] == 0:
    print("No payments found.")
else:
    payment = payments["items"][0]

    save_payment_event(payment)

    print("Payment saved successfully.")
    print("Payment ID:", payment["id"])
    print("Status:", payment["status"])