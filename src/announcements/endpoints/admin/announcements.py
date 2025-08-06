from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import admin_from_token

from src.user.schemas import GetUserSchema

from src.announcements.services import AnnouncementService
from src.announcements.schemas import GetAnnouncementUserListSchema

router = APIRouter(prefix="/announcements", tags=["Admin: Announcements"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetAnnouncementUserListSchema]],
    responses=generate_examples(auth=True, role=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_announcements(
    announcement_service: FromDishka[AnnouncementService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    _: GetUserSchema = Depends(admin_from_token),
) -> SuccessResponse[OffsetPagination[GetAnnouncementUserListSchema]]:
    results, total = await announcement_service.get_announcements_for_admin(
        limit=limit, offset=offset
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetAnnouncementUserListSchema,
        )
    )
