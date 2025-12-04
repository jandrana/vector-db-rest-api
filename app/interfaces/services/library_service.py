from abc import ABC, abstractmethod
from typing import List
from app.db.models import Library
from app.schemas.library import LibraryCreate, LibraryUpdate, LibraryDetail


class ILibraryReader(ABC):
    @abstractmethod
    def get_library(self, library_id: int) -> Library:
        pass

    @abstractmethod
    def get_all_libraries(self) -> List[Library]:
        pass

    @abstractmethod
    def get_library_with_details(self, library_id: int) -> LibraryDetail:
        pass


class ILibraryWriter(ABC):
    @abstractmethod
    def create_library(self, library: LibraryCreate) -> Library:
        pass

    @abstractmethod
    def update_library(self, library_id: int, library: LibraryUpdate) -> Library:
        pass

    @abstractmethod
    def delete_library(self, library_id: int) -> None:
        pass


class ILibraryService(ILibraryReader, ILibraryWriter):
    pass
