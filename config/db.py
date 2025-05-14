from pydantic import BaseModel, Field


class DBConfig(BaseModel):
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    name: str = Field(alias='DB_NAME')

    def url(self, is_async: bool = True) -> str:
        return f"postgresql+{'asyncpg' if is_async else 'psycopg2'}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
