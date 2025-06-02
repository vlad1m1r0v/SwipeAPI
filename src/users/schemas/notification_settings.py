from typing import Optional

from pydantic import BaseModel, Field

from src.users.enums import NotificationType


class UpdateNotificationSettingsSchema(BaseModel):
    redirect_notifications_to_agent: Optional[bool] = Field(default=None)
    notification_type: Optional[NotificationType] = Field(default=None)


class GetNotificationSettingsSchema(BaseModel):
    id: int
    redirect_notifications_to_agent: bool
    notification_type: NotificationType
