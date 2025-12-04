from app.interfaces.persistence import (
    IStorage,
    IActionLogger,
    IPersistenceManager,
    IActionHandlerProvider,
    IReplayModeManager,
)
from typing import Dict, Any, Generator, Tuple


class PersistenceManager(IPersistenceManager):
    def __init__(self, storage: IStorage, logger: IActionLogger):
        self.storage = storage
        self.logger = logger

    def save_action(self, action: str, data: Dict[str, Any]) -> None:
        self.logger.serialize_action(action, data)
        self.storage.save_action(action, data)

    def load_actions(self) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        for action, data in self.storage.load_actions():
            yield action, data

    def replay_actions(
        self,
        handler_provider: IActionHandlerProvider,
        replay_mode_manager: IReplayModeManager,
    ) -> None:
        replay_mode_manager.set_replay_mode(True)
        try:
            action_handlers = handler_provider.get_action_handlers()
            for action, data in self.load_actions():
                handler = action_handlers.get(action)
                if handler:
                    handler(action, data)
        finally:
            replay_mode_manager.set_replay_mode(False)
