from celery import Celery

from config import config

def setup_broker(celery: Celery) -> None:
    celery.conf.broker_url = config.broker.celery_broker_url
    celery.conf.result_backend = config.broker.celery_result_backend