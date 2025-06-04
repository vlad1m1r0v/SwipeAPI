# from datetime import timedelta

from celery.schedules import crontab

from pydantic import BaseModel, Field, Json


class CeleryConfig(BaseModel):
    broker_url: str = Field(alias="CELERY_BROKER_URL")
    result_backend: str = Field(alias="CELERY_RESULT_BACKEND")
    beat_schedule: Json = {
        "monthly_withdrawal": {
            "task": "monthly_withdrawal",
            # TODO: change to normal value
            # "schedule": timedelta(days=30),
            "schedule": crontab(minute="*/1"),
        }
    }
