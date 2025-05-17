from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

from src.core.schemas import FileInfo

from src.users.enums import ROLE


class GetUserSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: ROLE
    photo: Optional[FileInfo]


class UpdateUserSchema(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=r'^\+380\d{9}$')
    email: Optional[EmailStr]


__all__ = [
    "GetUserSchema",
    "UpdateUserSchema",
]
