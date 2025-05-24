from pydantic import BaseModel

from src.auth.enums import TokenType

from src.users.enums import Role


class BasePayloadSchema(BaseModel):
    id: int
    name: str
    email: str
    role: Role


class PayloadWithTypeSchema(BaseModel):
    sub: str
    type: TokenType
    name: str
    email: str
    role: Role


class PayloadWithExpDateSchema(PayloadWithTypeSchema):
    exp: int
    iat: int
    jti: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str