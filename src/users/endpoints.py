from typing import (
    Optional,
    Annotated
)

from pydantic import conint

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File
)

from src.auth.dependencies import user_from_token

from src.users.services import (
    UserService,
    ContactService,
    AgentContactService,
    SubscriptionService,
    BalanceService,
    NotificationSettingsService
)
from src.users.schemas import (
    GetUserSchema,
    UpdateUserSchema,
    UpdateContactSchema,
    UpdateAgentContactSchema,
    UpdateNotificationSettingsSchema
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile")
@inject
def get_profile(
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    return user


@router.patch("/account")
@inject
async def update_account(
        user_service: FromDishka[UserService],
        email: Optional[str] = Form(default=None),
        name: Optional[str] = Form(default=None),
        phone: Optional[str] = Form(default=None),
        photo: Optional[UploadFile] = File(default=None),
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    fields = UpdateUserSchema(
        email=email,
        name=name,
        phone=phone
    )

    data = {**fields.model_dump(exclude_none=True)}

    if photo:
        data["photo"] = photo

    await user_service.update(data=data, item_id=user.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.patch("/contact")
@inject
async def update_contact(
        contact_service: FromDishka[ContactService],
        user_service: FromDishka[UserService],
        data: Annotated[UpdateContactSchema, Form()],
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    await contact_service.update(data=data, item_id=user.contact.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.patch("/agent-contact")
@inject
async def update_agent_contact(
        agent_contact_service: FromDishka[AgentContactService],
        user_service: FromDishka[UserService],
        data: Annotated[UpdateAgentContactSchema, Form()],
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    await agent_contact_service.update(data=data, item_id=user.contact.id)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.patch("/subscription")
@inject
async def update_subscription(
        user_service: FromDishka[UserService],
        subscription_service: FromDishka[SubscriptionService],
        is_auto_renewal: bool = Form(default=False),
        user: GetUserSchema = Depends(user_from_token),
):
    await subscription_service.update(
        item_id=user.subscription.id,
        data={'is_auto_renewal': is_auto_renewal}
    )
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.post("/balance/deposit")
@inject
async def deposit_money(
        amount: Annotated[conint(le=9999), Form()],
        user_service: FromDishka[UserService],
        balance_service: FromDishka[BalanceService],
        user: GetUserSchema = Depends(user_from_token),
):
    await balance_service.deposit_money(item_id=user.balance.id, amount=amount)
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)


@router.patch("/notification-settings")
@inject
async def update_notification_settings(
        notification_settings_service: FromDishka[NotificationSettingsService],
        user_service: FromDishka[UserService],
        data: Annotated[UpdateNotificationSettingsSchema, Form()],
        user: GetUserSchema = Depends(user_from_token)
) -> GetUserSchema:
    await notification_settings_service.update(
        item_id=user.notification_settings.id,
        data={**data.model_dump(exclude_none=True)}
    )
    profile = await user_service.get_user_profile(item_id=user.id)
    return user_service.to_schema(data=profile, schema_type=GetUserSchema)