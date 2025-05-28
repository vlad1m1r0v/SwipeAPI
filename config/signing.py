from pydantic import BaseModel, Field


class SignConfig(BaseModel):
    sign_secret: str = Field(alias='SIGN_SECRET')
    sign_salt: str = Field(alias='SIGN_SALT')
    expire_seconds: int = 60