from typing import Annotated

from fastapi import APIRouter, Form

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from src.auth.schemas import TokensSchema
from src.auth.services import JwtService

from src.users.schemas import (
    CreateUserSchema,
    UserPayloadSchema,
    CreateContactSchema,
    CreateAgentContactSchema,
    CreateBalanceSchema,
    CreateSubscriptionSchema,
    CreateNotificationSettingsSchema,
)

from src.users.services import (
    UserService,
    ContactService,
    AgentContactService,
    SubscriptionService,
    NotificationSettingsService,
    BalanceService
)

from src.users.exceptions import UserAlreadyExistsException

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=TokensSchema)
@inject
async def register_user(
        jwt_service: FromDishka[JwtService],
        user_service: FromDishka[UserService],
        contact_service: FromDishka[ContactService],
        agent_contact_service: FromDishka[AgentContactService],
        subscription_service: FromDishka[SubscriptionService],
        notification_settings_service: FromDishka[NotificationSettingsService],
        balance_service: FromDishka[BalanceService],
        data: Annotated[CreateUserSchema, Form()]
):
    if await user_service.exists(email=data.email):
        raise UserAlreadyExistsException()

    user = await user_service.create_user(data)

    contact = CreateContactSchema(user_id=user.id, email=user.email, phone=user.phone)
    await contact_service.create(contact)

    agent_contact = CreateAgentContactSchema(user_id=user.id)
    await agent_contact_service.create(agent_contact)

    subscription = CreateSubscriptionSchema(user_id=user.id)
    await subscription_service.create(subscription)

    notification_settings = CreateNotificationSettingsSchema(user_id=user.id)
    await notification_settings_service.create(notification_settings)

    # balance = CreateBalanceSchema(user_id=user.id)
    # await balance_service.create(balance)

    user_payload = user_service.to_schema(data=user, schema_type=UserPayloadSchema)
    access_token = jwt_service.create_access_token(user_payload=user_payload)
    refresh_token = jwt_service.create_refresh_token(user_payload=user_payload)

    return TokensSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
