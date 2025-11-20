import json
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel

# Ensure folder exists before anything else
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "run_logs.jsonl"


def _json_safe(obj):
    """Recursive conversion to ensure JSON-safe logging."""
    if isinstance(obj, BaseModel):
        return _json_safe(obj.dict())

    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_json_safe(x) for x in obj]

    if isinstance(obj, datetime):
        return obj.isoformat()

    return obj


class MonitoringCallbackHandler:
    def __init__(self):
        self.log_file = LOG_FILE

    def _write_log(self, record: dict):
        safe_record = _json_safe(record)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(safe_record) + "\n")

    def _log(self, event_type: str, agent_name: str, payload: dict):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "agent_name": agent_name,
            "payload": payload,
        }
        self._write_log(entry)

    def on_agent_start(self, agent_name: str, input_data: dict):
        self._log("agent_start", agent_name, {"input": input_data})

    def on_agent_end(self, agent_name: str, output_data: dict):
        self._log("agent_end", agent_name, {"output": output_data})

    def on_error(self, agent_name: str, error: str):
        self._log("error", agent_name, {"error": str(error)})
