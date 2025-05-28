from itsdangerous import URLSafeTimedSerializer

from config import Config


class SignService:
    def __init__(self, config: Config):
        self._serializer = URLSafeTimedSerializer(
            secret_key=config.sign.sign_secret,
            salt=config.sign.sign_salt
        )
        self._seconds = config.sign.expire_seconds

    def encode(self, data: dict) -> str:
        return self._serializer.dumps(data)

    def decode(self, token: str) -> dict:
        return self._serializer.loads(token, max_age=self._seconds)
