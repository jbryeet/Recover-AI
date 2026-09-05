import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = None

if api_key:
    client = OpenAI(api_key=api_key)


def local_analysis(payment):
    """
    Local fallback analysis used when the AI API is unavailable.

    This keeps the demo functional without requiring API credits.
    """

    failure_reason = payment.get("failure_reason", "")
    retry_count = payment.get("retry_count", 0)

    if retry_count >= 2:
        return {
            "diagnosis": "Repeated payment failure detected.",
            "recommended_action": "stop",
            "reason": "Multiple retry attempts have already failed, so another attempt is unlikely to improve recovery.",
            "confidence": 0.95
        }

    if failure_reason == "authentication_failed":
        return {
            "diagnosis": "Payment authentication failed.",
            "recommended_action": "send_recovery_link",
            "reason": "A recovery link gives the customer another opportunity to complete authentication and payment.",
            "confidence": 0.91
        }

    if failure_reason == "payment_failed":
        return {
            "diagnosis": "Temporary payment failure detected with retry capacity remaining.",
            "recommended_action": "retry",
            "reason": "The payment has not exceeded the retry threshold, so a controlled retry is appropriate.",
            "confidence": 0.88
        }

    return {
        "diagnosis": "Payment failure requires controlled recovery handling.",
        "recommended_action": "stop",
        "reason": "The failure reason is not sufficiently reliable for an automated retry.",
        "confidence": 0.75
    }


def analyze_payment(payment):
    """
    Analyze a failed payment using AI when available.
    Falls back to local recovery intelligence when the API
    is unavailable or has no credits.
    """

    if client is None:
        return local_analysis(payment)

    prompt = f"""
You are a revenue recovery analyst.

Analyze this failed payment and recommend the best recovery strategy.

Payment information:
- Amount: ₹{payment["amount"] / 100:.2f}
- Payment method: {payment["method"]}
- Failure reason: {payment["failure_reason"]}
- Failure description: {payment["failure_description"]}
- Retry count: {payment["retry_count"]}

Choose exactly one action:
- retry
- send_recovery_link
- stop

Return ONLY valid JSON:

{{
    "diagnosis": "short explanation",
    "recommended_action": "retry | send_recovery_link | stop",
    "reason": "why this action is appropriate",
    "confidence": 0.0
}}
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return json.loads(response.output_text)

    except Exception as error:
        print(f"AI service unavailable: {error}")
        print("Using local recovery analysis.")

        return local_analysis(payment)