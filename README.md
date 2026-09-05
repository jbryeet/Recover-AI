# RecoverAI

AI-powered payment recovery system that helps businesses recover revenue from failed payments using intelligent recovery recommendations, deterministic safety rules, Razorpay integration, and an auditable recovery pipeline.

## Overview

Failed payments can directly translate into lost revenue. RecoverAI analyzes failed payment events and determines the most appropriate recovery strategy instead of blindly retrying every transaction.

The system combines AI-assisted analysis with deterministic business rules to make recovery decisions that are explainable, controlled, and auditable.

### Core Pipeline

Failed Payment
      ↓
Eligibility Check
      ↓
AI Analysis
      ↓
Policy & Guardrails
      ↓
Final Recovery Action
      ↓
Action Execution
      ↓
Audit Trail
      ↓
Recovery Outcome

The key design principle is:

AI = Recommendation
Policy = Authority
Execution = Controlled Action
Audit = Accountability
What RecoverAI Does

For every failed payment, RecoverAI can choose between:

Retry the payment
Send a recovery payment link
Stop recovery when further action is not appropriate

The system considers factors such as:

Payment failure reason
Payment method
Transaction amount
Previous retry attempts
Recovery eligibility
AI recommendation
Deterministic policy rules
AI-Assisted Recovery

RecoverAI uses an AI analysis layer to understand the context of a failed payment.

For eligible payments, the AI produces:

Diagnosis
Recommended recovery action
Reason for the recommendation
Confidence score

Example:

Failure:
payment_failed

AI Recommendation:
RETRY

Reason:
The payment has not exceeded the retry threshold,
so a controlled retry is appropriate.

Confidence:
0.88

The AI does not directly control payment execution.

A deterministic policy layer evaluates the recommendation before the final action is executed.

This prevents an AI recommendation from bypassing important recovery constraints.

Resilient AI Fallback

The recovery pipeline is designed to remain operational even when the external AI service is unavailable.

If the AI API cannot be reached or the account has insufficient API quota, RecoverAI automatically falls back to local recovery analysis.

AI API unavailable
       ↓
Local Recovery Analysis
       ↓
Recovery Recommendation
       ↓
Policy Validation
       ↓
Final Action

This makes the recovery pipeline resilient to external AI-service failures.

Razorpay Integration

RecoverAI integrates with Razorpay in Test Mode to demonstrate payment and recovery workflows.

The system can:

Create Razorpay test orders
Retrieve payment information
Process test payment events
Generate/reuse recovery payment links
Track recovery actions
Maintain an internal audit trail

No real-money transactions are used in the demo.

Recovery Strategies
1. Retry

Used when a payment failure appears recoverable and retry capacity remains.

Payment Failed
      ↓
Eligible
      ↓
Retry
2. Recovery Link

Used when the customer needs another opportunity to complete the payment, such as an authentication-related failure.

Payment Failed
      ↓
Authentication Issue
      ↓
Recovery Link
3. Stop

Used when automated recovery should not continue.

For example, a payment that has already exceeded the allowed retry attempts can be stopped instead of repeatedly retrying it.

Payment Failed
      ↓
Recovery Not Appropriate
      ↓
STOP
Dashboard

RecoverAI includes a Flask-based dashboard for monitoring recovery activity.

The dashboard displays:

Revenue at risk
Revenue recovered
Recovery rate
Recovery-eligible revenue
Recovered transactions
AI recommendations
Final recovery decisions
Recovery outcomes
Audit history
Example Demo Scenario
Payment	Failure	AI Recommendation	Final Action	Outcome
test_retry_001	Payment failed	Retry	Retry	Recovered
test_link_001	Authentication failed	Recovery Link	Recovery Link	Recovered
test_stop_001	Payment failed	Not evaluated	Stop	Not Recovered
Auditability

Every executed recovery action is recorded in an audit trail.

The audit log captures:

Payment ID
Action
Result
Timestamp

This makes it possible to understand what RecoverAI decided, what action was executed, and when it happened.

Evaluation Mode

The project includes a synthetic evaluation workflow to demonstrate recovery performance without using real customer transactions.

The demo can simulate:

Recovered payments
Unrecovered payments
Recovery amounts
Recovery rates

Example:

Revenue at Risk       ₹16,497
Revenue Recovered      ₹6,498
Recovery Rate            39.39%
Recovered Transactions       2

These values are synthetic demonstration results and should not be interpreted as production recovery performance.

