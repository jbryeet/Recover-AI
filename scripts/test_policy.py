from app.policy import decide_recovery_action


test_cases = [
    {
        "name": "AI agrees with retry",
        "payment": {
            "status": "failed",
            "retry_count": 0,
            "failure_reason": "payment_failed"
        },
        "ai": "retry"
    },
    {
        "name": "AI agrees with recovery link",
        "payment": {
            "status": "failed",
            "retry_count": 0,
            "failure_reason": "authentication_failed"
        },
        "ai": "send_recovery_link"
    },
    {
        "name": "AI tries retry after retry limit",
        "payment": {
            "status": "failed",
            "retry_count": 2,
            "failure_reason": "payment_failed"
        },
        "ai": "retry"
    },
    {
        "name": "AI recommendation conflicts with failure reason",
        "payment": {
            "status": "failed",
            "retry_count": 0,
            "failure_reason": "authentication_failed"
        },
        "ai": "retry"
    },
    {
        "name": "Payment already captured",
        "payment": {
            "status": "captured",
            "retry_count": 0,
            "failure_reason": None
        },
        "ai": "retry"
    },
    {
        "name": "Unknown payment state",
        "payment": {
            "status": "created",
            "retry_count": 0,
            "failure_reason": None
        },
        "ai": "retry"
    }
]


for case in test_cases:
    decision = decide_recovery_action(
        case["payment"],
        case["ai"]
    )

    print(
        f"{case['name']}\n"
        f"AI recommendation: {case['ai']}\n"
        f"Final decision: {decision}\n"
    )