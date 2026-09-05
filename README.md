# RecoverAI

**AI-powered payment recovery system for recovering revenue from failed payments using AI-assisted analysis, deterministic policies, Razorpay integration, and an auditable recovery pipeline.**

---

## Overview

Failed payments can directly translate into lost revenue.

RecoverAI analyzes failed payment events and determines the most appropriate recovery strategy instead of blindly retrying every transaction.

The system combines **AI-assisted analysis** with **deterministic business rules** to make recovery decisions that are explainable, controlled, and auditable.

### Core Pipeline

```text
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
Design Principle

AI = Recommendation
Policy = Authority
Execution = Controlled Action
Audit = Accountability

Problem

Failed payments create direct revenue leakage for businesses.

A simple retry strategy is not always effective because different payment failures require different recovery actions.

For example:

Some payments can be safely retried.
Some require the customer to complete authentication again.
Some should not be retried after repeated failures.

RecoverAI addresses this by analyzing each failed payment and selecting a controlled recovery strategy.

Solution

RecoverAI creates an automated recovery pipeline that:

Detects failed payments.
Checks whether the payment is eligible for recovery.
Analyzes the failure context using AI.
Generates a recommended recovery action.
Applies deterministic policy and safety rules.
Executes the approved recovery action.
Records the action in an audit trail.
Measures the resulting recovery outcome.
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
Example
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

The fallback is intentionally rule-based so that the core recovery workflow can continue without depending completely on an external AI service.

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
Razorpay Integration

RecoverAI integrates with Razorpay in Test Mode to demonstrate payment and recovery workflows.

The system can:

Create Razorpay test orders
Retrieve payment information
Process test payment events
Generate or reuse recovery payment links
Track recovery actions
Maintain an internal audit trail

Note: No real-money transactions are used in this project. Recovery outcomes shown in the dashboard are synthetic evaluation results.

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
Example Dashboard Metrics
Metric	Value
Revenue at Risk	₹16,497
Revenue Recovered	₹6,498
Recovery Rate	39.39%
Recovered Transactions	2
Recovery-Eligible Revenue	₹6,498
Transaction Recovery Rate	66.67%
Example Recovery Decisions
Payment ID	Amount	Failure Reason	AI Recommendation	Final Decision	Outcome
test_retry_001	₹2,499	payment_failed	RETRY	RETRY	RECOVERED
test_link_001	₹3,999	authentication_failed	SEND_RECOVERY_LINK	RECOVERY LINK	RECOVERED
test_stop_001	₹9,999	payment_failed	Not evaluated	STOP	NOT RECOVERED

The third payment is marked as not evaluated because it is not eligible for automated recovery, so the AI analysis stage is skipped.

Auditability

Every executed recovery action is recorded in an audit trail.

The audit log captures:

Payment ID
Action
Result
Timestamp

Example:

test_retry_001
      ↓
RETRY
      ↓
Retry scheduled
      ↓
Timestamp recorded

This makes it possible to understand:

Which payment was processed
What action was selected
What action was executed
What result occurred
When the action happened
Evaluation Mode

The project includes a synthetic evaluation workflow to demonstrate recovery performance without using real customer transactions.

The demo can simulate:

Recovered payments
Unrecovered payments
Recovery amounts
Recovery rates
Current Demo Results
Metric	Value
Revenue at Risk	₹16,497
Revenue Recovered	₹6,498
Recovery Rate	39.39%
Recovered Transactions	2
Recovery-Eligible Revenue	₹6,498
Transaction Recovery Rate	66.67%

These values are synthetic demonstration results and should not be interpreted as production recovery performance.

Architecture
                        ┌──────────────────────┐
                        │   Failed Payments    │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Eligibility Check    │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │    AI Analysis       │
                        │                      │
                        │ Diagnosis            │
                        │ Recommendation       │
                        │ Confidence           │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Policy & Guardrails  │
                        └──────────┬───────────┘
                                   │
                         ┌─────────┼─────────┐
                         │         │         │
                         ▼         ▼         ▼
                      RETRY   RECOVERY LINK  STOP
                         │         │         │
                         └─────────┼─────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Action Execution     │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │    Audit Trail       │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Recovery Outcome     │
                        └──────────────────────┘
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

The AI recommends.

The policy decides.

The execution layer performs the action.

The audit layer records what happened.

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
Technology	Purpose
Python	Core application logic
Flask	Web dashboard and server
SQLite	Payment events, decisions and audit data
Razorpay SDK	Payment and recovery-link integration
OpenAI API	AI-assisted payment analysis
python-dotenv	Environment configuration
HTML/CSS	Dashboard interface
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

Create a .env file in the project root.

RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret
OPENAI_API_KEY=your_openai_api_key

Never commit your .env file or API keys to GitHub.

5. Initialize the Database
python scripts/migrate_database.py
6. Create or Reset Demo Events
python scripts/reset_test_events.py
7. Run Recovery Analysis
python scripts/run_recovery.py
8. Execute Recovery Actions
python scripts/process_recovery.py
9. Simulate Evaluation Outcomes
python scripts/simulate_recovery_outcomes.py
10. Start the Dashboard
python -m app.server

Open the dashboard at:

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

The recovery action is then executed and recorded in the audit trail.

Failure Handling

RecoverAI is designed to handle failures in both the payment workflow and the AI service.

AI Service Failure

If the AI service is unavailable:

AI API Failure
      ↓
Local Fallback Analysis
      ↓
Policy Validation
      ↓
Recovery Action
Repeated Payment Failure

If a payment has already reached the retry limit:

Repeated Failure
      ↓
Eligibility / Policy Check
      ↓
STOP

This prevents uncontrolled repeated recovery attempts.

Security

Sensitive configuration is stored using environment variables.

The repository does not include:

Razorpay secret keys
OpenAI API keys
.env files
Local SQLite databases
Virtual environment files

These files are excluded through .gitignore.

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
Recovery probability prediction
Background job processing
Automated customer notifications
Monitoring and alerting
Production-grade authentication and authorization
A/B testing of recovery strategies
Support for additional payment gateways
Real-time recovery analytics
Continuous learning from recovery outcomes
Buildathon Context

RecoverAI was built as a payment recovery prototype for the Razorpay Buildathon.

The project focuses on using AI to improve payment recovery while maintaining deterministic controls over financial actions.

The main objective is to demonstrate how AI-assisted reasoning can be integrated into a payment workflow without allowing the AI model to directly execute uncontrolled financial operations.

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
Key Takeaway

RecoverAI is not simply a system that retries failed payments.

It is a controlled recovery pipeline that combines AI-assisted reasoning, deterministic safeguards, controlled execution, and complete auditability.

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
License

This project is currently intended as a buildathon and educational prototype.


Then save `README.md` and run:

```powershell
git add README.md
git commit -m "Update README"
git push
