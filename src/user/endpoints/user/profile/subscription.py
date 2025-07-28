from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends
from starlette import status

from src.core.utils import generate_examples
from src.core.schemas import SuccessResponse

from src.auth.dependencies import user_from_token

from src.user.services import (
    SubscriptionService,
    SubscriptionRenewalService,
)
from src.user.schemas import (
    GetUserSchema,
    GetSubscriptionSchema,
    UpdateSubscriptionSchema,
)

router = APIRouter(prefix="/subscription")


@router.patch(
    path="",
    response_model=SuccessResponse[GetSubscriptionSchema],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def update_subscription(
    subscription_service: FromDishka[SubscriptionService],
    data: UpdateSubscriptionSchema,
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetSubscriptionSchema]:
    result = await subscription_service.update(
        item_id=user.subscription.id, data=data.model_dump()
    )
    return SuccessResponse(
        data=subscription_service.to_schema(
            data=result, schema_type=GetSubscriptionSchema
        )
    )


@router.patch(
    path="/renew",
    response_model=SuccessResponse[GetSubscriptionSchema],
    responses=generate_examples(auth=True, role=True, user=True),
    status_code=status.HTTP_200_OK,
)
@inject
async def renew_subscription(
    subscription_service: FromDishka[SubscriptionService],
    subscription_renewal_service: FromDishka[SubscriptionRenewalService],
    user: GetUserSchema = Depends(user_from_token),
) -> SuccessResponse[GetSubscriptionSchema]:
    result = await subscription_renewal_service.renew_user_subscription(item_id=user.id)
    return SuccessResponse(
        data=subscription_service.to_schema(
            data=result, schema_type=GetSubscriptionSchema
        )
    )
