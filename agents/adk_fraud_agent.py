from models import ClaimState, FraudAssessment
from monitoring.callbacks import MonitoringCallbackHandler

monitor = MonitoringCallbackHandler()


class A2AMessage:
    def __init__(self, sender: str, receiver: str, payload: dict, protocol_version: str = "1.0"):
        self.sender = sender
        self.receiver = receiver
        self.protocol_version = protocol_version
        self.payload = payload

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "protocol_version": self.protocol_version,
            "payload": self.payload,
        }


# Pseudo ADK agent
class FraudDetectionADKAgent:
    def handle(self, message: A2AMessage) -> A2AMessage:
        monitor.on_agent_start("FraudDetectionADKAgent", message.to_dict())

        state_data = message.payload["claim_state"]
        state = ClaimState(**state_data)

        # Simple mock risk logic
        risk = 0.2
        flags = []

        if "third-party" in state.incident_description.lower():
            risk += 0.2
            flags.append("Third-party involvement")

        if "stolen" in state.incident_description.lower():
            risk += 0.4
            flags.append("Vehicle reported stolen")

        explanation = "Rule-based mock risk scoring based on incident description keywords."

        assessment = FraudAssessment(
            risk_score=min(risk, 1.0),
            flags=flags,
            explanation=explanation,
        )

        response_payload = {
            "fraud_assessment": assessment.dict()
        }

        reply = A2AMessage(
            sender="FraudDetectionADKAgent",
            receiver=message.sender,
            payload=response_payload,
        )

        monitor.on_agent_end("FraudDetectionADKAgent", reply.to_dict())
        return reply
