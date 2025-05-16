from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from src.auth.services import JwtService
from src.auth.exceptions import (
    InvalidTokenTypeException
)
from src.auth.enums import TokenTypeEnum

from src.users.services import UserService
from src.users.exceptions import (
    UserDoesNotExistException,
    InvalidRoleException
)
from src.users.schemas import GetUserSchema
from src.users.enums import UserRoleEnum

http_bearer = HTTPBearer(auto_error=False)


@inject
async def user_from_token(
        jwt_service: FromDishka[JwtService],
        user_service: FromDishka[UserService],
        auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)

) -> GetUserSchema:
    token = auth_credentials.credentials
    payload = jwt_service.decode_jwt(token)

    if payload['type'] != TokenTypeEnum.ACCESS_TOKEN:
        raise InvalidTokenTypeException()

    user = await user_service.get_one_or_none(id=int(payload['sub']))

    if not user:
        raise UserDoesNotExistException()

    if user.role != UserRoleEnum.USER:
        raise InvalidRoleException()

    return user_service.to_schema(data=user, schema_type=GetUserSchema)


__all__ = ["user_from_token"]
