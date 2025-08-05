from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.announcements.services import AnnouncementFilterService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_filter(
    filter_id: int,
    filter_service: FromDishka[AnnouncementFilterService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    announcement_filter = await filter_service.get(item_id=filter_id)

    if announcement_filter.user_id != user.id:
        raise IsNotOwnerException()

    return user
