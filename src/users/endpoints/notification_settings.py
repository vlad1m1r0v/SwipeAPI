from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import user_from_token

from src.users.services import UserService, NotificationSettingsService
from src.users.schemas import GetUserSchema, UpdateNotificationSettingsSchema

router = APIRouter()


@router.patch("/notification-settings")
@inject
async def update_notification_settings(
    notification_settings_service: FromDishka[NotificationSettingsService],
    user_service: FromDishka[UserService],
    data: Annotated[UpdateNotificationSettingsSchema, Form()],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    await notification_settings_service.update(
        item_id=user.notification_settings.id,
        data={**data.model_dump(exclude_none=True)},
    )
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
