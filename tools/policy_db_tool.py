import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "policies.json"

def load_policy(policy_id: str) -> dict:
    with open(DATA_PATH, "r") as f:
        policies = json.load(f)

    # Convert list → dict for fast lookup
    if isinstance(policies, list):
        policies = {p["policy_id"]: p for p in policies}

    return policies.get(policy_id, {})


def is_within_coverage(policy: dict, estimated_cost: float) -> bool:
    if not policy:
        return False

    limit = policy.get("coverage_amount", 0)
    return estimated_cost <= limit
