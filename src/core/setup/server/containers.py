from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka
import dishka as di

from config import Config, config

from src.core.ioc import ConfigProvider, SessionProvider, InMemoryDBProvider
from src.auth.ioc import AuthProvider
from src.users.ioc import UsersProvider
from src.admins.ioc import AdminsProvider


def setup_containers(app: FastAPI) -> None:
    container = di.make_async_container(
        ConfigProvider(),
        SessionProvider(),
        InMemoryDBProvider(),
        AuthProvider(),
        UsersProvider(),
        AdminsProvider(),
        context={Config: config},
    )

    setup_dishka(container, app)


__all__ = ["setup_containers"]
