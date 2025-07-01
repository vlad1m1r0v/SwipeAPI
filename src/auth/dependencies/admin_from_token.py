from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.services import JwtService
from src.auth.exceptions import TokenNotProvidedException, InvalidTokenTypeException
from src.auth.enums import TokenType
from src.auth.utils import http_bearer

from src.user.services import UserService
from src.user.enums import Role
from src.user.exceptions import UserDoesNotExistException, InvalidRoleException

from src.admin.schemas import GetAdminSchema


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

    if payload["type"] != TokenType.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    admin = await user_service.get_one_or_none(id=int(payload["sub"]))

    if not admin:
        raise UserDoesNotExistException()

    if admin.role != Role.ADMIN:
        raise InvalidRoleException()

    return user_service.to_schema(data=admin, schema_type=GetAdminSchema)
