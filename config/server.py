from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    url: str = Field(alias="SERVER_URL")
