import os

import razorpay
from dotenv import load_dotenv


load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(key_id, key_secret))

payment_link = client.payment_link.fetch("plink_1XIDmIrFFKGiI")

print("Payment Link found successfully.")
print("ID:", payment_link["id"])
print("Status:", payment_link["status"])
print("Amount:", payment_link["amount"])
print("Reference ID:", payment_link["reference_id"])
print("Short URL:", payment_link["short_url"])