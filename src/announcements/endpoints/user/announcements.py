from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query, Body
from starlette import status

from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from src.core.exceptions import (
    NotFoundException,
    IntegrityErrorException,
    IsNotOwnerException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

from src.announcements.services import AnnouncementService
from src.announcements.dependencies import check_user_owns_announcement
from src.announcements.schemas import (
    CreateAnnouncementSchema,
    UpdateAnnouncementSchema,
    GetAnnouncementUserListSchema,
    GetAnnouncementUserDetailSchema,
)

router = APIRouter(prefix="/announcements", tags=["User: Announcements"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetAnnouncementUserListSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_announcements(
    announcement_service: FromDishka[AnnouncementService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetAnnouncementUserListSchema]]:
    results, total = await announcement_service.get_announcements_for_user(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetAnnouncementUserListSchema,
        )
    )


@router.get(
    path="/{announcement_id}",
    response_model=SuccessResponse[GetAnnouncementUserDetailSchema],
    responses=generate_examples(
        IsNotOwnerException, NotFoundException, auth=True, role=True, user=True
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_announcement(
    announcement_service: FromDishka[AnnouncementService],
    announcement_id: int,
    _: GetUserSchema = Depends(check_user_owns_announcement),
) -> SuccessResponse[GetAnnouncementUserDetailSchema]:
    announcement = await announcement_service.get_announcement_detail_for_user(
        announcement_id
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=announcement, schema_type=GetAnnouncementUserDetailSchema
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetAnnouncementUserDetailSchema],
    response_model_exclude_none=True,
)
@inject
async def create_announcement(
    announcement_service: FromDishka[AnnouncementService],
    data: CreateAnnouncementSchema = Body(),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetAnnouncementUserDetailSchema]:
    created = await announcement_service.create_announcement(data=data.model_dump())
    announcement = await announcement_service.get_announcement_detail_for_user(
        created.id
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=announcement, schema_type=GetAnnouncementUserDetailSchema
        )
    )


@router.patch(
    path="/{announcement_id}",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetAnnouncementUserDetailSchema],
    response_model_exclude_none=True,
)
@inject
async def update_announcement(
    announcement_service: FromDishka[AnnouncementService],
    announcement_id: int,
    data: UpdateAnnouncementSchema = Body(),
    _: GetUserSchema = Depends(check_user_owns_announcement),
) -> SuccessResponse[GetAnnouncementUserDetailSchema]:
    updated = await announcement_service.update(
        item_id=announcement_id, data=data.model_dump()
    )
    announcement = await announcement_service.get_announcement_detail_for_user(
        updated.id
    )
    return SuccessResponse(
        data=announcement_service.to_schema(
            data=announcement, schema_type=GetAnnouncementUserDetailSchema
        )
    )


@router.delete(
    path="/{announcement_id}",
    response_model=SuccessResponse,
    responses=generate_examples(
        IsNotOwnerException,
        IntegrityErrorException,
        NotFoundException,
        auth=True,
        role=True,
        user=True,
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def delete_announcement(
    announcement_service: FromDishka[AnnouncementService],
    announcement_id: int,
    _: GetUserSchema = Depends(check_user_owns_announcement),
):
    await announcement_service.delete(item_id=announcement_id)
    return SuccessResponse(message="Announcement has been deleted successfully.")
