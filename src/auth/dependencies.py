from typing import Optional

from datetime import date

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from src.auth.services import JwtService
from src.auth.exceptions import (
    TokenNotProvidedException,
    InvalidTokenTypeException
)
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TOKEN_TYPE

from src.users.services import UserService
from src.users.schemas import GetUserSchema
from src.users.enums import ROLE
from src.users.exceptions import (
    UserDoesNotExistException,
    InvalidRoleException,
    SubscriptionExpiredException,
    UserBlacklistedException
)

from src.admins.schemas import GetAdminSchema
from src.admins.services import BlacklistService

http_bearer = HTTPBearer(auto_error=False)


def payload_from_token(token_type: TOKEN_TYPE):
    @inject
    async def _payload_from_token(
            jwt_service: FromDishka[JwtService],
            user_service: FromDishka[UserService],
            auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
    ) -> BasePayloadSchema:
        if not auth_credentials:
            raise TokenNotProvidedException()

        token = auth_credentials.credentials
        payload = jwt_service.decode_jwt(token)

        if payload["type"] != token_type:
            raise InvalidTokenTypeException()

        account = await user_service.get_one_or_none(id=int(payload["sub"]))

        if not account:
            raise UserDoesNotExistException()

        return user_service.to_schema(data=account, schema_type=BasePayloadSchema)

    return _payload_from_token


@inject
async def user_from_token(
        jwt_service: FromDishka[JwtService],
        user_service: FromDishka[UserService],
        blacklist_service: FromDishka[BlacklistService],
        auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> GetUserSchema:
    if not auth_credentials:
        raise TokenNotProvidedException()

    token = auth_credentials.credentials
    payload = jwt_service.decode_jwt(token)

    if payload["type"] != TOKEN_TYPE.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    user = await user_service.get_user_profile(item_id=int(payload["sub"]))

    if not user:
        raise UserDoesNotExistException()

    if user.role != ROLE.USER:
        raise InvalidRoleException()

    if user.subscription.expiry_date.date() <= date.today():
        raise SubscriptionExpiredException()

    if await blacklist_service.get_one_or_none(user_id=user.id):
        raise UserBlacklistedException()

    return user_service.to_schema(data=user, schema_type=GetUserSchema)


@inject
async def admin_from_token(
        jwt_service: FromDishka[JwtService],
        user_service: FromDishka[UserService],
        auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> GetAdminSchema:
    if not auth_credentials:
        raise TokenNotProvidedException()

    token = auth_credentials.credentials
    payload = jwt_service.decode_jwt(token)

    if payload["type"] != TOKEN_TYPE.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    admin = await user_service.get_one_or_none(id=int(payload["sub"]))

    if not admin:
        raise UserDoesNotExistException()

    if admin.role != ROLE.ADMIN:
        raise InvalidRoleException()

    return user_service.to_schema(data=admin, schema_type=GetAdminSchema)


__all__ = [
    "payload_from_token",
    "user_from_token",
    "admin_from_token"
]
