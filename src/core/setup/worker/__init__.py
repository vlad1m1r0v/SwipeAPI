from celery import Celery

from src.core.setup.worker.broker import setup_broker
from src.core.setup.worker.containers import setup_containers


def setup(celery: Celery) -> None:
    setup_broker(celery)
    setup_containers(celery)
