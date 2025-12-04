import json
import os
from typing import Dict, Any, Generator, Tuple
from app.interfaces.persistence import IStorage


class Storage(IStorage):
    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        self._check_file_exists()

    def _check_file_exists(self) -> None:
        """Create the file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write("")

    def save_action(self, action: str, data: Dict[str, Any]) -> None:
        log = {"action": action, "data": data}
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")
            f.flush()

    def load_actions(self) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        with open(self.file_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                log = json.loads(line)
                yield log["action"], log["data"]
