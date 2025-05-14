import enum


class TokenTypeEnum(str, enum.Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

__all__ = ["TokenTypeEnum"]