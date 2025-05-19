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
from src.auth.enums import TOKEN_TYPE

from src.users.services import UserService
from src.users.schemas import GetUserSchema
from src.users.enums import ROLE
from src.users.exceptions import (
    UserDoesNotExistException,
    InvalidRoleException
)

http_bearer = HTTPBearer(auto_error=False)


def user_from_token(token_type: TOKEN_TYPE = TOKEN_TYPE.ACCESS_TOKEN):
    @inject
    async def _user_from_token(
        jwt_service: FromDishka[JwtService],
        user_service: FromDishka[UserService],
        auth_credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
    ) -> GetUserSchema:
        token = auth_credentials.credentials
        payload = jwt_service.decode_jwt(token)

        if payload["type"] != token_type:
            raise InvalidTokenTypeException()

        user = await user_service.get_user_profile(item_id=int(payload["sub"]))

        if not user:
            raise UserDoesNotExistException()

        if user.role != ROLE.USER:
            raise InvalidRoleException()

        return user_service.to_schema(data=user, schema_type=GetUserSchema)

    return _user_from_token
