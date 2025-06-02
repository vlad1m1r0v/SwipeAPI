import enum


class TokenType(str, enum.Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"
