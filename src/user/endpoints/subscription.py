from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends

from src.auth.dependencies import user_from_token

from src.user.services import (
    UserService,
    SubscriptionService,
    SubscriptionRenewalService,
)
from src.user.schemas import GetUserSchema, UpdateSubscriptionSchema

router = APIRouter(prefix="/subscription", tags=["User: Subscription"])


@router.patch("", response_model=GetUserSchema)
@inject
async def update_subscription(
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    data: UpdateSubscriptionSchema,
    user: GetUserSchema = Depends(user_from_token),
):
    await subscription_service.update(
        item_id=user.subscription.id, data=data.model_dump()
    )
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.patch("/renew", response_model=GetUserSchema)
@inject
async def renew_subscription(
    user_service: FromDishka[UserService],
    subscription_renewal_service: FromDishka[SubscriptionRenewalService],
    user: GetUserSchema = Depends(user_from_token),
):
    await subscription_renewal_service.renew_user_subscription(item_id=user.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
