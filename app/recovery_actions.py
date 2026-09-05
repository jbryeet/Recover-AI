from datetime import datetime
import sqlite3

from app.database import DB_PATH
from app.razorpay_client import create_recovery_payment_link


def execute_recovery_action(payment, action):
    """
    Execute a bounded recovery action.

    Only send_recovery_link interacts with Razorpay.
    Duplicate recovery links are prevented.
    """

    payment_id = payment["payment_id"]

    # Retry action
    if action == "retry":
        result = "Retry scheduled"

    # Recovery link action
    elif action == "send_recovery_link":

        # Prevent duplicate recovery links
        if payment.get("recovery_link_id"):
            result = (
                f"Existing recovery link reused: "
                f"{payment['recovery_link_url']}"
            )

            return {
                "payment_id": payment_id,
                "action": action,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }

        # Create a new Razorpay Payment Link
        payment_link = create_recovery_payment_link(payment)

        # Save the link in our database
        connection = sqlite3.connect(DB_PATH)

        connection.execute("""
            UPDATE payment_events
            SET
                recovery_link_id = ?,
                recovery_link_url = ?
            WHERE payment_id = ?
        """, (
            payment_link["id"],
            payment_link["short_url"],
            payment_id
        ))

        connection.commit()
        connection.close()

        result = (
            f"Recovery payment link created: "
            f"{payment_link['short_url']}"
        )

    # Stop action
    elif action == "stop":
        result = "Recovery stopped"

    # Manual investigation
    elif action == "investigate":
        result = "Manual investigation required"

    # Unknown actions are blocked
    else:
        result = "Unknown action blocked"

    return {
        "payment_id": payment_id,
        "action": action,
        "result": result,
        "timestamp": datetime.utcnow().isoformat()
    }