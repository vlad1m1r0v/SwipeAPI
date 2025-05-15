from decimal import Decimal

from pydantic import BaseModel

from src.users.constants import DEFAULT_BALANCE


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


__all__ = [
    "CreateContactSchema",
    "CreateAgentContactSchema",
    "CreateBalanceSchema",
    "CreateSubscriptionSchema",
    "CreateNotificationSettingsSchema",
]
