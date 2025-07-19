from datetime import datetime

from pydantic import BaseModel


class CreateSubscriptionSchema(BaseModel):
    user_id: int
    is_auto_renewal: bool
    expiry_date: datetime


class UpdateSubscriptionSchema(BaseModel):
    is_auto_renewal: bool


class GetSubscriptionSchema(BaseModel):
    id: int
    is_auto_renewal: bool
    expiry_date: datetime
