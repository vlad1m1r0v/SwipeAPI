from celery import Celery

from src.core.setup.worker import setup

celery = Celery(__name__)

setup(celery)