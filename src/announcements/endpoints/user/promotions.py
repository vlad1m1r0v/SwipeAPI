from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Body
from starlette import status

from src.core.exceptions import (
    NotFoundException,
    IntegrityErrorException,
    IsNotOwnerException,
)
from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.user.schemas import GetUserSchema

from src.announcements.services import AnnouncementPromotionService
from src.announcements.dependencies import check_user_owns_promotion
from src.announcements.schemas import (
    GetPromotionWithExpiryDatesSchema,
    UpdatePromotionSchema,
)

router = APIRouter(prefix="/promotions", tags=["User: Promotions"])


@router.get(
    path="/{promotion_id}",
    response_model=SuccessResponse[GetPromotionWithExpiryDatesSchema],
    responses=generate_examples(
        IsNotOwnerException, NotFoundException, auth=True, role=True, user=True
    ),
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
@inject
async def get_promotion(
    promotion_service: FromDishka[AnnouncementPromotionService],
    promotion_id: int,
    _: GetUserSchema = Depends(check_user_owns_promotion),
) -> SuccessResponse[GetPromotionWithExpiryDatesSchema]:
    promotion = await promotion_service.get(promotion_id)
    return SuccessResponse(
        data=promotion_service.to_schema(
            data=promotion, schema_type=GetPromotionWithExpiryDatesSchema
        )
    )


@router.patch(
    path="/{promotion_id}",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        IntegrityErrorException, auth=True, role=True, user=True
    ),
    response_model=SuccessResponse[GetPromotionWithExpiryDatesSchema],
    response_model_exclude_none=True,
)
@inject
async def update_promotion(
    promotion_service: FromDishka[AnnouncementPromotionService],
    promotion_id: int,
    data: UpdatePromotionSchema = Body(),
    _: GetUserSchema = Depends(check_user_owns_promotion),
) -> SuccessResponse[GetPromotionWithExpiryDatesSchema]:
    promotion = await promotion_service.update_promotion(
        promotion_id=promotion_id, data=data.model_dump(exclude_none=True)
    )
    return SuccessResponse(
        data=promotion_service.to_schema(
            data=promotion, schema_type=GetPromotionWithExpiryDatesSchema
        )
    )
