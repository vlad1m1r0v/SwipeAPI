from datetime import datetime

from pydantic import BaseModel


class GetSubscriptionSchema(BaseModel):
    id: int
    is_auto_renewal: bool
    expiry_date: datetime