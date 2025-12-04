from abc import ABC, abstractmethod
from typing import Dict, Any, Callable


class IReplayableRepository(ABC):
    @abstractmethod
    def get_replay_handlers(self) -> Dict[str, Callable[[str, Dict[str, Any]], None]]:
        pass
