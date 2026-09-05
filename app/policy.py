MAX_RETRIES = 2

RETRYABLE_REASONS = {
    "payment_failed",
    "gateway_error",
    "network_error",
    "timeout",
}

CUSTOMER_ACTION_REASONS = {
    "authentication_failed",
    "incorrect_pin",
    "insufficient_funds",
}


def is_recovery_eligible(payment):
    """
    Determine whether a failed payment should enter
    the recovery workflow.
    """

    status = payment.get("status")
    retry_count = payment.get("retry_count", 0)
    failure_reason = payment.get("failure_reason")

    # Only failed payments can enter recovery.
    if status != "failed":
        return False

    # Stop after the maximum retry/recovery attempts.
    if retry_count >= MAX_RETRIES:
        return False

    # Only known recoverable failure types are eligible.
    if failure_reason in RETRYABLE_REASONS:
        return True

    if failure_reason in CUSTOMER_ACTION_REASONS:
        return True

    return False


def decide_recovery_action(payment, ai_recommendation=None):
    """
    Decide the final recovery action.

    AI may recommend an action, but deterministic policy
    and safety rules always have the final authority.
    """

    status = payment.get("status")
    retry_count = payment.get("retry_count", 0)
    failure_reason = payment.get("failure_reason")

    if status == "captured":
        return "stop"

    if retry_count >= MAX_RETRIES:
        return "stop"

    if status != "failed":
        return "investigate"

    if ai_recommendation in {
        "retry",
        "send_recovery_link",
        "stop"
    }:

        if (
            ai_recommendation == "retry"
            and failure_reason in RETRYABLE_REASONS
        ):
            return "retry"

        if (
            ai_recommendation == "send_recovery_link"
            and failure_reason in CUSTOMER_ACTION_REASONS
        ):
            return "send_recovery_link"

        if ai_recommendation == "stop":
            return "stop"

        return "investigate"

    if failure_reason in RETRYABLE_REASONS:
        return "retry"

    if failure_reason in CUSTOMER_ACTION_REASONS:
        return "send_recovery_link"

    return "stop"