from abc import ABC, abstractmethod
from typing import Dict, Any, Generator, Tuple, Callable


class IStorage(ABC):
    @abstractmethod
    def save_action(self, action: str, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def load_actions(self) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        pass


class IActionLogger(ABC):
    @abstractmethod
    def serialize_action(self, action: str, data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def deserialize_action(self, serialized: str) -> Tuple[str, Dict[str, Any]]:
        pass


class IActionHandlerProvider(ABC):
    @abstractmethod
    def get_action_handlers(self) -> Dict[str, Callable[[str, Dict[str, Any]], None]]:
        pass


class IReplayModeManager(ABC):
    @abstractmethod
    def set_replay_mode(self, enabled: bool) -> None:
        pass


class IPersistenceManager(ABC):
    @abstractmethod
    def save_action(self, action: str, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def load_actions(self) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        pass

    @abstractmethod
    def replay_actions(
        self,
        handler_provider: "IActionHandlerProvider",
        replay_mode_manager: "IReplayModeManager",
    ) -> None:
        pass
