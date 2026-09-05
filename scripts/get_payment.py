import os
import razorpay
from dotenv import load_dotenv

load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(key_id, key_secret))

payment_id = "pay_TUvQNTZWUlM93t"

payment = client.payment.fetch(payment_id)

print("Payment ID:", payment["id"])
print("Status:", payment["status"])
print("Amount:", payment["amount"])
print("Method:", payment["method"])
print("Order ID:", payment["order_id"])
print("Captured:", payment["captured"])
print("Error Code:", payment.get("error_code"))
print("Error Description:", payment.get("error_description"))
print("Error Source:", payment.get("error_source"))
print("Error Step:", payment.get("error_step"))
print("Error Reason:", payment.get("error_reason"))

