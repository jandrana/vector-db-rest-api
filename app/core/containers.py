from dependency_injector import containers, providers

from app.core.config import get_settings
from app.db.containers import DbContainer
from app.services.containers import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    """Main application container that ties together modules."""

    config = providers.Configuration()
    config.from_pydantic(get_settings())

    db = providers.Container(DbContainer, config=config)
    services = providers.Container(
        ServiceContainer,
        db=db,
        config=config,
    )