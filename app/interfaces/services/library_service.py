from abc import ABC, abstractmethod
from typing import List
from app.db.models import Library
from app.schemas.library import LibraryCreate, LibraryUpdate


class ILibraryReader(ABC):
    @abstractmethod
    def get_library(self, library_id: int) -> Library:
        pass

    # add page_size, page -> Tuple[List[Library], int, int]
    @abstractmethod
    def get_all_libraries(self) -> List[Library]:
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
