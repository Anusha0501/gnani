User Submits Claim in Streamlit
        │
        ▼
[ClaimIntakeAgent]
- Checks mandatory fields
- Creates initial ClaimState
        │
        ▼
[DamageAssessmentAgent]
- Uses mock_damage_scoring()
- Adds severity & repair cost
        │
        ▼
A2A Message → [FraudDetectionADKAgent]
- Rule-based fraud scoring
- Returns FraudAssessment
        │
        ▼
[DecisionAgent]
- Validate coverage
- Check fraud risk
- Approve / Reject / Escalate
        │
        ▼
UI Shows:
- Status
- Approved Amount
- Fraud Score & Flags
- Human-readable explanation
