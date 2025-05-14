from os import environ as env
from dotenv import load_dotenv

from pathlib import Path

from pydantic import BaseModel, Field

from config.db import DBConfig
from config.jwt import JWTConfig

BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=BASE_DIR / '.env')


class Config(BaseModel):
    jwt: JWTConfig = Field(default_factory=lambda: JWTConfig(**env))
    db: DBConfig = Field(default_factory=lambda: DBConfig(**env))


config = Config()

__all__ = ['Config', 'config']
