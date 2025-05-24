from typing import Optional

from datetime import date

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.services import JwtService
from src.auth.exceptions import (
    TokenNotProvidedException,
    InvalidTokenTypeException
)
from src.auth.enums import TokenType
from src.auth.utils import http_bearer

from src.users.services import UserService
from src.users.schemas import GetUserSchema
from src.users.enums import Role
from src.users.exceptions import (
    UserDoesNotExistException,
    InvalidRoleException,
    SubscriptionExpiredException,
    UserBlacklistedException
)

from src.admins.services import BlacklistService


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

    if payload["type"] != TokenType.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    user = await user_service.get_user_profile(item_id=int(payload["sub"]))

    if not user:
        raise UserDoesNotExistException()

    if user.role != Role.USER:
        raise InvalidRoleException()

    if user.subscription.expiry_date.date() <= date.today():
        raise SubscriptionExpiredException()

    if await blacklist_service.get_one_or_none(user_id=user.id):
        raise UserBlacklistedException()

    return user_service.to_schema(data=user, schema_type=GetUserSchema)