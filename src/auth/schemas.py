import re

from pydantic import (
    BaseModel,
    field_validator,
    EmailStr,
    Field
)

from src.users.enums import ROLE
from src.auth.enums import TOKEN_TYPE


class RegisterSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    phone: str = Field(pattern=r'^\+380\d{9}$')
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise ValueError("Password must contain at least one special character.")
        return value


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise ValueError("Password must contain at least one special character.")
        return value


class BasePayloadSchema(BaseModel):
    id: int
    name: str
    email: str
    role: ROLE


class PayloadWithTypeSchema(BaseModel):
    sub: str
    type: TOKEN_TYPE
    name: str
    email: str
    role: ROLE


class PayloadWithExpDateSchema(PayloadWithTypeSchema):
    exp: int
    iat: int
    jti: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


__all__ = [
    "RegisterSchema",
    "LoginSchema",
    "BasePayloadSchema",
    "PayloadWithTypeSchema",
    "PayloadWithExpDateSchema",
    "TokensSchema"
]
