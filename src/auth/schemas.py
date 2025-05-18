import re

from pydantic import (
    BaseModel,
    field_validator,
    EmailStr,
    Field
)
from pydantic_core.core_schema import ValidationInfo

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


class UpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise ValueError("Password must contain at least one special character.")
        return value

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, value: str, info: ValidationInfo) -> str:
        new_password = info.data.get('new_password')
        if new_password and value != new_password:
            raise ValueError("Passwords do not match.")
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
    "UpdatePasswordSchema",
    "BasePayloadSchema",
    "PayloadWithTypeSchema",
    "PayloadWithExpDateSchema",
    "TokensSchema"
]
