from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

from models import ClaimState, DamageAssessment, ClaimDecision
from tools.damage_scoring_tool import mock_damage_scoring
from tools.policy_db_tool import load_policy, is_within_coverage
from tools.notification_tool import send_notification
from monitoring.callbacks import MonitoringCallbackHandler
from datetime import datetime
import uuid
import os

load_dotenv()  

class NoLLMAgent(Agent):
    def post_init_setup(self):
        self.llm = None
        return None


monitor = MonitoringCallbackHandler()


class ClaimIntakeAgent(NoLLMAgent):
    def __init__(self):
        super().__init__(
            role="Intake Specialist",
            goal="Validate and record the user's insurance claim details.",
            backstory="Responsible for ensuring claim data accuracy and required field validation.",
            llm=False,
            verbose=False
        )

    def run(self, raw_input: dict) -> ClaimState:
        try:
            monitor.on_agent_start("ClaimIntakeAgent", raw_input)

            missing = []
            required = ["customer_name", "policy_id", "incident_timestamp",
                        "incident_description", "vehicle_number"]

            for field in required:
                if field not in raw_input or raw_input[field] in (None, ""):
                    missing.append(field)

            state = ClaimState(
                claim_id=raw_input.get("claim_id", f"CLAIM-{uuid.uuid4().hex[:6]}"),
                customer_name=raw_input.get("customer_name", "Unknown"),
                policy_id=raw_input.get("policy_id", ""),
                incident_timestamp=raw_input.get("incident_timestamp", datetime.utcnow()),
                incident_description=raw_input.get("incident_description", ""),
                vehicle_number=raw_input.get("vehicle_number", "UNKNOWN"),
                documents_valid=len(missing) == 0,
                missing_fields=missing
            )

            monitor.on_agent_end("ClaimIntakeAgent", state.dict())
            return state

        except Exception as e:
            monitor.on_error("ClaimIntakeAgent", str(e))
            raise


class DamageAssessmentAgent(NoLLMAgent):
    def __init__(self):
        super().__init__(
            role="Damage Assessment Expert",
            goal="Analyze damage severity and estimate repair cost.",
            backstory="Uses evidence and photos to approximate vehicle repair cost.",
            llm=False,
            verbose=False

        )

    def run(self, state: ClaimState, photos_count: int) -> ClaimState:
        try:
            monitor.on_agent_start("DamageAssessmentAgent", state.dict())

            result = mock_damage_scoring(state.incident_description, photos_count)
            assessment = DamageAssessment(**result)

            policy = load_policy(state.policy_id)
            if policy:
                coverage_limit = policy.get("coverage_amount", 0)
                assessment.estimated_repair_cost = min(assessment.estimated_repair_cost, coverage_limit)



            state.damage_assessment = assessment
            monitor.on_agent_end("DamageAssessmentAgent", state.dict())
            return state

        except Exception as e:
            monitor.on_error("DamageAssessmentAgent", str(e))
            raise


class DecisionAgent(NoLLMAgent):
    def __init__(self):
        super().__init__(
            role="Claims Decision Officer",
            goal="Approve, escalate, or reject claims.",
            backstory="Balances fraud checks and policy rules to ensure fair outcomes.",
            llm=False,
            verbose=False
        )
        # Gemini LLM configuration AFTER super()
        self.llm = LLM(
            model="gemini/gemini-2.0-flash",  # model naming fixed
            api_key=os.getenv("GOOGLE_API_KEY")
        )


    def run(self, state: ClaimState) -> ClaimDecision:
        try:
            monitor.on_agent_start("DecisionAgent", state.dict())

            da = state.damage_assessment
            fa = state.fraud_assessment

            policy = load_policy(state.policy_id)
            within_coverage = is_within_coverage(policy, da.estimated_repair_cost)

            reasons = []
            if not state.documents_valid:
                reasons.append("Missing mandatory fields: " + ", ".join(state.missing_fields))
            if fa.risk_score > 0.7:
                reasons.append(f"High fraud risk score: {fa.risk_score:.2f}")
            if not within_coverage:
                reasons.append("Cost exceeds allowable coverage limit")

            if state.documents_valid and within_coverage and fa.risk_score <= 0.4:
                status = "APPROVED"
                approved_amount = da.estimated_repair_cost
            elif fa.risk_score > 0.7:
                status = "ESCALATED"
                approved_amount = 0.0
            else:
                status = "REJECTED"
                approved_amount = 0.0

            if not reasons:
                reasons.append("All checks passed successfully.")

            decision = ClaimDecision(
                claim_id=state.claim_id,
                status=status,
                approved_amount=approved_amount,
                fraud_risk_score=fa.risk_score,
                reasons=reasons,
                customer_message=f"Your claim {state.claim_id} is {status}.",
                audit_log_id=f"LOG-{uuid.uuid4().hex[:8]}",
                generated_at=datetime.utcnow(),
            )

            send_notification(state.customer_name, decision.customer_message)
            monitor.on_agent_end("DecisionAgent", decision.dict())
            return decision

        except Exception as e:
            monitor.on_error("DecisionAgent", str(e))
            raise
