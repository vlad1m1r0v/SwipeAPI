from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.announcements.services import AnnouncementFavouriteService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_favourite_announcement(
    favourite_announcement_id: int,
    favourite_announcement_service: FromDishka[AnnouncementFavouriteService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    favourite_announcement = await favourite_announcement_service.get(
        item_id=favourite_announcement_id
    )

    if favourite_announcement.user_id != user.id:
        raise IsNotOwnerException()

    return user
