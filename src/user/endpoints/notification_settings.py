from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.services import NotificationSettingsService
from src.user.schemas import (
    GetUserSchema,
    GetNotificationSettingsSchema,
    UpdateNotificationSettingsSchema,
)

router = APIRouter()


@router.patch(
    path="/notification-settings",
    response_model=SuccessResponse[GetNotificationSettingsSchema],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    tags=["User: Profile"],
)
@inject
async def update_notification_settings(
    notification_settings_service: FromDishka[NotificationSettingsService],
    data: UpdateNotificationSettingsSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetNotificationSettingsSchema]:
    result = await notification_settings_service.update(
        item_id=user.notification_settings.id,
        data={**data.model_dump(exclude_none=True)},
    )
    return SuccessResponse(
        data=notification_settings_service.to_schema(
            data=result, schema_type=GetNotificationSettingsSchema
        )
    )
