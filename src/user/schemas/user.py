from typing import Optional

from pydantic import BaseModel, EmailStr, Field, computed_field

from config import config

from .contact import GetContactSchema
from .agent_contact import GetAgentContactSchema
from .notification_settings import GetNotificationSettingsSchema
from .subscription import GetSubscriptionSchema
from .balance import GetBalanceSchema

from src.user.enums import Role

from src.core.constants import PHONE_NUMBER


class UpdateUserAccountSchema(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=100)
    phone: Optional[str] = Field(pattern=PHONE_NUMBER)
    email: Optional[EmailStr]
    photo: Optional[str]


class GetUserAccountSchema(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    role: Role
    photo: Optional[str] = Field(exclude=True, default=None)

    @computed_field
    @property
    def photo_url(self) -> Optional[str]:
        return f"{config.server.url}/{self.photo}" if self.photo else None

    class Config:
        from_attributes = True


class GetUserSchema(GetUserAccountSchema):
    contact: GetContactSchema
    agent_contact: GetAgentContactSchema
    balance: GetBalanceSchema
    subscription: GetSubscriptionSchema
    notification_settings: GetNotificationSettingsSchema
