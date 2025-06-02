from celery import Celery

from dishka.integrations.celery import setup_dishka
import dishka as di

from config import Config, config

from src.core.ioc import (
    ConfigProvider,
    FastMailProvider,
    JinjaProvider,
)


def setup_containers(celery: Celery) -> None:
    container = di.make_container(
        ConfigProvider(),
        FastMailProvider(),
        JinjaProvider(),
        context={Config: config},
    )

    setup_dishka(container, celery)
