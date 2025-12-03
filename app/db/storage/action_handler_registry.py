from typing import Dict, Any, Callable
from app.interfaces.persistence import IActionHandlerProvider


class ActionHandlerRegistry(IActionHandlerProvider):
    def __init__(self):
        self._handlers: Dict[str, Callable[[str, Dict[str, Any]], None]] = {}

    def register_handlers(
        self, handlers: Dict[str, Callable[[str, Dict[str, Any]], None]]
    ) -> None:
        self._handlers.update(handlers)

    def get_action_handlers(self) -> Dict[str, Callable[[str, Dict[str, Any]], None]]:
        return self._handlers.copy()
