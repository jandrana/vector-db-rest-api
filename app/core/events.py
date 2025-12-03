from typing import Callable
from fastapi import FastAPI
from app.core.container import DIContainer
from app.core.config import Settings


def create_startup_handler(
    application: FastAPI, settings: Settings
) -> Callable[[], None]:
    async def startup_handler() -> None:
        try:
            application.state.container = DIContainer(settings)
        except Exception as e:
            application.state.startup_error = e

    return startup_handler
