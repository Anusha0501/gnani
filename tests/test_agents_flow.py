from agents.crew_agents import ClaimIntakeAgent, DamageAssessmentAgent, DecisionAgent
from agents.adk_fraud_agent import FraudDetectionADKAgent
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Initialize agents
intake_agent = ClaimIntakeAgent()
damage_agent = DamageAssessmentAgent()
fraud_agent = FraudDetectionADKAgent()
decision_agent = DecisionAgent()

# 1: Submit claim payload
raw_input = {
    "customer_name": "Rajesh Kumar",
    "policy_id": "POL1001",
    "incident_description": "Rear bumper damage due to collision",
    "vehicle_number": "KA05MU1234",
    "incident_timestamp": datetime.utcnow(),
}

# Step 1: Intake
state = intake_agent.run(raw_input)
pp.pprint(state.dict())

# Step 2: Damage assessment
state = damage_agent.run(state, photos_count=6)
pp.pprint(state.dict())

# Add estimated repair cost from damage score
policy = load_policy(state.policy_id)
state.damage_assessment.estimated_repair_cost = (
    state.damage_assessment.damage_score * policy["coverage_amount"]
)

# Step 3: Fraud assessment
state.fraud_assessment = fraud_agent.assess_fraud(
    state.policy_id, state.incident_description, photos_count=6
)

# Step 4: Decision
decision = decision_agent.run(state)
pp.pprint(decision.dict())
