from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    EmailStr
)

from src.core.schemas import FileInfo
from src.core.utils.validation import PHONE_NUMBER

from src.users.enums import (
    ROLE,
    NOTIFICATION_TYPE
)


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


class GetBalanceSchema(BaseModel):
    id: int
    value: float

class GetSubscriptionSchema(BaseModel):
    id: int
    is_auto_renewal: bool
    expiry_date: datetime

class UpdateNotificationSettingsSchema(BaseModel):
    redirect_notifications_to_agent: Optional[bool] = Field(default=None)
    notification_type: Optional[NOTIFICATION_TYPE] = Field(default=None)


class GetNotificationSettingsSchema(UpdateNotificationSettingsSchema):
    id: int

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
    balance: GetBalanceSchema
    subscription: GetSubscriptionSchema
    notification_settings: GetNotificationSettingsSchema


__all__ = [
    "UpdateContactSchema",
    "UpdateAgentContactSchema",
    "UpdateNotificationSettingsSchema",
    "UpdateUserSchema",
    "GetUserSchema"
]
