import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# ⬇️ Load environment variables from .env into OS env
load_dotenv()
import os
os.environ["CREWAI_NATIVE_PROVIDER"] = "disabled"
os.environ["CREWAI_DISABLE_LLM_FALLBACK"] = "true"
os.environ["CREWAI_DISABLE_OPENAI"] = "true"

from agents.crew_agents import ClaimIntakeAgent, DamageAssessmentAgent, DecisionAgent
from agents.adk_fraud_agent import FraudDetectionADKAgent, A2AMessage
from models import ClaimState
from models import FraudAssessment


st.set_page_config(page_title="ClaimSwift AI", layout="centered")

st.title("🚗 ClaimSwift – AI Motor Insurance Claim System")
st.markdown("Automated decision-making using **CrewAI + ADK agentic workflow**")

st.divider()
st.subheader("📝 Enter Claim Details")

customer_name = st.text_input("Customer Name", "")
policy_id = st.text_input("Policy ID", "")
vehicle_number = st.text_input("Vehicle Number", "")
incident_description = st.text_area("Incident Description", "")
photos_count = st.slider("Number of Damage Photos Submitted", 1, 10, 3)

if st.button("Submit Claim"):
    if not customer_name or not policy_id or not incident_description:
        st.error("⚠ Please fill all the required fields!")
        st.stop()

    with st.spinner("Processing your claim..."):

        intake_agent = ClaimIntakeAgent()
        raw_input = {
            "claim_id": f"CLAIM-{datetime.now().strftime('%H%M%S')}",
            "customer_name": customer_name,
            "policy_id": policy_id,
            "incident_timestamp": datetime.now(),
            "incident_description": incident_description,
            "vehicle_number": vehicle_number,
        }

        state: ClaimState = intake_agent.run(raw_input)

        damage_agent = DamageAssessmentAgent()
        state = damage_agent.run(state, photos_count)

        fraud_agent = FraudDetectionADKAgent()
        message = A2AMessage(
            sender="StreamlitUI",
            receiver="FraudDetectionADKAgent",
            payload={"claim_state": state.dict()},
        )
        response = fraud_agent.handle(message)
        state.fraud_assessment = FraudAssessment(**response.payload["fraud_assessment"])


        decision_agent = DecisionAgent()
        decision = decision_agent.run(state)

    st.success(f"🎉 Claim Status: {decision.status}")

    st.markdown("### 📘 Structured Claim Decision")
    st.json(decision.dict())

    reasons_md = ""
    for r in decision.reasons:
        reasons_md += f"- {r}\n"

    st.markdown("### 🧾 Summary Report")
    st.markdown(f"""
    - **Claim ID:** {decision.claim_id}
    - **Status:** `{decision.status}`
    - **Approved Amount:** ₹{decision.approved_amount:,.2f}
    - **Fraud Risk Score:** {decision.fraud_risk_score:.2f}
    - **Reasons:**  
    {reasons_md}
    - **Message to Customer:** {decision.customer_message}
    - **Generated At:** {decision.generated_at}
    """)


    st.info("📌 Your claim has been processed using autonomous AI decision workflow!")
