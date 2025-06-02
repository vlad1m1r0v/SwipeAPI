from os import environ as env
from dotenv import load_dotenv

from pydantic import BaseModel, Field

from config.db import DBConfig
from config.jwt import JWTConfig
from config.redis import RedisConfig
from config.email import EmailConfig
from config.signing import SignConfig

from src.core.constants import BASE_DIR

load_dotenv(dotenv_path=BASE_DIR / ".env")


class Config(BaseModel):
    jwt: JWTConfig = Field(default_factory=lambda: JWTConfig(**env))
    db: DBConfig = Field(default_factory=lambda: DBConfig(**env))
    redis: RedisConfig = Field(default_factory=lambda: RedisConfig(**env))
    email: EmailConfig = Field(default_factory=lambda: EmailConfig(**env))
    sign: SignConfig = Field(default_factory=lambda: SignConfig(**env))


config = Config()

__all__ = ["Config", "config"]
