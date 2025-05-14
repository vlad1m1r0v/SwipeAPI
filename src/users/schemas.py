from decimal import Decimal

from fastapi import Form
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

from src.users.enums import UserRoleEnum


class CreateUserSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field(pattern=r'^\+380\d{9}$')
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

    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            email: EmailStr = Form(...),
            phone: str = Form(...),
            password: str = Form(...),
    ):
        return cls(name=name, email=email, phone=phone, password=password)


class UserPayloadSchema(BaseModel):
    id: int
    name: str
    email: str
    role: UserRoleEnum


class CreateContactSchema(BaseModel):
    user_id: int
    email: str
    phone: str


class CreateAgentContactSchema(BaseModel):
    user_id: int


class CreateBalanceSchema(BaseModel):
    user_id: int
    value: Decimal | None


class CreateSubscriptionSchema(BaseModel):
    user_id: int


class CreateNotificationSettingsSchema(BaseModel):
    user_id: int


__all__ = [
    "CreateUserSchema",
    "UserPayloadSchema",
    "CreateContactSchema",
    "CreateAgentContactSchema",
    "CreateBalanceSchema",
    "CreateSubscriptionSchema",
    "CreateNotificationSettingsSchema",
]
