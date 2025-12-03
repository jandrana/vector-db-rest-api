import json
from typing import Dict, Any, Tuple
from app.interfaces.persistence import IActionLogger


class ActionLogger(IActionLogger):
    def serialize_action(self, action: str, data: Dict[str, Any]) -> str:
        return json.dumps({"action": action, "data": data})

    def deserialize_action(self, serialized: str) -> Tuple[str, Dict[str, Any]]:
        log = json.loads(serialized)
        return log["action"], log["data"]
