from decimal import Decimal
from typing import Optional

from advanced_alchemy.types import FileObject

from fastapi import UploadFile

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

from src.users.constants import DEFAULT_BALANCE
from src.users.enums import UserRoleEnum


class CreateContactSchema(BaseModel):
    user_id: int
    email: str
    phone: str


class CreateAgentContactSchema(BaseModel):
    user_id: int


class CreateBalanceSchema(BaseModel):
    user_id: int
    value: Decimal = DEFAULT_BALANCE


class CreateSubscriptionSchema(BaseModel):
    user_id: int


class CreateNotificationSettingsSchema(BaseModel):
    user_id: int

class GetUserSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: UserRoleEnum
    photo:  Optional[FileObject]


class UpdateUserSchema(
    BaseModel
):
    name: Optional[str] = Field(min_length=3, max_length=100)
    email: Optional[EmailStr]
    phone: Optional[str] = Field(pattern=r'^\+380\d{9}$')
    photo: Optional[FileObject] = Field(default=None, exclude=True)



__all__ = [
    "CreateContactSchema",
    "CreateAgentContactSchema",
    "CreateBalanceSchema",
    "CreateSubscriptionSchema",
    "CreateNotificationSettingsSchema",
    "GetUserSchema",
    "UpdateUserSchema",
]
