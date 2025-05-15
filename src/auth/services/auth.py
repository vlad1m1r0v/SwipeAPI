from src.auth.schemas import TokensSchema
from src.auth.services.jwt import JwtService

from src.users.exceptions import UserAlreadyExistsException
from src.users.schemas import (
    CreateUserSchema,
    CreateContactSchema,
    CreateAgentContactSchema,
    CreateBalanceSchema,
    CreateSubscriptionSchema,
    CreateNotificationSettingsSchema,
    UserPayloadSchema
)
from src.users.services import (
    UserService,
    ContactService,
    AgentContactService,
    SubscriptionService,
    NotificationSettingsService,
    BalanceService
)


class AuthService:
    def __init__(
            self,
            jwt_service: JwtService,
            user_service: UserService,
            contact_service: ContactService,
            agent_contact_service: AgentContactService,
            subscription_service: SubscriptionService,
            notification_settings_service: NotificationSettingsService,
            balance_service: BalanceService,
    ):
        self._jwt_service = jwt_service
        self._user_service = user_service
        self._contact_service = contact_service
        self._agent_contact_service = agent_contact_service
        self._subscription_service = subscription_service
        self._notification_settings_service = notification_settings_service
        self._balance_service = balance_service

    async def register_user(self, data: CreateUserSchema) -> TokensSchema:
        if await self._user_service.exists(email=data.email):
            raise UserAlreadyExistsException()

        user = await self._user_service.create_user(data)

        contact = CreateContactSchema(user_id=user.id, email=user.email, phone=user.phone)
        await self._contact_service.create(contact)

        agent_contact = CreateAgentContactSchema(user_id=user.id)
        await self._agent_contact_service.create(agent_contact)

        subscription = CreateSubscriptionSchema(user_id=user.id)
        await self._subscription_service.create(subscription)

        notification_settings = CreateNotificationSettingsSchema(user_id=user.id)
        await self._notification_settings_service.create(notification_settings)

        balance = CreateBalanceSchema(user_id=user.id)
        await self._balance_service.create(balance)

        user_payload = self._user_service.to_schema(data=user, schema_type=UserPayloadSchema)
        access_token = self._jwt_service.create_access_token(user_payload=user_payload)
        refresh_token = self._jwt_service.create_refresh_token(user_payload=user_payload)

        return TokensSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )


__all__ = ['AuthService']
