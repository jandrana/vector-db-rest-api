import json
import os
from typing import Dict, Any

DB_FILE = "vector_db.jsonl"


class Persistence:
    def __init__(self):
        self.db_file = DB_FILE

    def save_action(self, action: str, data: Dict[str, Any]):
        log = {"action": action, "data": data}
        with open(self.db_file, "a") as f:
            f.write(json.dumps(log) + "\n")

    def load_actions(self):
        if not os.path.exists(DB_FILE):
            return
        with open(DB_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    log = json.loads(line)
                    yield log["action"], log["data"]
                except Exception as e:
                    print(f"Skipping invalid log: {e}")
