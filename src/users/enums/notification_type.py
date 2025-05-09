import enum

class NotificationTypeEnum(str, enum.Enum):
    DISABLED = "disabled"
    ME = "me"
    AGENT = "agent"
    ME_AND_AGENT = "me_and_agent"