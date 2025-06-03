from celery import Celery

from config import config


def setup_broker(celery: Celery) -> None:
    celery.conf.broker_url = config.celery.broker_url
    celery.conf.result_backend = config.celery.result_backend
    celery.conf.beat_schedule = config.celery.beat_schedule
