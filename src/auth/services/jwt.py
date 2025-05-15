import uuid
from datetime import timedelta, datetime, UTC

import jwt

from config import Config
from src.auth.enums import TokenTypeEnum
from src.auth.schemas import CreateTokenPayloadSchema, TokenPayloadSchema
from src.users.schemas import UserPayloadSchema


class JwtService:
    def __init__(self, config: Config):
        self._public_key = config.jwt.public_key_path.read_text()
        self._private_key = config.jwt.private_key_path.read_text()
        self._algorithm = config.jwt.algorithm
        self._expire_minutes: int = config.jwt.access_token_expire_minutes
        self._expire_days = timedelta(days=config.jwt.refresh_token_expire_days)

    def create_access_token(self, user_payload: UserPayloadSchema) -> str:
        payload = CreateTokenPayloadSchema(
            type=TokenTypeEnum.ACCESS_TOKEN,
            sub=user_payload.id,
            name=user_payload.name,
            email=user_payload.email,
            role=user_payload.role,
        )

        return self._encode_jwt(payload=payload, expire_minutes=self._expire_minutes)

    def create_refresh_token(self, user_payload: UserPayloadSchema) -> str:
        payload = CreateTokenPayloadSchema(
            type=TokenTypeEnum.ACCESS_TOKEN,
            sub=user_payload.id,
            name=user_payload.name,
            email=user_payload.email,
            role=user_payload.role,
        )

        return self._encode_jwt(
            payload=payload,
            expire_minutes=self._expire_minutes,
            expire_timedelta=self._expire_days,
        )

    def _encode_jwt(
            self,
            payload: CreateTokenPayloadSchema,
            expire_minutes: int,
            expire_timedelta: timedelta | None = None
    ):
        now = datetime.now(UTC)

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode: TokenPayloadSchema = TokenPayloadSchema(
            **payload.model_dump(mode='json'),
            exp=expire,
            iat=now,
            jti=str(uuid.uuid4()),
        )

        encoded = jwt.encode(
            payload=to_encode.model_dump(mode='json'),
            key=self._private_key,
            algorithm=self._algorithm,
        )
        return encoded

    def _decode_jwt(self, token: str | bytes) -> TokenPayloadSchema:
        decoded = jwt.decode(
            token=token,
            key=self._public_key,
            algorithms=[self._algorithm],
        )
        return decoded


__all__ = ["JwtService"]
