from fastapi import FastAPI, Query
import json, uuid

app = FastAPI(title="ClaimSwift Demo")

# Load mock data
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

claims = load_json("data/claims.json")
policies = load_json("data/policies.json")
agents = load_json("data/agents.json")

# Helper functions
def get_policy(policy_number):
    return next((p for p in policies if p["policy_number"] == policy_number), None)

def get_agent_for_claim(amount):
    # return first agent who can approve
    return next((a for a in agents if a["approval_limit"] >= amount), None)

# Endpoint to process claim
@app.get("/process_claim")
def process_claim(claim_id: str):
    claim = next((c for c in claims if c["id"] == claim_id), None)
    if not claim:
        return {"error": "Claim not found"}

    policy = get_policy(claim["policy_number"])
    if not policy:
        return {"ref": str(uuid.uuid4()), "status": "Rejected", "reason": "Policy not found"}

    # Check coverage
    if claim["claim_amount"] > policy["coverage_amount"]:
        return {"ref": str(uuid.uuid4()), "status": "Rejected", "reason": "Claim amount exceeds coverage"}

    # Check documents (basic)
    required_docs = ["FIR", "Photos", "Repair Estimate"]
    if not all(doc in claim["documents_submitted"] for doc in required_docs):
        return {"ref": str(uuid.uuid4()), "status": "Review Required", "reason": "Missing documents"}

    # Assign agent
    agent = get_agent_for_claim(claim["claim_amount"])
    if not agent:
        return {"ref": str(uuid.uuid4()), "status": "Review Required", "reason": "No agent can approve this claim"}

    # Auto-approve
    claim["status"] = "Approved"
    return {
        "ref": str(uuid.uuid4()),
        "status": "Approved",
        "agent": agent["name"],
        "policy_number": claim["policy_number"],
        "claim_amount": claim["claim_amount"]
    }
