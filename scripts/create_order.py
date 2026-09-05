import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

if not key_id or not key_secret:
    raise RuntimeError("Razorpay credentials not found.")

client = razorpay.Client(auth=(key_id, key_secret))

order_data = {
    "amount": 249900,  # ₹2,499 in paise
    "currency": "INR",
    "receipt": "recoverai_test_001",
}

order = client.order.create(data=order_data)

print("Order created successfully")
print("Order ID:", order["id"])
print("Amount:", order["amount"])
print("Currency:", order["currency"])
print("Status:", order["status"])