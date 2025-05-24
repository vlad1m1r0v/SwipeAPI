from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from .contact import GetContactSchema
from .agent_contact import GetAgentContactSchema
from .notification_settings import GetNotificationSettingsSchema
from .subscription import GetSubscriptionSchema
from .balance import GetBalanceSchema

from src.users.enums import Role

from src.core.constants import PHONE_NUMBER
from src.core.schemas import FileInfo


class UpdateUserAccountSchema(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER)
    email: Optional[EmailStr]
    photo: Optional[FileInfo]


class GetUserAccountSchema(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    role: Role
    photo: Optional[FileInfo]


class GetUserSchema(GetUserAccountSchema):
    contact: GetContactSchema
    agent_contact: GetAgentContactSchema
    balance: GetBalanceSchema
    subscription: GetSubscriptionSchema
    notification_settings: GetNotificationSettingsSchema
