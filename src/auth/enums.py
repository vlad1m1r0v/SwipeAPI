import enum


class TOKEN_TYPE(str, enum.Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

__all__ = ["TOKEN_TYPE"]