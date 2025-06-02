from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import APIRouter, Depends, Form

from src.auth.dependencies import user_from_token

from src.users.services import UserService, SubscriptionService
from src.users.schemas import GetUserSchema


router = APIRouter()


@router.patch("/subscription")
@inject
async def update_subscription(
    user_service: FromDishka[UserService],
    subscription_service: FromDishka[SubscriptionService],
    is_auto_renewal: bool = Form(default=False),
    user: GetUserSchema = Depends(user_from_token),
):
    await subscription_service.update(
        item_id=user.subscription.id, data={"is_auto_renewal": is_auto_renewal}
    )
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)
