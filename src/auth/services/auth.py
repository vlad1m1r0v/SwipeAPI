from src.auth.schemas import (
    RegisterSchema,
    LoginSchema,
    BasePayloadSchema,
    TokensSchema
)

from src.auth.services.jwt import JwtService

from src.users.enums import ROLE

from src.users.schemas import GetUserSchema

from src.users.exceptions import (
    UserAlreadyExistsException,
    InvalidRoleException
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

    async def register_user(self, data: RegisterSchema) -> TokensSchema:
        if await self._user_service.exists(email=data.email):
            raise UserAlreadyExistsException()

        user = await self._user_service.create_user(data)

        await self._contact_service.create(
            {
                'user_id': user.id,
                'email': user.email,
                'phone': user.phone
            }
        )

        await self._agent_contact_service.create({
            'user_id': user.id
        })

        await self._subscription_service.create({
            'user_id': user.id
        })

        await self._notification_settings_service.create({
            'user_id': user.id
        })

        await self._balance_service.create({
            'user_id': user.id
        })

        user_schema = self._user_service.to_schema(data=user, schema_type=GetUserSchema)
        return self.generate_tokens(user_schema)

    async def login_user(self, data: LoginSchema) -> TokensSchema:
        user = await self._user_service.authenticate(data)

        if user.role != ROLE.USER:
            raise InvalidRoleException()

        user_schema = self._user_service.to_schema(data=user, schema_type=GetUserSchema)
        return self.generate_tokens(user_schema)

    def generate_tokens(self, user: GetUserSchema) -> TokensSchema:
        base_payload = BasePayloadSchema(**user.model_dump())

        access_token = self._jwt_service.create_access_token(base_payload=base_payload)
        refresh_token = self._jwt_service.create_refresh_token(base_payload=base_payload)

        return TokensSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )

    __all__ = ['AuthService']
