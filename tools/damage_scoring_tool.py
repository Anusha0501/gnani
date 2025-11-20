# Mock scoring tool for demo – satisfies "external tool" requirement

def mock_damage_scoring(incident_description: str, photos_count: int) -> dict:
    """
    Very simple mock scoring logic.
    In real life, this could call a Vision API or ML model.
    """
    base_cost = 5000
    severity = "LOW"

    if "total loss" in incident_description.lower() or "severe" in incident_description.lower():
        severity = "HIGH"
        base_cost = 150000
    elif "dent" in incident_description.lower() or "scratch" in incident_description.lower():
        severity = "MEDIUM"
        base_cost = 25000

    # Inflate based on number of photos
    estimated_cost = base_cost + photos_count * 1000
    confidence = 0.8 if severity != "LOW" else 0.6

    return {
        "severity": severity,
        "estimated_repair_cost": estimated_cost,
        "confidence": confidence,
    }
