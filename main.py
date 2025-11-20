from datetime import datetime
from models import ClaimState
from agents.crew_agents import ClaimIntakeAgent, DamageAssessmentAgent, DecisionAgent
from agents.adk_fraud_agent import FraudDetectionADKAgent, A2AMessage


def run_sample_claim():
    # Step 1: Intake
    raw_input = {
        "claim_id": "CLAIM-001",
        "customer_name": "Rahul Mehta",
        "policy_id": "POLICY-123",
        "incident_timestamp": datetime(2025, 11, 1, 18, 30),
        "incident_description": "Rear-end collision with moderate dent, no injuries.",
        "vehicle_number": "MH12AB1234",
    }

    intake_agent = ClaimIntakeAgent()
    state: ClaimState = intake_agent.run(raw_input)

    # Step 2: Damage Assessment
    damage_agent = DamageAssessmentAgent()
    state = damage_agent.run(state, photos_count=3)

    # Step 3: Fraud Detection (A2A, ADK)
    fraud_agent = FraudDetectionADKAgent()
    message = A2AMessage(
        sender="CrewOrchestrator",
        receiver="FraudDetectionADKAgent",
        payload={"claim_state": state.dict()},
    )
    response = fraud_agent.handle(message)
    state.fraud_assessment = response.payload["fraud_assessment"]

    # Step 4: Decision
    decision_agent = DecisionAgent()
    decision = decision_agent.run(state)

    # Structured output formats
    print("\n=== JSON Output ===")
    print(decision.json(indent=2))

    print("\n=== Markdown Summary ===")
    reasons_str = "".join(f"- {r}\n" for r in decision.reasons)
    markdown_summary = (
        "# Claim Decision Summary\n\n"
        f"- **Claim ID:** {decision.claim_id}\n"
        f"- **Status:** {decision.status}\n"
        f"- **Approved Amount:** ₹{decision.approved_amount:,.2f}\n"
        f"- **Fraud Risk Score:** {decision.fraud_risk_score:.2f}\n"
        f"- **Reasons:**\n{reasons_str}"
        f"- **Customer Message:** {decision.customer_message}\n"
    )
    print(markdown_summary)

    return decision


if __name__ == "__main__":
    run_sample_claim()
