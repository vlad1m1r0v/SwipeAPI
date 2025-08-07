from advanced_alchemy.service import OffsetPagination
from advanced_alchemy.filters import LimitOffset

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.builder.enums import (
    Type,
    Status,
    PropertyType,
    BillingOptions,
)

from src.apartments.enums import Rooms, Finishing

from src.core.exceptions import (
    NotFoundException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.announcements.schemas import (
    GetAnnouncementSharedDetailSchema,
    GetAnnouncementUserListSchema,
)
from src.announcements.services import AnnouncementService

from src.auth.dependencies import user_from_token

from src.user.schemas import GetUserSchema

router = APIRouter(prefix="/announcements", tags=["Shared: Announcements"])


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
    filter_id: int | None = Query(default=None),
    district: str | None = Query(default=None),
    neighbourhood: str | None = Query(default=None),
    price_min: int | None = Query(default=None),
    price_max: int | None = Query(default=None),
    area_min: float | None = Query(default=None),
    area_max: float | None = Query(default=None),
    rooms: Rooms | None = Query(default=None),
    finishing: Finishing | None = Query(default=None),
    complex_type: Type | None = Query(default=None),
    complex_status: Status | None = Query(alias="status", default=None),
    property_type: PropertyType | None = Query(default=None),
    billing_options: BillingOptions | None = Query(default=None),
    _: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[OffsetPagination[GetAnnouncementUserListSchema]]:
    results, total = await announcement_service.get_announcements_for_shared(
        limit=limit,
        offset=offset,
        filter_id=filter_id,
        district=district,
        neighbourhood=neighbourhood,
        price_min=price_min,
        price_max=price_max,
        area_min=area_min,
        area_max=area_max,
        rooms=rooms,
        finishing=finishing,
        complex_type=complex_type,
        status=complex_status,
        property_type=property_type,
        billing_options=billing_options,
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
    response_model=SuccessResponse[GetAnnouncementSharedDetailSchema],
    responses=generate_examples(NotFoundException, auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
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
