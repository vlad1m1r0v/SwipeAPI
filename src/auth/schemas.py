from datetime import datetime

from pydantic import BaseModel

from src.users.enums import UserRoleEnum
from src.auth.enums import TokenTypeEnum


class CreateTokenPayloadSchema(BaseModel):
    sub: int
    type: TokenTypeEnum
    name: str
    email: str
    role: UserRoleEnum


class TokenPayloadSchema(CreateTokenPayloadSchema):
    exp: datetime
    iat: datetime
    jti: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


__all__ = ["CreateTokenPayloadSchema", "TokenPayloadSchema", "TokensSchema"]