Project Structure
Recover-AI/
│
├── app/
│   ├── __init__.py
│   ├── ai_recovery.py
│   ├── audit.py
│   ├── database.py
│   ├── metrics.py
│   ├── policy.py
│   ├── razorpay_client.py
│   ├── recovery_actions.py
│   ├── server.py
│   │
│   └── templates/
│       ├── checkout.html
│       └── dashboard.html
│
├── scripts/
│   ├── create_order.py
│   ├── create_test_events.py
│   ├── get_payment.py
│   ├── process_recovery.py
│   ├── recovery_metrics.py
│   ├── run_recovery.py
│   ├── save_test_payment.py
│   ├── simulate_recovery_outcomes.py
│   ├── test_ai.py
│   ├── test_audit.py
│   ├── test_policy.py
│   └── test_recovery_actions.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
Tech Stack
Python
Flask
SQLite
Razorpay Python SDK
OpenAI API
python-dotenv
HTML/CSS
REST APIs
Getting Started
1. Clone the Repository
git clone https://github.com/jbryeet/Recover-AI.git
cd Recover-AI
2. Create a Virtual Environment
Windows
python -m venv .venv
.venv\Scripts\activate
macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the project root:

RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
OPENAI_API_KEY=your_openai_api_key

Never commit your .env file or API keys to GitHub.

5. Initialize the Database
python scripts/migrate_database.py
6. Create/Reset Demo Events
python scripts/reset_test_events.py
7. Run Recovery Analysis
python scripts/run_recovery.py
8. Execute Recovery Actions
python scripts/process_recovery.py
9. Simulate Evaluation Outcomes
python scripts/simulate_recovery_outcomes.py
10. Start the Dashboard
python -m app.server

Open:

http://127.0.0.1:5000/
Running the Complete Demo

The complete demonstration follows this sequence:

1. Create failed payment events
           ↓
2. Check recovery eligibility
           ↓
3. Analyze eligible payments
           ↓
4. Generate AI recommendations
           ↓
5. Apply deterministic policy
           ↓
6. Execute recovery actions
           ↓
7. Record audit events
           ↓
8. Simulate recovery outcomes
           ↓
9. Display metrics on dashboard
Example Recovery Flow

Consider a failed payment:

Amount: ₹2,499
Failure: payment_failed
Retry Count: 0

RecoverAI determines that the payment is eligible for recovery.

The AI recommends:

RETRY

The policy layer validates the recommendation.

Final decision:

RETRY

The recovery action is executed and recorded in the audit trail.

Why This Architecture?

A payment recovery system should not allow an AI model to directly control financial actions.

RecoverAI therefore separates:

Analysis
   ↓
Recommendation
   ↓
Policy
   ↓
Execution
   ↓
Audit

This separation provides:

Better control over automated actions
Explainable decisions
Clear auditability
Safer recovery workflows
Resilience when external AI services fail
Limitations

This project is a buildathon prototype rather than a production payment recovery platform.

Current limitations include:

Razorpay is used in Test Mode
Recovery outcomes are synthetically simulated
Local fallback logic is rule-based
No production customer notification system
No production-grade background job queue
No large-scale historical recovery dataset
No live production payment deployment
Future Improvements

Potential extensions include:

Learning recovery policies from historical payment outcomes
Customer-level recovery personalization
Better prediction of payment recovery probability
Background job processing
Automated customer notifications
Monitoring and alerting
Production-grade authentication and authorization
A/B testing of recovery strategies
More payment gateways
Real-time recovery analytics
Project Status

RecoverAI is a functional prototype demonstrating an end-to-end payment recovery workflow with:

Razorpay integration
AI-assisted analysis
Local AI fallback
Deterministic recovery policies
Recovery action execution
Audit logging
Synthetic outcome evaluation
Monitoring dashboard

Built as a Razorpay Buildathon project.

Key Takeaway

RecoverAI is not simply a system that retries failed payments.

It is a controlled recovery pipeline that combines AI-assisted reasoning with deterministic safeguards, controlled execution, and complete auditability.

Failed Payment
      ↓
Understand the failure
      ↓
Recommend a recovery strategy
      ↓
Validate the recommendation
      ↓
Execute safely
      ↓
Measure the outcome
      ↓
Learn from the result

After pasting and saving it, run:

```powershell
git add README.md
git commit -m "Polish README"
git push

Then refresh your GitHub repo.
