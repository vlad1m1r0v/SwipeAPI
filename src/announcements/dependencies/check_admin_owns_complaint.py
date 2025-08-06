from fastapi import Depends

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.announcements.services import AnnouncementComplaintService

from src.auth.dependencies import admin_from_token

from src.admin.schemas import GetAdminSchema

from src.core.exceptions import IsNotOwnerException


@inject
async def check_admin_owns_complaint(
    complaint_id: int,
    complaint_service: FromDishka[AnnouncementComplaintService],
    admin: GetAdminSchema = Depends(admin_from_token),
) -> GetAdminSchema:
    announcement_filter = await complaint_service.get(item_id=complaint_id)

    if announcement_filter.user_id != admin.id:
        raise IsNotOwnerException()

    return admin
