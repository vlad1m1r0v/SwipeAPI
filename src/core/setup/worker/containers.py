from celery import Celery

from dishka.integrations.celery import setup_dishka
import dishka as di

from config import Config, config

from src.users.ioc import UsersProvider

from src.core.ioc import (
    ConfigProvider,
    SessionProvider,
    FastMailProvider,
    JinjaProvider,
)


def setup_containers(celery: Celery) -> None:
    container = di.make_container(
        ConfigProvider(),
        SessionProvider(),
        FastMailProvider(),
        JinjaProvider(),
        UsersProvider(),
        context={Config: config},
    )

    setup_dishka(container, celery)
