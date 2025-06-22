from datetime import timedelta

from pydantic import BaseModel, Field, Json


class CeleryConfig(BaseModel):
    broker_url: str = Field(alias="CELERY_BROKER_URL")
    result_backend: str = Field(alias="CELERY_RESULT_BACKEND")
    beat_schedule: Json = {
        "daily_withdrawal": {
            "task": "daily_withdrawal",
            "schedule": timedelta(days=1),
        }
    }
