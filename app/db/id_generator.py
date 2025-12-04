from app.interfaces.id_generation import IIdGenerator


class IdGenerator(IIdGenerator):
    def __init__(self):
        self.lib_num = 0
        self.doc_num = 0
        self.chunk_num = 0

    def get_new_library_id(self) -> int:
        new_id = self.lib_num
        self.lib_num += 1
        return new_id

    def get_new_document_id(self) -> int:
        new_id = self.doc_num
        self.doc_num += 1
        return new_id

    def get_new_chunk_id(self) -> int:
        new_id = self.chunk_num
        self.chunk_num += 1
        return new_id

    def set_library_id(self, value: int) -> None:
        if value >= self.lib_num:
            self.lib_num = value + 1

    def set_document_id(self, value: int) -> None:
        if value >= self.doc_num:
            self.doc_num = value + 1

    def set_chunk_id(self, value: int) -> None:
        if value >= self.chunk_num:
            self.chunk_num = value + 1
