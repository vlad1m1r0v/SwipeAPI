from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka
import dishka as di

from config import Config, config

from src.core.ioc import ConfigProvider, SessionProvider, InMemoryDBProvider
from src.auth.ioc import AuthProvider
from src.user.ioc import UsersProvider
from src.admin.ioc import AdminProvider
from src.builder.ioc import BuilderProvider
from src.buildings.ioc import BuildingsProvider
from src.apartments.ioc import ApartmentsProvider
from src.announcements.ioc import AnnouncementsProvider
from src.notaries.ioc import NotaryProvider
from src.requests.ioc import RequestsProvider


def setup_containers(app: FastAPI) -> None:
    container = di.make_async_container(
        ConfigProvider(),
        SessionProvider(),
        InMemoryDBProvider(),
        AuthProvider(),
        UsersProvider(),
        AdminProvider(),
        BuilderProvider(),
        BuildingsProvider(),
        ApartmentsProvider(),
        AnnouncementsProvider(),
        NotaryProvider(),
        RequestsProvider(),
        context={Config: config},
    )

    setup_dishka(container, app)


__all__ = ["setup_containers"]
