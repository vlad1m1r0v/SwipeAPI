import uuid
from datetime import timedelta, datetime, UTC

import jwt

from config import Config
from src.auth.enums import TokenType
from src.auth.schemas import (
    BasePayloadSchema,
    PayloadWithTypeSchema,
    PayloadWithExpDateSchema
)


class JwtService:
    def __init__(self, config: Config):
        self._public_key = config.jwt.public_key_path.read_text()
        self._private_key = config.jwt.private_key_path.read_text()
        self._algorithm = config.jwt.algorithm
        self._expire_minutes: int = config.jwt.access_token_expire_minutes
        self._expire_days = timedelta(days=config.jwt.refresh_token_expire_days)

    def create_access_token(self, base_payload: BasePayloadSchema) -> str:
        payload = PayloadWithTypeSchema(
            type=TokenType.ACCESS_TOKEN,
            sub=str(base_payload.id),
            name=base_payload.name,
            email=base_payload.email,
            role=base_payload.role,
        )

        return self.encode_jwt(payload=payload, expire_minutes=self._expire_minutes)

    def create_refresh_token(self, base_payload: BasePayloadSchema) -> str:
        payload = PayloadWithTypeSchema(
            type=TokenType.REFRESH_TOKEN,
            sub=str(base_payload.id),
            name=base_payload.name,
            email=base_payload.email,
            role=base_payload.role,
        )

        return self.encode_jwt(
            payload=payload,
            expire_minutes=self._expire_minutes,
            expire_timedelta=self._expire_days,
        )

    def encode_jwt(
            self,
            payload: PayloadWithTypeSchema,
            expire_minutes: int,
            expire_timedelta: timedelta | None = None
    ):
        now = datetime.now(UTC)

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode: PayloadWithExpDateSchema = PayloadWithExpDateSchema(
            **payload.model_dump(mode='json'),
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
            jti=str(uuid.uuid4()),
        )

        encoded = jwt.encode(
            payload=to_encode.model_dump(mode='json'),
            key=self._private_key,
            algorithm=self._algorithm,
        )
        return encoded

    def decode_jwt(self, token: str | bytes) -> dict:
        decoded = jwt.decode(
            jwt=token,
            key=self._public_key,
            algorithms=[self._algorithm],
        )
        return decoded


__all__ = ["JwtService"]