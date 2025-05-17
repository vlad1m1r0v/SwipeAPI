from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka
import dishka as di

from config import (
    Config,
    config
)

from src.core.ioc import (
    ConfigProvider,
    SessionProvider
)
from src.auth.ioc import AuthProvider
from src.users.ioc import UsersProvider


def setup_containers(app: FastAPI) -> None:
    container = di.make_async_container(
        ConfigProvider(),
        SessionProvider(),
        AuthProvider(),
        UsersProvider(),
        context={Config: config},
    )

    setup_dishka(container, app)

__all__ = ["setup_containers"]
