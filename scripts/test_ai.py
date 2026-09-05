from app.ai_recovery import analyze_payment


payment = {
    "amount": 249900,
    "method": "card",
    "failure_reason": "payment_failed",
    "failure_description": "Payment failed temporarily",
    "retry_count": 0
}


result = analyze_payment(payment)

print("AI Diagnosis:")
print(result["diagnosis"])

print("\nRecommended Action:")
print(result["recommended_action"])

print("\nReason:")
print(result["reason"])

print("\nConfidence:")
print(result["confidence"])