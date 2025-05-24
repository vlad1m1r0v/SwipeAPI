from typing import Optional

from dishka import FromDishka
from dishka.integrations.fastapi import inject

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.auth.services import JwtService
from src.auth.exceptions import (
    TokenNotProvidedException,
    InvalidTokenTypeException
)
from src.auth.schemas import BasePayloadSchema
from src.auth.enums import TokenType
from src.auth.utils import http_bearer

from src.users.services import UserService
from src.users.exceptions import UserDoesNotExistException


def payload_from_token(token_type: TokenType):
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
