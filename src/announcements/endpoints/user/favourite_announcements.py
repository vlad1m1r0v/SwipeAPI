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

from src.announcements.services import AnnouncementFavouriteService
from src.announcements.dependencies import check_user_owns_favourite_announcement
from src.announcements.schemas import (
    CreateFavouriteAnnouncementSchema,
    GetFavouriteAnnouncementUserListSchema,
    GetFavouriteAnnouncementUserDetailSchema,
)

router = APIRouter(
    prefix="/favourite-announcements", tags=["User: Favourite Announcements"]
)


@router.get(
    path="",
    response_model=SuccessResponse[
        OffsetPagination[GetFavouriteAnnouncementUserListSchema]
    ],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_favourite_announcements(
    favourite_announcement_service: FromDishka[AnnouncementFavouriteService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetFavouriteAnnouncementUserListSchema]]:
    (
        results,
        total,
    ) = await favourite_announcement_service.get_favourite_user_announcements(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=favourite_announcement_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetFavouriteAnnouncementUserListSchema,
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetFavouriteAnnouncementUserDetailSchema],
)
@inject
async def create_favourite_announcement(
    favourite_announcement_service: FromDishka[AnnouncementFavouriteService],
    data: CreateFavouriteAnnouncementSchema = Body(),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetFavouriteAnnouncementUserDetailSchema]:
    created = await favourite_announcement_service.create(
        data={"user_id": user.id, **data.model_dump()}
    )
    favourite_announcement = (
        await favourite_announcement_service.get_favourite_user_announcement(created.id)
    )
    return SuccessResponse(
        data=favourite_announcement_service.to_schema(
            data=favourite_announcement,
            schema_type=GetFavouriteAnnouncementUserDetailSchema,
        )
    )


@router.delete(
    path="/{favourite_announcement_id}",
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
)
@inject
async def delete_favourite_announcement(
    favourite_announcement_service: FromDishka[AnnouncementFavouriteService],
    favourite_announcement_id: int,
    _: GetUserSchema = Depends(check_user_owns_favourite_announcement),
):
    await favourite_announcement_service.delete(item_id=favourite_announcement_id)
    return SuccessResponse(
        message="Announcement has been removed from favourites successfully."
    )
