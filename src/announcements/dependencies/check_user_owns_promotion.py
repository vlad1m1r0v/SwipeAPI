from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from sqlalchemy import orm

from src.announcements.models import Promotion, Announcement
from src.announcements.services import AnnouncementPromotionService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema
from src.core.exceptions import IsNotOwnerException


@inject
async def check_user_owns_promotion(
    promotion_id: int,
    promotion_service: FromDishka[AnnouncementPromotionService],
    user: GetUserSchema = Depends(user_from_token),
) -> GetUserSchema:
    promotion = await promotion_service.get(
        promotion_id,
        load=[
            orm.joinedload(Promotion.announcement),
            orm.joinedload(Promotion.announcement).joinedload(Announcement.apartment),
        ],
    )

    if promotion.announcement.apartment.user_id != user.id:
        raise IsNotOwnerException()

    return user
