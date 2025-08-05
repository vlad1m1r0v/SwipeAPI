from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.announcements.models import Announcement
from src.announcements.services import AnnouncementService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_announcement(
    announcement_id: int,
    announcement_service: FromDishka[AnnouncementService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    announcement = await announcement_service.get(
        announcement_id, load=[orm.joinedload(Announcement.apartment)]
    )

    if announcement.apartment.user_id != user.id:
        raise IsNotOwnerException()

    return user
