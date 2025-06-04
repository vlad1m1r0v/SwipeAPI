from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.services import JwtService
from src.auth.exceptions import TokenNotProvidedException, InvalidTokenTypeException
from src.auth.enums import TokenType
from src.auth.utils import http_bearer

from src.users.services import UserService
from src.users.enums import Role
from src.users.exceptions import UserDoesNotExistException, InvalidRoleException

from src.builders.schemas import GetBuilderSchema


@inject
async def builder_from_token(
    jwt_service: FromDishka[JwtService],
    user_service: FromDishka[UserService],
    auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> GetBuilderSchema:
    if not auth_credentials:
        raise TokenNotProvidedException()

    token = auth_credentials.credentials
    payload = jwt_service.decode_jwt(token)

    if payload["type"] != TokenType.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    builder = await user_service.get_builder_profile(item_id=int(payload["sub"]))

    if not builder:
        raise UserDoesNotExistException()

    if builder.role != Role.BUILDER:
        raise InvalidRoleException()

    return user_service.to_schema(data=builder, schema_type=GetBuilderSchema)
