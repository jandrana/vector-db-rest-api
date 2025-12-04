import threading
from dependency_injector import containers, providers

from app.db.id_generator import IdGenerator
from app.db.inverted_index import InvertedIndex
from app.db.repositories.chunk_repository import ChunkRepository
from app.db.repositories.document_repository import DocumentRepository
from app.db.repositories.library_repository import LibraryRepository
from app.db.repositories.search_repository import SearchRepository
from app.db.storage.action_handler_registry import ActionHandlerRegistry
from app.db.storage.action_logger import ActionLogger
from app.db.storage.persistence_manager import PersistenceManager
from app.db.storage.replay_mode_manager import RepositoryReplayModeManager
from app.db.storage.storage import Storage
from app.db.tokenization import DefaultTokenizationStrategy


class DbContainer(containers.DeclarativeContainer):
    """Container for database, persistence, and repository components."""

    config = providers.Configuration()
    lock = providers.Factory(threading.RLock)


    storage = providers.Singleton(Storage, file_path=config.DB_FILE)
    action_logger = providers.Singleton(ActionLogger)
    persistence_manager = providers.Singleton(
        PersistenceManager, storage=storage, logger=action_logger
    )


    id_generator = providers.Singleton(IdGenerator)
    tokenization_strategy = providers.Singleton(DefaultTokenizationStrategy)
    inverted_index = providers.Singleton(
        InvertedIndex, tokenization_strategy=tokenization_strategy
    )


    document_repository = providers.Singleton(
        DocumentRepository,
        storage=providers.Factory(dict),
        id_generator=id_generator,
        persistence_manager=persistence_manager,
        lock=lock,
    )

    library_repository = providers.Singleton(
        LibraryRepository,
        storage=providers.Factory(dict),
        id_generator=id_generator,
        persistence_manager=persistence_manager,
        lock=lock,
    )

    chunk_repository = providers.Singleton(
        ChunkRepository,
        storage=providers.Factory(dict),
        id_generator=id_generator,
        persistence_manager=persistence_manager,
        document_repository=document_repository,
        lock=lock,
    )

    search_repository = providers.Singleton(
        SearchRepository,
        chunk_repository=chunk_repository,
        inverted_index=inverted_index,
        lock=lock,
    )


    replayable_repositories = providers.List(
        library_repository, document_repository, chunk_repository
    )

    action_handler_registry = providers.Singleton(ActionHandlerRegistry)

    replay_mode_manager = providers.Singleton(
        RepositoryReplayModeManager, repositories=replayable_repositories
    )
