from datetime import date

from src.auth.tasks import send_forgot_password_email

from src.auth.exceptions import TokenAlreadyUsedException

from src.auth.schemas import (
    RegisterSchema,
    LoginSchema,
    BasePayloadSchema,
    TokensSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)

from src.auth.services.jwt import JwtService
from src.auth.services.sign import SignService

from src.user.enums import Role

from src.user.exceptions import (
    UserAlreadyExistsException,
    UserDoesNotExistException,
    InvalidRoleException,
    SubscriptionExpiredException,
    UserBlacklistedException,
)

from src.user.services import UserService, SubscriptionService

from src.admin.services import BlacklistService


class AuthService:
    def __init__(
        self,
        jwt_service: JwtService,
        sign_service: SignService,
        user_service: UserService,
        blacklist_service: BlacklistService,
        subscription_service: SubscriptionService,
    ):
        # Auth related services
        self._jwt_service = jwt_service
        self._sign_service = sign_service
        self._user_service = user_service

        # User related services
        self._blacklist_service = blacklist_service
        self._subscription_service = subscription_service

    async def register_user(self, data: RegisterSchema) -> TokensSchema:
        if await self._user_service.exists(email=data.email):
            raise UserAlreadyExistsException()

        user = await self._user_service.create_user(data)

        user_schema = self._user_service.to_schema(
            data=user, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(user_schema)

    async def register_admin(self, data: RegisterSchema) -> TokensSchema:
        if await self._user_service.exists(email=data.email):
            raise UserAlreadyExistsException()

        admin = await self._user_service.create_admin(data)

        admin_schema = self._user_service.to_schema(
            data=admin, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(admin_schema)

    async def register_builder(self, data: RegisterSchema) -> TokensSchema:
        if await self._user_service.exists(email=data.email):
            raise UserAlreadyExistsException()

        builder = await self._user_service.create_builder(data)

        builder_schema = self._user_service.to_schema(
            data=builder, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(builder_schema)

    async def login_builder(self, data: LoginSchema) -> TokensSchema:
        builder = await self._user_service.authenticate(data)

        if builder.role != Role.BUILDER:
            raise InvalidRoleException()

        builder_schema = self._user_service.to_schema(
            data=builder, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(builder_schema)

    async def login_user(self, data: LoginSchema) -> TokensSchema:
        user = await self._user_service.authenticate(data)

        if user.role != Role.USER:
            raise InvalidRoleException()

        subscription = await self._subscription_service.get_one_or_none(user_id=user.id)

        if subscription.expiry_date.date() <= date.today():
            raise SubscriptionExpiredException()

        if await self._blacklist_service.get_one_or_none(user_id=user.id):
            raise UserBlacklistedException()

        user_schema = self._user_service.to_schema(
            data=user, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(user_schema)

    async def login_admin(self, data: LoginSchema) -> TokensSchema:
        admin = await self._user_service.authenticate(data)

        if admin.role != Role.ADMIN:
            raise InvalidRoleException()

        admin_schema = self._user_service.to_schema(
            data=admin, schema_type=BasePayloadSchema
        )
        return self.generate_tokens(admin_schema)

    async def send_forgot_password_email(self, data: ForgotPasswordSchema) -> None:
        user = await self._user_service.get_one_or_none(email=data.email)

        if user is None:
            raise UserDoesNotExistException()

        token = self._sign_service.encode(data={"id": user.id, "email": data.email})
        send_forgot_password_email.delay(token=token, email=data.email)

    async def reset_password(self, data: ResetPasswordSchema) -> None:
        token = data.token

        if await self._sign_service.token_exists(token):
            raise TokenAlreadyUsedException()

        decoded = self._sign_service.decode(token)

        email = decoded["email"]
        user_id = decoded["id"]

        user = await self._user_service.get_one_or_none(email=email)

        if user is None:
            raise UserDoesNotExistException()

        await self._user_service.update(
            data={"password": data.new_password}, item_id=user_id
        )

        await self._sign_service.save_token(token=data.token)

    def generate_tokens(self, base_payload: BasePayloadSchema) -> TokensSchema:
        access_token = self._jwt_service.create_access_token(base_payload=base_payload)
        refresh_token = self._jwt_service.create_refresh_token(
            base_payload=base_payload
        )

        return TokensSchema(access_token=access_token, refresh_token=refresh_token)


__all__ = ["AuthService"]
