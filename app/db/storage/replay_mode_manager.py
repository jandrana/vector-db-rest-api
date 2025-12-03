from typing import List, Any
from app.interfaces.persistence import IReplayModeManager


class RepositoryReplayModeManager(IReplayModeManager):
    def __init__(self, repositories: List[Any]):
        self.repositories = repositories

    def set_replay_mode(self, enabled: bool) -> None:
        for repository in self.repositories:
            if hasattr(repository, "_replay_mode"):
                repository._replay_mode = enabled
