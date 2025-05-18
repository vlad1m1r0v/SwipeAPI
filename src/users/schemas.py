from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

from src.core.schemas import FileInfo
from src.core.utils.validation import PHONE_NUMBER

from src.users.enums import ROLE


class UpdateContactSchema(BaseModel):
    first_name: Optional[str] = Field(min_length=3, max_length=100, default=None)
    last_name: Optional[str] = Field(min_length=3, max_length=100, default=None)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER, default=None)
    email: Optional[EmailStr] = Field(default=None)


class GetContactSchema(UpdateContactSchema):
    id: int


class UpdateAgentContactSchema(UpdateContactSchema):
    pass


class GetAgentContactSchema(GetContactSchema):
    pass


class UpdateUserSchema(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER)
    email: Optional[EmailStr]


class GetUserSchema(UpdateUserSchema):
    id: int
    role: ROLE
    photo: Optional[FileInfo]
    contact: GetContactSchema
    agent_contact: GetAgentContactSchema


__all__ = [
    "UpdateContactSchema",
    "UpdateAgentContactSchema",
    "UpdateUserSchema",
    "GetUserSchema"
]
