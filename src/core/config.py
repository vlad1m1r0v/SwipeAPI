from os import environ as env
from pathlib import Path
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent.parent


class JWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class DBConfig(BaseModel):
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    name: str = Field(alias='DB_NAME')

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Config(BaseModel):
    jwt: JWTConfig = Field(default_factory=lambda: JWTConfig(**env))
    db: DBConfig = Field(default_factory=lambda: DBConfig(**env))
