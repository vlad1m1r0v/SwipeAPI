from pydantic import BaseModel, Field


class RedisConfig(BaseModel):
    celery_broker_url: str = Field(alias='CELERY_BROKER_URL')
    celery_result_backend: str = Field(alias='CELERY_RESULT_BACKEND')
    redis_storage_url: str = Field(alias='REDIS_STORAGE_URL')