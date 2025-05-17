import enum


class ROLE(str, enum.Enum):
    BUILDER = "builder"
    USER = "user"
    ADMIN = "admin"


class NOTIFICATION_TYPE(str, enum.Enum):
    DISABLED = "disabled"
    ME = "me"
    AGENT = "agent"
    ME_AND_AGENT = "me_and_agent"


__all__ = ["ROLE", "NOTIFICATION_TYPE"]
