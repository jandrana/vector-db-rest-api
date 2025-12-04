from dependency_injector import containers, providers


class ServiceContainer(containers.DeclarativeContainer):
    """Container for business services and application logic."""

    config = providers.Configuration()

    db = providers.DependenciesContainer()


    embedding_provider = providers.Singleton(
        "app.services.embedding.embedding_provider.CohereEmbeddingProvider",
        api_key=config.COHERE_API_KEY.as_(str),
        model=config.EMBEDDING_MODEL.as_(str),
    )

    embedding_service = providers.Singleton(
        "app.services.embedding.embedding_service.EmbeddingService",
        embedding_provider=embedding_provider,
        model=config.EMBEDDING_MODEL.as_(str),
    )


    library_service = providers.Singleton(
        "app.services.library_service.LibraryService",
        library_repository=db.library_repository,
        document_repository=db.document_repository,
    )

    document_service = providers.Singleton(
        "app.services.document_service.DocumentService",
        document_repository=db.document_repository,
        library_repository=db.library_repository,
        chunk_repository=db.chunk_repository,
    )

    chunk_service = providers.Singleton(
        "app.services.chunk_service.ChunkService",
        chunk_repository=db.chunk_repository,
        document_repository=db.document_repository,
        library_repository=db.library_repository,
        inverted_index=db.inverted_index,
    )

    index_service = providers.Singleton(
        "app.services.index_service.IndexService",
        chunk_repository=db.chunk_repository,
        embedding_service=embedding_service,
        library_repository=db.library_repository,
    )



    knn_strategy = providers.Factory(
        "app.services.search.strategies.knn_strategy.KnnSearchStrategy",
        chunk_repository=db.chunk_repository,
        embedding_service=embedding_service,
    )

    keyword_strategy = providers.Factory(
        "app.services.search.strategies.keyword_strategy.KeywordSearchStrategy",
        search_repository=db.search_repository,
    )

    def _create_search_service(
        knn_strategy_instance,
        keyword_strategy_instance,
    ):
        """Creates SearchService and registers strategies."""
        from app.services.search.search_service import SearchService

        service = SearchService()
        service.register_strategy("knn", knn_strategy_instance)
        service.register_strategy("keyword", keyword_strategy_instance)
        return service

    search_service = providers.Singleton(
        _create_search_service,
        knn_strategy_instance=knn_strategy,
        keyword_strategy_instance=keyword_strategy,
    )
