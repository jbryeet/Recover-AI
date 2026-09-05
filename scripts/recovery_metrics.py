from app.metrics import calculate_recovery_metrics


metrics = calculate_recovery_metrics()


print("===== RecoverAI Recovery Metrics =====\n")

print(
    f"Failed transactions: "
    f"{metrics['failed_transactions']}"
)

print(
    f"Revenue at risk: "
    f"₹{metrics['revenue_at_risk'] / 100:.2f}"
)

print(
    f"Recovery-eligible revenue: "
    f"₹{metrics['eligible_revenue'] / 100:.2f}"
)

print(
    f"Revenue recovered: "
    f"₹{metrics['recovered_revenue'] / 100:.2f}"
)

print(
    f"Recovered transactions: "
    f"{metrics['recovered_transactions']}"
)

print(
    f"Revenue recovery rate: "
    f"{metrics['revenue_recovery_rate']:.2f}%"
)

print(
    f"Transaction recovery rate: "
    f"{metrics['transaction_recovery_rate']:.2f}%"
)