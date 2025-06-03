from pydantic import BaseModel, Field


class InMemoryDBConfig(BaseModel):
    url: str = Field(alias="REDIS_STORAGE_URL")
