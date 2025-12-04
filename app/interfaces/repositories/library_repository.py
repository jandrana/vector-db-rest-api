from abc import ABC, abstractmethod
from typing import List, Optional
from app.db.models import Library


class ILibraryRepository(ABC):
    @abstractmethod
    def get(self, library_id: int) -> Optional[Library]:
        pass

    @abstractmethod
    def get_all(self) -> List[Library]:
        pass

    @abstractmethod
    def create(self, name: str, disk_id: Optional[int] = None) -> Library:
        pass

    @abstractmethod
    def update(self, library_id: int, name: Optional[str]) -> Optional[Library]:
        pass

    @abstractmethod
    def delete(self, library_id: int) -> bool:
        pass
