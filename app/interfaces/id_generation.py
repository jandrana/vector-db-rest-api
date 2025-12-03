from abc import ABC, abstractmethod


class IIdGenerator(ABC):
    @abstractmethod
    def get_new_library_id(self) -> int:
        pass

    @abstractmethod
    def get_new_document_id(self) -> int:
        pass

    @abstractmethod
    def get_new_chunk_id(self) -> int:
        pass

    @abstractmethod
    def set_library_id(self, value: int) -> None:
        pass

    @abstractmethod
    def set_document_id(self, value: int) -> None:
        pass

    @abstractmethod
    def set_chunk_id(self, value: int) -> None:
        pass
