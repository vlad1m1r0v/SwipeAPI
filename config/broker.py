from pydantic import BaseModel, Field


class BrokerConfig(BaseModel):
    celery_broker_url: str = Field(alias='CELERY_BROKER_URL')
    celery_result_backend: str = Field(alias='CELERY_RESULT_BACKEND')