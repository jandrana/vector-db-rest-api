import threading
from typing import Optional
from app.core.config import Settings, get_settings
from app.interfaces.repositories.library_repository import ILibraryRepository
from app.interfaces.repositories.document_repository import IDocumentRepository
from app.interfaces.repositories.chunk_repository import IChunkRepository
from app.interfaces.repositories.search_repository import ISearchRepository
from app.interfaces.repositories.replayable_repository import IReplayableRepository
from app.interfaces.persistence import (
    IStorage,
    IActionLogger,
    IPersistenceManager,
    IActionHandlerProvider,
    IReplayModeManager,
)
from app.interfaces.indexing import IInvertedIndex, ITokenizationStrategy
from app.interfaces.services.embedding_service import (
    IEmbeddingProvider,
    IEmbeddingService,
)
from app.interfaces.id_generation import IIdGenerator
from app.interfaces.services.library_service import ILibraryService
from app.interfaces.services.document_service import IDocumentService
from app.interfaces.services.chunk_service import IChunkService
from app.interfaces.services.index_service import IIndexService
from app.interfaces.services.search_service import ISearchService


class DIContainer:
    def __init__(self, settings: Optional[Settings] = None):
        self._settings = settings
        self._storage = None
        self._action_logger = None
        self._persistence_manager = None
        self._tokenization_strategy = None
        self._inverted_index = None
        self._id_generator = None
        self._library_repository = None
        self._document_repository = None
        self._chunk_repository = None
        self._search_repository = None
        self._embedding_provider = None
        self._embedding_service = None
        self._library_service = None
        self._document_service = None
        self._chunk_service = None
        self._index_service = None
        self._search_service = None
        self._action_handler_registry = None
        self._replay_mode_manager = None

        self._initialize_and_replay()

    def _initialize_and_replay(self) -> None:
        """Initialize all repositories and replay persisted actions."""
        _ = self.chunk_repository

        self.persistence.replay_actions(
            handler_provider=self.action_handler_registry,
            replay_mode_manager=self.replay_mode_manager,
        )

    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = get_settings()
        return self._settings

    @property
    def storage(self) -> IStorage:
        if self._storage is None:
            from app.db.storage.storage import Storage

            self._storage = Storage(file_path=self.settings.DB_FILE)
        return self._storage

    @property
    def action_logger(self) -> IActionLogger:
        if self._action_logger is None:
            from app.db.storage.action_logger import ActionLogger

            self._action_logger = ActionLogger()
        return self._action_logger

    @property
    def action_handler_registry(self) -> IActionHandlerProvider:
        if self._action_handler_registry is None:
            from app.db.storage.action_handler_registry import ActionHandlerRegistry

            registry = ActionHandlerRegistry()

            repositories = [
                self.library_repository,
                self.document_repository,
                self.chunk_repository,
            ]

            for repository in repositories:
                if isinstance(repository, IReplayableRepository):
                    handlers = repository.get_replay_handlers()
                    registry.register_handlers(handlers)

            self._action_handler_registry = registry
        return self._action_handler_registry

    @property
    def replay_mode_manager(self) -> IReplayModeManager:
        if self._replay_mode_manager is None:
            from app.db.storage.replay_mode_manager import RepositoryReplayModeManager

            self._replay_mode_manager = RepositoryReplayModeManager(
                [
                    self.library_repository,
                    self.document_repository,
                    self.chunk_repository,
                ]
            )
        return self._replay_mode_manager

    @property
    def persistence(self) -> IPersistenceManager:
        if self._persistence_manager is None:
            from app.db.storage.persistence_manager import PersistenceManager

            self._persistence_manager = PersistenceManager(
                storage=self.storage, logger=self.action_logger
            )
        return self._persistence_manager

    @property
    def tokenization_strategy(self) -> ITokenizationStrategy:
        if self._tokenization_strategy is None:
            from app.db.tokenization import DefaultTokenizationStrategy

            self._tokenization_strategy = DefaultTokenizationStrategy()
        return self._tokenization_strategy

    @property
    def inverted_index(self) -> IInvertedIndex:
        if self._inverted_index is None:
            from app.db.inverted_index import InvertedIndex

            self._inverted_index = InvertedIndex(
                tokenization_strategy=self.tokenization_strategy
            )
        return self._inverted_index

    @property
    def id_generator(self) -> IIdGenerator:
        if self._id_generator is None:
            from app.db.id_generator import IdGenerator

            self._id_generator = IdGenerator()
        return self._id_generator

    @property
    def library_repository(self) -> ILibraryRepository:
        if self._library_repository is None:
            from app.db.repositories.library_repository import LibraryRepository

            self._library_repository = LibraryRepository(
                storage={},
                id_generator=self.id_generator,
                persistence_manager=self.persistence,
                lock=threading.RLock(),
            )
        return self._library_repository

    @property
    def document_repository(self) -> IDocumentRepository:
        if self._document_repository is None:
            from app.db.repositories.document_repository import DocumentRepository

            self._document_repository = DocumentRepository(
                storage={},
                id_generator=self.id_generator,
                persistence_manager=self.persistence,
                lock=threading.RLock(),
            )
        return self._document_repository

    @property
    def chunk_repository(self) -> IChunkRepository:
        if self._chunk_repository is None:
            from app.db.repositories.chunk_repository import ChunkRepository

            self._chunk_repository = ChunkRepository(
                storage={},
                id_generator=self.id_generator,
                persistence_manager=self.persistence,
                inverted_index=self.inverted_index,
                document_repository=self.document_repository,
                lock=threading.RLock(),
            )

        return self._chunk_repository

    @property
    def search_repository(self) -> ISearchRepository:
        if self._search_repository is None:
            from app.db.repositories.search_repository import SearchRepository

            self._search_repository = SearchRepository(
                chunk_repository=self.chunk_repository,
                inverted_index=self.inverted_index,
                lock=threading.RLock(),
            )
        return self._search_repository

    @property
    def embedding_provider(self) -> IEmbeddingProvider:
        if self._embedding_provider is None:
            from app.services.embedding.embedding_provider import (
                CohereEmbeddingProvider,
            )

            self._embedding_provider = CohereEmbeddingProvider(
                api_key=self.settings.COHERE_API_KEY,
                model=self.settings.EMBEDDING_MODEL,
            )
        return self._embedding_provider

    @property
    def embedding_service(self) -> IEmbeddingService:
        if self._embedding_service is None:
            from app.services.embedding.embedding_service import EmbeddingService

            self._embedding_service = EmbeddingService(
                embedding_provider=self.embedding_provider,
                model=self.settings.EMBEDDING_MODEL,
            )
        return self._embedding_service

    @property
    def library_service(self) -> ILibraryService:
        if self._library_service is None:
            from app.services.library_service import LibraryService

            self._library_service = LibraryService(
                library_repository=self.library_repository,
                document_repository=self.document_repository,
            )
        return self._library_service

    @property
    def document_service(self) -> IDocumentService:
        if self._document_service is None:
            from app.services.document_service import DocumentService

            self._document_service = DocumentService(
                document_repository=self.document_repository,
                library_repository=self.library_repository,
                chunk_repository=self.chunk_repository,
            )
        return self._document_service

    @property
    def chunk_service(self) -> IChunkService:
        if self._chunk_service is None:
            from app.services.chunk_service import ChunkService

            self._chunk_service = ChunkService(
                chunk_repository=self.chunk_repository,
                document_repository=self.document_repository,
                library_repository=self.library_repository,
            )
        return self._chunk_service

    @property
    def index_service(self) -> IIndexService:
        if self._index_service is None:
            from app.services.index_service import IndexService

            self._index_service = IndexService(
                chunk_repository=self.chunk_repository,
                embedding_service=self.embedding_service,
                library_repository=self.library_repository,
            )
        return self._index_service

    @property
    def search_service(self) -> ISearchService:
        if self._search_service is None:
            from app.services.search.search_service import SearchService
            from app.services.search.strategies.knn_strategy import KnnSearchStrategy
            from app.services.search.strategies.keyword_strategy import (
                KeywordSearchStrategy,
            )

            search_service = SearchService()

            search_service.register_strategy(
                "knn",
                KnnSearchStrategy(
                    chunk_repository=self.chunk_repository,
                    embedding_service=self.embedding_service,
                ),
            )
            search_service.register_strategy(
                "keyword",
                KeywordSearchStrategy(search_repository=self.search_repository),
            )
            self._search_service = search_service
        return self._search_service
