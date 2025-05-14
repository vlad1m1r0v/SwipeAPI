import enum


class UserRoleEnum(str, enum.Enum):
    BUILDER = "builder"
    USER = "user"
    ADMIN = "admin"


class NotificationTypeEnum(str, enum.Enum):
    DISABLED = "disabled"
    ME = "me"
    AGENT = "agent"
    ME_AND_AGENT = "me_and_agent"


__all__ = ["UserRoleEnum", "NotificationTypeEnum"]
