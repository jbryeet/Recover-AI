import sqlite3

from app.database import DB_PATH
from app.policy import decide_recovery_action, is_recovery_eligible
from app.ai_recovery import analyze_payment


connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row

payments = connection.execute("""
    SELECT *
    FROM payment_events
    WHERE recovery_status = 'pending'
    ORDER BY id
""").fetchall()


if not payments:
    print("No pending recovery events found.")

else:
    print(f"Processing {len(payments)} recovery events...\n")

    for payment in payments:

        payment = dict(payment)

        # Step 1: Determine recovery eligibility
        eligible = is_recovery_eligible(payment)

        connection.execute("""
            UPDATE payment_events
            SET recovery_eligible = ?
            WHERE payment_id = ?
        """, (
            1 if eligible else 0,
            payment["payment_id"]
        ))

        # Ineligible payments are stopped immediately.
        if not eligible:

            final_decision = "stop"

            connection.execute("""
                UPDATE payment_events
                SET recovery_status = ?
                WHERE payment_id = ?
            """, (
                final_decision,
                payment["payment_id"]
            ))

            print(
                f"Payment: {payment['payment_id']}\n"
                f"Recovery Eligible: NO\n"
                f"Final Decision: STOP\n"
            )

            continue

        # Step 2: Ask AI to analyze eligible payments
        ai_result = analyze_payment(payment)

        ai_recommendation = ai_result.get(
            "recommended_action"
        )

        # Step 3: Save AI analysis
        connection.execute("""
            UPDATE payment_events
            SET
                ai_recommendation = ?,
                ai_diagnosis = ?,
                ai_confidence = ?
            WHERE payment_id = ?
        """, (
            ai_recommendation,
            ai_result.get("diagnosis"),
            ai_result.get("confidence"),
            payment["payment_id"]
        ))

        # Step 4: Deterministic policy makes final decision
        final_decision = decide_recovery_action(
            payment,
            ai_recommendation
        )

        # Step 5: Save final decision
        connection.execute("""
            UPDATE payment_events
            SET recovery_status = ?
            WHERE payment_id = ?
        """, (
            final_decision,
            payment["payment_id"]
        ))

        print(
            f"Payment: {payment['payment_id']}\n"
            f"Recovery Eligible: YES\n"
            f"AI Recommendation: {ai_recommendation}\n"
            f"AI Confidence: {ai_result.get('confidence')}\n"
            f"Final Decision: {final_decision}\n"
        )

    connection.commit()
    connection.close()

    print("AI-assisted recovery decisions saved successfully.")