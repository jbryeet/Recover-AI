import os
import requests
from dotenv import load_dotenv

load_dotenv()

key_id = os.getenv("RAZORPAY_KEY_ID")
key_secret = os.getenv("RAZORPAY_KEY_SECRET")

if not key_id or not key_secret:
    raise RuntimeError("Razorpay credentials not found.")

url = "https://api.razorpay.com/v1/payments"

response = requests.get(
    url,
    auth=(key_id, key_secret),
    params={"count": 1}
)

print("Status:", response.status_code)
print("Response:", response.json())