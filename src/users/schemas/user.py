from src.core.schemas import BaseModel

from pydantic import EmailStr, Field, field_validator
import re


class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(pattern=r'^\+380\d{9}$')
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r'[A-Z]', value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r'\d', value):
            raise ValueError(
                "Password must contain at least one number."
            )
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."
            )
        return value
