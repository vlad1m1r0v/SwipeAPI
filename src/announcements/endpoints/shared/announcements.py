from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status


from src.core.exceptions import (
    NotFoundException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.announcements.schemas import GetAnnouncementSharedDetailSchema
from src.announcements.services import AnnouncementService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/announcements", tags=["Shared: Announcements"])


@router.get(
    path="/{announcement_id}",
    response_model=SuccessResponse[GetAnnouncementSharedDetailSchema],
    responses=generate_examples(NotFoundException, auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def get_announcement(
    announcement_service: FromDishka[AnnouncementService],
    announcement_id: int,
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetAnnouncementSharedDetailSchema]:
    announcement = await announcement_service.get_announcement_detail_for_shared(
        user.id, announcement_id
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=announcement, schema_type=GetAnnouncementSharedDetailSchema
        )
    )
