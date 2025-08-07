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

from src.announcements.exceptions import FiltersAmountExceededException
from src.announcements.services import AnnouncementFilterService
from src.announcements.dependencies import check_user_owns_filter
from src.announcements.schemas import (
    CreateFilterSchema,
    GetFilterSchema,
    UpdateFilterSchema,
)

router = APIRouter(prefix="/filters", tags=["User: Filters"])


@router.get(
    path="",
    response_model=SuccessResponse[OffsetPagination[GetFilterSchema]],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_filters(
    filter_service: FromDishka[AnnouncementFilterService],
    limit: int = Query(default=20),
    offset: int = Query(default=0),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetFilterSchema]]:
    results, total = await filter_service.get_user_filters(
        limit=limit, offset=offset, user_id=user.id
    )
    return SuccessResponse(
        data=filter_service.to_schema(
            data=results,
            total=total,
            filters=[LimitOffset(limit=limit, offset=offset)],
            schema_type=GetFilterSchema,
        )
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        FiltersAmountExceededException,
        IntegrityErrorException,
        auth=True,
        role=True,
        user=True,
    ),
    response_model=SuccessResponse[GetFilterSchema],
    response_model_exclude_none=True,
)
@inject
async def create_filter(
    filter_service: FromDishka[AnnouncementFilterService],
    data: CreateFilterSchema = Body(),
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetFilterSchema]:
    created = await filter_service.create_filter(
        user_id=user.id, data={"user_id": user.id, **data.model_dump(exclude_none=True)}
    )
    return SuccessResponse(
        data=filter_service.to_schema(data=created, schema_type=GetFilterSchema)
    )


@router.patch(
    path="/{filter_id}",
    status_code=status.HTTP_201_CREATED,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetFilterSchema],
    response_model_exclude_none=True,
)
@inject
async def update_filter(
    filter_service: FromDishka[AnnouncementFilterService],
    filter_id: int,
    data: UpdateFilterSchema = Body(),
    _: GetUserSchema = Depends(check_user_owns_filter),
) -> SuccessResponse[GetFilterSchema]:
    updated = await filter_service.update(
        item_id=filter_id, data=data.model_dump(exclude_none=True)
    )
    return SuccessResponse(
        data=filter_service.to_schema(data=updated, schema_type=GetFilterSchema)
    )


@router.delete(
    path="/{filter_id}",
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
async def delete_filter(
    filter_service: FromDishka[AnnouncementFilterService],
    filter_id: int,
    _: GetUserSchema = Depends(check_user_owns_filter),
):
    await filter_service.delete(item_id=filter_id)
    return SuccessResponse(message="Filter has been deleted successfully.")
